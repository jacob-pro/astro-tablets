import dataclasses
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import *

from constants import MAX_NISAN_EQUINOX_DIFF_DAYS
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
    intercalary: str
    next_nisan: str
    months: List[PotentialMonthResult]


@dataclass
class MultiyearResult:
    base_year: float
    best_score: float
    potential_years: List[List[PotentialYearResult]]


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class Intercalary(Enum):
    UNKNOWN = "unknown"
    FALSE = "false"
    ULULU = "Ululu II"
    ADDARU = "Addaru II"


@dataclass
class YearToTest:
    index: int
    name: str
    intercalary: Intercalary
    func: Callable


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
        """
        Tries repeating the same month observations but assuming the month started either 0 or 1 days later
        than first lunar visibility
        Returns the best / highest scoring month
        """
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

    def repeat_year_with_alternate_starts(self, potential_years: List[Dict], name: str, intercalary: Intercalary,
                                           func: Callable[[float], List[PotentialMonthResult]]
                                           ) -> List[PotentialYearResult]:
        """
        Tries repeating the same set of year observations, but starting at different dates for Nisan I
        Returns a list in order of highest score, descending
        """
        all_results = []
        for y in potential_years:
            months = self.db.get_months(y['nisan_1'], count=14)
            if intercalary == Intercalary.ULULU or intercalary == Intercalary.ADDARU:
                # Exclude a late start if this year is intercalary
                next_nisan = months[13]
                next_venal = self.db.nearest_event_match_to_time(SUN, VERNAL_EQUINOX, next_nisan)
                if abs(next_venal - next_nisan) > MAX_NISAN_EQUINOX_DIFF_DAYS:
                    continue
            else:
                next_nisan = months[12]
            results = func(y['nisan_1'])
            total_score = sum(item.score for item in results)
            vernal = self.db.nearest_event_match_to_time(SUN, VERNAL_EQUINOX, y['nisan_1'])
            all_results.append(
                PotentialYearResult(total_score, name, jd_float_to_local_time(y['nisan_1'], self.data.timescale),
                                    jd_float_to_local_time(vernal, self.data.timescale),
                                    intercalary.value, jd_float_to_local_time(next_nisan, self.data.timescale), results))
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
    def output_json_for_year(results: List[MultiyearResult], year: Union[int, None]):
        if year is not None:
            filtered = list(filter(lambda x: x.base_year == year, results))
            if len(filtered) < 1:
                raise RuntimeError("Base year not found")
            with open('result_for_{}.json'.format(year), 'w') as outfile:
                json.dump(filtered[0], outfile, indent=2, cls=EnhancedJSONEncoder)

    def run_years(self, ys: List[YearToTest]) -> List[MultiyearResult]:
        years = list(map(lambda x: x[1], self.db.get_years().items()))
        results = []
        max_index = max(d.index for d in ys)
        assert ys[0].index == 0, "First index must be 0"
        for i in range(0, len(years) - max_index):
            rys = []
            for x in ys:
                rys.append(self.repeat_year_with_alternate_starts(years[i + x.index], x.name, x.intercalary, x.func))
            total_score = sum(item[0].score for item in rys)
            results.append(MultiyearResult(years[i][0]['year'], total_score, rys))
        return results
