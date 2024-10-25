import numpy as np
import pandas as pd
import classes as cs
import skills
from skills import skill_prices_dict
import os
import requests
import sys
import corrin_editing as c_e
import Corrin
import edit_this
import openpyxl


error_file = open("error.txt", "w")


def log_error(message):
    error_file.write(message + "\n")


def make_valid_dir_name(s):
    s = s.replace("\\", "_")
    s = s.replace("/", "_")
    s = s.replace(":", "_")
    s = s.replace("*", "_")
    s = s.replace("?", "_")
    s = s.replace("\"", "_")
    s = s.replace("<", "_")
    s = s.replace(">", "_")
    s = s.replace("|", "_")
    return s


def is_valid_hex_string(s):
    valid_chars = "0123456789abcdefABCDEF"
    return all(char in valid_chars for char in s)


def validate_corrin(df, mode, BR, CQ, REV, budget):
    to_be_removed = []
    for inn, r in df.iterrows():
        to_be_removed = to_be_removed + validate_skills(row=r, index=inn, BR=edit_this.PLAYING_BIRTHRIGHT,
                                                        CQ=edit_this.PLAYING_CONQUEST, REV=edit_this.PLAYING_REVELATION,
                                                        budget=edit_this.BUDGET)
        to_be_removed = to_be_removed + validate_boon_bane(row=r, index=inn, BR=edit_this.PLAYING_BIRTHRIGHT,
                                                           CQ=edit_this.PLAYING_CONQUEST,
                                                           REV=edit_this.PLAYING_REVELATION)
        to_be_removed = to_be_removed + validate_promotion(mode=edit_this.PROMOTION_MODE, row=r, index=inn,
                                                           BR=edit_this.PLAYING_BIRTHRIGHT,
                                                           CQ=edit_this.PLAYING_CONQUEST,
                                                           REV=edit_this.PLAYING_REVELATION)
        to_be_removed = to_be_removed + validate_body(row=r, index=inn)
        to_be_removed = to_be_removed + validate_name(row=r, index=inn)
        to_be_removed = to_be_removed + validate_face(row=r, index=inn)
        to_be_removed = to_be_removed + validate_hairstyle(row=r, index=inn)
        to_be_removed = to_be_removed + validate_hair_color(row=r, index=inn, df=df)
        to_be_removed = to_be_removed + validate_decoration(row=r, index=inn)
        to_be_removed = to_be_removed + validate_voice(row=r, index=inn)
        to_be_removed = to_be_removed + validate_detail(row=r, index=inn)
    to_be_removed = list(set(to_be_removed))
    df = df.drop(to_be_removed, inplace=True)


