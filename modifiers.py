# This file contains Corrin's base growths and his/her boon/bane modifiers for bases and growths.
# It also contains a function that allows one to Calculate a Corrin's stats
import numpy as np
import classes as cs


def calculate_stats(base_class, promoted_class, boon, bane):
    """
    This function takes in a base class, promoted class, boon and bane of a Corrin
    and calculates their stat sheet for every chapter in the game post Branch of Fate.
    :param base_class: String. The unpromoted class that Corrin is in.
    :param promoted_class: String. The class Corrin will promote into.
    :param boon: String. The boon of the Corrin.
    :param bane: String. The bane of the Corrin.
    :return: A 8x21 NumPy array where each row is the stats of Corrin at a chapter recruit, starting at Ch 7.
    """
    stats_order = {
        'HP': 0,
        'Strength': 1,
        'Magic': 2,
        'Skill': 3,
        'Speed': 4,
        'Luck': 5,
        'Defense': 6,
        'Resistance': 7
    }
    boon_index = stats_order[boon]
    bane_index = stats_order[bane]

    # The .fe14unit file does not include Corrin's personal bases and class bases, so we start with zero.
    up_corrin_bases = [0, 0, 0, 0, 0, 0, 0, 0]

    # CALCULATING CORRIN GROWTHS
    # Calculate Corrin's growths in both their unpromoted and promoted class.
    up_class_growths = cs.classes[cs.classes['Name'] == base_class]['Growths'].tolist()[0]
    p_class_growths = cs.classes[cs.classes['Name'] == promoted_class]['Growths'].tolist()[0]
    # Adds together all modifiers to get Corrin's growths.
    up_corrin_growths = [int(a + b + c + d) for a, b, c, d in
                         zip(up_class_growths, growths, grBoonMod[boon_index].tolist(), grBaneMod[bane_index].tolist())]
    p_corrin_growths = [int(a + b + c + d) for a, b, c, d in
                        zip(p_class_growths, growths, grBoonMod[boon_index].tolist(), grBaneMod[bane_index].tolist())]

    # CALCULATING CORRIN CAPS
    # Calculating the overall cap modifier is thankfully not that big of a deal, so we can do it in just one line. After
    # that, calculate the caps of the unpromoted and promoted classes.
    corrin_cap_mod = [int(a + b) for a, b in zip(capBoonMod[boon_index].tolist(), capBaneMod[bane_index].tolist())]
    up_corrin_caps = [int(a + b) for a, b in
                      zip(corrin_cap_mod, cs.classes[cs.classes['Name'] == base_class]['Caps'].tolist()[0])]
    p_corrin_caps = [int(a + b) for a, b in
                     zip(corrin_cap_mod, cs.classes[cs.classes['Name'] == promoted_class]['Caps'].tolist()[0])]

    # This stat sheet will hold the stats for Corrin for all points in the game. Each row is a different chapter,
    # starting at Ch 7 ending at Ch 27.
    stat_sheet = np.zeros(shape=(21, 8))

    # CALCULATING UNPROMOTED CORRIN STATS
    # Corrin's stats at level 7 chapter 7 recruit.
    stat_sheet[0] = [(0.06 * a) + b for a, b in zip(up_corrin_growths, up_corrin_bases)]
    # This array starts off at going from ch 7 to 8 and then until ch 18 when Corrin hits lvl 20, keeps track of how
    # many levels Corrin gains each chapter.
    level_amt = [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2]
    # Calculate Corrin's stats until and including lvl 20.
    for i in range(0, len(level_amt)):
        stat_sheet[i + 1] = [(level_amt[i] * 0.01 * a) + b for a, b in zip(up_corrin_growths, stat_sheet[i])]
        for j in range(0, 8):  # Make sure stats are properly capped
            if stat_sheet[i + 1][j] > up_corrin_caps[j]:
                stat_sheet[i + 1][j] = up_corrin_caps[j]

    # PROMOTING CORRIN AND CALCULATING PROMOTED CORRIN STATS
    # Calculating ch 19 at 20/2 promoted.
    stat_sheet[12] = [(0.01 * a) + b for a, b in zip(p_corrin_growths, stat_sheet[11])]
    level_amt_2 = [2, 2, 2, 2, 2, 2, 2, 2]
    # Calculate Corrin's stats from promotion till endgame
    for i in range(0, len(level_amt_2)):
        stat_sheet[i + 13] = [(level_amt_2[i] * 0.01 * a) + b for a, b in zip(p_corrin_growths, stat_sheet[i + 12])]
        for j in range(0, 8):  # Make sure stats are properly capped
            if stat_sheet[i + 13][j] > p_corrin_caps[j]:
                stat_sheet[i + 13][j] = p_corrin_caps[j]

    return stat_sheet


growths = [45, 45, 30, 40, 45, 45, 35, 25]  # Non-modified growths for all Corrins
bases = [2, 0, 1, 3, 1, 3, 1, 0]

# Base Modifier Arrays
baseBoonMod = [3, 2, 3, 3, 2, 3, 1, 1]
baseBaneMod = [-2, -1, -2, -2, -1, -2, -1, -1]

# Growth Modifier Arrays
grBoonMod = np.array([
    [15, 0, 0, 0, 0, 0, 5, 5],
    [0, 15, 0, 5, 0, 0, 5, 0],
    [0, 0, 20, 0, 5, 0, 0, 5],
    [0, 5, 0, 25, 0, 0, 5, 0],
    [0, 0, 0, 5, 15, 5, 0, 0],
    [0, 5, 5, 0, 0, 25, 0, 0],
    [0, 0, 0, 0, 0, 5, 10, 5],
    [0, 0, 5, 0, 5, 0, 0, 10],
])
grBaneMod = np.array([
    [-10, 0, 0, 0, 0, 0, -5, -5],
    [0, -10, 0, -5, 0, 0, -5, 0],
    [0, 0, -15, 0, -5, 0, 0, -5],
    [0, -5, 0, -20, 0, 0, -5, 0],
    [0, 0, 0, -5, -10, -5, 0, 0],
    [0, -5, -5, 0, 0, -20, 0, 0],
    [0, 0, 0, 0, 0, -5, -10, -5],
    [0, 0, -5, 0, -5, 0, 0, -10],
])

# Cap modifier arrays
capBoonMod = np.array([
    [0, 1, 1, 0, 0, 2, 2, 2],
    [0, 4, 0, 2, 0, 0, 2, 0],
    [0, 0, 4, 0, 2, 0, 0, 2],
    [0, 2, 0, 4, 0, 0, 2, 0],
    [0, 0, 0, 2, 4, 2, 0, 0],
    [0, 2, 2, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 2, 4, 2],
    [0, 0, 2, 0, 2, 0, 0, 4],
])
capBaneMod = np.array([
    [0, -1, -1, 0, 0, -1, -1, -1],
    [0, -3, 0, -1, 0, 0, -1, 0],
    [0, 0, -3, 0, -1, 0, 0, -1],
    [0, -1, 0, -3, 0, 0, -1, 0],
    [0, 0, 0, -1, -3, -1, 0, 0],
    [0, -1, -1, 0, 0, -3, 0, 0],
    [0, 0, 0, 0, 0, -1, -3, -1],
    [0, 0, -1, 0, -1, 0, 0, -3],
])
