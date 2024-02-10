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
    appears in a Creature's potential actions. The attributes include:
    name (str), which is the name of the spell; innate (bool), False
    for normal spellcasting, True for innate spell abilities; and frequency
    (int), set to 0 for normal spells, non-zero for innate abilities and
    indicated frequency per day or long rest that it can be used.
    """
    pass


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
