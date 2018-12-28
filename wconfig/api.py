"""wconfig public api"""
import os
from .file import *
from .objects import *
from .about import _ as about_this_software


def load_ini(location):
    ini_file = INI(location)
    return Configuration(ini_file)