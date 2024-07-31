from random import randint


class Dice:
    """This class implements the basic functions of random dice roll. It also
     implements the following additional concepts:
        Roll X dice and drop Y highest or lowest dice.
        Advantage (roll 2 dice for each die rolled and keep the highest)
        Disadvantage (roll 2 dice for each die rolled and keep the lowest)."""

    def __init__(self, dice_size: int, roll_type="normal",
                 dice_number=1, drop_number=0, highest=True,
                 debug=False):
        """
        The values for dice_size and dice_number must be positive integers. Values
        for roll_type must be "normal", "advantage", or "disadvantage". drop_number
        must be a positive integer or zero. It determines how many dice values to
        drop. highest determines if the lowest 'drop_number' are dropped from the
        aggregate (True) or the highest 'drop_number' (False).

        The debug argument reduces the number of messages appearing in the program
        output from this Class.
        :param dice_size: int, greater than one
        :param roll_type: str, "normal", "advantage", or "disadvantage"
        :param dice_number: int, greater than zero
        :param drop_number: int, 0 or positive integer less dice_number
        :param highest: bool
        ":param debug: bool, defaults to False
        """

        # Check the values of the parameters.
        if dice_size <= 1:
            raise ValueError(f"Dice: dice_size must be a positive integer greater than "
                             f"1. Value provided is {dice_size}.")
        if roll_type.lower() not in ("normal", "advantage", "disadvantage"):
            raise ValueError(f"Dice: roll_type must equal 'normal', 'advantage', "
                             f"or 'disadvantage'. Value provided is {roll_type}")
        if not isinstance(dice_number, int):
            raise ValueError(f"Dice: dice_number must be a positive integer. The "
                             f"variable type provided is {type(dice_number)}")
        elif dice_number < 1:
            raise ValueError(f"Dice: dice_number must be a positive integer. Value "
                             f"provided is {dice_number}.")
        if not isinstance(drop_number, int):
            raise ValueError(f"Dice: drop_number must be a positive integer or 0. The "
                             f"variable type provided is {type(drop_number)}")
        elif drop_number < 0:
            raise ValueError(f"Dice: drop_number must be a positive integer or 0. "
                             f"Value provided is {drop_number}.")
        elif drop_number >= dice_number:
            raise ValueError(f"Dice: drop_number must less than dice_number. Values"
                             f"provided are drop_number: {dice_number} and "
                             f"dice_number: {dice_number}.")

        self.dice_size = dice_size
        self.roll_type = roll_type
        self.number_of_rolls = dice_number
        self.number_of_rolls_dropped = drop_number
        self.drop_lowest = highest
        self.debug = debug

    def __str__(self):
        output = f"dice_size: {self.dice_size}\n" \
                 f"roll_type: {self.roll_type}\n" \
                 f"number_of_rolls: {self.number_of_rolls}\n" \
                 f"number_of_rolls_dropped: {self.number_of_rolls_dropped}\n" \
                 f"drop_lowest: {self.drop_lowest}"
        return output

    def __repr__(self):
        output = f"Dice({self.dice_size}, roll_type={self.roll_type}, dice_number={self.number_of_rolls}," \
                 f"highest={self.drop_lowest})"
        return output

    def _roll_advantage(self):
        roll1 = randint(1, self.dice_size)
        roll2 = randint(1, self.dice_size)
        if self.debug:
            print(f"Dice.roll_advantage: roll1: {roll1}. roll2: {roll2}")
        if roll1 >= roll2:
            return roll1
        else:
            return roll2

    def _roll_disadvantage(self):
        roll1 = randint(1, self.dice_size)
        roll2 = randint(1, self.dice_size)
        if self.debug:
            print(f"Dice.roll_disadvantage: roll1: {roll1}. roll2: {roll2}")
        if roll1 <= roll2:
            return roll1
        else:
            return roll2

    def roll(self):
        """This method implements the actual roll of the defined dice."""
        rolls = []
        if self.debug:
            print(f"Dice.roll: rolls: {rolls}")
        for n in range(self.number_of_rolls):
            match self.roll_type:
                case "normal":
                    roll = randint(1, self.dice_size)
                case "advantage":
                    roll = self._roll_advantage()
                case "disadvantage":
                    roll = self._roll_disadvantage()

            rolls.append(roll)

        rolls.sort()
        if self.debug:
            print(f"Dice.roll: rolls: {rolls}")
        if self.number_of_rolls_dropped > 0:
            if self.drop_lowest:
                rolls_final = rolls[self.number_of_rolls_dropped:]
            else:
                rolls_final = rolls[0: -self.number_of_rolls_dropped]
            if self.debug:
                print(f"Dice.roll: rolls_final: {rolls_final}")
            return sum(rolls_final)
        else:
            return sum(rolls)


