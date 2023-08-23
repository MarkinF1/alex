class Actions:
    play = 'play'
    pause = 'pause'
    stop = 'stop'
    next = 'next'
    say = 'say'
    unknown = 'unknown'


class Types:
    music = 'music'
    weather = 'weather'
    time = 'time'
    unknown = 'unknown'


class Command:
    def __init__(self, type_: str, action: str):
        self.__type = type_
        self.__action = action

    def type_(self):
        return self.__type

    def action(self):
        return self.__action
