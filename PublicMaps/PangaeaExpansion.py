#
#	FILE:	 PangaeaExpansion.py
#	AUTHOR:  Bob Thomas (Sirian)
#	CONTRIB: Soren Johnson, Andy Szybalski
#	MODDER:  Fuming
#	VERSION: 1.03fix1
#	PURPOSE: Global map script - Simulates a Pan-Earth SuperContinent
#-----------------------------------------------------------------------------
#	Copyright (c) 2005 Firaxis Games, Inc. All rights reserved.
#-----------------------------------------------------------------------------
#

import random

from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import MultilayeredFractal
from CvMapGeneratorUtil import HintedWorld
from CvMapGeneratorUtil import TerrainGenerator
from CvMapGeneratorUtil import FeatureGenerator
from CvMapGeneratorUtil import BonusBalancer
import Arboria
import Rainforest
import Tectonics

balancer = BonusBalancer()

def getDescription():
	return "TXT_KEY_MAP_SCRIPT_PANGAEA_DESCR"

def getNumCustomMapOptions():
	return 11

def getNumHiddenCustomMapOptions():
	return 10

def getCustomMapOptionName(argsList):
	[iOption] = argsList
	option_names = {
		0:	"TXT_KEY_MAP_SCRIPT_SHORELINE",
		1:	"TXT_KEY_MAP_WORLD_WRAP",
		2:  "TXT_KEY_CONCEPT_RESOURCES",
		3:  "TXT_KEY_PANGAEA_EXPANSION_RIVER_START",
		4:  "TXT_KEY_PANGAEA_EXPANSION_EXISTENCE_ARCHIPELAGO",
		5:  "TXT_KEY_PANGAEA_EXPANSION_RAGING_WHALE",
		6:  "TXT_KEY_PANGAEA_EXPANSION_AMOUNT_WHALE",
		7:  "TXT_KEY_PANGAEA_EXPANSION_AMOUNT_X10_WHALE",
		8: "TXT_KEY_PANGAEA_EXPANSION_TERRAIN_TYPE",
		9:  "TXT_KEY_PANGAEA_EXPANSION_FOREST_TYPE",
		10:  "TXT_KEY_PANGAEA_EXPANSION_BONUS_TYPE"
		}
	translated_text = unicode(CyTranslator().getText(option_names[iOption], ()))
	return translated_text

def getNumCustomMapOptionValues(argsList):
	[iOption] = argsList
	option_values = {
		0:	6,
		1:	3,
		2:  2,
		3:  2,
		4:  2,
		5:  5,
		6:  10,
		7:  10,
		8:  5,
		9:  4,
		10: 4
		}
	return option_values[iOption]

def getCustomMapOptionDescAt(argsList):
	[iOption, iSelection] = argsList
	selection_names = {
		0:	{
			0: "TXT_KEY_MAP_SCRIPT_RANDOM",
			1: "TXT_KEY_MAP_SCRIPT_NATURAL",
			2: "TXT_KEY_MAP_SCRIPT_PRESSED",
			3: "TXT_KEY_MAP_SCRIPT_SOLID",
			4: "TXT_KEY_PANGAEA_EXPANSION_MAP_SCRIPT_FLUID",
			5: "TXT_KEY_PANGAEA_EXPANSION_MAP_SCRIPT_TECTONICS_LIKE"
			},
		1:	{
			0: "TXT_KEY_MAP_WRAP_FLAT",
			1: "TXT_KEY_MAP_WRAP_CYLINDER",
			2: "TXT_KEY_MAP_WRAP_TOROID"
			},
		2:	{
			0: "TXT_KEY_WORLD_STANDARD",
			1: "TXT_KEY_MAP_BALANCED"
			},
		3:	{  # River start
			0: "TXT_KEY_PANGAEA_EXPANSION_DISABLE",
			1: "TXT_KEY_PANGAEA_EXPANSION_ENABLE"
			},
		4:	{
			0: "TXT_KEY_PANGAEA_EXPANSION_ALLOW_ARCHIPELAGO",
			1: "TXT_KEY_PANGAEA_EXPANSION_DISALLOW_ARCHIPELAGO"
			},
		5:	{  # Whale
			0: "TXT_KEY_PANGAEA_EXPANSION_DISABLE",
			1: "TXT_KEY_PANGAEA_EXPANSION_ENABLE",
			2: "TXT_KEY_PANGAEA_EXPANSION_RAGING_WHALE_LAKE_AND_COAST",
			3: "TXT_KEY_PANGAEA_EXPANSION_RAGING_WHALE_COAST",
			4: "TXT_KEY_PANGAEA_EXPANSION_RAGING_WHALE_LAKE"
			},
		6:	{  # x1
			0: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			1: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			2: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			3: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			4: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			5: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			6: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			7: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			8: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			9: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES"
			},
		7:	{  # x10
			0: "TXT_KEY_PANGAEA_EXPANSION_DISABLE",
			1: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			2: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			3: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			4: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			5: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			6: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			7: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			8: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES",
			9: "TXT_KEY_PANGAEA_EXPANSION_WHALE_TIMES"
			},
		8:	{
			0: "TXT_KEY_MAP_SCRIPT_RANDOM",
			1: "TXT_KEY_PANGAEA_EXPANSION_PANGAEA_LIKE",
			2: "TXT_KEY_PANGAEA_EXPANSION_ARBORIA_LIKE",
			3: "TXT_KEY_PANGAEA_EXPANSION_RAINFOREST_LIKE",
			4: "TXT_KEY_PANGAEA_EXPANSION_MAP_SCRIPT_TECTONICS_LIKE"
			},
		9:	{ 
			0: "TXT_KEY_MAP_SCRIPT_RANDOM",
			1: "TXT_KEY_PANGAEA_EXPANSION_PANGAEA_LIKE",
			2: "TXT_KEY_PANGAEA_EXPANSION_ARBORIA_LIKE",
			3: "TXT_KEY_PANGAEA_EXPANSION_RAINFOREST_LIKE"
			},
		10:	{
			0: "TXT_KEY_MAP_SCRIPT_RANDOM",
			1: "TXT_KEY_PANGAEA_EXPANSION_PANGAEA_LIKE",
			2: "TXT_KEY_PANGAEA_EXPANSION_ARBORIA_LIKE",
			3: "TXT_KEY_PANGAEA_EXPANSION_RAINFOREST_LIKE"
			}
		}
	translated_text = unicode(CyTranslator().getText(selection_names[iOption][iSelection], ()))
	if iOption == 6:  # x1 times
		translated_text = unicode(iSelection) + translated_text
	elif iOption == 7 and iSelection > 0:  # x10 times
		translated_text = u"+" + unicode(iSelection * 10) + translated_text
	return translated_text

def getCustomMapOptionDefault(argsList):
	[iOption] = argsList
	option_defaults = {
		0:	0,
		1:	1,
		2:  0,
		3:  1,
		4:  0,
		5: 0,
		6: 0,
		7: 0,
		8: 1,
		9: 1,
		10: 1
		}
	return option_defaults[iOption]

def isRandomCustomMapOption(argsList):
	[iOption] = argsList
	option_random = {
		0:	false,
		1:	false,
		2:  false,
		3:  false,
		4:  false,
		5: false,
		6: false,
		7: false,
		8: false,
		9: false,
		10: false
		}
	return option_random[iOption]

def getWrapX():
	map = CyMap()
	return (map.getCustomMapOption(1) == 1 or map.getCustomMapOption(1) == 2)

def getWrapY():
	map = CyMap()
	return (map.getCustomMapOption(1) == 2)

