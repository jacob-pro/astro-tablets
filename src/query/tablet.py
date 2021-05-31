import dataclasses
import itertools
import json
import roman
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import *

from skyfield.timelib import Timescale

from constants import MAX_NISAN_EQUINOX_DIFF_DAYS
from data import AstroData, SUN
from generate.lunar_calendar import VERNAL_EQUINOX
from query.database import Database, BabylonianDay
from query.abstract_query import AbstractQuery
from util import TimeValue


class Intercalary(Enum):
    UNKNOWN = "unknown"
    FALSE = "false"
    ULULU = "Ululu II"
    ADDARU = "Addaru II"

    def is_intercalary(self):
        return self == Intercalary.ULULU or self == Intercalary.ADDARU


@dataclass
class PotentialMonthResult:
    score: float
    name: str
    actual_month: int
    month_sunset_1: TimeValue
    first_visibility: TimeValue
    days_late: int
    observations: List[Dict]


@dataclass
class PotentialYearResult:
    score: float
    nisan_1: TimeValue
    next_nisan: TimeValue   # 12 or 13 months later depending on intercalary status
    best_compatible_path: bool
    _actual_year: int
    _intercalary: Intercalary
    months: List[PotentialMonthResult]


@dataclass
class YearResult:
    name: str
    actual_year: int
    vernal_equinox: TimeValue
    intercalary: Intercalary
    potentials: List[PotentialYearResult]


@dataclass
class MultiyearResult:
    base_year: float
    best_score: float
    years: List[YearResult]


