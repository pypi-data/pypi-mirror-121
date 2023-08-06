import os

import transformers

from vtorch.models.model import IModel


class InitializationDistillModelPipeline:
    def __init__(
        self,
        teacher_model: IModel,
        reduction: int,
        save_folder: str = "results",
        teacher_base_model_attr: str = "_base_model",
    ):
        """
        Parameters
        ----------
        teacher_model: IModel, teacher model
        reduction: the factor of reduction the children model's size
            (e.g with reduction=2 6-layer student would be initialized from the 12-layer teacher)
        save_folder: str (default = "results") folder to store student
        teacher_base_model_attr: str (default = "_base_model") attribute of base model (e.g Transformer) whose
            parameters will be used for initialization
        """
        self.teacher_model = teacher_model
        self.reduction = reduction
        self.save_folder = save_folder
        self.teacher_base_model_attr = teacher_base_model_attr

    def run(self, experiment_name: str) -> None:

        # TODO: classification head initialization

        config_py = experiment_name
        no_py_extension = 0
        no_config_root_folder = slice(1, None)
        results_subfolder_hierarchy = os.path.splitext(
            os.path.sep.join(config_py.split(os.path.sep)[no_config_root_folder])
        )[no_py_extension]
        save_folder = str(os.path.join(self.save_folder, results_subfolder_hierarchy))
        os.makedirs(save_folder, exist_ok=True)

        teacher_base_model = getattr(self.teacher_model, self.teacher_base_model_attr)
        teacher_config = teacher_base_model.config
        teacher_config.num_hidden_layers = teacher_config.num_hidden_layers // self.reduction

        student_base_model = getattr(transformers, teacher_base_model.__class__.__name__)(teacher_config)

        student_base_model_state_dict = student_base_model.state_dict()
        teacher_base_model_state_dict = teacher_base_model.state_dict()

        for student_key in student_base_model_state_dict.keys():
            # like "encoder.layer.4.attention.self.query.weight" -> "encoder.layer.9.attention.self.query.weight"
            teacher_key = ".".join(
                str((int(substring) * 2) + 1) if substring.isdigit() else substring
                for substring in student_key.split(".")
            )
            student_base_model_state_dict[student_key] = teacher_base_model_state_dict[teacher_key]

        student_base_model.load_state_dict(student_base_model_state_dict)

        setattr(self.teacher_model, self.teacher_base_model_attr, student_base_model)

        self.teacher_model.save(save_folder)
