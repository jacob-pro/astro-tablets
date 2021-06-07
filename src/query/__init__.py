from query.bm32234 import BM32234
from query.bm32312 import BM32312
from query.bm33066 import BM33066
from query.bm35115 import BM35115
from query.bm38462 import BM38462
from query.bm41222 import BM41222
from query.bm76738 import BM76738
from query.vat4956 import VAT4956


def get_tablet_class(tablet: str):
    if tablet == "bm32312":
        return BM32312
    if tablet == "bm41222":
        return BM41222
    if tablet == "bm76738":
        return BM76738
    if tablet == "bm35115":
        return BM35115
    if tablet == "bm32234":
        return BM32234
    if tablet == "bm38462":
        return BM38462
    if tablet == "vat4956":
        return VAT4956
    if tablet == "bm33066":
        return BM33066
    raise ValueError("Unknown tablet name")
