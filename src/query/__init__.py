from query.bm32312 import BM32312
from query.bm41222 import BM41222
from query.bm76738 import BM76738


def get_tablet_class(tablet: str):
    if tablet == "bm32312":
        return BM32312
    if tablet == "bm41222":
        return BM41222
    if tablet == "bm76738":
        return BM76738
    raise ValueError("Unknown tablet name")
