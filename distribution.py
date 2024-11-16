# import pandas as pd
# import numpy as np
# import classes as cs
#
# distribution = pd.read_excel("weapon_distribution.xlsx")
#
# def calculate_weapon_sheet(base_class, promoted_class):
#
#     weapon_sheet = np.zeros(shape=(21,5))
#
#     up_weapon_types = cs.classes[cs.classes["Name"] == base_class]["Weapon Types"].tolist()[0]
#     p_weapon_types = cs.classes[cs.classes["Name"] == promoted_class]["Weapon Types"].tolist()[0]
#     primary = np.setdiff1d(up_weapon_types, p_weapon_types)
#     secondary = np.setdiff1d(p_weapon_types, up_weapon_types)
#
#     base_class_route = cs.classes[cs.classes["Name"] == base_class]["Route"]
#     p_class_route = cs.classes[cs.classes["Name"] == promoted_class]["Route"]
#
#     # IF you have more than one weapon type unpromoted
#     if len(up_weapon_types) > 1:
#         if base_class == "Cavalier": # Primary lance secondary sword or sword/axe
#             # Chapter 7-14 Double iron, Chapter 15-18 Steel lance iron sword, Chapter 19-21 Steel Lance iron sword (+ axe), Chapter 22-E Silver Lance Steel Sword (+axe)
#             weapon_sheet[:8] = [52, 2, 0, 0, 0]
#             weapon_sheet[8:12] = [53, 2, 0, 0, 0]
#             pass
#         elif base_class == "Nohr Prince(ss)": # Primary sword secondary staff/tome secondary stone
#             # Chapter 7-14 Double iron, Chapter 15-18 Steel lance iron sword, Chapter 19-21 Steel Lance iron sword (+ axe), Chapter 22-E Silver Lance Steel Sword (+axe)
#             weapon_sheet[:8] = [22, 262, 0, 0, 0]
#             weapon_sheet[8:12] = [23, 262, 0, 0, 0]
#             pass
#     else:
#         for i in range(7, 19): # Iterate through each chapter
#             if base_class == "Kitsune" or base_class == "Wolfskin":
#                 weapon_sheet[:7] = [264, 0, 0, 0, 0]
#                 weapon_sheet[7:12] = [264, 265, 0, 0, 0]
#             weapon_sheet[:8] = [distribution[distribution["Route"] == base_class_route], 0, 0, 0, 0]
#
#
#
#
#
#     return weapon_sheet