import dataclasses
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

from data import AstroData, SUN
from generate.lunar_calendar import VERNAL_EQUINOX
from query.database import Database, BabylonianDay
from query.result import AbstractResult
from util import jd_float_to_local_time


@dataclass
class PotentialMonthResult:
    score: float
    name: str
    actual_month: int
    month_sunset_1: str
    first_visibility: str
    days_late: int
    observations: List[Dict]


@dataclass
class PotentialYearResult:
    score: float
    name: str
    nisan_1: str
    vernal_equinox: str
    months: List[PotentialMonthResult]


@dataclass
class MultiyearResult:
    base_year: float
    best_score: float
    potential_years: List


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class AbstractTablet(ABC):

    def __init__(self, data: AstroData, db: Database):
        self.data = data
        self.db = db

    @abstractmethod
    def do_query(self, subquery: Union[str, None], print_year: Union[int, None]):
        pass

    def repeat_month_with_alternate_starts(self, nisan_1: float, month_number: int, name: str,
                                           func: Callable[[List[BabylonianDay]], List[AbstractResult]]
                                           ) -> PotentialMonthResult:
        assert 1 <= month_number <= 13
        months = self.db.get_months(nisan_1)
        month_days = self.db.get_days(months[month_number - 1])
        all_results = []
        for start_offset in range(0, 2):
            results = func(month_days[start_offset:])
            score = sum(item.quality_score() for item in results)
            output = list(map(lambda x:
                              {**x.output(self.data.timescale),
                               **{'score': x.quality_score()},
                               **x.get_search_range().output(self.data.timescale)
                               }, results))
            sunset_one = jd_float_to_local_time(month_days[start_offset].sunset, self.data.timescale)
            first_vis = jd_float_to_local_time(month_days[0].sunset, self.data.timescale)
            all_results.append(PotentialMonthResult(score, name, month_number, sunset_one, first_vis, start_offset, output))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[0]

    def repeat_year_with_alternate_starts(self, potential_years: List[Dict], name: str,
                                           func: Callable[[float], List[PotentialMonthResult]]
                                           ) -> List[PotentialYearResult]:
        all_results = []
        for y in potential_years:
            results = func(y['nisan_1'])
            total_score = sum(item.score for item in results)
            vernal = self.db.nearest_event_match_to_time(SUN, VERNAL_EQUINOX, y['nisan_1'])
            all_results.append(
                PotentialYearResult(total_score, name, jd_float_to_local_time(y['nisan_1'], self.data.timescale),
                                    jd_float_to_local_time(vernal, self.data.timescale), results))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results

    @staticmethod
    def print_results(results: List[MultiyearResult], for_comment: str):
        results.sort(key=lambda x: x.best_score, reverse=True)
        print("Scores for {}".format(for_comment))
        print("Year   Score")
        for i in results:
            print(i.base_year, i.best_score)

    @staticmethod
    def output_results_for_year(results: List[MultiyearResult], year: Union[int, None]):
        filtered = list(filter(lambda x: x.base_year == year, results))
        if len(filtered) > 0:
            with open('result_for_{}.json'.format(year), 'w') as outfile:
                json.dump(filtered[0], outfile, indent=2, cls=EnhancedJSONEncoder)
