from data import *
from query.abstract_query import AbstractQuery
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary
from query.database import BabylonianDay
from query.lunar_six_query import LunarSixQuery, LunarSix


class VAT4956(AbstractTablet):

    def year_37_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, False, 4.0))

        return res

    def year_37(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_1 = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_37_month_1)
        return [month_1]


    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        tests = [YearToTest(0, "Nebuchadnezzar 37", Intercalary.FALSE, self.year_37)]
        res = self.run_years(tests)
        self.print_results(res, "Nebuchadnezzar 37")
        self.output_json_for_year(res, print_year, slim_results)
