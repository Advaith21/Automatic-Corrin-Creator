import numpy as np
import pandas as pd
import ast

# This file contains every single valid class in Corrinquest and their bases, growths, caps, their tier and their name.
# NOTE: With the exception of Monk, Shrine Maiden, Priestess, and Great Master, ALL IDs here refer to the MALE CLASS!!
# If you want the female class ID, just add 1 to it. So, the class ID for M!General is F, the ID for F!General is 10.
classes = pd.read_excel("classes.xlsx")

# Convert relevant columns from string representation to numpy arrays or lists
classes['Bases'] = classes['Bases'].apply(lambda x: np.fromstring(x, sep=', '))
classes['Growths'] = classes['Growths'].apply(lambda x: np.fromstring(x, sep=', '))
classes['Caps'] = classes['Caps'].apply(lambda x: np.fromstring(x, sep=', '))
for index, row in classes.iterrows():
    classes.at[index, "Weapon Types"] = [s.strip() for s in row["Weapon Types"].split(",")]
    if pd.notnull(row["Promotions"]):
        classes.at[index, "Promotions"] = [s.strip() for s in row["Promotions"].split(",")]
    classes.at[index, "Skills"] = [s.strip() for s in row["Skills"].split(",")]

# NohrPrince = {
#     'Name': "Nohr Prince(ss)",
#     'Tier': 1,
#     'Bases': np.array([17, 7, 3, 4, 5, 2, 5, 2]),
#     'Growths': np.array([15, 15, 10, 10, 10, 10, 10, 5]),
#     'Caps': np.array([40, 23, 17, 19, 21, 22, 21, 19]),
#     'Weapon Types': np.array(["Sword", "Stone"]),
#     'Promotions': np.array(["Nohr Noble", "Hoshido Noble"]),
#     'ID': '3'
# }
#
# HoshidoNoble = {
#     'Name': "Hoshido Noble",
#     'Tier': 2,
#     'Bases': np.array([19, 10, 4, 5, 6, 4, 7, 3]),
#     'Growths': np.array([15, 15, 10, 10, 10, 10, 15, 0]),
#     'Caps': np.array([60, 34, 28, 29, 30, 33, 31, 28]),
#     'Weapon Types': np.array(["Sword", "Staff", "Stone"]),
#     'ID': '5'
# }
#
# NohrNoble = {
#     'Name': "Nohr Noble",
#     'Tier': 2,
#     'Bases': np.array([18, 8, 6, 4, 7, 2, 6, 6]),
#     'Growths': np.array([15, 10, 15, 5, 15, 5, 5, 15]),
#     'Caps': np.array([60, 32, 31, 28, 32, 27, 29, 32]),
#     'Weapon Types': np.array(["Sword", "Tome", "Stone"]),
#     'ID': '1'
# }
#
# Samurai = {
#     'Name': "Samurai",
#     'Tier': 1,
#     'Bases': np.array([17, 4, 0, 5, 8, 3, 3, 3]),
#     'Growths': np.array([10, 10, 0, 15, 20, 15, 0, 10]),
#     'Caps': np.array([40, 20, 16, 23, 25, 24, 18, 20]),
#     'Weapon Types': np.array(["Sword"]),
#     'Promotions': np.array(["Swordmaster", "Master of Arms"]),
#     'ID': '21'
# }
#
# Swordmaster = {
#     'Name': "Swordmaster",
#     'Tier': 2,
#     'Bases': np.array([18, 6, 2, 7, 11, 4, 5, 5]),
#     'Growths': np.array([10, 10, 5, 15, 20, 15, 0, 10]),
#     'Caps': np.array([55, 30, 28, 32, 35, 33, 27, 31]),
#     'Weapon Types': np.array(["Sword"]),
#     'ID': '1f'
# }
#
# MasterOfArms = {
#     'Name': "Master of Arms",
#     'Tier': 2,
#     'Bases': np.array([20, 8, 0, 6, 9, 3, 7, 3]),
#     'Growths': np.array([20, 15, 0, 10, 10, 10, 10, 0]),
#     'Caps': np.array([65, 33, 25, 30, 30, 31, 31, 28]),
#     'Weapon Types': np.array(["Sword", "Lance", "Axe"]),
#     'ID': '23'
# }
#
# Villager = {
#     'Name': "Villager",
#     'Tier': 1,
#     'Bases': np.array([17, 5, 0, 4, 5, 3, 4, 0]),
#     'Growths': np.array([10, 10, 0, 10, 10, 20, 10, 0]),
#     'Caps': np.array([35, 19, 15, 19, 19, 22, 18, 15]),
#     'Weapon Types': np.array(["Lance"]),
#     'Promotions': np.array(["Master of Arms", "Merchant"]),
#     'ID': '6f'
# }
#
# Merchant = {
#     'Name': "Merchant",
#     'Tier': 2,
#     'Bases': np.array([20, 8, 0, 6, 5, 4, 8, 5]),
#     'Growths': np.array([20, 20, 0, 10, 5, 15, 10, 5]),
#     'Caps': np.array([65, 33, 25, 29, 28, 32, 33, 30]),
#     'Weapon Types': np.array(["Lance", "Bow"]),
#     'ID': '51'
# }
#
# Apothecary = {
#     'Name': "Apothecary",
#     'Tier': 1,
#     'Bases': np.array([18, 6, 0, 4, 4, 2, 6, 2]),
#     'Growths': np.array([20, 20, 0, 10, 10, 5, 10, 5]),
#     'Caps': np.array([45, 24, 15, 19, 19, 21, 23, 20]),
#     'Weapon Types': np.array(["Bow"]),
#     'Promotions': np.array(["Merchant", "Mechanist"]),
#     'ID': '4f'
# }
#
# OniSavage = {
#     'Name': "Oni Savage",
#     'Tier': 1,
#     'Bases': np.array([18, 6, 1, 2, 5, 0, 7, 1]),
#     'Growths': np.array([20, 20, 10, 0, 10, 0, 20, 0]),
#     'Caps': np.array([45, 24, 19, 16, 20, 17, 23, 18]),
#     'Weapon Types': np.array(["Axe"]),
#     'Promotions': np.array(["Oni Chieftain", "Blacksmith"]),
#     'ID': '27'
# }
#
# OniChieftain = {
#     'Name': "Oni Chieftain",
#     'Tier': 2,
#     'Bases': np.array([19, 9, 5, 2, 7, 0, 10, 5]),
#     'Growths': np.array([10, 20, 15, 0, 10, 0, 20, 5]),
#     'Caps': np.array([60, 34, 28, 25, 30, 25, 36, 31]),
#     'Weapon Types': np.array(["Axe", "Tome"]),
#     'ID': '25'
# }
#
# Blacksmith = {
#     'Name': "Blacksmith",
#     'Tier': 2,
#     'Bases': np.array([21, 8, 0, 9, 8, 3, 8, 2]),
#     'Growths': np.array([20, 15, 0, 15, 10, 5, 15, 0]),
#     'Caps': np.array([65, 33, 25, 32, 31, 30, 32, 27]),
#     'Weapon Types': np.array(["Sword", "Axe"]),
#     'ID': '29'
# }
#
# SpearFighter = {
#     'Name': "Spear Fighter",
#     'Tier': 1,
#     'Bases': np.array([17, 6, 0, 6, 6, 2, 5, 2]),
#     'Growths': np.array([15, 15, 0, 15, 15, 5, 10, 5]),
#     'Caps': np.array([40, 22, 15, 23, 22, 21, 22, 21]),
#     'Weapon Types': np.array(["Lance"]),
#     'Promotions': np.array(["Spear Master", "Basara"]),
#     'ID': '2d'
# }
#
# SpearMaster = {
#     'Name': "Spear Master",
#     'Tier': 2,
#     'Bases': np.array([18, 9, 0, 8, 8, 3, 7, 3]),
#     'Growths': np.array([15, 15, 0, 15, 15, 5, 10, 5]),
#     'Caps': np.array([60, 34, 25, 33, 32, 29, 30, 29]),
#     'Weapon Types': np.array(["Lance"]),
#     'ID': '2b'
# }
#
# Basara = {
#     'Name': "Basara",
#     'Tier': 2,
#     'Bases': np.array([20, 7, 5, 7, 7, 5, 7, 6]),
#     'Growths': np.array([20, 10, 10, 10, 10, 15, 5, 10]),
#     'Caps': np.array([65, 31, 30, 30, 31, 35, 30, 32]),
#     'Weapon Types': np.array(["Lance", "Tome"]),
#     'ID': '2f'
# }
#
# Diviner = {
#     'Name': "Diviner",
#     'Tier': 1,
#     'Bases': np.array([15, 0, 4, 5, 6, 1, 1, 3]),
#     'Growths': np.array([0, 5, 15, 10, 10, 5, 0, 10]),
#     'Caps': np.array([35, 17, 22, 20, 23, 19, 16, 20]),
#     'Weapon Types': np.array(["Tome"]),
#     'Promotions': np.array(["Onmyoji", "Basara"]),
#     'ID': '31'
# }
#
# Onmyoji = {
#     'Name': "Onmyoji",
#     'Tier': 2,
#     'Bases': np.array([16, 0, 7, 6, 7, 2, 3, 6]),
#     'Growths': np.array([0, 0, 20, 10, 15, 0, 0, 15]),
#     'Caps': np.array([45, 25, 33, 31, 32, 27, 25, 31]),
#     'Weapon Types': np.array(["Tome", "Staff"]),
#     'ID': '33'
# }
#
# Monk = {
#     'Name': "Monk",
#     'Tier': 1,
#     'Bases': np.array([16, 0, 3, 5, 5, 4, 2, 5]),
#     'Growths': np.array([0, 5, 10, 10, 15, 15, 0, 20]),
#     'Caps': np.array([35, 18, 21, 20, 22, 23, 17, 24]),
#     'Weapon Types': np.array(["Staff"]),
#     'Promotions': np.array(["Onmyoji", "Great Master"]),
#     'ID': '35'
# }
#
# ShrineMaiden = {
#     'Name': "Shrine Maiden",
#     'Tier': 1,
#     'Bases': np.array([16, 0, 3, 5, 5, 4, 2, 5]),
#     'Growths': np.array([0, 5, 10, 10, 15, 15, 0, 20]),
#     'Caps': np.array([35, 18, 21, 20, 22, 23, 17, 24]),
#     'Weapon Types': np.array(["Staff"]),
#     'Promotions': np.array(["Onmyoji", "Priestess"])
# }
#
# GreatMaster = {
#     'Name': "Great Master",
#     'Tier': 2,
#     'Bases': np.array([19, 8, 6, 6, 8, 5, 6, 7]),
#     'Growths': np.array([10, 15, 5, 5, 15, 15, 10, 10]),
#     'Caps': np.array([55, 32, 30, 31, 33, 32, 28, 32]),
#     'Weapon Types': np.array(["Lance", "Staff"]),
#     'ID': '37'
# }
#
# Priestess = {
#     'Name': "Priestess",
#     'Tier': 2,
#     'Bases': np.array([19, 6, 7, 6, 9, 5, 5, 8]),
#     'Growths': np.array([10, 10, 10, 5, 15, 15, 0, 20]),
#     'Caps': np.array([50, 29, 32, 30, 33, 34, 26, 34]),
#     'Weapon Types': np.array(["Bow", "Staff"])
# }
#
# SkyKnight = {
#     'Name': "Sky Knight",
#     'Tier': 1,
#     'Bases': np.array([16, 3, 0, 5, 7, 4, 2, 6]),
#     'Growths': np.array([0, 10, 0, 10, 15, 20, 0, 20]),
#     'Caps': np.array([35, 19, 16, 21, 23, 25, 18, 25]),
#     'Weapon Types': np.array(["Lance"]),
#     'Promotions': np.array(["Falcon Knight", "Kinshi Knight"]),
#     'ID': '3b'
# }
#
# FalconKnight = {
#     'Name': "Falcon Knight",
#     'Tier': 2,
#     'Bases': np.array([18, 5, 4, 6, 10, 5, 5, 9]),
#     'Growths': np.array([0, 10, 10, 10, 15, 20, 0, 20]),
#     'Caps': np.array([55, 28, 27, 30, 34, 35, 27, 35]),
#     'Weapon Types': np.array(["Lance", "Staff"]),
#     'ID': '39'
# }
#
# KinshiKnight = {
#     'Name': "Kinshi Knight",
#     'Tier': 2,
#     'Bases': np.array([17, 4, 1, 9, 8, 5, 4, 7]),
#     'Growths': np.array([0, 5, 0, 15, 15, 15, 0, 15]),
#     'Caps': np.array([50, 27, 26, 33, 31, 34, 25, 31]),
#     'Weapon Types': np.array(["Lance", "Bow"]),
#     'ID': '3d'
# }
#
# Archer = {
#     'Name': "Archer",
#     'Tier': 1,
#     'Bases': np.array([17, 5, 0, 7, 5, 2, 4, 1]),
#     'Growths': np.array([10, 15, 0, 15, 15, 5, 10, 0]),
#     'Caps': np.array([40, 21, 15, 23, 21, 20, 20, 17]),
#     'Weapon Types': np.array(["Bow"]),
#     'Promotions': np.array(["Sniper", "Kinshi Knight"]),
#     'ID': '3f'
# }
#
# Sniper = {
#     'Name': "Sniper",
#     'Tier': 2,
#     'Bases': np.array([19, 7, 0, 10, 9, 3, 6, 2]),
#     'Growths': np.array([10, 15, 0, 20, 15, 5, 10, 0]),
#     'Caps': np.array([55, 31, 25, 35, 33, 30, 31, 28]),
#     'Weapon Types': np.array(["Bow"]),
#     'ID': '41'
# }
#
# Ninja = {
#     'Name': "Ninja",
#     'Tier': 1,
#     'Bases': np.array([16, 3, 0, 8, 8, 1, 3, 3]),
#     'Growths': np.array([5, 5, 0, 20, 20, 0, 5, 15]),
#     'Caps': np.array([35, 17, 15, 25, 25, 18, 19, 20]),
#     'Weapon Types': np.array(["Hidden"]),
#     'Promotions': np.array(["Master Ninja", "Mechanist"]),
#     'ID': '4b'
# }
#
# MasterNinja = {
#     'Name': "Master Ninja",
#     'Tier': 2,
#     'Bases': np.array([17, 5, 0, 10, 11, 2, 4, 8]),
#     'Growths': np.array([5, 5, 0, 20, 20, 0, 5, 20]),
#     'Caps': np.array([55, 27, 25, 35, 35, 28, 26, 34]),
#     'Weapon Types': np.array(["Sword", "Hidden"]),
#     'ID': '49'
# }
#
# Mechanist = {
#     'Name': "Mechanist",
#     'Tier': 2,
#     'Bases': np.array([18, 7, 0, 9, 7, 2, 6, 6]),
#     'Growths': np.array([10, 10, 0, 15, 10, 5, 5, 15]),
#     'Caps': np.array([60, 30, 25, 33, 30, 30, 31, 31]),
#     'Weapon Types': np.array(["Hidden", "Bow"]),
#     'ID': '4d'
# }
#
# Kitsune = {
#     'Name': "Kitsune",
#     'Tier': 1,
#     'Bases': np.array([16, 5, 1, 6, 8, 4, 1, 4]),
#     'Growths': np.array([10, 10, 0, 15, 20, 10, 0, 20]),
#     'Caps': np.array([40, 20, 18, 23, 24, 24, 18, 23]),
#     'Weapon Types': np.array(["Stone"]),
#     'Promotions': np.array(["Nine-Tails"]),
#     'ID': '63'
# }
#
# NineTails = {
#     'Name': "Nine-Tails",
#     'Tier': 2,
#     'Bases': np.array([19, 6, 2, 9, 10, 5, 2, 8]),
#     'Growths': np.array([10, 10, 0, 15, 20, 10, 0, 20]),
#     'Caps': np.array([55, 29, 29, 33, 34, 33, 27, 34]),
#     'Weapon Types': np.array(["Stone"]),
#     'ID': '65'
# }
#
# Cavalier = {
#     'Name': "Cavalier",
#     'Tier': 1,
#     'Bases': np.array([17, 6, 0, 5, 5, 3, 5, 3]),
#     'Growths': np.array([10, 15, 0, 10, 10, 15, 10, 5]),
#     'Caps': np.array([40, 22, 15, 21, 20, 24, 22, 21]),
#     'Weapon Types': np.array(["Sword", "Lance"]),
#     'Promotions': np.array(["Paladin", "Great Knight"]),
#     'ID': '9'
# }
#
# Paladin = {
#     'Name': "Paladin",
#     'Tier': 2,
#     'Bases': np.array([19, 8, 1, 7, 7, 4, 7, 6]),
#     'Growths': np.array([10, 15, 0, 10, 10, 15, 10, 10]),
#     'Caps': np.array([60, 31, 26, 30, 30, 32, 32, 32]),
#     'Weapon Types': np.array(["Sword", "Lance"]),
#     'ID': '7'
# }
#
# GreatKnight = {
#     'Name': "Great Knight",
#     'Tier': 2,
#     'Bases': np.array([21, 10, 0, 6, 6, 3, 10, 2]),
#     'Growths': np.array([20, 20, 0, 10, 5, 5, 20, 0]),
#     'Caps': np.array([65, 35, 25, 29, 27, 28, 37, 28]),
#     'Weapon Types': np.array(["Sword", "Lance", "Axe"]),
#     'ID': 'b'
# }
#
# Knight = {
#     'Name': "Knight",
#     'Tier': 1,
#     'Bases': np.array([19, 8, 0, 5, 3, 3, 8, 1]),
#     'Growths': np.array([20, 20, 0, 15, 5, 10, 20, 0]),
#     'Caps': np.array([45, 24, 15, 22, 17, 22, 26, 18]),
#     'Weapon Types': np.array(["Lance"]),
#     'Promotions': np.array(["Great Knight", "General"]),
#     'ID': 'd'
# }
#
# General = {
#     'Name': "General",
#     'Tier': 2,
#     'Bases': np.array([22, 11, 0, 7, 3, 4, 12, 3]),
#     'Growths': np.array([25, 20, 0, 15, 0, 10, 20, 5]),
#     'Caps': np.array([70, 38, 25, 32, 25, 32, 40, 30]),
#     'Weapon Types': np.array(["Lance", "Axe"]),
#     'ID': 'f'
# }
#
# Fighter = {
#     'Name': "Fighter",
#     'Tier': 1,
#     'Bases': np.array([19, 7, 0, 6, 6, 2, 4, 1]),
#     'Growths': np.array([20, 20, 0, 15, 15, 5, 5, 0]),
#     'Caps': np.array([45, 25, 15, 23, 22, 21, 19, 18]),
#     'Weapon Types': np.array(["Axe"]),
#     'Promotions': np.array(["Berserker", "Hero"]),
#     'ID': '13'
# }
#
# Berserker = {
#     'Name': "Berserker",
#     'Tier': 2,
#     'Bases': np.array([24, 12, 0, 8, 9, 0, 5, 0]),
#     'Growths': np.array([30, 25, 0, 15, 15, 0, 0, 0]),
#     'Caps': np.array([70, 40, 25, 32, 33, 25, 27, 25]),
#     'Weapon Types': np.array(["Axe"]),
#     'ID': '11'
# }
#
# Mercenary = {
#     'Name': "Mercenary",
#     'Tier': 1,
#     'Bases': np.array([17, 5, 0, 7, 6, 2, 5, 2]),
#     'Growths': np.array([10, 15, 0, 20, 15, 5, 10, 5]),
#     'Caps': np.array([40, 22, 15, 24, 22, 20, 21, 19]),
#     'Weapon Types': np.array(["Sword"]),
#     'Promotions': np.array(["Hero", "Bow Knight"]),
#     'ID': '17'
# }
#
# Hero = {
#     'Name': "Hero",
#     'Tier': 2,
#     'Bases': np.array([20, 8, 0, 10, 8, 3, 7, 2]),
#     'Growths': np.array([20, 15, 0, 20, 15, 5, 10, 0]),
#     'Caps': np.array([60, 32, 25, 35, 32, 31, 30, 27]),
#     'Weapon Types': np.array(["Sword", "Axe"]),
#     'ID': '15'
# }
#
# BowKnight = {
#     'Name': "Bow Knight",
#     'Tier': 2,
#     'Bases': np.array([18, 6, 0, 8, 9, 3, 5, 6]),
#     'Growths': np.array([10, 10, 0, 15, 15, 10, 0, 10]),
#     'Caps': np.array([55, 29, 25, 32, 33, 30, 27, 32]),
#     'Weapon Types': np.array(["Sword", "Bow"]),
#     'ID': '19'
# }
#
# Outlaw = {
#     'Name': "Outlaw",
#     'Tier': 1,
#     'Bases': np.array([16, 3, 1, 4, 8, 1, 2, 4]),
#     'Growths': np.array([0, 10, 5, 10, 20, 0, 0, 20]),
#     'Caps': np.array([35, 19, 18, 20, 24, 18, 17, 22]),
#     'Weapon Types': np.array(["Bow"]),
#     'Promotions': np.array(["Bow Knight", "Adventurer"]),
#     'ID': '1b'
# }
#
# Adventurer = {
#     'Name': "Adventurer",
#     'Tier': 2,
#     'Bases': np.array([17, 4, 6, 6, 10, 2, 3, 8]),
#     'Growths': np.array([0, 5, 15, 5, 20, 0, 0, 20]),
#     'Caps': np.array([50, 27, 31, 27, 34, 27, 25, 34]),
#     'Weapon Types': np.array(["Bow", "Staff"]),
#     'ID': '1d'
# }
#
# WyvernRider = {
#     'Name': "Wyvern Rider",
#     'Tier': 1,
#     'Bases': np.array([17, 6, 0, 5, 4, 2, 7, 0]),
#     'Growths': np.array([10, 15, 5, 10, 10, 5, 20, 0]),
#     'Caps': np.array([40, 22, 17, 21, 20, 19, 24, 15]),
#     'Weapon Types': np.array(["Axe"]),
#     'Promotions': np.array(["Wyvern Lord", "Malig Knight"]),
#     'ID': '45'
# }
#
# WyvernLord = {
#     'Name': "Wyvern Lord",
#     'Tier': 2,
#     'Bases': np.array([19, 8, 0, 9, 6, 3, 10, 1]),
#     'Growths': np.array([10, 15, 0, 15, 10, 5, 20, 0]),
#     'Caps': np.array([60, 33, 25, 33, 29, 28, 35, 26]),
#     'Weapon Types': np.array(["Lance", "Axe"]),
#     'ID': '43'
# }
#
# MaligKnight = {
#     'Name': "Malig Knight",
#     'Tier': 2,
#     'Bases': np.array([18, 7, 6, 6, 5, 0, 8, 6]),
#     'Growths': np.array([0, 15, 15, 10, 5, 0, 10, 15]),
#     'Caps': np.array([55, 31, 30, 28, 27, 25, 31, 31]),
#     'Weapon Types': np.array(["Axe", "Tome"]),
#     'ID': '47'
# }
#
# DarkMage = {
#     'Name': "Dark Mage",
#     'Tier': 1,
#     'Bases': np.array([16, 0, 6, 3, 3, 1, 3, 5]),
#     'Growths': np.array([0, 10, 20, 0, 10, 0, 5, 10]),
#     'Caps': np.array([35, 19, 24, 16, 19, 18, 19, 22]),
#     'Weapon Types': np.array(["Tome"]),
#     'Promotions': np.array(["Sorcerer", "Dark Knight"]),
#     'ID': '55'
# }
#
# Sorcerer = {
#     'Name': "Sorcerer",
#     'Tier': 2,
#     'Bases': np.array([17, 0, 9, 4, 6, 1, 5, 8]),
#     'Growths': np.array([0, 0, 25, 0, 10, 0, 5, 15]),
#     'Caps': np.array([50, 25, 35, 26, 29, 26, 29, 33]),
#     'Weapon Types': np.array(["Tome"]),
#     'ID': '53'
# }
#
# DarkKnight = {
#     'Name': "Dark Knight",
#     'Tier': 2,
#     'Bases': np.array([19, 8, 6, 6, 5, 3, 8, 6]),
#     'Growths': np.array([15, 20, 10, 5, 5, 5, 15, 5]),
#     'Caps': np.array([55, 32, 31, 28, 27, 31, 34, 30]),
#     'Weapon Types': np.array(["Sword", "Tome"]),
#     'ID': '57'
# }
#
# Troubadour = {
#     'Name': "Troubadour",
#     'Tier': 1,
#     'Bases': np.array([15, 0, 3, 7, 5, 4, 1, 4]),
#     'Growths': np.array([0, 0, 10, 20, 10, 15, 0, 15]),
#     'Caps': np.array([35, 16, 19, 24, 20, 23, 16, 21]),
#     'Weapon Types': np.array(["Staff"]),
#     'Promotions': np.array(["Maid/Butler", "Strategist"]),
#     'ID': '5b'
# }
#
# Strategist = {
#     'Name': "Strategist",
#     'Tier': 2,
#     'Bases': np.array([16, 0, 7, 6, 7, 5, 2, 7]),
#     'Growths': np.array([0, 0, 15, 5, 10, 20, 0, 15]),
#     'Caps': np.array([45, 25, 33, 28, 31, 33, 25, 32]),
#     'Weapon Types': np.array(["Tome", "Staff"]),
#     'ID': '59'
# }
#
# MaidButler = {
#     'Name': "Maid/Butler",
#     'Tier': 2,
#     'Bases': np.array([18, 4, 5, 9, 8, 4, 5, 4]),
#     'Growths': np.array([0, 10, 10, 15, 15, 10, 5, 10]),
#     'Caps': np.array([50, 28, 31, 33, 33, 32, 29, 29]),
#     'Weapon Types': np.array(["Hidden", "Staff"]),
#     'ID': '5d'
# }
#
# Wolfskin = {
#     'Name': "Wolfskin",
#     'Tier': 1,
#     'Bases': np.array([19, 8, 0, 4, 6, 0, 4, 0]),
#     'Growths': np.array([20, 20, 0, 5, 15, 5, 10, 0]),
#     'Caps': np.array([45, 24, 15, 18, 22, 17, 21, 15]),
#     'Weapon Types': np.array(["Stone"]),
#     'Promotions': np.array(["Wolfssegner"]),
#     'ID': '5f'
# }
#
# Wolfssegner = {
#     'Name': "Wolfssegner",
#     'Tier': 2,
#     'Bases': np.array([22, 11, 0, 6, 7, 1, 7, 1]),
#     'Growths': np.array([20, 20, 0, 5, 15, 5, 10, 0]),
#     'Caps': np.array([65, 36, 25, 29, 31, 26, 32, 26]),
#     'Weapon Types': np.array(["Stone"]),
#     'ID': '61'
# }
#
# Songstress = {
#     'Name': "Songstress",
#     'Tier': 3,
#     'Bases': np.array([16, 3, 0, 6, 5, 3, 2, 3]),
#     'Growths': np.array([0, 10, 0, 20, 20, 20, 0, 0]),
#     'Caps': np.array([45, 28, 27, 31, 31, 35, 27, 28]),
#     'Weapon Types': np.array(["Lance"]),
#     'ID': '67'
# }
#
# DarkFalcon = {
#     'Name': "Dark Falcon",
#     'Tier': 3,
#     'Bases': np.array([17, 4, 7, 5, 9, 4, 3, 9]),
#     'Growths': np.array([0, 10, 15, 5, 15, 15, 0, 20]),
#     'Caps': np.array([45, 27, 32, 28, 33, 32, 26, 34]),
#     'Weapon Types': np.array(["Lance", "Tome"]),
#     'ID': '78'
# }
#
# DreadFighter = {
#     'Name': "Dread Fighter",
#     'Tier': 3,
#     'Bases': np.array([19, 8, 3, 6, 8, 1, 6, 9]),
#     'Growths': np.array([15, 15, 5, 5, 15, 0, 5, 20]),
#     'Caps': np.array([55, 32, 28, 29, 31, 26, 29, 34]),
#     'Weapon Types': np.array(["Sword", "Axe", "Hidden"]),
#     'ID': '76'
# }
#
# Lodestar = {
#     'Name': "Lodestar",
#     'Tier': 3,
#     'Bases': np.array([19, 7, 0, 10, 9, 7, 7, 2]),
#     'Growths': np.array([15, 10, 0, 20, 10, 25, 5, 5]),
#     'Caps': np.array([60, 29, 26, 35, 33, 40, 30, 29]),
#     'Weapon Types': np.array(["Sword"]),
#     'ID': '7c'
# }
#
# GreatLord = {
#     'Name': "Great Lord",
#     'Tier': 3,
#     'Bases': np.array([18, 8, 1, 8, 9, 5, 7, 3]),
#     'Growths': np.array([15, 15, 0, 10, 10, 15, 10, 5]),
#     'Caps': np.array([60, 30, 25, 32, 34, 35, 29, 31]),
#     'Weapon Types': np.array(["Sword", "Lance"]),
#     'ID': '7e'
# }
#
# Vanguard = {
#     'Name': "Vanguard",
#     'Tier': 3,
#     'Bases': np.array([21, 10, 0, 6, 7, 3, 9, 1]),
#     'Growths': np.array([20, 20, 0, 5, 5, 10, 15, 0]),
#     'Caps': np.array([65, 36, 25, 29, 30, 30, 32, 27]),
#     'Weapon Types': np.array(["Sword", "Axe"]),
#     'ID': '7d'
# }
#
# Grandmaster = {
#     'Name': "Grandmaster",
#     'Tier': 3,
#     'Bases': np.array([18, 7, 6, 8, 7, 2, 6, 8]),
#     'Growths': np.array([10, 15, 15, 15, 5, 0, 5, 15]),
#     'Caps': np.array([55, 31, 33, 33, 29, 26, 28, 33]),
#     'Weapon Types': np.array(["Sword", "Tome"]),
#     'ID': '7f'
# }
#
# Witch = {
#     'Name': "Witch",
#     'Tier': 3,
#     'Bases': np.array([17, 0, 10, 5, 9, 3, 4, 5]),
#     'Growths': np.array([5, 0, 25, 5, 20, 5, 0, 10]),
#     'Caps': np.array([50, 25, 36, 27, 34, 28, 26, 29]),
#     'Weapon Types': np.array(["Tome"]),
#     'ID': '7b'
# }
#
# Ballistician = {
#     'Name': "Ballistician",
#     'Tier': 3,
#     'Bases': np.array([18, 10, 0, 7, 2, 4, 3, 1]),
#     'Growths': np.array([5, 25, 0, 15, 0, 10, 5, 5]),
#     'Caps': np.array([50, 39, 25, 31, 25, 32, 27, 26]),
#     'Weapon Types': np.array(["Bow"]),
#     'ID': '7a'
# }
#
# classes = pd.DataFrame([
#     NohrPrince,
#     HoshidoNoble,
#     NohrNoble,
#     Samurai,
#     Swordmaster,
#     MasterOfArms,
#     Merchant,
#     Villager,
#     Apothecary,
#     OniSavage,
#     OniChieftain,
#     Blacksmith,
#     SpearFighter,
#     SpearMaster,
#     Basara,
#     Diviner,
#     Onmyoji,
#     Monk,
#     ShrineMaiden,
#     GreatMaster,
#     Priestess,
#     SkyKnight,
#     FalconKnight,
#     KinshiKnight,
#     Archer,
#     Sniper,
#     Ninja,
#     MasterNinja,
#     Mechanist,
#     Kitsune,
#     NineTails,
#     Cavalier,
#     Paladin,
#     GreatKnight,
#     Knight,
#     General,
#     Fighter,
#     Berserker,
#     Mercenary,
#     Hero,
#     BowKnight,
#     Outlaw,
#     Adventurer,
#     WyvernRider,
#     WyvernLord,
#     MaligKnight,
#     DarkMage,
#     Sorcerer,
#     DarkKnight,
#     Troubadour,
#     Strategist,
#     MaidButler,
#     Wolfskin,
#     Wolfssegner,
#     Songstress,
#     DarkFalcon,
#     DreadFighter,
#     Lodestar,
#     GreatLord,
#     Vanguard,
#     Grandmaster,
#     Witch,
#     Ballistician
# ])
