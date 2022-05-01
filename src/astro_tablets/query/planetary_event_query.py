import math
from typing import Union

from astro_tablets.constants import Planet
from astro_tablets.generate.planet_events import InnerPlanetPhenomena, OuterPlanetPhenomena
from astro_tablets.query.database import Database
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.util import TimeValue


class PlanetaryEventQuery(AbstractQuery):

    def __init__(self, db: Database, planet: Planet, event: Union[InnerPlanetPhenomena, OuterPlanetPhenomena],
                 target_time: SearchRange):
        self.target_time = target_time
        self.event = event
        nearest = db.nearest_event_match_to_time(planet, event.value, target_time.start)
        self.planet = planet
        if nearest is None:
            raise RuntimeError("Failed to find any event {} for {} - check database".format(event, planet.name))
        self.nearest = nearest

    def get_search_range(self) -> SearchRange:
        return self.target_time

    @staticmethod
    def result_function(x: float, cut_off: float) -> float:
        """
        An exponential function means the closest will be asymptotically closer to 1,
        but score will decrease as x approaches the cut_off
        """
        if x > cut_off:
            return 0
        return 1 - math.pow((1 + 10 * math.sqrt(cut_off)), x - cut_off)

    def quality_score(self) -> float:
        if self.nearest > self.target_time.end:
            diff = self.nearest - self.target_time.end
        elif self.nearest < self.target_time.start:
            diff = self.target_time.start - self.nearest
        else:
            return 1.0
        # The higher the cut_off the more lenient the result is
        cut_off = 48.0 / self.planet.event_frequency
        res = self.result_function(diff, cut_off)
        return max(res, 0)

    def output(self) -> dict:
        return {
            'planet': self.planet.name,
            'event': self.event.value,
            'nearest_time': TimeValue(self.nearest),
        }