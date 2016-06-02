# City Infomation Panel on Prduction Selection
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import CvScreensInterface
import CvConfigParser
import Popup as PyPopup
import sre
#import time

ArtFileMgr = CyArtFileMgr()

# globals
gc = CyGlobalContext()
localText = CyTranslator()
isShowCityInfoPanelPS = False
victory = False
pOldPlot = 0
NationalWonderList = []
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
CFG_EnabledCityInfoPanelPS = config.getboolean("City Info Panel", "Enabled",  True)
CFG_INFOPANE_PIX_PER_LINE_1 = config.getint("APL Info Pane", "Pixel Per Line Type 1", 15)
CFG_INFOPANE_PIX_PER_LINE_2 = config.getint("APL Info Pane", "Pixel Per Line Type 2", 20)

# sre compile
removeTag = sre.compile(r'<font=.*?>|</font>|<color=.*?>|</color>|<link=.*?>|</link>')
removeColor = sre.compile(r'<color=.*?>|</color>')

class CityInfoPanelPS:

	def Init(self):

		self.positionX = 150
		self.positionY = 150
		self.width = 215
		self.height = 343

		self.CITY_INFO_PANE			= "CIPS_INFO_PANE"
		self.CITY_INFO_TEXT			= "CIPS_INFO_TEXT"
		self.CITY_INFO_TEXT_SHADOW	= "CIPS_INFO_TEXT_SHADOW"

	def createCityInfoPanelPS(self):
		global CFG_EnabledCityInfoPanelPS
		global NationalWonderList

		self.Init()
		if (CyUserProfile().getPlayerOption(PlayerOptionTypes.PLAYEROPTION_MINIMIZE_POP_UPS)):
			CFG_EnabledCityInfoPanelPS = False

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.addPanel( "CIPSBackground", u"", u"", True, False, self.positionX, self.positionY, self.width, self.height, PanelStyles.PANEL_STYLE_TECH )
		screen.hide( "CIPSBackground" )

		NationalWonderList = [iBuilding for iBuilding in range(gc.getNumBuildingInfos()) if (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()))]
		NationalWonderList.remove(gc.getInfoTypeForString("BUILDING_PALACE"))

		return 0

	def setVictory(self):
		global victory

		victory = True

	def resetVictory(self):
		global victory

		victory = False

	def setCGEOption(self, Section, Key, Value):
		global CFG_EnabledCityInfoPanelPS

		if (Key == "Enabled"):
			CFG_EnabledCityInfoPanelPS = Value

	def hideCityInfoPanelPS(self):
		global isShowCityInfoPanelPS
		global CFG_EnabledCityInfoPanelPS

		if (not isShowCityInfoPanelPS):
			return

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "CIPSBackground" )
		screen.hide( "CIPSCityName" )
		screen.hide( "CIPSCityNameShadow" )
		screen.hide( "CIPSText1" )
		screen.hide( "CIPSText2" )

		isShowCityInfoPanelPS = False
		return 0

	def toggleCityInfoPanelPS(self, pCity):
		global isShowCityInfoPanelPS
		if (isShowCityInfoPanelPS):
			self.hideCityInfoPanelPS()
			isShowCityInfoPanelPS = False
		else:
			self.showCityInfoPanel(pCity)
			isShowCityInfoPanelPS = True

	def showCityInfoPanelPS(self, pCity):
		global victory
		global CFG_EnabledCityInfoPanelPS

		if (CyUserProfile().getPlayerOption(PlayerOptionTypes.PLAYEROPTION_MINIMIZE_POP_UPS)):
			CFG_EnabledCityInfoPanelPS = False

		if (CFG_EnabledCityInfoPanelPS and (not victory)):
			self.showCityInfoPanel(pCity)

	def showCityInfoPanel(self, pCity):
		global isShowCityInfoPanelPS
		self.Init()

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "CIPSBackground" )
		screen.hide( "CIPSCityName" )
		screen.hide( "CIPSCityNameShadow" )
		screen.hide( "CIPSText1" )
		screen.hide( "CIPSText2" )

		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		cityList = []
		iNumCity = pActivePlayer.getNumCities()

		cityListappend = cityList.append
		(pLoopCity, iter) = pActivePlayer.firstCity(False)
		while(pLoopCity):
			cityListappend(pLoopCity)
			(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

		sortMaintenance = [pLoopCity.getMaintenanceTimes100() for pLoopCity in cityList]
		sortHammer      = [pLoopCity.getCurrentProductionDifference(True, False) for pLoopCity in cityList]
		sortCommerce    = [pLoopCity.getYieldRate(YieldTypes.YIELD_COMMERCE) for pLoopCity in cityList]
		sortGold        = [pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_GOLD) for pLoopCity in cityList]
		sortResearch    = [pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) for pLoopCity in cityList]
		sortCulture     = [pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) for pLoopCity in cityList]
		sortGreatPeople = [pLoopCity.getGreatPeopleRate() for pLoopCity in cityList]
		sortEspionage   = [pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_ESPIONAGE) for pLoopCity in cityList]

		sortMaintenance.sort()
		sortHammer.sort()
		sortCommerce.sort()
		sortGold.sort()
		sortResearch.sort()
		sortCulture.sort()
		sortGreatPeople.sort()
		sortEspionage.sort()

		sortMaintenance.reverse()
		sortHammer.reverse()
		sortCommerce.reverse()
		sortGold.reverse()
		sortResearch.reverse()
		sortCulture.reverse()
		sortGreatPeople.reverse()
		sortEspionage.reverse()

		GetText = localText.getText
		szHappy       = GetText('TXT_CITY_INFO_PANEL_HAPPY', ())
		szHealth      = GetText('TXT_CITY_INFO_PANEL_HEALTH', ())
		szFood        = GetText('TXT_CITY_INFO_PANEL_FOOD', ())
		szMaintenance = GetText('TXT_CITY_INFO_PANEL_MAINTENANCE', ()) + str(sortMaintenance.index(pCity.getMaintenanceTimes100()) + 1)
		szHammer      = GetText('TXT_CITY_INFO_PANEL_HAMMER', ()) + str(sortHammer.index(pCity.getCurrentProductionDifference(True, False)) + 1)
		szCommerce    = GetText('TXT_CITY_INFO_PANEL_COMMERCE', ()) + str(sortCommerce.index(pCity.getYieldRate(YieldTypes.YIELD_COMMERCE)) + 1)
		szGold        = GetText('TXT_CITY_INFO_PANEL_GOLD', ()) + str(sortGold.index(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_GOLD)) + 1)
		szResearch    = GetText('TXT_CITY_INFO_PANEL_RESEARCH', ()) + str(sortResearch.index(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH)) + 1)
		szEspionage   = GetText('TXT_CITY_INFO_PANEL_ESPIONAGE', ()) + str(sortEspionage.index(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_ESPIONAGE)) + 1)
		szCulture     = GetText('TXT_CITY_INFO_PANEL_CULTURE', ()) + str(sortCulture.index(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)) + 1)
		szGreatPeople = GetText('TXT_CITY_INFO_PANEL_GREAT_PEOPLE', ()) + str(sortGreatPeople.index(pCity.getGreatPeopleRate()) + 1)

		szAutomation  = GetText('TXT_CITY_INFO_PANEL_AUTOMATION', ())
		szNationalWonder = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR) + GetText('TXT_KEY_PEDIA_NATIONAL_WONDER', ()) + u":"

		szText1 = szHappy + u"\n" + szHealth + u"\n" + szFood + u"\n" + szMaintenance + u"\n" + szHammer + u"\n" + szCommerce + u"\n" + szGold + u"\n" + szResearch + u"\n" + szEspionage + u"\n" + szCulture + u"\n" + szGreatPeople + u"\n" + szAutomation + u"\n" + szNationalWonder

		iCivicsBonus = pCity.getMilitaryHappiness() + pCity.getLargestCityHappiness() + pCity.getReligionGoodHappiness() + pCity.getFeatureGoodHappiness() + pCity.getBuildingHappiness(gc.getInfoTypeForString("BUILDING_BARRACKS"))
		if (pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_GLOBE_THEATRE")) != 0):
			szHappy = u"%c%s"%(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR), localText.getText('TXT_KEY_BUILDING_GLOBE_THEATRE', ()))
		else:
			if (pCity.happyLevel() - pCity.unhappyLevel(0) < 0):
				szHappy = u"%c<color=255,0,0,255> %+d</color>(%d)"%(CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR), pCity.happyLevel() - pCity.unhappyLevel(0), iCivicsBonus)
			else:
				szHappy = u"%c %+d(%d)"%(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR), pCity.happyLevel() - pCity.unhappyLevel(0), iCivicsBonus)
		if (pCity.goodHealth() - pCity.badHealth(False) < 0):
			szHealth = u"%c<color=255,0,0,255> %+d </color>"%(CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR), pCity.goodHealth() - pCity.badHealth(False))
		else:
			szHealth = u"%c %+d "%(CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR), pCity.goodHealth() - pCity.badHealth(False))
		szGold = u"%.2f %c"%(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_GOLD)/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		if (pCity.getCurrentProductionDifference(True, False) == pCity.getBaseYieldRate(YieldTypes.YIELD_PRODUCTION)):
			szHammer = u"%d %c"%(pCity.getCurrentProductionDifference(True, False), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
		else:
			szHammer = u"%d(%d) %c"%(pCity.getCurrentProductionDifference(True, False), pCity.getBaseYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
		if (pCity.isFoodProduction()):
			nFood = pCity.getCurrentProductionDifference(False, False) - pCity.getCurrentProductionDifference(True, False)
		else:
			nFood = pCity.foodDifference(True)
		szFood = u"%d %c"%(nFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
		szMaintenance = u"%.2f %c"%(pCity.getMaintenanceTimes100()/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		if (pCity.getYieldRate(YieldTypes.YIELD_COMMERCE) == pCity.getBaseYieldRate(YieldTypes.YIELD_COMMERCE)):
			szCommerce = u"%d %c"%(pCity.getYieldRate(YieldTypes.YIELD_COMMERCE), gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar())
		else:
			szCommerce = u"%d(%d) %c"%(pCity.getYieldRate(YieldTypes.YIELD_COMMERCE), pCity.getBaseYieldRate(YieldTypes.YIELD_COMMERCE), gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar())
		szResearch = u"%.2f %c"%(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH)/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		szEspionage = u"%.2f %c"%(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_ESPIONAGE)/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
		szCulture = u"%.2f %c"%(pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)/100.0, gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
		szGreatPeople = u"%d %c"%(pCity.getGreatPeopleRate(), CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR))

		AUTOMATION_ICON_DICT = {
			0 : unichr(gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()), # Emphasize Food
			1 : unichr(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()), # Emphasize Production
			2 : unichr(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()), # Emphasize Commerce
			3 : unichr(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()), # Emphasize Research
			4 : unichr(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)), # Emphasize GP
			5 : "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_AVOID_GROWTH").getPath() + " size=18></img>" # Emphasize Avoid Growth
		}

		nNumEmphasize = len(AUTOMATION_ICON_DICT)
		szAutomation = u""
		IsEmphasize = pCity.AI_isEmphasize
		if pCity.isCitizensAutomated():
			szAutomation += "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_CITIZENS_AUTOMATED").getPath() + " size=18></img>"
		if pCity.isProductionAutomated():
			szAutomation += "<img=" + ArtFileMgr.getInterfaceArtInfo("CGE_AUTOMATED_PRODUCTION_AUTOMATED").getPath() + " size=18></img>"
		for i in xrange(nNumEmphasize):
			nNum = nNumEmphasize - i - 1
			if (IsEmphasize(nNum)):
				szAutomation += AUTOMATION_ICON_DICT[nNum]
		szAutomation += unichr(ord(unichr(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar())) +1)

		if (CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)):
			szNationalWonder = u"\n%d/%d"%(pCity.getNumNationalWonders(), gc.getDefineINT("MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC"))
		else:
			szNationalWonder = u"<font=1>\n"
			for iBuilding in NationalWonderList:
				if (pCity.getNumBuilding(iBuilding) > 0):
					szNationalWonder += gc.getBuildingInfo(iBuilding).getDescription() + "\n"
			szNationalWonder += u"</font>"

		szText2 = szHappy + u"\n" + szHealth + u"\n" + szFood + u"\n" + szMaintenance + u"\n" + szHammer + u"\n" + szCommerce + u"\n" + szGold + u"\n" + szResearch + u"\n" + szEspionage + u"\n" + szCulture + u"\n" + szGreatPeople + u"\n" + szAutomation + szNationalWonder

		screen.moveToFront("CIPSBackground")
		screen.show("CIPSBackground")

		screen.setText( "CIPSCityNameShadow", "Background", localText.changeTextColor(pCity.getName(), gc.getInfoTypeForString("COLOR_BLACK")), CvUtil.FONT_CENTER_JUSTIFY, self.positionX + self.width/2 +1, self.positionY+11, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText( "CIPSCityName", "Background", pCity.getName(), CvUtil.FONT_CENTER_JUSTIFY, self.positionX + self.width/2, self.positionY+10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.addMultilineText( "CIPSText1", szText1, self.positionX + 6, self.positionY + 34, self.width, self.height, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText( "CIPSText2", szText2, self.positionX - 5, self.positionY + 34, self.width -5, self.height, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		isShowCityInfoPanelPS = True

	def showCityTerrainInfo(self, pCity):
		iForest = 0
		iJungle = 0
		iHill = 0
		iCoast = 0
		iGrass = 0
		iPlains = 0
		iFlood = 0
		iOasis = 0
		iTundra = 0
		iDesert = 0
		iPeak = 0
		iFarm = 0
		iCount = 0
		iImproveCount = 0
		iTotalHammer = 0
		iTotalCommerce = 0
		iTotalFood = 0

		iPlotX = pCity.getX()
		iPlotY = pCity.getY()
		for iXLoop in range(-2, +3):
			for iYLoop in range(-2, +3):
				if ((((iXLoop == 2) and (iYLoop == 2))) or \
					(((iXLoop == -2) and (iYLoop == 2))) or \
					(((iXLoop == 2) and (iYLoop == -2))) or \
					(((iXLoop == -2) and (iYLoop == -2))) or \
					(((iXLoop == 0) and (iYLoop == 0)))):
						continue
				lPlot = CyMap().plot(iPlotX + iXLoop, iPlotY + iYLoop)
				
				if (lPlot.isHills()):
					iHill += 1
				if (lPlot.isPeak()):
					iPeak += 1
					continue
				if (lPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_COAST")):
					iCoast += 1
				if (lPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_GRASS")):
					iGrass += 1
				if (lPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_TUNDRA")):
					iTundra += 1
				if (lPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_PLAINS")):
					iPlains += 1
				if (lPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT")):
					if (lPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")):
						iFlood += 1
					else:
						iDesert += 1

				if (lPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST")):
					iForest += 1
				if (lPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_JUNGLE")):
					iJungle += 1
				if (lPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_OASIS")):
					iOasis += 1
#				if (lPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_FARM")):
#					iFarm += 1
				iImproveCount += lPlot.getYield(YieldTypes.YIELD_FOOD)

				iTotalHammer += lPlot.calculateYield(YieldTypes.YIELD_PRODUCTION, True)
				iTotalCommerce += lPlot.calculateYield(YieldTypes.YIELD_COMMERCE, True)
				iTotalFood += lPlot.calculateYield(YieldTypes.YIELD_FOOD, True)

		iCountDiff = iFlood + iOasis - (iPlains + iCoast) - 2 * (iDesert + iPeak + iTundra) + (iFarm)
		iCount = 3 * (iFlood + iOasis) + 2 * iGrass + (iPlains + iCoast)
		popup = PyPopup.PyPopup(-1)

		popup.setHeaderString(localText.getText("TXT_KEY_CGE_FOOD_COUNT", (pCity.getName(), str(iImproveCount - (40 - 2 * (iDesert + iPeak + iTundra))), str(iCountDiff))))
		popup.setBodyString(localText.getText("TXT_KEY_CGE_FOOD_COUNT_DIFF", (iImproveCount, iCount)))
		popup.setBodyString("%dF,%dH,%dC"%(iTotalFood, iTotalHammer, iTotalCommerce))
		popup.addSeparator()

		popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("+1", ())), iFlood + iOasis))
		if (iFlood):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_FEATURE_FLOOD_PLAINS", ()), iFlood))
		if (iOasis):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_FEATURE_OASIS", ()), iOasis))
		popup.addSeparator()

		popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("0", ())), iGrass))
		if (iGrass):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_GRASS", ()), iGrass))
		popup.addSeparator()

		popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("-1", ())), iPlains + iCoast))
		if (iPlains):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_PLAINS", ()), iPlains))
		if (iCoast):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_COAST", ()), iCoast))
		if (iTundra):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_TUNDRA", ()), iTundra))
		popup.addSeparator()

		popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("-2", ())), iDesert + iTundra + iPeak))
		if (iTundra):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_TUNDRA", ()), iTundra))
		if (iDesert):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_DESERT", ()), iDesert))
		if (iPeak):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_PEAK", ()), iPeak))

		popup.addSeparator()
		if (iHill):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_TERRAIN_HILL", ()), iHill))
		if (iForest):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_FEATURE_FOREST", ()), iForest))
		if (iJungle):
			popup.setBodyString("%s: %d"%(localText.getText("TXT_KEY_FEATURE_JUNGLE", ()), iJungle))

		popup.launch(true, PopupStates.POPUPSTATE_QUEUED)

	def showCityRadiusInfo(self, pPlot):
		global pOldPlot

		if (pPlot == pOldPlot):
			return
		else:
			pOldPlot = pPlot

		szText = localText.getText("TXT_KEY_CGE_CITY_PLACEMENTS_INFO", ()) + u"\n"
		if(pPlot.isPeak() or pPlot.isWater() or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DUSTSEA") or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_CRATERRIM") or not pPlot.isRevealed(gc.getActivePlayer().getTeam(), False)):
			self.displayInfoPane("<font=2>%s\n<color=255,0,0,255>%s</color></font>"%(szText, localText.getText("TXT_KEY_CGE_CITY_PLACEMENTS_UNAVAILABLE", ())))
			return

		iForest = 0
		iJungle = 0
		iHill = 0
		iCoast = 0
		iGrass = 0
		iPlains = 0
		iFlood = 0
		iOasis = 0
		iTundra = 0
		iDesert = 0
		iPeak = 0
		iFarm = 0
		iTotalHammer = 0
		iTotalCommerce = 0
		iTotalFood = 0

		iPlotX = pPlot.getX()
		iPlotY = pPlot.getY()
		InfoTypeForStr = gc.getInfoTypeForString
		for iXLoop in xrange(-2, +3):
			for iYLoop in xrange(-2, +3):
				if ((((iXLoop == 2) and (iYLoop == 2))) or \
					(((iXLoop == -2) and (iYLoop == 2))) or \
					(((iXLoop == 2) and (iYLoop == -2))) or \
					(((iXLoop == -2) and (iYLoop == -2))) or \
					(((iXLoop == 0) and (iYLoop == 0)))):
						continue
				lPlot = CyMap().plot(iPlotX + iXLoop, iPlotY + iYLoop)
				lPlotTerrainType = lPlot.getTerrainType()
				lPlotFeatureType = lPlot.getFeatureType()
				lPlotcalcYield = lPlot.calculateYield

				if (lPlot.isHills()):
					iHill += 1
				if (lPlot.isPeak()):
					iPeak += 1
					continue
				if (lPlotTerrainType == InfoTypeForStr("TERRAIN_COAST")):
					iCoast += 1
				if (lPlotTerrainType == InfoTypeForStr("TERRAIN_GRASS")):
					iGrass += 1
				if (lPlotTerrainType == InfoTypeForStr("TERRAIN_TUNDRA")):
					iTundra += 1
				if (lPlotTerrainType == InfoTypeForStr("TERRAIN_PLAINS")):
					iPlains += 1
				if (lPlotTerrainType == InfoTypeForStr("TERRAIN_DESERT")):
					if (lPlotFeatureType == InfoTypeForStr("FEATURE_FLOOD_PLAINS")):
						iFlood += 1
					else:
						iDesert += 1

				if (lPlotFeatureType == InfoTypeForStr("FEATURE_FOREST")):
					iForest += 1
				if (lPlotFeatureType == InfoTypeForStr("FEATURE_JUNGLE")):
					iJungle += 1
				if (lPlotFeatureType == InfoTypeForStr("FEATURE_OASIS")):
					iOasis += 1

				iTotalHammer += lPlotcalcYield(YieldTypes.YIELD_PRODUCTION, True)
				iTotalCommerce += lPlotcalcYield(YieldTypes.YIELD_COMMERCE, True)
				iTotalFood += lPlotcalcYield(YieldTypes.YIELD_FOOD, True)

		szText = "%s%s\n"%(szText, localText.getText("TXT_KEY_CGE_CITY_PLACEMENTS_YIELD_COUNT", (iTotalFood, iTotalHammer, iTotalCommerce)))

		szText = "%s\n%s: %d\n"%(szText, localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("+1", ())), iFlood + iOasis)
		if (iFlood):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_FEATURE_FLOOD_PLAINS", ()), iFlood)
		if (iOasis):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_FEATURE_OASIS", ()), iOasis)


		szText = "%s\n%s: %d\n"%(szText, localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("0", ())), iGrass)
		if (iGrass):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_GRASS", ()), iGrass)


		szText = "%s\n%s: %d\n"%(szText, localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("-1", ())), iPlains + iCoast)
		if (iPlains):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_PLAINS", ()), iPlains)
		if (iCoast):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_COAST", ()), iCoast)
		if (iTundra):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_TUNDRA", ()), iTundra)


		szText = "%s\n%s: %d\n"%(szText, localText.getText("TXT_KEY_CGE_FOOD_SQUARE", ("-2", ())), iDesert + iTundra + iPeak)
		if (iTundra):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_TUNDRA", ()), iTundra)
		if (iDesert):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_DESERT", ()), iDesert)
		if (iPeak):
			szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_PEAK", ()), iPeak)

		if (iHill or iForest or iJungle):
			szText = "%s\n"%(szText)
		if (iHill):
			if (iForest or iJungle):
				szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_TERRAIN_HILL", ()), iHill)
			else:
				szText = "%s%s: %d"%(szText, localText.getText("TXT_KEY_TERRAIN_HILL", ()), iHill)
		if (iForest):
			if (iJungle):
				szText = "%s%s: %d\n"%(szText, localText.getText("TXT_KEY_FEATURE_FOREST", ()), iForest)
			else:
				szText = "%s%s: %d"%(szText, localText.getText("TXT_KEY_FEATURE_FOREST", ()), iForest)
		if (iJungle):
			szText = "%s%s: %d"%(szText, localText.getText("TXT_KEY_FEATURE_JUNGLE", ()), iJungle)

		self.displayInfoPane("<font=2>%s</font>"%(szText))

	def displayInfoPane(self, szText):

		self.Init()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# calculate text size
		dy = self.getTextLines(szText)

		# draw panel
		y = 300

		screen.hide(self.CITY_INFO_PANE)
		screen.hide(self.CITY_INFO_TEXT)
		screen.hide(self.CITY_INFO_TEXT_SHADOW)

		screen.setPanelSize(self.CITY_INFO_PANE, 5, y, 290, dy)

		# create shadow text
		szTextBlack = localText.changeTextColor(removeColor.sub("", szText), gc.getInfoTypeForString("COLOR_BLACK"))

		# display shadow text
		screen.addMultilineText(self.CITY_INFO_TEXT_SHADOW, szTextBlack, 10, y + 12, 287, dy - 3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		# display text
		screen.addMultilineText(self.CITY_INFO_TEXT, szText, 9, y + 10, 287, dy - 3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.show(self.CITY_INFO_PANE)
		screen.show(self.CITY_INFO_TEXT)
		screen.show(self.CITY_INFO_TEXT_SHADOW)

	def hideInfoPane(self):
		self.Init()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide(self.CITY_INFO_TEXT)
		screen.hide(self.CITY_INFO_TEXT_SHADOW)
		screen.hide(self.CITY_INFO_PANE)

	def getTextLines(self, szText):
		szText = removeTag.sub("", szText)
		iNormalLines = 0
		iBulletLines = 0
		lChapters = szText.split('\n')
		sComp = u"%c"%CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		for LooplChapters in lChapters:
			iWidth = CyInterface().determineWidth(LooplChapters)/(287)+1
			if (LooplChapters.find(sComp) != -1):
				iBulletLines += iWidth
			else:
				iNormalLines += iWidth
		dy = iNormalLines*CFG_INFOPANE_PIX_PER_LINE_1 + (iBulletLines)*CFG_INFOPANE_PIX_PER_LINE_2 + 10
		return dy
