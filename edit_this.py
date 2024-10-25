import numpy as np

# This is the budget for skills. Right now, this is calibrated for three routes. You should change this if you're not
# doing all three routes.
BUDGET = 250

# These variables are just a more convenient way to edit whether you're playing a route or not. If you're playing a
# route, put it down as "True." Otherwise, put it down as "False".
PLAYING_BIRTHRIGHT = True
PLAYING_CONQUEST = True
PLAYING_REVELATION = True

# This variable tells us what promotions will be allowed. I've currently built this to support three modes:
# 1: Only allow promotions into original promo set + DLC classes you share a weapon type with (e.g. Fighter can promo into Hero, Berserker, Dread Fighter or Vanguard).
# 2: Allow promotions into any class you share a weapon type with (e.g. Nohr Prince can promote into Wolfssegner).
# 3: Allow promotions into any class.
PROMOTION_MODE = 1

# This variable is the ID of your Google Sheet. You want what's after the d/ and the next / character.
SPREADSHEET_ID = "1OfCXIUhOMz9ANUtNADjdk9GvLxVqFR6EfmTYCIho6fs"

# This NumPy array holds the values of all the skills in the game. Edit this array if you want to re-assign skills
# values. Note that a value of -1 means that a skill is illegal or banned.
skill_prices = np.array([
    ["None", 0],
    ["Dragonskin", -1],
    ["Divine Shield", -1],
    ["Void Curse", -1],
    ["Self-Destruct", -1],
    ["Staff Savant", -1],
    ["Supportive", -1],
    ["Devoted Partner", -1],
    ["Evasive Partner", -1],
    ["Forceful Partner", -1],
    ["Vow of Friendship", -1],
    ["Peacebringer", -1],
    ["Capture", -1],
    ["Kidnap", -1],
    ["Born Steward", -1],
    ["Sweet Tooth", -1],
    ["Collector", -1],
    ["Beastbane", -1],
    ["Inspiring Song", -1],
    ["Foreign Princess", -1],
    ["Survey", -1],
    ["Opportunity Shot", -1],
    ["Rifled Barrel", -1],
    ["Surefooted", -1],
    ["Paragon", 150],
    ["Strengthtaker", 150],
    ["Magictaker", 150],
    ["Trample", 150],
    ["Shurikenfaire", 150],
    ["Tomefaire", 150],
    ["Immune Status", 150],
    ["Galeforce", 150],
    ["Bold Stance", 125],
    ["Winged Shield", 125],
    ["Axefaire", 125],
    ["Bowfaire", 125],
    ["Rally Spectrum", 125],
    ["Point Blank", 125],
    ["Replicate", 125],
    ["Fiery Blood", 125],
    ["Bushido", 125],
    ["Aggressor", 100],
    ["Swordfaire", 100],
    ["Lancefaire", 100],
    ["Awakening", 100],
    ["Chivalry", 100],
    ["Sisterhood", 100],
    ["Hit/Avo +20", 75],
    ["Strong Riposte", 75],
    ["Elbow Room", 75],
    ["Heavy Blade", 75],
    ["Rally Strength", 75],
    ["Rally Magic", 75],
    ["Inspiration", 75],
    ["Quixotic", 75],
    ["Defensetaker", 75],
    ["Speedtaker", 75],
    ["Rose's Thorns", 75],
    ["Nohr Enmity", 75],
    ["Puissance", 75],
    ["Shadowgift", 75],
    ["Competitive", 75],
    ["Vantage", 50],
    ["Noble Cause", 50],
    ["Strength +2", 50],
    ["Malefic Aura", 50],
    ["Magic +2", 50],
    ["Movement +1", 50],
    ["Dancing Blade", 50],
    ["Rally Speed", 50],
    ["Rally Defense", 50],
    ["Sol", 50],
    ["Quick Draw", 50],
    ["Life and Death", 50],
    ["Certain Blow", 50],
    ["Resist Status", 50],
    ["Renewal", 50],
    ["Lunge", 50],
    ["Perfectionist", 50],
    ["Lily's Poise", 50],
    ["Optimist", 50],
    ["Lucky Charm", 40],
    ["Fierce Mien", 40],
    ["Hit/Avo +10", 40],
    ["Beast Shield", 40],
    ["HP +5", 40],
    ["Speed +2", 40],
    ["Swordbreaker", 40],
    ["Shurikenbreaker", 40],
    ["Bowbreaker", 40],
    ["Rally Luck", 40],
    ["Rally Resistance", 40],
    ["Defender", 40],
    ["Tactical Advice", 40],
    ["Air Superiority", 40],
    ["Heartseeker", 40],
    ["Aptitude", 40],
    ["Charm", 40],
    ["Rallying Cry", 40],
    ["Quiet Strength", 40],
    ["Even Handed", 40],
    ["Odd Shaped", 40],
    ["Darting Blow", 40],
    ["Lucky Seven", 40],
    ["Amaterasu", 40],
    ["Shelter", 40],
    ["Better Odds", 40],
    ["Even Better", 40],
    ["Draconic Hex", 40],
    ["Savage Blow", 40],
    ["Seal Speed", 40],
    ["Spendthrift", 40],
    ["Astra", 40],
    ["Fierce Counter", 40],
    ["Opportunist", 40],
    ["Wind Disciple", 30],
    ["Defense +2", 30],
    ["Axebreaker", 30],
    ["Tomebreaker", 30],
    ["Lancebreaker", 30],
    ["Rally Skill", 30],
    ["Rally Movement", 30],
    ["Rend Heaven", 30],
    ["Aether", 30],
    ["Demoiselle", 30],
    ["Gentilhomme", 30],
    ["Armored Blow", 30],
    ["Lifetaker", 30],
    ["Iron Will", 30],
    ["Clarity", 30],
    ["Veteran Intuition", 30],
    ["Fortunate Son", 30],
    ["Voice of Peace", 30],
    ["Potent Potion", 30],
    ["Skilltaker", 30],
    ["Lucktaker", 30],
    ["Resistancetaker", 30],
    ["Immobilize", 30],
    ["Seal Resistance", 30],
    ["Perspicacious", 30],
    ["Gallant", 30],
    ["Hoshidan Unity", 25],
    ["Nohrian Trust", 25],
    ["Pass", 25],
    ["Dual Guardsman", 25],
    ["Death Blow", 25],
    ["Duelist's Blow", 25],
    ["Live to Serve", 25],
    ["Poison Strike", 25],
    ["Grisly Wound", 25],
    ["Quick Salve", 25],
    ["Seal Defense", 25],
    ["Fancy Footwork", 25],
    ["In Extremis", 25],
    ["Healing Descant", 25],
    ["Draconic Heir", 25],
    ["Guarded Bravery", 25],
    ["Luna", 20],
    ["Ignis", 20],
    ["Armor Shield", 20],
    ["Resistance +2", 20],
    ["Toxic Brew", 20],
    ["Dragon Fang", 20],
    ["Vengeance", 20],
    ["Shove", 20],
    ["Swap", 20],
    ["Dual Striker", 20],
    ["Warding Blow", 20],
    ["Counter", 20],
    ["Countermagic", 20],
    ["Golembane", 20],
    ["Relief", 20],
    ["Camaraderie", 20],
    ["Even Keel", 20],
    ["Bloodthirst", 20],
    ["Morbid Celebration", 20],
    ["Aching Blood", 20],
    ["Perfect Pitch", 20],
    ["Optimistic", 20],
    ["Pragmatic", 20],
    ["Pride", 20],
    ["Fearsome Blow", 20],
    ["Make A Killing", 20],
    ["Wary Fighter", 10],
    ["Miracle", 10],
    ["Skill +2", 10],
    ["Luck +4", 10],
    ["Aegis", 10],
    ["Pavise", 10],
    ["Salvage Blow", 10],
    ["Profiteer", 10],
    ["Good Fortune", 10],
    ["Locktouch", 10],
    ["Nobility", 10],
    ["Inevitable End", 10],
    ["Natural Cover", 10],
    ["Seal Strength", 10],
    ["Seal Magic", 10],
    ["Unmask", 10],
    ["Bibliophile", 10],
    ["Forager", 10],
    ["Prodigy", 10],
    ["Shuriken Mastery", 10],
    ["Vendetta", 10],
    ["Countercurse", 10],
    ["Gamble", 5],
    ["Lethality", 5],
    ["Dragon Ward", 5],
    ["Future Sight", 5],
    ["Witch's Brew", 5],
    ["Solidarity", 5],
    ["Underdog", 5],
    ["Miraculous Save", 5],
    ["Misfortunate", 5],
    ["Goody Basket", 5],
    ["Triple Threat", 5],
    ["Daydream", 5],
    ["Fierce Rival", 5],
    ["Highwayman", 5],
    ["Mischievous", 5],
    ["Reciprocity", 5],
    ["Playthings", 5],
    ["Icy Blood", 5],
    ["Haiku", 5],
    ["Calm", 5],
    ["Divine Retribution", 5],
    ["Pyrotechnics", 5]
])

