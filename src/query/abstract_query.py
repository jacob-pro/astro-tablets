from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

import inflect

from query.database import BabylonianDay
from util import TimeValue

p = inflect.engine()


@dataclass
class SearchRange:
    start: float
    end: float
    comment: str

    def output(self) -> dict:
        return {
            'search_start': TimeValue(self.start),
            'search_end': TimeValue(self.end),
            'date': self.comment,
        }

    @staticmethod
    def for_night(month: List[BabylonianDay], day_number: int):
        assert 1 <= day_number <= 30
        return SearchRange(month[day_number - 1].sunset, month[day_number - 1].sunrise,
                           "Night of the {}".format(p.ordinal(day_number)))

    @staticmethod
    def any_day(month: List[BabylonianDay]):
        return SearchRange(month[0].sunset, month[29].sunrise, "Any day")

    @staticmethod
    def x_plus(month: List[BabylonianDay], x: int):
        return SearchRange(month[x].sunset, month[29].sunrise, "{}+".format(x))


class AbstractQuery(ABC):

    @abstractmethod
    def quality_score(self) -> float:
        pass

    @abstractmethod
    def output(self) -> dict:
        pass

    @abstractmethod
    def get_search_range(self) -> SearchRange:
        pass


