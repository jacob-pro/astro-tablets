from data import AstroData
from query.database import Database


class QueryTablet:

    def __init__(self, data: AstroData, db: Database):
        self.data = data
        self.db = db

