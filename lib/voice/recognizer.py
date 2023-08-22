from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pyttsx3  # синтез речи (Text-To-Speech)
import json
import os

from lib.base_classes.singleton import SingletonMetaClass
from lib.commands import Command, Types, Actions
from lib.controller import Controller
from lib.logger import logger


class MicrophoneError(Exception):
    pass


class RecognizerError(Exception):
    pass


class Recognizer(metaclass=SingletonMetaClass):
    def __init__(self):
        self._config = Controller().recognizer_config
        self.__recognizer = speech_recognition.Recognizer()
        self.__microphone = speech_recognition.Microphone()
        self.__offline_model = None

        self.__init()

    def __init(self):
        if not os.path.exists(self._config.model_path):
            logger.error(f"Не найдена модель по пути {self._config.model_path}. "
                         "Её можно загрузить с сайта https://alphacephei.com/vosk/models ")
            return

        self.__offline_model = Model(self._config.model_path)

    def run(self) -> str:
        with self.__microphone:
            # регулирование уровня окружающего шума
            self.__recognizer.adjust_for_ambient_noise(self.__microphone, duration=2)

            audio = self.listen()
            while audio is None:
                audio = self.listen()

        audio_text = self.recognize(audio)

        return audio_text

    def listen(self):
        try:
            logger.debug("Слушаю...")
            audio = self.__recognizer.listen(self.__microphone, 5, 5)

            return audio

        except speech_recognition.WaitTimeoutError:
            return None

    def recognize(self, audio) -> str:
        if self._config.online:
            try:
                recognized_data = self.__recognize_online(audio)
                return recognized_data
            except Exception as exp:
                logger.warning(f"Не удалось распознать online. Ошибка: \n{exp}")

        try:
            recognized_data = self.__recognize_offline(audio)
        except Exception as exp:
            logger.error(f"Не удалось распознать offline. Ошибка: \n{exp}")
            raise RecognizerError

        return recognized_data

    def __recognize_online(self, audio) -> str:
        # использование online-распознавания через Google
        logger.debug("Начал распознование online...")
        recognized_data = self.__recognizer.recognize_google(audio, language=self._config.language).lower()

        return recognized_data

    def __recognize_offline(self, audio) -> str:
        # в случае проблем с доступом в Интернет происходит
        # попытка использовать offline-распознавание через Vosk
        if self.__offline_model is None:
            logger.warning("Модель для распознавания offline не создана. Не могу распознать текст в offline режиме.")
            raise RecognizerError

        logger.debug("Начал распознование offline...")
        recognized_data = ""

        offline_recognizer = KaldiRecognizer(self.__offline_model, audio.sample_rate)

        data = audio.frame_data
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]

        return recognized_data

    def create_command(self, data: str) -> Command:
        pass

