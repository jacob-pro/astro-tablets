from typing import Optional

import numpy as np

from astro_tablets.constants import MOON, Body, Confidence
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, ScoredResult, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.query.scorer import Scorer
from astro_tablets.util import TimeValue


class AngularSeparationQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        target_angle: float,
        target_position: Optional[EclipticPosition],
        target_time: SearchRange,
        angle_confidence: Confidence = Confidence.REGULAR,
    ):
        # The moon moves relatively quick, so our ephemeris which
        # are computed every few hours aren't super accurate
        if from_body == MOON or to_body == MOON:
            angle_confidence = Confidence.LOW

        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
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
                target_angle, target_position, x.angle, x.position, angle_confidence
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
        confidence: Confidence,
    ) -> float:
        """
        Calculates score based on the actual angle between two bodies, and the angle that is described on the tablet.
        The expected position (if specified) and actual position are also compared, giving an additional 0.2 to the
        score if they match.
        @param tablet_angle: The expected angular separation of the two bodies.
        @param tablet_position: The expected position of the two bodies relative to the ecliptic.
        @param actual: The actual angular separation.
        @param actual_position: The actual position of the two bodies relative to the ecliptic.
        @param confidence: How confident we are in reading the angle value
        @return: A score value (between 0 and 1)
        """
        angle_score = Scorer.score_separation(actual, tablet_angle, confidence)
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
