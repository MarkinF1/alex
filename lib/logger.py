import logging

logging.basicConfig(handlers=(logging.FileHandler('output.log'), logging.StreamHandler()),
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

