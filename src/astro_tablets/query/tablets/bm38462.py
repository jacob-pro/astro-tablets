from typing import List

from astro_tablets.constants import BERU_US
from astro_tablets.data import AstroData
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.abstract_tablet import (
    AbstractTablet,
    Intercalary,
    MonthResult,
    YearToTest,
)
from astro_tablets.query.database import BabylonianDay, Database
from astro_tablets.query.lunar_eclipse_query import (
    CompositePhaseTiming,
    ExpectedEclipseType,
    FirstContactRelative,
    FirstContactTime,
    LunarEclipseQuery,
)


class BM38462(AbstractTablet):
    def year_1_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1  [Year I of Nebukad]nezar. Month III, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_1_month_4_plus(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 2  [Month IX,] omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_1(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 3, self.year_1_month_3
        )
        month_b = self.try_multiple_months(nisan_1, 4, 12, self.year_1_month_4_plus)
        return [month_a, month_b]

    def year_2_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 3  [Year 2. Month II,] (after) 5? (months), omitted. Month VI was intercalary.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_2_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 4  [Month VII, the 1]4th?, 1 ⅔ bēru 5°, variant 1 ½ bēru, after sunset,
        # 5  it began in the [....] north; half was covered. In the north and west it began
        # 6  [to cl]ear. [1] ½ bēru onset and clearing. The west wind blew.
        t = 1.5 * BERU_US
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.PARTIAL,
                CompositePhaseTiming(0.5 * BERU_US),
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_2(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 5, self.year_2_month_a)
        month_b = self.try_multiple_months(
            nisan_1, 8, 13, self.year_2_month_b
        )  # Intercalary Ululu
        return [month_a, month_b]

    def year_3_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 7  [Year 3.] Month I, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_3_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 7  Month VII, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_3(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_3_month_1
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_3_month_7
        )
        return [month_a, month_b]

    def year_4_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 8  [Year 4. M]onth I, the 13th, middle watch, 3 bēru 5° after sunset,
        # 9  it began in the west and north. Three quarters
        # 10 [was covered.] It cleared in the north. The north wind blew.
        t = (3 * BERU_US) + 5
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.PARTIAL,
                None,
                None,
                SearchRange.for_night_and_day(month, 13),
            )
        ]

    def year_4_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 11 Month VII, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_4(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_4_month_1
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_4_month_7
        )
        return [month_a, month_b]

    def year_5_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 [Year 5. Month I, omitted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_5_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 Month VI₂, om[itted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_5_month_c(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 13 [Month XI,] (after) 5 months, 3 ½ bēru after sunset,
        # 14 [....] two-thirds was covered. In the south it was covered. In the west? [it cleared.]
        # 15 [In?] its eclipse, .... [....]
        t = 3.5 * BERU_US
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.PARTIAL,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_5(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_5_month_a
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_5_month_7
        )
        month_c = self.try_multiple_months(nisan_1, 8, 13, self.year_5_month_c)
        return [month_a, month_b, month_c]

    def year_10_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1  Month VIII, [....] .... [....]
        # 2  It cleared [in the west] and south [....] ⅔ bēru after [sunset?]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_10(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_10_month_8
        )
        return [month_a]

    def year_11_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 3  Year 11. Month II, [....] 10° after sunset it began
        # 4  it was total, and 10? [....]
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(10, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.TOTAL,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_11_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 4  Month VIII, omitted. Month XII was intercalary.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_11(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_11_month_2
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_11_month_8
        )
        return [month_a, month_b]

    def year_12_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5  Year 12. Month [I, omitted]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_12_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5  Month VII. omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_12_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 6  Month XII, the 15th. 10? [....nn]° after sunset [....]
        # 7  1 bēru 6° onset [and clearing.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.PARTIAL_OR_TOTAL,
                CompositePhaseTiming((1 * BERU_US) + 6),
                None,
                SearchRange.for_night_and_day(month, 15),
            )
        ]

    def year_12(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 6, self.year_12_month_a)
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_12_month_7
        )
        month_c = self.repeat_month_with_alternate_starts(
            nisan_1, 12, self.year_12_month_12
        )
        return [month_a, month_b, month_c]

    def year_13_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 8  Year 13. Month VI, [omitted]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_13_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 9  [Month XII, the 1]4th. it came out eclipsed. I bēru 10° [....]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.PARTIAL_OR_TOTAL,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_13(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_13_month_6
        )
        month_b = self.try_multiple_months(nisan_1, 7, 12, self.year_13_month_b)
        return [month_a, month_b]

    def year_14_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 10 [Year 1]4. [Month] VI, [omitted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_14_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 11 [Month XII. omitt]ed .... Month XII [was intercalary]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_14(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_14_month_6
        )
        month_b = self.try_multiple_months(nisan_1, 7, 12, self.year_14_month_b)
        return [month_a, month_b]

    def year_15_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 [Year 1]5. Month V, [omitt]ed.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_15_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12 Month X[I, omitted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_15(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_15_month_5
        )
        month_b = self.try_multiple_months(nisan_1, 10, 12, self.year_15_month_b)
        return [month_a, month_b]

    def year_16_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 13 [Year] 16. Month IV, [omitted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_16_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 14 [Month X,] the 14th. morning watch. ⅔ bēru before sunrise?.
        # 15 half of it was covered. [It set] eclipsed.
        t = 2 / 3 * BERU_US
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.BEFORE_SUNRISE),
                ExpectedEclipseType.PARTIAL,
                None,
                None,
                SearchRange.for_night_and_day(month, 14),
            )
        ]

    def year_16(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_16_month_4
        )
        month_b = self.try_multiple_months(nisan_1, 5, 12, self.year_16_month_b)
        return [month_a, month_b]

    def year_17_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 16 [Year] 17. Month IV, [omitted.]
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_17_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 17 [Month] X, the 13th, morning watch. 1 bēru 5° [before sunrise?]
        # 18 all of it was covered. [It set eclips]ed.
        t = (1 * BERU_US) + 5
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.BEFORE_SUNRISE),
                ExpectedEclipseType.TOTAL,
                None,
                None,
                SearchRange.for_night_and_day(month, 13),
            )
        ]

    def year_17(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_17_month_4
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 10, self.year_17_month_10
        )
        return [month_a, month_b]

    def year_24_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1'  [....] .... [....]
        # 2'  .... beginning of night, onset [....]
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(0, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_24(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_24_month_a)
        return [month_a]

    def year_25_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 3'  Year 25. Month V, 1 ½ bēru after sunset.
        t = 1.5 * BERU_US
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_25_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 4'  Month XI, evening watch, onset.
        # USAN = "first part of the night" (evening watch)
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(25, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_25(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_25_month_5
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 11, self.year_25_month_11
        )
        return [month_a, month_b]

    def year_26_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5'  Year 26. Month V, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_26_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 5'  Month XI, omitted. Month XII was intercalary.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_26(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_26_month_5
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 11, self.year_26_month_11
        )
        return [month_a, month_b]

    def year_27_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 6'  Year 27. Month III, (after) 5 (months), omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_27_month_9(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 6'  Month IX, omitted.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.UNKNOWN,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_27(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 3, self.year_27_month_3
        )
        month_b = self.repeat_month_with_alternate_starts(
            nisan_1, 9, self.year_27_month_9
        )
        return [month_a, month_b]

    def year_28_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 7'  Year 28. Month III, the 14th, ....
        # 8'  [....] .... [....] finger remaining
        # 9'  [....nn]°, it set eclipsed.
        return [
            LunarEclipseQuery(
                self.db,
                None,
                ExpectedEclipseType.PARTIAL_OR_TOTAL,
                None,
                None,
                SearchRange.for_night_and_day(month, 14),
            )
        ]

    def year_28_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 10' [Month IX, the 1]5th? 3 ½ bēru after sunset,
        # 11' it began [in] the east. All of it was covered.
        # 12· It cleared? in the west?. [nn] bēru onset and clearing.
        t = 3.5 * BERU_US
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                ExpectedEclipseType.TOTAL,
                None,
                None,
                SearchRange.any_day(month),
            )
        ]

    def year_28(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 3, self.year_28_month_3
        )
        month_b = self.try_multiple_months(
            nisan_1, 4, 13, self.year_28_month_b
        )  # Intercalary
        return [month_a, month_b]

    def year_29_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 13' Year 29. [Mon]th II, the 14th, [....]
        # 14' 1 bēru 10° before sunrise,
        t = (1 * BERU_US) + 10
        return [
            LunarEclipseQuery(
                self.db,
                FirstContactTime(t, FirstContactRelative.BEFORE_SUNRISE),
                ExpectedEclipseType.PARTIAL_OR_TOTAL,
                None,
                None,
                SearchRange.for_night_and_day(month, 14),
            )
        ]

    def year_29(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_29_month_2
        )
        return [month_a]

    def __init__(self, data: AstroData, db: Database):
        tests = [
            YearToTest(0, "Nebuchadnezzar 1", Intercalary.FALSE, self.year_1),
            YearToTest(1, "Nebuchadnezzar 2", Intercalary.ULULU, self.year_2),
            YearToTest(2, "Nebuchadnezzar 3", Intercalary.FALSE, self.year_3),
            YearToTest(3, "Nebuchadnezzar 4", Intercalary.FALSE, self.year_4),
            YearToTest(4, "Nebuchadnezzar 5", Intercalary.ULULU, self.year_5),
            YearToTest(9, "Nebuchadnezzar 10", Intercalary.FALSE, self.year_10),
            YearToTest(10, "Nebuchadnezzar 11", Intercalary.ADDARU, self.year_11),
            YearToTest(11, "Nebuchadnezzar 12", Intercalary.FALSE, self.year_12),
            YearToTest(12, "Nebuchadnezzar 13", Intercalary.FALSE, self.year_13),
            YearToTest(13, "Nebuchadnezzar 14", Intercalary.ADDARU, self.year_14),
            YearToTest(14, "Nebuchadnezzar 15", Intercalary.FALSE, self.year_15),
            YearToTest(15, "Nebuchadnezzar 16", Intercalary.FALSE, self.year_16),
            YearToTest(16, "Nebuchadnezzar 17", Intercalary.ADDARU, self.year_17),
            YearToTest(23, "Nebuchadnezzar 24", Intercalary.FALSE, self.year_24),
            YearToTest(24, "Nebuchadnezzar 25", Intercalary.FALSE, self.year_25),
            YearToTest(25, "Nebuchadnezzar 26", Intercalary.ADDARU, self.year_26),
            YearToTest(26, "Nebuchadnezzar 27", Intercalary.FALSE, self.year_27),
            YearToTest(27, "Nebuchadnezzar 28", Intercalary.ADDARU, self.year_28),
            YearToTest(28, "Nebuchadnezzar 29", Intercalary.FALSE, self.year_29),
        ]
        super().__init__(data, db, tests, "Nebuchadnezzar 1")
