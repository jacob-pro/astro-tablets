from data import *
from generate.angular_separation import EclipticPosition
from query.database import BabylonianDay
from query.abstract_query import SearchRange, AbstractQuery
from query.angular_separation_query import AngularSeparationQuery
from query.lunar_eclipse_query import FirstContactTime, FirstContactRelative, ExpectedEclipseType, LunarEclipseQuery
from query.tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary


class BM35115(AbstractTablet):

    def year_0_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        return [LunarEclipseQuery(self.db, FirstContactTime(40, FirstContactRelative.AFTER_SUNRISE),
                                  ExpectedEclipseType.UNKNOWN,
                                  SearchRange.any_day(month))]

    def year_0_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        return [LunarEclipseQuery(self.db, FirstContactTime(30, FirstContactRelative.BEFORE_SUNSET),
                                  ExpectedEclipseType.UNKNOWN,
                                  SearchRange.any_day(month))]

    def year_0(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_2 = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_0_month_2)
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_0_month_8)
        return [month_2, month_8]


    def year_2_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 14)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, range)]

    def year_2(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_1 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_2_month_1)
        return [month_1]


    def year_18_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        return [LunarEclipseQuery(self.db, FirstContactTime(10, FirstContactRelative.BEFORE_SUNSET),
                                  ExpectedEclipseType.UNKNOWN,
                                  SearchRange.any_day(month))]


    def year_18_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 13)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, range)]

    def year_18(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_2 = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_18_month_2)
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_18_month_8)
        return [month_2, month_8]


    def year_36_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day15 = SearchRange.for_night(month, 15)
        res1 = LunarEclipseQuery(self.db, None, ExpectedEclipseType.PARTIAL, day15)
        res2 = AngularSeparationQuery(self.db, MOON, ANTARES, 0, 20, EclipticPosition.BEHIND, day15)
        return [res1, res2]

    def year_36(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_3 = self.repeat_month_with_alternate_starts(nisan_1, 3, self.year_36_month_3)
        return [month_3]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Shamashshumukin Acc.", Intercalary.UNKNOWN, self.year_0),
                 YearToTest(2, "Shamashshumukin 2", Intercalary.UNKNOWN, self.year_2),
                 YearToTest(18, "Shamashshumukin 18", Intercalary.UNKNOWN, self.year_18),
                 YearToTest(36, "Kandalanu 16", Intercalary.UNKNOWN, self.year_36),
                 ]
        res = self.run_years(tests)
        self.print_results(res, "Shamashshumukin Acc.")
        self.output_json_for_year(res, print_year, slim_results)
