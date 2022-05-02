from dataclasses import dataclass
from enum import Enum, unique
from typing import Union

import inflect

LUNAR_VISIBILITY = 7.5

BABYLON_COORDS = ("32.55 N", "44.42 E")

# Babylonian angular separations converted to degrees
FINGER = 0.092
CUBIT = 2.2
HALO = 22.0

BERU_US = 30

# about 30 days - slightly more tolerant
MAX_NISAN_EQUINOX_DIFF_DAYS = 34


@unique
class TimePrecision(Enum):
    """When measurements of time are used (e.g. eclipse duration, lunar six), how highly time should be weighted when
    computing a score; e.g. for predictions we should expect the time to not be particularly accurate.
    A higher value means less tolerance for error"""

    REGULAR = 5
    LOW = 1.5


INFLECT_ENGINE = inflect.engine()


@dataclass
class InnerPlanetArcusVisionis:
    mf: float
    ml: float
    ef: float
    el: float


@dataclass
class OuterPlanetArcusVisionis:
    hr: float
    hs: float
    ar: float
    cs: float


@dataclass
class Body:
    name: str


@dataclass
class Planet(Body):
    name: str
    arcus_visionis: Union[InnerPlanetArcusVisionis, OuterPlanetArcusVisionis]
    is_inner: bool
    event_frequency: float  # Approx. average number of synodic events that occur in a one year period


MERCURY = Planet("mercury", InnerPlanetArcusVisionis(13.0, 9.5, 10.5, 11.0), True, 12)
VENUS = Planet("venus", InnerPlanetArcusVisionis(5.7, 6.0, 6.0, 5.2), True, 2.7)
MARS = Planet("mars", OuterPlanetArcusVisionis(14.5, 13.2, 6.0, 6.0), False, 1.9)
JUPITER = Planet("jupiter", OuterPlanetArcusVisionis(9.3, 7.4, 6.0, 6.0), False, 3.9)
SATURN = Planet("saturn", OuterPlanetArcusVisionis(13.0, 10.0, 8.0, 8.0), False, 3.9)


EARTH = Body("earth")
MOON = Body("moon")
SUN = Body("sun")

ALCYONE = Body("alcyone")
ANTARES = Body("antares")
BETA_CAPRICORNI = Body("beta capricorni")
BETA_GEMINORUM = Body("beta geminorum")
BETA_LIBRAE = Body("beta librae")
BETA_VIRGINIS = Body("beta virginis")
EPSILON_LEONIS = Body("epsilon leonis")
EPSILON_PISCIUM = Body("epsilon piscium")
FORTY_TWO_CANCRI = Body("42 cancri")
REGULUS = Body("regulus")
THETA_LEONIS = Body("theta leonis")
SHERATAN = Body("sheratan")


@dataclass
class Constellation:
    central_star: Body
    radius: float


NU_ARIETIS = Body("nu arietis")
NU_AURIGAE = Body("nu aurigae")
THETA_CANCRI = Body("theta cancri")
ETA_CAPRICORNI = Body("eta_capricorni")
OMEGA_GEMINORUM = Body("omega geminorum")
FIFTY_TWO_LEONIS = Body("52 leonis")
NU_LIBRAE = Body("nu librae")
THIRTY_SIX_PERSEI = Body("36 persei")
FIFTY_EIGHT_PISCIUM = Body("58 piscium")
ASCELLA = Body("ascella")
EPSILON_TAURI = Body("epsilon tauri")
THETA_VIRGINIS = Body("theta virginis")

ARIES = Constellation(NU_ARIETIS, 30)
AURIGA = Constellation(NU_AURIGAE, 32)
CANCER = Constellation(THETA_CANCRI, 25)
CAPRICORNUS = Constellation(ETA_CAPRICORNI, 28)
GEMINI = Constellation(OMEGA_GEMINORUM, 29)
LEO = Constellation(FIFTY_TWO_LEONIS, 40)
LIBRA = Constellation(NU_LIBRAE, 25)
PERSEUS = Constellation(THIRTY_SIX_PERSEI, 45)
PISCES = Constellation(FIFTY_EIGHT_PISCIUM, 50)
SAGITTARIUS = Constellation(ASCELLA, 40)
TAURUS = Constellation(EPSILON_TAURI, 48)
VIRGO = Constellation(THETA_VIRGINIS, 45)
