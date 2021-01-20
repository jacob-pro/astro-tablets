from query.tablet import QueryTablet


class BM41222(QueryTablet):

    def query(self):
        years = self.db.get_years()
        months = self.db.get_months(years.get(-726)[0]['nisan_1'])
        days = self.db.get_days(months[0])
        pass


