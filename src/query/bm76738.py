from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import OuterPlanetPhenomena
from query.database import BabylonianDay
from query.result import PlanetaryEventResult, SearchRange, AngularSeparationResult, AbstractResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult, YearToTest, Intercalary


class BM76738(AbstractTablet):

    def year_1_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        return [PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.LA, SearchRange.any_day(month))]

    def year_1_month_4(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day24 = SearchRange.for_night(month, 24)
        res1 = PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.FA, day24)
        # TODO add cancer
        return [res1]

    def year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 4, self.year_1_month_unknown)
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_1_month_4)
        return [month_a, month_4]


    def year_2_month_4(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        range = SearchRange(month[10].sunset, month[29].sunrise, "Day 10+")
        return [PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_2_month_5(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        any_day = SearchRange.any_day(month)
        res1 = PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.FA, any_day)
        res2 = AngularSeparationResult(self.db, SATURN, EPSILON_LEONIS, 0, 10, None, any_day)
        return [res1, res2]

    def year_2(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_2_month_4)
        month_5 = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_2_month_5)
        return [month_4, month_5]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None]):
        tests = [YearToTest(0, "Kandalanu 1", Intercalary.UNKNOWN, self.year_1),
                 YearToTest(1, "Kandalanu 2", Intercalary.UNKNOWN, self.year_2)
                 ]
        res = self.run_years(tests)
        self.print_results(res, "Kandalanu year 1")
        self.output_json_for_year(res, print_year)
