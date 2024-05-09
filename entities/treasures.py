class MagicItem:
    """
    This class handles magic items in RPGs. Since the tables only contain
    the name of the item, that is the only attribute available.
    """
    def __init__(self, name: str):
        self.item_name = name

    def __str__(self):
        s = f"Magic Item: {self.item_name}"
        return s


class OtherWealth:
    pass


class Coins:
    pass


class Treasure:
    pass
