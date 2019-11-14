import configparser
import os
import importlib
from typing import Type


class AppConfig:
    _debug: bool
    _description: str
    _name: str

    def __init__(self, debug: bool, description: str, name: str):
        self._debug = debug
        self._description = description
        self._name = name

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def description(self) -> str:
        return self._description

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def from_config_section(cls, config: configparser.ConfigParser, section_name: str):
        data = dict(
            name=config.get(section=section_name, option='name'),
            description=config.get(section=section_name, option='description'),
            debug=config.getboolean(section=section_name, option='debug')
        )
        return cls(**data)


class LoggingConfig:

    def __init__(self, level: str, format: str):
        self._level = level
        self._format = format

    @property
    def level(self):
        return self._level

    @property
    def format(self):
        return self._format

    @classmethod
    def from_config_section(cls, config: configparser.ConfigParser, section_name: str):
        data = dict(
            level=config.get(section=section_name, option='level'),
            format=config.get(section=section_name, option='format')
        )
        return cls(**data)


class ChuckNorrisApiConfig:
    _app_config: AppConfig
    _logging_config: LoggingConfig

    def __init__(self, app_config: AppConfig, logging_config: LoggingConfig):
        self._app_config = app_config
        self._logging_config = logging_config

    @property
    def app_config(self) -> AppConfig:
        return self._app_config

    @property
    def logging_config(self) -> LoggingConfig:
        return self._logging_config

    @classmethod
    def from_config(cls, config: configparser.ConfigParser):
        return cls(**dict(
            app_config=AppConfig.from_config_section(config=config, section_name='APP'),
            logging_config=LoggingConfig.from_config_section(config=config, section_name='LOGGING')
        ))


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


class ConfigLoader:
    _allowed_envs = ['test', 'local', 'development', 'staging', 'production']

    @staticmethod
    def _get_config_file_path():
        env = os.getenv('ENV', None)
        if not env:
            raise Exception('Environment variable ENV not set')
        elif env.lower() not in ConfigLoader._allowed_envs:
            raise Exception(f"Unknown environment {env}. It should be one of {', '.join(ConfigLoader._allowed_envs)}")
        else:
            lower_env = env.lower()
            return 'tests/resources/config/test.ini' if lower_env =='test' else f'/app/config/{lower_env}.ini'

    @staticmethod
    def load_config(t: Type):
        try:
            config: configparser.ConfigParser = configparser.ConfigParser(os.environ, interpolation=EnvInterpolation())
            config.read(ConfigLoader._get_config_file_path())
        except Exception as e:
            raise Exception(f'Unable to load configuration: {e}')
        try:
            module_name = globals()['__name__']
            module = importlib.import_module(module_name)
            target_class = getattr(module, t.__name__)
        except Exception as e:
            raise Exception(f'Unable to load class {t.__name__} from module {module_name}: {e}')
        return target_class.from_config(config=config)
