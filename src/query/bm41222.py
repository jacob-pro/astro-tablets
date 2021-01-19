from query.common import *
from data import AstroData
from query.tablet import QueryTablet


class BM41222(QueryTablet):

    def year_14_results(self, conn, year_14):
        for potential_year in year_14[1]:
            month_xii = get_months(conn, potential_year["nisan_1"])[11]
            day4 = get_day(conn, month_xii, 4)
            pass

        pass

    def test(self, conn: sqlite3.Connection, data: AstroData):
        years = get_years(conn)
        items = list(years.items())
        for i in range(0, len(years) - 5):
            y14 = self.year_14_results(conn, items[i])
            # evaluate(conn, items[i], items[i+3], items[i+5])

