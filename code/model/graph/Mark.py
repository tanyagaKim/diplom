import enum


class Mark(enum.Enum):
    start = 'start'
    end = 'end'


class MarkedStatus:
    def __init__(self, mark, status):
        self.mark = Mark
        self.status = str

        self.mark = mark
        self.status = status
