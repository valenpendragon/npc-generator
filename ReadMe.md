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

## The JSON Files

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

### config.json

This section describes in detail how to build the config.json. In this file, all of the required files, workbooks, and worksheets are listed explicitly. There is a sample file to assist with this. Understand that the program will use _config.json_ to make sure that it has all of the workbooks, worksheets, and stat data needed for the program to run properly.

Note: There are no optional workbooks or worksheets.

#### Required Tables

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


### conditions.json

### damage_types.json

### highlighting.json

## The Excel Format Workbooks

### test_workbook.xlsx

Placeholder

### Encounter Table Workbook

Placeholder until implemented

### CR-Based Treasure Tables Workbook

### Gems and Valuables Tables Workbook

### Magic Items Tables Workbooks

First off, this program is designed to handle as many workbooks of magic items as you see fit to use. They have to be added to config.json (see section above) and have to be laid out as up to 10 tables. This allows GMs to use all of their books of magic items if they so desire.

