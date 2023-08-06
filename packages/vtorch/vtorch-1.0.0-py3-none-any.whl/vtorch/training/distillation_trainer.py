import logging
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import torch
from clearml import Task
from torch.cuda.amp import GradScaler
from torch.nn.modules.loss import _Loss
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.nn import utils as nn_util

from ..data.entity import InstanceFeatureVectors  # noqa: F401
from ..data.iterators.base import DataIterator
from ..metrics import Metric
from ..models.model import IModel
from .trainer import Trainer

logger = logging.getLogger(__name__)


class DistillationTrainer(Trainer):
    def __init__(
        self,
        student_model: IModel,
        teacher_model: torch.nn.Module,  # as teacher model will not be saved, there is no need to use IModel
        optimizer: torch.optim.Optimizer,  # type: ignore
        metrics: Dict[str, Metric],
        label_keys: Tuple[str, Union[str, List[str]]],
        iterator: DataIterator,
        train_dataset: Iterable[InstanceFeatureVectors],
        num_epochs: int,
        shuffle: bool = True,
        validation_dataset: Optional[Iterable[InstanceFeatureVectors]] = None,
        validation_iterator: Optional[DataIterator] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric_name: str = "loss",
        early_stopping_metric_should_decrease: bool = True,
        accumulation_steps: int = 1,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        lr_scheduler: Optional[_LRScheduler] = None,  # type: ignore
        scaler: Optional[GradScaler] = None,
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        run_validation_each_global_steps: Optional[int] = None,
        clearml_task: Optional[Task] = None,
        seed: int = 12,
        comparison_loss: Optional[_Loss] = None,
        logits_postprocessing: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        comparison_loss_weight: float = 0.5,
    ) -> None:

        super().__init__(
            model=student_model,
            optimizer=optimizer,
            metrics=metrics,
            iterator=iterator,
            train_dataset=train_dataset,
            num_epochs=num_epochs,
            shuffle=shuffle,
            validation_dataset=validation_dataset,
            validation_iterator=validation_iterator,
            early_stopping=early_stopping,
            patience=patience,
            label_keys=label_keys,
            accumulation_steps=accumulation_steps,
            cuda_device=cuda_device,
            grad_norm=grad_norm,
            lr_scheduler=lr_scheduler,
            early_stopping_metric_name=early_stopping_metric_name,
            early_stopping_metric_should_decrease=early_stopping_metric_should_decrease,
            seed=seed,
            scaler=scaler,
            gradual_unfreezing_steps=gradual_unfreezing_steps,
            run_validation_each_global_steps=run_validation_each_global_steps,
            clearml_task=clearml_task,
        )

        self.teacher_model = teacher_model
        self.teacher_model.eval()
        self.comparison_loss_weight = comparison_loss_weight
        if comparison_loss is None:
            logger.warning("No `comparison loss was given to a trainer. Defaulting to `torch.nn.MSELoss()`")
            comparison_loss = torch.nn.MSELoss()
        self.comparison_loss = comparison_loss
        self.logits_postprocessing = logits_postprocessing

    def _batch_outputs_and_loss(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Sequence[torch.Tensor]:
        # to not scale by self.accumulation_steps loss twice
        accumulation_steps = 0
        if self.accumulation_steps > 1:
            accumulation_steps = self.accumulation_steps
            self.accumulation_steps = 0
        logits_student, loss = super(DistillationTrainer, self)._batch_outputs_and_loss(batch_group=batch_group)
        if accumulation_steps > 1:
            self.accumulation_steps = accumulation_steps

        logits_teacher = self._teacher_forward(batch_group)

        if self.logits_postprocessing is not None:
            logits_student = self.logits_postprocessing(logits_student)
            logits_teacher = self.logits_postprocessing(logits_teacher)

        loss_comparison = self.comparison_loss(logits_student, logits_teacher)

        loss = self.comparison_loss_weight * loss_comparison + (1 - self.comparison_loss_weight) * loss

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return logits_student, loss

    def _teacher_forward(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> torch.Tensor:
        if len(batch_group) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0]
        batch = nn_util.move_to_device(batch, self._cuda_devices[0])

        with torch.no_grad():  # no autocast here
            model_outputs, _ = self.model(**batch)

        return model_outputs
