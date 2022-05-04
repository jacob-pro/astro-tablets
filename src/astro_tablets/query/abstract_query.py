from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, List, TypeVar

from astro_tablets.constants import INFLECT_ENGINE
from astro_tablets.query.database import BabylonianDay
from astro_tablets.util import TimeValue

R = TypeVar("R")


@dataclass
class ScoredResult(Generic[R]):
    result: R
    score: float

    @staticmethod
    def score_results(
        results: List[R], score_fn: Callable[[R], float]
    ) -> List[ScoredResult[R]]:
        scored = list(
            map(
                lambda r: ScoredResult(r, score_fn(r)),
                results,
            )
        )
        scored.sort(
            key=lambda x: x.score,
            reverse=True,
        )
        return scored


@dataclass
class SearchRange:
    start: float
    end: float
    comment: str

    def output(self) -> dict:
        return {
            "search_start": TimeValue(self.start),
            "search_end": TimeValue(self.end),
            "date": self.comment,
        }

    @staticmethod
    def for_night(month: List[BabylonianDay], day_number: int) -> SearchRange:
        assert 1 <= day_number <= 30
        return SearchRange(
            month[day_number - 1].sunset,
            month[day_number - 1].sunrise,
            "Night of the {}".format(INFLECT_ENGINE.ordinal(day_number)),
        )

    @staticmethod
    def for_night_and_day(month: List[BabylonianDay], day_number: int) -> SearchRange:
        assert 1 <= day_number <= 30
        return SearchRange(
            month[day_number - 1].sunset,
            month[day_number].sunset,
            "Night and day of the {}".format(INFLECT_ENGINE.ordinal(day_number)),
        )

    @staticmethod
    def any_day(month: List[BabylonianDay]) -> SearchRange:
        return SearchRange(month[0].sunset, month[29].sunrise, "Any day")

    @staticmethod
    def x_plus(month: List[BabylonianDay], x: int) -> SearchRange:
        assert 1 <= x <= 30
        return SearchRange(month[x - 1].sunset, month[29].sunrise, "{}+".format(x))

    @staticmethod
    def range_of_nights(month: List[BabylonianDay], x: int, y: int) -> SearchRange:
        assert 1 <= x <= 30
        assert 1 <= y <= 30
        return SearchRange(
            month[x - 1].sunset, month[y - 1].sunrise, "{}-{}".format(x, y)
        )


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