def normalizeAddExtras():
	if (CyMap().getCustomMapOption(2) == 1):
		balancer.normalizeAddExtras()
	CyPythonMgr().allowDefaultImpl()	# do the rest of the usual normalizeStartingPlots stuff, don't overrride

	gc = CyGlobalContext()
	cymap = CyMap()
	iOption = cymap.getCustomMapOption(7) * 10 + cymap.getCustomMapOption(6)
	iOptionRaging = cymap.getCustomMapOption(5)
	if iOptionRaging:  # raging
		bRaging = True
		bIgnoreLatitude = True
		if iOptionRaging == 1:
			bWhaleInLake = False
			bWhaleInCoast = False
		elif iOptionRaging == 2:
			bWhaleInLake = True
			bWhaleInCoast = True
		elif iOptionRaging == 3:
			bWhaleInLake = False
			bWhaleInCoast = True
		else:
			bWhaleInLake = True
			bWhaleInCoast = False
	else:
		bRaging = False
		bIgnoreLatitude = False
		
	if iOption <= 1 and not bRaging:  # normal
		return
	# reference: CvMapGenerator::calculateNumBonusesToAdd()
	iWhale = gc.getInfoTypeForString("BONUS_WHALE")
	pBonusInfoWhale = gc.getBonusInfo(iWhale)
	iBase = pBonusInfoWhale.getConstAppearance() + \
	        random.randrange(pBonusInfoWhale.getRandAppearance1()) + \
	        random.randrange(pBonusInfoWhale.getRandAppearance2())
	iPlayers = gc.getGame().countCivPlayersAlive() * \
	           pBonusInfoWhale.getPercentPerPlayer() / 100
	iModifier = max(1, iOption - 1)  # Also default processing will be done after this function.
	if bRaging:
		iModifier *= 3
	iBonusCount = max(iModifier * iBase * iPlayers / 100, 1)

	if bRaging:
		plots = []
		if bWhaleInCoast and bWhaleInLake:
			for i in range(cymap.numPlots()):
				pPlot = cymap.plotByIndex(i)
				if pPlot.isWater() and pPlot.isPotentialCityWork() and pPlot.hasYield():
					plots.append(pPlot)

		elif not bWhaleInCoast and bWhaleInLake:  # lake
			for i in range(cymap.numPlots()):
				pPlot = cymap.plotByIndex(i)
				if pPlot.isWater() and pPlot.isPotentialCityWork() and pPlot.hasYield():
					if pPlot.canHaveBonus(iWhale, bIgnoreLatitude) or pPlot.isLake():
						plots.append(pPlot)

		elif bWhaleInCoast and not bWhaleInLake:  # coast
			for i in range(cymap.numPlots()):
				pPlot = cymap.plotByIndex(i)
				if pPlot.isWater() and pPlot.isPotentialCityWork() and pPlot.hasYield():
					if not pPlot.isLake():
						plots.append(pPlot)

		else:
			for i in range(cymap.numPlots()):  # ocean only
				pPlot = cymap.plotByIndex(i)
				if pPlot.canHaveBonus(iWhale, bIgnoreLatitude):
					plots.append(pPlot)

		random.shuffle(plots)
		for pPlot in plots:
			if pPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
				pPlot.setBonusType(iWhale)
				iBonusCount -= 1
			if iBonusCount == 0:
				break
	else:
		plots = [cymap.plotByIndex(i) for i in range(cymap.numPlots())]
		random.shuffle(plots)
		for pPlot in plots:
			if pPlot.canHaveBonus(iWhale, bIgnoreLatitude):
				pPlot.setBonusType(iWhale)
				iBonusCount -= 1
			if iBonusCount == 0:
				break

def addBonusType(argsList):
	[iBonusType] = argsList
	gc = CyGlobalContext()
	type_string = gc.getBonusInfo(iBonusType).getType()

	if (CyMap().getCustomMapOption(2) == 1):
		if (type_string in balancer.resourcesToBalance) or (type_string in balancer.resourcesToEliminate):
			return None # don't place any of this bonus randomly

	global bonusTypeRoll
	if bonusTypeRoll == 1:
		CyPythonMgr().allowDefaultImpl() # pretend we didn't implement this method, and let C handle this bonus in the default way
	elif bonusTypeRoll == 2:
		Arboria.addBonusType(argsList)
	elif bonusTypeRoll == 3:
		Rainforest.addBonusType(argsList)

def isAdvancedMap():
	"This map should show up in simple mode"
	return 0

def getGridSize(argsList):
	# Reduce grid sizes by one level.
	grid_sizes = {
		WorldSizeTypes.WORLDSIZE_DUEL:		(8,5),
		WorldSizeTypes.WORLDSIZE_TINY:		(10,6),
		WorldSizeTypes.WORLDSIZE_SMALL:		(13,8),
		WorldSizeTypes.WORLDSIZE_STANDARD:	(16,10),
		WorldSizeTypes.WORLDSIZE_LARGE:		(21,13),
		WorldSizeTypes.WORLDSIZE_HUGE:		(26,16)
	}

	if (argsList[0] == -1): # (-1,) is passed to function on loads
		return []
	[eWorldSize] = argsList
	return grid_sizes[eWorldSize]

def beforeGeneration():
	# Detect whether this game is primarily a team game or not. (1v1 treated as a team game!)
	# Team games, everybody starts on the coast. Otherwise, start anywhere on the pangaea.
	global isTeamGame
	gc = CyGlobalContext()
	iPlayers = gc.getGame().countCivPlayersEverAlive()
	iTeams = gc.getGame().countCivTeamsEverAlive()
	if iPlayers >= iTeams * 2 or iPlayers == 2:
		isTeamGame = True
	else:
		isTeamGame = False
	
	map = CyMap()
	dice = gc.getGame().getMapRand()
	iW = map.getGridWidth()
	iH = map.getGridHeight()
	food = CyFractal()
	food.fracInit(iW, iH, 7, dice, 0, -1, -1)
	# !!! ATTENTION !!!
	# Variables of other modules are manipulated.
	Arboria.food = Rainforest.food = food
	
	# 0: random, 1: default, 2: arboria-like, 3: rainforest-like, 4: tectonics-like
	global terrainTypeRoll
	userInputTerrainType = map.getCustomMapOption(8)
	if userInputTerrainType == 0:
		terrainTypeRoll = 1 + dice.get(getNumCustomMapOptionValues([8]) - 1, "Terrain Type - Pangaea PYTHON")
	else:
		terrainTypeRoll = userInputTerrainType
	print ("terrain type: ", terrainTypeRoll, ", option: ", userInputTerrainType)

	# 0: random, 1: default, 2: arboria-like, 3: rainforest-like
	global forestTypeRoll
	userInputForestType = CyMap().getCustomMapOption(9)
	if userInputForestType == 0:
		forestTypeRoll = 1 + dice.get(getNumCustomMapOptionValues([9]) - 1, "Forest Type - Pangaea PYTHON")
	else:
		forestTypeRoll = userInputForestType
	print ("forest type: ", forestTypeRoll, ", option: ", userInputForestType)

	# 0: random, 1: default, 2: arboria-like, 3: rainforest-like
	global bonusTypeRoll
	userInputBonusType = CyMap().getCustomMapOption(10)
	if userInputBonusType == 0:
		bonusTypeRoll = 1 + dice.get(getNumCustomMapOptionValues([10]) - 1, "Bonus Type - Pangaea PYTHON")
	else:
		bonusTypeRoll = userInputBonusType
	print ("bonus type: ", bonusTypeRoll, ", option: ", userInputBonusType)

