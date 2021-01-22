import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

from constants import Planet
from data import AstroData
from generate.angular_separation import EclipticPosition
from generate.planet_events import InnerPlanetPhenomena, OuterPlanetPhenomena
from query.database import Database
from util import jd_float_to_local_time


@dataclass
class TargetTime:
    nisan_1: float
    month_offset: int
    start: float
    end: float
    date: str

    def output(self, data: AstroData) -> dict:
        return {
            'start_time': jd_float_to_local_time(self.start, data.timescale),
            'end_time': jd_float_to_local_time(self.end, data.timescale),
            'nisan_1': jd_float_to_local_time(self.nisan_1, data.timescale),
            'date': self.date,
            'month_started_late': self.month_offset
        }


class AbstractResult(ABC):

    @abstractmethod
    def quality_score(self) -> float:
        pass

    @abstractmethod
    def output(self, data: AstroData) -> dict:
        pass


class PlanetaryEventResult(AbstractResult):

    def __init__(self, db: Database, planet: Planet, event: Union[InnerPlanetPhenomena, OuterPlanetPhenomena],
                 target_time: TargetTime):
        self.target_time = target_time
        self.event = event
        self.nearest = db.nearest_event_match_to_time(planet.name, event.value, target_time.start)
        self.planet = planet

    @staticmethod
    def result_function(x: float, cut_off: float) -> float:
        """
        An exponential function means the closest will be asymptotically closer to 1,
        but score will decrease as x approaches the cut_off
        """
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

    def output(self, data: AstroData) -> dict:
        return {
            'planet': self.planet.name,
            'event': self.event.value,
            'nearest_time': jd_float_to_local_time(self.nearest, data.timescale),
            'calendar': self.target_time.output(data),
        }


class AngularSeparationResult(AbstractResult):

    def __init__(self, db: Database, from_body: Union[Planet, str], to_body: Union[Planet, str], target_angle: float,
                 tolerance: float, target_position: Union[EclipticPosition, None], target_time: TargetTime):
        if type(from_body) == Planet:
            from_body = from_body.name
        if type(to_body) == Planet:
            to_body = to_body.name
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.target_angle = target_angle
        self.target_position = target_position
        self.tolerance = tolerance
        sep = db.separations_in_range(from_body, to_body, target_time.start, target_time.end)
        sep.sort(key=lambda x: abs(x['angle'] - target_angle))
        if target_position is not None:
            filtered = list(filter(lambda x: x['angle'] <= tolerance and x['position'] == target_position.value, sep))
            if len(filtered) > 0:
                self.best = filtered[0]
            else:
                self.best = sep[0]
        else:
            self.best = sep[0]

    def result_function(self, x: float) -> float:
        res = 1 - math.pow((x / (self.tolerance / 2.0)), 2)
        return max(res, 0)

    def quality_score(self) -> float:
        """
        If angle is within tolerance of the target_angle score 1.0
        Decreasing score as the angle moves from target_angle+tolerance up to target_angle + (1.5 * tolerance)
        Correct position (if specified) adds 0.2 to score
        """
        lower_bound = max(self.target_angle - self.tolerance, 0)
        upper_bound = self.target_angle + self.tolerance
        actual = self.best['angle']
        if lower_bound <= actual <= upper_bound:
            angle_score = 1.0
        else:
            diff = min(abs(actual - lower_bound), abs(actual - upper_bound))
            angle_score = self.result_function(diff)
        if angle_score == 0:
            return 0
        if self.target_position is not None:
            if self.best['position'] == self.target_position.value:
                position_score = 1
            else:
                position_score = 0
            return (angle_score * 0.8) + (position_score * 0.2)
        else:
            return angle_score

    def output(self, data: AstroData) -> dict:
        return {
            'from_body': self.from_body,
            'to_body': self.to_body,
            'angle': self.best['angle'],
            'position': self.best['position'],
            'at_time': jd_float_to_local_time(self.best['time'], data.timescale),
            'calendar': self.target_time.output(data),
        }

