from typing import Union

from astro_tablets.constants import Planet
from astro_tablets.generate.planet_events import (
    InnerPlanetPhenomena,
    OuterPlanetPhenomena,
)
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.query.scorer import Scorer
from astro_tablets.util import TimeValue


class PlanetaryEventQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        planet: Planet,
        event: Union[InnerPlanetPhenomena, OuterPlanetPhenomena],
        target_time: SearchRange,
    ):
        self.target_time = target_time
        self.event = event
        nearest = db.nearest_event_match_to_time(planet, event.value, target_time.start)
        self.planet = planet
        if nearest is None:
            raise RuntimeError(
                "Failed to find any event {} for {} - check database".format(
                    event, planet.name
                )
            )
        assert nearest is not None
        self.nearest = nearest
        self.score = self.calculate_score(
            nearest, target_time.start, target_time.end, planet.event_frequency
        )

    @staticmethod
    def calculate_score(
        time: float, expected_start: float, expected_end: float, event_frequency: float
    ) -> float:
        """
        Calculates score based on the difference in time between when a synodic event actually occurred, and the
        date (or date range) it was observed in the text.
        The more frequent that synodic occur for this planet, the greater accuracy we should expect from
        the observations.
        @param time: The actual time of the event
        @param expected_start: The beginning of the expected time interval
        @param expected_end: The end of the expected time interval
        @param event_frequency: How many synodic events occur in a year on average for this planet
        @return: A score value (between 0 and 1)
        """
        if time > expected_end:
            diff = time - expected_end
        elif time < expected_start:
            diff = expected_start - time
        else:
            return 1.0
        variance = 40 / event_frequency
        score = Scorer.score(diff, 0, 0, variance)
        return score

    def quality_score(self) -> float:
        return self.score

    def output(self) -> dict:
        return {
            "planet": self.planet.name,
            "event": self.event.value,
            "nearest_time": TimeValue(self.nearest),
        }

    def get_search_range(self) -> SearchRange:
        return self.target_time
