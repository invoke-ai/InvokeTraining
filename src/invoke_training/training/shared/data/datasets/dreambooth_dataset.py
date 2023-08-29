import random
import typing

import torch.utils.data

from invoke_training.training.shared.data.datasets.image_dir_dataset import (
    ImageDirDataset,
)


class DreamBoothDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        instance_dataset: ImageDirDataset,
        instance_prompt: str,
        class_dataset: typing.Optional[ImageDirDataset] = None,
        class_prompt: typing.Optional[str] = None,
        prior_preservation_loss_weight: int = 1.0,
        balance_datasets: bool = True,
        shuffle: bool = True,
    ):
        super().__init__()

        self._instance_dataset = instance_dataset
        self._instance_prompt = instance_prompt
        self._class_dataset = class_dataset
        self._class_prompt = class_prompt
        self._prior_preservation_loss_weight = prior_preservation_loss_weight

        # Calculate the *target* size (after rebalancing) of the instance and class datasets respectively.
        self._balanced_instance_dataset_size = len(self._instance_dataset)
        self._balanced_class_dataset_size = len(self._class_dataset) if self._class_dataset is not None else 0
        if balance_datasets and self._class_dataset is not None:
            self._balanced_instance_dataset_size = max(len(self._instance_dataset), len(self._class_dataset))
            self._balanced_class_dataset_size = max(len(self._instance_dataset), len(self._class_dataset))

        # Shuffle the dataset ordering.
        self._shuffle_map = list(range(self._balanced_instance_dataset_size + self._balanced_class_dataset_size))
        if shuffle:
            random.shuffle(self._shuffle_map)

    def _get_unshuffled_example(self, idx: int):
        if idx < self._balanced_instance_dataset_size:
            example = self._instance_dataset[idx % len(self._instance_dataset)]
            example["caption"] = self._instance_prompt
            example["loss_weight"] = 1.0
            return example
        elif idx < self._balanced_instance_dataset_size + self._balanced_class_dataset_size:
            example = self._class_dataset[(idx - self._balanced_instance_dataset_size) % len(self._class_dataset)]
            example["caption"] = self._class_prompt
            example["loss_weight"] = self._prior_preservation_loss_weight
            return example
        else:
            raise IndexError(
                f"Index '{idx}' is out of range for DreamBoothDataset of size {self._balanced_instance_dataset_size} + "
                f"{self._balanced_class_dataset_size} = "
                f"{self._balanced_instance_dataset_size + self._balanced_class_dataset_size}"
            )

    def __len__(self) -> int:
        return self._balanced_instance_dataset_size + self._balanced_class_dataset_size

    def __getitem__(self, idx: int) -> typing.Dict[str, typing.Any]:
        return self._get_unshuffled_example(self._shuffle_map[idx])