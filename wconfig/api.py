from .file import *
from .objects import *
from .about import pseudo_quine



def ini(location):

    data = INI(location)
    return Configuration(data)