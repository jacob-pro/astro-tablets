from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena
from query.result import PlanetaryEventResult, TargetTime, AngularSeparationResult, AbstractResult
from query.tablet import AbstractTablet, MultiplexedMonthResult


class BM41222(AbstractTablet):

    def shamash_14_xii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day4 = TargetTime(nisan_1, days_late, month[3].sunset, month[3].sunrise, "XII 4")
        # Mercury's first appearance in the west
        res1 = PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.EF, day4)
        # in the area of the Swallow.
        res2 = AngularSeparationResult(self.db, MERCURY, FIFTY_EIGHT_PISCIUM, 0, 50, None, day4)
        return [res1, res2]

    def shamash_year_14(self, nisan_1: float) -> List[MultiplexedMonthResult]:
        months = self.db.get_months(nisan_1)
        month_xii = self.db.get_days(months[11])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_xii, self.shamash_14_xii)
        return [res1]


    def shamash_17_ii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day19 = TargetTime(nisan_1, days_late, month[18].sunset, month[18].sunrise, "II 19")
        # mars was in [the area?] of the Old Man
        res1 = AngularSeparationResult(self.db, MARS, THIRTY_SIX_PERSEI, 0, 45, None, day19)
        # to the right of Mercury
        res2 = AngularSeparationResult(self.db, MARS, MERCURY, 0, 40, EclipticPosition.AHEAD, day19)
        return [res1, res2]

    def shamash_year_17(self, nisan_1: float) -> List[MultiplexedMonthResult]:
        months = self.db.get_months(nisan_1)
        month_ii = self.db.get_days(months[1])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_ii, self.shamash_17_ii)
        return [res1]


    def shamash_19_vii(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        day4 = TargetTime(nisan_1, days_late, month[3].sunset, month[3].sunrise, "VII 4")
        # Mercury stood for ⅔ cubit above? Mars
        res1 = AngularSeparationResult(self.db, MERCURY, MARS, (2/3 * CUBIT), 1 * CUBIT, EclipticPosition.ABOVE, day4)
        return [res1]

    def shamash_year_19(self, nisan_1: float) -> List[MultiplexedMonthResult]:
        months = self.db.get_months(nisan_1)
        month_vii = self.db.get_days(months[6])
        res1 = self.repeat_month_with_alternate_starts(nisan_1, month_vii, self.shamash_19_vii)
        return [res1]


    def query(self):
        years = self.db.get_years()
        items = list(years.items())
        matches = []
        for i in range(0, len(years) - 5):
            y14 = self.repeat_year_with_alternate_starts(items[i][1], self.shamash_year_14)
            y17 = self.repeat_year_with_alternate_starts(items[i + 3][1], self.shamash_year_17)
            y19 = self.repeat_year_with_alternate_starts(items[i + 5][1], self.shamash_year_19)
            total_score = sum(item[0].score for item in [y14, y17, y19])
            matches.append((items[i][1][0]['year'], total_score, [y14, y17, y19]))
        matches.sort(key=lambda x: x[1], reverse=True)
        for i in matches:
            print(i[0], i[1])
        pass


