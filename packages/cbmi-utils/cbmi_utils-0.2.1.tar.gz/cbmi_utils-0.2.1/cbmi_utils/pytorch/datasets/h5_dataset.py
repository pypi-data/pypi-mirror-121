from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import h5py
import numpy as np
from torch.utils.data import Dataset


class H5Dataset(Dataset):
    """
    Basic datset class for handling h5 files. Do not call this class directly.
    """
    def __init__(self, data_path: str, data_key: str, target_path: str, target_key: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        data_path = Path(data_path)
        target_path = Path(target_path)

        self.samples = h5py.File(data_path, 'r')[data_key]
        self.targets = h5py.File(target_path, 'r')[target_key]

        self.targets = np.squeeze(self.targets).tolist()
        self.classes = list(set(self.targets))
        self.transform = transform
        self.transform_target = transform_target

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        sample = self.samples[index]
        target = self.targets[index]

        if self.transform is not None:
            sample = self.transform(sample)

        if self.transform_target is not None:
            target = self.transform_target(target)

        return sample, target

    def __len__(self) -> int:
        return len(self.targets)
