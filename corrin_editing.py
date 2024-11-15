import numpy as np
import skills


# This file houses all the functions that main.py uses to edit Corrin files.

def is_valid_hex_string(s):
    valid_chars = "0123456789abcdefABCDEF"
    return all(char in valid_chars for char in s)


def return_hex(f_name):
    """
    Simple helper function that returns the hex string of a file, so you can quickly see if it's changed and how.
    :param f_name: Name of file from which to output
    :return: N/A
    """
    with open(f_name, 'rb') as f:
        b = f.read()
        h = b.hex()
        f.seek(0)
    return h


def reverse_bits(hex_str):
    s = ""
    if len(hex_str) < 38:
        d = 38 - len(hex_str)
        for i in range(0, d):
            s += '0'
        s = s + hex_str
    else:
        s = hex_str
    bytes_list = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    for i in range(0, 19):
        bytes_list[18 - i] = s[2 * i:(2 * i) + 2]
    result = ""
    for i in range(0, 19):
        result += bytes_list[i]
    return result

def edit_hex_in_string(hex_data, index, new_value):
    if len(new_value) == 1:
        new_value = '0' + new_value
    return hex_data[:index] + new_value + hex_data[index + 2:]

def edit_hair_color_in_string(hex_data, r, g, b, r_start, g_start, b_start):
    hex_data = edit_hex_in_string(hex_data, r_start, r)
    hex_data = edit_hex_in_string(hex_data, g_start, g)
    hex_data = edit_hex_in_string(hex_data, b_start, b)
    return hex_data

# DO NOT FUCK WITH THIS IT'S USED TO READ THE FE14UNIT FILE
NAME_START_INDEX = 604
BOON_INDEX = 656
BANE_INDEX = 658
TALENT_INDEX = 660
GENDER_INDEX = 664
BODY_INDEX = 666
FACE_INDEX = 668
HAIRSTYLE_INDEX = 670
HAIR_COLOR_R = 422
HAIR_COLOR_R_2 = 672
HAIR_COLOR_G = 424
HAIR_COLOR_G_2 = 674
HAIR_COLOR_B = 426
HAIR_COLOR_B_2 = 676
FEMALE_DECORATION_INDEX = 680
FACIAL_DETAIL_INDEX = 682
VOICE_INDEX = 684
BIRTHDAY_MONTH_INDEX = 686
BIRTHDAY_DATE_INDEX = 688
CLASS_INDEX = 30

# SAME HERE BUT THIS IS DEMARCATED FOR STAT LOCATIONS
HP_INDEX = 62
STR_INDEX = 64
MAG_INDEX = 66  # No, not A Certain Magical Index
SKL_INDEX = 68
SPD_INDEX = 70
LCK_INDEX = 72
DEF_INDEX = 74
RES_INDEX = 76

LEVEL_INDEX = 18
INTERNAL_LEVEL_INDEX = 22

# SAME HERE BUT THIS IS DEMARCATED FOR SKILLS
SKILL_1_INDEX = 178
SKILL_2_INDEX = 182
SKILL_3_INDEX = 186
SKILL_4_INDEX = 190
SKILL_5_INDEX = 194
LEARNED_SKILLS_INDEX = 524


def copy_file(source_file, destination_file):
    """
    Copies a file to the target destination under the target name.
    :param source_file: Name of the source file
    :param destination_file: Target path for destination file
    :return: None
    """
    with open(source_file, 'rb') as src:
        with open(destination_file, 'wb') as dst:
            dst.write(src.read())

