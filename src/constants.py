LUNAR_VISIBILITY = 7.5

BABYLON_COORDS = ('32.468 N', '44.550 E')

FINGER = 0.092
CUBIT = 2.2
HALO = 22.0


def convert_angle(value) -> float:
    if type(value) == int:
        return float(value)
    if type(value) == float:
        return value
    if type(value) == str:
        split = value.lower().split()
        if len(split) == 4 and split[1] == "cubits" and split[3] == "fingers":
            return int(split[0]) * CUBIT + int(split[2]) * FINGER
        if len(split) == 4 and split[1] == "fingers" and split[3] == "cubits":
            return int(split[0]) * FINGER + int(split[2]) * CUBIT
        if len(split) == 2 and split[1] == "cubits":
            return int(split[0]) * CUBIT
        if len(split) == 2 and split[1] == "fingers":
            return int(split[0]) * FINGER
        if value.lower() == "halo":
            return HALO
    raise ValueError


class InnerPlanetArcusVisionis(object):

    def __init__(self, mf, ml, ef, el):
        self.mf = mf
        self.ml = ml
        self.ef = ef
        self.el = el

    @staticmethod
    def mercury():
        return InnerPlanetArcusVisionis(13.0, 9.5, 10.5, 11.0)

    @staticmethod
    def venus():
        return InnerPlanetArcusVisionis(5.7, 6.0, 6.0, 5.2)


class OuterPlanetArcusVisionis(object):

    def __init__(self, hr, hs, ar, cs):
        self.hr = hr
        self.hs = hs
        self.ar = ar
        self.cs = cs

    @staticmethod
    def mars():
        return OuterPlanetArcusVisionis(14.5, 13.2, 6.0, 6.0)

    @staticmethod
    def jupiter():
        return OuterPlanetArcusVisionis(9.3, 7.4, 6.0, 6.0)

    @staticmethod
    def saturn():
        return OuterPlanetArcusVisionis(13.0, 10.0, 8.0, 8.0)
