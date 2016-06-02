##
## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## 12monkeys "Modified Special Domestic Advisor"
## Based on "Special Domestic Advisor" from Requies (civfanatics)
## 
## Version 1.8d / 14.04.06
##
## Requirements : Civ4 patch 1.61
##

from CvPythonExtensions import *
# Needed for DomPyCity which inherits from PyCity
# (subclassed for additional functions)
import CvUtil
import ScreenInput
import CvScreenEnums
import UserPrefs

# Needed to check for non-numbers (specially search function)
import re

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# Debugging help
def debug (stuff):
	stuff = "SpecDomAdv: " + stuff
	CyInterface().addImmediateMessage(stuff,"")

class CvModSpecialDomesticAdvisor:
	"Modified Special Domestic Advisor Screen"

	# Called when cIV is first booted up and everytime you switch out of cIV
	def __init__(self):

### CONFIG SWITCHES - BEGIN ###
		#
		# True  : only buildings and wonders are displayed which can be constructed by the civ
		# False : always all buildings are displayed
		self.bShowOnlyAvailableBuildings = True
		#
		# True  : only a single sign with a factor is dispalyed. Like "x4" if you have 4 specialists in the city. Good for low screen resolutions
		# False : for each specialist a single sign is displayed
		self.bShowCompressedSpecialists = True
		#
		# True  : in world wonder nad team project screen, only information about known civs are displayed
		# False : in world wonder nad team project screen, information about all civs are displayed
		self.bShowKnownCivsOnly = True
