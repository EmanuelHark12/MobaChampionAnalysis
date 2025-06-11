# src/mca/catalog.py
from pathlib import Path
import os

from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog
from kedro_datasets.partitions.partitioned_dataset import PartitionedDataset
from mca.src.mca.custom_data.year_partition import YearPartitionsDataset
#from mca.custom_data.year_partition import YearPartitionsDataset
# Caminho base do projeto
base_path = Path(__file__).resolve().parents[2]  # src/mca/
conf_path = base_path / "conf" / "base"
#conf_path = "conf/base"
# Carrega configs
conf_loader = OmegaConfigLoader(str(conf_path))
catalog_config = conf_loader["catalog"]
catalog = DataCatalog.from_config(catalog_config)

# Adiciona dataset customizado
partitioned_dataset = catalog._get_dataset("LolHistoric")
catalog.add("lol_historic_years", YearPartitionsDataset(partitioned_dataset))
