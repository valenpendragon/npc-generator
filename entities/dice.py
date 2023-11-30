import random


class Dice:
    """This class implements the basic functions of random dice roll. It also
     implements the following additional concepts:
        Roll X dice and drop Y highest or lowest dice.
        Advantage (roll 2 dice for each die rolled and keep the highest)
        Disadvantage (roll 2 dice for each die rolled and keep the lowest)."""

    def __init__(self, dice_size: int, roll_type="normal",
                 dice_number=1, drop_number=0, highest=True):
        """
        The values for dice_size and dice_number must be positive integers. Values
        for roll_type must be "normal", "advantage", or "disadvantage". drop_number
        must be a positive integer or zero. It determines how many dice values to
        drop. highest determines if the lowest 'drop_number' are dropped from the
        aggregate (True) or the highest 'drop_number' (False).
        :param dice_size: int, greater than one
        :param roll_type: str, "normal", "advantage", or "disadvantage"
        :param dice_number: int, greater than zero
        :param drop_number: int, 0 or positive integer less dice_number
        :param highest: bool
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
