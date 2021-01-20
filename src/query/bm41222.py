from data import MERCURY
from generate.planet_events import InnerPlanetPhenomena
from query.tablet import QueryTablet
from typing import *


class BM41222(QueryTablet):

    def shamash_14(self, potential_years: List):
        for y in potential_years:
            months = self.db.get_months(y['nisan_1'])
            month_xii_days = self.db.get_days(months[11])
            for start_offset in range(-1, 1):
                day_4 = month_xii_days[4 + start_offset]
                nearest = self.db.nearest_event_match_to_time(MERCURY, InnerPlanetPhenomena.EF.value, day_4.sunset)
                if abs(nearest - day_4.sunset) < 5:
                    print(y['year'])

    def query(self):
        years = self.db.get_years()
        items = list(years.items())
        for i in range(0, len(years) - 5):
            self.shamash_14(items[i][1])
            pass

        months = self.db.get_months(years.get(-726)[0]['nisan_1'])
        days = self.db.get_days(months[0])
        pass