class PangaeaHintedWorld:
	def generateSorensHintedPangaea(self):
		print "soren pangaea -- Solid, Irregular"
		NiTextOut("Setting Plot Types (Python Pangaea) ...")
		global hinted_world
		hinted_world = HintedWorld(8,4)

		mapRand = CyGlobalContext().getGame().getMapRand()

		for y in range(hinted_world.h):
			for x in range(hinted_world.w):
				if x in (0, hinted_world.w-1) or y in (0, hinted_world.h-1):
					hinted_world.setValue(x,y,0)
				else:
					hinted_world.setValue(x,y,200 + mapRand.get(55, "Plot Types - Pangaea PYTHON"))

		hinted_world.setValue(1, 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		hinted_world.setValue(2 + mapRand.get(2, "Plot Types - Pangaea PYTHON"), 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		hinted_world.setValue(4 + mapRand.get(2, "Plot Types - Pangaea PYTHON"), 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		hinted_world.setValue(6, 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		if (mapRand.get(2, "Plot Types - Pangaea PYTHON") == 0):
			hinted_world.setValue(2, 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		else:
			hinted_world.setValue(5, 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))

		hinted_world.buildAllContinents()
		return hinted_world.generatePlotTypes(shift_plot_types=True)

	def generateAndysHintedPangaea(self):
		print "andy pangaea -- Solid, Round"
		NiTextOut("Setting Plot Types (Python Pangaea Hinted) ...")
		global hinted_world
		hinted_world = HintedWorld(16,8)

		mapRand = CyGlobalContext().getGame().getMapRand()

		numBlocks = hinted_world.w * hinted_world.h
		numBlocksLand = int(numBlocks*0.33)
		cont = hinted_world.addContinent(numBlocksLand,mapRand.get(5, "Generate Plot Types PYTHON")+4,mapRand.get(3, "Generate Plot Types PYTHON")+2)
		if not cont:
			# Couldn't create continent! Reverting to Soren's Hinted Pangaea
			return self.generateSorensHintedPangaea()
		else:
			for x in range(hinted_world.w):
				for y in (0, hinted_world.h - 1):
					hinted_world.setValue(x,y, 1) # force ocean at poles
			hinted_world.buildAllContinents()
			return hinted_world.generatePlotTypes(shift_plot_types=True)

	def generateHintedPangaeaFluidSimple(self):
		print "Fluid, Simple"
		NiTextOut("Setting Plot Types (Python Pangaea) ...")
		global hinted_world
		hinted_world = HintedWorld(8,4)

		mapRand = CyGlobalContext().getGame().getMapRand()

		for y in range(hinted_world.h):
			for x in range(hinted_world.w):
				if x in (0, hinted_world.w-1) or y in (0, hinted_world.h-1):
					hinted_world.setValue(x,y,0)
				else:
					hinted_world.setValue(x,y,200 + mapRand.get(55, "Plot Types - Pangaea PYTHON"))

		for x in (1, 6):
			restBlock = (1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"))
			yBlocks = [y for y in range(1, 4)
			             if not y == restBlock]
			for y in yBlocks:
				hinted_world.setValue(x, y, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		
		if (mapRand.get(2, "Plot Types - Pangaea PYTHON") == 0):
			hinted_world.setValue(2 + mapRand.get(4, "Plot Types - Pangaea PYTHON"), 1 + mapRand.get(3, "Plot Types - Pangaea PYTHON"), mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		else:
			hinted_world.setValue(3 + mapRand.get(2, "Plot Types - Pangaea PYTHON"), 2, mapRand.get(64, "Plot Types - Pangaea PYTHON"))

		hinted_world.buildAllContinents()
		return hinted_world.generatePlotTypes(shift_plot_types=True)

	def generateHintedPangaeaFluidComplex(self):
		print "Fluid, Complex"
		NiTextOut("Setting Plot Types (Python Pangaea) ...")
		global hinted_world
		hinted_world = HintedWorld(16,8)

		mapRand = CyGlobalContext().getGame().getMapRand()

		for y in range(hinted_world.h):
			for x in range(hinted_world.w):
				if x in (0, hinted_world.w-1) or y in (0, hinted_world.h-1):
					hinted_world.setValue(x,y,0)
				else:
					hinted_world.setValue(x,y,200 + mapRand.get(55, "Plot Types - Pangaea PYTHON"))

		offsetX = 1
		for y in range(1, hinted_world.h - 1):
			hinted_world.setValue(offsetX, y, 0)

		tempWhole = set((x, y) for x in range(1 + offsetX, hinted_world.w - 1)
		                       for y in range(1, hinted_world.h - 1))
		tempOuter = set((x, y) for x in range(2 + offsetX, hinted_world.w - 2)
		                       for y in range(2, hinted_world.h - 2))
		tempInner = set((x, y) for x in range(3 + offsetX, hinted_world.w - 3)
                               for y in range(3, hinted_world.h - 3))
		tempCorner1 = set((x, y) for x in range(2 + offsetX, 6)
		                         for y in range(2, 4))
		tempCorner2 = set((x, y) for x in range(2 + offsetX, 6)
		                         for y in range(hinted_world.h - 4, hinted_world.h - 2))
		tempCorner3 = set((x, y) for x in range(hinted_world.w - 5, hinted_world.w - 2)
		                         for y in range(2, 4))
		tempCorner4 = set((x, y) for x in range(hinted_world.w - 5, hinted_world.w - 2)
		                         for y in range(hinted_world.h - 4, hinted_world.h - 2))
		# W: whole, O: outer, C: corner, I: inner, /: no use, X: offset x
		# 16 x 8
		# ////////////////
		# /XWWWWWWWWWWWWW/
		# /XWCCCOOOOOCCCW/
		# /XWCIIIIIIIIICW/
		# /XWCIIIIIIIIICW/
		# /XWCCCOOOOOCCCW/
		# /XWWWWWWWWWWWWW/
		# ////////////////

		seaBlocks = list(tempWhole - tempOuter)
		lakeBlocks = list(tempInner)
		cornerRand = mapRand.get(4, "Plot Types - Pangaea PYTHON")
		corners = [tempCorner1 - tempInner, tempCorner2 - tempInner, 
		           tempCorner3 - tempInner, tempCorner4 - tempInner]
		
		if cornerRand < 2:
			for i in range(30):
				index = mapRand.get(len(seaBlocks), "Shuffle - Pangaea PYTHON")
				seaX, seaY = seaBlocks.pop(index)
				hinted_world.setValue(seaX, seaY, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
			for i in range(16 - cornerRand * 4):
				index = mapRand.get(len(lakeBlocks), "Shuffle - Pangaea PYTHON")
				lakeX, lakeY = lakeBlocks.pop(index)
				hinted_world.setValue(lakeX, lakeY, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		
		else:
			for i in range(32):
				index = mapRand.get(len(seaBlocks), "Shuffle - Pangaea PYTHON")
				seaX, seaY = seaBlocks.pop(index)
				hinted_world.setValue(seaX, seaY, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
			for i in range(14 - cornerRand * 4):
				index = mapRand.get(len(lakeBlocks), "Shuffle - Pangaea PYTHON")
				lakeX, lakeY = lakeBlocks.pop(index)
				hinted_world.setValue(lakeX, lakeY, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		
		for i in range(cornerRand):
			index = mapRand.get(len(corners), "Shuffle - Pangaea PYTHON")
			cornerBlocks = corners.pop(index)
			for cornerX, cornerY in cornerBlocks:
				hinted_world.setValue(cornerX, cornerY, mapRand.get(64, "Plot Types - Pangaea PYTHON"))
		
		hinted_world.buildAllContinents()
		return hinted_world.generatePlotTypes(shift_plot_types=True)

class PangaeaMultilayeredFractal(CvMapGeneratorUtil.MultilayeredFractal):
	# Subclass. Only the controlling function overridden in this case.
	def generatePlotsByRegion(self, pangaea_type):
		# Sirian's MultilayeredFractal class, controlling function.
		# You -MUST- customize this function for each use of the class.
		#
		# The following grain matrix is specific to Pangaea.py
		sizekey = self.map.getWorldSize()
		sizevalues = {
			WorldSizeTypes.WORLDSIZE_DUEL:      3,
			WorldSizeTypes.WORLDSIZE_TINY:      3,
			WorldSizeTypes.WORLDSIZE_SMALL:     4,
			WorldSizeTypes.WORLDSIZE_STANDARD:  4,
			WorldSizeTypes.WORLDSIZE_LARGE:     4,
			WorldSizeTypes.WORLDSIZE_HUGE:      5
			}
		grain = sizevalues[sizekey]

		# Sea Level adjustment (from user input), limited to value of 5%.
		sea = self.gc.getSeaLevelInfo(self.map.getSeaLevel()).getSeaLevelChange()
		sea = min(sea, 5)
		sea = max(sea, -5)

		# The following regions are specific to Pangaea.py
		mainWestLon = 0.2
		mainEastLon = 0.8
		mainSouthLat = 0.2
		mainNorthLat = 0.8
		subcontinentDimension = 0.4
		bSouthwardShift = False

		# Define the three types.
		if pangaea_type == 2: # Pressed Polar
			print "Pressed Polar"
			numSubcontinents = 3
			# Place mainland near north or south pole?
			global polarShiftRoll
			polarShiftRoll = self.dice.get(2, "Shift - Pangaea PYTHON")
			if polarShiftRoll == 1:
				mainNorthLat += 0.175
				mainSouthLat += 0.175
				# Define potential subcontinent slots (regional definitions).
				# List values: [westLon, southLat, vertRange, horzRange, southShift]
				scValues = [[0.05, 0.375, 0.2, 0.0, 0],
							[0.55, 0.375, 0.2, 0.0, 0],
							[0.1, 0.225, 0.0, 0.15, 0],
							[0.3, 0.225, 0.0, 0.15, 0]
							]
			else:
				mainNorthLat -= 0.175
				mainSouthLat -= 0.175
				# List values: [westLon, southLat, vertRange, horzRange, southShift]
				scValues = [[0.05, 0.025, 0.2, 0.0, 0],
							[0.55, 0.025, 0.2, 0.0, 0],
							[0.1, 0.375, 0.0, 0.15, 0],
							[0.3, 0.375, 0.0, 0.15, 0]
							]
		elif pangaea_type == 1: # Pressed Equatorial
			print "Pressed Equatorial"
			# Define potential subcontinent slots (regional definitions).
			equRoll = self.dice.get(4, "Subcontinents - Pangaea PYTHON")
			if equRoll == 3: equRoll = 1 # 50% chance result = 1
			numSubcontinents = 2 + equRoll
			# List values: [westLon, southLat, vertRange, horzRange, southShift]
			scValues = [[0.05, 0.2, 0.2, 0.0, 0.0],
						[0.55, 0.2, 0.2, 0.0, 0.0],
						[0.2, 0.05, 0.0, 0.2, 0.0],
						[0.2, 0.55, 0.0, 0.2, 0.0]
						]
		else: # Natural
			print "Natural"
			subcontinentDimension = 0.3
			# Shift mainland north or south?
			global shiftRoll
			shiftRoll = self.dice.get(2, "Shift - Pangaea PYTHON")
			if shiftRoll == 1:
				mainNorthLat += 0.075
				mainSouthLat += 0.075
			else:
				mainNorthLat -= 0.075
				mainSouthLat -= 0.075
				bSouthwardShift = True
			# Define potential subcontinent slots (regional definitions).
			numSubcontinents = 4 + self.dice.get(3, "Subcontinents - Pangaea PYTHON")
			# List values: [westLon, southLat, vertRange, horzRange, southShift]
			scValues = [[0.05, 0.575, 0.0, 0.0, 0.15],
						[0.05, 0.275, 0.0, 0.0, 0.15],
						[0.2, 0.175, 0.0, 0.0, 0.15],
						[0.5, 0.175, 0.0, 0.0, 0.15],
						[0.65, 0.575, 0.0, 0.0, 0.15],
						[0.65, 0.275, 0.0, 0.0, 0.15],
						[0.2, 0.675, 0.0, 0.0, 0.15],
						[0.5, 0.675, 0.0, 0.0, 0.15]
						]

		# Generate the main land mass, first pass (to vary shape).
		mainWestX = int(self.iW * mainWestLon)
		mainEastX = int(self.iW * mainEastLon)
		mainNorthY = int(self.iH * mainNorthLat)
		mainSouthY = int(self.iH * mainSouthLat)
		mainWidth = mainEastX - mainWestX + 1
		mainHeight = mainNorthY - mainSouthY + 1

		mainWater = 55+sea

		self.generatePlotsInRegion(mainWater,
									mainWidth, mainHeight,
									mainWestX, mainSouthY,
									2, grain,
									self.iHorzFlags, self.iTerrainFlags,
									-1, -1,
									True, 15,
									2, False,
									False
									)

		# Second pass (to ensure cohesion).
		second_layerHeight = mainHeight/2
		second_layerWestX = mainWestX + mainWidth/10
		second_layerEastX = mainEastX - mainWidth/10
		second_layerWidth = second_layerEastX - second_layerWestX + 1
		second_layerNorthY = mainNorthY - mainHeight/4
		second_layerSouthY = mainSouthY + mainHeight/4

		second_layerWater = 60+sea

		self.generatePlotsInRegion(second_layerWater,
									second_layerWidth, second_layerHeight,
									second_layerWestX, second_layerSouthY,
									1, grain,
									self.iHorzFlags, self.iTerrainFlags,
									-1, -1,
									True, 15,
									2, False,
									False
									)

		# Add subcontinents.
		# Subcontinents can be akin to India/Alaska, Europe, or the East Indies.
		while numSubcontinents > 0:
			# Choose a slot for this subcontinent.
			if len(scValues) > 1:
				scIndex = self.dice.get(len(scValues), "Subcontinent Placement - Pangaea PYTHON")
			else:
				scIndex = 0
			[scWestLon, scSouthLat, scVertRange, scHorzRange, scSouthShift] = scValues[scIndex]
			scWidth = int(subcontinentDimension * self.iW)
			scHeight = int(subcontinentDimension * self.iH)
			scHorzShift = 0; scVertShift = 0
			if scHorzRange > 0.0:
				scHorzShift = self.dice.get(int(self.iW * scHorzRange), "Subcontinent Variance - Terra PYTHON")
			if scVertRange > 0.0:
				scVertShift = self.dice.get(int(self.iW * scVertRange), "Subcontinent Variance - Terra PYTHON")
			scWestX = int(self.iW * scWestLon) + scHorzShift
			scEastX = scWestX + scWidth
			if scEastX >= self.iW: # Trouble! Off the right hand edge!
				while scEastX >= self.iW:
					scWidth -= 1
					scEastX = scWestX + scWidth
			scSouthY = int(self.iH * scSouthLat) + scVertShift
			# Check for southward shift.
			if bSouthwardShift:
				scSouthY -= int(self.iH * scSouthShift)
			scNorthY = scSouthY + scHeight
			if scNorthY >= self.iH: # Trouble! Off the top edge!
				while scNorthY >= self.iH:
					scHeight -= 1
					scNorthY = scSouthY + scHeight

			if self.map.getCustomMapOption(4) == 0:  # allow archipelago
				scShape = self.dice.get(5, "Subcontinent Shape - Terra PYTHON")
			else:
				scShape = self.dice.get(4, "Subcontinent Shape - Terra PYTHON")
				scShape += 1
			if scShape > 1: # Regular subcontinent.
				scWater = 55+sea; scGrain = 1; scRift = -1
			elif scShape == 1: # Irregular subcontinent.
				scWater = 66+sea; scGrain = 2; scRift = 2
			else: # scShape == 0, Archipelago subcontinent.
				scWater = 77+sea; scGrain = grain; scRift = -1

			self.generatePlotsInRegion(scWater,
										scWidth, scHeight,
										scWestX, scSouthY,
										scGrain, grain,
										self.iRoundFlags, self.iTerrainFlags,
										6, 6,
										True, 7,
										scRift, False,
										False
										)

			del scValues[scIndex]
			numSubcontinents -= 1

		# All regions have been processed. Plot Type generation completed.
		return self.wholeworldPlotTypes


class PangaeaExRainforestTerrainGenerator(Rainforest.RainforestTerrainGenerator):
	def __init__(self):
		Rainforest.RainforestTerrainGenerator.__init__(self)
		
	def generateTerrain(self):
		terrainData = [0]*(self.iWidth*self.iHeight)
		for x in range(self.iWidth):
			for y in range(self.iHeight):
				iI = y*self.iWidth + x
				terrain = self.generateTerrainAtPlot(x, y)
				terrainData[iI] = terrain
# begin
# change: CvMapGeneratorUtil.TerrainGenerator
		# expand desert
		iTotalLandPlots = self.map.getLandPlots()
		iDesertPlots = 0
		for x in range(self.iWidth):
			for y in range(self.iHeight):
				if terrainData[y*self.iWidth + x] == self.terrainDesert:
					iDesertPlots += 1
		
		iLoopCount = 0
		print ("iLoopCount, iDesertPlots", iLoopCount, iDesertPlots)

		bIncrement = False
		bDecrement = False
		getDesertParcentage = lambda x: x * 100 / iTotalLandPlots
		if getDesertParcentage(iDesertPlots) < 15:
			bIncrement = True
		elif getDesertParcentage(iDesertPlots) > 17:
			bDecrement = True
		
		for iLoopCount in range(1, 16):
			if bIncrement:
				iDesertChange = 86 - iLoopCount * 4
				iDesertEdgeChange = 82 - iLoopCount * 4
				if getDesertParcentage(iDesertPlots) < 15 and iDesertEdgeChange > 0:
					self.iDesert = self.desert.getHeightFromPercent(iDesertChange)
					self.iDesertEdge = self.desert.getHeightFromPercent(iDesertEdgeChange)
				else:
					break
			elif bDecrement:
				iDesertChange = 86 + iLoopCount * 2
				iDesertEdgeChange = 82 + iLoopCount * 2
				if getDesertParcentage(iDesertPlots) > 17 and iDesertChange < 100:
					self.iDesert = self.desert.getHeightFromPercent(iDesertChange)
					self.iDesertEdge = self.desert.getHeightFromPercent(iDesertEdgeChange)
				else:
					break
			else:
				break

			for x in range(self.iWidth):
				for y in range(self.iHeight):
					iI = y*self.iWidth + x
					terrain = self.generateTerrainAtPlot(x, y)
					terrainData[iI] = terrain
			
			iDesertPlots = 0
			for x in range(self.iWidth):
				for y in range(self.iHeight):
					if terrainData[y*self.iWidth + x] == self.terrainDesert:
						iDesertPlots += 1
			print ("iLoopCount, iDesertPlots", iLoopCount, iDesertPlots)
# end
				
		return terrainData


class PangaeaExVoronoiPangaeaMap(Tectonics.voronoiPangaeaMap):
	def __init__(self,numPlayers):
		Tectonics.voronoiPangaeaMap.__init__(self,numPlayers)
# change: Tectonics.voronoiPangaeaMap
		self.peakAltitude = 10  # original: 11
		self.hillAltitude = 9  # original: 7
		self.landAltitude = 3
		self.altitudeVariation = 3

	def createMap(self):
		for y in range(self.mapHeight):
			for x in range(self.mapWidth):
				i = y*self.mapWidth + x
				height = self.heightMap[i]
				if (height > self.peakAltitude):
					if (self.dice.get(7,"Random pass") == 6):
						self.plotTypes[i] = PlotTypes.PLOT_HILLS
					else:
						self.plotTypes[i] = PlotTypes.PLOT_PEAK
				elif (height > self.hillAltitude):
					if (self.dice.get(20,"Random peak") == 19):
						self.plotTypes[i] = PlotTypes.PLOT_PEAK
					else:
						self.plotTypes[i] = PlotTypes.PLOT_HILLS
				elif (height > self.landAltitude):
# begin
# change: Tectonics.voronoiPangaeaMap
# original
##					self.plotTypes[i] = PlotTypes.PLOT_HILLS
					if (self.dice.get(30,"Random hills") == 0):
						self.plotTypes[i] = PlotTypes.PLOT_HILLS
					else:
						self.plotTypes[i] = PlotTypes.PLOT_LAND
# end
				else:
					self.plotTypes[i] = PlotTypes.PLOT_OCEAN


class PangaeaExTectonicsClimateGenerator(Tectonics.ClimateGenerator):
	def __init__(self):
		self.climate = 1
		gc = CyGlobalContext()
		self.map = gc.getMap()
		self.mapWidth = self.map.getGridWidth()
		self.maxWindForce = self.mapWidth / 8
		self.mapHeight = self.map.getGridHeight()
		self.terrainDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
		self.terrainPlains = gc.getInfoTypeForString("TERRAIN_PLAINS")
		self.terrainIce = gc.getInfoTypeForString("TERRAIN_SNOW")
		self.terrainTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
		self.terrainGrass = gc.getInfoTypeForString("TERRAIN_GRASS")
		self.terrain = [0] * (self.mapWidth*self.mapHeight)
		self.moisture = [0] * (self.mapWidth*self.mapHeight)
		self.dice = gc.getGame().getMapRand()

	def getLatitudeAtPlot(self, iX, iY):
		"returns a value in the range of 0-90 degrees"
		return self.map.plot(iX,iY).getLatitude()

	def computeTerrain(self):
		terrain = [0] * (self.mapWidth*self.mapHeight)
		for x in range(self.mapWidth):
			for y in range(self.mapHeight):
				if (self.map.plot(x,y).isWater()):
					self.terrain[y*self.mapWidth+x] = self.map.plot(x,y).getTerrainType()
				else:
					terrain[y*self.mapWidth+x] = self.getTerrain(self.getLatitudeAtPlot(x,y),self.moisture[y*self.mapWidth + x])
		for x in range(self.mapWidth):
			for y in range(self.mapHeight):
				if (not self.map.plot(x,y).isWater()):
					i = y*self.mapWidth+x
					self.terrain[i] = terrain[i]
					bias = self.dice.get(3,"Random terrain")
# begin
# change: Tectonics.ClimateGenerator
# original
##					if bias == 0 and y > 1:
##						self.terrain[i] = terrain[i-self.mapWidth]
##					if bias == 2 and y < self.mapHeight - 1:
##						self.terrain[i] = terrain[i+self.mapWidth]
					if bias == 0 and y > 1:
						if not self.map.plotByIndex(i-self.mapWidth).isWater():
							self.terrain[i] = terrain[i-self.mapWidth]
					if bias == 2 and y < self.mapHeight - 1:
						if not self.map.plotByIndex(i+self.mapWidth).isWater():
							self.terrain[i] = terrain[i+self.mapWidth]
# end

# begin
# change: Tectonics.ClimateGenerator
		# expand grass area
		iTotalLandPlots = self.map.getLandPlots()
		iGrassPlots = 0
		for x in range(self.mapWidth):
			for y in range(self.mapHeight):
				if self.terrain[y*self.mapWidth+x] == self.terrainGrass:
					iGrassPlots += 1
		
		iLoopCount = 0
		print ("iLoopCount, iGrass", iLoopCount, iGrassPlots)
		while iGrassPlots * 100 / iTotalLandPlots < 50 and iLoopCount < 10:
			iLoopCount += 1
			selectedPlots = set()
			for x in range(self.mapWidth):
				for y in range(self.mapHeight):
					if (not self.map.plot(x,y).isWater()):
						i = y*self.mapWidth+x
						if self.terrain[i] == self.terrainGrass:
							if y > 1 and y < self.mapHeight - 1:
								if self.terrain[i-self.mapWidth] == self.terrainPlains:
									selectedPlots.add(i-self.mapWidth)
								if self.terrain[i+self.mapWidth] == self.terrainPlains:
									selectedPlots.add(i+self.mapWidth)
								if x == 0:
									if self.terrain[i-1+self.mapWidth] == self.terrainPlains:
										selectedPlots.add(i-1+self.mapWidth)
								else:
									if self.terrain[i-1] == self.terrainPlains:
										selectedPlots.add(i-1)
								if x == self.mapWidth - 1:
									if self.terrain[i+1-self.mapWidth] == self.terrainPlains:
										selectedPlots.add(i+1-self.mapWidth)
								else:
									if self.terrain[i+1] == self.terrainPlains:
										selectedPlots.add(i+1)
			for idx in selectedPlots:
				if self.dice.get(3,"Random grass") == 0:
					iGrassPlots += 1
					self.terrain[idx] = self.terrainGrass
			print ("iLoopCount, iGrass", iLoopCount, iGrassPlots)
# end

		for x in range(self.mapWidth):
			for y in range(self.mapHeight):
				if (not self.map.plot(x,y).isWater()):
					i = y*self.mapWidth+x
# begin
# change: Tectonics.ClimateGenerator
# original
##					if self.terrain[i] == self.terrainDesert:
					if self.terrain[i] == self.terrainDesert or \
					   self.terrain[i] == self.terrainTundra or \
					   self.terrain[i] == self.terrainIce:
# end
						if y > 1 and y < self.mapHeight - 1:
							if self.terrain[i-self.mapWidth] == self.terrainGrass:
								self.terrain[i-self.mapWidth] = self.terrainPlains
							if self.terrain[i+self.mapWidth] == self.terrainGrass:
								self.terrain[i+self.mapWidth] = self.terrainPlains
							if self.terrain[i-1] == self.terrainGrass:
								self.terrain[i-1] = self.terrainPlains
							if self.terrain[i+1] == self.terrainGrass:
								self.terrain[i+1] = self.terrainPlains

	def getArcticTerrain(self, climate, latitude, moisture):
		polar = 0
# begin
# change: Tectonics.ClimateGenerator
# original
##		if (latitude > 70):
##			polar = latitude - 70
		if (latitude > 50):
			polar = latitude - 50
# end
			climate.ice += polar * polar * 3
			climate.tundra += polar * (2 + moisture)
# begin
# change: Tectonics.ClimateGenerator
			if (latitude >= 63):
				climate.ice *= 100
# end

	def getColdTerrain(self, climate, latitude, moisture):
# begin
# change: Tectonics.ClimateGenerator
# original
##		if (latitude > 60):
##			polar = latitude - 60
		if (latitude > 35):
			polar = latitude - 35
# end
			climate.tundra += polar * (5 + moisture) + self.dice.get(polar*3,"more tundra")
			if (moisture > 10):
				climate.plains += polar * (moisture - 10)

	def getTemperateTerrain(self, climate, latitude, moisture):
		temperate = 45 - abs(45 - latitude)
		climate.plains += temperate * (3 + moisture/2)
# begin
# change: Tectonics.ClimateGenerator
# original
##		climate.grass += temperate * (1 + moisture) + self.dice.get(temperate,"more grass")
		climate.grass += temperate * (1 + moisture) + self.dice.get(temperate * 3,"more grass")
# end

	def getTropicalTerrain(self, climate, latitude, moisture):
		tropical = 0
		if (latitude < 40):
			tropical = 20 - abs(20 - latitude)
		climate.plains += tropical * (12 - self.climate + moisture/2) + self.dice.get(tropical,"more plains")
# begin
# change: Tectonics.ClimateGenerator
# original
##		climate.grass += tropical * (moisture + self.climate)
		climate.grass += tropical * (moisture * 3 + self.climate)
# end
		climate.desert += tropical * (4 - self.climate) * 6

	def getEquatorialTerrain(self, climate, latitude, moisture):
		equator = 0
		if (latitude < 25):
			equator = 25 - latitude
		climate.plains += equator * 7
# begin
# change: Tectonics.ClimateGenerator
# original
##		climate.grass += equator * (3 + moisture) + self.dice.get(equator,"more grass")
		climate.grass += equator * (3 + moisture * 2) + self.dice.get(equator * 4,"more grass")
# end

	#I compute latitude as in the maputil but wtf is there a plot.latitude then?
	def getTerrain(self, latitude, moisture):
		class climates:
			def __init__(self):
				self.ice = 0
				self.tundra = 0
				self.plains = 0
				self.grass = 0
				self.desert = 0

		climate = climates()
		self.getArcticTerrain(climate, latitude, moisture)
		self.getColdTerrain(climate, latitude, moisture)
		self.getTemperateTerrain(climate, latitude, moisture)
		self.getTropicalTerrain(climate, latitude, moisture)
		self.getEquatorialTerrain(climate, latitude, moisture)
		
#		print (climate.ice, climate.tundra, climate.plains, climate.grass, climate.desert, "lat, moist:", latitude, moisture)
		
		if (climate.ice >= climate.tundra) and (climate.ice >= climate.plains) and (climate.ice >= climate.grass) and (climate.ice >= climate.desert):
			return self.terrainIce
		if (climate.tundra >= climate.plains) and (climate.tundra >= climate.grass) and (climate.tundra >= climate.desert):
			return self.terrainTundra
		if (climate.plains >= climate.grass) and (climate.plains >= climate.desert):
			return self.terrainPlains
		if (climate.grass >= climate.desert):
			return self.terrainGrass
		return self.terrainDesert


'''
Regional Variables Key:

iWaterPercent,
iRegionWidth, iRegionHeight,
iRegionWestX, iRegionSouthY,
iRegionGrain, iRegionHillsGrain,
iRegionPlotFlags, iRegionTerrainFlags,
iRegionFracXExp, iRegionFracYExp,
bStrip, strip,
rift_grain, has_center_rift,
invert_heights
'''

def generatePlotTypes():
	NiTextOut("Setting Plot Types (Python Pangaea) ...")
	global pangaea_type
	gc = CyGlobalContext()
	mapgen = CyMapGenerator()
	map = CyMap()
	dice = gc.getGame().getMapRand()
	hinted_world = PangaeaHintedWorld()
	fractal_world = PangaeaMultilayeredFractal()

	# Get user input.
	userInputLandmass = map.getCustomMapOption(0)
	if userInputLandmass == 5:  # Tectonics-like
		numPlayers = gc.getGame().countCivPlayersEverAlive()
		surface = gc.getMap().getGridWidth() * gc.getMap().getGridHeight()
		numPlayers = (numPlayers + surface / 400) / 2
		generator = PangaeaExVoronoiPangaeaMap(int(numPlayers * 1.2) + 1)  # original: numPlayers
		print ("Tectonics-like", "Tectonics Plate: ", numPlayers)
		return generator.generate()

	# Implement Pangaea by Type
	if userInputLandmass in (3, 4): # Solid or Fluid
		# Roll for type selection.
		typeRoll = dice.get(3, "PlotGen Chooser - Pangaea PYTHON")
		# Solid Shoreline cohesion check and catch - patched Dec 30, 2005 - Sirian
		# Error catching for non-cohesive results.
		cohesive = False
		while not cohesive:
			plotTypes = []
			if typeRoll == 2:
				if userInputLandmass == 4:
					plotTypes = hinted_world.generateHintedPangaeaFluidSimple()
				else:
					plotTypes = hinted_world.generateAndysHintedPangaea()
			else:
				if userInputLandmass == 4:
					plotTypes = hinted_world.generateHintedPangaeaFluidComplex()
				else:
					plotTypes = hinted_world.generateSorensHintedPangaea()
			mapgen.setPlotTypes(plotTypes)
			biggest_area = map.findBiggestArea(false)
			iTotalLandPlots = map.getLandPlots()
			iBiggestAreaPlots = biggest_area.getNumTiles()
			if iBiggestAreaPlots >= 0.9 * iTotalLandPlots:
				cohesive = True
		return plotTypes

	elif userInputLandmass == 2: # Pressed
		# Roll for type selection.
		typeRoll = dice.get(3, "PlotGen Chooser - Pangaea PYTHON")
		if typeRoll == 1:
			pangaea_type = 1
		else:
			pangaea_type = 2
		return fractal_world.generatePlotsByRegion(pangaea_type)

	elif userInputLandmass == 1: # Natural
		pangaea_type = 0
		return fractal_world.generatePlotsByRegion(pangaea_type)

	else: # Random
		global terrainRoll
		terrainRoll = dice.get(16, "PlotGen Chooser - Pangaea PYTHON")
		# 0-3 = Natural
		# 4 = Pressed, Equatorial
		# 5,6 = Pressed, Polar
		# 7,8 = Solid, Irregular
		# 9 = Solid, Round
		# 10,11 = Fluid, Complex
		# 12 = Fluid, Simple
		# 13-15 = Tectonics-like

		if terrainRoll in (13, 14, 15):
			numPlayers = gc.getGame().countCivPlayersEverAlive()
			surface = gc.getMap().getGridWidth() * gc.getMap().getGridHeight()
			numPlayers = (numPlayers + surface / 400) / 2
			generator = PangaeaExVoronoiPangaeaMap(int(numPlayers * 1.2) + 1)  # original: numPlayers
			print ("Tectonics-like", "Tectonics Plate: ", numPlayers)
			return generator.generate()
		elif terrainRoll in (7, 8, 9, 10, 11, 12):
			# Solid Shoreline cohesion check and catch - patched Dec 30, 2005 - Sirian
			cohesive = False
			while not cohesive:
				plotTypes = []
				if terrainRoll == 9:
					plotTypes = hinted_world.generateAndysHintedPangaea()
				elif terrainRoll in (7, 8):
					plotTypes = hinted_world.generateSorensHintedPangaea()
				elif terrainRoll == 12:
					plotTypes = hinted_world.generateHintedPangaeaFluidSimple()
				else:
					plotTypes = hinted_world.generateHintedPangaeaFluidComplex()
				mapgen.setPlotTypes(plotTypes)
				biggest_area = map.findBiggestArea(false)
				iTotalLandPlots = map.getLandPlots()
				iBiggestAreaPlots = biggest_area.getNumTiles()
				if iBiggestAreaPlots >= 0.9 * iTotalLandPlots:
					cohesive = True
			return plotTypes

		elif terrainRoll == 5 or terrainRoll == 6:
			pangaea_type = 2
			return fractal_world.generatePlotsByRegion(pangaea_type)
		elif terrainRoll == 4:
			pangaea_type = 1
			return fractal_world.generatePlotsByRegion(pangaea_type)
		else:
			pangaea_type = 0
			return fractal_world.generatePlotsByRegion(pangaea_type)

def generateTerrainTypes():
	# Run a check for cohesion failure.
	# If the largest land area contains less than 80% of the land (Natural/Pressed),
	# or less than 90% of the land (Solid), add a third layer of fractal terrain
	# to try to link the main landmasses in to a true Pangaea.
	gc = CyGlobalContext()
	map = CyMap()
	dice = gc.getGame().getMapRand()
	iHorzFlags = CyFractal.FracVals.FRAC_WRAP_X + CyFractal.FracVals.FRAC_POLAR
	biggest_area = map.findBiggestArea(false)
	global terrainRoll
	userInputShoreline = map.getCustomMapOption(0)
	iTotalLandPlots = map.getLandPlots()
	iBiggestAreaPlots = biggest_area.getNumTiles()
	print("Total Land: ", iTotalLandPlots, " Main Landmass Plots: ", iBiggestAreaPlots)
	if (userInputShoreline == 1 or userInputShoreline == 2 or (userInputShoreline == 0 and terrainRoll < 7)) and iBiggestAreaPlots < 0.8 * iTotalLandPlots:
		global pangaea_type
		print("Total Land: ", iTotalLandPlots, " Main Landmass Plots: ", iBiggestAreaPlots)
		print "Cohesion failure! Attempting to remedy..."
		#print("Pangaea Type: ", pangaea_type)
		iW = map.getGridWidth()
		iH = map.getGridHeight()
		iWestX = int(0.3 * iW)
		eastX = int(0.7 * iW)
		southLat = 0.4
		northLat = 0.6
		if pangaea_type == 0: # Natural
			global shiftRoll
			#print("Shift Roll: ", shiftRoll)
			if shiftRoll == 1:
				southLat += 0.075
				northLat += 0.075
			else:
				southLat -= 0.075
				northLat -= 0.075
		elif pangaea_type == 2: # Pressed Polar
			global polarShiftRoll
			#print("Polar Shift Roll: ", polarShiftRoll)
			if polarShiftRoll == 1:
				southLat += 0.175
				northLat += 0.175
			else:
				southLat -= 0.175
				northLat -= 0.175
		else: # Pressed Equatorial
			pass
		iSouthY = int(southLat * iH)
		northY = int(northLat * iH)
		iRegionWidth = eastX - iWestX + 1
		iRegionHeight = northY - iSouthY + 1

		# Init the plot types array and the regional fractals
		plotTypes = [] # reinit the array for each pass
		plotTypes = [PlotTypes.PLOT_OCEAN] * (iRegionWidth*iRegionHeight)
		regionContinentsFrac = CyFractal()
		regionHillsFrac = CyFractal()
		regionPeaksFrac = CyFractal()
		regionContinentsFrac.fracInit(iRegionWidth, iRegionHeight, 1, dice, iHorzFlags, 7, 5)
		regionHillsFrac.fracInit(iRegionWidth, iRegionHeight, 3, dice, iHorzFlags, 7, 5)
		regionPeaksFrac.fracInit(iRegionWidth, iRegionHeight, 4, dice, iHorzFlags, 7, 5)

		iWaterThreshold = regionContinentsFrac.getHeightFromPercent(40)
		iHillsBottom1 = regionHillsFrac.getHeightFromPercent(20)
		iHillsTop1 = regionHillsFrac.getHeightFromPercent(30)
		iHillsBottom2 = regionHillsFrac.getHeightFromPercent(70)
		iHillsTop2 = regionHillsFrac.getHeightFromPercent(80)
		iPeakThreshold = regionPeaksFrac.getHeightFromPercent(25)

		# Loop through the region's plots
		for x in range(iRegionWidth):
			for y in range(iRegionHeight):
				i = y*iRegionWidth + x
				val = regionContinentsFrac.getHeight(x,y)
				if val <= iWaterThreshold: pass
				else:
					hillVal = regionHillsFrac.getHeight(x,y)
					if ((hillVal >= iHillsBottom1 and hillVal <= iHillsTop1) or (hillVal >= iHillsBottom2 and hillVal <= iHillsTop2)):
						peakVal = regionPeaksFrac.getHeight(x,y)
						if (peakVal <= iPeakThreshold):
							plotTypes[i] = PlotTypes.PLOT_PEAK
						else:
							plotTypes[i] = PlotTypes.PLOT_HILLS
					else:
						plotTypes[i] = PlotTypes.PLOT_LAND

		for x in range(iRegionWidth):
			wholeworldX = x + iWestX
			for y in range(iRegionHeight):
				i = y*iRegionWidth + x
				if plotTypes[i] == PlotTypes.PLOT_OCEAN: continue # Not merging water!
				wholeworldY = y + iSouthY
				# print("Changing water plot at ", wholeworldX, wholeworldY, " to ", plotTypes[i])
				iWorld = wholeworldY*iW + wholeworldX
				pPlot = map.plotByIndex(iWorld)
				if pPlot.isWater():	# Only merging new land plots over old water plots.
					pPlot.setPlotType(plotTypes[i],True,True,False)

		# Smooth any graphical glitches these changes may have produced.
		map.recalculateAreas()

	# Now generate Terrain.
	NiTextOut("Generating Terrain (Python Pangaea) ...")
	global terrainTypeRoll
	if terrainTypeRoll == 1:
		terraingen = TerrainGenerator()
	elif terrainTypeRoll == 2:
		terraingen = Arboria.ArboriaTerrainGenerator()
	elif terrainTypeRoll == 3:
		terraingen = PangaeaExRainforestTerrainGenerator()
	elif terrainTypeRoll == 4:
		terraingen = PangaeaExTectonicsClimateGenerator()
	terrainTypes = terraingen.generateTerrain()

	return terrainTypes

def _isTectonicsMap():
	if terrainTypeRoll == 4:
		return True
	elif CyMap().getCustomMapOption(0) == 0 and terrainRoll in (13, 14, 15):
		return True
	elif CyMap().getCustomMapOption(0) == 5:
		return True
	return False

def addRivers():
	if _isTectonicsMap():
		#riverGenerator = riversMap()
		riverGenerator = Tectonics.riversFromSea()
		riverGenerator.seedRivers()
	else:
		CyPythonMgr().allowDefaultImpl()

def addFeatures():
	NiTextOut("Adding Features (Python Pangaea) ...")
	global forestTypeRoll
	if forestTypeRoll == 1:
		featuregen = FeatureGenerator()
	elif forestTypeRoll == 2:
		featuregen = Arboria.ArboriaFeatureGenerator()
	elif forestTypeRoll == 3:
		featuregen = Rainforest.RainforestFeatureGenerator()
	featuregen.addFeatures()
	return 0

def findStartingPlot(argsList):
	[playerID] = argsList

	def isValid(playerID, x, y):
		global isTeamGame
		map = CyMap()
		pPlot = map.plot(x, y)

		if (pPlot.getArea() != map.findBiggestArea(False).getID()):
			return false

		if isTeamGame:
			pWaterArea = pPlot.waterArea()
			if (pWaterArea.isNone()):
				return false
			return not pWaterArea.isLake()
		else:
			return true

	return CvMapGeneratorUtil.findStartingPlot(playerID, isValid)

def normalizeRemovePeaks():
	if _isTectonicsMap():
		Tectonics.normalizeRemovePeaks()
		
		# And remove hills too.
		gc = CyGlobalContext()
		dice = gc.getGame().getMapRand()
		cymap = CyMap()
		iRange = 2
		
		# for debug
		bDebug = False
		if bDebug:
			for i in range(gc.getMAX_CIV_PLAYERS()):
				if gc.getPlayer(i).isHuman():
					iFirstHumanPlayer = i
					break

		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			if gc.getPlayer(iPlayer).isAlive():
				iHillsCount = 0
				iPlainsHillsCount = 0
				selectedPlots = []
				pStartingPlot = gc.getPlayer(iPlayer).getStartingPlot()
				for offsetX in range(-iRange, iRange + 1):
					for offsetY in range(-iRange, iRange + 1):
						if (offsetX, offsetY) in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
							continue
						x = pStartingPlot.getX() + offsetX
						y = pStartingPlot.getY() + offsetY
						pPlot = cymap.plot(x, y)
						if pPlot.isHills():
							iHillsCount += 1
							if pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_PLAINS"):
								iPlainsHillsCount += 1
							if pPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
								selectedPlots.append(pPlot)
							if bDebug:
								CyEngine().addSign(pPlot, iFirstHumanPlayer, "hills")
								
				if bDebug:
					# begin debug print
					print ("player:", iPlayer, "start:", pStartingPlot.getX(), pStartingPlot.getY())
					print ("hills:", iHillsCount, "plains hills:", iPlainsHillsCount, "player:", iPlayer)
					print ("selectedPlots:")
					for p in selectedPlots:
						print ((p.getX(), p.getY())),
						CyEngine().removeSign(p, iFirstHumanPlayer)
						CyEngine().addSign(p, iFirstHumanPlayer, "selected hills")
					print ("")
					# end debug print
				
				stopRand = dice.get(3, "Stop rand")
				while iHillsCount + iPlainsHillsCount > 8 + stopRand and selectedPlots:
					pPlot = selectedPlots.pop(dice.get(len(selectedPlots), "Shuffle"))
					if pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_PLAINS"):
						iPlainsHillsCount -= 1
						if bDebug:
							CyEngine().removeSign(pPlot, iFirstHumanPlayer)
							CyEngine().addSign(pPlot, iFirstHumanPlayer, "hills/plains removed")
					else:
						if bDebug:
							CyEngine().removeSign(pPlot, iFirstHumanPlayer)
							CyEngine().addSign(pPlot, iFirstHumanPlayer, "hills removed")
					iHillsCount -= 1
					iFeature = pPlot.getFeatureType()
					
					pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True,False)
					pPlot.setTerrainType(gc.getInfoTypeForString("TERRAIN_GRASS"),True,True,False)
					if iFeature != FeatureTypes.NO_FEATURE:
						pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
						if pPlot.canHaveFeature(iFeature):
							pPlot.setFeatureType(iFeature, -1)
						else:
							pass
							print ("remove feature, type:", iFeature, (pPlot.getX(), pPlot.getY()), "player:", iPlayer)
					print ("remove hills", (pPlot.getX(), pPlot.getY()), "player:", iPlayer)
	else:
		CyPythonMgr().allowDefaultImpl()

def normalizeRemoveBadFeatures():
	CyPythonMgr().allowDefaultImpl()
	# Since it is necessary to process after normalizeAddLakes(), this is described here.
	if CyMap().getCustomMapOption(3):
		addExtraRivers()

D_NORTH = DirectionTypes.DIRECTION_NORTH
D_NORTHEAST = DirectionTypes.DIRECTION_NORTHEAST
D_EAST = DirectionTypes.DIRECTION_EAST
D_SOUTHEAST = DirectionTypes.DIRECTION_SOUTHEAST
D_SOUTH = DirectionTypes.DIRECTION_SOUTH
D_SOUTHWEST = DirectionTypes.DIRECTION_SOUTHWEST
D_WEST = DirectionTypes.DIRECTION_WEST
D_NORTHWEST = DirectionTypes.DIRECTION_NORTHWEST
D_NO_DIRECTION = DirectionTypes.NO_DIRECTION
CD_NORTH = CardinalDirectionTypes.CARDINALDIRECTION_NORTH
CD_EAST = CardinalDirectionTypes.CARDINALDIRECTION_EAST
CD_SOUTH = CardinalDirectionTypes.CARDINALDIRECTION_SOUTH
CD_WEST = CardinalDirectionTypes.CARDINALDIRECTION_WEST

def addExtraRivers():
	# Add rivers to coasts (or lakes) near starting plots.
	gc = CyGlobalContext()
	cymap = gc.getMap()
	offsets = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)]
	random.shuffle(offsets)

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		if not gc.getPlayer(iPlayer).isAlive():
			continue
		pStartingPlot = gc.getPlayer(iPlayer).getStartingPlot()
		print ("player", iPlayer, "starting plot", (pStartingPlot.getX(), pStartingPlot.getY()))
		if pStartingPlot.isRiver():
			continue

		print ("not river", iPlayer)
		rivers = [(D_NORTH, CD_EAST), (D_NORTH, CD_WEST),
		          (D_EAST, CD_SOUTH), (D_EAST, CD_NORTH),
		          (D_SOUTH, CD_WEST), (D_SOUTH, CD_EAST),
		          (D_WEST, CD_NORTH), (D_WEST, CD_SOUTH)]
		random.shuffle(rivers)
		while rivers:
			if _doExtraRiver(pStartingPlot, rivers):
				# succeed in river creation.
##				_printDebugStrings(pStartingPlot)
				break

	# The following process is the same as the thing of CvGame::normalizeAddRiver()
	# add floodplains to any desert tiles the new river passes through
	for k in range(cymap.numPlots()):
		pPlot = cymap.plotByIndex(k)
		assert pPlot != None

		for j in range(gc.getNumFeatureInfos()):
			if gc.getFeatureInfo(j).isRequiresRiver():
				if pPlot.canHaveFeature(j):
					if gc.getFeatureInfo(j).getAppearanceProbability() == 10000:

##						### debug text begin
##						infos = []
##						infos.append(gc.getTerrainInfo(pPlot.getTerrainType()))
##						infos.append(gc.getFeatureInfo(pPlot.getFeatureType()))
##						infos.append(gc.getBonusInfo(pPlot.getBonusType(TeamTypes.NO_TEAM)))
##						infos.append(gc.getImprovementInfo(pPlot.getImprovementType()))
##						for i in range(len(infos)):
##							if infos[i]:
##								infos[i] = infos[i].getText()
##							else:
##								infos[i] = "None"
##						print "terrain: " + infos[0]
##						print "feature: " + infos[1]
##						print "bonus: " + infos[2]
##						print "improvement: " + infos[3]
##						print ("change to floodplain", (pPlot.getX(), pPlot.getY()))
##						### debug text end
##
						if pPlot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
							pPlot.setBonusType(BonusTypes.NO_BONUS)
						pPlot.setFeatureType(j, -1)
						break

def _doExtraRiver(pStartingPlot, rivers):
	# Return True if succeed in river creation.
	# Calculate the plot river start.
	iStartX, iStartY = pStartingPlot.getX(), pStartingPlot.getY()
	direction, cardinalDirection = rivers.pop()
	if direction == D_NORTH:
		assert cardinalDirection in (CD_EAST, CD_WEST)
		if cardinalDirection == CD_EAST:
			pRiverPlot = plotDirection(iStartX, iStartY, D_NORTHWEST)
		else:
			pRiverPlot = plotDirection(iStartX, iStartY, D_NORTH)

	elif direction == D_EAST:
		assert cardinalDirection in (CD_NORTH, CD_SOUTH)
		if cardinalDirection == CD_SOUTH:
			pRiverPlot = plotDirection(iStartX, iStartY, D_NORTH)
		else:
			pRiverPlot = pStartingPlot

	elif direction == D_SOUTH:
		assert cardinalDirection in (CD_EAST, CD_WEST)
		if cardinalDirection == CD_EAST:
			pRiverPlot = plotDirection(iStartX, iStartY, D_WEST)
		else:
			pRiverPlot = pStartingPlot

	else:
		assert direction == D_WEST
		assert cardinalDirection in (CD_NORTH, CD_SOUTH)
		if cardinalDirection == CD_SOUTH:
			pRiverPlot = plotDirection(iStartX, iStartY, D_NORTHWEST)
		else:
			pRiverPlot = plotDirection(iStartX, iStartY, D_WEST)

	if not pRiverPlot:
		return False
	
	# check if river source plots are ocean.
	riverSourcePlots = _getRiverSourcePlots(pRiverPlot, cardinalDirection)
	for pPlot in riverSourcePlots:
		if pPlot and pPlot.isWater() and not pPlot.isLake():
##			print ("Ocean plot is found at river source.", (pPlot.getX(), pPlot.getY()))
			return False

	# iPass == 0: search another river
	# iPass == 1: search an ocean plot
	# iPass == 2: search a lake plot
	riverMouthPlots = _getRiverMouthPlots(pRiverPlot, cardinalDirection)
	pRiverDestPlot = plotCardinalDirection(pRiverPlot.getX(), pRiverPlot.getY(), cardinalDirection)
	for iPass in range(3):
		for iLoopPlot in range(len(riverMouthPlots)):
			if iPass == 0 and iLoopPlot > 0:
				# If iPass == 0, only need to search once.
				continue
			pPlot = riverMouthPlots[iLoopPlot]
			if not pPlot:
				continue
			
			bDoRiver = False
			if iPass == 0 and pRiverDestPlot.getRiverID() > -1:
				# Extend another river straightly.
				if cardinalDirection in (CD_NORTH, CD_WEST):
					if pRiverDestPlot.getRiverNSDirection() == cardinalDirection or \
					   pRiverDestPlot.getRiverWEDirection() == cardinalDirection:
						bDoRiver = True
				elif cardinalDirection in (CD_SOUTH, CD_EAST):
					pRiverSource = plotCardinalDirection(pRiverDestPlot.getX(), pRiverDestPlot.getY(), cardinalDirection)
					if pRiverSource.getRiverNSDirection() == cardinalDirection or \
					   pRiverSource.getRiverWEDirection() == cardinalDirection:
						bDoRiver = True

			elif iPass == 1 and pPlot.isWater() and not pPlot.isLake():
				bDoRiver = True
			elif iPass == 2 and pPlot.isLake() and not pRiverDestPlot.getRiverID() > -1:
				bDoRiver = True
			
			if bDoRiver:
				waterPlots = []
				_getAwayWaterPlot(riverSourcePlots, waterPlots)
				CyMapGenerator().doRiver(pRiverPlot, cardinalDirection)
				_giveBackWaterPlot(waterPlots)
				if pStartingPlot.isRiver():
					# Succeed in river creation.
					print ("succeed in river creation", "iPass", iPass, (pRiverPlot.getX(), pRiverPlot.getY()))
					return True
				else:
					return False
	return False

# There is a problem when creating a river near water plot.
# Although a land plot is in the upper stream side of the river source, 
# isRiver() returns True. Therefore _getAwayWaterPlot() and
# _giveBackWaterPlot() is used to avoid this problem.
def _getAwayWaterPlot(plots, waterPlots):
	# Temporarily change water plot into land before river creation.
	# It is necessary to avoid the bug.
	for pPlot in plots:
		if pPlot.isWater():
##			print ("get away water plot", (pPlot.getX(), pPlot.getY()), "bonus", pPlot.getBonusType(TeamTypes.NO_TEAM))
			pPlot.setPlotType(PlotTypes.PLOT_LAND,True,False,False)
			waterPlots.append(pPlot)

def _giveBackWaterPlot(waterPlots):
	# Restore changing by _getAwayWaterPlot() after river creation.
	# It is necessary to avoid the bug.
	for pPlot in waterPlots:
		pPlot.setPlotType(PlotTypes.PLOT_OCEAN,True,True,False)
##		print ("give back water plot, bonus:", pPlot.getBonusType(TeamTypes.NO_TEAM))

def _getRiverSourcePlots(pRiverPlot, cardinalDirection):
	if cardinalDirection == CD_NORTH:
		directions = (D_SOUTH, D_SOUTHEAST)
	elif cardinalDirection == CD_EAST:
		directions = (D_SOUTH, D_NO_DIRECTION)
	elif cardinalDirection == CD_SOUTH:
		directions = (D_NO_DIRECTION, D_EAST)
	else:
		directions = (D_EAST, D_SOUTHEAST)

	return tuple(plotDirection(pRiverPlot.getX(), pRiverPlot.getY(), direction)
					for direction in directions)

def _getRiverMouthPlots(pRiverPlot, cardinalDirection):
	if cardinalDirection == CD_NORTH:
		directions = (D_NORTH, D_NORTHEAST)
		pRiverMouthPlot = pRiverPlot
	elif cardinalDirection == CD_EAST:
		directions = (D_EAST, D_SOUTHEAST)
		pRiverMouthPlot = plotDirection(pRiverPlot.getX(), pRiverPlot.getY(), D_EAST)
	elif cardinalDirection == CD_SOUTH:
		directions = (D_SOUTH, D_SOUTHEAST)
		pRiverMouthPlot = plotDirection(pRiverPlot.getX(), pRiverPlot.getY(), D_SOUTH)
	else:
		directions = (D_WEST, D_SOUTHWEST)
		pRiverMouthPlot = pRiverPlot

	# Must return D_NORTH, D_EAST, D_SOUTH or D_WEST at first
	# (i.e. index is 0), for searching another river.
	return tuple(plotDirection(pRiverMouthPlot.getX(), pRiverMouthPlot.getY(), direction)
					for direction in directions)

def _printDebugStrings(pCenterPlot):
	plots = [plotXY(pCenterPlot.getX(), pCenterPlot.getY(), x, y)
				for x in range(-1, 2)
				for y in range(-1, 2)]

	print "    ------debug begin------"
	for pPlot in plots:
		print ("    -------- pos", pPlot.getX(), pPlot.getY())
		print ("        RiverID", pPlot.getRiverID())
		print ("        isRiver", pPlot.isRiver())
		print ("        isRiverSide", pPlot.isRiverSide())
		print ("        isNOfRiver", pPlot.isNOfRiver())
		print ("        isWOfRiver", pPlot.isWOfRiver())
		print ("        getRiverNSDirection", pPlot.getRiverNSDirection())
		print ("        getRiverWEDirection", pPlot.getRiverWEDirection())
		print ("        getRiverCrossingCount", pPlot.getRiverCrossingCount())
		print ("        isWater", pPlot.isWater())
		print ("        isLake", pPlot.isLake())
	print "    ------debug end------"
