from collections import namedtuple

from yaml import load, SafeLoader

from lib.logger import logger
from lib.base_classes.singleton import SingletonMetaClass


class Controller(metaclass=SingletonMetaClass):
    _recognizer = namedtuple('Recognizer', ['language', 'model_path', 'online'])
    _assistant = namedtuple('Assistant', ['name', 'sex', 'speech_language'])

    def __init__(self):
        try:
            with open('./config.yml', 'r') as config_file:
                CONFIG = load(config_file, SafeLoader)
                self.version: str = CONFIG['version']
                self.recognizer: Controller._recognizer = self._recognizer(**CONFIG['recognizer'])
                self.assistant: Controller._assistant = self._assistant(**CONFIG['assistant'])

        except Exception as exp:
            logger.error(f"Произошла ошибка при считывании конфига. Прекращение работы. \n{exp}")
            exit(1)


if __name__ == "__main__":
    s = Controller()
    print(s)
    s1 = Controller()
    print(s1)
