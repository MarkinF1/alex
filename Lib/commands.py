"""
Распознаватель речи определяет тип команды,
после чего кидает соответсвующее исключение,
которое будет обработано.
"""
from logger import logger


PLAY = 'play'
PAUSE = 'pause'
STOP = 'stop'
NEXT = 'next'
SAY = 'say'

TYPE_MUSIC = 'music'
TYPE_WEATHER = 'weather'
TYPE_TIME = 'time'


# --- Базовый класс для команд ---
class _BaseCommand(Exception):
    @property
    def type_(self):
        try:
            return self._type
        except AttributeError:
            logger.exception(f"Для класс {self} не указан тип команды.")
            return None

    @property
    def action(self):
        try:
            return self._action
        except AttributeError:
            logger.exception(f"Для класс {self} не указано действие команды.")
            return None


# --- Музыка ---
class _Music(_BaseCommand):
    def __init__(self):
        super(_Music, self).__init__()
        self._type = TYPE_MUSIC


class MusicPlay(_Music):
    def __init__(self):
        super(MusicPlay, self).__init__()
        self._action = PLAY


class MusicStop(_Music):
    def __init__(self):
        super(MusicStop, self).__init__()
        self._action = STOP


class MusicPause(_Music):
    def __init__(self):
        super(MusicPause, self).__init__()
        self._action = PAUSE
    pass


class MusicNext(_Music):
    def __init__(self):
        super(MusicNext, self).__init__()
        self._action = NEXT


# --- Погода ---
class WeatherSay(_BaseCommand):
    def __init__(self):
        super(WeatherSay, self).__init__()
        self._type = TYPE_WEATHER
        self._action = SAY


# --- Время ---
class TimeSay(_BaseCommand):
    def __init__(self):
        super(TimeSay, self).__init__()
        self._type = TYPE_TIME
        self._action = SAY
