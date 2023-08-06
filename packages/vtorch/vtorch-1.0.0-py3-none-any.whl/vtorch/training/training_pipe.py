import math
import os
from typing import Callable, Iterable, Optional

from clearml import Task
from transformers import PretrainedConfig

from vtorch.common.checks import ConfigurationError
from vtorch.common.persistance import Persistent
from vtorch.training import Trainer
from vtorch.training.callbacks import EarlyStopping


class TrainingPipeline:
    def __init__(
        self,
        project_name: str,
        trainer: Trainer,
        vectorizer: Persistent,  # TODO: to Vectorizer in the future, for the MultipleVectorizerContainer usage for now
        save_folder: str = "results",
        log_by_language: bool = True,
        language_subfolder_depth_id: Optional[int] = None,
    ) -> None:
        self.project_name = project_name
        self.trainer = trainer
        self.vectorizer = vectorizer
        self.save_folder = save_folder
        self.log_by_language = log_by_language
        self.language_subfolder_depth_id = language_subfolder_depth_id

    def run(self, experiment_name: str, experiment_name_suffix: str = "") -> None:

        config_py = experiment_name
        no_py_extension = 0
        no_config_root_folder = slice(1, None)
        results_subfolder_hierarchy = (
            os.path.splitext(os.path.sep.join(config_py.split(os.path.sep)[no_config_root_folder]))[no_py_extension]
            + "_"
            + experiment_name_suffix
        )

        save_folder = str(os.path.join(self.save_folder, results_subfolder_hierarchy))
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        experiment_tags = ["vtorch_3.0"]
        if self.log_by_language:
            if self.language_subfolder_depth_id is None:
                raise ConfigurationError(
                    "To use logging by language provide 'language_subfolder_depth_id'"
                    " argument during the initialization"
                )
            experiment_config_path = config_py.split(os.path.sep)
            language = "lang_" + experiment_config_path[self.language_subfolder_depth_id]
            experiment_tags.append(language)

        clearml_task = Task.init(
            project_name=self.project_name,
            task_name=results_subfolder_hierarchy.replace(os.path.sep, "_"),
            auto_resource_monitoring=True,
            auto_connect_arg_parser=True,
            auto_connect_frameworks={"pytorch": True},
        )
        clearml_task.set_resource_monitor_iteration_timeout(1e9)
        clearml_task.add_tags(experiment_tags)
        self._log_hyperparameters_template_method(clearml_task)
        clearml_task.upload_artifact(name="config", artifact_object=config_py)
        self.trainer.set_clearml_task(clearml_task=clearml_task)

        model = self.trainer.train()
        for obj, subfolder in (model, "model"), (self.vectorizer, "vectorizer"):
            obj_save_folder = os.path.join(save_folder, subfolder)
            if not os.path.exists(obj_save_folder):
                os.mkdir(obj_save_folder)
            obj.save(obj_save_folder)

    def _log_hyperparameters_template_method(self, clearml_task: Task) -> None:
        for log_hyperparameters in self._log_methods:
            log_hyperparameters(clearml_task)

    @property
    def _log_methods(self) -> Iterable[Callable[[Task], None]]:
        return [
            self._log_model_hyperparameters,
            self._log_optimization_hyperparameters,
            self._log_dataset_hyperparameters,
            self._log_trainer_hyperparameters,
        ]

    def _log_model_hyperparameters(self, clearml_task: Task) -> None:
        serializable_params = {}
        if hasattr(self.trainer.model, "config") and isinstance(self.trainer.model.config, PretrainedConfig):
            serializable_params = self.trainer.model.config.to_dict()
        clearml_task.connect({"model_class": self.trainer.model.__class__.__name__, **serializable_params})

    def _log_optimization_hyperparameters(self, clearml_task: Task) -> None:
        defaults = {
            f"optimizer_initial_param_{name}": value
            for name, value in getattr(self.trainer.optimizer, "defaults", {}).items()
        }
        clearml_task.connect(
            {
                "optimizer": self.trainer.optimizer.__class__.__name__,
                "scheduler": None
                if self.trainer.lr_scheduler is None
                else self.trainer.lr_scheduler.__class__.__name__,
                "grad_norm": getattr(self.trainer, "grad_norm", None),  # TODO: in order to create more general trainer
                **defaults,
            }
        )

    def _log_dataset_hyperparameters(self, clearml_task: Task) -> None:
        get_num_train_instances = getattr(self.trainer.train_data, "__len__", None)
        get_num_validation_instances = getattr(self.trainer.validation_data, "__len__", None)

        if get_num_train_instances is not None:
            num_train_instances = get_num_train_instances()
            train_batch_size: Optional[int] = math.ceil(
                num_train_instances / self.trainer.iterator.get_num_batches(self.trainer.train_data)
            )
        else:
            num_train_instances = None
            train_batch_size = None

        num_validation_instances = None if get_num_validation_instances is None else get_num_validation_instances()

        clearml_task.connect(
            {
                "train_iterator_class": self.trainer.iterator.__class__.__name__,
                "train_batch_size": train_batch_size,
                "validation_iterator_class": self.trainer.validation_iterator.__class__.__name__,
                "num_train_instances": num_train_instances,
                "num_validation_instances": num_validation_instances,
                "shuffle": getattr(self.trainer, "shuffle", None),  # TODO: in order to create more general trainer
            }
        )

    def _log_trainer_hyperparameters(self, clearml_task: Task) -> None:
        if isinstance(self.trainer.early_stopping_configuration, EarlyStopping):
            clearml_task.connect(self.trainer.early_stopping_configuration)

        clearml_task.connect(
            {
                "num_epochs": getattr(self.trainer, "num_epochs", None),
                "accumulation_steps": getattr(self.trainer, "accumulation_steps", None),
                "gradual_unfreezing_steps": getattr(self.trainer, "gradual_unfreezing_steps", None),
            }
        )
