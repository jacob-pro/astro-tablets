from abc import ABC, abstractmethod
from dataclasses import dataclass

from constants import Planet
from data import AstroData
from query.database import Database


@dataclass
class TargetTime:
    nisan_1: float
    month_1: float
    start: float
    end: float
    date: str


class AbstractResult(ABC):

    @abstractmethod
    def is_good_result(self) -> bool:
        pass

    @abstractmethod
    def print(self, data: AstroData) -> dict:
        pass


class PlanetaryEventResult(AbstractResult):

    def __init__(self, db: Database, planet: Planet, event: str, target_time: TargetTime):
        self.target_time = target_time
        self.nearest = db.nearest_event_match_to_time(planet.name, event, target_time.start)
        self.planet = planet

    def is_good_result(self) -> bool:
        if self.nearest > self.target_time.end:
            return (self.nearest - self.target_time.end) <= self.planet.tolerance_days
        elif self.nearest < self.target_time.start:
            return (self.target_time.start - self.nearest) <= self.planet.tolerance_days
        else:
            return True

    def print(self, data: AstroData) -> dict:
        pass


class AngularSeparationResult(AbstractResult):

    def is_good_result(self) -> bool:
        pass

    def print(self, data: AstroData) -> dict:
        pass
