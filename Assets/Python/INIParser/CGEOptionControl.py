# Civ IV Gameplay Enhancements Option Control Functions
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import CvConfigParser
import CvUtil

import TradeResourcePanel
import CityInfoPanelPS
import ExecutiveBriefing
import MoreCiv4lerts
import Civ4lerts
import CvMainInterface
import CvDiplomacyInterface
import CGEEventManager
import AlertsLog
import CGEUtils

try:
	import UnitStatisticsTools
	USsetOption = UnitStatisticsTools.UnitStatisticsTools()
except ImportError:
	USsetOption = None

localText = CyTranslator()
gc = CyGlobalContext()

CGEOptionCheckBox = {
	"CGECivName": 									{'Section': "Civ Name", 						'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGEMasterName": 								{'Section': "Master Name", 						'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGECityInfoPS": 								{'Section': "City Info Panel", 					'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGEDiplomacyAttitude": 						{'Section': "Diplomacy Attitude", 				'Key': "Show", 'Default': False, 'Tab': 1},
	"CGECombatExperienceCounter": 					{'Section': "Combat Experience Counter", 		'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGEGameTurnBar":			 					{'Section': "Game Turn Bar", 					'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGEGreatPersonBar":			 				{'Section': "Great Person Bar", 				'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGETopCultureCities":			 				{'Section': "Top Culture Cities", 				'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGEWinampGUI": 								{'Section': "Winamp GUI", 						'Key': "Enabled", 'Default': False, 'Tab': 1},
	"CGEUnitStatistics": 							{'Section': "Unit Statistics Mod", 				'Key': "Enabled", 'Default': False, 'Tab': 1},
	"CGETRPShow": 									{'Section': "Trade Resource Panel", 			'Key': "Show", 'Default': True, 'Tab': 1},
	"CGETRPShowEachTrade": 							{'Section': "Trade Resource Panel", 			'Key': "Trade", 'Default': False, 'Tab': 1},
	"CGETRPSmallIcons": 							{'Section': "Trade Resource Panel", 			'Key': "SmallIcons", 'Default': False, 'Tab': 1},
	"CGETRPCompressMode": 							{'Section': "Trade Resource Panel", 			'Key': "Compress Mode", 'Default': False, 'Tab': 1},
	"CGETRPShowSingleResource": 					{'Section': "Trade Resource Panel", 			'Key': "Show Single Resource", 'Default': False, 'Tab': 1},
	"CGEHideDeadCivilizations": 					{'Section': "Dead Civ Scoreboard Mod", 			'Key': "Hide Dead Civilizations", 'Default': False, 'Tab': 1},
	"CGEGreyOutDeadCivilizations": 					{'Section': "Dead Civ Scoreboard Mod", 			'Key': "Grey Out Dead Civilizations", 'Default': True, 'Tab': 1},
	"CGEShowDeadTag": 								{'Section': "Dead Civ Scoreboard Mod", 			'Key': "Show Dead Tag", 'Default': True, 'Tab': 1},
	"CGESpyDetect": 								{'Section': "Spy Detect", 						'Key': "Enabled", 'Default': True, 'Tab': 1},
	"CGECiv4lertsCityPendingGrowth": 				{'Section': "City Pending Growth", 				'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsCityPendingUnhealthy": 			{'Section': "City Pending Unhealthy", 			'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsCityPendingAngry": 				{'Section': "City Pending Angry", 				'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsCityGrowth": 						{'Section': "City Growth", 						'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsCityGrowthUnhealthy": 				{'Section': "City Growth Unhealthy", 			'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsCityGrowthAngry": 					{'Section': "City Growth Angry", 				'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGECiv4lertsGoldTrade": 						{'Section': "Gold Trade", 						'Key': "Enabled", 'Default': False, 'Tab': 2},
	"CGECiv4lertsGoldPerTurnTrade": 				{'Section': "Gold Per Turn Trade", 				'Key': "Enabled", 'Default': False, 'Tab': 2},
	"CGEExecutiveBriefing": 						{'Section': "Executive Briefing", 				'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGEMoreCiv4lerts": 							{'Section': "More Civ4lerts", 					'Key': "Enabled", 'Default': True, 'Tab': 2},
	"CGEMoreCiv4lertsCheckForDomPopVictory": 		{'Section': "More Civ4lerts", 					'Key': "CheckForDomPopVictory", 'Default': True, 'Tab': 2},
	"CGEMoreCiv4lertsCheckForDomLandVictory": 		{'Section': "More Civ4lerts", 					'Key': "CheckForDomLandVictory", 'Default': True, 'Tab': 2},
	"CGEMoreCiv4lertsCheckForCityBorderExpansion": 	{'Section': "More Civ4lerts", 					'Key': "CheckForCityBorderExpansion", 'Default': True, 'Tab': 2},
	"CGEMoreCiv4lertsCheckForNewTrades": 			{'Section': "More Civ4lerts", 					'Key': "CheckForNewTrades", 'Default': True, 'Tab': 2},
	"CGEAlertsInterference": 						{'Section': "CGE Alerts", 						'Key': "Interference", 'Default': True, 'Tab': 2},
	"CGEAlertsObsolete": 							{'Section': "CGE Alerts", 						'Key': "Obsolete", 'Default': True, 'Tab': 2},
	"CGEAlertsSpyStealTech": 						{'Section': "CGE Alerts", 						'Key': "SpyStealTech", 'Default': True, 'Tab': 2},
	"CGEAPLEnabled": 								{'Section': "APL General", 						'Key': "Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLCompress": 								{'Section': "APL General", 						'Key': "Compress Mode", 'Default': True, 'Tab': 3},
	"CGEAPLMissionInfo": 							{'Section': "APL General", 						'Key': "Mission Info Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLHealthBar": 								{'Section': "APL General", 						'Key': "Health Bar Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLUpgradeIndicator": 						{'Section': "APL General", 						'Key': "Upgrade Indicator Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLPromotionIndicator": 					{'Section': "APL General", 						'Key': "Promotion Indicator Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLWoundedIndicator": 						{'Section': "APL General", 						'Key': "Wounded Indicator Enabled", 'Default': True, 'Tab': 3},
	"CGEAPLWarlordIndicator": 						{'Section': "APL General", 						'Key': "Warlord Indicator Enabled", 'Default': True, 'Tab': 3},
	"CGERawCommerceDisplay": 						{'Section': "Raw Commerce Display", 			'Key': "Enabled", 'Default': True, 'Tab': 5},
	"CGECitizensAutomated": 						{'Section': "Citizens Automated", 				'Key': "Enabled", 'Default': True, 'Tab': 5},
	"CGEBottomContainerIcon": 						{'Section': "Bottom Container Icon", 			'Key': "Small", 'Default': True, 'Tab': 5},
	"CGESpecialistStackerEnabled": 					{'Section': "Specialist Stacker", 				'Key': "Enabled", 'Default': True, 'Tab': 5},
	"CGEHighlightForcedSpecialists": 				{'Section': "Specialist Stacker", 				'Key': "Highlight Forced Specialists", 'Default': True, 'Tab': 5},
	"CGEStackSuperSpecialists": 					{'Section': "Specialist Stacker", 				'Key': "Stack Super Specialists", 'Default': True, 'Tab': 5},
	"CGEDisplayUniqueSuperSpecialistsOnly": 		{'Section': "Specialist Stacker", 				'Key': "Display Unique Super Specialists Only", 'Default': False, 'Tab': 5},
	"CGEDynamicSuperSpecialistsSpacing": 			{'Section': "Specialist Stacker", 				'Key': "Dynamic Super Specialists Spacing", 'Default': True, 'Tab': 5},
	"CGEStackAngryCitizens": 						{'Section': "Specialist Stacker", 				'Key': "Stack Angry Citizens", 'Default': False, 'Tab': 5},
	"CGEDynamicAngryCitizenSpacing": 				{'Section': "Specialist Stacker", 				'Key': "Dynamic Angry Citizen Spacing", 'Default': True, 'Tab': 5},
	"CGEAlternateTimeText": 						{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternate Time Text", 'Default': True, 'Tab': 6},
	"CGEShowTurns": 								{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Turns", 'Default': True, 'Tab': 6},
	"CGEShowGameClock": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Game Clock", 'Default': True, 'Tab': 6},
	"CGEShowGameCompletedPercent": 					{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Game Completed Percent", 'Default': True, 'Tab': 6},
	"CGEShowGameCompletedTurns": 					{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Game Completed Turns", 'Default': False, 'Tab': 6},
	"CGEAlternateShowTurns": 						{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternate Show Turns", 'Default': True, 'Tab': 6},
	"CGEAlternateShowGameClock": 					{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternate Show Game Clock", 'Default': True, 'Tab': 6},
	"CGEAlternateShowGameCompletedPercent": 		{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternate Show Game Completed Percent", 'Default': False, 'Tab': 6},
	"CGEAlternateShowGameCompletedTurns": 			{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternate Show Game Completed Turns", 'Default': True, 'Tab': 6},
	"CGEShowEra": 									{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Era", 'Default': True, 'Tab': 6},
	"CGEShowReflectEraInTurnColor": 				{'Section': "Not Just Another Game Clock Mod", 	'Key': "Show Reflect Era In Turn Color", 'Default': True, 'Tab': 6},
	"CGEDisplayCurrentCivics":						{'Section': "CGEDLL", 							'Key': "Display Current Civics", 'Default': True, 'Tab': 1},
	"CGEDisplayAdditionalCityHelp":					{'Section': "CGEDLL",							'Key': "Display Additional City Help", 'Default': True, 'Tab': 1},
	"CGEDisplayCityRankOnProductionMenu":			{'Section': "CGEDLL", 							'Key': "Display City Rank On Production Menu", 'Default': True, 'Tab': 1},
	"CGETotalYieldFromCityFatCross":				{'Section': "CGEDLL", 							'Key': "Total Yield From City Fat Cross", 'Default': True, 'Tab': 1},
	"CGEShowHelp":									{'Section': "Unit Statistics Mod",			 	'Key': "Show Help", 'Default': True, 'Tab': 7},
	"CGEGlobalHighScore":							{'Section': "Unit Statistics Mod",			 	'Key': "Global High Score", 'Default': False, 'Tab': 7},
	"CGETrackAllPlayers":							{'Section': "Unit Statistics Mod", 				'Key': "Track All Players", 'Default': False, 'Tab': 7},
	"CGETrackTurnInformation":						{'Section': "Unit Statistics Mod",			 	'Key': "Track Turn Information", 'Default': True, 'Tab': 7},
	"CGETrackUnitHighScore":						{'Section': "Unit Statistics Mod",			 	'Key': "Track Unit High Score", 'Default': True, 'Tab': 7},
	"CGETrackUnitMovement":							{'Section': "Unit Statistics Mod",			 	'Key': "Track Unit Movement", 'Default': True, 'Tab': 7},
	"CGETrackNonCombatUnits":						{'Section': "Unit Statistics Mod",			 	'Key': "Track Non-Combat Units", 'Default': True, 'Tab': 7},
	"CGETrackGoodyReceived":						{'Section': "Unit Statistics Mod",			 	'Key': "Track Goody Received", 'Default': True, 'Tab': 7},
	"CGETrackUnitPromotions":						{'Section': "Unit Statistics Mod",			 	'Key': "Track Unit Promotions", 'Default': True, 'Tab': 7},
	"CGEShowAllPlayers":							{'Section': "Unit Statistics Mod",			 	'Key': "Show All Players", 'Default': False, 'Tab': 7},
	"CGEShowCombatCount":							{'Section': "Unit Statistics Mod",			 	'Key': "Show Combat Count", 'Default': True, 'Tab': 7},
	"CGEShowDamageInformation":						{'Section': "Unit Statistics Mod",			 	'Key': "Show Damage Information", 'Default': True, 'Tab': 7},
	"CGEShowOdds":									{'Section': "Unit Statistics Mod",			 	'Key': "Show Odds", 'Default': True, 'Tab': 7},
	"CGEShowExperience":							{'Section': "Unit Statistics Mod",			 	'Key': "Show Experience", 'Default': True, 'Tab': 7},
	"CGEShowUnitEventLog":							{'Section': "Unit Statistics Mod",			 	'Key': "Show Unit Event Log", 'Default': True, 'Tab': 7},
	"CGEShowLogTurnInformation":					{'Section': "Unit Statistics Mod",			 	'Key': "Show Log Turn Information", 'Default': True, 'Tab': 7},
	"CGEShowLogDateInformation":					{'Section': "Unit Statistics Mod",			 	'Key': "Show Log Date Information", 'Default': True, 'Tab': 7},
	"CGEShowLogTurnInformationFirst":				{'Section': "Unit Statistics Mod",			 	'Key': "Show Log Turn Information First", 'Default': True, 'Tab': 7},
	"CGEUnitNameRecycling":							{'Section': "Unit Statistics Mod",			 	'Key': "Unit Name Recycling", 'Default': True, 'Tab': 7},
	}

CGEOptionInt = {
	"TRPImportsExports": 							{'Section': "Trade Resource Panel", 			'Key': "Import and Export", 'Default': 0, 'Tab': 1},
	"TRPTechRes": 									{'Section': "Trade Resource Panel", 			'Key': "Technology and Resource", 'Default': 0, 'Tab': 1},
	"CGECiv4lertsGoldTradeThreshold": 				{'Section': "Gold Trade", 						'Key': "Threshold", 'Default': 50, 'Tab': 2},
	"CGECiv4lertsGoldPerTurnTradeThreshold": 		{'Section': "Gold Per Turn Trade", 				'Key': "Threshold", 'Default': 3, 'Tab': 2},
	"APLStackMode": 								{'Section': "APL General", 						'Key': "Stack Mode", 'Default': 0, 'Tab': 3},
	"CGEXPosition": 								{'Section': "APL Info Pane", 					'Key': "X Position", 'Default': 5, 'Tab': 3},
	"CGEYPosition": 								{'Section': "APL Info Pane", 					'Key': "Y Position", 'Default': 160, 'Tab': 3},
	"CGEXSize": 									{'Section': "APL Info Pane", 					'Key': "X Size", 'Default': 290, 'Tab': 3},
	"CGEPixelPerLineType1": 						{'Section': "APL Info Pane", 					'Key': "Pixel Per Line Type 1", 'Default': 24, 'Tab': 3},
	"CGEPixelPerLineType2": 						{'Section': "APL Info Pane", 					'Key': "Pixel Per Line Type 2", 'Default': 19, 'Tab': 3},
	"CGESpecialistStackWidth": 						{'Section': "Specialist Stacker", 				'Key': "Specialist Stack Width", 'Default': 20, 'Tab': 5},
	"CGEMaxSuperSpecialistButtons": 				{'Section': "Specialist Stacker", 				'Key': "Max Super Specialist Buttons", 'Default': 6, 'Tab': 5},
	"CGESuperSpecialistStackWidth": 				{'Section': "Specialist Stacker", 				'Key': "Super Specialist Stack Width", 'Default': 20, 'Tab': 5},
	"CGEMaxAngryCitizenButtons": 					{'Section': "Specialist Stacker", 				'Key': "Max Angry Citizen Buttons", 'Default': 6, 'Tab': 5},
	"CGEAngryCitizenStackWidth": 					{'Section': "Specialist Stacker", 				'Key': "Angry Citizen Stack Width", 'Default': 20, 'Tab': 5},
	"CGEAlternatingTime": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "Alternating Time", 'Default': 10, 'Tab': 6},
	}

CGEOptionFloat = {
	"CGEMoreCiv4lertsPopThreshold": 				{'Section': "More Civ4lerts", 					'Key': "PopThreshold", 'Default': 5.0, 'Tab': 2},
	"CGEMoreCiv4lertsLandThreshold": 				{'Section': "More Civ4lerts", 					'Key': "LandThreshold", 'Default': 5.0, 'Tab': 2},
	}

CGEOptionDropDown = {
	"AlertsLogDisplayTime1": 						{'Section': "Alerts Log", 						'Key': "Level1 Alert Message Time", 'Default': 4, 'Tab': 2},
	"AlertsLogDisplayTime2": 						{'Section': "Alerts Log", 						'Key': "Level2 Alert Message Time", 'Default': 4, 'Tab': 2},
	"AlertsLogDisplayTime3": 						{'Section': "Alerts Log", 						'Key': "Level3 Alert Message Time", 'Default': 4, 'Tab': 2},
	"CGEShowUnitServiceInformation": 				{'Section': "Unit Statistics Mod", 				'Key': "Show Unit Service Information", 'Default': 1, 'Tab': 7},
	"CGEUnitNaming": 								{'Section': "Unit Statistics Mod", 				'Key': "Unit Naming", 'Default': 1, 'Tab': 7},
	"CGEUnitNameNumber": 							{'Section': "Unit Statistics Mod", 				'Key': "Unit Name Number", 'Default': 1, 'Tab': 7},
	"CGEUnitNameAbreviation": 						{'Section': "Unit Statistics Mod", 				'Key': "Unit Name Abreviation", 'Default': 0, 'Tab': 7},
	"CGEUnitNameSpacing": 							{'Section': "Unit Statistics Mod", 				'Key': "Unit Name Spacing", 'Default': 0, 'Tab': 7},
	"CGEUnitNameDesc": 								{'Section': "Unit Statistics Mod", 				'Key': "Unit Name Desc", 'Default': 0, 'Tab': 7},
	}

CGEOptionDropDownColor = {
	"APLUnitNameColor": 							{'Section': "APL Info Pane Colors", 			'Key': "Unit Name Color", 'Default': "COLOR_YELLOW", 'Tab': 3},
	"APLUpgradePossibleColor": 						{'Section': "APL Info Pane Colors", 			'Key': "Upgrade Possible Color", 'Default': "COLOR_GREEN", 'Tab': 3},
	"APLUpgradeNotPossibleColor": 					{'Section': "APL Info Pane Colors", 			'Key': "Upgrade Not Possible Color", 'Default': "COLOR_RED", 'Tab': 3},
	"APLPromotionSpecialtiesColor": 				{'Section': "APL Info Pane Colors", 			'Key': "Promotion Specialties Color", 'Default': "COLOR_LIGHT_GREY", 'Tab': 3},
	"APLUnitTypeSpecialtiesColor": 					{'Section': "APL Info Pane Colors", 			'Key': "Unit Type Specialties Color", 'Default': "COLOR_WHITE", 'Tab': 3},
	"APLHealthColor": 								{'Section': "APL Stacked Bar Colors", 			'Key': "Health Color", 'Default': "COLOR_GREEN", 'Tab': 3},
	"APLWoundedColor": 								{'Section': "APL Stacked Bar Colors", 			'Key': "Wounded Color", 'Default': "COLOR_RED", 'Tab': 3},
	"AncientEraColor": 								{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_ANCIENT", 'Default': "COLOR_RED", 'Tab': 6},
	"ClassicalEraColor": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_CLASSICAL", 'Default': "COLOR_GREEN", 'Tab': 6},
	"MedievalEraColor": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_MEDIEVAL", 'Default': "COLOR_BLUE", 'Tab': 6},
	"RenaissanceEraColor": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_RENAISSANCE", 'Default': "COLOR_CYAN", 'Tab': 6},
	"IndustrialEraColor": 							{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_INDUSTRIAL", 'Default': "COLOR_YELLOW", 'Tab': 6},
	"ModernEraColor": 								{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_MODERN", 'Default': "COLOR_MAGENTA", 'Tab': 6},
	"FutureEraColor": 								{'Section': "Not Just Another Game Clock Mod", 	'Key': "ERA_FUTURE", 'Default': "COLOR_WHITE", 'Tab': 6},
	}

CGEDLLOptions = {}

CGEOptionColorIndex = [	"COLOR_WHITE",
						"COLOR_BLACK",
						"COLOR_DARK_GREY",
						"COLOR_GREY",
						"COLOR_LIGHT_GREY",
						"COLOR_RED",
						"COLOR_GREEN",
						"COLOR_BLUE",
						"COLOR_CYAN",
						"COLOR_YELLOW",
						"COLOR_MAGENTA",
						]

gOptionDict = {}
#	"": {'Section': "", 'Key': "", 'Default': True},

gOptionSetFunction = {
	"Civ Name":							CvMainInterface.CvMainInterface(),
	"Master Name":						CvMainInterface.CvMainInterface(),
	"City Info Panel":					CityInfoPanelPS.CityInfoPanelPS(),
	"Diplomacy Attitude":				CvDiplomacyInterface,
	"Combat Experience Counter":		CvMainInterface.CvMainInterface(),
	"Game Turn Bar":					CvMainInterface.CvMainInterface(),
	"Great Person Bar":					CvMainInterface.CvMainInterface(),
	"Winamp GUI":						CvMainInterface.CvMainInterface(),
	"Unit Statistics Mod":				USsetOption,
	"Trade Resource Panel":				TradeResourcePanel.TradeResourcePanel(),
	"Dead Civ Scoreboard Mod":			CvMainInterface.CvMainInterface(),
	"City Pending Growth":				Civ4lerts.Civ4lertsOption(),
	"City Pending Unhealthy":			Civ4lerts.Civ4lertsOption(),
	"City Pending Angry":				Civ4lerts.Civ4lertsOption(),
	"City Growth":						Civ4lerts.Civ4lertsOption(),
	"City Growth Unhealthy":			Civ4lerts.Civ4lertsOption(),
	"City Growth Angry":				Civ4lerts.Civ4lertsOption(),
	"Gold Trade":						Civ4lerts.Civ4lertsOption(),
	"Gold Per Turn Trade":				Civ4lerts.Civ4lertsOption(),
	"Executive Briefing":				ExecutiveBriefing.ExecutiveBriefing(),
	"More Civ4lerts":					MoreCiv4lerts.MoreCiv4lertsOption(),
	"CGE Alerts":						CGEEventManager.CGEEventOption(),
	"APL General":						None,
	"Raw Commerce Display":				None, #CvMainInterface.CvMainInterface(),
	"Citizens Automated":				None,
	"Specialist Stacker":				CvMainInterface.CvMainInterface(),
	"Not Just Another Game Clock Mod":	CvMainInterface.CvMainInterface(),
	"APL Info Pane":					None,
	"APL Info Pane Colors":				None,
	"APL Stacked Bar Colors":			None,
	"CGEDLL":							None,
	"Alerts Log":						AlertsLog.AlertsLog(),
	"Top Culture Cities":				CvMainInterface.CvMainInterface(),
	"Bottom Container Icon":			CvMainInterface.CvMainInterface(),
	"Spy Detect":						CGEUtils.CGEUtilsOption(),
	}

class CGEOptionControl:

	def InitValue(self):
		global gOptionDict
		global CGEDLLOptions

		gOptionDict = {}
		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")

		if (config != None):
			for Option in CGEOptionCheckBox.items():
				#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
				Value = config.getboolean(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
				gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}
			for Option in CGEOptionInt.items():
				#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
				Value = config.getint(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
				gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}
			for Option in CGEOptionFloat.items():
				#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
				Value = config.getfloat(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
				gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}
			for Option in CGEOptionDropDown.items():
				#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
				Value = config.getint(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
				gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}
			for Option in CGEOptionDropDownColor.items():
				#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
				Value = config.get(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
				gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}

		bHasCGEDLL = False
		#try:
		#	if (gc.isCGEBuild()):
		#		bHasCGEDLL = True
		#except:
		#	bHasCGEDLL = False

		if (bHasCGEDLL):
			CGEDLLOptions = {
				CGEOptionTypes.CGE_OPTION_DISPLAY_CURRENT_CIVICS:			{'Key': "Display Current Civics", 'Default': True},
				CGEOptionTypes.CGE_OPTION_ADDITIONAL_CITY_HELP:				{'Key': "Display Additional City Help", 'Default': True},
				CGEOptionTypes.CGE_OPTION_CITY_RANK_ON_PRODUCTION_MENU:		{'Key': "Display City Rank On Production Menu", 'Default': True},
				CGEOptionTypes.CGE_OPTION_TOTAL_YIELD_FROM_CITY_FAT_CROSS:	{'Key': "Total Yield From City Fat Cross", 'Default': True},
			}

			config_US = CvConfigParser.CvConfigParser("Unit Statistics Mod Config.ini")
			if (config_US != None):
				for Option in CGEOptionCheckBox.items():
					if (Option[1]['Section'] == "Unit Statistics Mod"):
						#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
						Value = config_US.getboolean(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
						gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}

				for Option in CGEOptionDropDown.items():
					if (Option[1]['Section'] == "Unit Statistics Mod"):
						#CvUtil.pyPrint("CGEOption: " + Option[0] + ", " + Option[1]['Section'] +  ", " + Option[1]['Key'])
						Value = config_US.getint(Option[1]['Section'], Option[1]['Key'], Option[1]['Default'])
						gOptionDict[Option[0]] = {'Section': Option[1]['Section'], 'Key': Option[1]['Key'], 'Default': Option[1]['Default'], 'Tab': Option[1]['Tab'], 'Value': Value, 'Modified': False}

	def getColorIndex(self):
		# color value = index + 2
		ColorIndex = ()
		for Index in CGEOptionColorIndex:
			ColorIndex += (localText.getText("TXT_KEY_CGE_OPTSCR_" + Index, ()), )

		return ColorIndex

	def getValue(self, OptionName):
		global gOptionDict

		result = gOptionDict[OptionName]['Value']
		return result

	def setDefaultValue(self, OptionName):
		global gOptionDict

		default = gOptionDict[OptionName]['Default']
		value = gOptionDict[OptionName]['Value']

		if (default != value):
			gOptionDict[OptionName]['Value'] = default
			gOptionDict[OptionName]['Modified'] = True
		return default
			#return True
		#return False

	def setValue(self, OptionName, Value):
		global gOptionDict

		#CvUtil.pyPrint("CGE set option: %s, %s"%(OptionName, Value))
		gOptionDict[OptionName]['Value'] = Value
		gOptionDict[OptionName]['Modified'] = True

		Section = gOptionDict[OptionName]['Section']
		Key = gOptionDict[OptionName]['Key']

		Function = gOptionSetFunction[Section]
		if (Section == "CGEDLL"):
			Function = self
		elif (Function == None):
			return
		Function.setCGEOption(Section, Key, Value)

	def writeINIFile(self):
		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")

		bConfigModified = False
		if (config != None and config.getINIFileName() != ""):
			for Option in CGEOptionCheckBox.items():
				if (gOptionDict[Option[0]]['Modified'] and gOptionDict[Option[0]]['Section'] != "Unit Statistics Mod"):
					#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
					config.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
					bConfigModified = True

			for Option in CGEOptionInt.items():
				if (gOptionDict[Option[0]]['Modified']):
					#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
					config.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
					bConfigModified = True

			for Option in CGEOptionFloat.items():
				if (gOptionDict[Option[0]]['Modified']):
					#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
					config.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
					bConfigModified = True

			for Option in CGEOptionDropDown.items():
				if (gOptionDict[Option[0]]['Modified'] and gOptionDict[Option[0]]['Section'] != "Unit Statistics Mod"):
					#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
					config.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
					bConfigModified = True

			for Option in CGEOptionDropDownColor.items():
				if (gOptionDict[Option[0]]['Modified']):
					#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
					config.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
					bConfigModified = True

			if (bConfigModified):
				config.writeINIfile()

		bHasCGEDLL = False
		#try:
		#	if (gc.isCGEBuild()):
		#		bHasCGEDLL = True
		#except:
		#	bHasCGEDLL = False

		if (bHasCGEDLL):
			bConfigModified = False
			config_US = CvConfigParser.CvConfigParser("Unit Statistics Mod Config.ini")
			if (config_US != None and config_US.getINIFileName() != ""):
				for Option in CGEOptionCheckBox.items():
					if (gOptionDict[Option[0]]['Modified'] and gOptionDict[Option[0]]['Section'] == "Unit Statistics Mod"):
						#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
						config_US.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
						bConfigModified = True

				for Option in CGEOptionDropDown.items():
					if (gOptionDict[Option[0]]['Modified'] and gOptionDict[Option[0]]['Section'] == "Unit Statistics Mod"):
						#CvUtil.pyPrint("CGE Write option: %s, %s, %s"%(Option[0], gOptionDict[Option[0]], gOptionDict[Option[0]]['Value']))
						config_US.setOption(gOptionDict[Option[0]]['Section'], gOptionDict[Option[0]]['Key'], str(gOptionDict[Option[0]]['Value']))
						bConfigModified = True

			if (bConfigModified):
				config_US.writeINIfile()

	def setCGEDLLOptions(self):
		bHasCGEDLL = False
		#try:
		#	if (gc.isCGEBuild()):
		#		bHasCGEDLL = True
		#except:
		#	return

		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")

		if (config != None and bHasCGEDLL):
			for Option in CGEDLLOptions.items():
					Value = config.getboolean("CGEDLL", Option[1]['Key'], Option[1]['Default'])
					gc.getGame().setCGEOption(Option[0], Value)

	def setCGEOption(self, Section, Key, Value):
		for Option in CGEDLLOptions.items():
			if (Option[1]['Key'] == Key):
				gc.getGame().setCGEOption(Option[0], Value)
				break
		return
		