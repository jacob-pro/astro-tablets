from typing import List

from astro_tablets.constants import (
    ANTARES,
    BETA_VIRGINIS,
    HEAD_OF_THE_LION,
    LEO,
    LIBRA,
    REGULUS,
    SAGITTARIUS,
    SATURN,
    VIRGO,
    Precision,
    Radius,
)
from astro_tablets.data import AstroData
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.generate.planet_events import OuterPlanetPhenomena
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.abstract_tablet import (
    AbstractTablet,
    Intercalary,
    MonthResult,
    YearToTest,
)
from astro_tablets.query.database import BabylonianDay, Database
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery
from astro_tablets.query.radius_query import WithinRadiusQuery


class BM76738(AbstractTablet):
    def year_1_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        return [
            # [Year 1 of Kand]alanu, ⌜month⌝ [..., day ..., last appearance.]
            PlanetaryEventQuery(
                self.db, SATURN, OuterPlanetPhenomena.LA, SearchRange.any_day(month)
            )
        ]

    def year_1_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 1, mont]h 4, day 24, in fr[ont of ... the Crab, first appearance.]
        range = SearchRange.for_night(month, 24)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_1(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 4, self.year_1_month_unknown)
        month_4 = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_1_month_4
        )
        return [month_a, month_4]

    def year_2_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Ye]ar 2, month 4, day 10+[x, ..., last appearance.]
        range = SearchRange.x_plus(month, 10)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_2_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 2, mon]th 5, broken, in the head of the Lion, first appearance; not [observed?.]
        any_day = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, any_day)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            HEAD_OF_THE_LION.central_star,
            HEAD_OF_THE_LION.radius,
            None,
            any_day,
        )
        return [res1, res2]

    def year_2(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_2_month_4
        )
        month_5 = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_2_month_5
        )
        return [month_4, month_5]

    def year_3_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Ye]ar 3, month 4, day 7, [last appearance.]
        range = SearchRange.for_night(month, 7)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_3_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 3], month 5, day 16, in the Lion behind the King (= α Leonis)
        range = SearchRange.for_night(month, 16)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            REGULUS,
            Radius.SMALL.value,
            EclipticPosition.BEHIND,
            range,
            Precision.LOW,
        )
        return [res1, res2]

    def year_3(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_3_month_4
        )
        month_5 = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_3_month_5
        )
        return [month_4, month_5]

    def year_4_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year] ⌜4⌝, at the end of month 4, last appearance
        range = SearchRange.for_night(month, 29)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_4_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 4, month 6?], day [x], in the middle of the Lion, first appearance
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, LEO.central_star, LEO.radius, None, range
        )
        return [res1, res2]

    def year_4(self, nisan_1: float) -> List[MonthResult]:
        month_4 = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_4_month_4
        )
        month_b = self.try_multiple_months(nisan_1, 5, 12, self.year_4_month_unknown)
        return [month_4, month_b]

    def year_5_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 5], month 5, day 23, last appearance.
        range = SearchRange.for_night(month, 23)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_5_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 5], at the end of month 6, first appearance;
        range = SearchRange.for_night(month, 29)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_5(self, nisan_1: float) -> List[MonthResult]:
        month_5 = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_5_month_5
        )
        month_6 = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_5_month_6
        )
        return [month_5, month_6]

    def year_6_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # Year 6, month 5, day 20, last appearance.
        range = SearchRange.for_night(month, 20)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_6_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 6], month 6, day 22, behind ⌜the rear foot of⌝ the Lion (= β Virginis), behind AN.GÚ.ME.MAR, first appearance.
        range = SearchRange.for_night(month, 22)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            BETA_VIRGINIS,
            Radius.MEDIUM.value,
            EclipticPosition.BEHIND,
            range,
            Precision.LOW,
        )
        return [res1, res2]

    def year_6(self, nisan_1: float) -> List[MonthResult]:
        month_5 = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_6_month_5
        )
        month_6 = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_6_month_6
        )
        return [month_5, month_6]

    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # Year 7, month 6, day 10+[x], last appearance.
        range = SearchRange.x_plus(month, 10)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 7], month 7, day 15, ⌜in front of⌝ the Furrow (α+ Virginis), first appearance.
        range = SearchRange.for_night(month, 15)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, VIRGO.central_star, VIRGO.radius, None, range
        )
        return [res1, res2]

    def year_7(self, nisan_1: float) -> List[MonthResult]:
        month_6 = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_7_month_6
        )
        month_7 = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_7_month_7
        )
        return [month_6, month_7]

    def year_8_month_vi2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, VIRGO.central_star, VIRGO.radius, None, range
        )
        return [res1, res2]

    def year_8_month_vii(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # Year 8, month 6 (Ululu II), day 5, behind the Furrow (α+ Virginis), last appearance.
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, VIRGO.central_star, VIRGO.radius, None, range
        )
        return [res1, res2]

    def year_8(self, nisan_1: float) -> List[MonthResult]:
        # Intercalary Ululu so offset by one
        month_6 = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_8_month_vi2
        )
        month_7 = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_8_month_vii
        )
        return [month_6, month_7]

    def year_9_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year] ⌜9, month 6⌝, [day] ⌜27/28?⌝, last appearance.
        range = SearchRange.any_day(month)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_9_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 9, month 8, day x]+1, ⌜within?⌝ the Balance,... [..., first appearance]
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, LIBRA.central_star, LIBRA.radius, None, range
        )
        return [res1, res2]

    def year_9(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_9_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 12, self.year_9_month_b)
        return [month_a, month_b]

    def year_10_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # Year 10, month] ⌜7⌝, day 20, behind the Balance, [last appearance].
        range = SearchRange.for_night(month, 20)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)
        res2 = WithinRadiusQuery(
            self.db, SATURN, LIBRA.central_star, LIBRA.radius, None, range
        )
        return [res1, res2]

    def year_10_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 10, month 8, day] 23, in front of the Forehead of the Scorpion, on the north side, first appearance;
        range = SearchRange.for_night(month, 23)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            ANTARES,
            Radius.MEDIUM.value,
            EclipticPosition.AHEAD,
            range,
            Precision.LOW,
        )
        return [res1, res2]

    def year_10(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_10_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 13, self.year_10_month_b)
        return [month_a, month_b]

    def year_11_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 11, month] 7, day 13, last appearance.
        range = SearchRange.for_night(month, 13)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_11_month_unknown(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 11, month 8, day] ⌜15⌝, above Lisi (= α Scorpii) ⌜6½ degrees⌝, first appearance;
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            ANTARES,
            Radius.SMALL.value,
            EclipticPosition.ABOVE,
            range,
            Precision.LOW,
        )
        return [res1, res2]

    def year_11(self, nisan_1: float) -> List[MonthResult]:
        month_7 = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_11_month_7
        )
        month_b = self.try_multiple_months(nisan_1, 7, 12, self.year_11_month_unknown)
        return [month_7, month_b]

    def year_12_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 12, month] 8, day 5, last appearance; ⌜because of⌝ cloud computed.
        range = SearchRange.for_night(month, 5)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_12_month_9(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 12, month] 9, day 5, at the beginning of Pabilsag (= Sagittarius + part of Ophiuchus), [first appearance?];
        range = SearchRange.for_night(month, 5)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            SAGITTARIUS.central_star,
            SAGITTARIUS.radius,
            None,
            range,
        )
        return [res1, res2]

    def year_12(self, nisan_1: float) -> List[MonthResult]:
        month_8 = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_12_month_8
        )
        month_9 = self.repeat_month_with_alternate_starts(
            nisan_1, 9, self.year_12_month_9
        )
        return [month_8, month_9]

    def year_13_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year] 13, month 8, day 26, last appearance;
        range = SearchRange.for_night(month, 26)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_13_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 13, month] 10, day 1, in the middle of Pabilsag, [first appearance;...]
        range = SearchRange.for_night(month, 1)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        res2 = WithinRadiusQuery(
            self.db,
            SATURN,
            SAGITTARIUS.central_star,
            SAGITTARIUS.radius,
            None,
            range,
        )
        return [res1, res2]

    def year_13(self, nisan_1: float) -> List[MonthResult]:
        month_8 = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_13_month_8
        )
        month_10 = self.repeat_month_with_alternate_starts(
            nisan_1, 10, self.year_13_month_10
        )
        return [month_8, month_10]

    def year_14_month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year] ⌜14⌝, month ⌜8⌝, ⌜day 20⌝, [last appearance;...]
        range = SearchRange.any_day(month)
        return [PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, range)]

    def year_14_month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        # [Year 14, month 9, day] ⌜20⌝[+?,...] ... [..., first appearance;...]
        range = SearchRange.any_day(month)
        res1 = PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, range)
        return [res1]

    def year_14(self, nisan_1: float) -> List[MonthResult]:
        month_a = self.try_multiple_months(nisan_1, 1, 12, self.year_14_month_a)
        month_b = self.try_multiple_months(nisan_1, 1, 12, self.year_14_month_b)
        return [month_a, month_b]

    def __init__(self, data: AstroData, db: Database):
        tests = [
            YearToTest(0, "Kandalanu 1", Intercalary.UNKNOWN, self.year_1),
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
        super().__init__(data, db, tests, "Kandalanu year 1")
