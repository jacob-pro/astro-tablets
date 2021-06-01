from data import *
from generate.angular_separation import EclipticPosition
from query.abstract_query import SearchRange, AbstractQuery
from query.database import BabylonianDay
from query.lunar_eclipse_query import FirstContactTime, FirstContactRelative, ExpectedEclipseType, LunarEclipseQuery, \
    CompositePhaseTiming, EclipsePosition
from query.tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary


class BM35115(AbstractTablet):

    def year_0_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1 Accession year of Šamaš-šumu-ukīn.
        # 2 month II, (after) 5 months;
        # 3 (eclipse) which was omitted.
        # 4 At 40° after sunrise.
        return [LunarEclipseQuery(self.db, FirstContactTime(40, FirstContactRelative.AFTER_SUNRISE),
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_0_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5 Month VIII, (eclipse) which was omitted.
        # 6 At 30° before sunset.
        return [LunarEclipseQuery(self.db, FirstContactTime(30, FirstContactRelative.BEFORE_SUNSET),
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_0(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_2 = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_0_month_2)
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_0_month_8)
        return [month_2, month_8]


    def year_2_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 4' (Year) 2, month I, the 14th, ....
        # 5' began?. At 3°? [....]
        # 6' after sunset.
        range = SearchRange.for_night(month, 14)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, None, None, range)]

    def year_2(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_1 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_2_month_1)
        return [month_1]


    def year_18_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1 (Year) 18 of Šamaš-šumu-ukīn,
        # 2 month II, (after) 5 months,
        # 3 (eclipse) which was omitted.
        # 4 At 1,0° before sunset.
        t = (1 * 60) + 0
        return [LunarEclipseQuery(self.db, FirstContactTime(t, FirstContactRelative.BEFORE_SUNSET),
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]


    def year_18_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5 Month VIII, the 13th, .... [....]
        # 6 and south [....]
        range = SearchRange.for_night_and_day(month, 13)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, None, None, range)]

    def year_18(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_2 = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_18_month_2)
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_18_month_8)
        return [month_2, month_8]


    def year_36_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1 (Year) 16 of Kandalānu,
        # 2 month III, (after) 5 months, the 15th, 2 fin[gers?]
        # 3 between north and east were covered.
        # 4 It cleared in the north. The north wind b[lew?.]
        # 5 20° onset, maximal phase, [and clearing ....]
        # 6 behind α Scorpii [it was eclipsed.]
        day15 = SearchRange.for_night_and_day(month, 15)
        location = EclipsePosition(ANTARES, 0, 20, EclipticPosition.BEHIND)
        res1 = LunarEclipseQuery(self.db, None, ExpectedEclipseType.PARTIAL, CompositePhaseTiming(20), location, day15)
        return [res1]

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