def validate_promotion(mode, row, index, BR, CQ, REV):
    """
    This function does two things. Depending on the mode selected, it makes sure that the base class of all Corrins
    can be promoted into the promoted class of those Corrins, and it makes sure that DLC classes cannot be entered before promotion.
    :param mode: Integer. Must be 1-3, inclusive. Tells the function what classes are allowed.
    :param row: Pandas Series. The current Corrin that is being edited.
    :param BR: Boolean. Are you playing Birthright this run? True if yes, False if no.
    :param CQ: Boolean. Are you playing Conquest this run? True if yes, False if no.
    :param REV: Boolean. Are you playing Revelation this run? True if yes, False if no.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    # Validation for mode as an integer between 1 and 3 inclusive
    if not 1 <= mode <= 3:
        print(
            f"ERROR IN validate_promotion: Invalid mode selection. You picked {mode}, which is invalid. Pick one of the following:\n"
            f"1: Only allow promotions into original promo set + DLC classes you share a weapon type with (eg. Fighter can promo into Hero, Berserker, Dread Fighter or Vanguard.\n"
            f"2: Allow promotions into any class you share a weapon type with (eg. Nohr Prince can promote into Wolfssegner)\n"
            f"3: Allow promotions into any class. The only validation this function will perform is to make sure Corrin can't be in a DLC/Amiibo class unpromoted."
        )
        return False
    if not isinstance(mode, int):
        print(
            f"ERROR IN validate_promotion: Invalid mode selection. You picked {mode}, which is not an integer. Pick one of the following:\n"
            f"1: Only allow promotions into original promo set + DLC classes you share a weapon type with (eg. Fighter can promo into Hero, Berserker, Dread Fighter or Vanguard.\n"
            f"2: Allow promotions into any class you share a weapon type with (eg. Nohr Prince can promote into Wolfssegner)\n"
            f"3: Allow promotions into any class. The only validation this function will perform is to make sure Corrin can't be in a DLC/Amiibo class unpromoted."
        )
        return False

    drop = False
    # For each route we only access the class info if the boolean is true, because if we try to otherwise it'll throw an error.
    if BR:
        drop = drop and (not validate_promotion_helper(mode, row[edit_this.BASE_CLASS_BR][0],
                                                       row[edit_this.PROMOTED_CLASS_BR][0],
                                                       row[edit_this.NAME][0]))
    if CQ:
        drop = drop and (not validate_promotion_helper(mode, row[edit_this.BASE_CLASS_CQ][0],
                                                       row[edit_this.PROMOTED_CLASS_CQ][0],
                                                       row[edit_this.NAME][0]))
    if REV:
        drop = drop and (not validate_promotion_helper(mode, row[edit_this.BASE_CLASS_REV][0],
                                                       row[edit_this.PROMOTED_CLASS_REV][0],
                                                       row[edit_this.NAME][0]))
    # If any of the validations come back false, this Corrin must be dropped.
    if drop:
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_promotion_helper(mode, base_class, promoted_class, cor_name):
    """
    This function is a helper function that returns true or false for just one Corrin. It should only be called by validate_promotion.
    :param mode: Integer. Must be 1-3, inclusive. Tells the function what classes are allowed.
    :param base_class: String. Class the Corrin is promoting from.
    :param promoted_class: String. Class the Corrin is promoting into.
    :param cor_name: String. Name of the Corrin. This is only used for error messages, so it's easier to debug.
    :return: Boolean. Returns true if this promotion is valid. Returns false if this promotion is invalid.
    """
    bc_series = cs.classes[cs.classes["Name"] == base_class]
    pc_series = cs.classes[cs.classes["Name"] == promoted_class]

    # Mode 1: Classes can only promote into classes that they'd normally be able to promote into and Amiibo/DLC
    # classes they share weapon types with.
    if mode == 1:
        # Step 1: Check to make sure that we have a valid base/promotion class in terms of tiers. If not,
        # send an error message and return.
        if bc_series["Tier"].tolist()[0] != 1:
            log_error(f"Invalid base class of {base_class} for Corrin \"{cor_name}\"")
            return False
        if pc_series["Tier"].tolist()[0] == 1:
            log_error(f"Invalid promoted class of {promoted_class} for Corrin \"{cor_name}\"")
            return False

        # Step 2: Obtain weapon types of unpromoted and promoted classes and valid promo options.
        bc_weapons = bc_series['Weapon Types'].tolist()[0]
        pc_weapons = pc_series['Weapon Types'].tolist()[0]
        bc_promo = bc_series['Promotions'].tolist()[0]
        valid = False

        # Step 3: Check if the promotion is a valid non-DLC/Amiibo one.
        for i in range(0, len(bc_promo)):
            if bc_promo[i] == promoted_class:
                return True

        # Step 4: At this point all promotions should be into DLC/Amiibo classes. If promoted_class is tier 2,
        # this promotion is invalid.
        if pc_series['Tier'].tolist()[0] != 3:
            log_error(f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\",\n"
                      f"as the promoted class is not DLC/Amiibo and is not in the base class's usual promo options.")
            return False

        # Step 5: Only promoted classes left are DLC/Amiibo, so we just check for weapon type commonality.
        for i in range(0, len(bc_weapons)):
            for j in range(0, len(pc_weapons)):
                if bc_weapons[i] == pc_weapons[j]:
                    valid = True
        if not valid:
            log_error(f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\".\n"
                      f"Under this mode, you cannot promote into a DLC/Amiibo class you don't share any weapon types with.")
            return False
        else:
            return True

    # Mode 2: Classes can promote into any class they share at least one weapon type with.
    if mode == 2:
        # Step 1: Check to make sure that we have a valid base/promotion class in terms of tiers. If not,
        # send an error message and return.
        if bc_series["Tier"].tolist()[0] != 1:
            log_error(f"Invalid base class of {base_class} for Corrin \"{cor_name}\"")
            return False
        if pc_series["Tier"].tolist()[0] == 1:
            log_error(f"Invalid promoted class of {promoted_class} for Corrin \"{cor_name}\"")
            return False

        # Step 2: Obtain weapon types of unpromoted and promoted classes.
        bc_weapons = bc_series['Weapon Types'].tolist()[0]
        pc_weapons = pc_series['Weapon Types'].tolist()[0]
        valid = False

        # Step 3: Because all classes you normally can promote into are classes you always share a weapon type with,
        # we only have to check weapon type commonality.
        for i in range(0, len(bc_weapons)):
            for j in range(0, len(pc_weapons)):
                if bc_weapons[i] == pc_weapons[j]:
                    valid = True
        if not valid:
            log_error(
                f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\".\nThe classes do not share a weapon type.")
            return False
        else:
            return True

    # Mode 3: Unrestricted promotions. Just check to make sure base_class is not a DLC/Amiibo class. YOU CAN CHANGE
    # THIS RESTRICTION BY EDITING THE FIRST IF STATEMENT TO READ "if bc_series["Tier"].tolist()[0] == 2:".
    if mode == 3:
        # Step 1: Check to make sure that we have a valid base/promotion class in terms of tiers. If not, send an error message and return.
        if bc_series["Tier"].tolist()[0] != 1:
            log_error(f"Invalid base class of {base_class} for Corrin \"{cor_name}\"")
            return False
        if pc_series["Tier"].tolist()[0] == 1:
            log_error(f"Invalid promoted class of {promoted_class} for Corrin \"{cor_name}\"")
            return False
        else:
            return True


def validate_boon_bane(row, index, BR, CQ, REV):
    """
    Makes sure all the Corrin's boons and banes aren't identical for a route, as that is impossible.
    Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :param BR: Boolean. Are you playing Birthright this run? True if yes, False if no.
    :param CQ: Boolean. Are you playing Conquest this run? True if yes, False if no.
    :param REV: Boolean. Are you playing Revelation this run? True if yes, False if no.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    drop = False
    if BR and row[edit_this.BOON_BR] == row[edit_this.BANE_BR]: drop = True
    if CQ and row[edit_this.BOON_CQ] == row[edit_this.BANE_CQ]: drop = True
    if REV and row[edit_this.BOON_REV] == row[edit_this.BANE_REV]: drop = True
    if drop:
        log_error(f"Corrin \'{row[edit_this.NAME]}\''s boon/bane input was invalid.")
        log_error(f"Birthright - Boon: {row[edit_this.BOON_BR]}, Bane: {row[edit_this.BANE_BR]}")
        log_error(f"Conquest - Boon: {row[edit_this.BOON_CQ]}, Bane: {row[edit_this.BANE_CQ]}")
        log_error(f"Revelation - Boon: {row[edit_this.BOON_REV]}, Bane: {row[edit_this.BANE_REV]}")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_body(row, index):
    """
    Makes sure all the Corrin's build values are valid. Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    if row[edit_this.BUILD] != 1 and row[edit_this.BUILD] != 2:
        print(f"Corrin \'{row[edit_this.NAME]}\''s body type input of {row[edit_this.BUILD]} was invalid.")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_name(row, index):
    """
    Makes sure all the Corrin's names are valid. Removes leading and trailing whitespace. Returns all invalid Corrin
    indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    row[edit_this.NAME] = row[edit_this.NAME].strip()
    if not 1 <= len(row[edit_this.NAME]) <= 8:
        log_error(f"Corrin \'{row[edit_this.NAME]}\''s name input was invalid.")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_face(row, index):
    """
    Makes sure all the Corrin's face values are valid. Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    if not 1 <= row[edit_this.FACE] <= 7:
        print(f"Corrin \'{row[edit_this.NAME]}\''s face input of {row[edit_this.FACE]} was invalid.")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_hairstyle(row, index):
    """
    Makes sure all the Corrin's face values are valid. Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    if not 1 <= row[edit_this.HAIRSTYLE] <= 12:
        print(f"Corrin \'{row[edit_this.NAME]}\''s hairstyle input of {row[edit_this.HAIRSTYLE]} was invalid.")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_detail(row, index):
    """
    Makes sure all the Corrin's facial features are valid. Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    if not 0 <= row[edit_this.FACIAL_FEATURE] <= 12:
        print(
            f"Corrin \'{row[edit_this.NAME]}\''s facial feature input of {row[edit_this.FACIAL_FEATURE]} was invalid.")
        indices_to_drop.append(index)
    # Drop the invalid rows
    return indices_to_drop


def validate_voice(row, index):
    """
    Makes sure all the Corrin's voices are valid. Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    if not 1 <= row[edit_this.VOICE] <= 3:
        print(f"Corrin \'{row[edit_this.NAME]}\''s voice input of {row[edit_this.VOICE]} was invalid.")
        indices_to_drop.append(index)

    # Drop the invalid rows
    return indices_to_drop


