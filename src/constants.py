from dataclasses import dataclass
from typing import *


LUNAR_VISIBILITY = 7.5

BABYLON_COORDS = ("32.55 N", "44.42 E")

FINGER = 0.092
CUBIT = 2.2
HALO = 22.0


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
    tolerance_days: float


MERCURY = Planet("mercury", InnerPlanetArcusVisionis(13.0, 9.5, 10.5, 11.0), True, 5)
VENUS = Planet("venus", InnerPlanetArcusVisionis(5.7, 6.0, 6.0, 5.2), True, 10)
MARS = Planet("mars", OuterPlanetArcusVisionis(14.5, 13.2, 6.0, 6.0), False, 20)
JUPITER = Planet("jupiter", OuterPlanetArcusVisionis(9.3, 7.4, 6.0, 6.0), False, 10)
SATURN = Planet("saturn", OuterPlanetArcusVisionis(13.0, 10.0, 8.0, 8.0), False, 10)
