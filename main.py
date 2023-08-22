from lib.logger import logger
from lib.voice.recognizer import Recognizer


class Alex:
    def __init__(self):
        self.recognizer = Recognizer()
        self.speaker = None

    def run(self):
        from time import sleep

        while True:
            logger.debug(f"Текст: {self.recognizer.run()}")
            # sleep(2)


if __name__ == '__main__':
    alex = Alex()
    alex.run()
