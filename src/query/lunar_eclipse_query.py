from dataclasses import dataclass
from enum import unique, Enum
from typing import Union

from query.database import Database
from query.abstract_query import AbstractQuery, SearchRange


@unique
class FirstContactRelative(Enum):
    BEFORE_SUNRISE = 0
    AFTER_SUNRISE = 1
    BEFORE_SUNSET = 2
    AFTER_SUNSET = 3


@dataclass
class FirstContactTime:
    time_degrees: float
    relative: FirstContactRelative


@unique
class ExpectedEclipseType(Enum):
    UNKNOWN = 0           # A prediction or uncertain if it was a prediction
    PARTIAL_OR_TOTAL = 1  # An observation, of uncertain type
    PARTIAL = 2           # An observation of a partial eclipse
    TOTAL = 3             # An observations of a total eclipse


class LunarEclipseQuery(AbstractQuery):

    def __init__(self, db: Database, first_contact: Union[None, FirstContactTime],
                 type: ExpectedEclipseType, target_time: SearchRange):
        pass

    def output(self) -> dict:
        pass

    def get_search_range(self) -> SearchRange:
        pass

    def quality_score(self) -> float:
        pass
