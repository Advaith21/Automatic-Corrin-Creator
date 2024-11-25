# Automatic-Corrin-Creator
This is a program that takes in data from a Google Sheets and outputs Corirns based on the information within the spreadsheet.

## What you need to make this tool work:
1. A Corrinquest sign-up sheet. If you don't have one, you can use mine as a base: https://forms.gle/rQw8LUxbVgC5eVvt6
2. The resulting Google Sheet file from the output of that Form.
3. Python of version at least 3.12.1
4. A Python IDE like PyCharm or Anaconda


## What the tool can edit:
1. Name
2. Gender / Build
3. Hairstyle / Hair Color (Allows custom hex colors)
4. Hair Pin (automatically validated for F!Corrin only)
5. Facial Detail
6. Voice
7. Boon/Bane (Validates to not allow impossible combinations like +Str -Str)
8. Base Class and Promotion (3 modes to choose from for promotion freedom)
9. Skill slot editing (Including allowing Corrin's slots to contain skills that are normally personals, like Bloodthirst)
10. Skill budgeting with modifiable values (Each submission gets X points to buy skills which cost more the more powerful they are)
11. Level, Internal Level, and automatic stat calculation
12. Weapon Rank auto-levelling

__What the tool should be able to handle but isn't yet tested on:__
1. Picking from 1-3 routes (The tool is optimized for 3 routes simultaneously and not for only 1 or 2 routes yet)
3. Inventory (Kind of a nebulous topic, what should a Corrin join with, but theoretically possible)

__What the tool is not planning to be able to do:__
1. Editing Corrin's accessories

## Files and what they do:
### Corrin.py
Defines a class "Corrin." This class contains all the attributes that will be used to directly edit the hex of a .fe14unit file. This file also validates all values passed into it, for example, making sure that the name it is passed in is actually valid.
### CorrinValidator.py
Given a dataframe, the budget of the run, whether one is playing each route, and information about the promotion mode, this file defines a class "CorrinValidator." It validates all the Corrins and drops any Corrins that aren't according to the specifications, marking it down in error.txt
### corrin_editing.py
Contains the functions actually used to edit the .fe14unit files. This file also contains a number of constant values used to keep track of where the location of different sets of data can be found. For example, the byte that contains the hex value for Corrin's current class is found at index 30.
### edit_this.py
Contains all constants that a Python-unfamiliar user should edit and their significance. This will contain things like skill_prices, a dictionary which allows users to define the prices of all skills, with -1 meaning the skill is illegal and PLAYING_BIRTHRIGHT, PLAYING_CONQUEST, and PLAYING_REVELATION, boolean constants which will inform the program about which routes the player is and is not playing. FINALLY, IMPORTANTLY, IF YOU ARE MAKING YOUR OWN SIGN-UP SHEET, YOU HAVE TO EDIT THE CONSTANTS IN THIS DOCUMENT SO THE PROGRAM DOES NOT TRY TO ACCESS INVALID INDICES.
### skills.py
Contains several dictionaries mapping skills by name to different values. skills_dict contains the hex values for each skill, and  skill_learn_values contains the encoded hex values for each skill that are used to define what skills a Corrin has learned.
### modifiers.py
Contains several arrays which carry information about how Corrin's boon/bane will affect their bases, growths, and caps and a function which calculates a Corrin's stat sheet from Chapter 7 all the way till Endgame when given their boon, bane, base class, and promoted class.
### classes.xlsx and classes.py
Contain all valid non-enemy-only classes (also excludes the DLC Pegasus Knight class) and their information. This information includes their name, tier, bases, growths, caps, weapon type access, promotions, and their in-game hex code ID, which allows us to edit Corrin's current class.
### gain_formulas.xlsx and weapon_ranks.py
Contains the information needed to automatically assign each Corrin their weapon ranks at their join time. gain_formulas contians a list of rates at which Corrins need to gain weapon rank to go from a specific rank to another (e.g. D rank to B rank unpromoted). weapon_ranks.py contains one member function, calculate_weapon_sheet, that uses this information and spits out a 21x8 NumPy array that can be referenced to create a set of weapon ranks for each Corrin for each chapter.
### Crash.fe14unit
Crash is the Adam. The Ymir. He is the first Corrin that every Corrin is made in the image of, and he will be venerated as such by us not really doing anything to venerate him it's just the Corrin that serves as a base Corrin.
### main.py
Contains all of the functionality of the program. main.py actually opens and imports the data from the google sheet, turns it into a Pandas DataFrame, passes it into CorrinValidator, creates the Corrin objects, and creates the new .fe14unit files.
