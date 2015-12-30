## Addon Event Manager Project
## Changes copyright Shin 2006
## (if any portion of this copyright should be found to be void, the remainder shall remain in full effect)
##
## PlayerUtils
#
# --Shin
# (aka. Belizan)

from CvPythonExtensions import *
from types import *
import random
import cPickle

gc = CyGlobalContext()

def initPlayerDictionary(pPlayer):
	playerDict = {}
	pPlayer.setScriptData(cPickle.dumps(playerDict))

def getPlayerDictionary(pPlayer):
	if (pPlayer.getScriptData() != ""):
		playerDict = cPickle.loads(pPlayer.getScriptData())
	else:
		playerDict = {}
	return playerDict

def setPlayerDictionary(pPlayer, playerDict):
	pPlayer.setScriptData(cPickle.dumps(playerDict))

def getPlayerDictionaryValue(pPlayer, sValue):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key(sValue)):
		return playerDict[sValue]
	else:
		return -1

def setPlayerDictionaryValue(pPlayer, sValKey, oValue):
	playerDict = getPlayerDictionary(pPlayer)
	playerDict[sValKey] = oValue
	setPlayerDictionary(pPlayer, playerDict)

def increasePlayerDictionaryValue(pPlayer, sValKey, iIncrement):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key(sValKey)):
		playerDict[sValKey] = playerDict[sValKey] + iIncrement
	else:
		playerDict[sValKey] = iIncrement
	setPlayerDictionary(pPlayer, playerDict)
	return playerDict[sValKey]

def removePlayerDictionaryValue(pPlayer, sValKey):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key(sValKey)):
		del playerDict[sValKey]
	setPlayerDictionary(pPlayer, playerDict)

def addToCounter(pPlayer, sCounter, iVal):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key(sCounter)):
		playerDict[sCounter] = playerDict[sCounter] + iVal
	else:
		playerDict[sCounter] = iVal
	setPlayerDictionary(pPlayer, playerDict)
	return playerDict[sCounter]

def resetCounter(pPlayer, sCounter):
	playerDict = getPlayerDictionary(pPlayer)
	playerDict[sCounter] = 0
	setPlayerDictionary(pPlayer, playerDict)

def getCounter(pPlayer, sCounter):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key(sCounter)):
		return playerDict[sCounter]
	else:
		return 0

def getGameOptionsDictionary(pPlayer):
	playerDict = getPlayerDictionary(pPlayer)
	if(playerDict.has_key("GameOptions")):
		return playerDict["GameOptions"]
	else:
		return {}

def setGameOptionsDictionary(pPlayer, dOptions):
	playerDict = getPlayerDictionary(pPlayer)
	playerDict["GameOptions"] = dOptions
	setPlayerDictionary(pPlayer, playerDict)

def getGameOption(pPlayer, sValKey):
	dOptions = getGameOptionsDictionary(pPlayer)
	if(dOptions.has_key(sValKey)):
		return dOptions[sValKey]
	else:
		return -1

def setGameOption(pPlayer, sValKey, sValue):
	dOptions = getGameOptionsDictionary(pPlayer)
	dOptions[sValKey] = sValue
	setGameOptionsDictionary(pPlayer, dOptions)

def addSignToList(pPlayer, pPlot):
	lSigns = PlayerUtils.getPlayerDictionaryValue(pPlayer, "SignsList")
	if(lSigns != -1):
		lSigns.append((pPlot.getX(), pPlot.getY()))
	else:
		lSigns = []
		lSigns.append((pPlot.getX(), pPlot.getY()))
	PlayerUtils.setPlayerDictionaryValue(pPlayer, "SignsList", lSigns)

# so inefficient it's funny
def removeSignFromList(pPlayer, pPlot):
	lSigns = PlayerUtils.getPlayerDictionaryValue(pPlayer, "SignsList")
	if(lSigns == -1):
		return
	else:
		for tPair in lSigns:
			if(pPlot.at(tPair[0], tPair[1])):
				lSigns.remove(tPair)
				break
		PlayerUtils.setPlayerDictionaryValue(pPlayer, "SignsList", lSigns)

def removeSiteFromList(pPlayer, pPlot):
	lSites = getPlayerDictionaryValue(pPlayer, "SiteList")
	if(lSites != -1):
		for tPair in lSites:
			if(pPlot.at(tPair[0], tPair[1])):
				lSites.remove(tPair)
				break
		setPlayerDictionaryValue(pPlayer, "SiteList", lSites)

def addSiteToList(pPlayer, pPlot):
	lSites = getPlayerDictionaryValue(pPlayer, "SiteList")
	if(lSites == -1):
		lSites = []
	lSites.append((pPlot.getX(), pPlot.getY()))
	setPlayerDictionaryValue(pPlayer, "SiteList", lSites)

