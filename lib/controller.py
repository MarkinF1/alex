from collections import namedtuple

from yaml import load, SafeLoader

from lib.logger import logger
from lib.base_classes.singleton import SingletonMetaClass


class Controller(metaclass=SingletonMetaClass):
    _recognizer_config = namedtuple('Recognizer', ['language', 'model_path', 'online'])
    _assistant_config = namedtuple('Assistant', ['name', 'sex', 'speech_language'])

    def __init__(self):
        try:
            with open('./config.yml', 'r') as config_file:
                CONFIG = load(config_file, SafeLoader)
                self.version: str = CONFIG['version']
                self.recognizer_config: Controller._recognizer_config = self._recognizer_config(**CONFIG['recognizer'])
                self.assistant_config: Controller._assistant_config = self._assistant_config(**CONFIG['assistant'])

        except Exception as exp:
            logger.error(f"Произошла ошибка при считывании конфига. Прекращение работы. \n{exp}")
            exit(1)


if __name__ == "__main__":
    s = Controller()
    print(s)
    s1 = Controller()
    print(s1)
