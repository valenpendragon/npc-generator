# This program's purpose is to generate encounters for TTRPGs.

NPC Generator has two main functions:
- Generate characters for the encounter based on encounter tables supplied by the user and options chosen.
- Generate treasure for the encounter based on Challenge Rating (used by SRD5E, Level Up A5E, and Black Flag Tales of the Valiant) initially.
- Generate some interesting background for main characters in the encounter.

This program requires the following files in the /data subdirectory:
- config.json
- conditions.json
- damage_types.json
- highlighting.json
- test_workbook.xlsx (included in package)
- Excel format workbook of encounter tables
- Excel format workbook of treasure tables arranged similar to 5E and A5E
- Excel format workbook of tables of gems and valuables
- at least one Excel format workbook of tables of magic items

The format and content of the json files is described in the sections below. The main program validates each file and provides insight into any problems found. Sample files will be included in the samples subdirectory.

The naming conventions for the workbooks and their worksheets will described in detail below. The format of each worksheet type is also described in detail. There is code built into the app to validate each workbook before proceeding, indicating which worksheets contained problems.

## 1 The JSON Files

Each of the json files are important to the proper functioning of this program. Here is a quick summary of their purposes. This readme assumes that the reader is familiar with json format. There are several editors that handle this format well. I personally recommend PyCharm or Visual Studio Code. That way, you have some feedback that the format breaks json coding itself.

- _config.json_ is the main configuration file of this program. 
- _conditions.json_ lists all of the conditions the game system allows.
- _damage_types.json_ lists all of the types of damages the GM wants to use in encounters. 
- _highlighting.json_ is how the GM tells the program which items will have _emphasis_ and which will have __strong emphasis__ in the programs output. This improves readability.

A word about notation below:
- Curly brackets are {} characters.
- Square brackets are [] characters.
- A semi-colon is this character :
- Double quotes are this character "

### 1.1 config.json

This section describes in detail how to build the config.json. In this file, all of the required files, workbooks, and worksheets are listed explicitly. There is a sample file to assist with this. Understand that the program will use _config.json_ to make sure that it has all of the workbooks, worksheets, and stat data needed for the program to run properly.

Note: There are no optional workbooks or worksheets.

#### 1.1.1 Required Tables

Below is the first section of the config.json. It starts off with "tables". The format is below:

    "tables": {
      "reguired tables": {
        "Encounter Tables Workbook": [
          "Worksheet Title",
          "Worksheet Title",
          "Worksheet Title"
         ],
         "Treasure Tables Workbook": [
           list of worksheet titles separated by commas
         ],
         "Gems and Valuables Workbook": [
           list of worksheet titles separated by commas
         ],
         "Magic Items Workbook": [
           list of workbook titles separated by commas
         ]
        }
      },

The "tables" section must be enclosed in curly brackets. The "required tables" subsection must be enclosed in curly brackets. Remember to put a semi-colon after these names since tables and required tables are keys identifying all of the items enclosed in the curly brackets that follows the semi-colon.

Every workbook name with file extension must be listed as it appears in the /data folder. These filenames must be enclosed in the double quotes  (a json standard). Otherwise, the file will be ignored.

Every worksheet that the program will use must be listed in the list as shown in the Encounter Tables. Each name must be enclosed in double quotes and the items separated by commas except the last entry. The full list of worksheets must be enclosed for each workbook must be enclosed in square brackets.

#### 1.1.2 Stat configuration
Placeholder for stat explanation

### 1.2 conditions.json

The basic format for this file is much simpler than the configuration master. It is a list of *condition*: *description* in a list. Descriptions of the conditions can be list of items to complete the definition of the condition and how it is used in game.

The specific format is below:

    {
      "condition name": [
        "description"
      ],
      "condition nane": [
        "description",
        "additional description",
        "more details"
      ]
    }

The entire list of condition:description pairs are enclosed in curly brackets. The condition name is enclosed in double quotes. The description(s) are enclosed in square brackets in order to contain all of the items needed. Each individual item is enclosed in double quotes and separated by commas.

There can be as many conditions as the user wants to define.

### 1.3 damage_types.json

Damage types uses an even simpler format of name:description pairing. The format is below.

    {
     "damage type": "description",
     "damage type": "description",
     "damage type": "description"
    }

Each damage type and description is enclosed in double quotes. The pair is separated from other pairs by commas.

### 1.4 highlighting.json

This is a required file, but this is where the user can define which words or phrases are emphasized or strongly emphasized in a web publishing sense. This corresponds the methods publishers use to emphasize or strongly emphasize terms or phrases in game book text. This only effects the screen appearance.

The format also straightforward. There are two lists. One is for emphasis, the second for strong emphasis. It can be seen below.

    {
     "emphasis": [
      "word", "more than one word", "word"
     ],
     "strong emphasis": [
      "phrase", "word", "phrase"
     ]
    }

The words, *emphasis* and **strong emphasis** are enclosed in double quotes. The individual words and phrases must be enclosed in double quotes and separated by commas. They can be on more than one line as well to make it easier to edit. The full lists must be enclosed in square brackets. There should be no overlap between the two lists, not even on words in the phrases. So, if the word *action* appears under "emphasis", *bonus action* cannot appear under **strong emphasis*. However, both could appear in the same list.

## 2 The Excel Format Workbooks

### 2.1 test_workbook.xlsx

Placeholder

### 2.2 Encounter Table Workbook

Placeholder until implemented

### 2.3 CR-Based Treasure Tables Workbook

### 2.4 Gems and Valuables Tables Workbook

### 2.5 Magic Items Tables Workbooks

First off, this program is designed to handle as many workbooks of magic items as you see fit to use. They have to be added to config.json (see section above) and have to be laid out as up to 10 tables. This allows GMs to use all of their books of magic items if they so desire.

