from typing import *

from skyfield.timelib import Time

from angular_separation import angular_separation
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


def mercury(data: AstroData, db: Database, start: Time, end: Time):
    print("Computing Mercury visibility...")
    events = inner_planet_events(data, data.get_body("Mercury"), start, end, InnerPlanetArcusVisionis.mercury())
    db.save_synodic_events("Saturn", events)


def mars(data: AstroData, db: Database, start: Time, end: Time):
    print("Computing Mars visibility...")
    events = outer_planet_events(data, data.get_body("Mars"), start, end, OuterPlanetArcusVisionis.mars())
    db.save_synodic_events("Mars", events)


def saturn(data: AstroData, db: Database, start: Time, end: Time):
    print("Computing Saturn visibility...")
    events = outer_planet_events(data, data.get_body("Saturn"), start, end, OuterPlanetArcusVisionis.saturn())
    db.save_synodic_events("Saturn", events)


def calendar(data: AstroData, db: Database, start: Time, end: Time):
    print("Computing lunar calendar...")
    for i in range(start.utc.year, end.utc.year + 1):
        db.save_equinox(vernal_equinox(data, i))
    days = days_in_range(data, start, end)
    db.save_days(days)


def separation(data: AstroData, db: Database, start: Time, end: Time, of: str, to: str):
    print("Computing separation between {} and {}...".format(of, to))
    current = start
    b1 = data.get_body(of)
    b2 = data.get_body(to)
    while current.tt <= end.tt:
        res = angular_separation(data, b1, b2, current)
        db.save_separation(of, to, res, current)
        delta = 1.0 / 24.0
        current = data.timescale.tt_jd(current.tt + delta)


def bm32312(data: AstroData, db: Database, start_year: int, end_year: int):
    start_day = data.timescale.tt_jd(vernal_equinox(data, start_year).tt - 32)
    end_day = data.timescale.tt_jd(vernal_equinox(data, end_year + 1).tt + 32)
    separation(data, db, start_day, end_day, "Mercury", "58 Piscium")
    separation(data, db, start_day, end_day, "Saturn", "58 Piscium")
    separation(data, db, start_day, end_day, "Mars", "Antares")
    separation(data, db, start_day, end_day, "Mars", "Nu Arietis")
    calendar(data, db, start_day, end_day)
    mars(data, db, start_day, end_day)
    saturn(data, db, start_day, end_day)
    mercury(data, db, start_day, end_day)


