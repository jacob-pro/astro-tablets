import math

from astro_tablets.constants import Confidence

ANGLE_ABS_ERROR_DEGREES = 0.1
TIME_ABS_ERROR_US = 1.5


def normal_pdf(x: float, mean: float, sd: float):
    sqrt_two_pi = math.sqrt(math.pi * 2)
    return math.exp(-((x - mean) ** 2) / 2 / sd**2) / (sqrt_two_pi * sd)


class Scorer:
    @staticmethod
    def time_error_factor_us(confidence: Confidence) -> float:
        if confidence == Confidence.REGULAR:
            return 0.2
        elif confidence == Confidence.LOW:
            return 0.6
        else:
            raise ValueError

    @staticmethod
    def angular_separation_factor(confidence: Confidence) -> float:
        if confidence == Confidence.REGULAR:
            return 0.4
        elif confidence == Confidence.LOW:
            return 1.2
        else:
            raise ValueError

    @staticmethod
    def score(
        actual: float, expected: float, proportional_err: float, absolute_err: float
    ):
        """
        A function for scoring results
        @param actual: The actual computed value for a time being tested.
        @param expected: The expected value from the tablet.
        @param proportional_err: How much error to allow proportional to the size of the expected value.
        @param absolute_err: How much error to allow regardless of the size of the expected value.
        @return: A score value (between 0 and 1)
        """
        sd = (expected * proportional_err) + absolute_err
        score = normal_pdf(actual, expected, sd)
        height = normal_pdf(expected, expected, sd)
        return score * (1 / height)

    @staticmethod
    def score_time(actual: float, expected: float, confidence: Confidence):
        """
        A function for scoring timings
        @param actual: The actual computed value for a time being tested.
        @param expected: The expected value from the tablet.
        @param confidence: How confident we are in reading the time value.
        @return: A score value (between 0 and 1)
        """
        return Scorer.score(
            actual, expected, Scorer.time_error_factor_us(confidence), TIME_ABS_ERROR_US
        )

    @staticmethod
    def score_separation(actual: float, expected: float, confidence: Confidence):
        """
        A function for scoring angular separations
        @param actual: The actual computed value for a time being tested.
        @param expected: The expected value from the tablet.
        @param confidence: How confident we are in reading the angle value.
        @return: A score value (between 0 and 1)
        """
        return Scorer.score(
            actual,
            expected,
            Scorer.angular_separation_factor(confidence),
            ANGLE_ABS_ERROR_DEGREES,
        )
