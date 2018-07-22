from dotenv import load_dotenv
from enum import Enum, unique
from os import getcwd, getenv, path


class Config:
    config = None

    @classmethod
    def get(cls, config_enum):
        if cls.config is None:
            cls.load()

        return cls.config[config_enum]

    @classmethod
    def set(cls, config_enum, value):
        if cls.config is None:
            cls.load()

        cls.config[config_enum] = value

    @classmethod
    def load(cls):
        """ Loads or reloads configuration from environment variables
        """
        env_path = path.join(getcwd(), '.env')
        load_dotenv(dotenv_path=env_path, verbose=True)

        cls.config = {k: getenv(cls.get_env_name(k))
                      for k in ConfigKey}

    @classmethod
    def get_env_name(cls, config_enum):
        return "MN_SOS_SCRAPER_%s" % config_enum.value


@unique
class ConfigKey(Enum):
    URL = 'URL'
    OUTPUT_FILE = 'OUTPUT_FILE'
