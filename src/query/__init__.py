from query.bm41222 import BM41222


def get_tablet_class(tablet: str):
    if tablet == "bm41222":
        return BM41222
    raise ValueError("Unknown tablet name")