### CONFIG SWITCHES - END ###

		self.runtimeInitDone = False

		self.NO_CITY = -1

		self.nTableX = 10   # Right/Left Margin
		self.nTableY = 70	# topmargin without header col (strange behavior of the table, btw)

		self.nPlusOffsetX = -4
		self.nMinusOffsetX = 16
		self.nPlusOffsetY = self.nMinusOffsetY = 30
		self.nPlusWidth = self.nPlusHeight = self.nMinusWidth = self.nMinusHeight = 20

		self.nSpecTextOffsetX = 0
		self.nSpecTextOffsetY = 50

		# view names
		self.DEF_AREA_NAME = "DefaultListBackground"
		self.SPEC_AREA_NAME = "SpecialListBackground"
		self.MIL_AREA_NAME = "MilitaryListBackground"
		self.BUILD_AREA_NAME = "BuildListBackground"
		self.WW_AREA_NAME = "WWListBackground"
		self.NW_AREA_NAME = "NWListBackground"
		self.TW_AREA_NAME = "TWListBackground"

		# control button names
		self.REDRAW_NAME = "DomesticRedraw"
		self.EXIT_NAME = "DomesticExit"
		self.BUILD_NAME = "DomesticBuild"
		self.WW_NAME = "DomesticWW"
		self.NW_NAME = "DomesticNW"
		self.TW_NAME = "DomesticTW"
		self.CITY_NAME = "DomesticCity"
		self.SPEC_NAME = "DomesticSpec"
		self.MIL_NAME = "DomesticMilitary"
		self.BACKGROUND_ID = "DomesticAdvisorBG"

		# cukture text names
		self.CULTURE_TEXT_NAME = "DomCultureText"
		self.GP_TEXT_NAME = "DomGPText"
		self.NUMBER_TEXT = "NUM"

		# specialists button names
		self.SPECIALIST_IMAGE_NAME = "DomCitizenImage"
		self.SPECIALIST_PLUS_NAME = "DomIncreaseSpecialist"
		self.SPECIALIST_MINUS_NAME = "DomDecreaseSpecialist"
		self.SPECIALIST_TEXT_NAME = "DomSpecialistText"

		# build button names
		self.BUILD_BUTTON_NAME = "DomBuildButtonName"
		self.BUILD_BUTTON_LEFT = "DomBuildButtonLeftName"
		self.BUILD_BUTTON_RIGHT = "DomBuildButtonRightName"

		# help item names
		self.HELP_BUTTON_NAME = "DomHelpButtonName"
		self.HELP_TEXT_NAME = "HELP_TEXT"
		self.HELP_BACKGROUND_ID = "DomesticAdvisorHelpBG"
		self.HELP_TEXT_ID = "HELP_TEXT_ID"

		self.m_nChosenCity = self.NO_CITY
		self.m_szMode = self.DEF_AREA_NAME
		self.m_bSpecialistChange = False
		self.m_nSpecialistChangeNumber = 0
		self.m_nLastSpecialistChange = 0

		self.CreateViewLists()

		# Values to check to see if we need to color the number
		self.PROBLEM_VALUES_DICT = {
			"GARRISON" : 0,
			"HAPPY" : -1,
			"HEALTH" : -1,
			"GROWTH" : -1,
			"FOOD" : -1,
			"PRODUCTION" : 0,
			"DEFENSE_TOTAL" : 0,
			"UNITS_MIL_GROUND_NUM" : 0,
			"UNITS_MIL_AIR_DEFENSE_NUM" : 0,
			"UNITS_MIL_AIR_PATROL" : 0,
		}

		# Values to check to see if we need to color the number as neutral
		self.NEUTRAL_VALUES_DICT = {
			"HAPPY" : 0,
			"HEALTH" : 0,
			"GROWTH" : 0,
			"FOOD" : 0,
			"UNITS_MIL_GROUND_NUM" : 1,
			}

		# Values to check to see if we need to color the number as great
		self.GREAT_VALUES_DICT = {
			"HAPPY" : 6,
			"HEALTH" : 6,
			"FOOD" : 6,
			"DEFENSE_DAMAGE" : 0,
			"DEFENSE_TOTAL" : 100,
			"UNITS_MIL_GROUND_NUM" : 3,
			"UNITS_MIL_AIR_DEFENSE_NUM" : 3,
			"UNITS_MIL_AIR_PATROL" : 3,
			}

		# Dictionary of the coloring dictionaries!
		self.COLOR_DICT_DICT = {
			"PROBLEM": self.PROBLEM_VALUES_DICT,
			"NEUTRAL": self.NEUTRAL_VALUES_DICT,
			"GREAT": self.GREAT_VALUES_DICT,
			}

		# This creates the set of ALL coloring keys.
		# Do NOT touch.
		self.COLOR_SET = set()
		for clDict in self.COLOR_DICT_DICT.values():
			self.COLOR_SET.update(clDict.keys())

		# Values to change on an update
		# (True indicates update when we DON'T switch to/from food production)
		# Most of this MIGHT change because the computer might be switching
		# plots it's working or creating/removing specialists.

		# TODO: Unfortunately, right now, we have no way of knowing when it's
		# switching from food production to non-food production and vice versa.
		self.UPDATE_DICT = {
			"HAPPY": True,
			"GROWTH" : False,
			"FOOD": False,
			"PRODUCTION": True,
			"COMMERCE": False,
			"GOLD": True,
			"RESEARCH": True,
			"CULTURE_RATE": True,
			"GREATPEOPLE_RATE": False,
			"PRODUCING": True,
			"SPECIALISTS": False,
			"ESPIONAGE": True,
			"AUTOMATION": True
			}

		self.HEADER_DICT = None
		self.JUSTIFY_DICT = None
		self.HELP_DICT = None
		self.AUTOMATION_ICON_DICT = None
		self.COLOR_DICT = None
		self.CITY_PRODUCING_DICT = {}

		# Input handling functions
		self.DomesticScreenInputMap = {
			self.SPEC_NAME				: self.Spec,
			self.SPECIALIST_PLUS_NAME	: self.HandleSpecialistPlus,
			self.SPECIALIST_MINUS_NAME	: self.HandleSpecialistMinus,
			self.EXIT_NAME				: self.DomesticExit,
			self.REDRAW_NAME			: self.Redraw,
			self.BUILD_NAME				: self.Build,
			self.WW_NAME				: self.WW,
			self.NW_NAME				: self.NW,
			self.TW_NAME				: self.TW,
			self.BUILD_BUTTON_LEFT		: self.BuildLeft,
			self.BUILD_BUTTON_RIGHT		: self.BuildRight,
			self.CITY_NAME				: self.City,
			self.MIL_NAME				: self.Mil,
			}

		self.lBuildings = None
		self.lWW = None
		self.lNW = None
		self.lTW = None

	def CreateViewLists(self):
		# View definitions:
		#
		#  the "Column Name" is the unique key which handles the content of the column
		#  the "Width" defines the width as a relative value. The absolute value is calculated by the current screen resolution.
		#  the order the values are defined is the order they are displayed in the table.
		#  the Views for buildings, wonders and projects could not be changed, they are hardcoded.
		#  For Header and Justify definitions, look in the procedure "SetConstants"
		#  
		#  To add or remove a line, just comment is in or out and adjust the width.
		#  column "BUTTON" and "NAME" should always be he first two columns in the given order, so please done touch them. Of cause, you can resize them.
		#
		self.DEF_VIEW_LIST = [
			# Columns Name				Width
			("BUTTON", 					25.0),
			("NAME",					90.0),
			("LANDMARKS", 				80.0),
			("POPULATION", 				38.0),
			("HAPPY", 					38.0),
			("HEALTH", 					38.0),
			("GROWTH", 					38.0),
			("FOOD", 					38.0),
			("PRODUCTION", 				41.0),
			("MAINTENANCE", 			38.0),
			("MAINTENANCE_DISTANCE",	38.0),
			("TRADE", 					38.0),
			("COMMERCE", 				38.0),
			("GOLD", 					38.0),
			("RESEARCH", 				38.0),
			("ESPIONAGE", 				38.0),
			("CULTURE_RATE", 			38.0),
			("CULTURE", 				50.0),
			("GREATPEOPLE_RATE", 		38.0),
			("GREATPEOPLE", 			42.0),
			("PRODUCING", 				110.0),
			("TURNS", 					38.0),
			]
		self.DEF_VIEW_COLS_SIZE = 0

		self.SPEC_VIEW_LIST = [
			# Columns Name			Width
			("BUTTON", 				25.0),
			("NAME",				90.0),
			("AUTOMATION",			110.0),
			("SPECIALISTS",			132.0),
			("RELIGIONS",			105.0),
			("CORPORATIONS",		105.0),
			("HAPPY",				38.0),
			("GROWTH",				38.0),
			("FOOD",				38.0),
			("PRODUCTION",			38.0),
			("GOLD",				38.0),
			("RESEARCH",			38.0),
			("CULTURE_RATE",		38.0),
			("GREATPEOPLE_RATE",	38.0),
			("PRODUCING",			100.0),
			("TURNS",				38.0),
			]
		self.SPEC_VIEW_COLS_SIZE = 0

		self.MIL_VIEW_LIST = [
			# Columns Name						Width
			("BUTTON",							15.0),
			("NAME",							70.0),
			("THREATS",							15.0),
			("DISORDER",						30.0),
			("NO_MILITARY_ANGER",				20.0),
			("WAR_WEARINESS",					22.0),
			("FREE_EXPERIENCE",					40.0),
			("COASTAL",							15.0),
			("CONSCRIPT_UNIT",					55.0),
			("DEFENSE_VIS",						30.0),
			("DEFENSE_DAMAGE",					25.0),
			("DEFENSE_TOTAL",					20.0),
			("UNITS_TOTAL_NUM",					20.0),
			("UNITS_MIL_NUM",					20.0),
			("UNITS_MIL_GROUND_NUM",			20.0),
			("UNITS_MIL_SEA_NUM",				20.0),
			("UNITS_MIL_AIR_NUM",				20.0),
			("UNITS_MIL_GROUND_DEFENSE_SUM",	25.0),
			("UNITS_MIL_GROUND_DEFENSE_AVG",	25.0),
			("UNITS_MIL_AIR_DEFENSE_NUM",		20.0),
			("UNITS_MIL_AIR_DEFENSE_AVG",		25.0),
			("UNITS_MIL_AIR_PATROL",			20.0),
		]
		self.MIL_VIEW_COLS_SIZE = 0

	def SetHeaderDict(self):
		# Header Information (Must be here, because C++ functions aren't
		# available upon startup of CIV)
		self.HEADER_DICT = {
			"BUTTON" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BUTTON", ()),
			"NAME" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_NAME", ()),
			"DATE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_FOUNDED", ()),
			"LANDMARKS" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_LANDMARKS", ()),
			"POPULATION" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_POPULATION", ()),
			"POPULATION_REAL": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_POPULATION_REAL", ()),
			"GARRISON" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GARRISON", ()) % self.militaryIcon,
			"HAPPY" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_HAPPY", ()) % self.happyIcon,
			"BASE_HAPPY": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_HAPPY", ()) % self.happyIcon,
			"BASE_UNHAPPY": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_UNHAPPY", ()) %  self.unhappyIcon,
			"HEALTH" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_HEALTH", ()) % self.healthIcon,
			"BASE_GOODHEALTH": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_GOODHEALTH", ()) % self.healthIcon,
			"BASE_BADHEALTH": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_BADHEALTH", ()) % self.sickIcon,
			"GROWTH" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GROWTH", ()) % self.redfoodIcon,
			"FOOD" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_FOOD", ()) % self.foodIcon,
			"FOOD_STORED" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_FOOD_STORED", ()) % self.foodIcon,
			"BASE_FOOD": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_FOOD", ()) % self.foodIcon,
			"PRODUCTION" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_PRODUCTION", ()) % self.hammerIcon,
			"BASE_PRODUCTION": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_PRODUCTION", ()) % self.hammerIcon,
			"MAINTENANCE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_MAINTENANCE", ()) % self.badGoldIcon,
			"MAINTENANCE_DISTANCE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_MAINTENANCE_DISTANCE", ()) % self.badGoldIcon,
			"MAINTENANCE_NUMCITIES" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_MAINTENANCE_NUMCITIES", ()) % self.badGoldIcon,
			"TRADE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_TRADE", ()) % self.tradeIcon,
			"COMMERCE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_COMMERCE", ()) % self.commerceIcon,
			"GOLD" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GOLD", ()) % self.goldIcon,
			"RESEARCH" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_RESEARCH", ()) % self.researchIcon,
			"CULTURE_RATE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_CULTURE_RATE", ()) % self.cultureIcon,
			"CULTURE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_CULTURE", ()) % self.cultureIcon,
			"GREATPEOPLE_RATE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GREATPEOPLE_RATE", ()) % self.figureheadIcon,
			"GREATPEOPLE" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GREATPEOPLE", ()) % self.figureheadIcon,
			"GREATPEOPLE_TURNS" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_GREATPEOPLE_TURNS", ()) % self.figureheadIcon,
			"GREATGENERAL" : "<img=" + gc.getUnitInfo(gc.getInfoTypeForString("UNIT_GREAT_GENERAL")).getButton() + " size=20></img>",
			"PRODUCING" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_PRODUCING", ()),
			"TURNS" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_TURNS", ()),
			"RELIGIONS" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_RELIGIONS", ()),
			"SPECIALISTS" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_SPECIALISTS", ()),
			"AUTOMATION" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_AUTOMATION", ()),
			"DEFENSE_VIS": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_DEFENSE_VIS", ()) % self.defenseIcon,
			"DEFENSE_DAMAGE": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_DEFENSE_DAMAGE", ()) % self.defenseIcon,
			"DEFENSE_TOTAL": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_DEFENSE_TOTAL", ()) % self.defenseIcon,
			"CONSCRIPT": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_CONSCRIPT", ()),
			"CONSCRIPT_UNIT": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_CONSCRIPT_UNIT", ()),
			"POWER": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_POWER", ()) % self.powerIcon,
			"THREATS": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_THREATS", ()),
			"DISORDER": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_DISORDER", ()),
			"NO_MILITARY_ANGER": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_NO_MILITARY_ANGER", ()),
			"WAR_WEARINESS": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_WAR_WEARINESS", ()),
			"FREE_EXPERIENCE": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_FREE_EXPERIENCE", ()),
			"COASTAL": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_COASTAL", ()),
			"UNITS_TOTAL_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_TOTAL_NUM", ()),
			"UNITS_MIL_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_NUM", ()),
			"UNITS_MIL_GROUND_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_GROUND_NUM", ()),
			"UNITS_MIL_SEA_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_SEA_NUM", ()),
			"UNITS_MIL_AIR_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_AIR_NUM", ()),
			"UNITS_MIL_GROUND_DEFENSE_SUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_GROUND_DEFENSE_SUM", ()),
			"UNITS_MIL_GROUND_DEFENSE_AVG": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_GROUND_DEFENSE_AVG", ()),
			"UNITS_MIL_AIR_DEFENSE_NUM": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_AIR_DEFENSE_NUM", ()),
			"UNITS_MIL_AIR_DEFENSE_AVG": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_AIR_DEFENSE_AVG", ()),
			"UNITS_MIL_AIR_PATROL": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_UNITS_MIL_AIR_PATROL", ()),
			"ESPIONAGE": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_ESPIONAGE", ()) % self.espionageIcon,
			"CORPORATIONS": localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_CORPORATIONS", ()),
			"BASE_GOLD" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_GOLD", ()) % self.goldIcon,
			"BASE_RESEARCH" : localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BASE_RESEARCH", ()) % self.researchIcon,
		}

	def SetJustifyDict(self):
		# Header Information (Must be here, because C++ functions aren't
		# available upon startup of CIV)
		self.JUSTIFY_DICT = {
			"BUTTON" : CvUtil.FONT_CENTER_JUSTIFY,
			"NAME" : CvUtil.FONT_LEFT_JUSTIFY,
			"DATE" : CvUtil.FONT_LEFT_JUSTIFY, 
			"LANDMARKS" : CvUtil.FONT_LEFT_JUSTIFY,
			"POPULATION" : CvUtil.FONT_RIGHT_JUSTIFY,
			"POPULATION_REAL": CvUtil.FONT_RIGHT_JUSTIFY,
			"GARRISON" : CvUtil.FONT_RIGHT_JUSTIFY,
			"HAPPY" : CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_HAPPY": CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_UNHAPPY": CvUtil.FONT_RIGHT_JUSTIFY,
			"HEALTH" : CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_GOODHEALTH": CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_BADHEALTH": CvUtil.FONT_RIGHT_JUSTIFY,
			"GROWTH" : CvUtil.FONT_RIGHT_JUSTIFY,
			"FOOD" : CvUtil.FONT_RIGHT_JUSTIFY,
			"FOOD_STORED" : CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_FOOD": CvUtil.FONT_RIGHT_JUSTIFY,
			"PRODUCTION" : CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_PRODUCTION": CvUtil.FONT_RIGHT_JUSTIFY,
			"MAINTENANCE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"MAINTENANCE_DISTANCE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"MAINTENANCE_NUMCITIES" : CvUtil.FONT_RIGHT_JUSTIFY,
			"TRADE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"COMMERCE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"GOLD" : CvUtil.FONT_RIGHT_JUSTIFY,
			"RESEARCH" : CvUtil.FONT_RIGHT_JUSTIFY,
			"CULTURE_RATE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"CULTURE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"GREATPEOPLE_RATE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"GREATPEOPLE" : CvUtil.FONT_RIGHT_JUSTIFY,
			"GREATPEOPLE_TURNS" : CvUtil.FONT_RIGHT_JUSTIFY,
			"PRODUCING" : CvUtil.FONT_LEFT_JUSTIFY,
			"TURNS" : CvUtil.FONT_RIGHT_JUSTIFY,
			"RELIGIONS" : CvUtil.FONT_LEFT_JUSTIFY,
			"SPECIALISTS" : CvUtil.FONT_LEFT_JUSTIFY,
			"AUTOMATION" : CvUtil.FONT_LEFT_JUSTIFY,
			"DEFENSE_VIS": CvUtil.FONT_RIGHT_JUSTIFY,
			"DEFENSE_DAMAGE": CvUtil.FONT_RIGHT_JUSTIFY,
			"DEFENSE_TOTAL": CvUtil.FONT_RIGHT_JUSTIFY,
			"CONSCRIPT": CvUtil.FONT_RIGHT_JUSTIFY,
			"CONSCRIPT_UNIT": CvUtil.FONT_LEFT_JUSTIFY,
			"POWER": CvUtil.FONT_CENTER_JUSTIFY,
			"THREATS": CvUtil.FONT_CENTER_JUSTIFY,
			"DISORDER": CvUtil.FONT_CENTER_JUSTIFY,
			"NO_MILITARY_ANGER": CvUtil.FONT_RIGHT_JUSTIFY,
			"WAR_WEARINESS": CvUtil.FONT_RIGHT_JUSTIFY,
			"FREE_EXPERIENCE": CvUtil.FONT_RIGHT_JUSTIFY,
			"COASTAL": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_TOTAL_NUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_NUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_GROUND_NUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_SEA_NUM": CvUtil.FONT_RIGHT_JUSTIFY, 
			"UNITS_MIL_AIR_NUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_GROUND_DEFENSE_SUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_GROUND_DEFENSE_AVG": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_AIR_DEFENSE_NUM": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_AIR_DEFENSE_AVG": CvUtil.FONT_RIGHT_JUSTIFY,
			"UNITS_MIL_AIR_PATROL": CvUtil.FONT_RIGHT_JUSTIFY,
			"ESPIONAGE": CvUtil.FONT_RIGHT_JUSTIFY,
			"CORPORATIONS": CvUtil.FONT_LEFT_JUSTIFY,
			"BASE_GOLD" : CvUtil.FONT_RIGHT_JUSTIFY,
			"BASE_RESEARCH" : CvUtil.FONT_RIGHT_JUSTIFY,
		}

	def SetHelpDict(self):
		self.HELP_DICT = {  
			"BUTTON" : localText.getText("TXT_KEY_DOM_ADV_HELP_BUTTON", ()),
			"NAME" : localText.getText("TXT_KEY_DOM_ADV_HELP_NAME", ())%(self.occupationIcon),
			"DATE" : localText.getText("TXT_KEY_DOM_ADV_HELP_DATE", ()),
			"LANDMARKS" : localText.getText("TXT_KEY_DOM_ADV_HELP_LANDMARKS", ()) % (self.starIcon, self.silverStarIcon, self.bulletIcon, self.powerIcon, self.angryIcon, self.occupationIcon, self.tradeIcon),
			"POPULATION" : localText.getText("TXT_KEY_DOM_ADV_HELP_POPULATION", ()), 
			"POPULATION_REAL": localText.getText("TXT_KEY_DOM_ADV_HELP_POPULATION_REAL", ()),
			"GARRISON" : localText.getText("TXT_KEY_DOM_ADV_HELP_GARRISON", ()),
			"HAPPY" : localText.getText("TXT_KEY_DOM_ADV_HELP_HAPPY", ()),
			"BASE_HAPPY": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_HAPPY", ()), 
			"BASE_UNHAPPY": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_UNHAPPY", ()), 
			"HEALTH" : localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_HEALTH", ()),
			"BASE_GOODHEALTH": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_GOODHEALTH", ()), 
			"BASE_BADHEALTH": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_BADHEALTH", ()), 
			"GROWTH" : localText.getText("TXT_KEY_DOM_ADV_HELP_GROWTH", ()), 
			"FOOD" : localText.getText("TXT_KEY_DOM_ADV_HELP_FOOD", ()), 
			"FOOD_STORED" : localText.getText("TXT_KEY_DOM_ADV_HELP_FOOD_STORED", ()),
			"BASE_FOOD": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_FOOD", ()),
			"PRODUCTION" : localText.getText("TXT_KEY_DOM_ADV_HELP_PRODUCTION", ()),
			"BASE_PRODUCTION": localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_PRODUCTION", ()),
			"MAINTENANCE" : localText.getText("TXT_KEY_DOM_ADV_HELP_MAINTENANCE", ()),
			"MAINTENANCE_DISTANCE" : localText.getText("TXT_KEY_DOM_ADV_HELP_MAINTENANCE_DISTANCE", ()),
			"MAINTENANCE_NUMCITIES" : localText.getText("TXT_KEY_DOM_ADV_HELP_MAINTENANCE_NUMCITIES", ()),
			"TRADE" : localText.getText("TXT_KEY_DOM_ADV_HELP_TRADE", ()),
			"COMMERCE" : localText.getText("TXT_KEY_DOM_ADV_HELP_COMMERCE", ()),
			"GOLD" : localText.getText("TXT_KEY_DOM_ADV_HELP_GOLD", ()),
			"RESEARCH" : localText.getText("TXT_KEY_DOM_ADV_HELP_RESEARCH", ()),
			"CULTURE_RATE" : localText.getText("TXT_KEY_DOM_ADV_HELP_CULTURE_RATE", ()),
			"CULTURE" :  localText.getText("TXT_KEY_DOM_ADV_HELP_CULTURE", ()),
			"GREATPEOPLE_RATE" : localText.getText("TXT_KEY_DOM_ADV_HELP_GREATPEOPLE_RATE", ()),
			"GREATPEOPLE" : localText.getText("TXT_KEY_DOM_ADV_HELP_GREATPEOPLE", ()),
			"GREATPEOPLE_TURNS" : localText.getText("TXT_KEY_DOM_ADV_HELP_GREATPEOPLE_TURNS", ()),
			"PRODUCING" : localText.getText("TXT_KEY_DOM_ADV_HELP_PRODUCING", ()),
			"TURNS" : localText.getText("TXT_KEY_DOM_ADV_HELP_TURNS", ()),
			"RELIGIONS" : localText.getText("TXT_KEY_DOM_ADV_HELP_RELIGIONS", ()),
			"SPECIALISTS" : localText.getText("TXT_KEY_DOM_ADV_HELP_SPECIALISTS", ()),
			"AUTOMATION" : localText.getText("TXT_KEY_DOM_ADV_HELP_AUTOMATION", ()) % (self.CITIZENS_AUTOMATED_ICON, self.PRODUCTION_AUTOMATED_ICON, self.AUTOMATION_ICON_DICT[0], self.AUTOMATION_ICON_DICT[1], self.AUTOMATION_ICON_DICT[2], self.AUTOMATION_ICON_DICT[3], self.AUTOMATION_ICON_DICT[4], self.AUTOMATION_ICON_DICT[5]),
			"DEFENSE_VIS": localText.getText("TXT_KEY_DOM_ADV_HELP_DEFENSE_VIS", ()),
			"DEFENSE_DAMAGE": localText.getText("TXT_KEY_DOM_ADV_HELP_DEFENSE_DAMAGE", ()),
			"DEFENSE_TOTAL": localText.getText("TXT_KEY_DOM_ADV_HELP_DEFENSE_TOTAL", ()),
			"CONSCRIPT": localText.getText("TXT_KEY_DOM_ADV_HELP_CONSCRIPT", ()),
			"CONSCRIPT_UNIT":  localText.getText("TXT_KEY_DOM_ADV_HELP_CONSCRIPT_UNIT", ()),
			"POWER": localText.getText("TXT_KEY_DOM_ADV_HELP_POWER", ()) % self.powerIcon,
			"THREATS": localText.getText("TXT_KEY_DOM_ADV_HELP_THREATS", ()) % self.angryIcon,
			"DISORDER": localText.getText("TXT_KEY_DOM_ADV_HELP_DISORDER", ()) % (self.occupationIcon, self.angryIcon ),
			"NO_MILITARY_ANGER": localText.getText("TXT_KEY_DOM_ADV_HELP_NO_MILITARY_ANGER", ()) % (self.happyIcon, self.unhappyIcon ),
			"WAR_WEARINESS": localText.getText("TXT_KEY_DOM_ADV_HELP_WAR_WEARINESS", ()),
			"FREE_EXPERIENCE": localText.getText("TXT_KEY_DOM_ADV_HELP_FREE_EXPERIENCE", ()),
			"COASTAL": localText.getText("TXT_KEY_DOM_ADV_HELP_COASTAL", ()),
			"UNITS_TOTAL_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_TOTAL_NUM", ()),
			"UNITS_MIL_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_NUM", ()),
			"UNITS_MIL_GROUND_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_GROUND_NUM", ()),
			"UNITS_MIL_SEA_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_SEA_NUM", ()),
			"UNITS_MIL_AIR_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_AIR_NUM", ()),
			"UNITS_MIL_GROUND_DEFENSE_SUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_GROUND_DEFENSE_SUM", ()),
			"UNITS_MIL_GROUND_DEFENSE_AVG": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_GROUND_DEFENSE_AVG", ()),
			"UNITS_MIL_AIR_DEFENSE_NUM": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_AIR_DEFENSE_NUM", ()),
			"UNITS_MIL_AIR_DEFENSE_AVG": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_AIR_DEFENSE_AVG", ()),
			"UNITS_MIL_AIR_PATROL": localText.getText("TXT_KEY_DOM_ADV_HELP_UNITS_MIL_AIR_PATROL", ()),
			"ESPIONAGE": localText.getText("TXT_KEY_DOM_ADV_HELP_ESPIONAGE", ()),
			"CORPORATIONS": localText.getText("TXT_KEY_DOM_ADV_HELP_CORPORATIONS", ()),
			"BASE_GOLD" : localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_GOLD", ()),
			"BASE_RESEARCH" : localText.getText("TXT_KEY_DOM_ADV_HELP_BASE_RESEARCH", ()),
		}

	def SetConstants(self):

		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		if (self.runtimeInitDone) and (self.nScreenWidth == (screen.getXResolution() - 10)) and (self.nScreenLength == (screen.getYResolution() - 250)):
			return

		## screen sizes
		self.nScreenWidth = screen.getXResolution() - 10
		self.nScreenLength = screen.getYResolution() -250

		## table sizes
		self.nTableWidth = self.nScreenWidth - (2 * self.nTableX)
		self.nTableLength = self.nScreenLength - 230#250

		## culture level legend
		self.nCultureLevelX = self.nScreenWidth - 300	# x-coord of text legend
		self.nCultureLevelY = self.nScreenLength - 150	# y-coord of text legend
		self.nCultureLevelDistance = 13		# y spacing of texts
		self.nCultureLevelTextOffset = 150	# x spacing between level texts and level points

		## great person 
		self.nGPLevelX = self.nScreenWidth - 50	# x-coord
		self.nGPLevelY = self.nScreenLength - 150	# y-coord
		self.nGPLevelDistance = 26 # x spacing between  texts and points

		## specialists area in specialist view
		self.nFirstSpecialistX = 30	# x-coord
		self.nSpecialistY = self.nScreenLength - 150	# y-coord
		self.nSpecialistWidth = 32
		self.nSpecialistLength = 32
		self.nSpecialistDistance = 70

		## great person 
		self.nFreeColonyX = self.nScreenWidth - 40	# x-coord
		self.nFreeColonyY = self.nScreenLength - 82	# y-coord

		## selection button positions
		# thats what I called the "smart-button-spacing" ;D
		# it takes care that all buttons have the same space between, so that there are no overlaps
		self.buttonTextMilitary = localText.getText("TXT_KEY_DOM_ADV_WORLD_MILITARY_VIEW", ())
		self.buttonTextProjects = localText.getText("TXT_KEY_DOM_ADV_TEAM_PROJECTS_VIEW", ())
		self.buttonTextWorldWonders = localText.getText("TXT_KEY_DOM_ADV_WORLD_WONDERS_VIEW", ())
		self.buttonTextNationalWonders = localText.getText("TXT_KEY_DOM_ADV_NATIONAL_WONDERS_VIEW", ())
		self.buttonTextBuildings = localText.getText("TXT_KEY_DOM_ADV_BUILDINGS_VIEW", ())
		self.buttonTextExit = localText.getText("TXT_KEY_DOM_ADV_SCREEN_EXIT", ())
		self.buttonTextSpecialists = localText.getText("TXT_KEY_DOM_ADV_SPECIALISTS_VIEW", ())
		self.buttonTextCity = localText.getText("TXT_KEY_DOM_ADV_CITY_VIEW", ())
		self.buttonTextRedraw = localText.getText("TXT_KEY_DOM_ADV_REDRAW", ())

		self.Button_List = [
			(self.buttonTextExit, 0),
			(self.buttonTextRedraw, 0),
			(self.buttonTextProjects, 0),
			(self.buttonTextNationalWonders, 0),
			(self.buttonTextWorldWonders, 0),
			(self.buttonTextBuildings, 0),
			(self.buttonTextMilitary, 0),
			(self.buttonTextSpecialists, 0),
			(self.buttonTextCity, 0),
		]

		# looking how much characters all button texts have in sum
		iLen = 0
		for i in range(len(self.Button_List)):
			iLen += len(self.Button_List[i][0])

		# the average width of a character in pixels. ( I hope they never changed the font ;) )
		avgPixPerChar = 8
		# calculating the space between two buttons in pixel 
		nButtonSpace = (self.nScreenWidth-iLen*avgPixPerChar)//len(self.Button_List)

		# getting some space on the left and right
		x = nButtonSpace//2
		for i in xrange(len(self.Button_List)):
			self.Button_List[i] = (self.Button_List[i][0], self.nScreenWidth-x)
			x += len(self.Button_List[i][0])*avgPixPerChar+nButtonSpace

		# y position of the buttons
		self.nButtonsY = self.nScreenLength - 47

		## column sizes for building/wonder screen
		self.BUILD_BUTTON_COL_SIZE = int(25.0)
		self.BUILD_NAME_COL_SIZE = int(110.0/1000*self.nTableWidth)
		self.BUILD_TURNS_COL_SIZE = int(40.0/1000*self.nTableWidth)
		self.BUILD_OUTPUT_COL_SIZE = 40

		## building / wonder buttons (pedia buttons) size and position
		## number of pedia buttons and table columns per screen
		self.BUILD_BUTTON_SIZE 		= float(self.nTableY/2.0)
		self.BUILD_NUM_COLS 		= int(float(self.nTableWidth - 15 - self.BUILD_BUTTON_COL_SIZE - self.BUILD_NAME_COL_SIZE - self.BUILD_TURNS_COL_SIZE - self.BUILD_OUTPUT_COL_SIZE*3) / float(self.BUILD_BUTTON_SIZE) )

		## x-step of pedia button
		self.BUILD_BUTTON_X_STEP 	= int(self.BUILD_BUTTON_SIZE)

		## size of pedia buttons
		self.BUILD_BUTTON_X_SIZE 	= int(self.BUILD_BUTTON_SIZE-2)
		self.BUILD_BUTTON_Y_SIZE 	= self.BUILD_BUTTON_X_SIZE

		## position of pedia buttons
		self.BUILD_BUTTON_X_OFFSET 	= int(self.nTableX+self.BUILD_BUTTON_COL_SIZE+self.BUILD_NAME_COL_SIZE)
		self.BUILD_BUTTON_Y_OFFSET 	= int(self.BUILD_BUTTON_SIZE)  + 2#int(self.nTableY-10-self.BUILD_BUTTON_SIZE)

		## building / wonder left/right button data
		self.BUILD_BUTTON_LEFT_X 	= 50
		self.BUILD_BUTTON_RIGHT_X 	= 80
		self.BUILD_BUTTON_LR_Y_OFFSET = self.BUILD_BUTTON_Y_OFFSET
		self.BUILD_BUTTON_LR_X_SIZE = 40
		self.BUILD_BUTTON_LR_Y_SIZE = 40

		self.BUILD_FROM_COL 		= 0
		self.BUILD_TO_COL 			= self.BUILD_FROM_COL + self.BUILD_NUM_COLS - 1
		self.WW_FROM_COL 			= 0
		self.WW_TO_COL 				= self.WW_FROM_COL + self.BUILD_NUM_COLS - 1
		self.NW_FROM_COL 			= 0
		self.NW_TO_COL 				= self.NW_FROM_COL + self.BUILD_NUM_COLS - 1
		self.TW_FROM_COL 			= 0
		self.TW_TO_COL 				= self.TW_FROM_COL + self.BUILD_NUM_COLS - 1

		## Help Buttons
		self.HELP_BUTTON_X_OFFSET	= 10
		self.HELP_BUTTON_Y_OFFSET	= self.BUILD_BUTTON_Y_OFFSET+10
		self.HELP_BUTTON_X_SIZE		= 20
		self.HELP_BUTTON_Y_SIZE		= 20
		## Help button location for Building/Wonder screens
		self.HELP_BUTTON_PAGE_X		= self.nTableX
		self.HELP_BUTTON_PAGE_Y		= self.HELP_BUTTON_Y_OFFSET

		self.HELP_PANEL_X			= 0
		self.HELP_PANEL_Y			= self.HELP_BUTTON_Y_OFFSET+25
		self.HELP_PANEL_X_SIZE		= 400
		self.HELP_PANEL_PIX_PER_LINE  = 18
		self.HELP_CHAR_PER_LINE		= 60

		# Calculate some view list parameters
		if self.DEF_VIEW_COLS_SIZE == 0:
			for i in xrange(len(self.DEF_VIEW_LIST)):
				self.DEF_VIEW_COLS_SIZE += self.DEF_VIEW_LIST[i][1]

		if self.SPEC_VIEW_COLS_SIZE == 0:
			for i in xrange(len(self.SPEC_VIEW_LIST)):
				self.SPEC_VIEW_COLS_SIZE += self.SPEC_VIEW_LIST[i][1]

		if self.MIL_VIEW_COLS_SIZE == 0:
			for i in xrange(len(self.MIL_VIEW_LIST)):
				self.MIL_VIEW_COLS_SIZE += self.MIL_VIEW_LIST[i][1]

		# define special symbols
		self.angryIcon = u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR)
		self.defenseIcon = u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR)
		self.foodIcon = u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()
		self.redfoodIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BAD_FOOD_CHAR)
		self.goldIcon = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()
		self.badGoldIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BAD_GOLD_CHAR)
		self.figureheadIcon = u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)
		self.hammerIcon = u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
		self.happyIcon = u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)
		self.unhappyIcon = u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)
		self.healthIcon = u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)
		self.sickIcon = u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR)
		self.lawIcon = u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR)
		self.occupationIcon = u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
		self.militaryIcon = u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
		self.powerIcon = u"%c" % CyGame().getSymbolID(FontSymbols.POWER_CHAR)
		self.commerceIcon = u"%c" % gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()
		self.cultureIcon = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()
		self.researchIcon = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()
		self.tradeIcon = u"%c" % CyGame().getSymbolID(FontSymbols.TRADE_CHAR)
		self.starIcon = u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
		self.silverStarIcon = u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
		self.bulletIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		self.espionageIcon = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar()

		# Special symbols for building, wonder and project views
		self.objectUnderConstruction = self.hammerIcon

		# add the colors dependant on the statuses
		self.objectHave = localText.changeTextColor("x", gc.getInfoTypeForString("COLOR_GREEN")) #"+"
		self.objectNotPossible = localText.changeTextColor("-", gc.getInfoTypeForString("COLOR_RED")) #"-"
		self.objectPossible = localText.changeTextColor("o", gc.getInfoTypeForString("COLOR_BLUE")) #"o"
		self.objectHaveObsolete = localText.changeTextColor("x", gc.getInfoTypeForString("COLOR_WHITE")) #"+"
		self.objectNotPossibleConcurrent = localText.changeTextColor("-", gc.getInfoTypeForString("COLOR_YELLOW")) #"-"
		self.objectPossibleConcurrent = localText.changeTextColor("o", gc.getInfoTypeForString("COLOR_YELLOW")) #"o"

		# set texts for True and False values
		self.textTRUE = localText.getText("TXT_KEY_DOM_ADV_MISC_TRUE", ())
		self.textFALSE = localText.getText("TXT_KEY_DOM_ADV_MISC_FALSE", ())

		if self.AUTOMATION_ICON_DICT == None:
			# Header Information (Must be here, because C++ functions aren't available upon startup of CIV)
			self.AUTOMATION_ICON_DICT = {
				0 : self.foodIcon, # Emphasize Food
				1 : self.hammerIcon, # Emphasize Production
				2 : self.goldIcon, # Emphasize Gold?
				3 : self.researchIcon, # Emphasize Research
				4 : self.figureheadIcon, # Emphasize GP
				5 : "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_AVOID_GROWTH").getPath() + " size=18></img>"# Emphasize Avoid Growth
				}
		self.CITIZENS_AUTOMATED_ICON = "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_CITIZENS_AUTOMATED").getPath() + " size=18></img>"
		self.PRODUCTION_AUTOMATED_ICON = "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_PRODUCTION_AUTOMATED").getPath() + " size=18></img>"

		self.PromoCombatList = [i for i in range(gc.getNumPromotionInfos()) if (gc.getPromotionInfo(i).getCombatPercent() > 0)]
		self.PromoGarrisonList = [i for i in range(gc.getNumPromotionInfos()) if (gc.getPromotionInfo(i).getCityDefensePercent() > 0)]

		if self.COLOR_DICT == None:
			# Colors to highlight with for each type of number (Must be here,
			#  because C++ functions aren't available upon startup of CIV)
			self.COLOR_DICT = {
				"PROBLEM": gc.getInfoTypeForString("COLOR_RED"),
				"NEUTRAL": gc.getInfoTypeForString("COLOR_YELLOW"),
				"GREAT": gc.getInfoTypeForString("COLOR_GREEN"),
				}

		if self.HEADER_DICT == None:
			self.SetHeaderDict()

		if self.JUSTIFY_DICT == None:
			self.SetJustifyDict()

		if (self.HELP_DICT == None):
			self.SetHelpDict()
			GreenInfo = gc.getInfoTypeForString("COLOR_GREEN")
			for (szIndex, szHelp) in self.HELP_DICT.items():
				self.HELP_DICT[szIndex] = "<font=2>%s\n%s%s</font>"%(localText.changeTextColor( u"%s: [%s]\n" % (self.HEADER_DICT[szIndex], szIndex), GreenInfo), szHelp, self.GetColorHelpText(szIndex))

			self.HELP_DICT["BUILD_VIEW"] = "<font=2>%s\n%s</font>"%(localText.changeTextColor( u"%s: [%s]\n" % (self.buttonTextBuildings, "BUILD_VIEW"), GreenInfo), localText.getText("TXT_KEY_DOM_ADV_HELP_BUILD_VIEW", ()) % (self.objectHave, self.objectPossible, self.objectUnderConstruction, self.objectNotPossible, self.objectHaveObsolete))
			self.HELP_DICT["WW_VIEW"] = "<font=2>%s\n%s</font>"%(localText.changeTextColor( u"%s: [%s]\n" % (self.buttonTextBuildings, "WW_VIEW"), GreenInfo), localText.getText("TXT_KEY_DOM_ADV_HELP_WW_VIEW", ()) % (self.objectHave,  self.objectPossible, self.objectUnderConstruction, self.objectNotPossible, self.objectHaveObsolete, self.objectPossibleConcurrent, self.objectNotPossibleConcurrent))
			self.HELP_DICT["NW_VIEW"] = "<font=2>%s\n%s</font>"%(localText.changeTextColor( u"%s: [%s]\n" % (self.buttonTextNationalWonders, "NW_VIEW"), GreenInfo), localText.getText("TXT_KEY_DOM_ADV_HELP_NW_VIEW", ()) % (self.objectHave, self.objectPossible, self.objectUnderConstruction, self.objectNotPossible, self.objectHaveObsolete))
			self.HELP_DICT["TW_VIEW"] = "<font=2>%s\n%s</font>"%(localText.changeTextColor( u"%s: [%s]\n" % (self.buttonTextProjects, "TW_VIEW"), GreenInfo), localText.getText("TXT_KEY_DOM_ADV_HELP_TW_VIEW", ()) % (self.objectHave, self.objectPossible, self.objectUnderConstruction, self.objectNotPossible, self.objectHaveObsolete))

