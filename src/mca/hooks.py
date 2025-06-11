from kedro.framework.hooks import hook_impl
from dotenv import load_dotenv
import os

class EnvHook:
    @hook_impl
    def before_pipeline_run(self):
        load_dotenv(".env")

# src/mca/hooks.py ou outro local apropriado
from kedro.io import DataCatalog
from kedro.framework.hooks import hook_impl
from mca.src.mca.custom_data.year_partition import YearPartitionsDataset

class CatalogRegistrationHooks:
    @hook_impl
    def register_catalog(self, catalog: DataCatalog) -> DataCatalog:
        partitioned_dataset = catalog._get_dataset("LolHistoric")
        year_partitioned_dataset = YearPartitionsDataset(partitioned_dataset)
        catalog.add("lol_historic_years", year_partitioned_dataset)
        return catalog

