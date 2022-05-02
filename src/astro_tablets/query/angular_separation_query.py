import math
from typing import Optional

from astro_tablets.constants import Body
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.database import Database, Separation
from astro_tablets.util import TimeValue


class AngularSeparationQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        target_angle: float,
        tolerance: float,
        target_position: Optional[EclipticPosition],
        target_time: SearchRange,
    ):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.target_angle = target_angle
        self.target_position = target_position
        self.tolerance = tolerance
        sep = db.separations_in_range(
            from_body, to_body, target_time.start, target_time.end
        )
        if len(sep) < 1:
            raise RuntimeError(
                "Failed to find any separations between {} and {} at {} to {}, check database".format(
                    from_body.name, to_body.name, target_time.start, target_time.end
                )
            )
        sep.sort(key=lambda x: abs(x.angle - target_angle))

        if target_position is not None:
            target_some = target_position

            def filter_fn(x: Separation):
                return x.angle <= tolerance and x.position == target_some.value

            filtered = list(
                filter(
                    filter_fn,
                    sep,
                )
            )
            if len(filtered) > 0:
                self.best = filtered[0]
            else:
                self.best = sep[0]
        else:
            self.best = sep[0]

    def get_search_range(self) -> SearchRange:
        return self.target_time

    @staticmethod
    def separation_score(
        target_angle: float,
        tolerance: float,
        target_position: Optional[EclipticPosition],
        actual: float,
        actual_position: str,
    ):
        """
        If angle is within tolerance of the target_angle score 1.0
        Decreasing score as the angle moves from target_angle+tolerance up to target_angle + (1.5 * tolerance)
        Correct position (if specified) adds 0.2 to score
        """
        lower_bound = max(target_angle - tolerance, 0)
        upper_bound = target_angle + tolerance
        if lower_bound <= actual <= upper_bound:
            angle_score = 1.0
        else:
            diff = min(abs(actual - lower_bound), abs(actual - upper_bound))
            res = 1 - math.pow((diff / (tolerance / 2.0)), 2)
            angle_score = max(res, 0)
        if angle_score == 0:
            return 0
        if target_position is not None:
            if actual_position == target_position.value:
                position_score = 1
            else:
                position_score = 0
            return (angle_score * 0.8) + (position_score * 0.2)
        else:
            return angle_score

    def quality_score(self) -> float:
        return self.separation_score(
            self.target_angle,
            self.tolerance,
            self.target_position,
            self.best.angle,
            self.best.position,
        )

    def output(self) -> dict:
        return {
            "from_body": self.from_body.name,
            "to_body": self.to_body.name,
            "angle": self.best.angle,
            "position": self.best.position,
            "at_time": TimeValue(self.best.time),
        }
