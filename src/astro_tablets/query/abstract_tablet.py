from __future__ import annotations

import dataclasses
import json
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional

import roman
from skyfield.timelib import Timescale

from astro_tablets.constants import MAX_NISAN_EQUINOX_DIFF_DAYS
from astro_tablets.data import SUN, AstroData
from astro_tablets.generate.lunar_calendar import VERNAL_EQUINOX
from astro_tablets.query.abstract_query import AbstractQuery
from astro_tablets.query.compatible_combinations import (
    CanBeFollowedBy,
    Result,
    generate_compatible_combinations,
)
from astro_tablets.query.database import BabylonianDay, Database, PotentialYear
from astro_tablets.util import PROGRESS_CALLBACK, TimeValue


class MonthLength(Enum):
    UNKNOWN = "unknown"
    TWENTY_NINE = "29"
    THIRTY = "30"


@dataclass
class PotentialMonthResult(CanBeFollowedBy):
    score: float
    name: str
    actual_month: int
    month_sunset_1: TimeValue
    first_visibility: TimeValue
    next_month_sunset_1: Optional[TimeValue]
    days_late: int
    observations: List[Dict]
    _length: MonthLength

    def can_be_followed_by(self, potential2: PotentialMonthResult) -> bool:
        # Months are incompatible if the month afterwards does not start when this one ends
        # Although we can only do this check if we know the length of this month for certain
        # noinspection PyProtectedMember
        if (
            self._length != MonthLength.UNKNOWN
            and self.actual_month == potential2.actual_month - 1
        ):
            if potential2.month_sunset_1.inner != self.next_month_sunset_1.inner:  # type: ignore
                return False
        return True


@dataclass
class MonthResult(Result):
    potentials: List[PotentialMonthResult]


class Intercalary(Enum):
    UNKNOWN = "unknown"
    FALSE = "false"
    ULULU = "Ululu II"
    ADDARU = "Addaru II"

    def is_intercalary(self) -> bool:
        return self == Intercalary.ULULU or self == Intercalary.ADDARU


@dataclass
class PotentialYearResult(CanBeFollowedBy):
    score: float
    nisan_1: TimeValue
    next_nisan: TimeValue  # 12 or 13 months later depending on intercalary status
    best_compatible_path: bool
    month_lengths_compatible: bool
    _actual_year: int  # Underscore to hide from JSON output
    _intercalary: Intercalary
    months: List[PotentialMonthResult]

    def can_be_followed_by(self, potential2: PotentialYearResult) -> bool:
        # Years are incompatible if the year afterwards does not start when this one ends
        # Although we can only do this check if we know the length of this year for certain
        # noinspection PyProtectedMember
        if (
            self._intercalary != Intercalary.UNKNOWN
            and self._actual_year == potential2._actual_year - 1
        ):
            if potential2.nisan_1 != self.next_nisan:
                return False
        return True


@dataclass
class YearResult(Result):
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
                if k.startswith("_"):
                    dict.pop(k)
            return dict
        if type(o) == Intercalary:
            return o.value
        if type(o) == TimeValue:
            return o.format(self.ts)
        return super().default(o)


@dataclass
class YearToTest:
    index: int
    name: str
    intercalary: Intercalary
    func: Callable[[float], List[MonthResult]]


