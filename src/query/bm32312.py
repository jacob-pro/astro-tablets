from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena, OuterPlanetPhenomena
from query.result import AbstractResult, AngularSeparationResult, TargetTime, PlanetaryEventResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult
from typing import *
from constants import *
from data import *


class BM32312(AbstractTablet):

    def month_a(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        res = []
        day14 = TargetTime(nisan_1, days_late, month[13].sunset, month[13].sunrise, "14th")
        # Mercury's last appearance in the east behind Pisces
        res.append(PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.ML, day14))
        res.append(AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day14))
        # Saturn's last appearance behind Pisces
        res.append(PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.LA, day14))
        res.append(AngularSeparationResult(self.db, SATURN, PISCES.central_star, 0, PISCES.radius, EclipticPosition.BEHIND, day14))

        day17 = TargetTime(nisan_1, days_late, month[16].sunset, month[16].sunrise, "17th")
        # Mars became stationary
        res.append(PlanetaryEventResult(self.db, MARS, OuterPlanetPhenomena.ST, day17))
        # it came close to the bright star of the Scorpion's head
        res.append(AngularSeparationResult(self.db, MARS, ANTARES, 0, 10, None, day17))

        return res

    def month_b(self, month: List, days_late: int, nisan_1: float) -> List[AbstractResult]:
        res = []
        day5 = TargetTime(nisan_1, days_late, month[4].sunset, month[4].sunrise, "5th")
        # Mercury's first appearance in the east in Pisces
        res.append(PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.MF, day5))
        res.append(AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day5))

        day19 = TargetTime(nisan_1, days_late, month[18].sunset, month[18].sunrise, "19th")
        # Venus stood in the region of Aries, 10 fingers behind Mars
        res.append(AngularSeparationResult(self.db, VENUS, MARS, 10 * FINGER, 10 * FINGER, EclipticPosition.BEHIND, day19))
        res.append(AngularSeparationResult(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day19))

        day20 = TargetTime(nisan_1, days_late, month[19].sunset, month[19].sunrise, "20th")
        # Mars was 1 finger to the left of the front? of Aries
        res.append(AngularSeparationResult(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day20))

        return res

    def shamash_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        months = self.db.get_months(nisan_1)
        month_a_attempts = []
        month_b_attempts = []
        for m in months:
            month_a_attempts.append(self.repeat_month_with_alternate_starts(nisan_1, self.db.get_days(m), self.month_a))
            month_b_attempts.append(self.repeat_month_with_alternate_starts(nisan_1, self.db.get_days(m), self.month_b))
        month_a_attempts.sort(key=lambda x: x.score, reverse=True)
        month_b_attempts.sort(key=lambda x: x.score, reverse=True)
        return [month_a_attempts[0], month_b_attempts[0]]

    def do_query(self, _subquery: Union[str, None], print_year: Union[int, None]):
        years = self.db.get_years()
        year_items = list(map(lambda x: x[1], years.items()))
        results = []
        for y in year_items:
            y16 = self.repeat_year_with_alternate_starts(y, self.shamash_year_16)
            results.append(MultiyearResult(y[0]['year'], y16[0].score, [y16]))
        self.print_top_results(results, "Shamash-shum-ukin year 16")
        self.output_results_for_year(results, print_year)