# These are the NAMES OF THE COLUMNS IN YOUR GOOGLE SHEETS. For example, the section of the submission where the name
# should be submitted is named "Name of Corrin (8 Characters Max)" on my end, but if your form has it named differently,
# edit these constants.
NAME = "Name of Corrin (8 Characters Max)"
GENDER = "Gender of Corrin"
BUILD = "Build"
FACE = "Face"
HAIRSTYLE = "Hairstyle"
HAIR_CLIP = "Hair Clip (F!Corrin Only) (0 means no clip)"
FACIAL_FEATURE = "Facial Feature (0 means no facial feature)"
VOICE = "Voice (1=Childish, 2=Neutral, 3=Mature)"
HAIR_COLOR = "Hair Color Hex values (Should be in RRGGBB format)"

BOON_BR = "Boon [Birthright]"
BANE_BR = "Bane [Birthright]"
BASE_CLASS_BR = "Base Class [Birthright]"
PROMOTED_CLASS_BR = "Promoted Class [Birthright]"
SKILLS_BR = "Skill Selection [Birthright]"

BOON_CQ = "Boon [Conquest]"
BANE_CQ = "Bane [Conquest]"
BASE_CLASS_CQ = "Base Class [Conquest]"
PROMOTED_CLASS_CQ = "Promoted Class [Conquest]"
SKILLS_CQ = "Skill Selection [Conquest]"

BOON_REV = "Boon [Revelation]"
BANE_REV = "Bane [Revelation]"
BASE_CLASS_REV = "Base Class [Revelation]"
PROMOTED_CLASS_REV = "Promoted Class [Revelation]"
SKILLS_REV = "Skill Selection [Revelation]"
