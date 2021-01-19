from data import AstroData


class QueryTablet:

    def __init__(self, data: AstroData, db):
        self.data = data
        self.db = db
