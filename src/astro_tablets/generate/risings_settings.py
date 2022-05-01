from dataclasses import dataclass
from enum import Enum, unique

from skyfield import almanac
from skyfield.timelib import Time

from astro_tablets.data import AstroData, Body
from typing import *


@unique
class RiseSetType(Enum):
    RISE = "rise"
    SET = "set"


@dataclass
class RisingOrSetting:
    time: Time
    type: RiseSetType


def risings_and_settings(data: AstroData, body: Body, t0: Time, t1: Time) -> List[RisingOrSetting]:
    f = almanac.risings_and_settings(data.ephemeris, data.get_body(body), data.babylon_topos)
    t, y = almanac.find_discrete(t0, t1, f)

    out = []
    for ti, yi in zip(t, y):
        type = RiseSetType.RISE if yi else RiseSetType.SET
        out.append(RisingOrSetting(ti, type))
    return out
