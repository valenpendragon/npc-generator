from collections import namedtuple

# value is an integer or float in the main currency for the game.  For D&D, that
# would be integer gold pieces. For TFT, that would silver dollars.
Gem = namedtuple('Gem', ['type', 'value'])
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
    that often show up in treasures. These items have more attributes
    than magic items. There are gems and valuables. Arguments must be in
    the form of tuples. The length determines if the tuple represents a
    gem or valuable. Gem requires (type, value). Valuable requires (item,
    example, value). value is always an integer or a float.
    """
    def __init__(self, *args):
        self.item_list = []
        for item in args:
            match len(item):
                case 2:
                    new_item = Gem(type=item[0], value=item[1])
                case 3:
                    new_item = Valuable(item=item[0], example=item[1], value=item[2])
                case _:
                    error_msg = (f"OtherWealth: Treasure items must have "
                                 f"either length 2 (gem) or length 3 (valuable), "
                                 f"not {len(item)}.")
                    raise ValueError(error_msg)
            self.item_list.append(new_item)

    def __str__(self):
        s = "Other Valuables:\n"
        for item in self.item_list:
            if isinstance(item, Gem):
                s += f"Gem: {item.type}, value: {item.value}\n"
            else:
                s += f"Valuable: {item.item}, example: {item.example}, value: {item.value}\n"
        return s


class Treasure:
    pass
