import pathlib

from skyfield.iokit import Loader
from skyfield.timelib import GREGORIAN_START


class TimeData:

    def __init__(self):
        path = pathlib.Path(__file__).parent.parent.absolute() / 'skyfield-data'
        load = Loader(path.as_posix())
        self.timescale = load.timescale()
        self.timescale.julian_calendar_cutoff = GREGORIAN_START
