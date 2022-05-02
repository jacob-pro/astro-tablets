from astro_tablets.constants import HALO, MOON, Body
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.database import Database
from astro_tablets.util import TimeValue

# A higher value is more tolerant of error
LAMBDA = 0.5


class HaloQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        from_body: Body,
        to_body: Body,
        target_time: SearchRange,
        halo_size: float = HALO,
    ):
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.halo_size = halo_size
        sep = db.separations_in_range(
            from_body, to_body, target_time.start, target_time.end
        )
        if len(sep) < 1:
            raise RuntimeError(
                "Failed to find any separations between {} and {} at {} to {}, check database".format(
                    MOON.name, to_body.name, target_time.start, target_time.end
                )
            )
        sep.sort(key=lambda x: x.angle)
        self.best = sep[0]

    def get_search_range(self) -> SearchRange:
        return self.target_time

    @staticmethod
    def score(
        halo_size: float,
        actual_angle: float,
    ) -> float:
        if actual_angle <= halo_size:
            return 1.0
        diff = actual_angle - halo_size
        score = -pow(diff / (halo_size * LAMBDA), 2) + 1.0
        if score < 0:
            return 0
        return score

    def quality_score(self) -> float:
        return self.score(
            self.halo_size,
            self.best.angle,
        )

    def output(self) -> dict:
        return {
            "from_body": self.from_body.name,
            "to_body": self.to_body.name,
            "angle": self.best.angle,
            "at_time": TimeValue(self.best.time),
        }
