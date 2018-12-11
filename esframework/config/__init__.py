""" configuration classes """
import configparser


class ESConfig(object):
    """ default ESConfig object """
    __instance = None
    __config = None

    def __new__(cls):
        if ESConfig.__instance is None:
            ESConfig.__instance = object.__new__(cls)
        return ESConfig.__instance

    def load(self, file: str):
        config = configparser.ConfigParser()
        config.read(file)
        self.__config = config

    def get(self, section: str, key: str):
        return self.__config[section][key]


