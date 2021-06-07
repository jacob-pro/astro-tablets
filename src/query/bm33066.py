from enum import unique, Enum

from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import OuterPlanetPhenomena, InnerPlanetPhenomena
from query.abstract_query import AbstractQuery, SearchRange
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary
from query.angular_separation_query import AngularSeparationQuery
from query.database import BabylonianDay
from query.lunar_eclipse_query import LunarEclipseQuery, ExpectedEclipseType
from query.lunar_six_query import LunarSixQuery, LunarSix
from query.planetary_event_query import PlanetaryEventQuery


@unique
class BM33066Mode(Enum):
    ALL = "All"
    ECLIPSE_ONLY = "Eclipses Only"
    LUNAR_SIX_ONLY = "Lunar Six Only"
    PLANET_ONLY = "Planetary Only"


class VAT4956(AbstractTablet):

    def year_7_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 30))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 9))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 2.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 8 + 1/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 7 + 2/3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 16))

        return res

    def year_7_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 23))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 8 + 2/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 1))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 1 + 2/3))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 14.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21))

        return res

    def year_7_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 18.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 9.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        return res

    def year_7_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 27))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 4))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        return res

    def year_7_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 10, low_precision=True))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 3.5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 2.5, low_precision=True))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 11))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 7.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 22.5))

        return res

    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15 + 2/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 1 + 1/3))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 8 + 2/3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        return res

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 16 + 2/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 6.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 7.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 12))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 3))
            res.append(LunarSixQuery(self.db, month, 26, LunarSix.KUR, 22))

        return res

    def year_7(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_i = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_7_month_1)
        month_ii = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_7_month_2)
        month_iii = self.repeat_month_with_alternate_starts(nisan_1, 3, self.year_7_month_3)
        month_iv = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_7_month_4)
        month_v = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_7_month_5)
        month_vi = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_7_month_6)
        month_vii = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_7_month_7)

        return [month_i, month_ii, month_iii, month_iv, month_v, month_vi, month_vii]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        if subquery == "eclipse_only":
            self.mode = BM33066Mode.ECLIPSE_ONLY
        elif subquery == "lunar_six_only":
            self.mode = BM33066Mode.LUNAR_SIX_ONLY
        elif subquery == "planet_only":
            self.mode = BM33066Mode.PLANET_ONLY
        else:
            self.mode = BM33066Mode.ALL
        tests = [YearToTest(0, "Cambyses 7", Intercalary.ADDARU, self.year_7)]
        res = self.run_years(tests)
        self.print_results(res, "Cambyses 7 ({})".format(self.mode.value))
        self.output_json_for_year(res, print_year, slim_results)
