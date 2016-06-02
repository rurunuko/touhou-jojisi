#
#   FILE:    Earth3.py(DQ3.py)
#   AUTHOR:  GRM7584 (Script adapted directly from Sirian's Terra script)
#   PURPOSE: Global map script - Simulates Randomized Earth
#-----------------------------------------------------------------------------
#   Copyright (c) 2005 Firaxis Games, Inc. All rights reserved.
#-----------------------------------------------------------------------------
#

from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import MultilayeredFractal
from CvMapGeneratorUtil import TerrainGenerator
from CvMapGeneratorUtil import FeatureGenerator

'''
MULTILAYERED FRACTAL NOTES

The MultilayeredFractal class was created for use with this script.

I worked to make it adaptable to other scripts, though, and eventually it
migrated in to the MapUtil file along with the other primary map classes.

- Bob Thomas   July 13, 2005


TERRA NOTES

Terra turns out to be our largest size map. This is the only map script
in the original release of Civ4 where the grids are this large!

This script is also the one that got me started in to map scripting. I had 
this idea early in the development cycle and just kept pestering until Soren 
turned me loose on it, finally. Once I got going, I just kept on going!

- Bob Thomas   September 20, 2005

Earth2 NOTES

This is based purely on the Terra script, albeit with a lot more similarity
to Earth in terms of landmasses. Rocky Climate and Normal Sea Levels strongly
recommended for maximum earthiness.

Earth3 NOTES

This script is identical to the Earth2 script, except that the original
civ placement script from Terra/Earth2 has been removed, and replaced with
the civ placement script from LiDiCesare's "Tectonics" script.  Civs will
now be placed anywhere in the New and Old World -- although the new placement script
should have removed the chance of them being located on one or two tile
islands.

Because the Earth3 map is significantly larger than comparable maps of its size,
it is recommended that the players use at least 2-3 more active civilizations
than the default recommendation for that size.  (E.g., use 9 or 10 civs on a
STANDARD sized map instead of the default 7.)

- John Palchak   December 9, 2007
'''

def getDescription():
    return "Derivative Mapscript Simulating a randomized DragonQuest3-World"

def isAdvancedMap():
    "This map should show up in simple mode"
    return 0

def getGridSize(argsList):
    "Enlarge the grids! According to Soren, DragonQuest3-World maps are usually huge anyway."
    grid_sizes = {
        WorldSizeTypes.WORLDSIZE_DUEL:      (10,6),
        WorldSizeTypes.WORLDSIZE_TINY:      (15,9),
        WorldSizeTypes.WORLDSIZE_SMALL:     (20,12),
        WorldSizeTypes.WORLDSIZE_STANDARD:  (25,15),
        WorldSizeTypes.WORLDSIZE_LARGE:     (30,18),
        WorldSizeTypes.WORLDSIZE_HUGE:      (40,24)
    }

def minStartingDistanceModifier():
    return -15


#
# Starting position generation.
#
def findStartingPlot(argsList):
	gc = CyGlobalContext()
	map = CyMap()
	dice = gc.getGame().getMapRand()
	iPlayers = gc.getGame().countCivPlayersEverAlive()
	areas = CvMapGeneratorUtil.getAreas()
	areaValue = [0] * map.getIndexAfterLastArea()	

	isolatedStarts = false
	userInputLandmass = CyMap().getCustomMapOption(0)
	if (userInputLandmass == 4):     #                 "Islands"
		isolatedStarts = true

	if iPlayers < 2 or iPlayers > 18:
		bSuccessFlag = False
		CyPythonMgr().allowDefaultImpl()
		return

	for area in areas:
		if area.isWater(): continue 
		areaValue[area.getID()] = area.calculateTotalBestNatureYield() + area.getNumRiverEdges() + 2 * area.countCoastalLand() + 3 * area.countNumUniqueBonusTypes()

	# Shuffle players so the same player doesn't always get the first pick.
	player_list = []
	for plrCheckLoop in range(18):
		if CyGlobalContext().getPlayer(plrCheckLoop).isEverAlive():
			player_list.append(plrCheckLoop)
	shuffledPlayers = []
	for playerLoop in range(iPlayers):
		iChoosePlayer = dice.get(len(player_list), "Shuffling Players - Highlands PYTHON")
		shuffledPlayers.append(player_list[iChoosePlayer])
		del player_list[iChoosePlayer]

	# Loop through players, assigning starts for each.
	for assign_loop in range(iPlayers):
		playerID = shuffledPlayers[assign_loop]
		player = gc.getPlayer(playerID)
		bestAreaValue = 0
		global bestArea
		bestArea = None
		for area in areas:
			if area.isWater(): continue 
			players = 2*area.getNumStartingPlots()
			#Avoid single players on landmasses:
			if (false == isolatedStarts and players == 0):
				if (assign_loop == iPlayers - 1):
					players = 4
				else:
					players = 2
			value = areaValue[area.getID()] / (1 + 2*area.getNumStartingPlots() )
			if (value > bestAreaValue):
				bestAreaValue = value;
				bestArea = area
		def isValid(playerID, x, y):
			global bestArea
			plot = CyMap().plot(x,y)
			if (plot.getArea() != bestArea):
				return false
			if (self.getLatitudeAtPlot(x,y) >= 75):
				return false
			return true
		findstart = CvMapGeneratorUtil.findStartingPlot(playerID,isValid)
		sPlot = map.plotByIndex(findstart)
		player.setStartingPlot(sPlot,true)
#	return None
	return CvMapGeneratorUtil.findStartingPlot(playerID, isValid)

