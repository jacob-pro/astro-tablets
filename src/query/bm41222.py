from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena
from query.database import BabylonianDay
from query.abstract_query import SearchRange, AbstractQuery
from query.planetary_event_query import PlanetaryEventQuery
from query.angular_separation_query import AngularSeparationQuery
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary


class BM41222(AbstractTablet):

    ## Shamash-shum-ukin

    def shamash_14_xii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day4 = SearchRange.for_night(month, 4)
        # Mercury's first appearance in the west
        res1 = PlanetaryEventQuery(self.db, MERCURY, InnerPlanetPhenomena.EF, day4)
        # in the area of the Swallow.
        res2 = AngularSeparationQuery(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day4)
        return [res1, res2]

    def shamash_year_14(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 12, self.shamash_14_xii)
        return [res1]


    def shamash_17_ii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day19 = SearchRange.for_night(month, 19)
        # mars was in [the area?] of the Old Man
        res1 = AngularSeparationQuery(self.db, MARS, PERSEUS.central_star, 0, PERSEUS.radius, None, day19)
        # to the right of Mercury
        res2 = AngularSeparationQuery(self.db, MARS, MERCURY, 0, 30, EclipticPosition.AHEAD, day19)
        return [res1, res2]

    def shamash_year_17(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 2, self.shamash_17_ii)
        return [res1]


    def shamash_19_vii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day4 = SearchRange.for_night(month, 4)
        # Mercury stood for ⅔ cubit above? Mars
        res1 = AngularSeparationQuery(self.db, MERCURY, MARS, (2 / 3 * CUBIT), 1 * CUBIT, EclipticPosition.ABOVE, day4)
        return [res1]

    def shamash_year_19(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 7, self.shamash_19_vii)
        return [res1]


    ## Kandalanu

    def kand_1_iii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day28 = SearchRange.for_night(month, 28)
        # Mercury was in the back of Mars?
        res1 = AngularSeparationQuery(self.db, MERCURY, MARS, 0, 30, EclipticPosition.BEHIND, day28)
        day29 = SearchRange.for_night(month, 29)
        # Mercury in the area of the Lion
        res2 = AngularSeparationQuery(self.db, MERCURY, LEO.central_star, 0, LEO.radius, None, day29)
        return [res1, res2]

    def kand_year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, self.kand_1_iii)
        return [res1]


    def kand_12_i(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day8 = SearchRange.for_night(month, 8)
        # Mercury, in the area of Pleiades
        res1 = AngularSeparationQuery(self.db, MERCURY, ALCYONE, 0, 10, None, day8)
        # Mercury was 2 ⅔ cubits above? Mars?
        res2 = AngularSeparationQuery(self.db, MERCURY, MARS, (2 + 2 / 3) * CUBIT, 2 * CUBIT, EclipticPosition.ABOVE, day8)
        return [res1, res2]

    def kand_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.kand_12_i)
        return [res1]


    def kand_16_iii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day20 = SearchRange.for_night(month, 20)
        # Mercury stood 1 cubit 4 fingers behind Mars.
        res1 = AngularSeparationQuery(self.db, MERCURY, MARS, (1 * CUBIT + 4 * FINGER), 1 * CUBIT, EclipticPosition.BEHIND, day20)
        return [res1]

    def kand_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, self.kand_16_iii)
        return [res1]

    # Nabopolassar

    def nabo_7_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # Mercury was balanced 6 fingers above Mars.
        res1 = AngularSeparationQuery(self.db, MERCURY, MARS, 6 * FINGER, 6 * FINGER, EclipticPosition.ABOVE,
                                      SearchRange.any_day(month))
        return [res1]

    def nabo_year_7(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.try_multiple_months(nisan_1, 1, 13, self.nabo_7_unknown)
        return [res1]


    def nabo_12_iv(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day18 = SearchRange.for_night(month, 18)
        # Mars was with Pleiades
        res1 = AngularSeparationQuery(self.db, MARS, ALCYONE, 0, 10, None, day18)
        return [res1]

    def nabo_12_vi(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day13 = SearchRange.for_night(month, 13)
        # Mars was ⅔ cubit above the Chariot
        res1 = AngularSeparationQuery(self.db, MARS, AURIGA.central_star, 0, AURIGA.radius, None, day13)
        return [res1]

    def nabo_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        iv = self.repeat_month_with_alternate_starts(nisan_1, 4, self.nabo_12_iv)
        vi = self.repeat_month_with_alternate_starts(nisan_1, 6, self.nabo_12_vi)
        return [iv, vi]


    def nabo_13_iii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day1 = SearchRange.for_night(month, 1)
        # Mars was [....] above α Leonis.
        res1 = AngularSeparationQuery(self.db, MARS, REGULUS, 0, 20, EclipticPosition.ABOVE, day1)
        return [res1]

    def nabo_13_v(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        day3 = SearchRange.for_night(month, 3)
        # Mars ... it was with β Virginis
        res1 = AngularSeparationQuery(self.db, MARS, BETA_VIRGINIS, 0, 10, None, day3)
        return [res1]

    def nabo_year_13(self, nisan_1: float) -> List[PotentialMonthResult]:
        iii = self.repeat_month_with_alternate_starts(nisan_1, 3, self.nabo_13_iii)
        v = self.repeat_month_with_alternate_starts(nisan_1, 5, self.nabo_13_v)
        return [iii, v]

    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):

        if subquery is not None:

            if subquery == "shamash":
                tests = [YearToTest(0, "Shamash-shum-ukin 14", Intercalary.ADDARU, self.shamash_year_14),
                         YearToTest(3, "Shamash-shum-ukin 17", Intercalary.UNKNOWN, self.shamash_year_17),
                         YearToTest(5, "Shamash-shum-ukin 19", Intercalary.UNKNOWN, self.shamash_year_19)]
                res = self.run_years(tests)
                self.print_results(res, "Shamash-shum-ukin year 14")

            elif subquery == "kandalanu":
                tests = [YearToTest(0, "Kandalanu 1", Intercalary.UNKNOWN, self.kand_year_1),
                         YearToTest(11, "Kandalanu 12", Intercalary.UNKNOWN, self.kand_year_12),
                         YearToTest(15, "Kandalanu 16", Intercalary.UNKNOWN, self.kand_year_16)]
                res = self.run_years(tests)
                self.print_results(res, "Kandalanu year 1")

            elif subquery == "nabopolassar":
                tests = [YearToTest(0, "Nabopolassar 7", Intercalary.ADDARU, self.nabo_year_7),
                         YearToTest(5, "Nabopolassar 12", Intercalary.ADDARU, self.nabo_year_12),
                         YearToTest(6, "Nabopolassar 13", Intercalary.FALSE, self.nabo_year_13)]
                res = self.run_years(tests)
                self.print_results(res, "Nabopolassar year 7")

            else:
                raise RuntimeError("Please specify a valid subquery for this tablet")

        else:
            tests = [YearToTest(0, "Shamash-shum-ukin 14", Intercalary.ADDARU, self.shamash_year_14),
                     YearToTest(3, "Shamash-shum-ukin 17", Intercalary.UNKNOWN, self.shamash_year_17),
                     YearToTest(5, "Shamash-shum-ukin 19", Intercalary.UNKNOWN, self.shamash_year_19),
                     YearToTest(7, "Kandalanu 1", Intercalary.UNKNOWN, self.kand_year_1),
                     YearToTest(18, "Kandalanu 12", Intercalary.UNKNOWN, self.kand_year_12),
                     YearToTest(22, "Kandalanu 16", Intercalary.UNKNOWN, self.kand_year_16),
                     YearToTest(35, "Nabopolassar 7", Intercalary.ADDARU, self.nabo_year_7),
                     YearToTest(40, "Nabopolassar 12", Intercalary.ADDARU, self.nabo_year_12),
                     YearToTest(41, "Nabopolassar 13", Intercalary.FALSE, self.nabo_year_13)]
            res = self.run_years(tests)
            self.print_results(res, "Shamash-shum-ukin year 14 to Nabopolassar (assuming reigns of 20, and 22)")

        self.output_json_for_year(res, print_year, slim_results)
