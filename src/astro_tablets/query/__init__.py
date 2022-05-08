from typing import Optional

from astro_tablets.data import AstroData
from astro_tablets.query.abstract_tablet import AbstractTablet
from astro_tablets.query.database import Database
from astro_tablets.query.tablets.bm32234 import BM32234
from astro_tablets.query.tablets.bm32312 import BM32312
from astro_tablets.query.tablets.bm33066 import BM33066
from astro_tablets.query.tablets.bm35115 import BM35115
from astro_tablets.query.tablets.bm38462 import BM38462
from astro_tablets.query.tablets.bm41222 import BM41222
from astro_tablets.query.tablets.bm76738 import BM76738
from astro_tablets.query.tablets.vat4956 import VAT4956


def get_query_tablet(
    tablet: str, data: AstroData, db: Database, subquery: Optional[str]
) -> AbstractTablet:
    if tablet == "BM32312":
        return BM32312(data, db)
    if tablet == "BM41222":
        return BM41222(data, db, subquery)
    if tablet == "BM76738":
        return BM76738(data, db)
    if tablet == "BM35115":
        return BM35115(data, db)
    if tablet == "BM32234":
        return BM32234(data, db)
    if tablet == "BM38462":
        return BM38462(data, db)
    if tablet == "VAT4956":
        return VAT4956(data, db, subquery)
    if tablet == "BM33066":
        return BM33066(data, db, subquery)
    raise ValueError("Unknown tablet name")