# CGE-LE - begin
			#if (not UserPrefs.vistaCheck):
			#	self.HELP_DICT["BUILD_VIEW"] = localText.getText("TXT_KEY_DOM_ADV_HELP_VISTA_WARNING", ())
			#	self.HELP_DICT["WW_VIEW"] = localText.getText("TXT_KEY_DOM_ADV_HELP_VISTA_WARNING", ())
			#	self.HELP_DICT["NW_VIEW"] = localText.getText("TXT_KEY_DOM_ADV_HELP_VISTA_WARNING", ())
			#	self.HELP_DICT["TW_VIEW"] = localText.getText("TXT_KEY_DOM_ADV_HELP_VISTA_WARNING", ())
# CGE-LE - end

		self.runtimeInitDone = True

	def GetColorHelpText(self, sCol):
		sHelp = ""
		# If the key is one we want to possibly color
		if (sCol in self.COLOR_SET):
			sHelp = u"\n\n" + localText.getText("TXT_KEY_DOM_ADV_MISC_COLORS", ()) + " :"
			# check for problem values
			if (sCol in self.PROBLEM_VALUES_DICT):
				sHelp += u"\n" + localText.changeTextColor(u" %s &lt;= %d"%(localText.getText("TXT_KEY_DOM_ADV_MISC_PROBLEM", ()), self.PROBLEM_VALUES_DICT[sCol]), self.COLOR_DICT["PROBLEM"])
			if (sCol in self.NEUTRAL_VALUES_DICT):
				sHelp += u"\n" + localText.changeTextColor(u" %s == %d"%(localText.getText("TXT_KEY_DOM_ADV_MISC_NEUTRAL", ()), self.NEUTRAL_VALUES_DICT[sCol]), self.COLOR_DICT["NEUTRAL"])
			if (sCol in self.GREAT_VALUES_DICT):
				sHelp += u"\n" + localText.changeTextColor(u" %s >= %d"%(localText.getText("TXT_KEY_DOM_ADV_MISC_GREAT", ()), self.GREAT_VALUES_DICT[sCol]), self.COLOR_DICT["GREAT"])
		return sHelp

	def getCityList(self, iPlayer):
		lCity = []
		pPlayer = gc.getPlayer(iPlayer)
		(loopCity, iter) = pPlayer.firstCity(false)
		while (loopCity):
			if (not loopCity.isNone() and loopCity.getOwner() == iPlayer ): #only valid cities
				lCity.append(loopCity)
			(loopCity, iter) = pPlayer.nextCity(iter, false)
		return lCity

	def getProductionOtherCivs(self, iBuildingType, lList):
		# Loop through players to determine Wonders
		iActivePlayer = gc.getGame().getActivePlayer()
		pActivePlayer = gc.getPlayer(iActivePlayer)
		iActivePlayerTeam = gc.getTeam(pActivePlayer.getTeam()).getID()
		for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
			if (iPlayerLoop != pActivePlayer):
				pPlayer = gc.getPlayer(iPlayerLoop)
				iPlayerTeam = pPlayer.getTeam()
				# No barbs and only display national wonders for the active player's team
	 			if (pPlayer and not pPlayer.isBarbarian()):
					# Loop through this player's cities and determine if they have any wonders to display
					for pCity in self.getCityList(iPlayerLoop):
						# Loop through projects to find any under construction
						if (iBuildingType == 3): # projects 
							for iProjectLoop in xrange(len(lList)):
								iProjectProd = pCity.getProductionProject()
								# Project is being constructed
								if (iProjectProd == iProjectLoop):
									# Project Mode
									if (iPlayerTeam == iActivePlayerTeam):
										# is in construction by team mate
										lList[iProjectLoop] = (lList[iProjectLoop][0], lList[iProjectLoop][1], 1)
						# Loop through buildings
						else:
							for iBuildingLoop in xrange(len(lList)):
								iBuildingProd = pCity.getProductionBuilding()
								BuildingClassType = gc.getBuildingInfo(iBuildingLoop).getBuildingClassType()
								# World Wonder Mode
								if (iBuildingType == 2 and isWorldWonderClass(BuildingClassType)):
									# Is this city building a wonder?
									if (iBuildingProd == iBuildingLoop):
										# Only show our wonders under construction
										if (iPlayerTeam == iActivePlayerTeam):
											# is in construction by team mate
											lList[iBuildingProd] = (lList[iBuildingProd][0], lList[iBuildingProd][1], 1)
								# National/Team Wonder Mode
								elif iBuildingType == 1 and (isNationalWonderClass(BuildingClassType) or isTeamWonderClass(BuildingClassType)):
									# Is this city building a wonder?
									if (iBuildingProd == iBuildingLoop):
										# Only show our wonders under construction
										if (iPlayerTeam == iActivePlayerTeam):
											# is in construction by team mate
											lList[iBuildingProd] = (lList[iBuildingProd][0], lList[iBuildingProd][1], 1)
		return lList

	def getBuildingType(self, iBuilding):
		if (isWorldWonderClass(iBuilding)):
			# world wonder
			return 2

		if (isTeamWonderClass(iBuilding)):
			# team wonder
			return 3

		if (isNationalWonderClass(iBuilding)):
			# national wonder
			return 1

		# Regular building
		return 0

	def CheckVisibility(self, iBuilding, iBuildingType):
		if (not self.bShowOnlyAvailableBuildings):
			return True
		iPlayer = gc.getGame().getActivePlayer()
		pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		for pLoopCity in self.getCityList(iPlayer):
			if (iBuildingType == 3):
				if (pLoopCity.canCreate(iBuilding, False, True)):
					return True
				elif (pTeam.getProjectCount(iBuilding) > 0):
					return True
			else:
				if (pLoopCity.getNumBuilding(iBuilding) != 0):
					return True
				elif (pLoopCity.isProductionBuilding()):
					if (iBuilding == pLoopCity.getProductionBuilding()):
						return True
				else:
					if (pLoopCity.canConstruct(iBuilding, False, True, False)):
						return True
		return False

	def getBuildingSortedList(self, iBuildingType):
		listSorted = []
		listSortedAppend = listSorted.append
		if (iBuildingType == 3):
			# projects
			for iBuilding in xrange(gc.getNumProjectInfos()):
				if (self.CheckVisibility(iBuilding, iBuildingType)):
					listSortedAppend((iBuilding, gc.getProjectInfo(iBuilding).getDescription(), 0))
			listSorted.sort()
		else:
			# buildings and wonders
			BuildingSet = set()
			BuildingSetAdd = BuildingSet.add
			getCivBuilding = gc.getCivilizationInfo(gc.getPlayer(gc.getGame().getActivePlayer()).getCivilizationType()).getCivilizationBuildings
			for iBuilding in xrange(gc.getNumBuildingClassInfos()):
				BuildingIndex = getCivBuilding(iBuilding)
				if (self.getBuildingType(iBuilding) == iBuildingType):
					if (self.CheckVisibility(BuildingIndex, iBuildingType)):
						BuildingSetAdd(BuildingIndex)
			listSorted = [(BuildingIndex, gc.getBuildingInfo(BuildingIndex).getDescription(), 0) for BuildingIndex in BuildingSet]
			listSorted.sort()
			if (iBuildingType == 2):
				listSorted = self.getProductionOtherCivs(iBuildingType, listSorted)

		return listSorted

	def getCurrentCity(self):
		if (self.m_nChosenCity != self.NO_CITY):
			return gc.getPlayer(gc.getGame().getActivePlayer()).getCity(self.m_nChosenCity)
		else:
			return None

	# Screen construction function
	# This is the function that's called whenever F1 is pressed.
	def interfaceScreen(self):
		self.SetConstants()

		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		self.nScreenX = (screen.getXResolution() - self.nScreenWidth) / 2
		self.nScreenY = (screen.getYResolution() - self.nScreenLength) / 5 + 50
		screen.setDimensions(self.nScreenX, self.nScreenY, self.nScreenWidth, self.nScreenLength -20)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		self.drawBasicScreen()
		self.drawScreen(self.m_szMode)

	def drawBasicScreen(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		# Here we set the background widget and exit button, and we show the screen
		screen.addPanel( self.BACKGROUND_ID, u"", u"", True, False, 0, 29, self.nScreenWidth, self.nScreenLength, PanelStyles.PANEL_STYLE_MAIN )
		# Text Buttons

		screen.setText(self.EXIT_NAME, "Background", self.Button_List[0][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[0][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText(self.REDRAW_NAME, "Background", self.Button_List[1][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[1][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.TW_NAME, "Background", self.Button_List[2][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[2][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.NW_NAME, "Background", self.Button_List[3][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[3][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.WW_NAME, "Background", self.Button_List[4][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[4][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.BUILD_NAME, "Background", self.Button_List[5][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[5][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.MIL_NAME, "Background", self.Button_List[6][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[6][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.SPEC_NAME, "Background", self.Button_List[7][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[7][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(self.CITY_NAME, "Background", self.Button_List[8][0], CvUtil.FONT_RIGHT_JUSTIFY, self.Button_List[8][1], self.nButtonsY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		bCanLiberate = False
		(loopCity, iter) = pPlayer.firstCity(False)
		while (loopCity):
			if (loopCity.getLiberationPlayer(False) != -1):
				bCanLiberate = True
				break
			(loopCity, iter) = pPlayer.nextCity(iter, False)

		if (bCanLiberate or pPlayer.canSplitEmpire()):
			screen.setImageButton("DomesticSplit", "", self.nFreeColonyX, self.nFreeColonyY, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FREE_COLONY).getActionInfoIndex(), -1)
			screen.setStyle("DomesticSplit", "Button_HUDAdvisorVictory_Style")

		# Specialist Screen Toggle Button
		self.drawCultureLevel()
		self.drawSpecialists()

	def drawCultureLevel(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		# Cultural Levels Text
		screen.setText (self.CULTURE_TEXT_NAME, "Background", self.HEADER_DICT["CULTURE"], CvUtil.FONT_LEFT_JUSTIFY, self.nCultureLevelX, self.nCultureLevelY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		nGameSpeed = CyGame().getGameSpeedType()
		iCount = 2
		for i in xrange (gc.getNumCultureLevelInfos()):
			pCultureLevel = gc.getCultureLevelInfo(i)
			nValue = pCultureLevel.getSpeedThreshold(nGameSpeed)
			if (nValue != 0):
				screen.setText(self.CULTURE_TEXT_NAME + str(i), "Background", "<font=2>%s</font>"%(pCultureLevel.getText()), CvUtil.FONT_LEFT_JUSTIFY, self.nCultureLevelX, self.nCultureLevelY + (self.nCultureLevelDistance * iCount), -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setText(self.CULTURE_TEXT_NAME + self.NUMBER_TEXT + str(i), "Background", "<font=2>%d</font>"%(nValue), CvUtil.FONT_RIGHT_JUSTIFY, self.nCultureLevelX + self.nCultureLevelTextOffset, self.nCultureLevelY + (self.nCultureLevelDistance * iCount), -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iCount += 1

		# GP Level Text
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		screen.setText(self.GP_TEXT_NAME, "Background", self.HEADER_DICT["GREATPEOPLE"], CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.GP_TEXT_NAME + self.NUMBER_TEXT, "Background", "<font=2>%d</font>"%(pPlayer.greatPeopleThreshold(False)), CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY + self.nGPLevelDistance, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setText(self.GP_TEXT_NAME + "1", "Background", self.HEADER_DICT["GREATGENERAL"], CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY + self.nGPLevelDistance * 2, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.GP_TEXT_NAME + self.NUMBER_TEXT + "1", "Background", "<font=2>%d</font>"%(pPlayer.greatPeopleThreshold(True)), CvUtil.FONT_RIGHT_JUSTIFY, self.nGPLevelX, self.nGPLevelY + self.nGPLevelDistance * 3, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	# Draw the specialist and their increase and decrease buttons
	def drawSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		# Citizen Buttons
		for i in xrange(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isVisible()):
				szI = str(i)
				szName = self.SPECIALIST_IMAGE_NAME + szI
				screen.setImageButton(szName, gc.getSpecialistInfo(i).getTexture(), self.nFirstSpecialistX + (self.nSpecialistDistance * i), self.nSpecialistY, self.nSpecialistWidth, self.nSpecialistLength, WidgetTypes.WIDGET_CITIZEN, i, -1)
				screen.hide(szName)
				# Increase Specialists...
				szName = self.SPECIALIST_PLUS_NAME + szI
				screen.setButtonGFC(szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nPlusOffsetX, self.nSpecialistY + self.nPlusOffsetY, self.nPlusWidth, self.nPlusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
				screen.hide(szName)
				# Decrease specialists
				szName = self.SPECIALIST_MINUS_NAME + szI
				screen.setButtonGFC(szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nMinusOffsetX, self.nSpecialistY + self.nMinusOffsetY, self.nMinusWidth, self.nMinusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
				screen.hide(szName)
				# Specialist text
				szName = self.SPECIALIST_TEXT_NAME + szI
				screen.setText(szName, "Background", "", CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.hide(szName)

	def showSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		self.hideSpecialists()
		pCity = self.getCurrentCity()
		if (pCity):
			nPopulation = pCity.getPopulation()
			nFreeSpecial = pCity.totalFreeSpecialists()
			# For each specialist type
			for i in xrange(gc.getNumSpecialistInfos()):
				if (gc.getSpecialistInfo(i).isVisible()):
					szI = str(i)
					# Show all the specialist images
					screen.show(self.SPECIALIST_IMAGE_NAME + szI)
					szName = self.SPECIALIST_TEXT_NAME + szI
					screen.setText(szName, "Background", "%d/%d"%(pCity.getSpecialistCount(i), pCity.getMaxSpecialistCount(i)), CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.show(szName)
					# If the specialist is valid
					if (pCity.isSpecialistValid(i, 1) and (pCity.getForceSpecialistCount(i) < (nPopulation + nFreeSpecial))):
						screen.show(self.SPECIALIST_PLUS_NAME + szI)
					if (pCity.getSpecialistCount(i) > 0 or pCity.getForceSpecialistCount(i) > 0):
						screen.show(self.SPECIALIST_MINUS_NAME + szI)

	def hideSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		# Hide Buttons
		for i in xrange(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isVisible()):
				szI = str(i)
				screen.hide(self.SPECIALIST_IMAGE_NAME + szI)
				screen.hide(self.SPECIALIST_PLUS_NAME + szI)
				screen.hide(self.SPECIALIST_MINUS_NAME + szI)
				screen.hide(self.SPECIALIST_TEXT_NAME + szI)

	def hideHelpButtons(self, len):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		for i in xrange(len):
			# help button
			screen.hide(self.HELP_BUTTON_NAME + str(i))

	def hide(self, screen, screenType):
		screen.hide(screenType)
		if (screenType == self.SPEC_AREA_NAME):
			self.hideSpecialists()
			self.hideHelpButtons(len(self.SPEC_VIEW_LIST))
		elif (screenType == self.DEF_AREA_NAME):
			self.hideHelpButtons(len(self.DEF_VIEW_LIST))
		elif (screenType == self.MIL_AREA_NAME):
			self.hideHelpButtons(len(self.MIL_VIEW_LIST))
		elif (screenType == self.BUILD_AREA_NAME):
			self.HideButtons (self.BUILD_AREA_NAME)
		elif (screenType == self.WW_AREA_NAME):
			self.HideButtons (self.WW_AREA_NAME)
		elif (screenType == self.NW_AREA_NAME):
			self.HideButtons (self.NW_AREA_NAME)
		elif (screenType == self.TW_AREA_NAME):
			self.HideButtons (self.TW_AREA_NAME)

	# Create the Default Domestic Advisor Screen
	def drawScreen(self, szMode):

		self.lBuildings = self.getBuildingSortedList(0) # Usual Buildings
		self.lWW = self.getBuildingSortedList(2) # World Wonders
		self.lNW = self.getBuildingSortedList(1) # National Wonders
		self.lTW = self.getBuildingSortedList(3) # Team Projects

		if self.BUILD_TO_COL > len(self.lBuildings)-1:
			self.BUILD_TO_COL = len(self.lBuildings)-1
		if self.WW_TO_COL > len(self.lWW)-1:
			self.WW_TO_COL = len(self.lWW)-1
		if self.NW_TO_COL > len(self.lNW)-1:
			self.NW_TO_COL = len(self.lNW)-1
		if self.TW_TO_COL > len(self.lTW)-1:
			self.TW_TO_COL = len(self.lTW)-1

		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		if (szMode == self.DEF_AREA_NAME):
			self.m_szMode = self.DEF_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
		elif (szMode == self.SPEC_AREA_NAME):
			self.m_szMode = self.SPEC_AREA_NAME
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
			self.showSpecialists()
		elif (szMode == self.BUILD_AREA_NAME):
			self.m_szMode = self.BUILD_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
			self.ShowButtons(szMode)
		elif (szMode == self.WW_AREA_NAME):
			self.m_szMode = self.WW_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
			self.ShowButtons(szMode)
		elif (szMode == self.NW_AREA_NAME):
			self.m_szMode = self.NW_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
			self.ShowButtons(szMode)
		elif (szMode == self.TW_AREA_NAME):
			self.m_szMode = self.TW_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.ShowButtons(szMode)
		elif (szMode == self.MIL_AREA_NAME):
			self.m_szMode = self.MIL_AREA_NAME
			self.hide(screen, self.SPEC_AREA_NAME)
			self.hide(screen, self.DEF_AREA_NAME)
			self.hide(screen, self.MIL_AREA_NAME)
			self.hide(screen, self.BUILD_AREA_NAME)
			self.hide(screen, self.WW_AREA_NAME)
			self.hide(screen, self.NW_AREA_NAME)
			self.hide(screen, self.TW_AREA_NAME)
		else:
			return
		# Erase the flag?
		CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
		# Draw the city list...
		self.drawContents(szMode)
		screen.enableSort(szMode)

	def ShowButtons (self, szArea):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		if (szArea == self.BUILD_AREA_NAME):
			lList = self.lBuildings
			iFrom = self.BUILD_FROM_COL
			iTo = self.BUILD_TO_COL
		elif (szArea == self.WW_AREA_NAME):
			lList = self.lWW
			iFrom = self.WW_FROM_COL
			iTo = self.WW_TO_COL
		elif (szArea == self.NW_AREA_NAME):
			lList = self.lNW
			iFrom = self.NW_FROM_COL
			iTo = self.NW_TO_COL
		elif (szArea == self.TW_AREA_NAME):
			lList = self.lTW
			iFrom = self.TW_FROM_COL
			iTo = self.TW_TO_COL
		else:
			return
		i = 0
		for iI in xrange(len(lList)):
			# set the header
			if (iFrom <= iI <= iTo):
				szName = self.BUILD_BUTTON_NAME + str(i)
				if (szArea == self.TW_AREA_NAME):
					screen.setImageButton(szName, gc.getProjectInfo(lList[iI][0]).getButton(), self.BUILD_BUTTON_X_OFFSET+i*self.BUILD_BUTTON_X_STEP, self.BUILD_BUTTON_Y_OFFSET, self.BUILD_BUTTON_X_SIZE, self.BUILD_BUTTON_Y_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, lList[iI][0], -1)
				else: 
					screen.setImageButton(szName, gc.getBuildingInfo(lList[iI][0]).getButton(), self.BUILD_BUTTON_X_OFFSET+i*self.BUILD_BUTTON_X_STEP, self.BUILD_BUTTON_Y_OFFSET, self.BUILD_BUTTON_X_SIZE, self.BUILD_BUTTON_Y_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, lList[iI][0], -1)
				i += 1
		# Left Button
		if (iFrom > 0):
			screen.setButtonGFC(self.BUILD_BUTTON_LEFT, u"", "", self.BUILD_BUTTON_LEFT_X, self.BUILD_BUTTON_LR_Y_OFFSET, self.BUILD_BUTTON_LR_X_SIZE, self.BUILD_BUTTON_LR_Y_SIZE, WidgetTypes.WIDGET_GENERAL, 0, 1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
		else:
			screen.hide(self.BUILD_BUTTON_LEFT)

		# right Button
		if (iTo < len(lList)-1):
			screen.setButtonGFC(self.BUILD_BUTTON_RIGHT, u"", "", self.BUILD_BUTTON_RIGHT_X, self.BUILD_BUTTON_LR_Y_OFFSET, self.BUILD_BUTTON_LR_X_SIZE, self.BUILD_BUTTON_LR_Y_SIZE, WidgetTypes.WIDGET_GENERAL, 0, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		else:
			screen.hide(self.BUILD_BUTTON_RIGHT)

	def HideButtons(self, szArea):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		if (szArea == self.BUILD_AREA_NAME):
			lList = self.lBuildings
			iFrom = self.BUILD_FROM_COL
			iTo = self.BUILD_TO_COL
		elif (szArea == self.WW_AREA_NAME):
			lList = self.lWW
			iFrom = self.WW_FROM_COL
			iTo = self.WW_TO_COL
		elif (szArea == self.NW_AREA_NAME):
			lList = self.lNW
			iFrom = self.NW_FROM_COL
			iTo = self.NW_TO_COL
		elif (szArea == self.TW_AREA_NAME):
			lList = self.lTW
			iFrom = self.TW_FROM_COL
			iTo = self.TW_TO_COL
		else:
			return
		i = 0
		for iI in xrange(len(lList)):
			if (iFrom <= iI <= iTo):
				screen.hide(self.BUILD_BUTTON_NAME + str(i))
				i += 1
		screen.hide(self.BUILD_BUTTON_LEFT)
		screen.hide(self.BUILD_BUTTON_RIGHT)

	# headers...
	def drawHeaders(self, szArea):
		# Get the screen
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		if ((szArea == self.BUILD_AREA_NAME) or (szArea == self.WW_AREA_NAME) or (szArea == self.NW_AREA_NAME) or (szArea == self.TW_AREA_NAME)):

			if (szArea == self.BUILD_AREA_NAME):
				lList = self.lBuildings
				iFrom = self.BUILD_FROM_COL
				iTo = self.BUILD_TO_COL
			elif (szArea == self.WW_AREA_NAME):
				lList = self.lWW
				iFrom = self.WW_FROM_COL
				iTo = self.WW_TO_COL
			elif (szArea == self.NW_AREA_NAME):
				lList = self.lNW	
				iFrom = self.NW_FROM_COL
				iTo = self.NW_TO_COL
			elif (szArea == self.TW_AREA_NAME):
				lList = self.lTW	
				iFrom = self.TW_FROM_COL
				iTo = self.TW_TO_COL
			else:
				return

			screen.setTableColumnHeader(szArea, 0, "<font=2>%s</font>"%(localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_BUTTON", ())), self.BUILD_BUTTON_COL_SIZE)
			screen.setTableColumnHeader(szArea, 1, "<font=2>%s</font>"%(localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_NAME", ())), self.BUILD_NAME_COL_SIZE)

			i = 1
			for iI in xrange(len(lList)):
				# set the header
				if (iFrom <= iI <= iTo):
					i += 1
					screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(lList[iI][1]), self.BUILD_BUTTON_X_STEP)

			i += 1
			screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(self.HEADER_DICT["BASE_PRODUCTION"]), self.BUILD_OUTPUT_COL_SIZE)
			i += 1
			screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(self.HEADER_DICT["BASE_GOLD"]), self.BUILD_OUTPUT_COL_SIZE)
			i += 1
			screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(self.HEADER_DICT["BASE_RESEARCH"]), self.BUILD_OUTPUT_COL_SIZE)

			i += 1
			screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(localText.getText("TXT_KEY_DOM_ADV_COL_HEADER_TURNS", ())), self.BUILD_TURNS_COL_SIZE)

		else:
			if (szArea == self.DEF_AREA_NAME):
				lList = self.DEF_VIEW_LIST
				colSize = self.DEF_VIEW_COLS_SIZE
			elif (szArea == self.SPEC_AREA_NAME):
				lList = self.SPEC_VIEW_LIST
				colSize = self.SPEC_VIEW_COLS_SIZE
			elif (szArea == self.MIL_AREA_NAME):
				lList = self.MIL_VIEW_LIST
				colSize = self.MIL_VIEW_COLS_SIZE
			else:
				return

			y = self.HELP_BUTTON_Y_OFFSET
			x = self.HELP_BUTTON_X_OFFSET

			# For each column
			#szImage = "<img=%s size=%d></img>"%(ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), self.HELP_BUTTON_X_SIZE)
			szImage = self.bulletIcon
			for i in xrange(len(lList)):
				# column header
				dx = int( float(lList[i][1]) / (float(colSize)) * (self.nTableWidth-10) )
				screen.setTableColumnHeader(szArea, i, "<font=2>%s</font>"%(self.HEADER_DICT[lList[i][0]]), dx)

				# help button
				screen.setHelpLabel(self.HELP_BUTTON_NAME + str(i), "Background", szImage, CvUtil.FONT_LEFT_JUSTIFY, x+dx/2-self.HELP_BUTTON_X_SIZE/2, y, -0.3, FontTypes.TITLE_FONT, self.HELP_DICT[lList[i][0]])
				x += dx

	# Function to calculate value given a certain city and key
	def CalculateValue(self, pCity, szKey):
		# Initialize Return Value
		szReturn = ""

		if (szKey == "DATE"):
			# City founded date...
			szReturn = unicode(CyGameTextMgr().getTimeStr(pCity.getGameTurnFounded(), False))

		elif (szKey == "NAME"):
			# City name...
			szReturn = pCity.getName()
			if (pCity.getLiberationPlayer(False) != -1):
				szReturn += self.occupationIcon

		elif (szKey == "LANDMARKS"):
			# Landmarks...

			# First look for Government Centers
			if pCity.isGovernmentCenter():
				# And distinguish between the Capital and the others (Forbidden Palace
				# and Versailles)
				if pCity.isCapital():
					szReturn += self.starIcon
				else:
					szReturn += self.silverStarIcon

			# add National Wonder Landmarks
			for iWonder in xrange(pCity.getNumNationalWonders()):
				szReturn += self.bulletIcon

			if pCity.isPower():
				szReturn += self.powerIcon
			if pCity.isDisorder():
				if pCity.isOccupation():
					szReturn += "%s(%s)"%(self.occupationIcon, pCity.getOccupationTimer())
				else:
					szReturn += self.angryIcon

			if (pCity.isConnectedToCapital(gc.getGame().getActivePlayer())):
				szReturn += self.tradeIcon

		elif (szKey == "DISORDER"):
			# is the city in disorder or is it occupied
			if pCity.isDisorder():
				if pCity.isOccupation():
					szReturn += "%s:%s"%(self.occupationIcon, pCity.getOccupationTimer())
				else:
					szReturn += self.angryIcon
			else:
				szReturn = u""

		elif (szKey == "POWER"):
			# Powerplant
			if pCity.isPower():
				szReturn = self.powerIcon
			else:
				szReturn = u""

		elif (szKey == "POPULATION"):
			# Population
			szReturn = unicode(pCity.getPopulation())

		elif (szKey == "POPULATION_REAL"):
			# Population
			szReturn = unicode(pCity.getRealPopulation())

		elif (szKey == "GARRISON"):
			# Garrison
			szReturn = unicode(pCity.getMilitaryHappinessUnits())

		elif (szKey == "HAPPY"):
			# Replace Happiness/Unhappiness with Net Happiness...
			szReturn = unicode(pCity.happyLevel() - pCity.unhappyLevel(0))

		elif (szKey == "BASE_HAPPY"):
			# Real happy population
			szReturn = unicode(pCity.happyLevel())

		elif (szKey == "BASE_UNHAPPY"):
			# Real unhappy population
			szReturn = unicode(pCity.unhappyLevel(0))

		elif (szKey == "HEALTH"):
			# combine health/unhealthy... to Net City Health
			szReturn = unicode(pCity.goodHealth() - pCity.badHealth(False))

		elif (szKey == "BASE_GOODHEALTH"):
			# Good health people
			szReturn = unicode(pCity.getGoodHealth())

		elif (szKey == "BASE_BADHEALTH"):
			# Bad health people
			szReturn = unicode(pCity.getBadHealth())

		elif (szKey == "GROWTH"):
			# Turns til Growth
			nFood = pCity.foodDifference(True)

			# If this is a food production (i.e., worker or settler)
			if (pCity.isFoodProduction()):
				# We need to indicate there's no growth manually
				szReturn = "-"
			else:
				# Otherwise, just call FoodTurnsLeft
				szReturn = unicode(pCity.getFoodTurnsLeft())

			# Not enough food, so calculate how many turns until we starve.
			# We put this here because we still starve if building a food production
			if nFood < 0:
				# Use floor divide (//) because we want the number it'll drop below 0
				# (that's also the reason for the additional 1)
				szReturn = unicode((pCity.getFood()+1) // nFood)

		elif (szKey == "FOOD_STORED"):
			# the food stored in the city
			szReturn = unicode(pCity.getFood())

		elif (szKey == "FOOD"):
			# Replace Food/Food Used with Net Food AND Turns until Growth...
			# If this is a food production (i.e., worker or settler)
			if (pCity.isFoodProduction()):
				nFood = pCity.getCurrentProductionDifference(False, False) - pCity.getCurrentProductionDifference(True, False)
			else:
				nFood = pCity.foodDifference(True)
			szReturn = unicode(nFood)

		elif (szKey == "BASE_FOOD"):
			# base food production
			szReturn = unicode(pCity.getBaseYieldRate(YieldTypes.YIELD_FOOD))

		elif (szKey == "COMMERCE_BASE"):
			# base commerce production
			szReturn = unicode(pCity.getBaseYieldRate(YieldTypes.YIELD_COMMERCE))

		elif (szKey == "BASE_PRODUCTION"):
			# base city production (hammers)
			szReturn = unicode(pCity.getBaseYieldRate(YieldTypes.YIELD_PRODUCTION))
		
		elif (szKey == "PRODUCTION"):
			# Production status
			szReturn = unicode(pCity.getCurrentProductionDifference(True, False))

		elif (szKey == "MAINTENANCE"):
			# City Maintanance...
			szReturn = unicode(pCity.getMaintenance())
			#szReturn = u"%.2f"%(pCity.city.getMaintenanceTimes100()/100.0)

		elif (szKey == "MAINTENANCE_DISTANCE"):
			# City Maintanance caused by distance to capital/governemnt center...
			szReturn = unicode(pCity.calculateDistanceMaintenance())

		elif (szKey == "MAINTENANCE_NUMCITIES"):
			# City Maintanance caused by number of cities...
			szReturn = unicode(pCity.calculateNumCitiesMaintenance())

		elif (szKey == "TRADE"):
			# Trade status...
			nTotalTradeProfit = 0
			# For each trade route possible
			for nTradeRoute in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
				# Get the next trade city
				pTradeCity = pCity.getTradeCity(nTradeRoute)
				# Not quite sure what this does but it's in the MainInterface
				# and I pretty much C&Ped :p
				if (pTradeCity and pTradeCity.getOwner() >= 0):
					for j in xrange(YieldTypes.NUM_YIELD_TYPES):
						iTradeProfit = pCity.calculateTradeYield(j, pCity.calculateTradeProfit(pTradeCity))

						# If the TradeProfit is greater than 0 add it to the total
						if (iTradeProfit > 0):
							nTotalTradeProfit += iTradeProfit

			szReturn = unicode(nTotalTradeProfit)

		elif (szKey == "COMMERCE"):
			# Commerce status...
			szReturn = unicode(pCity.getYieldRate(YieldTypes.YIELD_COMMERCE))

		elif (szKey == "BASE_GOLD"):
			# base Gold
			szReturn = unicode(pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD))

		elif (szKey == "GOLD"):
			# Gold status...
			szReturn = unicode(pCity.getCommerceRate(CommerceTypes.COMMERCE_GOLD))

		elif (szKey == "BASE_RESEARCH"):
			# base research
			szReturn = unicode(pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_RESEARCH))

		elif (szKey == "RESEARCH"):
			# Science rate...
			szReturn = unicode(pCity.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH))

		elif (szKey == "CULTURE_RATE"):
			# Culture status...
			szReturn = unicode(pCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE))

		elif (szKey == "CULTURE"):
			# Total Culture
			szReturn = unicode(pCity.getCulture(gc.getGame().getActivePlayer()))

		elif (szKey == "GREATPEOPLE_RATE"):
			# Great Person
			szReturn = unicode(pCity.getGreatPeopleRate())

		elif (szKey == "GREATPEOPLE"):
			# Great Person
			szReturn = unicode(pCity.getGreatPeopleProgress())

		elif (szKey == "GREATPEOPLE_TURNS"):
			# turns till a great person is created.
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			if (pCity.getGreatPeopleRate() != 0):
				# force round up
				szReturn = unicode( int((( float(pPlayer.greatPeopleThreshold(False) - pCity.getGreatPeopleProgress())) / float(pCity.getGreatPeopleRate()))+0.999) )
			else:
				szReturn = u"-"

		elif (szKey == "PRODUCING"):
			# Producing
			# If there's something in the queue,
			iQueueLength = pCity.getOrderQueueLength()
			if (iQueueLength > 0):
				# Get the name of whatever it's producing.
				if (iQueueLength > 1):
					szReturn = pCity.getProductionName() + "[%i]"%(int(iQueueLength))
				else:
					szReturn = pCity.getProductionName()
# CGE-LE - begin
				if (pCity.isProductionUnit()):
					Order = pCity.getOrderFromQueue(0)
					if (Order):
						if (Order.bSave):
							szReturn = "* " + szReturn
# CGE-LE - end
			# Otherwise we're not producing anything. Leave it blank.
			else:
				szReturn = "-"
			# Store what the city is producing
			self.CITY_PRODUCING_DICT[pCity.getName()] = szReturn

		elif (szKey == "TURNS"):
			# Turns left to finish actual production 
			# If there's something in the queue,
			iQueueLength = pCity.getOrderQueueLength()
			if (iQueueLength > 0 and not pCity.isProductionProcess()):
				if (iQueueLength > 1):
					szReturn = "%d [%i]"%(pCity.getProductionTurnsLeft(), int(iQueueLength))
				else:
					szReturn = unicode(pCity.getProductionTurnsLeft())
				if (pCity.canHurry(0, False) or pCity.canHurry(1, False)):
					szReturn = localText.changeTextColor(szReturn, gc.getInfoTypeForString("COLOR_YELLOW"))
			# Otherwise we're not producing anything. Leave it blank.
			else:
				szReturn = "-"

		elif (szKey == "RELIGIONS"):
			# Religions...
			szHC = u""
			szRel = u""

			for i in xrange(gc.getNumReligionInfos()):
				if (pCity.isHasReligion(i)):
					if (pCity.isHolyCityByType(i)):
						szHC += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
					else:
						szRel += u"%c" %(gc.getReligionInfo(i).getChar())
			szReturn = szHC + szRel

		elif (szKey == "THREATS"):
			# city threats 
			szReturn = u""
			pPlayerIsAtWar = gc.getTeam(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam()).isAtWar
			for i in xrange(gc.getMAX_PLAYERS()):
				if (pPlayerIsAtWar(gc.getPlayer(i).getTeam())):
					if pCity.isVisible(gc.getPlayer(i).getTeam(), False):
						szReturn =  self.angryIcon
						break

		elif (szKey == "SPECIALISTS"):
			# Specialists...
			szReturn += "<font=1>"
			# For each specialist type
			for i in xrange(gc.getNumSpecialistInfos()):
				if self.bShowCompressedSpecialists:
					nCount = pCity.getSpecialistCount(i)
					# If more than one specialist
					if (nCount > 1):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>x" + str(nCount)
					elif (nCount == 1):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>"
				else:
					for nCount in xrange(pCity.getSpecialistCount(i)):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>"

			# For each Super Specialist
			for i in xrange(gc.getNumSpecialistInfos()):
				if self.bShowCompressedSpecialists:
					nCount = pCity.getFreeSpecialistCount(i)
					# If more than one specialist
					if (nCount > 1):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>x" + str(nCount)
					elif (nCount == 1):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>"
				else:
					for nCount in xrange(pCity.getFreeSpecialistCount(i)):
						szReturn += "<img=" + gc.getSpecialistInfo(i).getTexture() + " size=22></img>"
			#if (len(szTemp)):
			#	szReturn += ", " + szTemp
			szReturn += "</font>"

		elif (szKey == "AUTOMATION"):
			# Automated values
			szReturn += "<font=1>"

			nNumEmphasize = len(self.AUTOMATION_ICON_DICT)
			if (pCity.isCitizensAutomated()):
				szReturn += self.CITIZENS_AUTOMATED_ICON
			if (pCity.isProductionAutomated()):
				szReturn += self.PRODUCTION_AUTOMATED_ICON
			for i in xrange(nNumEmphasize):
				nNum = nNumEmphasize - i - 1
				if (pCity.AI_isEmphasize(nNum)):
					szReturn += self.AUTOMATION_ICON_DICT[nNum]

		elif (szKey == "DEFENSE_VIS"):
			# visible defense value. Is equal DEFENSE_BUILDING - DEFENSE_DAMAGE
			szReturn = unicode(pCity.getDefenseModifier(False))

		elif (szKey == "DEFENSE_DAMAGE"):
			# amount of damage on the city defense
			szReturn = unicode(pCity.getDefenseDamage())

		elif (szKey == "DEFENSE_TOTAL"):
			# total defense modifier (unsure what this valiu doesn mean!)
			szReturn = unicode(pCity.getDefenseModifier(False))

		elif (szKey == "CONSCRIPT"):
			# can city conspript ...
			if pCity.canConscript():
				szReturn = self.textTRUE
			else: 
				szReturn = self.textFALSE

		elif (szKey == "CONSCRIPT_UNIT"):
			# best unit type the city can conspript ...
			if pCity.canConscript():
				szReturn = unicode(gc.getUnitInfo(pCity.getConscriptUnit()).getDescription())
			else:
				szReturn = unicode("-")

		elif (szKey == "NO_MILITARY_ANGER"):
			# amount of anger produced because there is are no military units in the city
			if pCity.getNoMilitaryPercentAnger() == 0:
				szReturn = self.happyIcon
			else:
				szReturn = self.unhappyIcon

		elif (szKey == "WAR_WEARINESS"):
			szReturn = unicode(pCity.getWarWearinessModifier())

		elif (szKey == "FREE_EXPERIENCE"):
			# amount of free experiences points for produced units
			# stolen from CvCity::getProductionExperience in CvCity.cpp
			#szTemp = u""
			pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			iFreeEXP = pCity.getFreeExperience() + pCity.getSpecialistFreeExperience()
			iFreeEXP += pActivePlayer.getFreeExperience()
			if (pActivePlayer.getStateReligion() != -1):
				if (pCity.isHasReligion(pActivePlayer.getStateReligion())):
					iFreeEXP += pActivePlayer.getStateReligionFreeExperience()

			szReturn = u"%d, %d, %d"%(iFreeEXP + pCity.getDomainFreeExperience(DomainTypes.DOMAIN_LAND), iFreeEXP + pCity.getDomainFreeExperience(DomainTypes.DOMAIN_SEA), iFreeEXP + pCity.getDomainFreeExperience(DomainTypes.DOMAIN_AIR))

		elif (szKey == "COASTAL"):
			# is city at the coast...
			if (pCity.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN())):
				szReturn = self.textTRUE
			else: 
				szReturn = self.textFALSE

		elif (szKey == "UNITS_TOTAL_NUM"):
			# number of player units in the city.
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				if (pCity.plot().getUnit(i).getOwner() == iActivePlayer):
					Value += 1
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_NUM"):
			# number of players military units in the city.
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)) and (pUnit.getOwner() == iActivePlayer):
					Value += 1
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_GROUND_NUM"):
			# number of players military ground units in the city.
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnitTypeInfo.getCombat() > 0) and (pUnit.getOwner() == iActivePlayer) and (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_LAND):
					Value += 1
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_SEA_NUM"):
			# number of players military sea units in the city. 
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnitTypeInfo.getCombat() > 0) and (pUnit.getOwner() == iActivePlayer) and (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_SEA):
					Value += 1
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_AIR_NUM"):
			# number of players military air units in the city. 
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnitTypeInfo.getAirCombat() > 0) and (pUnit.getOwner() == iActivePlayer) and (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_AIR):
					Value += 1
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_GROUND_DEFENSE_SUM"):
			# sum of players military ground units combat and defense strength. 
			# it take consideration of promotions, damages and defense modifiers.
			# this roughly pictures the actual city defense strength for a ground attack.
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnitTypeInfo.getCombat() > 0) and (pUnit.getOwner() == iActivePlayer) and (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_LAND):
					Value += int(self.calculateUnitStrength(pUnit, pCity))
			szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_GROUND_DEFENSE_AVG"):
			# average values of players military ground units combat and defense strength. 
			# it take consideration of promotions, damages and defense modifiers.
			# this roughly pictures the quality of the actual city defense units against a ground attack.
			Value = 0
			cnt = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnitTypeInfo.getCombat() > 0) and (pUnit.getOwner() == iActivePlayer) and (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_LAND):
					Value += int(self.calculateUnitStrength(pUnit, pCity))
					cnt += 1
			if (cnt > 0):
				szReturn = unicode(Value//cnt)
			else:
				szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_AIR_DEFENSE_NUM"):
			# number of players military air defense units in the city. 
			# these could be ground, sea and air units.
			# it roughly pictures the air defense of the city.
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnit.getOwner() == iActivePlayer) and (pUnit.currInterceptionProbability() > 0):
					Value += 1
			szReturn = unicode(Value)
			
		elif (szKey == "UNITS_MIL_AIR_DEFENSE_AVG"):
			# average air interception probability of players military air defense units in the city.
			# these could be ground, sea and air units
			# it roughly pictures the air defense capability of the city.
			Value = 0
			cnt = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnit.getOwner() == iActivePlayer) and (pUnit.currInterceptionProbability() > 0):
					Value += pUnit.currInterceptionProbability()
					cnt += 1
			if (cnt > 0):
				szReturn = unicode(Value//cnt)
			else:
				szReturn = unicode(Value)

		elif (szKey == "UNITS_MIL_AIR_PATROL"):
			# number of units on air patrol
			Value = 0
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(i)
				pUnitTypeInfo = gc.getUnitInfo(pCity.plot().getUnit(i).getUnitType())
				if (pUnit.getOwner() == iActivePlayer) and (pUnit.currInterceptionProbability() > 0):
					pGroup = pUnit.getGroup()
					if (pGroup.getActivityType() == ActivityTypes.ACTIVITY_INTERCEPT):
						Value += 1
			szReturn = unicode(Value)

		elif (szKey == "ESPIONAGE"):
			szReturn = unicode(pCity.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE))

		elif (szKey == "CORPORATIONS"):
			# Corporations...
			szHQ = u""
			szCorp = u""
			for i in range(gc.getNumCorporationInfos()):
				if (pCity.isHasCorporation(i)):
					if (pCity.isHeadquartersByType(i)):
						szHQ += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
					else:
						szCorp += u"%c" %(gc.getCorporationInfo(i).getChar())
			szReturn = szHQ + szCorp

		# return the final value
		return szReturn

	def calculateUnitStrength(self, pUnit, pCity):
		PromoInfo = gc.getPromotionInfo
		# get unit combat modifiers
		fCombat = 0
		for i in self.PromoCombatList:
			if (pUnit.isHasPromotion(i)):
				fCombat += PromoInfo(i).getCombatPercent()
		fCombat = float(fCombat * 0.01)

		# get unit city defense modifiers
		fDefense = 0
		for i in self.PromoGarrisonList:
			if (pUnit.isHasPromotion(i)):
				fCombat += PromoInfo(i).getCityDefensePercent()
		fDefense = float(fDefense * 0.01)

		# get the current ctiy defense modifier
		fCityDefense = float(pCity.getDefenseModifier(False)*0.01)

		# the calculation is more a good guess. So if there is an error in the calculation inform me please.
		# target of this function is, to calculate the units strength for city defense.
		return float(pUnit.baseCombatStr() * (1.0-pUnit.getDamage()*0.01) * (1.0+fCombat+fDefense+fCityDefense))

	def CheckCity(self, pCity, lList, i, szArea):
# CGE-LE - begin
		#if (not UserPrefs.vistaCheck):
		#	return "--"
# CGE-LE - end
		# city has this building already
		if (szArea == self.TW_AREA_NAME):
			if (lList[i][0] == pCity.getProductionProject()):
				return self.objectUnderConstruction
			if not pCity.canCreate(lList[i][0], False, False):
				pTeam = gc.getTeam(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam())
				if (pTeam.getProjectCount(lList[i][0]) >= gc.getProjectInfo(lList[i][0]).getMaxTeamInstances()) and (pTeam.getProjectMaking(lList[i][0]) == 0):
					return self.objectHave
				else:
					return self.objectNotPossible
			return self.objectPossible
		else:
			if (pCity.getNumBuilding(lList[i][0]) != 0):
				if (pCity.getNumActiveBuilding(lList[i][0]) != 0):
					# building is not obsolete
					return self.objectHave
				else:
					# building is obsolete
					return self.objectHaveObsolete
			# cbuilding is under construction (first place of queue only)
			if (lList[i][0] == pCity.getProductionBuilding()):
				return self.objectUnderConstruction
			else:
				# buildings, world wonders and national wonder
				if not pCity.canConstruct(lList[i][0], False, False, False):
					if (szArea == self.WW_AREA_NAME):
						if (lList[i][2] == 2):
							# is currently build by an opponent civ
							return self.objectNotPossibleConcurrent
						else:
							return self.objectNotPossible
					else:
						bFoundinQueue = False
						for iOrder in xrange(pCity.getOrderQueueLength()):
							pOrderData = pCity.getOrderFromQueue(iOrder)
							if (pOrderData.eOrderType == OrderTypes.ORDER_CONSTRUCT):
								if (pOrderData.iData1 == lList[i][0]):
									bFoundinQueue = True
						if (not bFoundinQueue):
							return self.objectNotPossible
			if (szArea == self.WW_AREA_NAME) and (lList[i][2] == 2):
				# is currently build by an opponent civ
				return self.objectPossibleConcurrent
			else:
				return self.objectPossible

	def ColorCityValues(self, nValue, szKey):
		"Colors city values which we might want to alert the user to."
		# If the key is one we want to possibly color
		if (szKey in self.COLOR_SET):
			# If we don't have a plain integer
			if (re.search("[-+]", nValue)):
				# Color it red and return it
				return localText.changeTextColor(nValue, gc.getInfoTypeForString("COLOR_RED"))
			# For each type of comparison
			for szCompareType, clDict in self.COLOR_DICT_DICT.items():
				# Get the color we will use.
				color = self.COLOR_DICT[szCompareType]
				# If the dictionary has the key and the comparison is appropriate
				if (clDict.has_key(szKey) and \
					(szCompareType == "PROBLEM" and int(nValue) <= clDict[szKey] or szCompareType == "NEUTRAL" and int(nValue) == clDict[szKey] or szCompareType == "GREAT" and int(nValue) >= clDict[szKey])):
					# Color and return it
					return localText.changeTextColor(nValue, color)
		# Otherwise, just return the regular value
		return nValue

	# Function to draw the contents of the cityList passed in
	def drawContents(self, szArea):
		# Get the screen and the player
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		screen.moveToFront("Background")

		if (szArea == self.DEF_AREA_NAME):
			lList = self.DEF_VIEW_LIST
			screen.addTableControlGFC(szArea, len(lList), self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		elif (szArea == self.SPEC_AREA_NAME):
			lList = self.SPEC_VIEW_LIST
			screen.addTableControlGFC(szArea, len(lList), self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		elif (szArea == self.MIL_AREA_NAME):
			lList = self.MIL_VIEW_LIST
			screen.addTableControlGFC(szArea, len(lList), self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		elif (szArea == self.BUILD_AREA_NAME):
			screen.addTableControlGFCWithHelp(szArea, self.BUILD_TO_COL-self.BUILD_FROM_COL+7, self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD, self.HELP_DICT["BUILD_VIEW"])
		elif (szArea == self.WW_AREA_NAME):
			screen.addTableControlGFCWithHelp(szArea, self.WW_TO_COL-self.WW_FROM_COL+7, self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD, self.HELP_DICT["WW_VIEW"])
		elif (szArea == self.NW_AREA_NAME):
			screen.addTableControlGFCWithHelp(szArea, self.NW_TO_COL-self.NW_FROM_COL+7, self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD, self.HELP_DICT["NW_VIEW"])
		elif (szArea == self.TW_AREA_NAME):
			screen.addTableControlGFCWithHelp(szArea, self.TW_TO_COL-self.TW_FROM_COL+7, self.nTableX, self.nTableY, self.nTableWidth, self.nTableLength, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD, self.HELP_DICT["TW_VIEW"])
		else:
			return
		# Build the table
		screen.enableSelect(szArea, True)
		# Loop through the cities
		for (i, pLoopCity) in enumerate(self.getCityList(gc.getGame().getActivePlayer())):
			screen.appendTableRow(szArea)
			if ((szArea == self.BUILD_AREA_NAME) or (szArea == self.WW_AREA_NAME) or (szArea == self.NW_AREA_NAME) or (szArea == self.TW_AREA_NAME)):
				# city zoom button
				screen.setTableText(szArea, 0, i, "", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(), WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
				# city name column
				szValue = self.ColorCityValues(self.CalculateValue(pLoopCity, "NAME"), "NAME")
				screen.setTableText(szArea, 1, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				# buildings column
				l = 1
				if (szArea == self.BUILD_AREA_NAME):
					lList = self.lBuildings
					iFrom = self.BUILD_FROM_COL
					iTo = self.BUILD_TO_COL
				elif (szArea == self.WW_AREA_NAME):
					lList = self.lWW
					iFrom = self.WW_FROM_COL
					iTo = self.WW_TO_COL
				elif (szArea == self.NW_AREA_NAME):
					lList = self.lNW
					iFrom = self.NW_FROM_COL
					iTo = self.NW_TO_COL
				elif (szArea == self.TW_AREA_NAME):
					lList = self.lTW
					iFrom = self.TW_FROM_COL
					iTo = self.TW_TO_COL
				else:
					return
				for iI in xrange(len(lList)):
					if (iFrom <= iI <= iTo):
						l += 1
						szValue = self.CheckCity(pLoopCity, lList, iI, szArea)
						screen.setTableText(szArea, l, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				l += 1
				szValue = self.ColorCityValues(self.CalculateValue (pLoopCity, "BASE_PRODUCTION"), "BASE_PRODUCTION")
				screen.setTableInt(szArea, l, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				l += 1
				szValue = self.ColorCityValues(self.CalculateValue (pLoopCity, "BASE_GOLD"), "BASE_GOLD")
				screen.setTableInt(szArea, l, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				l += 1
				szValue = self.ColorCityValues(self.CalculateValue (pLoopCity, "BASE_RESEARCH"), "BASE_RESEARCH")
				screen.setTableInt(szArea, l, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				# productions turns left 
				l += 1
				szValue = self.ColorCityValues(self.CalculateValue (pLoopCity, "TURNS"), "TURNS")
				screen.setTableText(szArea, l, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			else:
				# For each column
				for ii in xrange(len(lList)):
					justify = self.JUSTIFY_DICT[lList[ii][0]]

					if (lList[ii][0] == "BUTTON"): 
						screen.setTableText(szArea, 0, i, "", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(), WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
					else:
						if (justify == CvUtil.FONT_RIGHT_JUSTIFY):
							funcTableWrite = screen.setTableInt
						else:
							funcTableWrite = screen.setTableText
						szValue = self.ColorCityValues(self.CalculateValue(pLoopCity, lList[ii][0]), lList[ii][0])
						funcTableWrite(szArea, ii, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, justify)
			i += 1
		self.drawHeaders(szArea)
		if (self.m_nChosenCity < pPlayer.getNumCities() and self.m_nChosenCity != self.NO_CITY):
			screen.selectRow(szArea, self.m_nChosenCity, True)
		else:
			self.m_nChosenCity = self.NO_CITY
		screen.moveToBack(self.BACKGROUND_ID)
		self.updateAppropriateCitySelection(szArea, pPlayer.getNumCities())

	def HandleSpecialistPlus(self, inputClass):
		pCity = self.getCurrentCity()
		if (pCity):
			if self.m_bSpecialistChange and self.m_nLastSpecialistChange == inputClass.getID():
				nMaxSpecial = pCity.getMaxSpecialistCount(self.m_nLastSpecialistChange)
				self.m_nSpecialistChangeNumber += 1
				if (self.m_nSpecialistChangeNumber > nMaxSpecial):
					self.m_nSpecialistChangeNumber = nMaxSpecial
			else:
				self.m_bSpecialistChange = True
				self.m_nLastSpecialistChange = inputClass.getID()
				self.m_nSpecialistChangeNumber = pCity.getSpecialistCount(self.m_nLastSpecialistChange) + 1
		return 0

	def HandleSpecialistMinus(self, inputClass):
		pCity = self.getCurrentCity()
		if (pCity):
			if self.m_bSpecialistChange and self.m_nLastSpecialistChange == inputClass.getID():
				self.m_nSpecialistChangeNumber -= 1
				if (self.m_nSpecialistChangeNumber < 0):
					self.m_nSpecialistChangeNumber = 0
			else:
				self.m_bSpecialistChange = True
				self.m_nLastSpecialistChange = inputClass.getID()
				self.m_nSpecialistChangeNumber = pCity.getSpecialistCount(self.m_nLastSpecialistChange) - 1
#			self.m_nTimesChanged = 0
		return 0

	def Spec(self, inputClass):
		self.m_szMode = self.SPEC_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1

	def Mil(self, inputClass):
		self.m_szMode = self.MIL_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1
		
	def City(self, inputClass):
		self.m_szMode = self.DEF_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1

	def DomesticExit(self, inputClass):
		return 0

	def Redraw(self, inputClass):
		# Redraw the screen
		self.drawScreen (self.m_szMode)
		return 1

	def Build(self, inputClass):
		self.m_szMode = self.BUILD_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1

	def WW(self, inputClass):
		self.m_szMode = self.WW_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1

	def NW(self, inputClass):
		self.m_szMode = self.NW_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1
		
	def TW(self, inputClass):
		self.m_szMode = self.TW_AREA_NAME
		self.drawScreen (self.m_szMode)
		return 1

	def BuildLeft(self, inputClass):
		if (self.m_szMode == self.BUILD_AREA_NAME):
			if (self.BUILD_FROM_COL > 0):
				self.BUILD_FROM_COL -= self.BUILD_NUM_COLS
				self.BUILD_TO_COL -= self.BUILD_NUM_COLS
				if self.BUILD_FROM_COL < 0:
					self.BUILD_FROM_COL = 0
					self.BUILD_TO_COL = self.BUILD_NUM_COLS-1
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.WW_AREA_NAME):
			if (self.WW_FROM_COL > 0):
				self.WW_FROM_COL -= self.BUILD_NUM_COLS
				self.WW_TO_COL -= self.BUILD_NUM_COLS
				if self.WW_FROM_COL < 0:
					self.WW_FROM_COL = 0
					self.WW_TO_COL = self.BUILD_NUM_COLS-1
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.NW_AREA_NAME):
			if (self.NW_FROM_COL > 0):
				self.NW_FROM_COL -= self.BUILD_NUM_COLS
				self.NW_TO_COL -= self.BUILD_NUM_COLS
				if self.NW_FROM_COL < 0:
					self.NW_FROM_COL = 0
					self.NW_TO_COL = self.BUILD_NUM_COLS-1
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.TW_AREA_NAME):
			if (self.TW_FROM_COL > 0):
				self.TW_FROM_COL -= self.BUILD_NUM_COLS
				self.TW_TO_COL -= self.BUILD_NUM_COLS
				if self.TW_FROM_COL < 0:
					self.TW_FROM_COL = 0
					self.TW_TO_COL = self.BUILD_NUM_COLS-1
				self.drawScreen(self.m_szMode)
		return 1

	def BuildRight(self, inputClass):
		if (self.m_szMode == self.BUILD_AREA_NAME):
			if (self.BUILD_TO_COL < (len(self.lBuildings)-1)):
				self.BUILD_FROM_COL += self.BUILD_NUM_COLS
				self.BUILD_TO_COL += self.BUILD_NUM_COLS
				if self.BUILD_TO_COL > (len(self.lBuildings)-1):
					self.BUILD_TO_COL = len(self.lBuildings)-1
					self.BUILD_FROM_COL = len(self.lBuildings)-self.BUILD_NUM_COLS
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.WW_AREA_NAME):
			if (self.WW_TO_COL < (len(self.lWW)-1)):
				self.WW_FROM_COL += self.BUILD_NUM_COLS
				self.WW_TO_COL += self.BUILD_NUM_COLS
				if self.WW_TO_COL > (len(self.lWW)-1):
					self.WW_TO_COL = len(self.lWW)-1
					self.WW_FROM_COL = len(self.lWW)-self.BUILD_NUM_COLS
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.NW_AREA_NAME):
			if (self.NW_TO_COL < (len(self.lNW)-1)):
				self.NW_FROM_COL += self.BUILD_NUM_COLS
				self.NW_TO_COL += self.BUILD_NUM_COLS
				if self.NW_TO_COL > (len(self.lNW)-1):
					self.NW_TO_COL = len(self.lNW)-1
					self.NW_FROM_COL = len(self.lNW)-self.BUILD_NUM_COLS
				self.drawScreen(self.m_szMode)
		elif (self.m_szMode == self.TW_AREA_NAME):
			if (self.TW_TO_COL < (len(self.lTW)-1)):
				self.TW_FROM_COL += self.BUILD_NUM_COLS
				self.TW_TO_COL += self.BUILD_NUM_COLS
				if self.TW_TO_COL > (len(self.lTW)-1):
					self.TW_TO_COL = len(self.lTW)-1
					self.TW_FROM_COL = len(self.lTW)-self.BUILD_NUM_COLS
				self.drawScreen(self.m_szMode)
		return 1

	# Will handle the input for this screen...
	def handleInput(self, inputClass):
		' Calls function mapped in DomesticScreenInputMap'
		# only get from the map if it has the key
		# If we get that a listbox item was selected
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			if (inputClass.getMouseX() == 0):
				screen.hideScreen()

				CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True);

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setText(u"showDomesticAdvisor")
				popupInfo.addPopup(inputClass.getData1())
			else:
				# Store the index
				nIndex = inputClass.getData()
				self.m_nChosenCity = nIndex

				if (self.m_szMode == self.SPEC_AREA_NAME):
					self.showSpecialists()

				# And pass it back to the screen
				self.updateAppropriateCitySelection(self.m_szMode, gc.getPlayer(gc.getGame().getActivePlayer()).getNumCities())

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_R)):
				return self.Redraw (inputClass)
			elif (inputClass.getData() == int(InputTypes.KB_C)):
				return self.City (inputClass)
			elif (inputClass.getData() == int(InputTypes.KB_S)):
				return self.Spec (inputClass)

		# Otherwise, we got something else
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.DomesticScreenInputMap.has_key(inputClass.getFunctionName())):
				'Calls function mapped in CvSpecDomesticAdvisor'
				# only get from the map if it has the key
				# get bound function from map and call it
				return self.DomesticScreenInputMap.get(inputClass.getFunctionName())(inputClass)
			elif (inputClass.getFunctionName() == "DomesticSplit"):
				screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
				screen.hideScreen()
				return 1
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) or (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			if (self.DomesticScreenInputMap.has_key(inputClass.getFunctionName())):
				self.DomesticScreenInputMap.get(inputClass.getFunctionName())(inputClass)
				return 1
		return 0

	def updateAppropriateCitySelection(self, scr, nCities):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.updateAppropriateCitySelection(scr, nCities, 1)

	def isFoodProductionChange(self, pCity):
		szCity = pCity.getName()
		# If we already have noted what this city was producing
		if (self.CITY_PRODUCING_DICT.has_key(szCity)):
			# Get if we switched to/from a food production
			bFoodSearch = re.search("Worker|Settler", self.CITY_PRODUCING_DICT[szCity])
			bFoodProductionSwitch = ((pCity.isFoodProduction () and not bFoodSearch) or (not pCity.isFoodProduction() and bFoodSearch))
		else:
			# Otherwise, there's no way it's a food production switch
			bFoodProductionSwitch = False
		return bFoodProductionSwitch

	def updateScreen(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		if (self.m_szMode == self.DEF_AREA_NAME):
			lList = self.DEF_VIEW_LIST
		elif (self.m_szMode == self.SPEC_AREA_NAME):
			lList = self.SPEC_VIEW_LIST
		elif (self.m_szMode == self.MIL_AREA_NAME):
			lList = self.MIL_VIEW_LIST
		elif ((self.m_szMode == self.BUILD_AREA_NAME) or (self.m_szMode == self.WW_AREA_NAME) or (self.m_szMode == self.NW_AREA_NAME) or (self.m_szMode == self.TW_AREA_NAME)):
			self.drawScreen (self.m_szMode)
			return
		else:
			return

		cityList = self.getCityList(gc.getGame().getActivePlayer())
		# for each city in list
		for i in xrange(screen.getTableNumRows(self.m_szMode)):
			# get list city name
			loopCity = screen.getTableText(self.m_szMode, 1, i)
			# match with citylist to get city object
			pLoopCity = None
			for tempLoopCity in cityList:
				if (loopCity == tempLoopCity.getName()):
					pLoopCity = tempLoopCity
					break

			if (pLoopCity):
				bFoodProductionChange = self.isFoodProductionChange(pLoopCity)
				# For each value that needs updating
				for key, value in self.UPDATE_DICT.items():
					# If the key is in this table and it's updatable with the change type
					for ii in xrange(len(lList)):
						if (lList[ii][0] == key) and (bFoodProductionChange or value):
							szValue = self.ColorCityValues(self.CalculateValue (pLoopCity, key), key)
							if (self.JUSTIFY_DICT[key] == CvUtil.FONT_RIGHT_JUSTIFY):
								screen.setTableInt(self.m_szMode, ii, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, self.JUSTIFY_DICT[key])
							else:
								screen.setTableText(self.m_szMode, ii, i, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, self.JUSTIFY_DICT[key])

		return

	def handleSpecialistUpdate(self):
		""" This function returns if we should handle the Specialist Update."""
		# If we have a specialist change and it's in the specialist table mode
		if (self.m_bSpecialistChange and (self.m_szMode == self.SPEC_AREA_NAME)):
			# Get the current city and return if the specialist has completed changing
			pCity = self.getCurrentCity()
			if (pCity):
				return self.isSpecialistChange(pCity)
		return False

	def isSpecialistChange(self, pCity):
		return self.m_nSpecialistChangeNumber == pCity.getSpecialistCount(self.m_nLastSpecialistChange)

	# Function to draw the contents of the cityList passed in
	def updateRow(self, szArea, nRow):

		# Get the screen and the player
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		if (szArea == self.SPEC_AREA_NAME):
			lList = self.SPEC_VIEW_LIST
		else:
			return

		pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(nRow)


		# For each column
		for i in xrange(len(lList)):
			justify = self.JUSTIFY_DICT[lList[i][0]]
			if (justify == CvUtil.FONT_RIGHT_JUSTIFY):
				funcTableWrite = screen.setTableInt
			else:
				funcTableWrite = screen.setTableText
			szValue = self.ColorCityValues(self.CalculateValue(pCity, lList[i][0]), lList[i][0])
			funcTableWrite(szArea, i, nRow, szValue, "", WidgetTypes.WIDGET_GENERAL, -1, -1, justify)

		screen.setTableText(szArea, 0, 0, "", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(), WidgetTypes.WIDGET_ZOOM_CITY, pCity.getOwner(), pCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

		self.updateAppropriateCitySelection(szArea, gc.getPlayer(gc.getGame().getActivePlayer()).getNumCities())

	def update(self, fDelta):
		""" Update the Advisor."""
		# If we can handle the specialist update, do so.
		if (CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)
			if (self.handleSpecialistUpdate()):
				self.showSpecialists()
				self.updateRow(self.m_szMode, self.m_nChosenCity)
				# We've handled it.
				self.m_bSpecialistChange = False
			else:
				self.updateScreen()

		return
