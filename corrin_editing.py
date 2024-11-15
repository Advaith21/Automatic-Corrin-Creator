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