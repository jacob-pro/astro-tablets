from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import OuterPlanetPhenomena
from query.abstract_query import AbstractQuery, SearchRange
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary
from query.angular_separation_query import AngularSeparationQuery
from query.database import BabylonianDay
from query.lunar_six_query import LunarSixQuery, LunarSix
from query.planetary_event_query import PlanetaryEventQuery


class VAT4956(AbstractTablet):

    def year_37_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []
        # Sîn (Moon) appeared behind the Bull of Heaven (Taurus)
        res.append(AngularSeparationQuery(self.db, MOON, TAURUS.central_star, 0, TAURUS.radius,
                                          EclipticPosition.BEHIND, SearchRange.for_night(month, 1)))
        # Kajjamānu (Saturn) was in front of the Swallow (Pisces).
        res.append(AngularSeparationQuery(self.db, SATURN, PISCES.central_star, 0, PISCES.radius,
                                          EclipticPosition.AHEAD, SearchRange.for_night(month, 1)))
        # the 9th, beginning of the night, Sîn (Moon) stood 1 cubit in front of the Rear Foot of the Lion (β Virginis).
        res.append(AngularSeparationQuery(self.db, MOON, BETA_VIRGINIS, 1 * CUBIT, 1 * CUBIT,
                                          EclipticPosition.AHEAD, SearchRange.for_night(month, 9)))
        #  The 11th] or the 12th Sagmegar (Jupiter) ‘rose to daylight’ (AR).
        res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.AR,
                                       SearchRange.range_of_nights(month, 11, 12)))
        #  NA (sunrise to moonset) was 4.
        res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, False, 4.0))
        return res

    def year_37_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        return res

    def year_37(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_1 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_37_month_1)
        month_2 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_37_month_2)
        return [month_1, month_2]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Nebuchadnezzar 37", Intercalary.FALSE, self.year_37)]
        res = self.run_years(tests)
        self.print_results(res, "Nebuchadnezzar 37")
        self.output_json_for_year(res, print_year, slim_results)
