import math
import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import TypeAdapter

from invoke_training.config.optimizer.optimizer_config import AdamOptimizerConfig
from invoke_training.config.pipeline_config import PipelineConfig
from invoke_training.pipelines.invoke_train import train


@dataclass
class Override:
    base_output_prefix: str
    batch_size: int

    def get_base_output_dir(self):
        return os.path.join(self.base_output_prefix, f"bs_{self.batch_size}")

    def apply(self, config: PipelineConfig):
        config.base_output_dir = self.get_base_output_dir()
        config.optimizer = AdamOptimizerConfig()
        config.train_batch_size = self.batch_size


def run_training(base_config_path, override: Override, dataset_size: int):
    with open(base_config_path, "r") as f:
        cfg = yaml.safe_load(f)

    pipeline_adapter: TypeAdapter[PipelineConfig] = TypeAdapter(PipelineConfig)
    train_config = pipeline_adapter.validate_python(cfg)

    override.apply(train_config)

    target_steps = 2000
    min_epochs = 10
    max_epochs = 300
    steps_per_epoch = math.ceil(dataset_size / train_config.train_batch_size)
    target_num_epochs = math.ceil(target_steps / steps_per_epoch)
    num_epochs = min(max(target_num_epochs, min_epochs), max_epochs)

    validate_every_n_epochs = num_epochs // 10  # Validate at 10 checkpoints.
    train_config.max_train_epochs = num_epochs
    train_config.save_every_n_epochs = 5000  # Intentionally high so that we don't save checkpoints to save disk space.
    train_config.validate_every_n_epochs = validate_every_n_epochs  # Generate validation images often.

    print(f"Max train epochs: {train_config.max_train_epochs}")
    print(f"Validate every n epochs: {train_config.validate_every_n_epochs}")

    train(train_config)


def main():
    base_config_path = Path(__file__).parent / "configs/sdxl_lora_avp_1x24gb.yaml"
    name_prefix = "output/hp_tuning/sdxl_avp_1x24gb/"
    dataset_size = 16

    run_overrides = [
        Override(base_output_prefix=name_prefix, batch_size=4),
        Override(base_output_prefix=name_prefix, batch_size=1),
    ]

    for override in run_overrides:
        run_training(base_config_path, override, dataset_size)


if __name__ == "__main__":
    main()