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

MAX_NISAN_EQUINOX_DIFF_DAYS = 34


@unique
class Precision(Enum):
    REGULAR = 0
    # Low precision is useful when the text is damaged  / unclear / or is a prediction
    LOW = 1


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
class Circle:
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

ARIES = Circle(NU_ARIETIS, 30)
AURIGA = Circle(NU_AURIGAE, 32)
CANCER = Circle(THETA_CANCRI, 25)
CAPRICORNUS = Circle(ETA_CAPRICORNI, 28)
GEMINI = Circle(OMEGA_GEMINORUM, 29)
LEO = Circle(FIFTY_TWO_LEONIS, 40)
LIBRA = Circle(NU_LIBRAE, 25)
PERSEUS = Circle(THIRTY_SIX_PERSEI, 45)
PISCES = Circle(FIFTY_EIGHT_PISCIUM, 50)
SAGITTARIUS = Circle(ASCELLA, 40)
TAURUS = Circle(EPSILON_TAURI, 48)
VIRGO = Circle(THETA_VIRGINIS, 45)

HEAD_OF_THE_LION = Circle(EPSILON_LEONIS, 15)
PLEIADES = Circle(ALCYONE, 5)
PRAESEPE = Circle(FORTY_TWO_CANCRI, 3)  # Beehive Cluster


# Useful constants when the text doesn't specify precisely how close two bodies are.
# Should be used in conjunction with Precision.LOW to reflect this is not exactly known.
@unique
class Radius(Enum):
    SMALL = 5
    MEDIUM = 10
