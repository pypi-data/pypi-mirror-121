from dataclasses import dataclass, field
from mlplatform_lib.dataclass.experiment.type import ExperimentType
from mlplatform_lib.dataclass.model.type import ModelStatus


@dataclass
class ModelDto:
    id: int = field(init=False, default=0)
    experiment_type: ExperimentType = field(init=False)
    model_path: str