def colorizeCityPlots(pPlayer):
	CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
	for iDX in xrange(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iDX)
		iX = pCity.getX()
		iY = pCity.getY()
		sColor = "COLOR_WHITE"
		if(CyInterface().getHeadSelectedCity() != None):
			if(pCity.getID() == CyInterface().getHeadSelectedCity().getID()):
				sColor = "COLOR_YELLOW"
		for x in xrange(-2, 3):
			for y in xrange(-2, 3):
				pTempPlot = gc.getMap().plot(iX + x, iY + y)
				if(not pTempPlot.isNone()):
					if(pTempPlot.getWorkingCity().getID() == pCity.getID()):
						CyEngine().addColoredPlotAlt(pTempPlot.getX(), pTempPlot.getY(), PlotStyles.PLOT_STYLE_BOX_OUTLINE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER, sColor, .5)

def colorizeCitySites(pPlayer):
	#CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
	lSites = getPlayerDictionaryValue(pPlayer, "SiteList")
	if(lSites != -1):
		for tPair in lSites:
			iX = tPair[0]
			iY = tPair[1]
			sColor = "COLOR_GREEN"
			for x in xrange(-2, 3):
				for y in xrange(-2, 3):
					if(abs(x) + abs(y) != 4):
						pPlot = gc.getMap().plot(iX + x, iY + y)
						if(not pPlot.isNone()):
							CyEngine().addColoredPlotAlt(pPlot.getX(), pPlot.getY(), PlotStyles.PLOT_STYLE_BOX_OUTLINE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER, sColor, .5)

def colorizeUnitsByMP(pPlayer, pPerspectivePlayer, bDraw=True, bList=False):
	# I should examine the PlotLandscapeLayers more carefully, they're way crowded right now.
	if(bDraw):
		iLayer = PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER
		CyEngine().clearColoredPlots(iLayer)

	map = CyMap()
	iW = map.getGridWidth()
	iH = map.getGridHeight()
	iPlayer = pPlayer.getID()
	barbPlots = []  # [mp, x, y]
	#Faster to sweep visible plots or all barbarian units I wonder...
	for x in xrange(iW):
		for y in xrange(iH):
			pPlot = map.plot(x,y)
			mp = 0
			mmp = 0
			if(pPlot.isVisible(pPerspectivePlayer.getTeam(), False)):
				if(pPlot.getNumUnits() > 0):
					for idx in range(pPlot.getNumUnits()):
						pUnit = pPlot.getUnit(idx)
						if(pUnit.getOwner() == iPlayer):
							#mp = pUnit.getMoves()
							mp = pUnit.baseMoves()
							#message = "Test.. %d, %d with new %d, and old %d" %(x, y, mp, mmp)
                            #CyInterface().addMessage(gc.getActivePlayer().getID(),True,len(message),message,'',0,'Art/Interface/Buttons/actions/Recon.dds',ColorTypes(8),x,y,True,True)

							if(mp > mmp):
								mmp = mp
				if(mmp > 0):
					barbPlots.append([mmp, x, y, gc.getUnitInfo(pUnit.getUnitType()).getButton()])

	for entry in barbPlots:
		iMP = entry[0]
		iX = entry[1]
		iY = entry[2]
		sButton = entry[3]
		if(bList):
			if(iMP == 1):
				iColor = 6
			elif(iMP == 2):
				iColor = 8
			elif(iMP == 3):
				iColor = 7 
			elif(iMP == 4):
				iColor = 5
			else:
				iColor = 9
			message = "Barbarians at (%d, %d) with %d move(s)." %(iX, iY, iMP)
			CyInterface().addMessage(gc.getActivePlayer().getID(),True,len(message),message,'',0,sButton,ColorTypes(iColor),iX,iY,True,True)

		if(bDraw):
			# Alternate alpha values for more flexibility?
			if(iMP == 1):
				sColor = "COLOR_YELLOW"
				fAlpha = .4
			elif(iMP == 2):
				sColor = "COLOR_YELLOW"
				fAlpha = .9
			elif(iMP == 3):
				sColor = "COLOR_RED"
				fAlpha = .4
			elif(iMP == 4):
				sColor = "COLOR_RED"
				fAlpha = .9
			else:
				sColor = "COLOR_PLAYER_DARK_RED"
				fAlpha = .7
			CyEngine().addColoredPlotAlt(iX, iY, PlotStyles.PLOT_STYLE_BOX_OUTLINE, iLayer, sColor, fAlpha)

def getLeaderInfo(pPlayer):
	iLd = pPlayer.getLeaderType()
	pLeaderHeadInfo = gc.getLeaderHeadInfo(iLd)
	return pLeaderHeadInfo

def getFlavorValue(pPlayer, eFlavor):
	pLeader = getLeaderInfo(pPlayer)

	# gc.getFlavorTypes(int)  gc.getNumFlavorTypes()
	for iDX in xrange(gc.getNumFlavorTypes()):
		if(gc.getFlavorTypes(iDX) == eFlavor):
			iFlavor = iDX
			break

	return pLeader.getFlavorValue(iFlavor)

def hasTrait(pPlayer, eTrait):
	pLeader = getLeaderInfo(pPlayer)
	iTrait = gc.getInfoTypeForString(eTrait)
	if(iTrait == -1):
		return False

	return pLeader.hasTrait(iTrait)
