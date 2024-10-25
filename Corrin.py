import modifiers
import numpy as np
import edit_this


# Every time you create a new Corrin, you should use this.
# IMPORTANT NOTE: DO NOT CREATE A CORRIN BEFORE YOU VALIDATE THE DATA!!!!
# This assumes that you've already made sure that all the values for the variables are valid,
# like for example Hairstyle is a value from 1-12 (inclusive).
class Corrin:
    def __init__(self, df_row):
        # Step 1: Get Corrin's name.
        self.name = df_row[edit_this.NAME].strip()

        # Step 2: Get Corrin's gender. Don't blame me for Fates's blind trust in the gender binary!
        self.gender = df_row[edit_this.GENDER]

        # Step 3: Get Corrin's build (short or tall)
        self.body = df_row[edit_this.BUILD]

        # Step 4: Get Corrin's face
        self.face = df_row[edit_this.FACE]

        # Step 5: Get Corrin's hairstyle
        self.style = df_row[edit_this.HAIRSTYLE]

        # Step 6: Get Corrin's hair clip. If the Corrin doesn't have one or is male, this'll be 0.
        self.decoration = df_row[edit_this.HAIR_CLIP]

        # Step 7: Get Corrin's facial feature (eye-patch, scar, etc.) If the Corrin doesn't have one, this'll be 0.
        self.detail = df_row[edit_this.FACIAL_FEATURE]

        # Step 8: Get Corrin's voice. In the US version of Fates, there's only 3 options per gender.
        self.voice = df_row[edit_this.VOICE]

        # Step 9: Get Corrin's hair color. Right now, I'm only supporting RGB because I can't be fucked making 30
        # corrins to figure out all the default hex values.
        self.hair_color = [df_row[edit_this.HAIR_COLOR][0:2], df_row[edit_this.HAIR_COLOR][2:4],
                           df_row[edit_this.HAIR_COLOR][4:6]]

        # Step 10: Get Corrin's boons and banes. This will be a 3 value array no matter what, but if you're only
        # doing 1 or 2 routes, the program will simply access the routes that you'll have data for.
        self.boon = [df_row[edit_this.BOON_BR], df_row[edit_this.BOON_CQ], df_row[edit_this.BOON_REV]]
        self.bane = [df_row[edit_this.BANE_BR], df_row[edit_this.BANE_CQ], df_row[edit_this.BANE_REV]]

        # Step 11: Get Corrin's base class and promotion. Like the boons and banes, this is also a 3-value array.
        # In this step, we also account for the rare gender-locked classes in Fates, those being Monk, Shrine Maiden,
        # Maid, Butler, Priestess, and Great Master.
        self.base_class = [df_row[edit_this.BASE_CLASS_BR], df_row[edit_this.BASE_CLASS_CQ],
                           df_row[edit_this.BASE_CLASS_REV]]
        self.promotion = [df_row[edit_this.PROMOTED_CLASS_BR], df_row[edit_this.PROMOTED_CLASS_CQ],
                          df_row[edit_this.PROMOTED_CLASS_REV]]
        for i in range(0, len(self.base_class)):
            if self.base_class[i] == "Monk/Shrine Maiden":
                if self.gender == "Male":
                    self.base_class[i] = "Monk"
                if self.gender == "Female":
                    self.base_class[i] = "Shrine Maiden"
        for i in range(0, len(self.promotion)):
            if self.promotion[i] == "Maid/Butler":
                if self.gender == "Male":
                    self.promotion[i] = "Butler"
                if self.gender == "Female":
                    self.promotion[i] = "Maid"

        # Step 12: Get Corrin's skills. This will be a 3x5 array. Just like the previous two, if you're doing less
        # than 3 routes, the program will handle it. The 5 is for the skill slots per route. Not all skill slots will
        # be filled, and those will have a value of "None".
        if len(df_row[edit_this.SKILLS_BR]) > 5:
            df_row[edit_this.SKILLS_BR] = df_row[edit_this.SKILLS_BR][0:5]
        if len(df_row[edit_this.SKILLS_CQ]) > 5:
            df_row[edit_this.SKILLS_CQ] = df_row[edit_this.SKILLS_CQ][0:5]
        if len(df_row[edit_this.SKILLS_REV]) > 5:
            df_row[edit_this.SKILLS_REV] = df_row[edit_this.SKILLS_REV][0:5]
        self.skills = [df_row[edit_this.SKILLS_BR], df_row[edit_this.SKILLS_CQ], df_row[edit_this.SKILLS_REV]]

        # Step 13: Get Corrin's stat sheet. This isn't a normal level-based stat sheet. It takes Corrin's growths/bases
        # and turns it into a 21-row array. Each row represents what Corrin's stats will be at a given chapter, starting
        # from Chapter 7 and going all the way to Chapter 27. This also doesn't count class bases or Corrin's bases,
        # because when editing the hex values, FEFTwiddler also does not count those.
        self.stats = np.round(
            [modifiers.calculate_stats(self.base_class[0], self.promotion[0], self.boon[0], self.bane[0]),
             modifiers.calculate_stats(self.base_class[1], self.promotion[1], self.boon[1], self.bane[1]),
             modifiers.calculate_stats(self.base_class[2], self.promotion[2], self.boon[2], self.bane[2])])
        for i in range(0, 3):
            for j in range(0, 21):
                for k in range(0, 8):
                    if self.stats[i][j][k] < 0:
                        self.stats[i][j][k] = 0

        self.stats = self.stats.astype(int).astype(str)

    def __repr__(self):
        return (f"Corrin(name='{self.name}', boon='{self.boon}', bane='{self.bane}', gender='{self.gender}', "
                f"base_class='{self.base_class}', body={self.body}, face={self.face}, style={self.style}, "
                f"hair_color={self.hair_color}, decoration={self.decoration}, detail={self.detail}, voice={self.voice},"
                f" skills={self.skills})")
