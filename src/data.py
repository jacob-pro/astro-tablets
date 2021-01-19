import pathlib

from skyfield.data import hipparcos
from skyfield.iokit import Loader
from skyfield.starlib import Star
from skyfield.timelib import GREGORIAN_START
from skyfield.toposlib import Topos

from constants import BABYLON_COORDS


class AstroData:

    def __init__(self, time_only=False):
        path = pathlib.Path(__file__).parent.parent.absolute() / 'skyfield-data'
        load = Loader(path.as_posix())
        self.timescale = load.timescale()
        self.timescale.julian_calendar_cutoff = GREGORIAN_START
        if not time_only:
            self.ephemeris = load('de431t.bsp')
            self.babylon = Topos(*BABYLON_COORDS)
            with load.open(hipparcos.URL) as f:
                self.stars = hipparcos.load_dataframe(f)

    def get_body(self, name: str):
        # Solar System
        if name == "Mercury":
            return self.ephemeris["mercury BARYCENTER"]
        if name == "Venus":
            return self.ephemeris["venus BARYCENTER"]
        if name == "Mars":
            return self.ephemeris["mars BARYCENTER"]
        if name == "Saturn":
            return self.ephemeris["saturn BARYCENTER"]
        if name == "Jupiter":
            return self.ephemeris["jupiter BARYCENTER"]
        if name == "Moon":
            return self.ephemeris["moon"]
        # Stars
        if name == "Sheratan": # β Arietis
            return Star.from_dataframe(self.stars.loc[8903])
        if name == "Antares":  # α Scorpii
            return Star.from_dataframe(self.stars.loc[80763])
        if name == "Nu Arietis":
            return Star.from_dataframe(self.stars.loc[12332])
        if name == "58 Piscium":
            return Star.from_dataframe(self.stars.loc[3675])
        if name == "Epsilon Piscium":
            return Star.from_dataframe(self.stars.loc[4906])
        if name == "36 Persei":
            return Star.from_dataframe(self.stars.loc[16499])
        if name == "Alcyone":
            return Star.from_dataframe(self.stars.loc[17702])
        if name == "Nu Aurigae":
            return Star.from_dataframe(self.stars.loc[27673])
        if name == "Regulus":
            return Star.from_dataframe(self.stars.loc[49669])
        if name == "Beta Virginis":
            return Star.from_dataframe(self.stars.loc[57757])
        raise ValueError
