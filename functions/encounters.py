from abc import ABC


class Encounter(ABC):
    """
    This abstract base class will be used to create encounters
    of various types by establishing the basic operations for
    any encounter. The likely types to come out of this class
    are: CR-only encounters (generating treasure for an encounter
    already created by another means); complete encounter in which
    the application will help generate creatures while updating the
    overall CR of the encounter; and random encounters which will
    be derived from a random encounter table
    """
    pass


class Creature(ABC):
    """
    This abstract base class establishes basic operations for any
    creature that could be part of an encounter. It also establishes
    the basic attributes of any creature. This will build the stat
    bloc.
    """
    pass


class Spell:
    """
    This class stores data on a spell or spell-like ability that
    appears in a Creature's potential actions. The attributes store
    data on the spell and its effects.
    """
    pass


class SpellCasting:
    """
    This class contains the casting level of the Crea
    """


class Action:
    """
    This class stores data on actions that a creature can take on its
    turn. This includes attack type, bonus to hit, range, area of
    effect, damage, damage type, and description.
    """
    pass


class MultiAttack:
    """
    This class specifies the number of attacks permitted to the creature
    and which of the attacks this applies to.
    """
    pass
