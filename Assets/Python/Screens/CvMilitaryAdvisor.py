## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
#import time
import Popup as PyPopup
import CGEUtils

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

class UnitGroup:
	def __init__(self):
		self.label = ""
		self.units = []

	def setLabel(self, label):
		self.label = label

	def addUnit(self, idx):
		self.units.append(idx)

class CombatTypeGroupHelper:
	def getGroupId(self, unit):
		return unit.getUnitCombatType()

	def getGroupLabel(self,groupId):
		if (groupId != -1):
			return gc.getUnitCombatInfo(groupId).getDescription()
		else:
			return localText.getText( "TXT_KEY_MILITARY_ADVISOR_DOMESTIC_UNITS", () ) + str(gc.getNumUnitCombatInfos())

	def compareGroups(self, groupId1, groupId2):
		return cmp(groupId1, groupId2)

class StackGroupHelper:
	SINGLE_STACK = -1

	def __init__(self):
		self.stackList = [self.SINGLE_STACK]

	def getGroupId(self, unit):
		plot = CyMap().plot(unit.getX(), unit.getY())
		if (not plot.isCity()):
			numUnits = 0
			for unitIndex in range(plot.getNumUnits()):
				if (plot.getUnit(unitIndex).getOwner() == unit.getOwner()):
					numUnits += 1
			if (numUnits == 1):
				return self.SINGLE_STACK

		plotIndex = CyMap().plotNum(unit.getX(), unit.getY())

		if (not plotIndex in self.stackList):
			self.stackList.append(plotIndex)

		return plotIndex

	def getGroupLabel(self, groupId):
		if (groupId == self.SINGLE_STACK):
			return localText.getText( "TXT_KEY_MILITARY_ADVISOR_SINGLE_STACK", () )
		plot = CyMap().plotByIndex(groupId)
		if (plot.isCity()):
			return plot.getPlotCity().getName()
		else:
			return "%s (%d, %d)"%(localText.getText("TXT_KEY_MILITARY_ADVISOR_STACK", ()), plot.getX(), plot.getY())

	def compareGroups(self, groupId1, groupId2):
		if (groupId1 == self.SINGLE_STACK):
			return 1
		elif (groupId2 == self.SINGLE_STACK):
			return -1
		elif (CyMap().plotByIndex(groupId1).isCity() and not CyMap().plotByIndex(groupId2).isCity()):
			return -1
		elif (CyMap().plotByIndex(groupId2).isCity() and not CyMap().plotByIndex(groupId1).isCity()):
			return 1
		else:
			return cmp(self.getGroupLabel(groupId1), self.getGroupLabel(groupId2))

class LocationGroupHelper:
	INVALID		= -1
	CITY		= 0
	HOME		= 1
	FRIENDLY	= 2
	NEUTRAL		= 3
	ENEMY		= 4
	RIVAL		= 5

	def getGroupId(self, unit):
		plot = CyMap().plot(unit.getX(), unit.getY())
		if (not plot.isOwned()):
			return self.NEUTRAL
		if (plot.getOwner() == unit.getOwner()):
			if (plot.isCity()):
				return self.CITY
			else:
				return self.HOME

		unitTeam = gc.getTeam(gc.getPlayer(unit.getOwner()).getTeam())
		plotTeam = gc.getPlayer(plot.getOwner()).getTeam()

		if (unitTeam.isOpenBorders(plotTeam)):
			return self.FRIENDLY
		else:
			return self.RIVAL

		if (unitTeam.isAtWar(plotTeam)):
			return self.ENEMY

		return self.INVALID

	def getGroupLabel(self,groupId):
		if (groupId == self.CITY):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_CITY_GARRISON", ())
		elif (groupId == self.HOME):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_HOME_TERRITORY", ())
		elif (groupId == self.FRIENDLY):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_FRIENDLY_TERRITORY", ())
		elif (groupId == self.NEUTRAL):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_NEUTRAL_TERRITORY", ())
		elif (groupId == self.ENEMY):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_ENEMY_TERRITORY", ())
		elif (groupId == self.RIVAL):
			return localText.getText("TXT_KEY_MILITARY_ADVISOR_RIVAL_TERRITORY", ())
		else:
			return "ERROR, INVALID GROUP ID (LocationGroup)"

	def compareGroups(self, groupId1, groupId2):
		return cmp(groupId1, groupId2)
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

