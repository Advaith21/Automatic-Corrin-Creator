import numpy as np
import pandas as pd

# This file contains every single valid class in Corrinquest and their bases, growths, caps, their tier and their name.
# NOTE: With the exception of Monk, Shrine Maiden, Priestess, and Great Master, ALL IDs here refer to the MALE CLASS!!
# If you want the female class ID, just add 1 to it. So, the class ID for M!General is F, the ID for F!General is 10.
# Also note that the DLC classes not named Dread Fighter and Dark Falcon DO NOT HAVE GENDER VERSIONS so all Witches
# regardless of gender will have an ID of 7b.
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