def validate_hair_color(row, index, df):
    """
    Checks the hair color value of the given dataframe and makes sure it's a valid hex value.
    It also converts any uppercase characters to lowercase characters.
    If there is a # at the start of the hex code, this parses it properly.
    Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []
    # Step 1: Convert all letters to lowercase as that's what the .fe14unit file needs and store it in a variable.
    h_string = row[edit_this.HAIR_COLOR].lower()
    h_string = h_string.strip()

    if len(h_string) < 6:
        indices_to_drop.append(index)
        log_error(
            f"Corrin '{row[edit_this.NAME]}'s hair color input of '{row[edit_this.HAIR_COLOR]}' was invalid.")

    # Step 2: Handle the case where the user properly input the hex values.

    elif is_valid_hex_string(h_string) and len(h_string) == 6:
        h_string = h_string

    # Step 3: Handle the case where the user input a hex string but then some extra stuff after it.
    elif is_valid_hex_string(h_string[0:6]):
        h_string = h_string[0:6]

    # Step 4: Handle the case where the user improperly input the hex value as "#rrggbb" instead of just "rrggbb".
    elif h_string[0] == "#" and len(h_string) == 7 and is_valid_hex_string(h_string[1:]):
        h_string = h_string[1:]

    # If we reach this else statement then we've encountered something either unparsable or something we can
    # parse but don't know how yet.
    else:
        indices_to_drop.append(index)
        log_error(
            f"Corrin '{row[edit_this.NAME]}'s hair color input of '{row[edit_this.HAIR_COLOR]}' was invalid.")

    df.at[index, edit_this.HAIR_COLOR] = h_string
    # Drop the invalid rows
    return indices_to_drop


def validate_decoration(row, index):
    """
    Makes sure all the Corrin's decorations are valid and that male Corrins do not have any hair pins.
    Returns all invalid Corrin indices.
    :param row: Pandas Series. The current Corrin that is being edited.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    """
    indices_to_drop = []

    if row[edit_this.GENDER] == "Male" and row[edit_this.HAIR_CLIP] != 0:
        row[edit_this.HAIR_CLIP] = 0
    elif not 0 <= row[edit_this.HAIR_CLIP] <= 5:
        print(f"Corrin \'{row[edit_this.NAME]}\''s hair pin input of {row[edit_this.HAIR_CLIP]} was invalid.")
        indices_to_drop.append(index)

    # Drop the invalid rows
    return indices_to_drop


def validate_skills(row, index, BR, CQ, REV, budget):
    '''
    Makes sure all of each Corrin's skills are valid and checks for banned skills. Logs all problems with Corrins
    and returns indices of problem Corrins.
    :param row: Pandas Series. The current Corrin that is being edited.
    :param BR: Boolean. Are you playing Birthright this run? True if yes, False if no.
    :param CQ: Boolean. Are you playing Conquest this run? True if yes, False if no.
    :param REV: Boolean. Are you playing Revelation this run? True if yes, False if no.
    :param budget: Int. The combined values of all the skills should not exceed this budget value. If it does, the Corrin will be dropped.
    :return: indices_to_drop: List. Indices of all Corrins that violated the validation in this function.
    '''
    routes = 0
    indices_to_drop = []

    if BR: routes += 1
    if CQ: routes += 1
    if REV: routes += 1
    if routes == 0:
        print("ERROR. ZERO ROUTES SELECTED.")
        exit(1)

    current_skill_sum = 0
    if BR:
        current_skill_sum += skill_sum(row[edit_this.SKILLS_BR])
    if CQ:
        current_skill_sum += skill_sum(row[edit_this.SKILLS_CQ])
    if REV:
        current_skill_sum += skill_sum(row[edit_this.SKILLS_REV])
    if current_skill_sum < 0:
        log_error(f"Corrin \'{row[edit_this.NAME]}\''s skillset contains at least one banned skill.")
        indices_to_drop.append(index)
    if current_skill_sum > budget:
        log_error(f"Corrin \'{row[edit_this.NAME]}\''s skillset is over budget.")
        indices_to_drop.append(index)

    # Drop the invalid rows
    return indices_to_drop


def skill_sum(a):
    """
    This function just sums up the skills in a list.
    :param a: List. List of skills that need to be added up
    :return: Sum of skill prices.
    """
    current_skill_sum = 0
    for i in a:
        # If we somehow let in an invalid skill, we have to return.
        if skill_prices_dict[i] < 0:
            current_skill_sum = -999
            return current_skill_sum

        current_skill_sum += skill_prices_dict[i]
    return current_skill_sum


def get_google_sheet(spreadsheet_id, out_dir, out_file):
    """
    This function acquires a Google Sheet and turns it into a .csv file that we can more easily interpret and edit in Python.
    :param spreadsheet_id: The part of the Google Sheet's link that corresponds to the unique spreadsheet ID.
    :param out_dir: Directory this function will output the csv file to.
    :param out_file: The name of the csv file that will be outputted.
    :return: None
    """
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(out_dir, out_file)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print('CSV file saved to: {}'.format(filepath))
    else:
        print(f'Error downloading Google Sheet: {response.status_code}')
        sys.exit(1)


def reformat_skills(skills_str):
    '''
    The way the Google form is set up, the skills for each route are sent in together with skill prices. This just fixes that.
    :param skills_str: String. The unedited Skill list string.
    :return: A list with Corrin's skills in a more digestible and editable format.
    '''
    # Split the string on commas and strip unwanted characters
    skills_list = [skill.split(' (')[0].strip() for skill in skills_str.split(',')]
    while len(skills_list) < 5:
        skills_list.append('None')
    return skills_list


# For your Corrinquest, you'll want to replace the first string with the part of your share url that's after the /d/
# and before the /edit?..etc. Right now, it's using my data.
get_google_sheet(edit_this.SPREADSHEET_ID, "./", "data.csv")

# If you're customizing this file to your needs, just ignore this segment.
data = pd.read_csv("data.csv")
columns_to_reformat = [edit_this.SKILLS_BR, edit_this.SKILLS_CQ, edit_this.SKILLS_REV]
for column in columns_to_reformat:
    data[column] = data[column].apply(reformat_skills)

# This step validates all the Corrins' information If any element is invalid, that Corrin will be dropped from the dataframe.
# The BR, CQ and REV variables represent IF YOU'RE PLAYING THAT ROUTE OR NOT. "budget" IS THE SKILL BUDGET ACROSS ALL THREE ROUTES.
validate_corrin(data, edit_this.PROMOTION_MODE, edit_this.PLAYING_BIRTHRIGHT, edit_this.PLAYING_CONQUEST,
                edit_this.PLAYING_REVELATION, edit_this.BUDGET)

# Create our Corrin objects and populate all the data.
corrin_list = []
for index, row in data.iterrows():
    corrin_list.append(Corrin.Corrin(row))

# Create a nested set of folders that we can use to store the .fe14unit files more easily.
for corrin in corrin_list:
    c_name = corrin.name
    c_name = make_valid_dir_name(c_name)
    # Make a main directory for this Corrin's fe14unit files.
    os.makedirs(c_name, exist_ok=True)
    # Make 3 subfolders, one for each route.
    subfolders = [f"{c_name}_B", f"{c_name}_C", f"{c_name}_R"]
    for subfolder in subfolders:
        os.makedirs(os.path.join(c_name, subfolder), exist_ok=True)

level_values = [7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 2, 4, 6, 8, 10, 12, 14, 16, 18]
level_values_dlc = [7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
internal_level_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20, 20, 20, 20]
internal_level_values_dlc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tracker = float(0)
tracker_max = float(len(corrin_list))

for corrin in corrin_list:
    c_name = corrin.name
    c_name = make_valid_dir_name(c_name)
    for i in range(0, 3):
        for j in range(0, 21):

            # Step 1: Figure out the file name that we're going to output to.
            if i == 0:
                file_name = f"./{c_name}/{c_name}_B/{c_name}_B_{j + 7}.fe14unit"
            elif i == 1:
                file_name = f"./{c_name}/{c_name}_C/{c_name}_C_{j + 7}.fe14unit"
            else:
                file_name = f"./{c_name}/{c_name}_R/{c_name}_R_{j + 7}.fe14unit"

            # Step 2: Copy Crash to create a file with the correct file name but none of the correct data yet.
            c_e.copy_file("Crash.fe14unit", file_name)

            # Step 3: Edit the fe14unit file's route-universal data except gender to have all the right information
            dlc_amiibo = ((cs.classes[cs.classes["Name"] == corrin.promotion[i]])["Tier"] == 3)

            # Get the internal/level values for the current point in the game
            if bool(np.array(dlc_amiibo)[0]):
                l_val = level_values_dlc[j]
                il_val = internal_level_values_dlc[j]
            else:
                l_val = level_values[j]
                il_val = internal_level_values[j]

            # Get the class ID for the current point in the game
            if j < 12:
                c_val = (cs.classes[cs.classes["Name"] == corrin.base_class[i]])["ID"]
            else:
                c_val = (cs.classes[cs.classes["Name"] == corrin.promotion[i]])["ID"]

            c_e.edit_corrin(file_name, new_name=corrin.name, body=corrin.body, face=corrin.face, hairstyle=corrin.style,
                            decoration=corrin.decoration, detail=corrin.detail,voice=corrin.voice,
                            hair_color=[corrin.hair_color[0],corrin.hair_color[1], corrin.hair_color[2]],
                            talent=corrin.base_class[i], gender=corrin.gender,boon=corrin.boon[i],bane=corrin.bane[i],
                            learned_skills=skills.calculate_skills_value(corrin.skills[i]),
                            sks=corrin.skills[i],stats=corrin.stats[i][j], level=l_val, internal_level=il_val,
                            new_class_hex_num=c_val)

            # c_e.edit_name(file_name, corrin.name)
            # c_e.edit_body(file_name, corrin.body)
            # c_e.edit_face(file_name, corrin.face)
            # c_e.edit_hairstyle(file_name, corrin.style)
            # c_e.edit_female_decoration(file_name, corrin.decoration)
            # c_e.edit_facial_detail(file_name, corrin.detail)
            # c_e.edit_voice(file_name, corrin.voice)
            # c_e.edit_hair_color(file_name, corrin.hair_color[0], corrin.hair_color[1], corrin.hair_color[2])
            #
            # # Step 4: Edit the different fe14unit files correctly with the route-specific information
            # c_e.edit_talent_gender(file_name, corrin.base_class[i], corrin.gender)
            # c_e.edit_boon_bane(file_name, corrin.boon[i], corrin.bane[i])
            # c_e.edit_learned_skills(file_name, skills.calculate_skills_value(corrin.skills[i]))
            # for k in range(0, 5):
            #     if corrin.skills[i][k] != "None":
            #         c_e.edit_skill(file_name, corrin.skills[i][k], k + 1)
            # c_e.edit_stats(file_name, corrin.stats[i][j])
            #
            #
            # if j < 12:
            #     c_e.edit_class(file_name, (cs.classes[cs.classes["Name"] == corrin.base_class[i]])["ID"])
            # else:
            #     c_e.edit_class(file_name, (cs.classes[cs.classes["Name"] == corrin.promotion[i]])["ID"])


    tracker = tracker + 1
    print(f"Corrin {corrin.name} has been completed. {round((tracker / tracker_max) * 100, 2)}% complete.")

error_file.close()
