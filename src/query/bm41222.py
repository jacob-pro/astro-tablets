from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena
from query.result import PlanetaryEventResult, TargetTime, AngularSeparationResult, AbstractResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult


class BM41222(AbstractTablet):

    def shamash_14_xii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day4 = TargetTime(nisan_1, days_late, month[3].sunset, month[3].sunrise, "XII/4")
        # Mercury's first appearance in the west
        res1 = PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.EF, day4)
        # in the area of the Swallow.
        res2 = AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day4)
        return [res1, res2]

    def shamash_year_14(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_xii = self.db.get_days(months[11])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_xii, self.shamash_14_xii)
        return [res1]


    def shamash_17_ii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day19 = TargetTime(nisan_1, days_late, month[18].sunset, month[18].sunrise, "II/19")
        # mars was in [the area?] of the Old Man
        res1 = AngularSeparationResult(self.db, MARS, PERSEUS.central_star, 0, PERSEUS.radius, None, day19)
        # to the right of Mercury
        res2 = AngularSeparationResult(self.db, MARS, MERCURY, 0, 30, EclipticPosition.AHEAD, day19)
        return [res1, res2]

    def shamash_year_17(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_ii = self.db.get_days(months[1])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_ii, self.shamash_17_ii)
        return [res1]


    def shamash_19_vii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day4 = TargetTime(nisan_1, days_late, month[3].sunset, month[3].sunrise, "VII/4")
        # Mercury stood for ⅔ cubit above? Mars
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (2/3 * CUBIT), 1 * CUBIT, EclipticPosition.ABOVE, day4)
        return [res1]

    def shamash_year_19(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_vii = self.db.get_days(months[6])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_vii, self.shamash_19_vii)
        return [res1]

    def shamash(self):
        years = self.db.get_years()
        items = list(map(lambda x: x[1], years.items()))
        results = []
        for i in range(0, len(years) - 5):
            y14 = self.repeat_year_with_alternate_starts(items[i], self.shamash_year_14)
            y17 = self.repeat_year_with_alternate_starts(items[i + 3], self.shamash_year_17)
            y19 = self.repeat_year_with_alternate_starts(items[i + 5], self.shamash_year_19)
            total_score = sum(item[0].score for item in [y14, y17, y19])
            results.append(MultiyearResult(items[i][0]['year'], total_score, [y14, y17, y19]))
        self.print_top_results(results, "Shamash-shum-ukin year 14")


    def kand_1_iii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day28 = TargetTime(nisan_1, days_late, month[27].sunset, month[27].sunrise, "III/28")
        # Mercury was in the back of Mars?
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, 0, 30, EclipticPosition.BEHIND, day28)
        return [res1]

    def kand_year_1(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_iii = self.db.get_days(months[2])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_iii, self.kand_1_iii)
        return [res1]


    def kand_12_i(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day8 = TargetTime(nisan_1, days_late, month[7].sunset, month[7].sunrise, "I/8")
        # Mercury, in the area of Pleiades
        res1 = AngularSeparationResult(self.db, MERCURY, ALCYONE, 0, 10, None, day8)
        # Mercury was 2 ⅔ cubits above? Mars?
        res2 = AngularSeparationResult(self.db, MERCURY, MARS, (2 + 2/3) * CUBIT, 2 * CUBIT, EclipticPosition.ABOVE, day8)
        return [res1, res2]

    def kand_year_12(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_i = self.db.get_days(months[0])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_i, self.kand_12_i)
        return [res1]


    def kand_16_iii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day20 = TargetTime(nisan_1, days_late, month[19].sunset, month[19].sunrise, "III/20")
        # Mercury stood 1 cubit 4 fingers behind Mars.
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (1 * CUBIT + 4 * FINGER), 1 * CUBIT, EclipticPosition.BEHIND, day20)
        return [res1]

    def kand_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_iii = self.db.get_days(months[2])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_iii, self.kand_16_iii)
        return [res1]

    def kandalanu(self):
        years = self.db.get_years()
        items = list(map(lambda x: x[1], years.items()))
        results = []
        for i in range(0, len(years) - 15):
            y1 = self.repeat_year_with_alternate_starts(items[i], self.kand_year_1)
            y12 = self.repeat_year_with_alternate_starts(items[i + 11], self.kand_year_12)
            y16 = self.repeat_year_with_alternate_starts(items[i + 15], self.kand_year_16)
            total_score = sum(item[0].score for item in [y1, y12, y16])
            results.append(MultiyearResult(items[i][0]['year'], total_score,  [y1, y12, y16]))
        self.print_top_results(results, "Kandalanu year 1")


    def do_query(self, subquery: Union[str, None]):
        if subquery == "shamash":
            self.shamash()
        elif subquery == "kandalanu":
            self.kandalanu()
        else:
            raise RuntimeError("Please specify a valid subquery for this tablet")

