from abc import ABC
from .dice import Dice


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
    This class will also contain the attributes listed belows. The
    table lists attribute, the class required to store it, and a
    description or restricted list of a possible values:

        Attribute       Class           Description
        ---------------------------------------------------------------------
        name            str             name of the Creature
        size            str             ['tiny', 'small', 'medium', 'large',
                                         'huge', 'gargantuan', 'titanic']
        type            str             ['aberration', 'beast', 'celestials',
                                         'constructs', 'dragons', 'elementals',
                                         'fey', 'fiends', 'giants', 'humanoids',
                                         'monstrosities', 'oozes', 'plant',
                                         'undead']
        cr              float           challenge rating
        difficulty      str             ['normal', 'elite']
        legendary       bool            only True for legendary Creatures
        armor_class     int             creature's AC
        hit_points      int             can store the quick estimate or actual HP
        hit_dice        Dice            stores the number and type of Dice (and
                                        roll the actual if needed
        speed           Speed           dictionary of the creatures speeds
        strength        Stat            the strength ability score
        constitution    Stat            the constitution ability score
        dexterity       Stat            the dexterity ability score
        intelligence    Stat            the intelligence ability score
        wisdom          Stat            the wisdom ability score
        charisma        Stat            the charisma ability score
        prof_bonus      int             Creature's proficiency bonus, if any
        maneuver_dc     int             difficulty class of Creature's attacks
        skills          list of Skill   list of Skills
        resistances     list of str     list of resistances to damage types
        immunities      list of str     list of condition and damage immunities
        vulnerabilities list of str     list of damage types the Creature is
                                        vulnerable to
        senses          list of Sense   list of Senses, if any
        languages       list of str     list of languages Creatures knows, can include
                                        'telepathy'
        abilities       list of str     list of abilities
        actions         list of Action  any ability that can used as an action
        reactions       list of Action  any ability that can used as a reaction
        bonus_actions   list of Action  any ability that can used as a bonus action
        spell_casting   SpellCasting    must exist for innate, psionic, or normal
                                        spellcasting; should be None for any creature
                                        that has no spellcasting ability
        legendary_actions list of Action any legendary ability, most of which are
                                         LimitedUseAction
        legendary_resists list of Action any legendary resistances, most of which are
                                         LimitedUseAction

    Note: actions, reactions, bonus_actions, and legendary_actions can contain
    LimitedUseAction.
    """
    pass


class Stat:
    """
    This class stores attributes for a stat of a Creature. The
    attributes are value (int) and modifier (int).
    """
    pass


class Sense:
    """
    This class stores 3 attributes: name of sense (str), range of sense (int),
    and description of sense (str). That last one can be blank. Sense names
    should be restricted to ['blindsight', 'darkvision', 'tremorsense', and
    'truesight'].
    """
    pass


class Spell:
    """
    This class stores data on a spell or spell-like ability that
    appears in a Creature's potential actions. The attributes are:
        Attribute   Class       Description
        name        str         name of the spell
        desc        str         descriptive text of the spell
        range       int         distance in ft that it can be cast,
                                if short/long are defined, use long,
                                0 indicates touch, 5 indicate melee
                                range
        type        str         damage type it can inflict
        damage      Dice        the number and type of dice used to roll
                                the damage, use dice=0 and dice_no=0
                                for spells that do not do specific damage
        dice_mod    int         this attribute stores -1 for disadvantage
                                0 for normal roll, and +1 for advantage
        damage_mod  int         modifier for the attack damage after
                                rolling
        innate      bool        False for normal spellcasting, True for
                                innate spell abilities
        frequency   int         0 for normal spells, non-zero for any
                                ability that has a specified number of
                                times per day or long/short rest that
                                it may be used
    dice defaults to 0, dice_no to 0, dice_mod to 0  mod to 0, innate to
    False, and frequency to 0.
    """
    def __init__(self, name: str, desc: str, range: int, dice=0,
                 dice_no=0, dice_mod=0, mod=0, innate=False,
                 frequency=0):
        self.name = name
        self.desc = desc
        self.range = range
        self.mod = mod
        self.innate = innate
        self.frequency = frequency
        self.dice_mod = dice_mod
        if dice != 0 and dice_no != 0:
            if dice_mod == -1:
                self.damage = Dice(dice, dice_number=dice_no,
                                   roll_type="disadvantage")
            elif dice_mod == 1:
                self.damage = Dice(dice, dice_number=dice_no,
                                   roll_type="advantage")
            else:
                self.damage = Dice(dice, dice_number=dice_no)
        else:
            self.damage = None


class SpellCasting:
    """
    This class contains the casting level of the Creature, spell slots,
    and instances of Spell for spells. It can be used for innate and
    normal spellcasting.
    """
    pass


class Action:
    """
    This class stores data on actions that a creature can take on its
    turn. This includes attributes: name(str), attack_type (str), bonus_to_hit
    (int), range (int), area_of_effect (str), damage (Dice or int), damage type
    (str), and description (str). Only description is required.
    """
    pass


class LimitedUseAction(Action):
    """
    This class adds all of the options listed in Action and adds additional
    attributes: dictionary. The acceptable key:value pairs are:
        'x/day': int, at least 1
         recharge': Dice
        'rest recharge': str, 'short' or 'long'
        'bloodied': bool, default False
    The LimitedUseAction can have any or all of the modifiers present. Any that
    appear modify how it works.
    """
    pass


class MultiAttack:
    """
    This class specifies the number of attacks permitted to the creature
    and which of the attacks this applies to.
    """
    pass


class Speed:
    """
    This class stores the Creature's movement rates. The dictionary
    class is used to keep the speeds straight. There is 1 required
    speed: walk. Other speeds can be added with optional keywords:
    burrow, climb, fly, and swim.
    """
    pass


class Skill:
    """
    This class store skills, along with modifiers. The modifiers
    include: stat mod, proficiency bonus, and expertise dice (which
    uses Dice class).
    """
    pass