class EnhancedJSONEncoder(json.JSONEncoder):

    def __init__(self, ts: Timescale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ts = ts

    def default(self, o):
        if dataclasses.is_dataclass(o):
            dict = o.__dict__
            for k in list(dict.keys()):
                if k.startswith('_'):
                    dict.pop(k)
            return dict
        if type(o) == Intercalary:
            return o.value
        if type(o) == TimeValue:
            return o.string(self.ts)
        return super().default(o)


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
    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        pass

    def repeat_month_with_alternate_starts(self, nisan_1: float, month_number: int,
                                           func: Callable[[List[BabylonianDay]], List[AbstractQuery]], name=None
                                           ) -> PotentialMonthResult:
        """
        Tries repeating the same month observations but assuming the month started either 0 or 1 days later
        than first lunar visibility
        Returns the best / highest scoring month
        """
        assert 1 <= month_number <= 13
        months = self.db.get_months(nisan_1)
        month_days = self.db.get_days(months[month_number - 1])
        name = name if name is not None else roman.toRoman(month_number)
        all_results = []
        for start_offset in range(0, 2):
            results = func(month_days[start_offset:])
            score = sum(item.quality_score() for item in results)
            output = list(map(lambda x:
                              {**x.output(),
                               **{'score': x.quality_score()},
                               **x.get_search_range().output()
                               }, results))
            sunset_one = TimeValue(month_days[start_offset].sunset)
            first_vis = TimeValue(month_days[0].sunset)
            all_results.append(PotentialMonthResult(score, name, month_number, sunset_one, first_vis, start_offset, output))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[0]

    def repeat_year_with_alternate_starts(self, potential_years: List[Dict], name: str, intercalary: Intercalary,
                                           func: Callable[[float], List[PotentialMonthResult]]
                                           ) -> YearResult:
        """
        Tries repeating the same set of year observations, but starting at different dates for Nisan I
        Returns a list in order of highest score, descending
        """
        all_results = []
        vernal = self.db.nearest_event_match_to_time(SUN, VERNAL_EQUINOX, potential_years[0]['nisan_1'])
        year_number = potential_years[0]['year']
        for y in potential_years:
            months = self.db.get_months(y['nisan_1'], count=14)
            if intercalary.is_intercalary():
                # Exclude a late start if this year is intercalary, i.e. make sure that whichever year
                # would follow this one is still valid
                next_nisan = months[13]
                next_venal = self.db.nearest_event_match_to_time(SUN, VERNAL_EQUINOX, next_nisan)
                if abs(next_venal - next_nisan) > MAX_NISAN_EQUINOX_DIFF_DAYS:
                    continue
            else:
                next_nisan = months[12]
            results = func(y['nisan_1'])
            total_score = sum(item.score for item in results)
            all_results.append(
                PotentialYearResult(score=total_score, nisan_1=TimeValue(y['nisan_1']),
                                    next_nisan=TimeValue(next_nisan), months=results,
                                    _intercalary=intercalary, _actual_year=year_number, best_compatible_path=False))
        all_results.sort(key=lambda x: x.score, reverse=True)
        return YearResult(name, year_number, TimeValue(vernal), intercalary, all_results)

    @staticmethod
    def print_results(results: List[MultiyearResult], for_comment: str):
        results.sort(key=lambda x: x.best_score, reverse=True)
        print("Scores for {}".format(for_comment))
        print("Year   Score")
        for i in results:
            print(i.base_year, i.best_score)

    def output_json_for_year(self, results: List[MultiyearResult], year: Union[int, None], slim_results: bool):
        if year is not None:
            filtered = list(filter(lambda x: x.base_year == year, results))
            if len(filtered) < 1:
                raise RuntimeError("Base year not found")
            year_to_print = filtered[0]

            if slim_results is True:
                for y in year_to_print.years:
                    y.potentials = list(filter(lambda x: x.best_compatible_path is True, y.potentials))

            with open('result_for_{}.json'.format(year), 'w') as outfile:
                encoder = EnhancedJSONEncoder(self.data.timescale, indent=2)
                raw = encoder.encode(year_to_print)
                outfile.write(raw)

    @staticmethod
    def total_score(yrs: List[YearResult]) -> float:
        potential_list = list(map(lambda x: x.potentials, yrs))
        product = list(itertools.product(*potential_list))
        compatible_products = []
        for i in product:
            incompatible = False
            # Years are incompatible if the year afterwards does not start when this one ends
            # Although we can only do this check if we know the length of this year for certain
            for y in i:
                if y._intercalary != Intercalary.UNKNOWN:
                    match_next_y = list(filter(lambda x: x._actual_year == y._actual_year + 1, i))  # type: List[PotentialYearResult]
                    if len(match_next_y) > 0:
                        if match_next_y[0].nisan_1 != y.next_nisan:
                            incompatible = True
            if not incompatible:
                compatible_products.append(i)
        assert len(compatible_products) > 0
        compatible_products.sort(key=lambda y: sum(x.score for x in y), reverse=True)
        for e in compatible_products[0]:
            e.best_compatible_path = True
        return sum(x.score for x in compatible_products[0])

    def run_years(self, ys: List[YearToTest]) -> List[MultiyearResult]:
        years = list(map(lambda x: x[1], self.db.get_years().items()))
        results = []
        max_index = max(d.index for d in ys)
        assert ys[0].index == 0, "First index must be 0"
        for i in range(0, len(years) - max_index):
            yrs = []  # type: List[YearResult]
            for x in ys:
                yrs.append(self.repeat_year_with_alternate_starts(years[i + x.index], x.name, x.intercalary, x.func))
            total_score = self.total_score(yrs)
            results.append(MultiyearResult(years[i][0]['year'], total_score, yrs))
        return results

    def try_multiple_months(self, nisan_1: float, start: int, end: int,
                            fn: Callable[[List[BabylonianDay]], List[AbstractQuery]], comment=None) -> PotentialMonthResult:
        attempts = []
        comment = "Unknown month between {} and {}".format(start, end) if comment is None else comment
        for m in range(start, end+1):
            attempts.append(
                self.repeat_month_with_alternate_starts(nisan_1, m, fn, name=comment))
        attempts.sort(key=lambda x: x.score, reverse=True)
        return attempts[0]