def edit_corrin(f_name, level, sks, internal_level, stats, new_class_hex_num, new_name, boon, bane, talent, gender, body, face, hairstyle, hair_color, decoration, detail, voice, learned_skills):
    with open(f_name, 'rb+') as f:
        byte_data = f.read()
        hex_data = byte_data.hex()

        # Level and internal level
        hex_data = edit_hex_in_string(hex_data, LEVEL_INDEX, hex(level)[2:])
        hex_data = edit_hex_in_string(hex_data, INTERNAL_LEVEL_INDEX, hex(internal_level)[2:])

        # Stats
        indices = [HP_INDEX, STR_INDEX, MAG_INDEX, SKL_INDEX, SPD_INDEX, LCK_INDEX, DEF_INDEX, RES_INDEX]
        for i, stat in enumerate(stats):
            hex_data = edit_hex_in_string(hex_data, indices[i], hex(int(stat))[2:])

        # Class
        hex_data = edit_hex_in_string(hex_data, CLASS_INDEX, new_class_hex_num)

        # Name
        if len(new_name) > 8:
            raise ValueError("ERROR. Name too long.")
        cur = NAME_START_INDEX
        for char in new_name:
            hex_data = edit_hex_in_string(hex_data, cur, hex(ord(char))[2:])
            cur += 4

        # Boon and Bane
        stats = {'HP': '1', 'Strength': '2', 'Magic': '3', 'Skill': '4', 'Speed': '5', 'Luck': '6', 'Defense': '7', 'Resistance': '8'}
        hex_data = edit_hex_in_string(hex_data, BOON_INDEX, stats[boon])
        hex_data = edit_hex_in_string(hex_data, BANE_INDEX, stats[bane])

        # Talent and Gender
        genders = {'Male': '00', 'Female': '01'}
        male_classes = {'Nohr Prince(ss)': '08', 'Cavalier': '09', 'Knight': '0d', 'Fighter': '13', 'Mercenary': '17', 'Outlaw': '1b', 'Samurai': '21', 'Oni Savage': '27', 'Spear Fighter': '2d', 'Diviner': '31', 'Monk': '35', 'Sky Knight': '3b', 'Archer': '3f', 'Wyvern Rider': '45', 'Ninja': '4b', 'Apothecary': '4f', 'Dark Mage': '55', 'Troubadour': '5c', 'Wolfskin': '5f', 'Kitsune': '63', 'Villager': '68'}
        female_classes = {'Nohr Prince(ss)': '08', 'Cavalier': '0a', 'Knight': '0e', 'Fighter': '14', 'Mercenary': '18', 'Outlaw': '1c', 'Samurai': '22', 'Oni Savage': '28', 'Spear Fighter': '2e', 'Diviner': '32', 'Shrine Maiden': '36', 'Sky Knight': '3c', 'Archer': '40', 'Wyvern Rider': '46', 'Ninja': '4c', 'Apothecary': '50', 'Dark Mage': '56', 'Troubadour': '5c', 'Wolfskin': '60', 'Kitsune': '64', 'Villager': '69'}
        hex_data = edit_hex_in_string(hex_data, GENDER_INDEX, genders[gender])
        if gender == 'Male':
            hex_data = edit_hex_in_string(hex_data, TALENT_INDEX, male_classes[talent])
        else:
            hex_data = edit_hex_in_string(hex_data, TALENT_INDEX, female_classes[talent])

        # Body, Face, Hairstyle
        hex_data = edit_hex_in_string(hex_data, BODY_INDEX, hex(body - 1)[2:])
        hex_data = edit_hex_in_string(hex_data, FACE_INDEX, hex(face - 1)[2:])
        hex_data = edit_hex_in_string(hex_data, HAIRSTYLE_INDEX, hex(hairstyle - 1)[2:])

        # Hair Color
        hex_data = edit_hair_color_in_string(hex_data, hair_color[0], hair_color[1], hair_color[2], HAIR_COLOR_R, HAIR_COLOR_G, HAIR_COLOR_B)

        # Female Decoration, Facial Detail, Voice
        hex_data = edit_hex_in_string(hex_data, FEMALE_DECORATION_INDEX, hex(decoration)[2:])
        hex_data = edit_hex_in_string(hex_data, FACIAL_DETAIL_INDEX, hex(detail)[2:])
        hex_data = edit_hex_in_string(hex_data, VOICE_INDEX, hex(voice - 1)[2:])

        # Skills
        skill_indices = [SKILL_1_INDEX, SKILL_2_INDEX, SKILL_3_INDEX, SKILL_4_INDEX, SKILL_5_INDEX]
        for i in range(0,5):
            s_name = sks[i]
            if s_name != "None":
                s_hex = skills.skills_dict[s_name]  # Assuming skills_dict from skills.py is available
                hex_data = edit_hex_in_string(hex_data, skill_indices[i], s_hex)

        # Learned Skills
        r_hex = reverse_bits(learned_skills)
        hex_data = hex_data[:LEARNED_SKILLS_INDEX] + r_hex + hex_data[LEARNED_SKILLS_INDEX + len(r_hex):]

        f.seek(0)
        f.write(bytes.fromhex(hex_data))

