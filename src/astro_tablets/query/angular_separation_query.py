import math
from typing import Optional

from astro_tablets.constants import Body, Precision
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, ScoredResult, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.util import TimeValue


def angular_separation_tolerance(precision: Precision) -> float:
    if precision == Precision.REGULAR:
        return 5.0
    elif precision == Precision.LOW:
        return 1.5
    else:
        raise ValueError


class AngularSeparationQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        target_angle: float,
        target_position: Optional[EclipticPosition],
        target_time: SearchRange,
        angle_precision: Precision = Precision.REGULAR,
    ):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.target_angle = target_angle
        self.target_position = target_position
        self.precision = angle_precision
        sep = db.separations_in_range(
            from_body, to_body, target_time.start, target_time.end
        )
        if len(sep) < 1:
            raise RuntimeError(
                "Failed to find any separations between {} and {} at {} to {}, check database".format(
                    from_body.name, to_body.name, target_time.start, target_time.end
                )
            )
        results = ScoredResult.score_results(
            sep,
            lambda x: self.calculate_score(
                target_angle, target_position, x.angle, x.position, angle_precision
            ),
        )
        self.best = results[0].result
        self.score = results[0].score

    @staticmethod
    def calculate_score(
        tablet_angle: float,
        tablet_position: Optional[EclipticPosition],
        actual: float,
        actual_position: str,
        precision: Precision,
    ) -> float:
        """
        Correct position (if specified) adds 0.2 to score
        """
        t = angular_separation_tolerance(precision)
        diff = abs(actual - tablet_angle)
        angle_score = math.pow(t, -diff)
        assert 0 <= angle_score <= 1

        if tablet_position is not None:
            position_score = 1 if actual_position == tablet_position.value else 0
            return (angle_score * 0.8) + (position_score * 0.2)
        else:
            return angle_score

    def quality_score(self) -> float:
        return self.score

    def output(self) -> dict:
        return {
            "from_body": self.from_body.name,
            "to_body": self.to_body.name,
            "angle": self.best.angle,
            "position": self.best.position,
            "at_time": TimeValue(self.best.time),
        }

    def get_search_range(self) -> SearchRange:
        return self.target_time
