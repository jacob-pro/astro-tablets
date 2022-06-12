from typing import Optional

import numpy as np

from astro_tablets.constants import Body, Confidence
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, ScoredResult, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.query.scorer import Scorer
from astro_tablets.util import TimeValue


class WithinRadiusQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        radius: float,
        target_position: Optional[EclipticPosition],
        target_time: SearchRange,
        confidence: Confidence = Confidence.REGULAR,
    ):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.radius = radius
        self.target_position = target_position
        sep = db.separations_in_range(
            from_body.name, to_body.name, target_time.start, target_time.end
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
                radius, target_position, x.angle, x.position, confidence
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
        confidence: Confidence,
    ) -> float:
        """
        Calculates score based on the actual angle between two bodies, and the angle it is expected to be less than.
        The expected position (if specified) and actual position are also compared, giving an additional 0.2 to the
        score if they match.
        @param radius: The maximum expected separation angle.
        @param tablet_position: The expected position of the two bodies relative to the ecliptic.
        @param actual_angle: The actual angular separation.
        @param actual_position: The actual position of the two bodies relative to the ecliptic.
        @param confidence: How confident that the radius value is correct / precise
        @return: A score value (between 0 and 1)
        """
        # If the angle is within the radius, then it is an exact match
        if actual_angle <= radius:
            angle_score = 1.0
        else:
            # Otherwise, score based on how far outside the radius
            angle_score = Scorer.score_separation(actual_angle, radius, confidence)

        assert 0 <= angle_score <= 1

        # Compare the actual vs expected positions
        if tablet_position is not None:
            position_score = 1 if actual_position == tablet_position.value else 0
            return float(np.average([angle_score, position_score], weights=[0.8, 0.2]))
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
