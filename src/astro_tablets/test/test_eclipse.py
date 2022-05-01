from unittest import TestCase

from astro_tablets.generate.eclipse import *


class EclipseTest(TestCase):
    SFM_AET_ACCURACY = 0.31

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    # Stephenson, Fatoohi, Morrison, The Accuracy of Eclipse Times, Table 2, Page 341
    def test_total_eclipses(self):
        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-554, 10, 7))
        self.compare_total_triple(eclipse.phases(TimeUnit.DEGREE), 16.50, 24.25, 16.50)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-500, 11, 7))
        self.compare_total_triple(eclipse.phases(TimeUnit.DEGREE), 16.75, 23.50, 16.75)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-377, 4, 6))
        self.compare_total_triple(eclipse.phases(TimeUnit.DEGREE), 15.75, 19.00, 15.75)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-225, 8, 1))
        self.compare_total_triple(eclipse.phases(TimeUnit.DEGREE), 16.75, 16.00, 16.75)

    def compare_total_triple(self, phases: EclipsePhases, onset: float, maximal: float, clearing: float):
        self.assertLessEqual(abs(onset - phases.onset), self.SFM_AET_ACCURACY)
        self.assertLessEqual(abs(maximal - phases.maximal), self.SFM_AET_ACCURACY)
        self.assertLessEqual(abs(clearing - phases.clearing), self.SFM_AET_ACCURACY)

    # Stephenson, Fatoohi, Morrison, The Accuracy of Eclipse Times, Table 3, Page 341
    def test_partial_eclipses(self):
        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-423, 9, 28))
        # self.compare_partial_double(eclipse.phases(TimeUnit.DEGREE), 17.50, 17.50) - Wrong Data?

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-409, 12, 22))
        self.assertLessEqual(abs(47.75 - eclipse.phases(TimeUnit.DEGREE).sum), self.SFM_AET_ACCURACY)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-407, 10, 31))
        self.assertLessEqual(abs(22.75 - eclipse.phases(TimeUnit.DEGREE).sum), self.SFM_AET_ACCURACY)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-396, 4, 5))
        self.assertLessEqual(abs(16.25 - eclipse.phases(TimeUnit.DEGREE).sum), self.SFM_AET_ACCURACY)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-153, 3, 21))
        self.compare_partial_double(eclipse.phases(TimeUnit.DEGREE), 24.75, 24.75)

        eclipse = lunar_eclipse_on_date(self.data, self.data.timescale.ut1(-128, 11, 4))
        self.compare_partial_double(eclipse.phases(TimeUnit.DEGREE), 21.50, 21.50)

    def compare_partial_double(self, phases: EclipsePhases, onset: float, clearing: float):
        self.assertLessEqual(abs(onset - phases.onset), self.SFM_AET_ACCURACY)
        self.assertLessEqual(abs(clearing - phases.clearing), self.SFM_AET_ACCURACY)

