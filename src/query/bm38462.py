from data import *
from generate.angular_separation import EclipticPosition
from query.abstract_query import SearchRange, AbstractQuery
from query.angular_separation_query import AngularSeparationQuery
from query.database import BabylonianDay
from query.lunar_eclipse_query import FirstContactTime, FirstContactRelative, ExpectedEclipseType, LunarEclipseQuery, \
    EclipsePosition, SeparatePhaseTimings
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary


class BM38462(AbstractTablet):

    def year_1_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1  [Year I of Nebukad]nezar. Month III, omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_1_month_4_plus(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 2  [Month IX,] omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.repeat_month_with_alternate_starts(nisan_1, 3, self.year_1_month_3)
        month_b = self.try_multiple_months(nisan_1, 4, 12, self.year_1_month_4_plus)
        return [month_a, month_b]


    def year_2_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 3  [Year 2. Month II,] (after) 5? (months), omitted. Month VI was intercalary.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_2_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 2  [Month IX,] omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_2(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 5, self.year_2_month_a)
        month_b = self.try_multiple_months(nisan_1, 8, 13, self.year_2_month_b)  # Intercalary Ululu
        return [month_a, month_b]


    def year_3_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 7  [Year 3.] Month I, omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_3_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 7  Month VII, omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_3(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_3_month_1)
        month_b = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_3_month_7)
        return [month_a, month_b]


    def year_4_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 8  [Year 4. M]onth I, the 13th, middle watch, 3 bēru 5° after sunset,
        # 9  it began in the west and north. Three quarters
        # 10 [was covered.] It cleared in the north. The north wind blew.
        t = (3 * 30) + 5
        return [LunarEclipseQuery(self.db, FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                                  ExpectedEclipseType.PARTIAL, None, None,
                                  SearchRange.for_night_and_day(month, 13))]

    def year_4_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 11 Month VII, omitted.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_4(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_4_month_1)
        month_b = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_4_month_7)
        return [month_a, month_b]


    def year_5_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 [Year 5. Month I, omitted.]
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_5_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 Month VI₂, om[itted.]
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_5_month_c(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 13 [Month XI,] (after) 5 months, 3 ½ bēru after sunset,
        # 14 [....] two-thirds was covered. In the south it was covered. In the west? [it cleared.]
        # 15 [In?] its eclipse, .... [....]
        t = (3.5 * 30)
        return [LunarEclipseQuery(self.db, FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                                  ExpectedEclipseType.PARTIAL, None, None,
                                  SearchRange.any_day(month))]

    def year_5(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_5_month_a)
        month_b = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_5_month_7)
        month_c = self.try_multiple_months(nisan_1, 8, 13, self.year_5_month_c)
        return [month_a, month_b, month_c]

    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Nebuchadnezzar 1", Intercalary.FALSE, self.year_1),
                 YearToTest(1, "Nebuchadnezzar 2", Intercalary.ULULU, self.year_2),
                 YearToTest(2, "Nebuchadnezzar 3", Intercalary.FALSE, self.year_3),
                 YearToTest(3, "Nebuchadnezzar 4", Intercalary.FALSE, self.year_4),
                 YearToTest(4, "Nebuchadnezzar 5", Intercalary.ULULU, self.year_5),
                 YearToTest(1, "Nebuchadnezzar 10", Intercalary.FALSE, self.year_10),
                 YearToTest(10, "Nebuchadnezzar 11", Intercalary.ADDARU, self.year_11),
                 YearToTest(11, "Nebuchadnezzar 12", Intercalary.FALSE, self.year_12),
                 YearToTest(12, "Nebuchadnezzar 13", Intercalary.FALSE, self.year_13),
                 YearToTest(13, "Nebuchadnezzar 14", Intercalary.ADDARU, self.year_14),
                 YearToTest(14, "Nebuchadnezzar 15", Intercalary.FALSE, self.year_15),
                 YearToTest(15, "Nebuchadnezzar 16", Intercalary.FALSE, self.year_16),
                 YearToTest(16, "Nebuchadnezzar 17", Intercalary.ADDARU, self.year_17),
                 YearToTest(23, "Nebuchadnezzar 24", Intercalary.FALSE, self.year_24),
                 YearToTest(24, "Nebuchadnezzar 25", Intercalary.FALSE, self.year_25),
                 YearToTest(25, "Nebuchadnezzar 26", Intercalary.FALSE, self.year_26),
                 YearToTest(26, "Nebuchadnezzar 27", Intercalary.ADDARU, self.year_27),
                 YearToTest(27, "Nebuchadnezzar 28", Intercalary.FALSE, self.year_28),
                 YearToTest(28, "Nebuchadnezzar 29", Intercalary.ADDARU, self.year_29),
                 ]
        res = self.run_years(tests)
        self.print_results(res, "Nebuchadnezzar 1")
        self.output_json_for_year(res, print_year, slim_results)
