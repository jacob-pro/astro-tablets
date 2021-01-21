from abc import ABC
from dataclasses import dataclass
from typing import *

from data import AstroData
from query.database import Database
from query.result import AbstractResult
from util import jd_float_to_string


@dataclass
class MultiplexedMonthResult:
    score: float
    output: List[Dict]


@dataclass
class PotentialYearResult:
    score: float
    nisan_1: float
    months: List[MultiplexedMonthResult]


class AbstractTablet(ABC):

    def __init__(self, data: AstroData, db: Database):
        self.data = data
        self.db = db

    def repeat_month_with_alternate_starts(self, nisan_1: float, month: List,
                                           func: Callable[[List, int, float], List[AbstractResult]]
                                           ) -> MultiplexedMonthResult:
        all_results = []
        for start_offset in range(0, 2):
            results = func(month[start_offset:], start_offset, nisan_1)
            score = sum(item.quality_score() for item in results)
            output = list(map(lambda x: x.output(self.data), results))
            all_results.append(MultiplexedMonthResult(score, output))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[0]

    def repeat_year_with_alternate_starts(self, potential_years: List,
                                           func: Callable[[float], List[MultiplexedMonthResult]]
                                           ) -> List[PotentialYearResult]:
        all_results = []
        for y in potential_years:
            results = func(y['nisan_1'])
            total_score = sum(item.score for item in results)
            all_results.append(
                PotentialYearResult(total_score, jd_float_to_string(y['nisan_1'], self.data.timescale), results))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results
