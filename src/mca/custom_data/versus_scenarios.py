from kedro.io import AbstractDataset
from kedro_datasets.partitions import PartitionedDataset
from typing import Any, Dict, Union

import pandas as pd
import re
from collections import defaultdict
from pathlib import Path
import glob

class VersusScenarios(AbstractDataset):
    def __init__(self, partitioned_dataset: Union[PartitionedDataset, dict]):
        """Initialize with either a PartitionedDataset object or config dict"""
        print(f"Raw config received: {partitioned_dataset}")
        #print(f"Raw config received - path: {partitioned_dataset.path}")
        # Handle both dictionary config and PartitionedDataset object
        if isinstance(partitioned_dataset, PartitionedDataset):
            #self._path = partitioned_dataset.path
            self._path = partitioned_dataset._path
            self._dataset_config = partitioned_dataset._dataset_config
            self._dataset = partitioned_dataset
        elif isinstance(partitioned_dataset, dict):
            self._path = partitioned_dataset['path']
            self._dataset_config = partitioned_dataset.get('dataset', {})
            self._dataset = PartitionedDataset(
                path=self._path,
                dataset=self._dataset_config
            )
        else:
            raise TypeError(f"Expected PartitionedDataset or dict, got {type(partitioned_dataset)}")

    def _load(self) -> Dict[str, pd.DataFrame]:
        result = {}
        final_path = Path(self._path).resolve().parents[3] / self._path
        #print(self._path)
        #print(Path(self._path).parent)
        #print(Path(self._path).resolve().parents[0])
        #print(Path(self._path).resolve().parents[3])

        #print(Path(self._path).resolve().parents[3]).glob("*_scenarios.csv"))
        #print([csv_file for csv_file in Path(self._path).resolve().parents[0].glob("*_scenarios.csv")])
        #Path(self._path).glob
        #Path(self._path).resolve().parents[0]
        for csv_file in final_path.glob("*_scenarios.csv"):
            year = csv_file.stem.split("_")[0]
            df = pd.read_csv(csv_file, **self._dataset_config.get("load_args", {}))
            if year in result:
                result[year].append(df)
            else:
                result[year] = [df]
        
        return {year: pd.concat(dfs) for year, dfs in result.items()}
    def _loaded_(self) -> Dict[str, pd.DataFrame]:
        partitions = self._dataset.load()
        print(partitions)
        if not partitions:
            raise DatasetError(f"No partitions found in '{self._path}'. Expected files like '2014_scenarios.csv'")
        
        result = {}
        for filename, dataset in partitions.items():
            year = filename.split("_")[0]  # Extrai o ano do nome do arquivo
            df = dataset.load()  # Carrega o DataFrame diretamente
            if year in result:
                result[year].append(df)
            else:
                result[year] = [df]
        
        # Concatena todos os DataFrames do mesmo ano
        return {year: pd.concat(dfs) for year, dfs in result.items()}
    def _load__(self) -> Dict[str, pd.DataFrame]:
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
                    result[match.group(1)].append(df)
                else:
                    raise TypeError(f"Esperado método bound de CSVDataset, mas recebi: {type(partition_dataset)}")
                print(f"Loaded DataFrame shape: {df.shape}")
                result[match.group(1)].append(df)
        
        return {year: pd.concat(dfs) for year, dfs in result.items()}

    def _save(self, data: Dict[str, pd.DataFrame]) -> None:
        for scenario, df in data.items():
            # Salva cada cenário em uma subpasta separada
            partition_path = f"{scenario}_scenarios.csv"
            full_path = str(Path(self._path) / partition_path)
            
            dataset = self._partitioned_dataset._dataset_type(
                filepath=full_path,
            #    **self._dataset_config
            )
            dataset.save(df)

    def _describe(self) -> Dict:
        return {
            "path": self._path,
            "dataset_type": "versus_scenario_partitions",
            "description": "Versus scenarios partitioned by scenario type"
        }