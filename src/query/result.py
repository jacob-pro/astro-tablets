from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

from constants import Planet
from data import AstroData
from query.database import Database


@dataclass
class TargetTime:
    nisan_1: float
    month_offset: int
    start: float
    end: float
    date: str


class AbstractResult(ABC):

    @abstractmethod
    def result_quality(self) -> bool:
        pass

    @abstractmethod
    def print(self, data: AstroData) -> dict:
        pass


class PlanetaryEventResult(AbstractResult):

    def __init__(self, db: Database, planet: Planet, event: str, target_time: TargetTime):
        self.target_time = target_time
        self.nearest = db.nearest_event_match_to_time(planet.name, event, target_time.start)
        self.planet = planet

    def result_quality(self) -> bool:
        if self.nearest > self.target_time.end:
            return (self.nearest - self.target_time.end) <= self.planet.tolerance_days
        elif self.nearest < self.target_time.start:
            return (self.target_time.start - self.nearest) <= self.planet.tolerance_days
        else:
            return True

    def print(self, data: AstroData) -> dict:
        pass


class AngularSeparationResult(AbstractResult):

    def __init__(self, db: Database, from_body: str, to_body: str, min: Union[float, None], max: float,
                 target_time: TargetTime):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.min = min
        self.max = max
        sep = db.separations_in_range(from_body, to_body, target_time.start, target_time.end)

    def result_quality(self) -> bool:
        pass

    def print(self, data: AstroData) -> dict:
        pass
