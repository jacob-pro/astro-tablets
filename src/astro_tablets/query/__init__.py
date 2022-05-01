from typing import Optional

from astro_tablets.data import AstroData
from astro_tablets.query.abstract_tablet import AbstractTablet
from astro_tablets.query.bm32234 import BM32234
from astro_tablets.query.bm32312 import BM32312
from astro_tablets.query.bm33066 import BM33066
from astro_tablets.query.bm35115 import BM35115
from astro_tablets.query.bm38462 import BM38462
from astro_tablets.query.bm41222 import BM41222
from astro_tablets.query.bm76738 import BM76738
from astro_tablets.query.database import Database
from astro_tablets.query.vat4956 import VAT4956


def get_tablet(
    tablet: str, data: AstroData, db: Database, subquery: Optional[str]
) -> AbstractTablet:
    if tablet == "bm32312":
        return BM32312(data, db)
    if tablet == "bm41222":
        return BM41222(data, db, subquery)
    if tablet == "bm76738":
        return BM76738(data, db)
    if tablet == "bm35115":
        return BM35115(data, db)
    if tablet == "bm32234":
        return BM32234(data, db)
    if tablet == "bm38462":
        return BM38462(data, db)
    if tablet == "vat4956":
        return VAT4956(data, db, subquery)
    if tablet == "bm33066":
        return BM33066(data, db, subquery)
    raise ValueError("Unknown tablet name")