class CvMilitaryAdvisor:
	"Military Advisor"

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################
	groupSelectionName = "MIL_groupSelection"
	unitCheckBox = "MIL_unitCheckBox"

	NO_GROUPS_ID = 0
	STACK_GROUP_ID = 1
	COMBAT_TYPE_GROUP_ID = 2
	LOCATION_GROUP_ID = 3
	AUTO_RECON_ID = 4

	numGroups = 0
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

	def __init__(self, screenId):
		self.screenId = screenId
		self.MILITARY_SCREEN_NAME = "MilitaryAdvisor"
		self.BACKGROUND_ID = "MilitaryAdvisorBackground"
		self.EXIT_ID = "MilitaryAdvisorExitWidget"

		self.WIDGET_ID = "MilitaryAdvisorWidget"
		self.REFRESH_WIDGET_ID = "MilitaryAdvisorRefreshWidget"
		self.ATTACH_WIDGET_ID = "MilitaryAdvisorAttachWidget"
		self.SELECTION_WIDGET_ID = "MilitaryAdvisorSelectionWidget"
		self.ATTACHED_WIDGET_ID = "MilitaryAdvisorAttachedWidget" # no need to explicitly delete these
		self.LEADER_BUTTON_ID = "MilitaryAdvisorLeaderButton"
		self.UNIT_PANEL_ID = "MilitaryAdvisorUnitPanel"
		self.LEADER_PANEL_ID = "MilitaryAdvisorLeaderPanel"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList"
		self.RADAR_PANEL = "MilitaryAdvisorRadarPanel"
		self.RADAR_BUTTON = "MilitaryAdvisorRadarPanelButton"
		self.GREAT_GENERAL_BAR_ID = "MilitaryAdvisorGreatGeneralBar"
		self.GREAT_GENERAL_LABEL_ID = "MilitaryAdvisorGreatGeneralLabel"
		self.AUTO_ORDER_CHECKBOX = "MilitaryAdvisorAutoOrderCheckBox"

		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 8
		self.BORDER_WIDTH = 4
		self.W_HELP_AREA = 200

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.nWidgetCount = 0
		self.nRefreshWidgetCount = 0
		self.nAttachedWidgetCount = 0
		self.iActivePlayer = -1
		self.selectedPlayerList = []
		self.selectedUnitList = []
		self.enemyUnitList = set()
		self.RadarState = False

		self.X_TEXT = 625
		self.Y_TEXT = 190
		self.W_TEXT = 380
		self.H_TEXT = 500

		self.X_LEADERS = 20
		self.Y_LEADERS = 80
		self.W_LEADERS = 985
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12

		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		self.bUnitDetails = False
		self.iShiftKeyDown = 0

	def getScreen(self):
		return CyGInterfaceScreen(self.MILITARY_SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	# Screen construction function
	def interfaceScreen(self):

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.EXIT_TEXT = u"<font=4>%s</font>"%(localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper())
		self.TITLE = u"<font=4b>%s</font>"%(localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper())

		self.nWidgetCount = 0

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()
		self.X_EXIT = self.W_SCREEN - 30
		self.Y_EXIT = self.H_SCREEN - 37
		self.Y_BOTTOM_PANEL = self.H_SCREEN - 55
		self.iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")

		screen = self.getScreen()

		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		screen.addDrawControl(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.unitBackgroundName = self.getNextWidgetName()
		screen.addPanel(self.unitBackgroundName, "", "", True, True, 0, 48, 305, self.H_SCREEN - 48, PanelStyles.PANEL_STYLE_CITY_LEFT)
		self.ordersPanelName = self.getNextWidgetName()
		screen.addPanel( self.ordersPanelName, "", "", True, True, 305, self.H_SCREEN - 55, self.W_SCREEN - 305, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.addPanel( "TopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		self.viewX = 315
		self.viewWidth = self.W_SCREEN - 325
		self.viewHeight = self.H_SCREEN - 270
		self.viewY = self.H_SCREEN - self.viewHeight - 100 #ミニマップのy座標
		self.viewMargin = 20
		#ミニマップの青ラウンドバックグラウンドパネル
		screen.addPanel( "", u"", "", False, False, self.viewX, self.viewY, self.viewWidth, self.viewHeight, PanelStyles.PANEL_STYLE_MAIN )

		self.initMinimap()

		screen.addDropDownBoxGFC(self.groupSelectionName, 15, 8, 260, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(self.groupSelectionName, localText.getText("TXT_KEY_MILITARY_ADVISOR_DONT_GROUP_UNITS", ()), self.NO_GROUPS_ID, self.NO_GROUPS_ID, True)
		screen.addPullDownString(self.groupSelectionName, localText.getText("TXT_KEY_MILITARY_ADVISOR_GROUP_BY_STACK", ()), self.STACK_GROUP_ID, self.STACK_GROUP_ID, False)
		screen.addPullDownString(self.groupSelectionName, localText.getText("TXT_KEY_MILITARY_ADVISOR_GROUP_BY_COMBAT_TYPE", ()), self.COMBAT_TYPE_GROUP_ID, self.COMBAT_TYPE_GROUP_ID, False)
		screen.addPullDownString(self.groupSelectionName, localText.getText("TXT_KEY_MILITARY_ADVISOR_GROUP_BY_LOCATION", ()), self.LOCATION_GROUP_ID, self.LOCATION_GROUP_ID, False)
		screen.addPullDownString(self.groupSelectionName, localText.getText("TXT_KEY_MILITARY_ADVISOR_AUTO_RECON", ()), self.AUTO_RECON_ID, self.AUTO_RECON_ID, False)

		self.unitPanelName = self.getNextWidgetName()
		self.unitGroupName = self.getNextWidgetName()

		self.szHeader = self.getNextWidgetName()
		screen.setText(self.szHeader, "Background", self.TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.X_LEADERS = self.viewX
		self.Y_LEADERS = 60
		self.W_LEADERS = self.viewWidth -110
		self.H_LEADERS = 102
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12
		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		screen.addPanel(self.LEADER_PANEL_ID, "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)
		# Radar Button
		self.enemyUnitList = []
		self.RadarState = False
		screen.addPanel(self.RADAR_PANEL, "", "", False, True, self.W_SCREEN - 112, self.Y_LEADERS, self.H_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)
		screen.addCheckBoxGFC(self.RADAR_BUTTON, "Art/Interface/Buttons/Radar.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.W_SCREEN - 93, self.Y_LEADERS + 19, 64, 64, WidgetTypes.WIDGET_GENERAL, 1000, 1000, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setState(self.RADAR_BUTTON, False)

		screen.addCheckBoxGFC(self.AUTO_ORDER_CHECKBOX, "Art/Interface/Buttons/AutoOrder.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_EXIT-32, self.Y_BOTTOM_PANEL - 35, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setState(self.AUTO_ORDER_CHECKBOX, CGEUtils.CGEUtils().isAutoOrder())

		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos()
		self.selectedUnitList = []
		self.selectedPlayerList.append(self.iActivePlayer)

		self.X_GREAT_GENERAL_BAR = self.X_LEADERS + 10
		self.Y_GREAT_GENERAL_BAR = self.Y_BOTTOM_PANEL - 35
		self.W_GREAT_GENERAL_BAR = 300
		self.H_GREAT_GENERAL_BAR = 30
		self.drawCombatExperience()

		self.refresh(True)

	def initMinimap(self):
		screen = self.getScreen()
		mapWidth = self.viewWidth - 2 * self.viewMargin
		mapHeight = self.viewHeight - 2 * self.viewMargin

		mapHeightPref = (mapWidth * CyMap().getGridHeight()) / CyMap().getGridWidth()
		if (mapHeightPref > mapHeight):
			mapWidth = (mapHeight * CyMap().getGridWidth()) / CyMap().getGridHeight()
			horMapMargin = (self.viewWidth - mapWidth) / 2
			verMapMargin = self.viewMargin
		else:
			mapHeight = mapHeightPref
			horMapMargin = self.viewMargin
			verMapMargin = (self.viewHeight - mapHeight) / 2
		viewY = self.H_SCREEN - 100
		screen.initMinimap( self.viewX + horMapMargin, self.viewX + self.viewWidth - horMapMargin
						  , self.viewY + verMapMargin, self.viewY + self.viewHeight - verMapMargin, self.Z_CONTROLS)

		screen.updateMinimapSection(False, False)

		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

	def initPlotView(self):
		self.plotview = self.getNextWidgetName()
		#TODO maybe init with view of capital

	def unitDescription(self, unit):
			strengthText = u""
			if (unit.getDomainType() == DomainTypes.DOMAIN_AIR):
				if (unit.airBaseCombatStr() > 0):
					if (unit.isHurt()):
						strengthText = u"%.1f/%d%c" %(((float(unit.airBaseCombatStr() * unit.currHitPoints())) / (float(unit.maxHitPoints()))), unit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						strengthText = u"%d%c" %(unit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
			else:
				if (unit.canFight()):
					if (unit.isHurt()):
						strengthText = u"%.1f/%d%c" %(((float(unit.baseCombatStr() * unit.currHitPoints())) / (float(unit.maxHitPoints()))), unit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						strengthText = u"%d%c" %(unit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
			movesText = u""
			if ( (unit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
				iDenom = 1
			else:
				iDenom = 0
			iCurrMoves = ((unit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
			if (unit.baseMoves() == iCurrMoves):
				movesText = u"%d%c" %(unit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
			else:
				movesText = u"%d/%d%c" %(iCurrMoves, unit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
			szUnitName = unit.getNameNoDesc()
			if (szUnitName == ""):
				szUnitName = gc.getUnitInfo(unit.getUnitType()).getDescription()

			return u"<font=3>" + szUnitName + u": " + strengthText + u" " + movesText + u"</font>"

	def checkBoxName(self, idx):
		return self.unitCheckBox + str(idx)

	def addGroupPanel(self, label, groupIndex):
		screen = self.getScreen()
		screen.attachPanel( self.unitBackgroundName, self.unitGroupName + str(groupIndex), "", "", True, False, PanelStyles.PANEL_STYLE_DAWNTOP )
		screen.attachLabel(self.unitGroupName + str(groupIndex), self.unitGroupName + "%dfill1"%(groupIndex), "<font=4> </font>")
		screen.attachLabel(self.unitGroupName + str(groupIndex), self.unitGroupName + "%dfill2"%(groupIndex), "<font=3> </font>")
		screen.setLabelAt( self.unitGroupName + "%dLabel"%(groupIndex), self.unitGroupName + str(groupIndex)
						 , u"<font=4>%s</font>"%(label), CvUtil.FONT_CENTER_JUSTIFY
						 , (305 - 17) / 2, 8, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def addUnitToList(self, unit, idx):
		screen = self.getScreen()
		screen.attachPanel(self.unitBackgroundName, self.unitPanelName + str(idx), "", "", False, False, PanelStyles.PANEL_STYLE_OUT)
		screen.attachLabel(self.unitPanelName + str(idx), self.unitPanelName + "%ddummy"%(idx), "            " )
		screen.addCheckBoxGFCAt(self.unitPanelName + str(idx), self.checkBoxName(idx)
							   , gc.getUnitInfo(unit.getUnitType()).getButton()
							   , ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()
							   , 1, 2, 46, 46, WidgetTypes.WIDGET_GENERAL, idx, idx, ButtonStyles.BUTTON_STYLE_LABEL, False)
		# Leader
		if (unit.isHasPromotion(self.iPromoLeader)): # has Leader promotion
			screen.addDDSGFCAt(self.unitPanelName + str(idx) + "leader", self.unitPanelName + str(idx), gc.getPromotionInfo(self.iPromoLeader).getButton()
							   , 32, 30, 20, 20, WidgetTypes.WIDGET_GENERAL, idx, -1, False)

		if ((unit.getOwner(), unit.getID()) in self.selectedUnits):
			screen.setState(self.checkBoxName(idx), True)

		szLevel = "Lv.: %d"%(unit.getLevel())
		if (unit.getLevel() > 3):
			szLevel = "<color=255,255,0,255>%s</color>"%(szLevel)
		szExp = "XP:<font=4> </font>%d/%d"%(unit.getExperience(), unit.experienceNeeded())
		if (unit.getExperience() >= unit.experienceNeeded()):
			szExp = "<color=255,255,0,255>%s</color>"%(szExp)
		szText = "%s\n%s, %s"%(self.unitDescription(unit), szLevel, szExp)
		szPromotion = u"<font=3>"
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			if (unit.isHasPromotion(iPromotion) and iPromotion != self.iPromoLeader):
				szPromotion += " <img=%s size=20></img>"%(gc.getPromotionInfo(iPromotion).getButton())
		szPromotion += "</font>"
		screen.attachMultilineText(self.unitPanelName + str(idx), self.unitPanelName + "%dinfo"%(idx), "%s %s"%(szText, szPromotion), WidgetTypes.WIDGET_GENERAL, idx, idx, CvUtil.FONT_LEFT_JUSTIFY)

	def addUnitsToList(self):

		screen = self.getScreen()
		screen.hide(self.unitBackgroundName)

		szHilite = ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()

		for idx in xrange(len(self.unitList)):
			unit = self.unitList[idx]
			szPanelName = self.unitPanelName + str(idx)
			screen.attachPanel(self.unitBackgroundName, szPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_OUT)
			screen.attachLabel(szPanelName, szPanelName + "dummy", "            " )
			screen.addCheckBoxGFCAt(szPanelName, self.checkBoxName(idx), gc.getUnitInfo(unit.getUnitType()).getButton()
								   , szHilite, 1, 2, 46, 46, WidgetTypes.WIDGET_GENERAL, idx, idx, ButtonStyles.BUTTON_STYLE_LABEL, False)
			# Leader
			if (unit.isHasPromotion(self.iPromoLeader)): # has Leader promotion
				screen.addDDSGFCAt(szPanelName + "leader", szPanelName, gc.getPromotionInfo(self.iPromoLeader).getButton(), 32, 30, 20, 20, WidgetTypes.WIDGET_GENERAL, idx, -1, False)

			if ((unit.getOwner(), unit.getID()) in self.selectedUnits):
				screen.setState(self.checkBoxName(idx), True)

			szLevel = "Lv.: " + str(unit.getLevel())
			if (unit.getLevel() > 3):
				szLevel = "<color=255,255,0,255>%s</color>"%(szLevel)
			szExp = "XP:<font=4> </font>%d/%d"%(unit.getExperience(), unit.experienceNeeded())
			if (unit.getExperience() >= unit.experienceNeeded()):
				szExp = "<color=255,255,0,255>%s</color>"%(szExp)
			szText = self.unitDescription(unit) + "\n" + szLevel + ", " + szExp
			szPromotion = u"<font=3>"
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if (unit.isHasPromotion(iPromotion) and iPromotion != self.iPromoLeader):
					szPromotion += " <img=" + gc.getPromotionInfo(iPromotion).getButton() + " size=20></img>"
			szPromotion += "</font>"
			screen.attachMultilineText(szPanelName, szPanelName + "info", szText + " " + szPromotion, WidgetTypes.WIDGET_GENERAL, idx, idx, CvUtil.FONT_LEFT_JUSTIFY)

		screen.show(self.unitBackgroundName)

	def AutoReconUnitsList(self):
		screen = self.getScreen()
		screen.hide(self.unitBackgroundName)

		szHilite = ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()

		for idx in xrange(len(self.unitList)):
			szPanelName = self.unitPanelName + str(idx)
			screen.deleteWidget(szPanelName)
			screen.deleteWidget(szPanelName + "dummy")
			screen.deleteWidget(self.checkBoxName(idx))
			screen.deleteWidget(szPanelName + "leader")
			screen.deleteWidget(szPanelName + "info")

		for idx in xrange(len(self.AutoReconList)):
			unit = self.AutoReconList[idx]
			szPanelName = self.unitPanelName + str(idx)
			screen.attachPanel(self.unitBackgroundName, szPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_OUT)
			screen.attachLabel(szPanelName, szPanelName + "dummy", "            " )
			screen.addCheckBoxGFCAt(szPanelName, self.checkBoxName(idx), gc.getUnitInfo(unit.getUnitType()).getButton()
								   , szHilite, 1, 2, 46, 46, WidgetTypes.WIDGET_GENERAL, idx, idx, ButtonStyles.BUTTON_STYLE_LABEL, False)
			# Leader
			if (unit.isHasPromotion(self.iPromoLeader)): # has Leader promotion
				screen.addDDSGFCAt(szPanelName + "leader", szPanelName, gc.getPromotionInfo(self.iPromoLeader).getButton(), 32, 30, 20, 20, WidgetTypes.WIDGET_GENERAL, idx, -1, False)

			if ((unit.getOwner(), unit.getID()) in self.selectedUnits):
				screen.setState(self.checkBoxName(idx), True)

			szLevel = "Lv.: " + str(unit.getLevel())
			if (unit.getLevel() > 3):
				szLevel = "<color=255,255,0,255>%s</color>"%(szLevel)
			szExp = "XP:<font=4> </font>%d/%d"%(unit.getExperience(), unit.experienceNeeded())
			if (unit.getExperience() >= unit.experienceNeeded()):
				szExp = "<color=255,255,0,255>%s</color>"%(szExp)
			szText = self.unitDescription(unit) + "\n" + szLevel + ", " + szExp
			szPromotion = u"<font=3>"
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if (unit.isHasPromotion(iPromotion) and iPromotion != self.iPromoLeader):
					szPromotion += " <img=" + gc.getPromotionInfo(iPromotion).getButton() + " size=20></img>"
			szPromotion += "</font>"
			screen.attachMultilineText(szPanelName, szPanelName + "info", szText + " " + szPromotion, WidgetTypes.WIDGET_GENERAL, idx, idx, CvUtil.FONT_LEFT_JUSTIFY)

		screen.show(self.unitBackgroundName)

	def toggleUnitCheckBox(self, unitIndex):
		screen = self.getScreen()
		if (len(self.AutoReconList) > 0):
			unit = self.AutoReconList[unitIndex]
		else:
			unit = self.unitList[unitIndex]

		if ( screen.getCheckBoxState(self.checkBoxName(unitIndex)) ):
			self.selectedUnits.append((unit.getOwner(), unit.getID()))
		else:
			self.selectedUnits.remove((unit.getOwner(), unit.getID()))

		self.refreshMinimap()

	def groupSelectionChanged(self, groupId):
		screen = self.getScreen()
		for groupIndex in xrange(self.numGroups):
			screen.deleteWidget(self.unitGroupName + str(groupIndex))

		screen.hide(self.unitBackgroundName)

		if (groupId == self.NO_GROUPS_ID):
			self.addUnitsToList()
			self.AutoReconList = []
		elif (groupId == self.AUTO_RECON_ID):
			if (gc.getGame().getActivePlayer() in self.selectedPlayerList):
				self.AutoReconList = CGEUtils.CGEUtils().getAutoReconUnitsList()
			else:
				self.AutoReconList = []
			self.AutoReconUnitsList()
		else:
			self.createGroup(groupId)
			self.AutoReconList = []

		screen.show(self.unitBackgroundName)
		self.refreshMinimap()

	def createGroup(self, groupID):
		screen = self.getScreen()

		self.groups = {}
		if (groupID == self.STACK_GROUP_ID):
			groupHelper = StackGroupHelper()
		elif (groupID == self.COMBAT_TYPE_GROUP_ID):
			groupHelper = CombatTypeGroupHelper()
		elif (groupID == self.LOCATION_GROUP_ID):
			groupHelper = LocationGroupHelper()

		for idx in xrange(len(self.unitList)):
			groupId = groupHelper.getGroupId(self.unitList[idx])
			if (self.groups.has_key(groupId)):
				self.groups[groupId].addUnit(idx)
			else:
				self.groups[groupId] = UnitGroup()
				self.groups[groupId].addUnit(idx)

		keys = self.groups.keys()
		if (groupID == self.STACK_GROUP_ID):
			keys.sort(groupHelper.compareGroups)
		else:
			keys.sort()

		groupIndex = 0
		AddUnitToList = self.addUnitToList
		AddGroupPanel = self.addGroupPanel
		screen.hide(self.unitBackgroundName)
		for groupId in keys:
			AddGroupPanel(groupHelper.getGroupLabel(groupId), groupIndex)
			groupIndex += 1
			units = self.groups[groupId].units
			for idx in units:
				AddUnitToList(self.unitList[idx], idx)
		screen.show(self.unitBackgroundName)

		self.numGroups = groupIndex

	def refreshMinimap(self):
		screen = self.getScreen()
		screen.minimapClearAllFlashingTiles()

		self.showEnemyMinimap()
		iColor = gc.getInfoTypeForString("COLOR_GREEN")
		iColorWar = gc.getInfoTypeForString("COLOR_YELLOW")
		ActiveTeam = gc.getGame().getActiveTeam()
		for (iOwner, iUnitID) in self.selectedUnits:
			unit = gc.getPlayer(iOwner).getUnit(iUnitID)
			if (gc.getTeam(ActiveTeam).isAtWar(gc.getPlayer(unit.getOwner()).getTeam())):
				screen.minimapFlashPlot(unit.getX(), unit.getY(), iColorWar, -1)
			else:
				screen.minimapFlashPlot(unit.getX(), unit.getY(), iColor, -1)
		if (len(self.AutoReconList) > 0):
			for (iOwner, iUnitID) in self.selectedUnits:
				unit = gc.getPlayer(iOwner).getUnit(iUnitID)
				lTarget = CGEUtils.CGEUtils().getTargetPlot(unit.getID())
				if (lTarget != None):
					screen.minimapFlashPlot(lTarget[0], lTarget[1], gc.getInfoTypeForString("COLOR_BLUE"), -1)

	def showEnemyMinimap(self):
		# Radar Button
		if (self.RadarState):
			screen = self.getScreen()
			iColorEnemy = gc.getInfoTypeForString("COLOR_RED")
			for unit in self.enemyUnitList:
				screen.minimapFlashPlot(unit[0], unit[1], iColorEnemy, -1)

	def updatePlotView(self, x, y):
		screen = self.getScreen()
		screen.addPlotGraphicGFC( self.plotview, self.viewX + self.viewMargin, self.viewY + self.viewMargin
								, self.viewWidth - self.viewMargin * 2, self.viewHeight - self.viewMargin * 2
								, CyMap().plot(x, y), 800, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )

##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def update(self, fDelta):
		screen = self.getScreen()
		screen.updateMinimap(fDelta)

	def minimapClicked(self):
		self.hideScreen()

	def refresh(self, bReload):
		if (self.iActivePlayer < 0):
			return

		screen = self.getScreen()

		listLeaders = []
		listLeadersappend = listLeaders.append
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
				listLeadersappend(iLoopPlayer)

		iNumLeaders = len(listLeaders)
		if iNumLeaders >= self.LEADER_COLUMNS:
			iButtonSize = self.LEADER_BUTTON_SIZE / 2
		else:
			iButtonSize = self.LEADER_BUTTON_SIZE

		iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))

		# loop through all players and display leaderheads
		eActivePlayer = gc.getGame().getActivePlayer()
		ActiveCanEspMission = gc.getPlayer(eActivePlayer).canDoEspionageMission
		iSeeDemoMission = -1
		for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
				iSeeDemoMission = iMissionLoop

		for iIndex in xrange(iNumLeaders):
			iLoopPlayer = listLeaders[iIndex]
			player = gc.getPlayer(iLoopPlayer)

			x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
			y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)

			if (bReload):
				if player.isBarbarian():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(player.getLeaderType()).getButton()
				screen.addCheckBoxGFC(self.getLeaderButton(iLoopPlayer), szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(self.getLeaderButton(iLoopPlayer), (iLoopPlayer in self.selectedPlayerList))

				if (iLoopPlayer == eActivePlayer):
					szPower = str(player.getPower())
				elif (player.isBarbarian()):
					szPower = ""
				else:
					if (ActiveCanEspMission(0, iLoopPlayer, None, -1)):
						if (gc.getTeam(gc.getPlayer(eActivePlayer).getTeam()).getDefensivePower() < (player.getPower() * gc.getLeaderHeadInfo(iLoopPlayer).getMaxWarDistantPowerRatio() / 100)):
							szPower = u"<color=%d,%d,%d,%d>%d</color>" %(255, 0, 0, 255, player.getPower())
						elif (gc.getTeam(gc.getPlayer(eActivePlayer).getTeam()).getDefensivePower() < (player.getPower() * gc.getLeaderHeadInfo(iLoopPlayer).getMaxWarNearbyPowerRatio() / 100)):
							szPower = u"<color=%d,%d,%d,%d>%d</color>" %(255, 255, 0, 255, player.getPower())
						else:
							szPower = u"%d" %(player.getPower())
					else:
						szPower = ""
				screen.addMultilineText("%spower"%(self.getLeaderButton(iLoopPlayer)), szPower, x, y + iButtonSize, iButtonSize, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		screen.minimapClearAllFlashingTiles()
		self.showEnemyMinimap()
		screen.addPanel(self.unitBackgroundName, "", "", True, True, 0, 48, 305, self.H_SCREEN - 48, PanelStyles.PANEL_STYLE_CITY_LEFT)

		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			if (iLoopPlayer in self.selectedPlayerList):
				tempunitList = []
				tempunitListappend = tempunitList.append
				player = gc.getPlayer(iLoopPlayer)
				(loopUnit, iter) = player.firstUnit(False)
				while (loopUnit):
					if (iLoopPlayer == loopUnit.getOwner()):
						bVisible = False
						plot = loopUnit.plot()

						if (not plot.isNone()):
							bVisible = plot.isVisible(iActiveTeam, False) and not loopUnit.isInvisible(iActiveTeam, False)

						if (bVisible):
							tempunitListappend((-loopUnit.getUnitType(), -loopUnit.getLevel(), -loopUnit.getExperience(), loopUnit))
					(loopUnit, iter) = player.nextUnit(iter, false)

				self.selectedUnits = []
				tempunitList.sort()
				self.unitList = [unit for (_, _, _, unit) in tempunitList]
				self.groupSelectionChanged(screen.getSelectedPullDownID(self.groupSelectionName))

	def isSelectedGroup(self, iGroup, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if iGroup == -1:
				return False
		return ((iGroup + gc.getNumUnitInfos()) in self.selectedGroupList)

	def isSelectedUnitType(self, iUnit, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if self.isSelectedGroup(gc.getUnitInfo(iUnit).getUnitCombatType(), True):
				return True
		return (iUnit in self.selectedGroupList)

	def isSelectedUnit(self, iPlayer, iUnitId, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			unit = gc.getPlayer(iPlayer).getUnit(iUnitId)
			if self.isSelectedGroup(gc.getUnitInfo(unit.getUnitType()).getUnitCombatType(), True):
				return True
			if self.isSelectedUnitType(unit.getUnitType(), True):
				return True
		return ((iPlayer, iUnitId) in self.selectedUnitList)

	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedPlayerList):
				self.selectedPlayerList.remove(iPlayer)
			else:
				self.selectedPlayerList.append(iPlayer)
		else:
			self.selectedPlayerList = []
			self.selectedPlayerList.append(iPlayer)

		self.refresh(True)

	def getLeaderButton(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName

	def refreshSelectedGroup(self, iSelected):
		if (iSelected in self.selectedGroupList):
			self.selectedGroupList.remove(iSelected)
		else:
			self.selectedGroupList.append(iSelected)
		self.refreshUnitSelection(False)

	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnitList):
			self.selectedUnitList.remove(selectedUnit)
		else:
			self.selectedUnitList.append(selectedUnit)
		self.refreshUnitSelection(False)

	def drawCombatExperience(self):

		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):
			iExperience = gc.getPlayer(self.iActivePlayer).getCombatExperience()

			screen = self.getScreen()
			screen.addStackedBarGFC(self.GREAT_GENERAL_BAR_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))
			screen.setLabel(self.GREAT_GENERAL_LABEL_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 8, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)

	def getEnemyUnitList(self):
		ActiveTeam = gc.getTeam(gc.getGame().getActiveTeam())
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()
		self.enemyUnitList = set()
		enemyUnitListadd = self.enemyUnitList.add
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(iActiveTeam) or gc.getGame().isDebugMode())):
				if (ActiveTeam.isAtWar(gc.getPlayer(iLoopPlayer).getTeam()) or player.isBarbarian()):
					(loopUnit, iter) = player.firstUnit(False)
					while (loopUnit):
						if (iLoopPlayer == loopUnit.getOwner() and not loopUnit.isInvisible(iActiveTeam, False)):
							plot = loopUnit.plot()
							if (not plot.isNone()):
								if (plot.isVisible(iActiveTeam, False)):
									enemyUnitListadd((loopUnit.getX(), loopUnit.getY()))
						(loopUnit, iter) = player.nextUnit(iter, false)


		if (self.RadarState):
			self.RadarState = False
		else:
			self.RadarState = True

		self.refreshMinimap()

	def handleInput (self, inputClass):
		screen = self.getScreen()
		if (inputClass.getFunctionName() == self.RADAR_BUTTON and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED
															  and inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP ): # radar
			self.getEnemyUnitList()
		if (inputClass.getFunctionName() == self.unitCheckBox and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED): # unit selected
			if (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
				self.toggleUnitCheckBox(inputClass.getData1())
			elif (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
				iIndex = inputClass.getData1()
				iRefUnitType = self.unitList[iIndex].getUnitType()
				bState =  not screen.getCheckBoxState(self.checkBoxName(iIndex))
				for iLoop in xrange(len(self.unitList)):
					pLoopUnit = self.unitList[iLoop]
					if (pLoopUnit.getUnitType() == iRefUnitType):
						tLoopUnit = (pLoopUnit.getOwner(), pLoopUnit.getID())
						if (bState):
							if (tLoopUnit not in self.selectedUnits):
								self.selectedUnits.append(tLoopUnit)
						else:
							if (tLoopUnit in self.selectedUnits):
								self.selectedUnits.remove(tLoopUnit)
						screen.setState(self.checkBoxName(iLoop), bState)
				self.refreshMinimap()
		if ( inputClass.getFunctionName() == self.groupSelectionName and 
			 inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ): # group changed
			iIndex = screen.getSelectedPullDownID(self.groupSelectionName)
			self.groupSelectionChanged(iIndex)
		if (inputClass.getFunctionName() == self.AUTO_ORDER_CHECKBOX and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			CGEUtils.CGEUtils().setAutoOrder(screen.getCheckBoxState(self.AUTO_ORDER_CHECKBOX))
		return 0
