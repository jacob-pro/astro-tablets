from typing import *

from constants import OuterPlanetArcusVisionis, InnerPlanetArcusVisionis
from data import AstroData
from database import Database
from lunar_calendar import vernal_equinox
from planet_events import outer_planet_events, inner_planet_events

FN_TYPE = Callable[[AstroData, Database, int, int], None]


def match(tablet: str) -> Tuple[FN_TYPE, int, int]:
    if tablet == "bm32312":
        return bm32312, -701, -601
    raise ValueError("Unknown tablet name")


def mercury(data: AstroData, db: Database, start: int, end: int):
    print("Working on Mercury events...")
    events = inner_planet_events(data, data.get_body("Mercury"),
                                 data.timescale.utc(start, 1, 1),
                                 data.timescale.utc(end + 1, 6, 1),
                                 InnerPlanetArcusVisionis.mercury())
    db.save_synodic_events("Saturn", events)


def mars(data: AstroData, db: Database, start: int, end: int):
    print("Working on Mars events...")
    events = outer_planet_events(data, data.get_body("Mars"),
                                 data.timescale.utc(start, 1, 1),
                                 data.timescale.utc(end + 1, 6, 1),
                                 OuterPlanetArcusVisionis.mars())
    db.save_synodic_events("Mars", events)


def saturn(data: AstroData, db: Database, start: int, end: int):
    print("Working on Saturn events...")
    events = outer_planet_events(data, data.get_body("Saturn"),
                                 data.timescale.utc(start, 1, 1),
                                 data.timescale.utc(end + 1, 6, 1),
                                 OuterPlanetArcusVisionis.saturn())
    db.save_synodic_events("Saturn", events)


def calendar(data: AstroData, db: Database, start: int, end: int):
    print("Working on Calendar...")
    for i in range(start, end + 1):
        db.save_equinox(vernal_equinox(data, i))


def bm32312(data: AstroData, db: Database, start: int, end: int):
    calendar(data, db, start, end)
    mars(data, db, start, end)
    saturn(data, db, start, end)
    mercury(data, db, start, end)


