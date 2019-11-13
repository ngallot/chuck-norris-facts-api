from app.config import ConfigLoader, ChuckNorrisApiConfig

__version__ = '1.0.0'
config: ChuckNorrisApiConfig = ConfigLoader.load_config(ChuckNorrisApiConfig)