from collections import namedtuple
from enum import unique, Enum

from skyfield.framelib import ecliptic_frame
from skyfield.timelib import Time

from data import AstroData
from util import change_in_longitude


@unique
class EclipticPosition(Enum):
    BEHIND = "behind"
    AHEAD = "ahead"
    BELOW = "below"
    ABOVE = "above"


def _ecliptic_position(deg_above: float, deg_ahead: float) -> EclipticPosition:
    if deg_above > 0 and deg_above > abs(deg_ahead):
        return EclipticPosition.ABOVE
    elif deg_above < 0 and abs(deg_above) > abs(deg_ahead):
        return EclipticPosition.BELOW
    elif deg_ahead < 0:
        return EclipticPosition.BEHIND
    else:
        return EclipticPosition.AHEAD


AngularSeparationResult = namedtuple('AngularSeparationResult', 'angle position')


def angular_separation(data: AstroData, body1, body2, t0: Time) -> AngularSeparationResult:
    """
    Computes angle between the two bodies
    And also the position of body1 relative to body2 along the ecliptic
    """
    p1 = data.get_babylon().at(t0).observe(body1).apparent()
    p2 = data.get_babylon().at(t0).observe(body2).apparent()
    sep = p1.separation_from(p2)

    # eclat between -180 and 180
    # eclon between 0 and 360
    p1_eclat, p1_eclon, _ = p1.frame_latlon(ecliptic_frame)
    p2_eclat, p2_eclon, _ = p2.frame_latlon(ecliptic_frame)
    deg_above = p1_eclat.degrees - p2_eclat.degrees
    deg_ahead = change_in_longitude(p1_eclon.degrees, p2_eclon.degrees)

    return AngularSeparationResult(sep, _ecliptic_position(deg_above, deg_ahead))
