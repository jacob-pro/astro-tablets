from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena, OuterPlanetPhenomena
from query.database import BabylonianDay
from query.result import AbstractResult, AngularSeparationResult, SearchRange, PlanetaryEventResult
from query.tablet import AbstractTablet, PotentialMonthResult, MultiyearResult, YearToTest


class BM32312(AbstractTablet):

    def month_a(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        res = []
        day14 = SearchRange.for_night(month, 14)
        # Mercury's last appearance in the east behind Pisces
        res.append(PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.ML, day14))
        res.append(AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day14))
        # Saturn's last appearance behind Pisces
        res.append(PlanetaryEventResult(self.db, SATURN, OuterPlanetPhenomena.LA, day14))
        res.append(AngularSeparationResult(self.db, SATURN, PISCES.central_star, 0, PISCES.radius, EclipticPosition.BEHIND, day14))

        day17 = SearchRange.for_night(month, 17)
        # Mars became stationary
        res.append(PlanetaryEventResult(self.db, MARS, OuterPlanetPhenomena.ST, day17))
        # it came close to the bright star of the Scorpion's head
        res.append(AngularSeparationResult(self.db, MARS, ANTARES, 0, 10, None, day17))

        return res

    def month_b(self, month: List[BabylonianDay]) -> List[AbstractResult]:
        res = []
        day5 = SearchRange.for_night(month, 5)
        # Mercury's first appearance in the east in Pisces
        res.append(PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.MF, day5))
        res.append(AngularSeparationResult(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day5))

        day19 = SearchRange.for_night(month, 19)
        # Venus stood in the region of Aries, 10 fingers behind Mars
        res.append(AngularSeparationResult(self.db, VENUS, MARS, 10 * FINGER, 10 * FINGER, EclipticPosition.BEHIND, day19))
        res.append(AngularSeparationResult(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day19))

        day20 = SearchRange.for_night(month, 20)
        # Mars was 1 finger to the left of the front? of Aries
        res.append(AngularSeparationResult(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day20))

        return res

    def shamash_year_16(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_a_attempts = []
        month_b_attempts = []
        for month_number in range(1, 13):
            month_a_attempts.append(self.repeat_month_with_alternate_starts(nisan_1, month_number, "Month A (Probably I)", self.month_a))
            month_b_attempts.append(self.repeat_month_with_alternate_starts(nisan_1, month_number, "Month B", self.month_b))
        month_a_attempts.sort(key=lambda x: x.score, reverse=True)
        month_b_attempts.sort(key=lambda x: x.score, reverse=True)
        return [month_a_attempts[0], month_b_attempts[0]]

    def do_query(self, _subquery: Union[str, None], print_year: Union[int, None]):
        tests = [YearToTest(0, "Shamash-shum-ukin 16", self.shamash_year_16)]
        results = self.run_years(tests)
        self.print_results(results, "Shamash-shum-ukin year 16")
        self.output_json_for_year(results, print_year)
