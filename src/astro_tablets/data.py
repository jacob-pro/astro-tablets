import os
import pathlib

from skyfield.data import hipparcos
from skyfield.iokit import Loader
from skyfield.starlib import Star
from skyfield.timelib import GREGORIAN_START
from skyfield.toposlib import Topos

from astro_tablets.constants import (
    ALCYONE,
    ANTARES,
    ASCELLA,
    BABYLON_COORDS,
    BETA_CAPRICORNI,
    BETA_GEMINORUM,
    BETA_LIBRAE,
    BETA_VIRGINIS,
    EARTH,
    EPSILON_LEONIS,
    EPSILON_PISCIUM,
    EPSILON_TAURI,
    ETA_CAPRICORNI,
    FIFTY_EIGHT_PISCIUM,
    FIFTY_TWO_LEONIS,
    FORTY_TWO_CANCRI,
    JUPITER,
    MARS,
    MERCURY,
    MOON,
    NU_ARIETIS,
    NU_AURIGAE,
    NU_LIBRAE,
    OMEGA_GEMINORUM,
    REGULUS,
    SATURN,
    SHERATAN,
    SUN,
    THETA_CANCRI,
    THETA_LEONIS,
    THETA_VIRGINIS,
    THIRTY_SIX_PERSEI,
    VENUS,
    Body,
)


class AstroData:
    def __init__(self, time_only=False):
        path = pathlib.Path(__file__).parent.parent.parent.absolute() / "skyfield-data"
        if not os.path.isdir(path):
            raise RuntimeError("'skyfield-data' folder does not exist")
        load = Loader(path.as_posix())
        self.timescale = load.timescale()
        self.timescale.julian_calendar_cutoff = GREGORIAN_START
        if not time_only:
            self.ephemeris = load("de431t.bsp")
            self.babylon_topos = Topos(*BABYLON_COORDS)
            with load.open(hipparcos.URL) as f:
                self.stars = hipparcos.load_dataframe(f)

    def get_body(self, body: Body):

        if body == MERCURY:
            return self.ephemeris["MERCURY BARYCENTER"]
        if body == VENUS:
            return self.ephemeris["VENUS BARYCENTER"]
        if body == EARTH:
            return self.ephemeris["EARTH"]
        if body == MARS:
            return self.ephemeris["MARS BARYCENTER"]
        if body == SATURN:
            return self.ephemeris["SATURN BARYCENTER"]
        if body == JUPITER:
            return self.ephemeris["JUPITER BARYCENTER"]
        if body == MOON:
            return self.ephemeris["MOON"]
        if body == SUN:
            return self.ephemeris["SUN"]

        if body == ALCYONE:
            return Star.from_dataframe(self.stars.loc[17702])
        if body == ANTARES:
            return Star.from_dataframe(self.stars.loc[80763])
        if body == BETA_CAPRICORNI:
            return Star.from_dataframe(self.stars.loc[100345])
        if body == BETA_GEMINORUM:
            return Star.from_dataframe(self.stars.loc[37826])
        if body == BETA_LIBRAE:
            return Star.from_dataframe(self.stars.loc[74785])
        if body == BETA_VIRGINIS:
            return Star.from_dataframe(self.stars.loc[57757])
        if body == EPSILON_LEONIS:
            return Star.from_dataframe(self.stars.loc[47908])
        if body == EPSILON_PISCIUM:
            return Star.from_dataframe(self.stars.loc[4906])
        if body == FORTY_TWO_CANCRI:
            return Star.from_dataframe(self.stars.loc[42578])
        if body == REGULUS:
            return Star.from_dataframe(self.stars.loc[49669])
        if body == THETA_LEONIS:
            return Star.from_dataframe(self.stars.loc[54879])
        if body == SHERATAN:
            return Star.from_dataframe(self.stars.loc[8903])

        if body == NU_ARIETIS:
            return Star.from_dataframe(self.stars.loc[12332])
        if body == NU_AURIGAE:
            return Star.from_dataframe(self.stars.loc[27673])
        if body == THETA_CANCRI:
            return Star.from_dataframe(self.stars.loc[41822])
        if body == ETA_CAPRICORNI:
            return Star.from_dataframe(self.stars.loc[104019])
        if body == OMEGA_GEMINORUM:
            return Star.from_dataframe(self.stars.loc[33927])
        if body == FIFTY_TWO_LEONIS:
            return Star.from_dataframe(self.stars.loc[52689])
        if body == NU_LIBRAE:
            return Star.from_dataframe(self.stars.loc[73945])
        if body == THIRTY_SIX_PERSEI:
            return Star.from_dataframe(self.stars.loc[16499])
        if body == FIFTY_EIGHT_PISCIUM:
            return Star.from_dataframe(self.stars.loc[3675])
        if body == ASCELLA:
            return Star.from_dataframe(self.stars.loc[93506])
        if body == EPSILON_TAURI:
            return Star.from_dataframe(self.stars.loc[20889])
        if body == THETA_VIRGINIS:
            return Star.from_dataframe(self.stars.loc[64238])

        raise ValueError(f"unknown body {body}")

    def get_babylon(self):
        return self.get_body(EARTH) + self.babylon_topos
