import math
from typing import Optional

from astro_tablets.constants import Body
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, ScoredResult, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.util import TimeValue

LAMBDA = 8


class WithinRadiusQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        radius: float,
        target_position: Optional[EclipticPosition],
        target_time: SearchRange,
    ):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.radius = radius
        self.target_position = target_position
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
                radius, target_position, x.angle, x.position
            ),
        )

        # Tiebreaker for matching top scores
        tie_breaker = list(filter(lambda x: x.score == results[0].score, results))
        # Sort by closest angle
        tie_breaker.sort(key=lambda x: x.result.angle)

        self.best = tie_breaker[0].result
        self.score = tie_breaker[0].score

    @staticmethod
    def calculate_score(
        radius: float,
        tablet_position: Optional[EclipticPosition],
        actual_angle: float,
        actual_position: str,
    ) -> float:
        """
        Correct position (if specified) adds 0.2 to score
        """
        if actual_angle <= radius:
            return 1.0
        diff = abs(actual_angle - radius) / radius
        angle_score = math.pow(LAMBDA, -diff)
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
