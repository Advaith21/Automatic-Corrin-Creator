import edit_this
from skills import skill_prices_dict
import classes as cs


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


def is_valid_hex_string(s):
    valid_chars = "0123456789abcdefABCDEF"
    return all(char in valid_chars for char in s)


class CorrinValidator:
    def __init__(self, df, mode, BR, CQ, REV, budget):
        self.df = df
        self.mode = mode
        self.BR = BR
        self.CQ = CQ
        self.REV = REV
        self.budget = budget
        self.to_be_removed = []
        self.error_log = open("error.txt", 'a')

        # The program can't just handle "Monk/Shrine Maiden" or "Maid/Butler" as your class, so this sorts that out.
        for inn, r in self.df.iterrows():
            if r[edit_this.BASE_CLASS_BR] == "Monk/Shrine Maiden":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.BASE_CLASS_BR] = "Monk"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.BASE_CLASS_BR] = "Shrine Maiden"
            if r[edit_this.BASE_CLASS_CQ] == "Monk/Shrine Maiden":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.BASE_CLASS_CQ] = "Monk"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.BASE_CLASS_CQ] = "Shrine Maiden"
            if r[edit_this.BASE_CLASS_REV] == "Monk/Shrine Maiden":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.BASE_CLASS_REV] = "Monk"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.BASE_CLASS_REV] = "Shrine Maiden"

            if r[edit_this.PROMOTED_CLASS_BR] == "Maid/Butler":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_BR] = "Butler"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_BR] = "Maid"
            if r[edit_this.PROMOTED_CLASS_CQ] == "Maid/Butler":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_CQ] = "Butler"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_CQ] = "Maid"
            if r[edit_this.PROMOTED_CLASS_REV] == "Maid/Butler":
                if r[edit_this.GENDER] == "Male":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_REV] = "Butler"
                if r[edit_this.GENDER] == "Female":
                    self.df.at[inn, edit_this.PROMOTED_CLASS_REV] = "Maid"
                

    def log_error(self, message):
        self.error_log.write(message + "\n")

    def validate_all(self):
        for inn, r in self.df.iterrows():
            self.validate_name(r, inn)
            self.validate_body(r, inn)
            self.validate_face(r, inn)
            self.validate_hairstyle(r, inn)
            self.validate_detail(r, inn)
            self.validate_decoration(r, inn)
            self.validate_voice(r, inn)
            self.validate_boon_bane(r, inn)
            self.validate_hair_color(r, inn)
            self.validate_skills(r, inn)
            self.validate_promotion(r, inn)
        
        self.to_be_removed = list(set(self.to_be_removed))
        self.df.drop(self.to_be_removed, inplace=True)
        self.error_log.close()

    def validate_name(self, row, index):
        """Makes sure the current row's Corrin has a valid name."""
        row[edit_this.NAME] = row[edit_this.NAME].strip()  # Remove all leading/terminating whitespace
        # Check for valid name length
        if not 1 <= len(row[edit_this.NAME]) <= 8:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s name input was invalid.")
            self.to_be_removed.append(index)

    def validate_body(self, row, index):
        """Makes sure the current row's Corrin has a valid body type (1 or 2)."""
        if row[edit_this.BUILD] not in [1, 2]:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s body type input of {row[edit_this.BUILD]} was invalid.")
            self.to_be_removed.append(index)

    def validate_hairstyle(self, row, index):
        if not 1 <= row[edit_this.HAIRSTYLE] <= 12:
            self.log_error(
                f"Corrin \'{row[edit_this.NAME]}\''s hairstyle input of {row[edit_this.HAIRSTYLE]} was invalid.")
            self.to_be_removed.append(index)

    def validate_face(self, row, index):
        if not 1 <= row[edit_this.FACE] <= 7:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s face input of {row[edit_this.FACE]} was invalid.")
            self.to_be_removed.append(index)

    def validate_detail(self, row, index):
        if not 0 <= row[edit_this.FACIAL_FEATURE] <= 12:
            self.log_error(
                f"Corrin \'{row[edit_this.NAME]}\''s facial feature input of {row[edit_this.FACIAL_FEATURE]} was invalid.")
            self.to_be_removed.append(index)

    def validate_decoration(self, row, index):
        if row[edit_this.GENDER] == "Male" and row[edit_this.HAIR_CLIP] != 0:
            row[edit_this.HAIR_CLIP] = 0
        elif not 0 <= row[edit_this.HAIR_CLIP] <= 5:
            self.log_error(
                f"Corrin \'{row[edit_this.NAME]}\''s hair pin input of {row[edit_this.HAIR_CLIP]} was invalid.")
            self.to_be_removed.append(index)

    def validate_voice(self, row, index):
        if not 1 <= row[edit_this.VOICE] <= 3:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s voice input of {row[edit_this.VOICE]} was invalid.")
            self.to_be_removed.append(index)

    def validate_hair_color(self, row, index):

        # Convert all the values to lower case.
        h_string = row[edit_this.HAIR_COLOR].lower()
        h_string = h_string.strip()

        # Step 1: Check to make sure they didn't just send in something that's far too short.
        if len(h_string) < 6:
            self.log_error(
                f"Corrin \'{row[edit_this.NAME]}\''s hair color input of '{row[edit_this.HAIR_COLOR]}' was invalid.")
            self.to_be_removed.append(index)

        # Step 2: Handle the case where the user properly input the hex values.
        elif is_valid_hex_string(h_string) and len(h_string) == 6:
            h_string = h_string

        # Step 3: Handle the case where the user input a hex string but then some extra stuff after it.
        elif is_valid_hex_string(h_string[0:6]):
            h_string = h_string[0:6]

        # Step 4: Handle the case where the user improperly input the hex value as "#rrggbb" instead of just "rrggbb".
        elif h_string[0] == "#" and len(h_string) == 7 and is_valid_hex_string(h_string[1:]):
            h_string = h_string[1:]

        # Step 5: If the program reaches this else, then something is wrong, but we don't know what.
        else:
            self.log_error(
                f"Corrin \'{row[edit_this.NAME]}\''s hair color input of '{row[edit_this.HAIR_COLOR]}' was invalid.")
            self.to_be_removed.append(index)

        # Step 6: If we actually edited the string from #rrggbb to rrggbb, the dataframe also has to reflect that.
        self.df.at[index, edit_this.HAIR_COLOR] = h_string

    def validate_boon_bane(self, row, index):
        drop = False
        # Check each route to see if it's invalid
        if self.BR and row[edit_this.BOON_BR] == row[edit_this.BANE_BR]: drop = True
        if self.CQ and row[edit_this.BOON_CQ] == row[edit_this.BANE_CQ]: drop = True
        if self.REV and row[edit_this.BOON_REV] == row[edit_this.BANE_REV]: drop = True

        # Output the error
        if drop:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s boon/bane input was invalid.")
            self.log_error(f"\tBirthright - Boon: {row[edit_this.BOON_BR]}, Bane: {row[edit_this.BANE_BR]}")
            self.log_error(f"\tConquest - Boon: {row[edit_this.BOON_CQ]}, Bane: {row[edit_this.BANE_CQ]}")
            self.log_error(f"\tRevelation - Boon: {row[edit_this.BOON_REV]}, Bane: {row[edit_this.BANE_REV]}")
            self.to_be_removed.append(index)

    def validate_skills(self, row, index):

        routes = 0

        if self.BR: routes += 1
        if self.CQ: routes += 1
        if self.REV: routes += 1

        if routes == 0:
            print("ERROR. ZERO ROUTES SELECTED.")
            exit(1)

        i = 0

        if self.BR: i += skill_sum(row[edit_this.SKILLS_BR])
        if self.CQ: i += skill_sum(row[edit_this.SKILLS_CQ])
        if self.REV: i += skill_sum(row[edit_this.SKILLS_REV])

        if i < 0:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s skillset contains at least one banned skill.")
            self.to_be_removed.append(index)
        elif i > self.budget:
            self.log_error(f"Corrin \'{row[edit_this.NAME]}\''s skillset is over budget.")
            self.to_be_removed.append(index)

    def validate_promotion(self, row, index):
        drop = False
        if self.BR:
            drop |= not self.validate_promotion_helper(row[edit_this.BASE_CLASS_BR], row[edit_this.PROMOTED_CLASS_BR],
                                                       row[edit_this.NAME])
        if self.CQ:
            drop |= not self.validate_promotion_helper(row[edit_this.BASE_CLASS_CQ], row[edit_this.PROMOTED_CLASS_CQ],
                                                       row[edit_this.NAME])
        if self.REV:
            drop |= not self.validate_promotion_helper(row[edit_this.BASE_CLASS_REV], row[edit_this.PROMOTED_CLASS_REV],
                                                       row[edit_this.NAME])

        if drop:
            self.to_be_removed.append(index)

    def validate_promotion_helper(self, base_class, promoted_class, cor_name):
        bc_series = cs.classes[cs.classes["Name"] == base_class]
        pc_series = cs.classes[cs.classes["Name"] == promoted_class]
    
        if self.mode == 1:
            return self.check_mode_1(bc_series, pc_series, base_class, promoted_class, cor_name)
        elif self.mode == 2:
            return self.check_mode_2(bc_series, pc_series, base_class, promoted_class, cor_name)
        elif self.mode == 3:
            return self.check_mode_3(bc_series, pc_series, base_class, promoted_class, cor_name)
        else:
            self.log_error(f"ERROR IN validate_promotion: Invalid mode selection {self.mode}")
            return False

    def check_mode_1(self, bc_series, pc_series, base_class, promoted_class, cor_name):
        if not self.validate_tiers(bc_series, pc_series, base_class, promoted_class, cor_name):
            return False

        bc_weapons = bc_series['Weapon Types'].tolist()[0]
        pc_weapons = pc_series['Weapon Types'].tolist()[0]
        bc_promo = bc_series['Promotions'].tolist()[0]

        # You can normally promote into this class
        if any(promo == promoted_class for promo in bc_promo):
            return True

        # If you can't noramlly promote into it, it has to be a DLC class
        elif pc_series['Tier'].tolist()[0] != 3:
            self.log_error(f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\".")
            return False

        # If it is a DLC class, you have to share a weapon type
        for i in range(0, len(bc_weapons)):
            if bc_weapons[i] in pc_weapons:
                return True

        # If we reach here something has gone wrong we gotta return false.
        self.log_error(f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\".")
        return False

    def check_mode_2(self, bc_series, pc_series, base_class, promoted_class, cor_name):
        if not self.validate_tiers(bc_series, pc_series, base_class, promoted_class, cor_name):
            return False

        bc_weapons = bc_series['Weapon Types'].tolist()[0]
        pc_weapons = pc_series['Weapon Types'].tolist()[0]

        if any(bc_weapon == pc_weapon for bc_weapon in bc_weapons for pc_weapon in pc_weapons):
            return True

        self.log_error(
            f"Invalid promotion from {base_class} to {promoted_class} for Corrin \"{cor_name}\". The classes do not share a weapon type.")
        return False

    def check_mode_3(self, bc_series, pc_series, base_class, promoted_class, cor_name):
        if not self.validate_tiers(bc_series, pc_series, base_class, promoted_class, cor_name):
            return False

        return True

    def validate_tiers(self, bc_series, pc_series, base_class, promoted_class, cor_name):
        bc_series = cs.classes[cs.classes["Name"] == base_class]
        pc_series = cs.classes[cs.classes["Name"] == promoted_class]

        if bc_series["Tier"].tolist()[0] != 1:
            self.log_error(f"Invalid base class of {base_class} for Corrin \"{cor_name}\"")
            return False
        if pc_series["Tier"].tolist()[0] == 1:
            self.log_error(f"Invalid promoted class of {promoted_class} for Corrin \"{cor_name}\"")
            return False
        return True
