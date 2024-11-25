import pandas as pd
import numpy as np
import classes as cs

# What I need to do:
# Step 1: Get a Corrin's base class and promoted class.
# Step 2: Create a blank weapon sheet with their weapon ranks for each chapter ( 21x8 )
# Step 3: For the first 12 rows (before promotion)
#   Use the protocol to raise from D to their class's capped weapon rank at the 12th row and use it to fill in the first 12 rows
# Step 4: For the last 8 rows (post-promotion)
#   Look at the class's promoted weapon types and their current weapon rank and raise it to the cap accordingly.
#
# E-B, E-A, D-C, D-B, C-B, B-B, B-A, B-S
# The rest can be implemented later.
# E-B/E-A: New weapon type to B/A cap
# D-C: Villager
# D-B: All non-villager classes
# C-B: Villager lance rank post-promo
# B-B: Weapon Type that stays capped after promotion
# B-A: Weapon Type that goes from B-A cap post promo
# B-S: S rank classes

gain_formulas = pd.read_excel("gain_formulas.xlsx")

weapon_type_dict = {
    "Sword": 0,
    "Lance": 1,
    "Axe": 2,
    "Hidden": 3,
    "Bow": 4,
    "Tome": 5,
    "Staff": 6,
    "Stone": 7
}

def calculate_weapon_sheet(base_class, promoted_class):
    """
    This function takes a Corrin's base class and promoted class and returns a table that provides their weapon ranks
    at each recruit so that it can be edited into their unit data appropriately.
    :param base_class: Unpromtoed class of the Corrin. Has to be pre-validated.
    :param promoted_class: Class the Corrin will promote into. Has to be pre-validated.
    :return: NumPy array, 21x8 in size. Row = chapter recruited on, from 7-27, column = weapon type.
    """

    # Create the weapon sheet that we will edit and return.
    weapon_sheet = np.zeros(shape=(21, 8))

    # Obtain the Corrin's base class weapon types and promoted class weapon types to use later.
    up_weapon_types = cs.classes[cs.classes["Name"] == base_class]["Weapon Types"].tolist()[0]
    p_weapon_types = cs.classes[cs.classes["Name"] == promoted_class]["Weapon Types"].tolist()[0]

    # Go through the class's unpromoted weapon types
    for i in range(0, len(up_weapon_types)):

        # Obtain the name and cap of the current weapon type.
        type = up_weapon_types[i]
        cap = cs.classes[cs.classes["Name"] == base_class][type].tolist()[0]

        # Edit the first 12 rows of the weapon sheet to properly level weapon rank till promotion
        if cap == "C":
            weapon_sheet[:, weapon_type_dict[type]][0:12] = gain_formulas["D-C"][0:12]
        else:
            weapon_sheet[:, weapon_type_dict[type]][0:12] = gain_formulas["D-B"][0:12]

    # Go through the class's promoted weapon types
    for i in range(0, len(p_weapon_types)):

        # Obtain the name, unpromoted cap and promoted cap of the current weapon type.
        type = p_weapon_types[i]
        up_cap = cs.classes[cs.classes["Name"] == base_class][type].tolist()[0]
        p_cap = cs.classes[cs.classes["Name"] == promoted_class][type].tolist()[0]

        # Figure out the unpromoted and promoted weapon types and handle the cases properly, editing the sheet.
        if up_cap == "E":
            if p_cap == "B":
                weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["E-B"][12:]
            else:
                weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["E-A"][12:]
        elif up_cap == "C":
            weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["C-B"][12:]
        else:
            if p_cap == "B":
                weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["B-B"][12:]
            elif p_cap == "A":
                weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["B-A"][12:]
            else:
                weapon_sheet[:, weapon_type_dict[type]][12:] = gain_formulas["B-S"][12:]

    # Finally, return the weapon sheet.
    return weapon_sheet