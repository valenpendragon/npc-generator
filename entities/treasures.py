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
    the name of the item, that is the only attribute available. The source
    attribute contains the name of actual worksheet it came from. The
    standard embeds the workbook name at least partly in each worksheet
    name, enabling the GM to find the right source for the full description.
    """
    def __init__(self, name: str, source: str):
        self.item_name = name
        self.item_source = source

    def __str__(self):
        s = f"Magic Item: {self.item_name}. Source: {self.item_source}."
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

    def delete_item(self, index):
        """
        This method deletes a Gem or Valuable item from the item_list attribute
        using the index of the item. It acts similar to pop, returning the item
        removed from self.item_list. There is an error trap to prevent removal
        of a non-existent object from stopping execution.
        :param index: int
        :return: Gem, Valuable, or False
        """
        max_index = len(self.item_list)
        if max_index > index:
            item = self.item_list.pop(index)
            print(f"OtherWealth.delete_item: Item, {item}, removed from "
                  f"OtherWealth object at index {index}.")
            return item
        else:
            error_msg = (f"OtherWealth.delete_item: Index is out of range "
                         f"for this object. max_index is {max_index-1}.")
            print(error_msg)
            return False


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

    def add_item(self, item, index=None):
        """
        This method adds an item to Treasure.item_list. The item must
        be of type Coin, MagicItem, or OtherWealth. Any other object
        type will raise a TypeError.
        :param item: object of type Coin, MagicItme, or OtherWealth
        :param index: int, defaults to None
        :return: None
        """
        if (isinstance(item, Coin) or
                isinstance(item, OtherWealth) or
                isinstance(item, MagicItem)):
            if index is not None:
                self.item_list.insert(index, item)
            else:
                self.item_list.append(item)
        elif (isinstance(item, Gem) or
                isinstance(item, Valuable)):
            error_msg = (f"Treasure.add_item: Gems and Valuable items "
                         f"must be added to an OtherValuable object "
                         f"and the latter added to Treasure.")
            raise TypeError(error_msg)
        else:
            error_msg = (f"Treasure.add_item: Items supplied as arguments "
                         f"to this class must be of type Coin, "
                         f"MagicItem, or OtherWealth, not type, "
                         f"{type(item)}.")
            raise TypeError(error_msg)

    def remove_item(self, index: int):
        """
        This method removes a treasure item from the item_list attribute.
        It included error trapping to prevent IndexError from stopping
        execution. It will produce an error message. It returns True if
        the index exists, False otherwise.
        :param index: int
        :return: bool
        """
        try:
            item = self.item_list.pop(index)
        except IndexError:
            print(f"Treasure.remove_item: The index, {index} is out of "
                  f"range. The actual max index is "
                  f"{len(self.item_list)-1}.")
            return False
        else:
            print(f"Treasure.remove_item: item {item} removed from Treasure.")
            print(f"Treasure.remove_item: Treasure is now {self}.")

    def replace_item(self, index, new_item):
        """
        This method replaces a treasure item from the item_list attribute
        with a new item of Coin, MagicItem, or OtherValuable type.
        It includes error trapping to prevent IndexError from stopping
        execution. It will produce an error message instead. This method
        returns True if the index exists, False otherwise.
        :param index: int
        :param new_item: a Coin, MagicItem, or OtherValuable object
        :return: bool
        """
        max_range = len(self.item_list)
        print(f"Treasure.replace_item: index: {index}. max_range: {max_range}.")
        if (isinstance(new_item, Coin) or
                isinstance(new_item, MagicItem) or
                isinstance(new_item, OtherWealth)):
            if index >= max_range:
                print(f"Treasure.replace_item: Index is out of range for "
                      f"this treasure object. Max index is {max_range - 1}.")
                return False
            else:
                item = self.item_list[index]
                self.item_list[index] = new_item
                print(f"Treasure.replace_item: Item {item} has been replaced "
                      f"with new item {new_item}. Treasure is now: {self}.")
        elif isinstance(new_item, Gem) or isinstance(new_item, Valuable):
            error_msg = (f"Treasure.replace_item: Gem and Valuable items "
                         f"must be added to an OtherValuable and the latter "
                         f"added to Treasure.")
            raise TypeError(error_msg)
        else:
            error_msg = (f"Treasure.replace_item: Treasure can onl use Coin, "
                         f"MagicItem, and OtherValuable objects, not "
                         f"{type(new_item)}.")
            raise TypeError(error_msg)


if __name__ == "__main__":
    desc_item_1 = "+1 Weapon"
    desc_item_2 = "healing potion"
    desc_item_3 = "robe of the archmage"
    desc_item_4 = "magic gumballs"
    source_item_1 = "Book of Weapons 1"
    source_item_2 = "Book of Potions 1"
    source_item_3 = "Book of Armor 10"
    source_item_4 = "Book of Foods Creating Breath Weapons"

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
    coin5 = Coin(45, "gp")
    print("Cash as coins created.")

    magic_item_1 = MagicItem(desc_item_1, source_item_1)
    magic_item_2 = MagicItem(desc_item_2, source_item_2)
    magic_item_3 = MagicItem(desc_item_3, source_item_3)
    magic_item_4 = MagicItem(desc_item_4, source_item_4)
    print(f"Magic items: {magic_item_1}, {magic_item_2}, {magic_item_3}, "
          f"{magic_item_4}.")

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

    print(f"main: Testing Treasure.add_item with index argument.")
    treasure_1.add_item(magic_item_4, 1)
    treasure_3.add_item(magic_item_4, index=0)
    for item in (treasure_1, treasure_2, treasure_3):
        print(item)

    print(f"main: Testing removal of an item from each treasure object.")
    treasure_1.remove_item(0)
    treasure_2.remove_item(1)
    treasure_3.remove_item(2)

    for item in (treasure_1, treasure_2, treasure_3):
        print(item)

    print(f"main: Testing Treasure.replace_item.")
    treasure_3.replace_item(2, coin3)
    treasure_1.replace_item(2, magic_item_1)

    for item in (treasure_1, treasure_2, treasure_3):
        print(item)

    print(f"main: Testing removal of Gems and Valuables from OtherWealth "
          f"objects.")
    print(f"main: The first test will produce an error message withouth "
          f"stopping execution.")
    other_wealth_1.delete_item(2)
    other_wealth_2.delete_item(0)
    other_wealth_3.delete_item(1)
    for item in (other_wealth_1, other_wealth_2, other_wealth_3):
        print(f"main: {item}")
