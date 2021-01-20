from abc import ABC, abstractmethod


class AbstractResult(ABC):

    @abstractmethod
    def is_good_result(self) -> bool:
        pass

    @abstractmethod
    def get_fields(self) -> dict:
        pass


class PlanetaryEventResult(AbstractResult):

    def is_good_result(self) -> bool:
        pass

    def get_fields(self) -> dict:
        pass
