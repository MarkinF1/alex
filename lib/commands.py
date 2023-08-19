"""
Команды реализованы в виде исключений для
упрощения проброса от распознавателя к обработчику.
"""
from logger import logger


class Actions:
    play = 'play'
    pause = 'pause'
    stop = 'stop'
    next = 'next'
    say = 'say'


class Types:
    music = 'music'
    weather = 'weather'
    time = 'time'


# --- Базовый класс для команд ---
class _BaseCommand(Exception):
    @property
    def type_(self):
        try:
            return self._type
        except AttributeError:
            logger.exception(f"Для класса {type(self)} не указан тип команды.")

    @property
    def action(self):
        try:
            return self._action
        except AttributeError:
            logger.exception(f"Для класса {type(self)} не указано действие команды.")


# --- Музыка ---
class _Music(_BaseCommand):
    def __init__(self):
        super(_Music, self).__init__()
        self._type = Types.music


class MusicPlay(_Music):
    def __init__(self):
        super(MusicPlay, self).__init__()
        self._action = Actions.play


class MusicStop(_Music):
    def __init__(self):
        super(MusicStop, self).__init__()
        self._action = Actions.stop


class MusicPause(_Music):
    def __init__(self):
        super(MusicPause, self).__init__()
        self._action = Actions.pause


class MusicNext(_Music):
    def __init__(self):
        super(MusicNext, self).__init__()
        self._action = Actions.next


# --- Погода ---
class WeatherSay(_BaseCommand):
    def __init__(self):
        super(WeatherSay, self).__init__()
        self._type = Types.weather
        self._action = Actions.say


# --- Время ---
class TimeSay(_BaseCommand):
    def __init__(self):
        super(TimeSay, self).__init__()
        self._type = Types.time
        self._action = Actions.say
