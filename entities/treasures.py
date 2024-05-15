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
        if len(self.item_list) == 0:
            return "Treasure List is empty"
        else:
            s = f"Treasure List:\n"
            for item in self.item_list:
                if (isinstance(item, MagicItem) or
                        isinstance(item, OtherWealth)):
                    s += f"{item}\n"
                else:
                    s += f"Cash: {item.number} {item.type}\n"
            return s.replace('\n\n', '\n')

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
    desc_item_1 = "+1 Weapon"
    desc_item_2 = "healing potion"
    desc_item_3 = "robe of the archmage"

    gem1 = Gem("opal",
               'Transparent, iridescent, many colors including white, black, blue,'
               ' red, and green', 250)
    gem2 = Gem("diamond",
               "Transparent and clear (the most prized diamonds have no visible "
               "inclusions or flaws)", 5000)
    gem3 = Gem("jade", "Translucent green", 100)
    print("Gems created.")
    valuable1 = Valuable("necklace", "Ruby pendant or string of pearls", 2500)
    valuable2 = Valuable("statuary", "Marble bust or small silver idol", 250)
    valuable3 = Valuable('earrings',
                         "Dangling platinum earrings or white and black pearl pendants",
                         750)
    print('Valuables created.')
    coin1 = Coin(350, 'cp')
    coin2 = Coin(400, 'sp')
    coin3 = Coin(150, 'gp')
    coin4 = Coin(70, 'pp')
    print("Cash as coins created.")

    magic_item_1 = MagicItem(desc_item_1)
    magic_item_2 = MagicItem(desc_item_2)
    magic_item_3 = MagicItem(desc_item_3)
    print(f"Magic items: {magic_item_1}, {magic_item_2}, {magic_item_3}")

    other_wealth_1 = OtherWealth()
    other_wealth_1.add_item(gem1)
    other_wealth_1.add_item(valuable1)
    other_wealth_2 = OtherWealth()
    other_wealth_2.add_item(gem2)
    other_wealth_2.add_item(valuable2)
    other_wealth_3 = OtherWealth()
    other_wealth_3.add_item(gem3)
    other_wealth_3.add_item(valuable3)
    print("Other wealth created from gems and valuables.")
    try:
        other_wealth_3.add_item(magic_item_1)
    except TypeError:
        print(f"Error test: OtherWealth can only add items of type"
              f" Gem or Valuable.\n")

    for item in (other_wealth_1, other_wealth_2, other_wealth_3):
        print(item)

    treasure_1 = Treasure(magic_item_1, other_wealth_1, coin1)
    treasure_2 = Treasure(magic_item_2, other_wealth_2, coin2)
    treasure_3 = Treasure(magic_item_3, other_wealth_3, coin3,
                          coin4)
    print("Error test: Treasures created from cash (coin), magic items,"
          " and other wealth.")

    try:
        treasure_4 = Treasure(magic_item_1, gem1, valuable2)
    except TypeError:
        print(f"Treasure can only add items of type Coin, OtherWealth, "
              f"or MagicItem.\n")

    for item in (treasure_1, treasure_2, treasure_3):
        print(item)
