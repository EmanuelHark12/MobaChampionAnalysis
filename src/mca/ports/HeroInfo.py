from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
from dotenv import load_dotenv
import os
import requests

class HeroInfo:

    def __init__(self):
        load_dotenv()
            
            # Configuração segura com fallback
        self.base_url = os.getenv("HERO_INFO_URL")
    
    

    def get_hero_stats(self,champion:str):
        hero_url = self.base_url + "/hero/stats"
        body = {"hero_name":champion}
        response = requests.post(hero_url,json=body)
        response.raise_for_status()
        data = response.json()
        return data