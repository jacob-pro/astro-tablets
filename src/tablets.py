from typing import *

from constants import OuterPlanetArcusVisionis, InnerPlanetArcusVisionis
from data import AstroData
from database import Database
from lunar_calendar import vernal_equinox, days_in_range
from planet_events import outer_planet_events, inner_planet_events

FN_TYPE = Callable[[AstroData, Database, int, int], None]


def match(tablet: str) -> Tuple[FN_TYPE, int, int]:
    if tablet == "bm32312":
        return bm32312, -701, -601
    raise ValueError("Unknown tablet name")


def mercury(data: AstroData, db: Database, start: int, end: int):
    print("Computing Mercury visibility...")
    events = inner_planet_events(data, data.get_body("Mercury"),
                                 data.timescale.ut1(start, 1, 1),
                                 data.timescale.ut1(end + 1, 6, 1),
                                 InnerPlanetArcusVisionis.mercury())
    db.save_synodic_events("Saturn", events)


def mars(data: AstroData, db: Database, start: int, end: int):
    print("Computing Mars visibility...")
    events = outer_planet_events(data, data.get_body("Mars"),
                                 data.timescale.ut1(start, 1, 1),
                                 data.timescale.ut1(end + 1, 6, 1),
                                 OuterPlanetArcusVisionis.mars())
    db.save_synodic_events("Mars", events)


def saturn(data: AstroData, db: Database, start: int, end: int):
    print("Computing Saturn visibility...")
    events = outer_planet_events(data, data.get_body("Saturn"),
                                 data.timescale.ut1(start, 1, 1),
                                 data.timescale.ut1(end + 1, 6, 1),
                                 OuterPlanetArcusVisionis.saturn())
    db.save_synodic_events("Saturn", events)


def calendar(data: AstroData, db: Database, start: int, end: int):
    print("Computing lunar calendar...")
    for i in range(start, end + 1):
        db.save_equinox(vernal_equinox(data, i))
    begin = data.timescale.tt_jd(vernal_equinox(data, start).tt - 31)
    end = data.timescale.tt_jd(vernal_equinox(data, end + 1).tt + 31)
    days = days_in_range(data, begin, end)
    db.save_days(days)


def bm32312(data: AstroData, db: Database, start: int, end: int):
    calendar(data, db, start, end)
    mars(data, db, start, end)
    saturn(data, db, start, end)
    mercury(data, db, start, end)


