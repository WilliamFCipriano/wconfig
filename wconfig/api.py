from .file import *
from .objects import *


def ini(location):

    data = INI(location)
    return Configuration(data)