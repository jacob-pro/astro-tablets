from astro_tablets.data import *
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.generate.planet_events import InnerPlanetPhenomena, OuterPlanetPhenomena
from astro_tablets.query.abstract_query import SearchRange, AbstractQuery
from astro_tablets.query.abstract_tablet import AbstractTablet, YearToTest, Intercalary, MonthResult
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.database import BabylonianDay
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery


class BM32312(AbstractTablet):

    def month_a(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []
        day14 = SearchRange.for_night(month, 14)
        # Mercury's last appearance in the east behind Pisces
        res.append(PlanetaryEventQuery(self.db, MERCURY, InnerPlanetPhenomena.ML, day14))
        res.append(AngularSeparationQuery(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day14))
        # Saturn's last appearance behind Pisces
        res.append(PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, day14))
        res.append(AngularSeparationQuery(self.db, SATURN, PISCES.central_star, 0, PISCES.radius, EclipticPosition.BEHIND, day14))

        day17 = SearchRange.for_night(month, 17)
        # Mars became stationary
        res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.ST, day17))
        # it came close to the bright star of the Scorpion's head
        res.append(AngularSeparationQuery(self.db, MARS, ANTARES, 0, 10, None, day17))

        return res

    def month_b(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []
        day5 = SearchRange.for_night(month, 5)
        # Mercury's first appearance in the east in Pisces
        res.append(PlanetaryEventQuery(self.db, MERCURY, InnerPlanetPhenomena.MF, day5))
        res.append(AngularSeparationQuery(self.db, MERCURY, PISCES.central_star, 0, PISCES.radius, None, day5))

        day19 = SearchRange.for_night(month, 19)
        # Venus stood in the region of Aries, 10 fingers behind Mars
        res.append(AngularSeparationQuery(self.db, VENUS, MARS, 10 * FINGER, 10 * FINGER, EclipticPosition.BEHIND, day19))
        res.append(AngularSeparationQuery(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day19))

        day20 = SearchRange.for_night(month, 20)
        # Mars was 1 finger to the left of the front? of Aries
        res.append(AngularSeparationQuery(self.db, MARS, ARIES.central_star, 0, ARIES.radius, None, day20))

        return res

    def shamash_year_16(self, nisan_1: float) -> List[MonthResult]:
        # Unknown intercalary status
        month_a = self.try_multiple_months(nisan_1, 1, 13, self.month_a, comment="Month A (Probably I)")
        month_b = self.try_multiple_months(nisan_1, 1, 13, self.month_b, comment="Month B")
        return [month_a, month_b]

    def do_query(self, _subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Shamash-shum-ukin 16", Intercalary.UNKNOWN, self.shamash_year_16)]
        results = self.run_years(tests)
        self.print_results(results, "Shamash-shum-ukin year 16")
        self.output_json_for_year(results, print_year, slim_results)
