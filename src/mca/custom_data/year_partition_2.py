from kedro.io import AbstractDataset
from kedro_datasets.partitions import PartitionedDataset
from typing import Any, Dict

import pandas as pd
import re
from collections import defaultdict

class YearPartitionsDataset(AbstractDataset):
    def __init__(self, partitioned_dataset: dict):
        """Initialize with validated config"""
        # Print raw input for debugging
        print(f"Raw config received: {partitioned_dataset}")
        
        # Extract and validate config
        self._path = partitioned_dataset['path']
        self._dataset_config = partitioned_dataset.get('dataset', {})
        
        # Initialize partitioned dataset
        self._dataset = PartitionedDataset(
            path=self._path,
            dataset=self._dataset_config
        )
        
        # Debug print final dataset config
        print(f"Initialized PartitionedDataset: {self._dataset}")
        print(f"Dataset type: {type(self._dataset)}")
        print(f"Dataset config: {self._dataset._dataset_config}")

    def _load(self) -> Dict[str, pd.DataFrame]:
        partitions = self._dataset.load()
        print(f"Found partitions: {list(partitions.keys())}")
        
        # Rest of your loading logic...
        result = defaultdict(list)
        for partition_key, partition_dataset in partitions.items():
            print(f"Processing partition: {partition_key}")
            print(f"Partition: {partition_dataset}")
            match = re.match(r'^(\d{4})', partition_key)
            if match:
                if callable(partition_dataset) and hasattr(partition_dataset, "__self__"):
                    df = partition_dataset.__self__.load()
                    print(df.head(5))
                    result[match.group(1)].append(df)
                else:
                    raise TypeError(f"Esperado método bound de CSVDataset, mas recebi: {type(partition_dataset)}")
                print(f"Loaded DataFrame shape: {df.shape}")
                result[match.group(1)].append(df)
        
        return {year: pd.concat(dfs) for year, dfs in result.items()}

    def _save(self, data) -> None:
        raise NotImplementedError("Read-only dataset")

    def _describe(self) -> dict:
        return {"description": "Groups partitioned data by year"}