import numpy as np
import pandas as pd
import classes as cs
import skills
from CorrinValidator import CorrinValidator
import os
import requests
import sys
import corrin_editing as c_e
import Corrin
import edit_this
error_file = open("error.txt", "w")
import openpyxl

def create_corrin_directories(c_list):
    n_count = {}  # Dictionary to keep track of the count for each name

    for c in c_list:
        c_n = c.name
        if c_n not in n_count:
            n_count[c_n] = 1
        else:
            n_count[c_n] += 1

        u_name = f"{c_n}_{n_count[c_n]}"
        u_name = make_valid_dir_name(u_name)  # Ensure valid directory name

        # Make a main directory for this Corrin's fe14unit files
        os.makedirs(u_name, exist_ok=True)

        # Make 3 subfolders, one for each route
        subfolders = [f"{u_name}_B", f"{u_name}_C", f"{u_name}_R"]
        for subfolder in subfolders:
            os.makedirs(os.path.join(u_name, subfolder), exist_ok=True)

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
    """
    The way the Google form is set up, the skills for each route are sent in together with skill prices. This just fixes that.
    :param skills_str: String. The unedited Skill list string.
    :return: A list with Corrin's skills in a more digestible and editable format.
    """
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
validator = CorrinValidator(df=data, mode=edit_this.PROMOTION_MODE, BR=edit_this.PLAYING_BIRTHRIGHT,
                            CQ=edit_this.PLAYING_CONQUEST, REV=edit_this.PLAYING_REVELATION, budget=edit_this.BUDGET)
validator.validate_all()

# Create our Corrin objects and populate all the data.
corrin_list = []
for index, row in data.iterrows():
    corrin_list.append(Corrin.Corrin(row))

# Create a nested set of folders that we can use to store the .fe14unit files more easily.
create_corrin_directories(corrin_list)

level_values = [7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 2, 4, 6, 8, 10, 12, 14, 16, 18]
level_values_dlc = [7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
internal_level_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20, 20, 20, 20]
internal_level_values_dlc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tracker = float(0)
tracker_max = float(len(corrin_list))

for corrin in corrin_list:
    # This holds how many times each name has been seen before.
    name_count = {}

    c_name = corrin.name
    if c_name not in name_count:
        name_count[c_name] = 1
    else:
        name_count[c_name] += 1

    unique_name = f"{c_name}_{name_count[c_name]}"
    unique_name = make_valid_dir_name(unique_name)  # Ensure valid directory name

    for i in range(0, 3):
        for j in range(0, 21):

            # Step 1: Figure out the file name that we're going to output to.
            if i == 0:
                file_name = f"./{unique_name}/{unique_name}_B/{unique_name}_B_{j + 7}.fe14unit"
            elif i == 1:
                file_name = f"./{unique_name}/{unique_name}_C/{unique_name}_C_{j + 7}.fe14unit"
            else:
                file_name = f"./{unique_name}/{unique_name}_R/{unique_name}_R_{j + 7}.fe14unit"

            # Step 2: Copy Crash to create a file with the correct file name but none of the correct data yet.
            c_e.copy_file("Crash.fe14unit", file_name)

            # Step 3: Edit the fe14unit file's route-universal data except gender to have all the right information
            dlc_amiibo = ((cs.classes[cs.classes["Name"] == corrin.promotion[i]])["Tier"] == 3)

            # Get the internal/level values for the current point in the game and get autolevelled skills

            pre_autolevel_skills = [i for i in corrin.skills[i]]

            if bool(np.array(dlc_amiibo)[0]):
                l_val = level_values_dlc[j]
                il_val = internal_level_values_dlc[j]
                # Add autolevelled skills onto the list.
                if l_val < 10:# Lvl 1 skill only
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0][0:1]
                elif 10 <= l_val <= 20:# Lvl 1/10 skills
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0]
                elif 20 <= l_val < 25:# Lvl 1/10 skills and DLC class lvl 1/10 skills
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0] + cs.classes[cs.classes["Name"] == corrin.promotion[i]]["Skills"].tolist()[0][0:2]
                elif 25 <= l_val < 35:# Lvl 1/10 skills of both classes and DLC class lvl 25 skill
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0] + cs.classes[cs.classes["Name"] == corrin.promotion[i]]["Skills"].tolist()[0][0:3]
                elif l_val >= 35:# All skills from both classes
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0] + cs.classes[cs.classes["Name"] == corrin.promotion[i]]["Skills"].tolist()[0]
            else:
                l_val = level_values[j]
                il_val = internal_level_values[j]
                # Add autolevelled skills onto the list.
                if l_val < 10 and il_val == 0:# Lvl 1 skill only
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0][0:1]
                elif l_val >= 10 and il_val == 0:# Unpromoted skills only
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0]
                elif 5 <= l_val < 15 and il_val == 20:# Unpromoted skills + lvl 5 promoted skill
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0] + cs.classes[cs.classes["Name"] == corrin.promotion[i]]["Skills"].tolist()[0][0:1]
                elif l_val >= 15 and il_val == 20:# All 4 skills.
                    pre_autolevel_skills = pre_autolevel_skills + cs.classes[cs.classes["Name"] == corrin.base_class[i]]["Skills"].tolist()[0] + cs.classes[cs.classes["Name"] == corrin.promotion[i]]["Skills"].tolist()[0]

                    # Get the class ID for the current point in the game, checking for gender
            if j < 12:
                c_val = (cs.classes[cs.classes["Name"] == corrin.base_class[i]])["ID"]
                if corrin.gender == "Female" and np.array(c_val)[0] not in ["36", "38", "5e", "67", "7a", "7b", "7c", "7d", "7e", "7f"]:
                    c_val = hex(int(np.array(c_val)[0], 16) + 1)[2:]
                else:
                    c_val = np.array(c_val)[0]

            else:
                c_val = (cs.classes[cs.classes["Name"] == corrin.promotion[i]])["ID"]
                if corrin.gender == "Female" and np.array(c_val)[0] not in ["36", "38", "5e", "67", "7a", "7b", "7c", "7d", "7e", "7f"]:
                    c_val = hex(int(np.array(c_val)[0], 16) + 1)[2:]
                else:
                    c_val = np.array(c_val)[0]


            c_e.edit_corrin(file_name, new_name=corrin.name, body=corrin.body, face=corrin.face, hairstyle=corrin.style,
                            decoration=corrin.decoration, detail=corrin.detail, voice=corrin.voice,
                            hair_color=[corrin.hair_color[0], corrin.hair_color[1], corrin.hair_color[2]],
                            talent=corrin.base_class[i], gender=corrin.gender, boon=corrin.boon[i], bane=corrin.bane[i],
                            learned_skills=skills.calculate_skills_value(pre_autolevel_skills),
                            sks=corrin.skills[i], stats=corrin.stats[i][j], level=l_val, internal_level=il_val,
                            new_class_hex_num=c_val, weapon_rank=corrin.weapon_ranks[i][j])

    tracker = tracker + 1
    print(f"Corrin {corrin.name} has been completed. {round((tracker / tracker_max) * 100, 2)}% complete.")

error_file.close()