# Useful functions to help use Dice are below.
def return_die_roll(s, debug=False):
    """
    This function takes a string in format ndm or nDm where n and m are
    integers. It will return the die roll called for.
    The parameter, debug, controls the output of debug messages.
    :param s: str
    :param debug: bool, defaults to False
    :return: int
    """
    s = s.lower()
    l = s.split('d')
    if debug:
        print(f"return_die_roll: s: {s}. l: {l}.")
    try:
        n = int(l[0])
        m = int(l[1])
        if debug:
            print(f"return_die_roll: n: {n}. m: {m}.")
    except ValueError:
        error_msg = (f"Dice.return_die_roll: The string provided must be in the "
                     f"format 'ndm' or 'nDm' where n and m are integers. The"
                     f"string supplied is {s}.")
        raise ValueError(error_msg)

    return Dice(m, dice_number=n, debug=debug).roll()


if __name__ == "__main__":
    debug = True
    d6 = Dice(6, debug=debug)
    d8 = Dice(8, debug=debug)
    print(f"main: d6: {d6.roll()}.")
    print(f"main: d8: {d8.roll()}.")
    hit_dice_test8 = Dice(8, dice_number=12, debug=debug)
    print(f"main: 12d8 HD Test: {hit_dice_test8.roll()}")
    hit_dice_test_with_advantage8 = Dice(8, dice_number=12,
                                         roll_type="advantage", debug=debug)
    print(f"main: 12d8 HD Test with Advantage on HD: "
          f"{hit_dice_test_with_advantage8.roll()}")
    hit_dice_test_with_disadvantage8 = Dice(8, dice_number=12,
                                            roll_type="disadvantage", debug=debug)
    print(f"main: 12d8 HD Test with Disadvantage on HD: "
          f"{hit_dice_test_with_disadvantage8.roll()}")
    hit_dice_test10 = Dice(10, dice_number=12, debug=debug)
    print(f"main: 12d10 HD Test: {hit_dice_test10.roll()}")
    hit_dice_test_with_advantage10 = Dice(10, dice_number=12,
                                          roll_type="advantage", debug=debug)
    print(f"main: 12d10 HD Test with Advantage on HD: "
          f"{hit_dice_test_with_advantage10.roll()}")
    hit_dice_test_with_disadvantage10 = Dice(10, dice_number=12,
                                             roll_type="disadvantage", debug=debug)
    print(f"main: 12d10 HD Test with Disadvantage on HD: "
          f"{hit_dice_test_with_disadvantage10.roll()}")
    save = Dice(20, debug=debug)
    print(f"main: Saving Throw: {save.roll()}")
    save_with_advantage = Dice(20, roll_type="advantage", debug=debug)
    print(f"main: Save with Advantage: {save_with_advantage.roll()}")
    save_with_disadvantage = Dice(20, roll_type="disadvantage", debug=debug)
    print(f"main: Save with Disadvantage: {save_with_disadvantage.roll()}")
    stat_roll_4d6_drop_lowest = Dice(6, dice_number=4,
                                     drop_number=1, debug=debug)
    print(f"main: Roll 4d6, drop lowest, and take sum: {stat_roll_4d6_drop_lowest.roll()}")
    stat_roll_4d6_drop_highest = Dice(6, dice_number=4,
                                      drop_number=1, highest=False,
                                      debug=debug)
    print(f"main: Roll 4d6, drop highest, and take sum: "
          f"{stat_roll_4d6_drop_highest.roll()}")
    roll_5d6_drop_lowest_2 = Dice(6, dice_number=5,
                                  drop_number=2, highest=True,
                                  debug=debug)
    print(f"main: Roll 5d6, drop 2 lowest: {roll_5d6_drop_lowest_2.roll()}")
    roll_5d6_drop_highest_2 = Dice(6, dice_number=5,
                                   drop_number=2, highest=False,
                                   debug=debug)
    print(f"main: Roll 5d6, drop 2 highest: {roll_5d6_drop_highest_2.roll()}")
    print(f"main: Testing return_die_roll(2d6): "
          f"{return_die_roll('2d6', debug)}")
    print(f"main: Testing return_die_roll(3d10): "
          f"{return_die_roll('3d10', debug)}")
