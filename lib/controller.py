from logger import logger
from lib.base_classes.singleton import SingletonMetaClass


class Controller(metaclass=SingletonMetaClass):
    def __init__(self):
        logger.info("Объект Controller создан.")


if __name__ == "__main__":
    s = Controller()
    print(s)
    s1 = Controller()
    print(s1)
