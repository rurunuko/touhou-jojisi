## Colonize the Moon Mod Project
## Changes copyright Shin 2005
## (if any portion of this copyright should be found to be void, the remainder shall remain in full effect)
##
## CityUtils
#
# --Shin
# (aka. Belizan)

from CvPythonExtensions import *
from types import *
import random
import string
import cPickle

gc = CyGlobalContext()
gExistCityGrid = set()

def initCityDictionary(pCity):
	cityDict = {}
	pCity.setScriptData(cPickle.dumps(cityDict))

def getCityDictionary(pCity):
	if(pCity.getScriptData() != ""):
		cityDict = cPickle.loads(pCity.getScriptData())
	else:
		cityDict = {}
	return cityDict

def setCityDictionary(pCity, cityDict):
	pCity.setScriptData(cPickle.dumps(cityDict))

def getCityDictionaryValue(pCity, sValKey):
	cityDict = getCityDictionary(pCity)
	if(cityDict.has_key(sValKey)):
		return cityDict[sValKey]
	else:
		return 0

def setCityDictionaryValue(pCity, sValKey, oVal):
	cityDict = getCityDictionary(pCity)
	cityDict[sValKey] = oVal
	setCityDictionary(pCity, cityDict)

def increaseCityDictionaryValue(pCity, sValKey, iIncrement):
	cityDict = getCityDictionary(pCity)
	cityDict[sValKey] = cityDict[sValKey] + iIncrement
	setCityDictionary(pCity, cityDict)
	return cityDict[sValKey]

def removeCityDictionaryValue(pCity, sValKey):
	cityDict = getCityDictionary(pCity)
	if(cityDict.has_key(sValKey)):
		del cityDict[sValKey]
	setCityDictionary(pCity, cityDict)

def setArchitecture(pCity, sArchitecture):
	cityDict = getCityDictionary(pCity)
	cityDict["architecture"] = sArchitecture
	setCityDictionary(pCity, cityDict)

def getArchitecture(pCity):
	cityDict = getCityDictionary(pCity)
	if(cityDict.has_key("architecture")):
		return cityDict["architecture"]
	else:
		return "Default"

def clearRecentCombat(pCity):
	cityDict = getCityDictionary(pCity)
	cityDict["recentCombat"] = 0
	setCityDictionary(pCity, cityDict)

def pushRecentCombat(pCity):
	cityDict = getCityDictionary(pCity)
	if(cityDict.has_key("recentCombat")):
		iRC = cityDict["recentCombat"] + 1
	else:
		iRC = 1
	cityDict["recentCombat"] = iRC
	setCityDictionary(pCity, cityDict)
	return iRC

def colorizeCityGridForPlot(pPlot, pPlayer):
	if(pPlot.isNone()):
		return
	if(pPlot.isPeak() or pPlot.isWater() or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DUSTSEA") or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_CRATERRIM") or not pPlot.isRevealed(pPlayer.getTeam(), False)):
		CyEngine().addColoredPlotAlt(pPlot.getX(), pPlot.getY(), PlotStyles.PLOT_STYLE_BOX_OUTLINE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER, "COLOR_RED", .7)
		return

	SiteSet = set()
	SiteSetadd = SiteSet.add
	if (pPlayer.getScriptData() != ""):
		playerDict = cPickle.loads(pPlayer.getScriptData())
		if (playerDict.has_key("SiteList")):
			for (iX, iY) in playerDict["SiteList"]:
				for x in xrange(-2, 3):
					for y in xrange(-2, 3):
						if (abs(x) + abs(y) != 4):
							pTempPlot = gc.getMap().plot(iX + x, iY + y)
							if (not pTempPlot.isNone()):
								SiteSetadd((iX + x, iY + y))

	iX = pPlot.getX()
	iY = pPlot.getY()
	for x in xrange(-2, 3):
		for y in xrange(-2, 3):
			if(abs(x) + abs(y) != 4):
				iTempX = iX + x
				iTempY = iY + y
				pTempPlot = gc.getMap().plot(iTempX, iTempY)
				if(not pTempPlot.isNone()):
					if ((iTempX, iTempY) in gExistCityGrid):
						sColor = "COLOR_PLAYER_DARK_RED"
					elif ((iTempX, iTempY) in SiteSet):
						sColor = "COLOR_YELLOW"
					else:
						sColor = "COLOR_CYAN"
					CyEngine().addColoredPlotAlt(iTempX, iTempY, PlotStyles.PLOT_STYLE_BOX_OUTLINE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER, sColor, .7)

def InitExistCityGrid():
	global gExistCityGrid

	gExistCityGrid = set()
	gExistCityGridadd = gExistCityGrid.add

	pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
	(pLoopCity, iter) = pActivePlayer.firstCity(False)
	while (pLoopCity):
		iX = pLoopCity.getX()
		iY = pLoopCity.getY()
		for x in xrange(-2, 3):
			for y in xrange(-2, 3):
				pTempPlot = gc.getMap().plot(iX + x, iY + y)
				if (not pTempPlot.isNone()):
					if (pTempPlot.getWorkingCity().getID() == pLoopCity.getID()):
						gExistCityGridadd((iX + x, iY + y))
		(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)
