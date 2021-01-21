from data import MERCURY
from generate.planet_events import InnerPlanetPhenomena
from query.result import PlanetaryEventResult, TargetTime
from query.tablet import QueryTablet
from typing import *


class BM41222(QueryTablet):

    def shamash_14(self, potential_years: List):
        for y in potential_years:
            months = self.db.get_months(y['nisan_1'])
            month_xii_days = self.db.get_days(months[11])
            for start_offset in range(-1, 1):
                day_4 = month_xii_days[4 + start_offset]
                time = TargetTime(y['nisan_1'], month_xii_days[1 + start_offset].sunset, day_4.sunset, day_4.sunrise, "XII 4")
                res = PlanetaryEventResult(self.db, MERCURY, InnerPlanetPhenomena.EF.value, time)
                if res.is_good_result():
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


