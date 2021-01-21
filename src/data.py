import pathlib

from skyfield.data import hipparcos
from skyfield.iokit import Loader
from skyfield.starlib import Star
from skyfield.timelib import GREGORIAN_START
from skyfield.toposlib import Topos

from constants import *

EARTH = "earth"
MOON = "moon"
SUN = "sun"

SHERATAN = "sheratan"
ANTARES = "antares"
NU_ARIETIS = "nu arietis"
FIFTY_EIGHT_PISCIUM = "58 piscium"
EPSILON_PISCIUM = "epsilon piscium"
THIRTY_SIX_PERSEI = "36 persei"
ALCYONE = "alcyone"
NU_AURIGAE = "nu aurigae"
REGULUS = "regulus"
BETA_VIRGINIS = "beta virginis"


class AstroData:

    def __init__(self, time_only=False):
        path = pathlib.Path(__file__).parent.parent.absolute() / 'skyfield-data'
        load = Loader(path.as_posix())
        self.timescale = load.timescale()
        self.timescale.julian_calendar_cutoff = GREGORIAN_START
        if not time_only:
            self.ephemeris = load('de431t.bsp')
            self.babylon_topos = Topos(*BABYLON_COORDS)
            with load.open(hipparcos.URL) as f:
                self.stars = hipparcos.load_dataframe(f)

    def get_body(self, name: str):
        name = name.lower()

        if name == MERCURY.name:
            return self.ephemeris["MERCURY BARYCENTER"]
        if name == VENUS.name:
            return self.ephemeris["VENUS BARYCENTER"]
        if name == EARTH:
            return self.ephemeris["EARTH"]
        if name == MARS.name:
            return self.ephemeris["MARS BARYCENTER"]
        if name == SATURN.name:
            return self.ephemeris["SATURN BARYCENTER"]
        if name == JUPITER.name:
            return self.ephemeris["JUPITER BARYCENTER"]
        if name == MOON:
            return self.ephemeris["MOON"]
        if name == SUN:
            return self.ephemeris["SUN"]

        if name == SHERATAN:
            return Star.from_dataframe(self.stars.loc[8903])
        if name == ANTARES:
            return Star.from_dataframe(self.stars.loc[80763])
        if name == NU_ARIETIS:
            return Star.from_dataframe(self.stars.loc[12332])
        if name == FIFTY_EIGHT_PISCIUM:
            return Star.from_dataframe(self.stars.loc[3675])
        if name == EPSILON_PISCIUM:
            return Star.from_dataframe(self.stars.loc[4906])
        if name == THIRTY_SIX_PERSEI:
            return Star.from_dataframe(self.stars.loc[16499])
        if name == ALCYONE:
            return Star.from_dataframe(self.stars.loc[17702])
        if name == NU_AURIGAE:
            return Star.from_dataframe(self.stars.loc[27673])
        if name == REGULUS:
            return Star.from_dataframe(self.stars.loc[49669])
        if name == BETA_VIRGINIS:
            return Star.from_dataframe(self.stars.loc[57757])

        raise ValueError

    def get_babylon(self):
        return self.get_body(EARTH) + self.babylon_topos
