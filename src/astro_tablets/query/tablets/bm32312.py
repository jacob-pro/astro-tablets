from typing import List

from astro_tablets.constants import (
    ANTARES,
    ARIES,
    FINGER,
    MARS,
    MERCURY,
    PISCES,
    SATURN,
    VENUS,
    Confidence,
    Radius,
)
from astro_tablets.data import AstroData
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.generate.planet_events import (
    InnerPlanetPhenomena,
    OuterPlanetPhenomena,
)
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.abstract_tablet import (
    AbstractTablet,
    Intercalary,
    MonthResult,
    YearToTest,
)
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.database import BabylonianDay, Database
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery
from astro_tablets.query.radius_query import WithinRadiusQuery


class BM32312(AbstractTablet):
    def month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        day14 = SearchRange.for_night(month, 14)
        # Mercury's last appearance in the east behind Pisces
        res.append(
            PlanetaryEventQuery(self.db, MERCURY, InnerPlanetPhenomena.ML, day14)
        )
        res.append(
            WithinRadiusQuery(
                self.db, MERCURY, PISCES.central_star, PISCES.radius, None, day14
            )
        )
        # Saturn's last appearance behind Pisces
        res.append(PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, day14))
        res.append(
            WithinRadiusQuery(
                self.db,
                SATURN,
                PISCES.central_star,
                PISCES.radius,
                EclipticPosition.BEHIND,
                day14,
            )
        )

        day17 = SearchRange.for_night(month, 17)
        # Mars became stationary
        res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.ST, day17))
        # it came close to the bright star of the Scorpion's head
        res.append(
            WithinRadiusQuery(
                self.db, MARS, ANTARES, Radius.SMALL.value, None, day17, Confidence.LOW
            )
        )

        return res

    def month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        day5 = SearchRange.for_night(month, 5)
        # Mercury's first appearance in the east in Pisces
        res.append(PlanetaryEventQuery(self.db, MERCURY, InnerPlanetPhenomena.MF, day5))
        res.append(
            WithinRadiusQuery(
                self.db, MERCURY, PISCES.central_star, PISCES.radius, None, day5
            )
        )

        day19 = SearchRange.for_night(month, 19)
        # Venus stood in the region of Aries, 10 fingers behind Mars
        res.append(
            AngularSeparationQuery(
                self.db,
                VENUS,
                MARS,
                10 * FINGER,
                EclipticPosition.BEHIND,
                day19,
            )
        )
        res.append(
            WithinRadiusQuery(
                self.db, MARS, ARIES.central_star, ARIES.radius, None, day19
            )
        )

        day20 = SearchRange.for_night(month, 20)
        # Mars was 1 finger to the left of the front? of Aries
        res.append(
            WithinRadiusQuery(
                self.db, MARS, ARIES.central_star, ARIES.radius, None, day20
            )
        )

        return res

    def shamash_year_16(self, nisan_1: float) -> List[MonthResult]:
        # Unknown intercalary status
        month_a = self.try_multiple_months(
            nisan_1, 1, 13, self.month_a, comment="Month A (Probably I)"
        )
        month_b = self.try_multiple_months(
            nisan_1, 1, 13, self.month_b, comment="Month B"
        )
        return [month_a, month_b]

    def __init__(self, data: AstroData, db: Database):
        tests = [
            YearToTest(
                0, "Shamash-shum-ukin 16", Intercalary.UNKNOWN, self.shamash_year_16
            )
        ]
        super().__init__(data, db, tests, "Shamash-shum-ukin year 16")
