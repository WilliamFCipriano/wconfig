"""wconfig public api"""
import os
from .file import *
from .about import _ as about_software

_default_locations = ['test', 'setup', 'config']


class ModuleInterface:

    def _load_defaults(self, reload=False):

        if not reload:
            self._default_config_dict = dict()
            self._default_config_list = list()

        global _default_locations
        for location in _default_locations:

            try:
                configuration = ConfigurationLazyLoader(location)
                self._default_config_dict[configuration.location] = configuration
                self._default_config_list.append(configuration.location)

            except UnrecoverableIOError:
                continue

    def __init__(self):
        self._default_locations = ['test.ini']
        self._default_config_dict = dict()
        self._default_config_list = list()

    def __getattr__(self, item):
        if item == '_about':
            return about_software()
        elif item in self._default_config_list:
            return self._default_config_dict[item]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        print(key, value)


class ConfigurationLazyLoader:

    def __init__(self, location):

        if os.path.isfile(location):
            self.location = location
        else:
            raise UnrecoverableIOError






API = ModuleInterface()

