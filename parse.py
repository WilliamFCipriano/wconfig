class ParserError(Exception):
    pass


class INIFile:

    def __init__(self, data):
        self.raw_data = data

