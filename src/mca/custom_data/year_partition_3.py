from kedro.io import AbstractDataset
from typing import Dict, Any
from collections import defaultdict
import re
import pandas as pd
from kedro.io import DataCatalog
from kedro_datasets.partitions.partitioned_dataset import PartitionedDataset
from kedro.config import OmegaConfigLoader

class YearPartitionsDataset(AbstractDataset):
    #def __init__(self, partitioned_dataset: str | AbstractDataset, catalog: DataCatalog = None):
    #    """Decora um PartitionedDataset existente para extrair anos."""
    #    if isinstance(partitioned_dataset, str):
    #        if catalog is None:
    #            # Try to get default catalog if not provided
    #           conf_loader = OmegaConfigLoader("conf/base")
    #            catalog_config = conf_loader["catalog"]
    #            catalog = DataCatalog.from_config(catalog_config)
    #        self._dataset = catalog._get_dataset(partitioned_dataset)
    #    else:
    #        self._dataset = partitioned_dataset
    def __init__(self, partitioned_dataset: dict | AbstractDataset):
        """Initialize with either config dict or instantiated dataset"""
        if isinstance(partitioned_dataset, dict):
            # Create new instance to avoid recursion
            self._dataset = PartitionedDataset(**partitioned_dataset)
        else:
            self._dataset = partitioned_dataset
    def _load(self) -> Dict[str, Any]:
        partitions = self._dataset.load()
        print(partitions)
        result = defaultdict(list)

        for partition_key, dataset in partitions.items():
            match = re.match(r'^(\d{4})', partition_key)
            if match:
                year = match.group(1)
                df = dataset.load()
                result[year].append(df)
            else:
                raise ValueError(f"Partição '{partition_key}' inválida. Esperado prefixo com ano.")

        return {year: pd.concat(dfs, ignore_index=True) for year, dfs in result.items()}

    def _save(self, data: Any) -> None:
        raise NotImplementedError("Somente leitura")

    def _describe(self) -> Dict[str, Any]:
        return {"partitions": "Extração de anos dos datasets particionados"}