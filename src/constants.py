from dataclasses import dataclass
from typing import *


LUNAR_VISIBILITY = 7.5

BABYLON_COORDS = ("32.55 N", "44.42 E")

FINGER = 0.092
CUBIT = 2.2
HALO = 22.0

US_TIME_DEGREE_MINUTES = 4
BERU_MINUTES = 30 * US_TIME_DEGREE_MINUTES

MAX_NISAN_EQUINOX_DIFF_DAYS = 31


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
class Planet:
    name: str
    arcus_visionis: Union[InnerPlanetArcusVisionis, OuterPlanetArcusVisionis]
    is_inner: bool
    event_frequency: float  # Approx. average number of synodic events that occur in a one year period


MERCURY = Planet("mercury", InnerPlanetArcusVisionis(13.0, 9.5, 10.5, 11.0), True, 12)
VENUS = Planet("venus", InnerPlanetArcusVisionis(5.7, 6.0, 6.0, 5.2), True, 2.7)
MARS = Planet("mars", OuterPlanetArcusVisionis(14.5, 13.2, 6.0, 6.0), False, 1.9)
JUPITER = Planet("jupiter", OuterPlanetArcusVisionis(9.3, 7.4, 6.0, 6.0), False, 3.9)
SATURN = Planet("saturn", OuterPlanetArcusVisionis(13.0, 10.0, 8.0, 8.0), False, 3.9)


@dataclass
class Constellation:
    central_star: str
    radius: float


NU_ARIETIS = "nu arietis"
NU_AURIGAE = "nu aurigae"
THETA_CANCRI = "theta cancri"
ETA_CAPRICORNI = "eta_capricorni"
FIFTY_TWO_LEONIS = "52 leonis"
NU_LIBRAE = "nu librae"
THIRTY_SIX_PERSEI = "36 persei"
FIFTY_EIGHT_PISCIUM = "58 piscium"
ASCELLA = "ascella"
THETA_VIRGINIS = "theta virginis"

ARIES = Constellation(NU_ARIETIS, 30)
AURIGA = Constellation(NU_AURIGAE, 32)
CANCER = Constellation(THETA_CANCRI, 25)
CAPRICORNUS = Constellation(ETA_CAPRICORNI, 28)
LEO = Constellation(FIFTY_TWO_LEONIS, 40)
LIBRA = Constellation(NU_LIBRAE, 25)
PERSEUS = Constellation(THIRTY_SIX_PERSEI, 45)
PISCES = Constellation(FIFTY_EIGHT_PISCIUM, 50)
SAGITTARIUS = Constellation(ASCELLA, 40)
VIRGO = Constellation(THETA_VIRGINIS, 45)
