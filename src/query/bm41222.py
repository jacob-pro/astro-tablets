from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena
from query.database import BabylonianDay
from query.result import PlanetaryEventResult, SearchRange, AngularSeparationResult, AbstractResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult


class BM41222(AbstractTablet):

    ## Shamash-shum-ukin

    def shamash_14_xii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day4 = SearchRange(month[3].sunset, month[3].sunrise, "4th")
        # Mercury's first appearance in the west
        res1 = PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.EF, day4)
        # in the area of the Swallow.
        res2 = AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day4)
        return [res1, res2]

    def shamash_year_14(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 12, "Year 14 XII", self.shamash_14_xii)
        return [res1]


    def shamash_17_ii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day19 = SearchRange(month[18].sunset, month[18].sunrise, "19th")
        # mars was in [the area?] of the Old Man
        res1 = AngularSeparationResult(self.db, MARS, PERSEUS.central_star, 0, PERSEUS.radius, None, day19)
        # to the right of Mercury
        res2 = AngularSeparationResult(self.db, MARS, MERCURY, 0, 30, EclipticPosition.AHEAD, day19)
        return [res1, res2]

    def shamash_year_17(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 2, "Year 17 II", self.shamash_17_ii)
        return [res1]


    def shamash_19_vii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day4 = SearchRange(month[3].sunset, month[3].sunrise, "4th")
        # Mercury stood for ⅔ cubit above? Mars
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (2/3 * CUBIT), 1 * CUBIT, EclipticPosition.ABOVE, day4)
        return [res1]

    def shamash_year_19(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 7, "Year 19 VII", self.shamash_19_vii)
        return [res1]

    def shamash(self, years: List) -> List[MultiyearResult]:
        results = []
        for i in range(0, len(years) - 5):
            y14 = self.repeat_year_with_alternate_starts(years[i], "Shamash-shum-ukin 14", self.shamash_year_14)
            y17 = self.repeat_year_with_alternate_starts(years[i + 3], "Shamash-shum-ukin 17", self.shamash_year_17)
            y19 = self.repeat_year_with_alternate_starts(years[i + 5], "Shamash-shum-ukin 19", self.shamash_year_19)
            total_score = sum(item[0].score for item in [y14, y17, y19])
            results.append(MultiyearResult(years[i][0]['year'], total_score, [y14, y17, y19]))
        return results

    ## Kandalanu

    def kand_1_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day28 = SearchRange(month[27].sunset, month[27].sunrise, "28th")
        # Mercury was in the back of Mars?
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, 0, 30, EclipticPosition.BEHIND, day28)
        return [res1]

    def kand_year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 1 III", self.kand_1_iii)
        return [res1]


    def kand_12_i(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day8 = SearchRange(month[7].sunset, month[7].sunrise, "8th")
        # Mercury, in the area of Pleiades
        res1 = AngularSeparationResult(self.db, MERCURY, ALCYONE, 0, 10, None, day8)
        # Mercury was 2 ⅔ cubits above? Mars?
        res2 = AngularSeparationResult(self.db, MERCURY, MARS, (2 + 2/3) * CUBIT, 2 * CUBIT, EclipticPosition.ABOVE, day8)
        return [res1, res2]

    def kand_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 1, "Year 12 I", self.kand_12_i)
        return [res1]


    def kand_16_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day20 = SearchRange(month[19].sunset, month[19].sunrise, "20th")
        # Mercury stood 1 cubit 4 fingers behind Mars.
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (1 * CUBIT + 4 * FINGER), 1 * CUBIT, EclipticPosition.BEHIND, day20)
        return [res1]

    def kand_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        res1 = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 16 III", self.kand_16_iii)
        return [res1]

    def kandalanu(self, years: List) -> List[MultiyearResult]:
        results = []
        for i in range(0, len(years) - 15):
            y1 = self.repeat_year_with_alternate_starts(years[i], "Kanalanu 1", self.kand_year_1)
            y12 = self.repeat_year_with_alternate_starts(years[i + 11], "Kanalanu 15", self.kand_year_12)
            y16 = self.repeat_year_with_alternate_starts(years[i + 15], "Kanalanu 16", self.kand_year_16)
            total_score = sum(item[0].score for item in [y1, y12, y16])
            results.append(MultiyearResult(years[i][0]['year'], total_score, [y1, y12, y16]))
        return results

    # Nabopolassar

    def nabo_7_unknown(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day = SearchRange(month[0].sunset, month[30].sunrise, "?")
        # Mercury was balanced 6 fingers above Mars.
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, 6 * FINGER, 6 * FINGER, EclipticPosition.ABOVE, day)
        return [res1]

    def nabo_year_7(self, nisan_1: float) -> List[PotentialMonthResult]:
        attempts = []
        for m in range(1, 13):
            attempts.append(self.repeat_month_with_alternate_starts(nisan_1, m, "Year 7 ?", self.nabo_7_unknown))
        attempts.sort(key=lambda x: x.score, reverse=True)
        return attempts[:1]


    def nabo_12_iv(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day = SearchRange(month[17].sunset, month[17].sunrise, "18th")
        # Mars was with Pleiades
        res1 = AngularSeparationResult(self.db, MARS, ALCYONE, 0, 10, None, day)
        return [res1]

    def nabo_12_vi(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day = SearchRange(month[12].sunset, month[12].sunrise, "13th")
        # Mars was ⅔ cubit above the Chariot
        res1 = AngularSeparationResult(self.db, MARS, AURIGA.central_star, 0, AURIGA.radius, None, day)
        return [res1]

    def nabo_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        iv = self.repeat_month_with_alternate_starts(nisan_1, 4, "Year 12 IV", self.nabo_12_iv)
        vi = self.repeat_month_with_alternate_starts(nisan_1, 6, "Year 12 VI", self.nabo_12_vi)
        return [iv, vi]


    def nabo_13_iii(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day = SearchRange(month[0].sunset, month[0].sunrise, "1st")
        # Mars was [....] above α Leonis.
        res1 = AngularSeparationResult(self.db, MARS, REGULUS, 0, 20, EclipticPosition.ABOVE, day)
        return [res1]

    def nabo_13_v(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        day = SearchRange(month[2].sunset, month[2].sunrise, "3rd")
        # Mars ... it was with β Virginis
        res1 = AngularSeparationResult(self.db, MARS, BETA_VIRGINIS, 0, 10, None, day)
        return [res1]

    def nabo_year_13(self, nisan_1: float) -> List[PotentialMonthResult]:
        iii = self.repeat_month_with_alternate_starts(nisan_1, 3, "Year 13 III", self.nabo_13_iii)
        v = self.repeat_month_with_alternate_starts(nisan_1, 5, "Year 13 V", self.nabo_13_v)
        return [iii, v]


    def nabopolassar(self, years: List) -> List[MultiyearResult]:
        results = []
        for i in range(0, len(years) - 6):
            y7 = self.repeat_year_with_alternate_starts(years[i], "Nabopolassar 7", self.nabo_year_7)
            y12 = self.repeat_year_with_alternate_starts(years[i + 5], "Nabopolassar 12", self.nabo_year_12)
            y13 = self.repeat_year_with_alternate_starts(years[i + 6], "Nabopolassar 13", self.nabo_year_13)
            total_score = sum(item[0].score for item in [y7, y12, y13])
            results.append(MultiyearResult(years[i][0]['year'], total_score, [y7, y12, y13]))
        return results


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None]):
        years = self.db.get_years()
        year_items = list(map(lambda x: x[1], years.items()))
        if subquery == "shamash":
            res = self.shamash(year_items)
            self.print_top_results(res, "Shamash-shum-ukin year 14")
        elif subquery == "kandalanu":
            res = self.kandalanu(year_items)
            self.print_top_results(res, "Kandalanu year 1")
        elif subquery == "nabopolassar":
            res = self.nabopolassar(year_items)
            self.print_top_results(res, "Nabopolassar year 7")
        else:
            raise RuntimeError("Please specify a valid subquery for this tablet")
        self.output_results_for_year(res, print_year)