class AbstractTablet(ABC):
    INVALID_MONTH_LENGTH_PENALTY = 0.8

    tests: List[YearToTest]
    scores_title: str

    def __init__(
        self, data: AstroData, db: Database, tests: List[YearToTest], scores_title: str
    ):
        """
        Constructor for an Abstract Query Tablet, should be called by all subclasses.
        @param data: Reference to the Astronomical Data files.
        @param db: A connection to the generated database for this tablet.
        @param tests: A set of tests we are querying.
        @param scores_title: The title the scores output should be given.
        """
        # Validate tests are setup correctly
        if tests[0].index != 0:
            raise RuntimeError("First test index must be 0")
        self.data = data
        self.db = db
        self.tests = tests
        self.scores_title = scores_title

    def repeat_month_with_alternate_starts(
        self,
        nisan_1: float,
        month_number: int,
        func: Callable[[List[BabylonianDay]], List[AbstractQuery]],
        name=None,
        length=MonthLength.UNKNOWN,
    ) -> MonthResult:
        """
        Tries repeating the same set of month observations but starting at different dates for first lunar visibility
        (either the first or one day later)
        @param nisan_1: The time of first possible lunar visibility at sunset
        @param month_number: The month number in the year
        @param func: Individual queries for the month
        @param name: Name of the month
        @param length: If the month is confirmed to be 29 or 30 days long
        @return: A MonthResult
        """
        assert 1 <= month_number <= 13
        months = self.db.get_months(nisan_1)
        month_days = self.db.get_days(months[month_number - 1])
        name = name if name is not None else roman.toRoman(month_number)
        all_results = []
        for start_offset in range(0, 2):
            results = func(month_days[start_offset:])
            score = sum(item.quality_score() for item in results)
            output = list(
                map(
                    lambda x: {
                        **x.output(),
                        **{"score": x.quality_score()},
                        **x.get_search_range().output(),
                    },
                    results,
                )
            )
            sunset_one = TimeValue(month_days[start_offset].sunset)
            first_vis = TimeValue(month_days[0].sunset)
            next_month = None
            if length == MonthLength.TWENTY_NINE:
                next_month = TimeValue(month_days[start_offset + 29].sunset)
            elif length == MonthLength.THIRTY:
                next_month = TimeValue(month_days[start_offset + 30].sunset)
            all_results.append(
                PotentialMonthResult(
                    score=score,
                    name=name,
                    actual_month=month_number,
                    month_sunset_1=sunset_one,
                    next_month_sunset_1=next_month,
                    first_visibility=first_vis,
                    days_late=start_offset,
                    observations=output,
                    _length=length,
                )
            )
        all_results.sort(key=lambda x: x.score, reverse=True)
        return MonthResult(all_results)

    def repeat_year_with_alternate_starts(
        self,
        potential_years: List[PotentialYear],
        name: str,
        intercalary: Intercalary,
        func: Callable[[float], List[MonthResult]],
    ) -> YearResult:
        """
        Tries repeating the same set of year observations, but starting at different possible dates for Nisan 1
        Returns a list in order of highest score, descending
        @param potential_years: Possible start dates for a given year
        @param name: The name the year is referenced as within the tablet
        @param intercalary: Whether this year is known to be intercalary or not
        @param func: The month queries
        @return: A YearResult
        """
        all_results = []
        vernal = self.db.nearest_event_match_to_time(
            SUN, VERNAL_EQUINOX, potential_years[0].nisan_1
        )
        if vernal is None:
            raise RuntimeError("Unable to find vernal equinox time")
        year_number = potential_years[0].year
        for y in potential_years:
            months = self.db.get_months(y.nisan_1, count=14)
            if intercalary.is_intercalary():
                # Exclude a late start if this year is intercalary, i.e. make sure that whichever year
                # would follow this one is still valid
                next_nisan = months[13]
                next_vernal = self.db.nearest_event_match_to_time(
                    SUN, VERNAL_EQUINOX, next_nisan
                )
                if abs(next_vernal - next_nisan) > MAX_NISAN_EQUINOX_DIFF_DAYS:  # type: ignore
                    continue
            else:
                next_nisan = months[12]
            results = func(y.nisan_1)
            compatible_paths: List[
                List[PotentialMonthResult]
            ] = generate_compatible_combinations(results)
            compatible_paths.sort(key=lambda y: sum(x.score for x in y), reverse=True)
            if len(compatible_paths) == 0:
                months_list = list(map(lambda x: x.potentials[0], results))
                total_score = (
                    sum(item.score for item in months_list)
                    * self.INVALID_MONTH_LENGTH_PENALTY
                )
            else:
                months_list = compatible_paths[0]
                total_score = sum(item.score for item in months_list)
            all_results.append(
                PotentialYearResult(
                    score=total_score,
                    nisan_1=TimeValue(y.nisan_1),
                    next_nisan=TimeValue(next_nisan),
                    months=months_list,
                    _intercalary=intercalary,
                    _actual_year=year_number,
                    best_compatible_path=False,
                    month_lengths_compatible=len(compatible_paths) > 0,
                )
            )
        all_results.sort(key=lambda x: x.score, reverse=True)
        return YearResult(
            name, year_number, TimeValue(vernal), intercalary, all_results
        )

    @staticmethod
    def _total_year_score(yrs: List[YearResult]) -> float:
        compatible_products: List[
            List[PotentialYearResult]
        ] = generate_compatible_combinations(yrs)
        assert len(compatible_products) > 0
        compatible_products.sort(key=lambda y: sum(x.score for x in y), reverse=True)
        for e in compatible_products[0]:
            e.best_compatible_path = True
        return sum(x.score for x in compatible_products[0])

    def try_multiple_months(
        self,
        nisan_1: float,
        start: int,
        end: int,
        fn: Callable[[List[BabylonianDay]], List[AbstractQuery]],
        comment=None,
    ) -> MonthResult:
        """
        Useful when the month number is not clear / damaged
        @param nisan_1: The start of the year
        @param start: The first month number to scan from
        @param end: The last month number to test (inclusive)
        @param fn: The individual queries for the month
        @param comment: A comment describing this month
        @return: The best MonthResult that was found
        """
        attempts: List[MonthResult] = []
        comment = (
            "Unknown month between {} and {}".format(start, end)
            if comment is None
            else comment
        )
        for m in range(start, end + 1):
            attempts.append(
                self.repeat_month_with_alternate_starts(nisan_1, m, fn, name=comment)
            )
        attempts.sort(key=lambda x: x.potentials[0].score, reverse=True)
        return attempts[0]

    def _run_years(self, progress: PROGRESS_CALLBACK) -> List[MultiyearResult]:
        years = self.db.get_years()
        results = []
        max_index = max(d.index for d in self.tests)
        range_top = len(years) - max_index
        if range_top < 0:
            raise RuntimeError("Data range must be greater or equal to query range")
        for i in range(0, range_top):
            if progress:
                progress(i / range_top)
            yrs: List[YearResult] = []
            for idx, x in enumerate(self.tests):
                yrs.append(
                    self.repeat_year_with_alternate_starts(
                        years[i + x.index], x.name, x.intercalary, x.func
                    )
                )
            total_score = self._total_year_score(yrs)
            results.append(MultiyearResult(years[i][0].year, total_score, yrs))
        if progress:
            progress(1.0)
        return results

    def write_scores(self, path: str, progress: PROGRESS_CALLBACK) -> None:
        """
        Computes and outputs the score for each base year in the database in descending order.
        @param progress: Callback to report on computation progress.
        @param path: The path to save the scores file.
        """
        results = self._run_years(progress)
        results.sort(key=lambda x: x.best_score, reverse=True)
        info_text = (
            f"Database generated on {self.db.info.time} for {self.db.info.tablet} "
            f"covering {self.db.info.start_year} to {self.db.info.end_year}"
        )
        lines = [info_text, f"Scores for {self.scores_title}", "Year   Score"]
        for i in results:
            lines.append(f"{i.base_year} {i.best_score}")
        with open(path, "w") as file:
            file.write("\n".join(lines))

    def write_single_year(self, base_year: int, full_results: bool, path: str):
        """
        Computes and outputs detailed results for a single base year.
        @param base_year: The year (AD) to use.
        @param full_results: Whether all possible year results should be output.
        @param path: The path to save the JSON file.
        """

        # Filter so that base_year has the first index in the list
        years = list(
            filter(lambda y_list: y_list[0].year >= base_year, self.db.get_years())
        )
        yrs: List[YearResult] = []
        for idx, x in enumerate(self.tests):
            yrs.append(
                self.repeat_year_with_alternate_starts(
                    years[x.index], x.name, x.intercalary, x.func
                )
            )
        total_score = self._total_year_score(yrs)
        year_to_print = MultiyearResult(base_year, total_score, yrs)

        if full_results is False:
            for y in year_to_print.years:
                y.potentials = list(
                    filter(lambda x: x.best_compatible_path is True, y.potentials)
                )

        with open(path, "w") as outfile:
            encoder = EnhancedJSONEncoder(self.data.timescale, indent=2)
            raw = encoder.encode(year_to_print)
            outfile.write(raw)
