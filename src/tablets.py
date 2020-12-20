from data import AstroData
from typing import *

from database import Database


def match(tablet: str) -> Callable[[AstroData, Database, Union[int, None], Union[int, None]], None]:
    if tablet == "bm32312":
        return bm32312
    raise ValueError("Unknown tablet name")


def bm32312(data: AstroData, db: Database, start, end):
    print("Computing ephemeris for BM32312...")
    pass