class EarthMultilayeredFractal(CvMapGeneratorUtil.MultilayeredFractal):
    # Subclass. Only the controlling function overridden in this case.
    def generatePlotsByRegion(self):
        # Sirian's MultilayeredFractal class, controlling function.
        # You -MUST- customize this function for each use of the class.
        #
        # The following grain matrix is specific to DQ3.py
        sizekey = self.map.getWorldSize()
        sizevalues = {
            WorldSizeTypes.WORLDSIZE_DUEL:      (3,2,1),
            WorldSizeTypes.WORLDSIZE_TINY:      (3,2,1),
            WorldSizeTypes.WORLDSIZE_SMALL:     (4,2,1),
            WorldSizeTypes.WORLDSIZE_STANDARD:  (4,2,1),
            WorldSizeTypes.WORLDSIZE_LARGE:     (4,2,1),
            WorldSizeTypes.WORLDSIZE_HUGE:      (5,2,1)
            }
        (ScatterGrain, BalanceGrain, GatherGrain) = sizevalues[sizekey]

        # Sea Level adjustment (from user input), limited to value of 5%.
        sea = self.gc.getSeaLevelInfo(self.map.getSeaLevel()).getSeaLevelChange()
        sea = min(sea, 5)
        sea = max(sea, -5)

        # The following regions are specific to DQ3.py

        TohokuWestLon = 0.20
        TohokuEastLon = 0.38
        TohokuNorthLat = 0.95
        TohokuSouthLat = 0.89
        ShimabaraWestLon = 0.23
        ShimabaraEastLon = 0.38
        ShimabaraNorthLat = 0.07
        ShimabaraSouthLat = 0.00
        KyusyuWestLon = 0.43
        KyusyuEastLon = 0.54
        KyusyuNorthLat = 0.80
        KyusyuSouthLat = 0.35
        AtamiWestLon = 0.33
        AtamiEastLon = 0.52
        AtamiNorthLat = 0.71
        AtamiSouthLat = 0.56
        WakayamaWestLon = 0.68
        WakayamaEastLon = 0.86
        WakayamaNorthLat = 0.47
        WakayamaSouthLat = 0.35
        SaninWestLon = 0.54
        SaninEastLon = 0.68
        SaninNorthLat = 0.27
        SaninSouthLat = 0.15
        NotoWestLon = 0.56
        NotoEastLon = 0.59
        NotoNorthLat = 0.16
        NotoSouthLat = 0.10
        TsushimaWestLon = 0.69
        TsushimaEastLon = 0.90
        TsushimaNorthLat = 0.08
        TsushimaSouthLat = 0.00
        EhimeWestLon = 0.27
        EhimeEastLon = 0.35
        EhimeNorthLat = 0.84
        EhimeSouthLat = 0.70
        NaganoWestLon = 0.66
        NaganoEastLon = 0.79
        NaganoNorthLat = 0.82
        NaganoSouthLat = 0.57
        GihuWestLon = 0.37
        GihuEastLon = 0.43
        GihuNorthLat = 0.52
        GihuSouthLat = 0.38
        NagasakiWestLon = 0.26
        NagasakiEastLon = 0.29
        NagasakiNorthLat = 0.79
        NagasakiSouthLat = 0.64
        OitaWestLon = 0.29
        OitaEastLon = 0.48
        OitaNorthLat = 0.57
        OitaSouthLat = 0.48
        KagoshimaWestLon = 0.37
        KagoshimaEastLon = 0.47
        KagoshimaNorthLat = 0.21
        KagoshimaSouthLat = 0.09
        IseWestLon = 0.58
        IseEastLon = 0.67
        IseNorthLat = 0.72
        IseSouthLat = 0.66
        OkiWestLon = 0.56
        OkiEastLon = 0.62
        OkiNorthLat = 0.86
        OkiSouthLat = 0.76
        HamamatsuWestLon = 0.21
        HamamatsuEastLon = 0.30
        HamamatsuNorthLat = 0.59
        HamamatsuSouthLat = 0.52
        SatsumaWestLon = 0.24
        SatsumaEastLon = 0.32
        SatsumaNorthLat = 0.25
        SatsumaSouthLat = 0.18
        TokyoWestLon = 0.71
        TokyoEastLon = 0.82
        TokyoNorthLat = 0.51
        TokyoSouthLat = 0.27
        SendaiWestLon = 0.22
        SendaiEastLon = 0.36
        SendaiNorthLat = 0.42
        SendaiSouthLat = 0.24
        TakeshimaWestLon = 0.61
        TakeshimaEastLon = 0.74
        TakeshimaNorthLat = 0.99
        TakeshimaSouthLat = 0.90
        SanyoWestLon = 0.26
        SanyoEastLon = 0.48
        SanyoNorthLat = 0.91
        SanyoSouthLat = 0.80
        IshikawaWestLon = 0.74
        IshikawaEastLon = 0.78
        IshikawaNorthLat = 0.29
        IshikawaSouthLat = 0.14
        NagatoWestLon = 0.67
        NagatoEastLon = 0.77
        NagatoNorthLat = 0.87
        NagatoSouthLat = 0.80
        KinkiWestLon = 0.16
        KinkiEastLon = 0.23
        KinkiNorthLat = 0.71
        KinkiSouthLat = 0.62
        KochiWestLon = 0.78
        KochiEastLon = 0.84
        KochiNorthLat = 0.74
        KochiSouthLat = 0.60
        TanegashimaWestLon = 0.72
        TanegashimaEastLon = 0.77
        TanegashimaNorthLat = 0.58
        TanegashimaSouthLat = 0.50
        KashimaWestLon = 0.62
        KashimaEastLon = 0.67
        KashimaNorthLat = 0.17
        KashimaSouthLat = 0.09
        FukushimaWestLon = 0.17
        FukushimaEastLon = 0.35
        FukushimaNorthLat = 0.54
        FukushimaSouthLat = 0.39
        HachizyouWestLon = 0.43
        HachizyouEastLon = 0.52
        HachizyouNorthLat = 0.35
        HachizyouSouthLat = 0.29
        BousouWestLon = 0.53
        BousouEastLon = 0.60
        BousouNorthLat = 0.69
        BousouSouthLat = 0.48
        TokushimaWestLon = 0.20
        TokushimaEastLon = 0.28
        TokushimaNorthLat = 0.82
        TokushimaSouthLat = 0.70
        SadogashimaWestLon = 0.53
        SadogashimaEastLon = 0.61
        SadogashimaNorthLat = 0.48
        SadogashimaSouthLat = 0.38
        GotouWestLon = 0.14
        GotouEastLon = 0.20
        GotouNorthLat = 0.92
        GotouSouthLat = 0.81
        SetouchiWestLon = 0.37
        SetouchiEastLon = 0.41
        SetouchiNorthLat = 0.79
        SetouchiSouthLat = 0.73


        # Simulate Tohoku.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Tohoku
        TohokuWestX = int(self.iW * TohokuWestLon)
        TohokuEastX = int(self.iW * TohokuEastLon)
        TohokuNorthY = int(self.iH * TohokuNorthLat)
        TohokuSouthY = int(self.iH * TohokuSouthLat)
        TohokuWidth = TohokuEastX - TohokuWestX + 1
        TohokuHeight = TohokuNorthY - TohokuSouthY + 1

        TohokuWater = 45+sea
        
        self.generatePlotsInRegion(TohokuWater,
				   TohokuWidth, TohokuHeight,
				   TohokuWestX, TohokuSouthY,
				   BalanceGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Shimabara.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Shimabara
        ShimabaraWestX = int(self.iW * ShimabaraWestLon)
        ShimabaraEastX = int(self.iW * ShimabaraEastLon)
        ShimabaraNorthY = int(self.iH * ShimabaraNorthLat)
        ShimabaraSouthY = int(self.iH * ShimabaraSouthLat)
        ShimabaraWidth = ShimabaraEastX - ShimabaraWestX + 1
        ShimabaraHeight = ShimabaraNorthY - ShimabaraSouthY + 1

        ShimabaraWater = 55+sea
        
        self.generatePlotsInRegion(ShimabaraWater,
				   ShimabaraWidth, ShimabaraHeight,
				   ShimabaraWestX, ShimabaraSouthY,
				   ScatterGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   1, True,
				   False
				   )

        # Simulate the Western Hemisphere - Kyusyu.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Kyusyu Mainland
        KyusyuWestX = int(self.iW * KyusyuWestLon)
        KyusyuEastX = int(self.iW * KyusyuEastLon)
        KyusyuNorthY = int(self.iH * KyusyuNorthLat)
        KyusyuSouthY = int(self.iH * KyusyuSouthLat)
        KyusyuWidth = KyusyuEastX - KyusyuWestX + 1
        KyusyuHeight = KyusyuNorthY - KyusyuSouthY + 1

        KyusyuWater = 25+sea
        
        self.generatePlotsInRegion(KyusyuWater,
				   KyusyuWidth, KyusyuHeight,
				   KyusyuWestX, KyusyuSouthY,
				   GatherGrain, BalanceGrain,
				   self.iVertFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Atami.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Atami
        AtamiWestX = int(self.iW * AtamiWestLon)
        AtamiEastX = int(self.iW * AtamiEastLon)
        AtamiNorthY = int(self.iH * AtamiNorthLat)
        AtamiSouthY = int(self.iH * AtamiSouthLat)
        AtamiWidth = AtamiEastX - AtamiWestX + 1
        AtamiHeight = AtamiNorthY - AtamiSouthY + 1

        AtamiWater = 15+sea
        
        self.generatePlotsInRegion(AtamiWater,
				   AtamiWidth, AtamiHeight,
				   AtamiWestX, AtamiSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Wakayama.
        NiTextOut("Generating Central America (Python Japan) ...")
        # Set dimensions of Wakayama
        WakayamaWestX = int(self.iW * WakayamaWestLon)
        WakayamaEastX = int(self.iW * WakayamaEastLon)
        WakayamaNorthY = int(self.iH * WakayamaNorthLat)
        WakayamaSouthY = int(self.iH * WakayamaSouthLat)
        WakayamaWidth = WakayamaEastX - WakayamaWestX + 1
        WakayamaHeight = WakayamaNorthY - WakayamaSouthY + 1

        WakayamaWater = 35+sea
        
        self.generatePlotsInRegion(WakayamaWater,
				   WakayamaWidth, WakayamaHeight,
				   WakayamaWestX, WakayamaSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Sanin.
        NiTextOut("Generating Central America (Python Japan) ...")
        # Set dimensions of Sanin
        SaninWestX = int(self.iW * SaninWestLon)
        SaninEastX = int(self.iW * SaninEastLon)
        SaninNorthY = int(self.iH * SaninNorthLat)
        SaninSouthY = int(self.iH * SaninSouthLat)
        SaninWidth = SaninEastX - SaninWestX + 1
        SaninHeight = SaninNorthY - SaninSouthY + 1

        SaninWater = 35+sea
        
        self.generatePlotsInRegion(SaninWater,
				   SaninWidth, SaninHeight,
				   SaninWestX, SaninSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Noto.
        NiTextOut("Generating Central America (Python Japan) ...")
        # Set dimensions of Noto
        NotoWestX = int(self.iW * NotoWestLon)
        NotoEastX = int(self.iW * NotoEastLon)
        NotoNorthY = int(self.iH * NotoNorthLat)
        NotoSouthY = int(self.iH * NotoSouthLat)
        NotoWidth = NotoEastX - NotoWestX + 1
        NotoHeight = NotoNorthY - NotoSouthY + 1

        NotoWater = 35+sea
        
        self.generatePlotsInRegion(NotoWater,
				   NotoWidth, NotoHeight,
				   NotoWestX, NotoSouthY,
				   GatherGrain, GatherGrain,
				   self.iVertFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - The Tsushima.
        NiTextOut("Generating Central America (Python Japan) ...")
        # Set dimensions of The Tsushima
        TsushimaWestX = int(self.iW * TsushimaWestLon)
        TsushimaEastX = int(self.iW * TsushimaEastLon)
        TsushimaNorthY = int(self.iH * TsushimaNorthLat)
        TsushimaSouthY = int(self.iH * TsushimaSouthLat)
        TsushimaWidth = TsushimaEastX - TsushimaWestX + 1
        TsushimaHeight = TsushimaNorthY - TsushimaSouthY + 1

        TsushimaWater = 90+sea
        
        self.generatePlotsInRegion(TsushimaWater,
				   TsushimaWidth, TsushimaHeight,
				   TsushimaWestX, TsushimaSouthY,
				   ScatterGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Ehime.
        NiTextOut("Generating South America (Python Japan) ...")
        # Set dimensions of Ehime
        EhimeWestX = int(self.iW * EhimeWestLon)
        EhimeEastX = int(self.iW * EhimeEastLon)
        EhimeNorthY = int(self.iH * EhimeNorthLat)
        EhimeSouthY = int(self.iH * EhimeSouthLat)
        EhimeWidth = EhimeEastX - EhimeWestX + 1
        EhimeHeight = EhimeNorthY - EhimeSouthY + 1

        EhimeWater = 25+sea
        
        self.generatePlotsInRegion(EhimeWater,
				   EhimeWidth, EhimeHeight,
				   EhimeWestX, EhimeSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Nagano.
        NiTextOut("Generating South America (Python Japan) ...")
        # Set dimensions of Nagano
        NaganoWestX = int(self.iW * NaganoWestLon)
        NaganoEastX = int(self.iW * NaganoEastLon)
        NaganoNorthY = int(self.iH * NaganoNorthLat)
        NaganoSouthY = int(self.iH * NaganoSouthLat)
        NaganoWidth = NaganoEastX - NaganoWestX + 1
        NaganoHeight = NaganoNorthY - NaganoSouthY + 1

        NaganoWater = 35+sea
        
        self.generatePlotsInRegion(NaganoWater,
				   NaganoWidth, NaganoHeight,
				   NaganoWestX, NaganoSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Gihu.
        NiTextOut("Generating South America (Python Japan) ...")
        # Set dimensions of Gihu
        GihuWestX = int(self.iW * GihuWestLon)
        GihuEastX = int(self.iW * GihuEastLon)
        GihuNorthY = int(self.iH * GihuNorthLat)
        GihuSouthY = int(self.iH * GihuSouthLat)
        GihuWidth = GihuEastX - GihuWestX + 1
        GihuHeight = GihuNorthY - GihuSouthY + 1

        GihuWater = 25+sea
        
        self.generatePlotsInRegion(GihuWater,
				   GihuWidth, GihuHeight,
				   GihuWestX, GihuSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Nagasaki.
        NiTextOut("Generating Europe (Python Japan) ...")
        # Set dimensions of Nagasaki
        NagasakiWestX = int(self.iW * NagasakiWestLon)
        NagasakiEastX = int(self.iW * NagasakiEastLon)
        NagasakiNorthY = int(self.iH * NagasakiNorthLat)
        NagasakiSouthY = int(self.iH * NagasakiSouthLat)
        NagasakiWidth = NagasakiEastX - NagasakiWestX + 1
        NagasakiHeight = NagasakiNorthY - NagasakiSouthY + 1

        NagasakiWater = 15+sea
        
        self.generatePlotsInRegion(NagasakiWater,
				   NagasakiWidth, NagasakiHeight,
				   NagasakiWestX, NagasakiSouthY,
				   BalanceGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Oita.
        NiTextOut("Generating Europe (Python Japan) ...")
        # Set dimensions of Oita
        OitaWestX = int(self.iW * OitaWestLon)
        OitaEastX = int(self.iW * OitaEastLon)
        OitaNorthY = int(self.iH * OitaNorthLat)
        OitaSouthY = int(self.iH * OitaSouthLat)
        OitaWidth = OitaEastX - OitaWestX + 1
        OitaHeight = OitaNorthY - OitaSouthY + 1

        OitaWater = 25+sea
        
        self.generatePlotsInRegion(OitaWater,
				   OitaWidth, OitaHeight,
				   OitaWestX, OitaSouthY,
				   BalanceGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Kagoshima.
        NiTextOut("Generating Europe (Python Japan) ...")
        # Set dimensions of Kagoshima
        KagoshimaWestX = int(self.iW * KagoshimaWestLon)
        KagoshimaEastX = int(self.iW * KagoshimaEastLon)
        KagoshimaNorthY = int(self.iH * KagoshimaNorthLat)
        KagoshimaSouthY = int(self.iH * KagoshimaSouthLat)
        KagoshimaWidth = KagoshimaEastX - KagoshimaWestX + 1
        KagoshimaHeight = KagoshimaNorthY - KagoshimaSouthY + 1

        KagoshimaWater = 45+sea
        
        self.generatePlotsInRegion(KagoshimaWater,
				   KagoshimaWidth, KagoshimaHeight,
				   KagoshimaWestX, KagoshimaSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Ise.
        NiTextOut("Generating Europe (Python Japan) ...")
        # Set dimensions of Ise
        IseWestX = int(self.iW * IseWestLon)
        IseEastX = int(self.iW * IseEastLon)
        IseNorthY = int(self.iH * IseNorthLat)
        IseSouthY = int(self.iH * IseSouthLat)
        IseWidth = IseEastX - IseWestX + 1
        IseHeight = IseNorthY - IseSouthY + 1

        IseWater = 45+sea
        
        self.generatePlotsInRegion(IseWater,
				   IseWidth, IseHeight,
				   IseWestX, IseSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Oki.
        NiTextOut("Generating Europe (Python Japan) ...")
        # Set dimensions of Oki
        OkiWestX = int(self.iW * OkiWestLon)
        OkiEastX = int(self.iW * OkiEastLon)
        OkiNorthY = int(self.iH * OkiNorthLat)
        OkiSouthY = int(self.iH * OkiSouthLat)
        OkiWidth = OkiEastX - OkiWestX + 1
        OkiHeight = OkiNorthY - OkiSouthY + 1

        OkiWater = 90+sea
        
        self.generatePlotsInRegion(OkiWater,
				   OkiWidth, OkiHeight,
				   OkiWestX, OkiSouthY,
				   ScatterGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Satsuma.
        NiTextOut("Generating Satsuma (Python Japan) ...")
        # Set dimensions of Satsuma
        SatsumaWestX = int(self.iW * SatsumaWestLon)
        SatsumaEastX = int(self.iW * SatsumaEastLon)
        SatsumaNorthY = int(self.iH * SatsumaNorthLat)
        SatsumaSouthY = int(self.iH * SatsumaSouthLat)
        SatsumaWidth = SatsumaEastX - SatsumaWestX + 1
        SatsumaHeight = SatsumaNorthY - SatsumaSouthY + 1

        SatsumaWater = 45+sea
        
        self.generatePlotsInRegion(SatsumaWater,
				   SatsumaWidth, SatsumaHeight,
				   SatsumaWestX, SatsumaSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Hamamatsu.
        NiTextOut("Generating Satsuma (Python Japan) ...")
        # Set dimensions of Hamamatsu
        HamamatsuWestX = int(self.iW * HamamatsuWestLon)
        HamamatsuEastX = int(self.iW * HamamatsuEastLon)
        HamamatsuNorthY = int(self.iH * HamamatsuNorthLat)
        HamamatsuSouthY = int(self.iH * HamamatsuSouthLat)
        HamamatsuWidth = HamamatsuEastX - HamamatsuWestX + 1
        HamamatsuHeight = HamamatsuNorthY - HamamatsuSouthY + 1

        HamamatsuWater = 35+sea
        
        self.generatePlotsInRegion(HamamatsuWater,
				   HamamatsuWidth, HamamatsuHeight,
				   HamamatsuWestX, HamamatsuSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Tokyo.
        NiTextOut("Generating Tokyo (Python Japan) ...")
        # Set dimensions of Tokyo
        TokyoWestX = int(self.iW * TokyoWestLon)
        TokyoEastX = int(self.iW * TokyoEastLon)
        TokyoNorthY = int(self.iH * TokyoNorthLat)
        TokyoSouthY = int(self.iH * TokyoSouthLat)
        TokyoWidth = TokyoEastX - TokyoWestX + 1
        TokyoHeight = TokyoNorthY - TokyoSouthY + 1

        TokyoWater = 35+sea
        
        self.generatePlotsInRegion(TokyoWater,
				   TokyoWidth, TokyoHeight,
				   TokyoWestX, TokyoSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Sendai.
        NiTextOut("Generating Sendai (Python Japan) ...")
        # Set dimensions of Sendai
        SendaiWestX = int(self.iW * SendaiWestLon)
        SendaiEastX = int(self.iW * SendaiEastLon)
        SendaiNorthY = int(self.iH * SendaiNorthLat)
        SendaiSouthY = int(self.iH * SendaiSouthLat)
        SendaiWidth = SendaiEastX - SendaiWestX + 1
        SendaiHeight = SendaiNorthY - SendaiSouthY + 1

        SendaiWater = 35+sea
        
        self.generatePlotsInRegion(SendaiWater,
				   SendaiWidth, SendaiHeight,
				   SendaiWestX, SendaiSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Takeshima.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Takeshima
        TakeshimaWestX = int(self.iW * TakeshimaWestLon)
        TakeshimaEastX = int(self.iW * TakeshimaEastLon)
        TakeshimaNorthY = int(self.iH * TakeshimaNorthLat)
        TakeshimaSouthY = int(self.iH * TakeshimaSouthLat)
        TakeshimaWidth = TakeshimaEastX - TakeshimaWestX + 1
        TakeshimaHeight = TakeshimaNorthY - TakeshimaSouthY + 1

        TakeshimaWater = 60+sea
        
        self.generatePlotsInRegion(TakeshimaWater,
				   TakeshimaWidth, TakeshimaHeight,
				   TakeshimaWestX, TakeshimaSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Sanyo.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Sanyo
        SanyoWestX = int(self.iW * SanyoWestLon)
        SanyoEastX = int(self.iW * SanyoEastLon)
        SanyoNorthY = int(self.iH * SanyoNorthLat)
        SanyoSouthY = int(self.iH * SanyoSouthLat)
        SanyoWidth = SanyoEastX - SanyoWestX + 1
        SanyoHeight = SanyoNorthY - SanyoSouthY + 1

        SanyoWater = 25+sea
        
        self.generatePlotsInRegion(SanyoWater,
				   SanyoWidth, SanyoHeight,
				   SanyoWestX, SanyoSouthY,
				   GatherGrain, GatherGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Ishikawa.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Ishikawa
        IshikawaWestX = int(self.iW * IshikawaWestLon)
        IshikawaEastX = int(self.iW * IshikawaEastLon)
        IshikawaNorthY = int(self.iH * IshikawaNorthLat)
        IshikawaSouthY = int(self.iH * IshikawaSouthLat)
        IshikawaWidth = IshikawaEastX - IshikawaWestX + 1
        IshikawaHeight = IshikawaNorthY - IshikawaSouthY + 1

        IshikawaWater = 45+sea
        
        self.generatePlotsInRegion(IshikawaWater,
				   IshikawaWidth, IshikawaHeight,
				   IshikawaWestX, IshikawaSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Nagato.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Nagato
        NagatoWestX = int(self.iW * NagatoWestLon)
        NagatoEastX = int(self.iW * NagatoEastLon)
        NagatoNorthY = int(self.iH * NagatoNorthLat)
        NagatoSouthY = int(self.iH * NagatoSouthLat)
        NagatoWidth = NagatoEastX - NagatoWestX + 1
        NagatoHeight = NagatoNorthY - NagatoSouthY + 1

        NagatoWater = 55+sea
        
        self.generatePlotsInRegion(NagatoWater,
				   NagatoWidth, NagatoHeight,
				   NagatoWestX, NagatoSouthY,
				   GatherGrain, BalanceGrain,
				   self.iVertFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Kinki.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Kinki
        KinkiWestX = int(self.iW * KinkiWestLon)
        KinkiEastX = int(self.iW * KinkiEastLon)
        KinkiNorthY = int(self.iH * KinkiNorthLat)
        KinkiSouthY = int(self.iH * KinkiSouthLat)
        KinkiWidth = KinkiEastX - KinkiWestX + 1
        KinkiHeight = KinkiNorthY - KinkiSouthY + 1

        KinkiWater = 35+sea
        
        self.generatePlotsInRegion(KinkiWater,
				   KinkiWidth, KinkiHeight,
				   KinkiWestX, KinkiSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Kochi.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Kochi
        KochiWestX = int(self.iW * KochiWestLon)
        KochiEastX = int(self.iW * KochiEastLon)
        KochiNorthY = int(self.iH * KochiNorthLat)
        KochiSouthY = int(self.iH * KochiSouthLat)
        KochiWidth = KochiEastX - KochiWestX + 1
        KochiHeight = KochiNorthY - KochiSouthY + 1

        KochiWater = 45+sea
        
        self.generatePlotsInRegion(KochiWater,
				   KochiWidth, KochiHeight,
				   KochiWestX, KochiSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Tanegashima.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Tanegashima
        TanegashimaWestX = int(self.iW * TanegashimaWestLon)
        TanegashimaEastX = int(self.iW * TanegashimaEastLon)
        TanegashimaNorthY = int(self.iH * TanegashimaNorthLat)
        TanegashimaSouthY = int(self.iH * TanegashimaSouthLat)
        TanegashimaWidth = TanegashimaEastX - TanegashimaWestX + 1
        TanegashimaHeight = TanegashimaNorthY - TanegashimaSouthY + 1

        TanegashimaWater = 65+sea
        
        self.generatePlotsInRegion(TanegashimaWater,
				   TanegashimaWidth, TanegashimaHeight,
				   TanegashimaWestX, TanegashimaSouthY,
				   ScatterGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Kashima.
        NiTextOut("Generating Asia (Python Japan) ...")
        # Set dimensions of Kashima
        KashimaWestX = int(self.iW * KashimaWestLon)
        KashimaEastX = int(self.iW * KashimaEastLon)
        KashimaNorthY = int(self.iH * KashimaNorthLat)
        KashimaSouthY = int(self.iH * KashimaSouthLat)
        KashimaWidth = KashimaEastX - KashimaWestX + 1
        KashimaHeight = KashimaNorthY - KashimaSouthY + 1

        KashimaWater = 35+sea
        
        self.generatePlotsInRegion(KashimaWater,
				   KashimaWidth, KashimaHeight,
				   KashimaWestX, KashimaSouthY,
				   BalanceGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Eastern Hemisphere - Fukushima.
        NiTextOut("Generating Fukushima (Python Japan) ...")
        # Set dimensions of Fukushima
        FukushimaWestX = int(self.iW * FukushimaWestLon)
        FukushimaEastX = int(self.iW * FukushimaEastLon)
        FukushimaNorthY = int(self.iH * FukushimaNorthLat)
        FukushimaSouthY = int(self.iH * FukushimaSouthLat)
        FukushimaWidth = FukushimaEastX - FukushimaWestX + 1
        FukushimaHeight = FukushimaNorthY - FukushimaSouthY + 1

        FukushimaWater = 25+sea
        
        self.generatePlotsInRegion(FukushimaWater,
				   FukushimaWidth, FukushimaHeight,
				   FukushimaWestX, FukushimaSouthY,
				   GatherGrain, BalanceGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the South Pacific - South Pacific.
        NiTextOut("Generating Pacific (Python Japan) ...")
        # Set dimensions of South Pacific
        HachizyouWestX = int(self.iW * HachizyouWestLon)
        HachizyouEastX = int(self.iW * HachizyouEastLon)
        HachizyouNorthY = int(self.iH * HachizyouNorthLat)
        HachizyouSouthY = int(self.iH * HachizyouSouthLat)
        HachizyouWidth = HachizyouEastX - HachizyouWestX + 1
        HachizyouHeight = HachizyouNorthY - HachizyouSouthY + 1

        HachizyouWater = 75+sea
        
        self.generatePlotsInRegion(HachizyouWater,
				   HachizyouWidth, HachizyouHeight,
				   HachizyouWestX, HachizyouSouthY,
				   ScatterGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Bousou.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Bousou
        BousouWestX = int(self.iW * BousouWestLon)
        BousouEastX = int(self.iW * BousouEastLon)
        BousouNorthY = int(self.iH * BousouNorthLat)
        BousouSouthY = int(self.iH * BousouSouthLat)
        BousouWidth = BousouEastX - BousouWestX + 1
        BousouHeight = BousouNorthY - BousouSouthY + 1

        BousouWater = 45+sea
        
        self.generatePlotsInRegion(BousouWater,
				   BousouWidth, BousouHeight,
				   BousouWestX, BousouSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Tokushima.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Tokushima
        TokushimaWestX = int(self.iW * TokushimaWestLon)
        TokushimaEastX = int(self.iW * TokushimaEastLon)
        TokushimaNorthY = int(self.iH * TokushimaNorthLat)
        TokushimaSouthY = int(self.iH * TokushimaSouthLat)
        TokushimaWidth = TokushimaEastX - TokushimaWestX + 1
        TokushimaHeight = TokushimaNorthY - TokushimaSouthY + 1

        TokushimaWater = 35+sea
        
        self.generatePlotsInRegion(TokushimaWater,
				   TokushimaWidth, TokushimaHeight,
				   TokushimaWestX, TokushimaSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Sadogashima.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Sadogashima
        SadogashimaWestX = int(self.iW * SadogashimaWestLon)
        SadogashimaEastX = int(self.iW * SadogashimaEastLon)
        SadogashimaNorthY = int(self.iH * SadogashimaNorthLat)
        SadogashimaSouthY = int(self.iH * SadogashimaSouthLat)
        SadogashimaWidth = SadogashimaEastX - SadogashimaWestX + 1
        SadogashimaHeight = SadogashimaNorthY - SadogashimaSouthY + 1

        SadogashimaWater = 80+sea
        
        self.generatePlotsInRegion(SadogashimaWater,
				   SadogashimaWidth, SadogashimaHeight,
				   SadogashimaWestX, SadogashimaSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Gotou.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Gotou
        GotouWestX = int(self.iW * GotouWestLon)
        GotouEastX = int(self.iW * GotouEastLon)
        GotouNorthY = int(self.iH * GotouNorthLat)
        GotouSouthY = int(self.iH * GotouSouthLat)
        GotouWidth = GotouEastX - GotouWestX + 1
        GotouHeight = GotouNorthY - GotouSouthY + 1

        GotouWater = 80+sea
        
        self.generatePlotsInRegion(GotouWater,
				   GotouWidth, GotouHeight,
				   GotouWestX, GotouSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # Simulate the Western Hemisphere - Setouchi.
        NiTextOut("Generating North America (Python Japan) ...")
        # Set dimensions of Setouchi
        SetouchiWestX = int(self.iW * SetouchiWestLon)
        SetouchiEastX = int(self.iW * SetouchiEastLon)
        SetouchiNorthY = int(self.iH * SetouchiNorthLat)
        SetouchiSouthY = int(self.iH * SetouchiSouthLat)
        SetouchiWidth = SetouchiEastX - SetouchiWestX + 1
        SetouchiHeight = SetouchiNorthY - SetouchiSouthY + 1

        SetouchiWater = 80+sea
        
        self.generatePlotsInRegion(SetouchiWater,
				   SetouchiWidth, SetouchiHeight,
				   SetouchiWestX, SetouchiSouthY,
				   GatherGrain, ScatterGrain,
				   self.iRoundFlags, self.iTerrainFlags,
				   5, 5,
				   True, 5,
				   -1, False,
				   False
				   )

        # All regions have been processed. Plot Type generation completed.
        return self.wholeworldPlotTypes

'''
Regional Variables Key:

iWaterPercent,
iRegionWidth, iRegionHeight,
iRegionWestX, iRegionSouthY,
iRegionGrain, iRegionHillsGrain,
iRegionPlotFlags, iRegionTerrainFlags,
iRegionFracXExp, iRegionFracYExp,
bShift, iStrip,
rift_grain, has_center_rift,
invert_heights
'''

def generatePlotTypes():
    NiTextOut("Setting Plot Types (Python Japan) ...")
    # Call generatePlotsByRegion() function, from TerraMultilayeredFractal subclass.
    global plotgen
    plotgen = EarthMultilayeredFractal()
    return plotgen.generatePlotsByRegion()

class Earth3TerrainGenerator(CvMapGeneratorUtil.TerrainGenerator):
        def __init__(self, iDesertPercent=30, iPlainsPercent=24,
	             fSnowLatitude=0.82, fTundraLatitude=0.75,
	             fGrassLatitude=0.1, fDesertBottomLatitude=0.1,
	             fDesertTopLatitude=0.3, fracXExp=-1,
	             fracYExp=-1, grain_amount=3):
                self.gc = CyGlobalContext()
		self.map = CyMap()

		grain_amount += self.gc.getWorldInfo(self.map.getWorldSize()).getTerrainGrainChange()
		
		self.grain_amount = grain_amount

		self.iWidth = self.map.getGridWidth()
		self.iHeight = self.map.getGridHeight()

		self.mapRand = self.gc.getGame().getMapRand()
		
		self.iFlags = 0  # Disallow FRAC_POLAR flag, to prevent "zero row" problems.
		if self.map.isWrapX(): self.iFlags += CyFractal.FracVals.FRAC_WRAP_X
		if self.map.isWrapY(): self.iFlags += CyFractal.FracVals.FRAC_WRAP_Y

		self.deserts=CyFractal()
		self.plains=CyFractal()
		self.variation=CyFractal()

		iDesertPercent += self.gc.getClimateInfo(self.map.getClimate()).getDesertPercentChange()
		iDesertPercent = min(iDesertPercent, 100)
		iDesertPercent = max(iDesertPercent, 0)

		self.iDesertPercent = iDesertPercent
		self.iPlainsPercent = iPlainsPercent

		self.iDesertTopPercent = 100
		self.iDesertBottomPercent = max(0,int(100-iDesertPercent))
		self.iPlainsTopPercent = 100
		self.iPlainsBottomPercent = max(0,int(100-iDesertPercent-iPlainsPercent))
		self.iMountainTopPercent = 75
		self.iMountainBottomPercent = 60

		fSnowLatitude += self.gc.getClimateInfo(self.map.getClimate()).getSnowLatitudeChange()
		fSnowLatitude = min(fSnowLatitude, 1.0)
		fSnowLatitude = max(fSnowLatitude, 0.0)
		self.fSnowLatitude = fSnowLatitude

		fTundraLatitude += self.gc.getClimateInfo(self.map.getClimate()).getTundraLatitudeChange()
		fTundraLatitude = min(fTundraLatitude, 1.0)
		fTundraLatitude = max(fTundraLatitude, 0.0)
		self.fTundraLatitude = fTundraLatitude

		fGrassLatitude += self.gc.getClimateInfo(self.map.getClimate()).getGrassLatitudeChange()
		fGrassLatitude = min(fGrassLatitude, 1.0)
		fGrassLatitude = max(fGrassLatitude, 0.0)
		self.fGrassLatitude = fGrassLatitude

		fDesertBottomLatitude += self.gc.getClimateInfo(self.map.getClimate()).getDesertBottomLatitudeChange()
		fDesertBottomLatitude = min(fDesertBottomLatitude, 1.0)
		fDesertBottomLatitude = max(fDesertBottomLatitude, 0.0)
		self.fDesertBottomLatitude = fDesertBottomLatitude

		fDesertTopLatitude += self.gc.getClimateInfo(self.map.getClimate()).getDesertTopLatitudeChange()
		fDesertTopLatitude = min(fDesertTopLatitude, 1.0)
		fDesertTopLatitude = max(fDesertTopLatitude, 0.0)
		self.fDesertTopLatitude = fDesertTopLatitude
		
		self.fracXExp = fracXExp
		self.fracYExp = fracYExp

		self.initFractals()
		
	def initFractals(self):
		self.deserts.fracInit(self.iWidth, self.iHeight, self.grain_amount, self.mapRand, self.iFlags, self.fracXExp, self.fracYExp)
		self.iDesertTop = self.deserts.getHeightFromPercent(self.iDesertTopPercent)
		self.iDesertBottom = self.deserts.getHeightFromPercent(self.iDesertBottomPercent)

		self.plains.fracInit(self.iWidth, self.iHeight, self.grain_amount+1, self.mapRand, self.iFlags, self.fracXExp, self.fracYExp)
		self.iPlainsTop = self.plains.getHeightFromPercent(self.iPlainsTopPercent)
		self.iPlainsBottom = self.plains.getHeightFromPercent(self.iPlainsBottomPercent)

		self.variation.fracInit(self.iWidth, self.iHeight, self.grain_amount, self.mapRand, self.iFlags, self.fracXExp, self.fracYExp)

		self.terrainDesert = self.gc.getInfoTypeForString("TERRAIN_DESERT")
		self.terrainPlains = self.gc.getInfoTypeForString("TERRAIN_PLAINS")
		self.terrainIce = self.gc.getInfoTypeForString("TERRAIN_SNOW")
		self.terrainTundra = self.gc.getInfoTypeForString("TERRAIN_TUNDRA")
		self.terrainGrass = self.gc.getInfoTypeForString("TERRAIN_GRASS")

	def getLatitudeAtPlot(self, iX, iY):
		"""given a point (iX,iY) such that (0,0) is in the NW,
		returns a value between 0.0 (tropical) and 1.0 (polar).
		This function can be overridden to change the latitudes; for example,
		to make an entire map have temperate terrain, or to make terrain change from east to west
		instead of from north to south"""
		lat = abs((self.iHeight / 2) - iY)/float(self.iHeight/2) # 0.0 = equator, 1.0 = pole

		# Adjust latitude using self.variation fractal, to mix things up:
		lat += (128 - self.variation.getHeight(iX, iY))/(255.0 * 5.0)

		# Limit to the range [0, 1]:
		if lat < 0:
			lat = 0.0
		if lat > 1:
			lat = 1.0

		return lat

	def generateTerrain(self):		
		terrainData = [0]*(self.iWidth*self.iHeight)
		for x in range(self.iWidth):
			for y in range(self.iHeight):
				iI = y*self.iWidth + x
				terrain = self.generateTerrainAtPlot(x, y)
				terrainData[iI] = terrain
		return terrainData

	def generateTerrainAtPlot(self,iX,iY):
		lat = self.getLatitudeAtPlot(iX,iY)

		if (self.map.plot(iX, iY).isWater()):
			return self.map.plot(iX, iY).getTerrainType()

		terrainVal = self.terrainGrass

		if lat >= self.fSnowLatitude:
			terrainVal = self.terrainIce
		elif lat >= self.fTundraLatitude:
			terrainVal = self.terrainTundra
		elif lat < self.fGrassLatitude:
			terrainVal = self.terrainGrass
		else:
			desertVal = self.deserts.getHeight(iX, iY)
			plainsVal = self.plains.getHeight(iX, iY)
			if ((desertVal >= self.iDesertBottom) and (desertVal <= self.iDesertTop) and (lat >= self.fDesertBottomLatitude) and (lat < self.fDesertTopLatitude)):
				terrainVal = self.terrainDesert
			elif ((plainsVal >= self.iPlainsBottom) and (plainsVal <= self.iPlainsTop)):
				terrainVal = self.terrainPlains

		if (terrainVal == TerrainTypes.NO_TERRAIN):
			return self.map.plot(iX, iY).getTerrainType()

		return terrainVal

def generateTerrainTypes():
	NiTextOut("Generating Terrain (Python Terra) ...")
	terraingen = Earth3TerrainGenerator()
	terrainTypes = terraingen.generateTerrain()
	return terrainTypes

def addFeatures():
	NiTextOut("Adding Features (Python Japan) ...")
	featuregen = FeatureGenerator()
	featuregen.addFeatures()
	return 0
