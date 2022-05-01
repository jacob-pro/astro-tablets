from astro_tablets.data import *
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.generate.planet_events import OuterPlanetPhenomena
from astro_tablets.query.database import BabylonianDay
from astro_tablets.query.abstract_query import SearchRange, AbstractQuery
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.abstract_tablet import AbstractTablet, MonthResult, YearToTest, Intercalary


class BM76738(AbstractTablet):

    def year_1_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, SearchRange.any_day(month))]

    def year_1_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 24)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_1(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 4, self.year_1_month_unknown)
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_1_month_4)
        return [month_a, month_4]


    def year_2_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.x_plus(month, 10)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_2_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        any_day = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, any_day)
        res2 = AngularSeparationQuery(self.db, SATURN, EPSILON_LEONIS, 0, 20, None, any_day)
        return [res1, res2]

    def year_2(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_2_month_4)
        month_5 = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_2_month_5)
        return [month_4, month_5]


    def year_3_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 7)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_3_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 16)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, REGULUS, 0, 20, EclipticPosition.BEHIND, range)
        return [res1, res2]

    def year_3(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_3_month_4)
        month_5 = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_3_month_5)
        return [month_4, month_5]


    def year_4_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 29)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_4_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, LEO.central_star, 0, LEO.radius, None, range)
        return [res1, res2]

    def year_4(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_4_month_4)
        month_b = self.try_multiple_months(nisan_1, 5, 12, self.year_4_month_unknown)
        return [month_4, month_b]


    def year_5_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 23)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_5_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 29)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_5(self, nisan_1: float) -> List[MonthResult]:
        month_5 = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_5_month_5)
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_5_month_6)
        return [month_5, month_6]


    def year_6_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 20)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_6_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 22)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, BETA_VIRGINIS, 0, 20, EclipticPosition.BEHIND, range)
        return [res1, res2]

    def year_6(self, nisan_1: float) -> List[MonthResult]:
        month_5 = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_6_month_5)
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_6_month_6)
        return [month_5, month_6]


    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.x_plus(month, 10)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 15)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, VIRGO.central_star, 0, VIRGO.radius, None, range)
        return [res1, res2]

    def year_7(self, nisan_1: float) -> List[MonthResult]:
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_7_month_6)
        month_7 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_7_month_7)
        return [month_6, month_7]

    def year_8_month_vi2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, VIRGO.central_star, 0, VIRGO.radius, None, range)
        return [res1, res2]

    def year_8_month_vii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, VIRGO.central_star, 0, VIRGO.radius, None, range)
        return [res1, res2]

    def year_8(self, nisan_1: float) -> List[MonthResult]:
        # Intercalary Ululu so offset by one
        month_6 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_8_month_vi2)
        month_7 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_8_month_vii)
        return [month_6, month_7]


    def year_9_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_9_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, LIBRA.central_star, 0, LIBRA.radius, None, range)
        return [res1, res2]

    def year_9(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_9_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 12, self.year_9_month_b)
        return [month_a, month_b]


    def year_10_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 20)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, LIBRA.central_star, 0, LIBRA.radius, None, range)
        return [res1, res2]

    def year_10_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 23)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, ANTARES, 0, 20, EclipticPosition.AHEAD, range)
        return [res1, res2]

    def year_10(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_10_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 13, self.year_10_month_b)
        return [month_a, month_b]


    def year_11_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 13)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_11_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, ANTARES, 0, 20, EclipticPosition.ABOVE, range)
        return [res1, res2]

    def year_11(self, nisan_1: float) -> List[MonthResult]:
        month_7 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_11_month_7)
        month_b = self.try_multiple_months(nisan_1, 7, 12, self.year_11_month_unknown)
        return [month_7, month_b]


    def year_12_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 5)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_12_month_9(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, SAGITTARIUS.central_star, 0, SAGITTARIUS.radius, None, range)
        return [res1, res2]

    def year_12(self, nisan_1: float) -> List[MonthResult]:
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_12_month_8)
        month_9 = self.repeat_month_with_alternate_starts(nisan_1, 9, self.year_12_month_9)
        return [month_8, month_9]


    def year_13_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 26)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_13_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 1)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = AngularSeparationQuery(self.db, SATURN, SAGITTARIUS.central_star, 0, SAGITTARIUS.radius, None, range)
        return [res1, res2]

    def year_13(self, nisan_1: float) -> List[MonthResult]:
        month_8 = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_13_month_8)
        month_10 = self.repeat_month_with_alternate_starts(nisan_1, 10, self.year_13_month_10)
        return [month_8, month_10]


    def year_14_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_14_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_14(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_14_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 12, self.year_14_month_b)
        return [month_a, month_b]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Kandalanu 1", Intercalary.UNKNOWN, self.year_1),
                 YearToTest(1, "Kandalanu 2", Intercalary.UNKNOWN, self.year_2),
                 YearToTest(2, "Kandalanu 3", Intercalary.UNKNOWN, self.year_3),
                 YearToTest(3, "Kandalanu 4", Intercalary.FALSE, self.year_4),
                 YearToTest(4, "Kandalanu 5", Intercalary.ULULU, self.year_5),
                 YearToTest(5, "Kandalanu 6", Intercalary.FALSE, self.year_6),
                 YearToTest(6, "Kandalanu 7", Intercalary.FALSE, self.year_7),
                 YearToTest(7, "Kandalanu 8", Intercalary.ULULU, self.year_8),
                 YearToTest(8, "Kandalanu 9", Intercalary.FALSE, self.year_9),
                 YearToTest(9, "Kandalanu 10", Intercalary.ADDARU, self.year_10),
                 YearToTest(10, "Kandalanu 11", Intercalary.FALSE, self.year_11),
                 YearToTest(11, "Kandalanu 12", Intercalary.UNKNOWN, self.year_12),
                 YearToTest(12, "Kandalanu 13", Intercalary.UNKNOWN, self.year_13),
                 YearToTest(13, "Kandalanu 14", Intercalary.UNKNOWN, self.year_14),
                 ]
        res = self.run_years(tests)
        self.print_results(res, "Kandalanu year 1")
        self.output_json_for_year(res, print_year, slim_results)
