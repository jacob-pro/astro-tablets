import pathlib
from distutils.util import strtobool
from typing import Optional

from astro_tablets.data import AstroData
from astro_tablets.query.database import Database as QueryDatabase


def get_answer(question: str) -> bool:
    while True:
        print("{} [Y/N]".format(question))
        try:
            return strtobool(input()) == 1
        except ValueError:
            pass


def default_database_path(tablet: str) -> str:
    default_path = (
        pathlib.Path(__file__).parent.parent.parent.absolute()
        / f"./generated/{tablet.lower()}.db"
    )
    return default_path.as_posix()


def query_database_decorator(func):
    def wrapper(tablet: str, db: Optional[str], **kwargs):
        data = AstroData(time_only=True)
        db_path = default_database_path(tablet) if db is None else db
        db_obj = QueryDatabase(db_path)
        if db_obj.info.tablet.lower() != tablet.lower():
            raise RuntimeError("Database info doesn't match the requested tablet")
        func(data, tablet, db_obj, **kwargs)

    return wrapper
