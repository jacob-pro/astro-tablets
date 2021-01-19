from common import *
from data import AstroData


def year_14_results(conn, year_14):
    for potential_year in year_14[1]:
        month_xii = get_months(conn, potential_year["nisan_1"])[11]
        day4 = get_day(conn, month_xii, 4)
        pass

    pass


def bm41222(conn: sqlite3.Connection, data: AstroData):
    years = get_years(conn)
    items = list(years.items())
    for i in range(0, len(years) - 5):
        y14 = year_14_results(conn, items[i])
        # evaluate(conn, items[i], items[i+3], items[i+5])