# def edit_level(f_name, level, internal_level):
#     if level < 16:
#         level = '0' + str(hex(level)[2:])
#     else:
#         level = str(hex(level)[2:])
#     if internal_level < 16:
#         internal_level = '0' + str(hex(internal_level)[2:])
#     else:
#         internal_level = str(hex(internal_level)[2:])
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:LEVEL_INDEX] + level + hex_data[LEVEL_INDEX + 2:]
#         hex_data = hex_data[:INTERNAL_LEVEL_INDEX] + internal_level + hex_data[INTERNAL_LEVEL_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#         return
#
#
# # NOTE: CORRIN PERSONAL BASES AND CLASS BASES ARE NOT COUNTED TOWARDS THIS VALUE
# def edit_stats(f_name, stats):
#     """
#     This edits corrin's stats.
#     :param f_name: Name of file to which it should output
#     :param stats: 8-value String array with stats
#     :return: None
#     """
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         for i in range(0, len(stats)):
#             stats[i] = str(hex(int(stats[i]))[2:])
#             if len(stats[i]) == 1:
#                 stats[i] = '0' + stats[i]
#         hex_data = hex_data[:HP_INDEX] + stats[0] + hex_data[HP_INDEX + 2:]
#         hex_data = hex_data[:STR_INDEX] + stats[1] + hex_data[STR_INDEX + 2:]
#         hex_data = hex_data[:MAG_INDEX] + stats[2] + hex_data[MAG_INDEX + 2:]
#         hex_data = hex_data[:SKL_INDEX] + stats[3] + hex_data[SKL_INDEX + 2:]
#         hex_data = hex_data[:SPD_INDEX] + stats[4] + hex_data[SPD_INDEX + 2:]
#         hex_data = hex_data[:LCK_INDEX] + stats[5] + hex_data[LCK_INDEX + 2:]
#         hex_data = hex_data[:DEF_INDEX] + stats[6] + hex_data[DEF_INDEX + 2:]
#         hex_data = hex_data[:RES_INDEX] + stats[7] + hex_data[RES_INDEX + 2:]
#
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_class(f_name, new_class_hex_num):
#     addon = np.array(new_class_hex_num)[0]
#     if isinstance(addon, float):
#         print(addon)
#     if len(addon) == 1:
#         addon = '0' + addon
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:CLASS_INDEX] + addon + hex_data[CLASS_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_name(f_name, new_name):
#     if len(new_name) > 8:
#         print("ERROR. Name too long.")
#         exit(1)
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         cur = NAME_START_INDEX
#         for i in range(0, len(new_name)):
#             hex_data = hex_data[:cur] + hex(ord(new_name[i]))[2:] + hex_data[cur + 2:]
#             cur += 4
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# # Takes in boon and banes AS STRINGS NO SHORTENING OF THE STATS EITHER and edits the Corrin's data to reflect this.
# def edit_boon_bane(f_name, boon, bane):
#     stats = {'HP': '1', 'Strength': '2', 'Magic': '3', 'Skill': '4', 'Speed': '5', 'Luck': '6', 'Defense': '7',
#              'Resistance': '8'}
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:BOON_INDEX] + '0' + hex(int(stats[boon]))[2:] + hex_data[BOON_INDEX + 2:]
#         hex_data = hex_data[:BANE_INDEX] + '0' + hex(int(stats[bane]))[2:] + hex_data[BANE_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# # We have to edit the talent and the gender at the same time because we need to make sure that female Corrins are
# # linked to female classes and male Corrins are linked to male classes.
# def edit_talent_gender(f_name, talent, gender):
#     with open(f_name, 'rb+') as f:
#
#         genders = {'Male': '00', 'Female': '01'}
#
#         male_classes = {'Nohr Prince(ss)': '08', 'Cavalier': '09', 'Knight': '0d', 'Fighter': '13', 'Mercenary': '17',
#                         'Outlaw': '1b',
#                         'Samurai': '21',
#                         'Oni Savage': '27', 'Spear Fighter': '2d', 'Diviner': '31', 'Monk': '35',
#                         'Sky Knight': '3b',
#                         'Archer': '3f', 'Wyvern Rider': '45', 'Ninja': '4b', 'Apothecary': '4f', 'Dark Mage': '55',
#                         'Troubadour': '5c', 'Wolfskin': '5f', 'Kitsune': '63', 'Villager': '68'}
#
#         female_classes = {'Nohr Prince(ss)': '08', 'Cavalier': '0a', 'Knight': '0e', 'Fighter': '14', 'Mercenary': '18',
#                           'Outlaw': '1c',
#                           'Samurai': '22', 'Oni Savage': '28', 'Spear Fighter': '2e', 'Diviner': '32',
#                           'Shrine Maiden': '36', 'Sky Knight': '3c', 'Archer': '40', 'Wyvern Rider': '46',
#                           'Ninja': '4c', 'Apothecary': '50', 'Dark Mage': '56', 'Troubadour': '5c', 'Wolfskin': '60',
#                           'Kitsune': '64', 'Villager': '69'}
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:GENDER_INDEX] + genders[gender] + hex_data[GENDER_INDEX + 2:]
#         if gender == 'Male':
#             hex_data = hex_data[:TALENT_INDEX] + male_classes[talent] + hex_data[TALENT_INDEX + 2:]
#         elif gender == 'Female':
#             hex_data = hex_data[:TALENT_INDEX] + female_classes[talent] + hex_data[TALENT_INDEX + 2:]
#
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# # Body type is the short/tall decision
# def edit_body(f_name, body):
#     with open(f_name, 'rb+') as f:
#         body = body - 1
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:BODY_INDEX] + '0' + str(hex(body)[2:]) + hex_data[BODY_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_face(f_name, face):
#     with open(f_name, 'rb+') as f:
#         face = face - 1
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:FACE_INDEX] + '0' + str(hex(face)[2:]) + hex_data[FACE_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_hairstyle(f_name, hairstyle):
#     with open(f_name, 'rb+') as f:
#         hairstyle = hairstyle - 1
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         # print(hex_data)
#         hex_data = hex_data[:HAIRSTYLE_INDEX] + '0' + str(hex(hairstyle)[2:]) + hex_data[HAIRSTYLE_INDEX + 2:]
#         # print(hex_data)
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_hair_color(f_name, r, g, b):
#     edit_hair_color_helper(f_name, r, g, b, HAIR_COLOR_R, HAIR_COLOR_G, HAIR_COLOR_B)
#
#
# def edit_hair_color_helper(f_name, r, g, b, r_start, g_start, b_start):
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:r_start] + r + hex_data[r_start + 2:]
#         hex_data = hex_data[:g_start] + g + hex_data[g_start + 2:]
#         hex_data = hex_data[:b_start] + b + hex_data[b_start + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_female_decoration(f_name, decoration):
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:FEMALE_DECORATION_INDEX] + '0' + str(hex(decoration)[2:]) + hex_data[
#                                                                                          FEMALE_DECORATION_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_facial_detail(f_name, detail):
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:FACIAL_DETAIL_INDEX] + '0' + str(hex(detail)[2:]) + hex_data[FACIAL_DETAIL_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_voice(f_name, voice):
#     with open(f_name, 'rb+') as f:
#         voice = voice - 1
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:VOICE_INDEX] + '0' + str(hex(voice)[2:]) + hex_data[VOICE_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
#
# def edit_birthday(f_name, day, month):
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:BIRTHDAY_DATE_INDEX] + hex(ord(day))[2:] + hex_data[BIRTHDAY_DATE_INDEX + 2:]
#         hex_data = hex_data[:BIRTHDAY_MONTH_INDEX] + hex(ord(month))[2:] + hex_data[BIRTHDAY_MONTH_INDEX + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
#
# def edit_learned_skills(f_name, hex_string):
#     r_hex = reverse_bits(hex_string)
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:LEARNED_SKILLS_INDEX] + r_hex + hex_data[LEARNED_SKILLS_INDEX + len(r_hex):]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#
#     return
#
#
# def edit_skill(f_name, s_name, skill_slot):
#     """
#     Edit the skill hex value for the given Corrin's corresponding skill slot.
#     :param f_name: String. File name for the .fe14unit file that will be edited
#     :param s_name: String. Name of the skill that will be added to this Corrin.
#     :param skill_slot: Int. Skill slot that the skill will be added to.
#     :return: None
#     """
#     if s_name == "None":
#         return
#
#     # Define the indices for each skill slot
#     skill_indices = {
#         1: SKILL_1_INDEX,
#         2: SKILL_2_INDEX,
#         3: SKILL_3_INDEX,
#         4: SKILL_4_INDEX,
#         5: SKILL_5_INDEX
#     }
#
#     # Get the index for the given skill number
#     skill_index = skill_indices.get(skill_slot)
#
#     # You can only assign skills to skill slots 1-5.
#     if skill_index is None:
#         raise ValueError("Invalid skill number. Must be between 1 and 5.")
#
#     # Convert the skill to hex using the dictionary in skills.py
#     s_hex = skills.skills_dict[s_name]
#
#     # Open the file and edit it.
#     with open(f_name, 'rb+') as f:
#         byte_data = f.read()
#         hex_data = byte_data.hex()
#         hex_data = hex_data[:skill_index] + s_hex + hex_data[skill_index + 2:]
#         f.seek(0)
#         f.write(bytes.fromhex(hex_data))
#     return
