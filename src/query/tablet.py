from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

from data import AstroData
from query.database import Database
from query.result import AbstractResult
from util import jd_float_to_string


@dataclass
class PotentialMonthResult:
    score: float
    report: List[Dict]


@dataclass
class PotentialYearResult:
    score: float
    nisan_1: float
    months: List[PotentialMonthResult]


@dataclass
class MultiyearResult:
    base_year: float
    score: float
    results: List


class AbstractTablet(ABC):

    def __init__(self, data: AstroData, db: Database):
        self.data = data
        self.db = db

    @abstractmethod
    def do_query(self, subquery: Union[str, None]):
        pass

    def repeat_month_with_alternate_starts(self, nisan_1: float, month: List,
                                           func: Callable[[List, int, float], List[AbstractResult]]
                                           ) -> PotentialMonthResult:
        all_results = []
        for start_offset in range(0, 2):
            results = func(month[start_offset:], start_offset, nisan_1)
            score = sum(item.quality_score() for item in results)
            output = list(map(lambda x: x.output(self.data), results))
            all_results.append(PotentialMonthResult(score, output))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[0]

    def repeat_year_with_alternate_starts(self, potential_years: List,
                                           func: Callable[[float], List[PotentialMonthResult]]
                                           ) -> List[PotentialYearResult]:
        all_results = []
        for y in potential_years:
            results = func(y['nisan_1'])
            total_score = sum(item.score for item in results)
            all_results.append(
                PotentialYearResult(total_score, jd_float_to_string(y['nisan_1'], self.data.timescale), results))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results

    @staticmethod
    def print_top_results(results: List[MultiyearResult], for_comment: str):
        results.sort(key=lambda x: x.score, reverse=True)
        print("Top matches for {}".format(for_comment))
        print("Year   Score")
        for i in results[:10]:
            print(i.base_year, i.score)
