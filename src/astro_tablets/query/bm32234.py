from astro_tablets.data import *
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import SearchRange, AbstractQuery
from astro_tablets.query.abstract_tablet import AbstractTablet, YearToTest, Intercalary, MonthResult
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.database import BabylonianDay
from astro_tablets.query.lunar_eclipse_query import FirstContactTime, FirstContactRelative, ExpectedEclipseType, LunarEclipseQuery, \
    EclipsePosition, SeparatePhaseTimings


class BM32234(AbstractTablet):

    def year_14_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 3' (Year) 14 of Nebukadnezar
        # 4' month VI, (eclipse) which was omitted.
        # 5' With sunrise.
        return [LunarEclipseQuery(self.db, FirstContactTime(0, FirstContactRelative.AFTER_SUNRISE),
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_14_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 6' [Mon]th XII, the 14th, (eclipse) which was omitted.
        # 7' .... after? sunrise?.
        return [LunarEclipseQuery(self.db, None,
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.for_night_and_day(month, 14))]

    def year_14(self, nisan_1: float) -> List[MonthResult]:
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_14_month_6)
        month_12 = self.repeat_month_with_alternate_starts(nisan_1, 12, self.year_14_month_12)
        return [month_6, month_12]


    def year_31_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 1'  [Month XII, ....]
        # 2'  [....] ....
        # 3'  it cleared [from] east to north.
        # 4'  The south wind blew. I cubit
        # 5'  in front of Libra it was eclipsed.
        # 6'  Saturn rose in Capricorn; Mars
        # 7'  was 2 cubits in front of α Scorpii.
        # 8'  At 1,30° after sunset.
        t = (1 * 60) + 30
        range = SearchRange.any_day(month)
        eclipse_pos = EclipsePosition(LIBRA.central_star, 0, LIBRA.radius, EclipticPosition.AHEAD)
        eclipse_time = FirstContactTime(t, FirstContactRelative.AFTER_SUNSET)
        eclipse = LunarEclipseQuery(self.db, eclipse_time, ExpectedEclipseType.PARTIAL_OR_TOTAL, None, eclipse_pos, range)

        if eclipse.best is not None:
            time = eclipse.best['closest_approach_time']
            range = SearchRange(time - 1, time + 1, "Within a day of the eclipse")

        mars = AngularSeparationQuery(self.db, MARS, ANTARES, 2 * CUBIT, 1 * CUBIT, EclipticPosition.AHEAD, range)
        saturn = AngularSeparationQuery(self.db, SATURN, CAPRICORNUS.central_star, 0, CAPRICORNUS.radius, None, range)
        return [eclipse, mars, saturn]

    def year_31(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 13, self.year_31_month_unknown)
        return [month_a]


    def year_32_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 9'  (Year) 32 of Nebukadnezar,
        # 10' month VI, (eclipse) which was omitted.
        # 11' At 35° before sunset.
        return [LunarEclipseQuery(self.db, FirstContactTime(35, FirstContactRelative.BEFORE_SUNSET),
                                  ExpectedEclipseType.UNKNOWN, None, None,
                                  SearchRange.any_day(month))]

    def year_32_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 12' Month XII, the 15th?, ....
        # 13' .... [....]
        range = SearchRange.for_night_and_day(month, 15)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, None, None, range)]

    def year_32(self, nisan_1: float) -> List[MonthResult]:
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_32_month_6)
        month_12 = self.repeat_month_with_alternate_starts(nisan_1, 12, self.year_32_month_12)
        return [month_6, month_12]


    def year_50_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 2' Month VII, the 13th, in 17° on the east side'
        # 3' all was covered; 28° maximal phase.
        # 4' In 20° it cleared from east to west.
        # 5' Its eclipse was red.
        # 6' Behind the rump of Aries it was eclipsed.
        # 7' During onset, the north wind blew, during clearing. the west wind.
        # 8' At 55° before sunrise.
        day13 = SearchRange.for_night_and_day(month, 13)
        eclipse_length = SeparatePhaseTimings(17, 28, 20)
        eclipse_time = FirstContactTime(55, FirstContactRelative.BEFORE_SUNRISE)
        location = EclipsePosition(ARIES.central_star, 0, ARIES.radius, EclipticPosition.BEHIND)
        res1 = LunarEclipseQuery(self.db, eclipse_time, ExpectedEclipseType.TOTAL, eclipse_length, location, day13)
        return [res1]

    def year_50_month_13(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 9' Month XII₂, the 15th [....]
        range = SearchRange.for_night_and_day(month, 15)
        return [LunarEclipseQuery(self.db, None, ExpectedEclipseType.UNKNOWN, None, None, range)]

    def year_50(self, nisan_1: float) -> List[MonthResult]:
        month_7 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_50_month_7)
        month_13 = self.repeat_month_with_alternate_starts(nisan_1, 13, self.year_50_month_13, name="Addaru II")
        return [month_7, month_13]


    def year_68_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # 4'  Month VII, the 11+[xth, ....]
        # 5'  ⅔ of the disk to tota[lity ....]
        # 6'  not total, it set eclipsed.
        # 7'  The north wind which was set to the west side
        # 8'  blew. 5°
        # 9'  in front of η Tauri it was eclipsed.
        # 10' At 14° before [sunrise].
        # Comment: V' 5': the missing word at the end of the line may have meant "was missing"
        # Visibility description kind of unclear
        range = SearchRange.x_plus(month, 11)
        eclipse_time = FirstContactTime(14, FirstContactRelative.BEFORE_SUNRISE)
        location = EclipsePosition(ALCYONE, 0, 15, EclipticPosition.AHEAD)
        res1 = LunarEclipseQuery(self.db, eclipse_time, ExpectedEclipseType.UNKNOWN, None, location, range)
        return [res1]

    def year_68(self, nisan_1: float) -> List[MonthResult]:
        month_7 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_68_month_7)
        return [month_7]


    def do_query(self, subquery: Optional[str], print_year: Optional[int], slim_results: bool):
        tests = [YearToTest(0, "Nebuchadnezzar 14", Intercalary.ADDARU, self.year_14),
                 YearToTest(17, "Nebuchadnezzar 31", Intercalary.ULULU, self.year_31),
                 YearToTest(18, "Nebuchadnezzar 32", Intercalary.FALSE, self.year_32),
                 YearToTest(36, "Nebuchadnezzar 50", Intercalary.ADDARU, self.year_50),
                 YearToTest(54, "Nebuchadnezzar 68", Intercalary.UNKNOWN, self.year_68),
                 ]
        res = self.run_years(tests)
        self.print_results(res, "Nebuchadnezzar 14")
        self.output_json_for_year(res, print_year, slim_results)
