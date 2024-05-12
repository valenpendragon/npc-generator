from collections import namedtuple

# value is an integer or float in the main currency for the game.  For D&D, that
# would be integer gold pieces. For TFT, that would silver dollars.
Gem = namedtuple('Gem',
                 ['type', 'description', 'value'])
Valuable = namedtuple('Valuable',
                      ['item', 'example', 'value'])
Coin = namedtuple('Coin', ['number', 'type'])


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
    """
    This class handles objects of value other than coins and magic items
    that often show up in treasures. __init__ simply creates an empty
    OtherWealth object. Each gem or valuable needs to added to an
    OtherWealth object using the add_item method.
    """
    def __init__(self):
        self.item_list = []

    def __str__(self):
        s = "Other Valuables:\n"
        for item in self.item_list:
            if isinstance(item, Gem):
                s += (f"Gem: {item.type}, "
                      f"description: {item.description}, "
                      f"value: {item.value}.\n")
            else:
                s += (f"Valuable: {item.item}, example: {item.example}, "
                      f"value: {item.value}\n")
        return s

    def add_item(self, item):
        """
        This method adds an item to OtherWealth.item_list. The item must be either a
        Gem or Valuable object, otherwise a TypeError will be raised.
        :return: None
        """
        if isinstance(item, Gem) or isinstance(item, Valuable):
            self.item_list.append(item)
        else:
            error_msg = (f"OtherWealth.add_item: Only items of type Gem or Valuable "
                         f"may added to OtherWealth objects. items is type "
                         f"{type(item)}.")
            raise TypeError(error_msg)


class Treasure:
    """
    This class only takes a list of objects of classes MagicItem, Coin, or
    OtherWealth. Any other type of item included in the arguments will
    raise a TypeError.
    """
    def __init__(self, *args):
        self.item_list = []
        for item in args:
            self.add_item(item)

    def __str__(self):
        s = f"Treasure List:\n"
        for item in self.item_list:
            s += f"{item}\n"
        return s

    def add_item(self, item):
        """
        This method adds an item to Treasure.item_list. The item must
        be of type Coin, MagicItem, or OtherWealth. Any other object
        type will raise a TypeError.
        :param item: object of type Coin, MagicItme, or OtherWealth
        :return: None
        """
        if (isinstance(item, Coin) or
                isinstance(item, OtherWealth) or
                isinstance(item, MagicItem)):
            self.item_list.append(item)
        else:
            error_msg = (f"Treasure: Items supplied as arguments "
                         f"to this class must be of type Coin, "
                         f"MagicItem, or OtherWealth, not type, "
                         f"{type(item)}.")
            raise TypeError(error_msg)


if __name__ == "__main__":
    pass
