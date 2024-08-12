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

### config.json

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

