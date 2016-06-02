## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import CvDiplomacy
import re
import CvScreenEnums
import CvConfigParser

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
ShowOCA = config.getboolean("Diplomacy Attitude", "Show", False)

AttitudeFontMap = {
		AttitudeTypes.ATTITUDE_FURIOUS	: "Art/Interface/Buttons/AttFonts/AttFont0.dds",
		AttitudeTypes.ATTITUDE_ANNOYED	: "Art/Interface/Buttons/AttFonts/AttFont1.dds",
		AttitudeTypes.ATTITUDE_CAUTIOUS	: "Art/Interface/Buttons/AttFonts/AttFont2.dds",
		AttitudeTypes.ATTITUDE_PLEASED	: "Art/Interface/Buttons/AttFonts/AttFont3.dds",
		AttitudeTypes.ATTITUDE_FRIENDLY	: "Art/Interface/Buttons/AttFonts/AttFont4.dds",
	}

def beginDiplomacy (argsList):
	"""
	This is what gets called when you first begin diplomacy
	The first parameter argsList[0] is the 'comment type', or how they feel about you
	"""
	global ShowOCA

	eComment = argsList[0]
	commentArgsSize = argsList[1]
	if (commentArgsSize):
		commentArgs = argsList[2:]
		CvUtil.pyAssert(len(commentArgs)==commentArgsSize, "comment args tuple size mismatch")
		print "tuple size", len(commentArgs), ", commentArgsSize ", commentArgsSize
	else:
		commentArgs=[]
	diploClass = CvDiplomacy.CvDiplomacy()

	screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
	iCenterX = screen.centerX(0)
	iY = screen.centerY(0) + 60
	screen.addPanel("OCABackground1", "", "", True, True, iCenterX + 685, iY, 80, 455, PanelStyles.PANEL_STYLE_EMPTY)
	screen.addPanel("OCABackground2", "", "", True, True, iCenterX + 245, iY, 80, 455, PanelStyles.PANEL_STYLE_EMPTY)
	screen.hide("OCABackground1")
	screen.hide("OCABackground2")

	eGetActivePlayer = gc.getGame().getActivePlayer()
	iActiveTeam = gc.getPlayer(eGetActivePlayer).getTeam()
	eWhoTradingWith = CyDiplomacy().getWhoTradingWith()
	eTeamTradingWith = gc.getPlayer(eWhoTradingWith).getTeam()
	iPlayerCount = 0

	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		eGetLoopPlayer = gc.getPlayer(iLoopPlayer)
		eGetLoopTeam = gc.getTeam(eGetLoopPlayer.getTeam())
		if (iLoopPlayer != eWhoTradingWith and iLoopPlayer != eGetActivePlayer and eGetLoopPlayer.isAlive() and eGetLoopTeam.isHasMet(eTeamTradingWith) and (eGetLoopTeam.isHasMet(iActiveTeam) or gc.getGame().isDebugMode()) and not eGetLoopPlayer.isBarbarian() and not eGetLoopPlayer.isMinorCiv()):

			szPlayerCount = str(iPlayerCount)
			playerPanelName1 = "PlayerPanel1" + szPlayerCount
			szGFCName1 = "PLayerPanelGFC1" + szPlayerCount
			szTextName1 = "PLayerPanelText1" + szPlayerCount
			screen.attachPanel("OCABackground1", playerPanelName1, "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
			screen.attachImageButton(playerPanelName1, szGFCName1, gc.getLeaderHeadInfo(eGetLoopPlayer.getLeaderType()).getButton(), GenericButtonSizes.BUTTON_SIZE_24, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, eWhoTradingWith, False)
			if (eGetLoopTeam.isAtWar(eTeamTradingWith)):
				screen.addDDSGFCAt(szGFCName1 + "_1", playerPanelName1, ArtFileMgr.getInterfaceArtInfo("CGE_RED_BUTTON_HILITE").getPath(), 20, 6, 24, 24, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, eWhoTradingWith, True)
			screen.addDDSGFCAt(szTextName1, playerPanelName1, AttitudeFontMap[eGetLoopPlayer.AI_getAttitude(eWhoTradingWith)], 45, 6, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

			if (ShowOCA):
				playerPanelName2 = "PlayerPanel2" + szPlayerCount
				szGFCName2 = "PLayerPanelGFC2" + szPlayerCount
				szTextName2 = "PLayerPanelText2" + szPlayerCount
				screen.attachPanel("OCABackground2", playerPanelName2, "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton(playerPanelName2, szGFCName2, gc.getLeaderHeadInfo(eGetLoopPlayer.getLeaderType()).getButton(), GenericButtonSizes.BUTTON_SIZE_24, WidgetTypes.WIDGET_LEADERHEAD, eWhoTradingWith, iLoopPlayer, False)
				screen.addDDSGFCAt(szTextName2, playerPanelName2, AttitudeFontMap[gc.getPlayer(eWhoTradingWith).AI_getAttitude(iLoopPlayer)], 45, 6, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			iPlayerCount += 1

	if (iPlayerCount < 13):
		screen.setPanelSize("OCABackground1", iCenterX + 685, iY, 80, 35*iPlayerCount)

	screen.show("OCABackground1")
	if (ShowOCA):
		if (iPlayerCount < 13):
			screen.setPanelSize("OCABackground2", iCenterX + 245, iY, 80, 35*iPlayerCount)
		screen.show("OCABackground2")

	diploClass.setAIComment(eComment, *commentArgs)	#unpack args tuple

def handleUserResponse (argsList):
	"First parameter of argsList if the comment they clicked on..."
	diploClass = CvDiplomacy.CvDiplomacy()

	eComment = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	diploClass.handleUserResponse(eComment, iData1, iData2)

def dealCanceled ():
	diploClass = CvDiplomacy.CvDiplomacy()

	diploClass.dealCanceled()

def refresh (argsList):
	diploClass = CvDiplomacy.CvDiplomacy()
	diploClass.determineResponses(argsList[0])

def toggleDebugLogging():
	CvDiplomacy.DebugLogging = not CvDiplomacy.DebugLogging

def setCGEOption(Section, Key, Value):
	global ShowOCA

	if (Key == "Show"):
		ShowOCA = Value

