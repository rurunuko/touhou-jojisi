## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import math
import CvEventInterface

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################
import IconGrid
#from IconGrid import IconGrid
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

import CvForeignAdvisor
import TechTree
import re

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# Debugging help
def ExoticForPrint (stuff):
	stuff = "ExoForAdv: " + stuff
	CvUtil.pyPrint (stuff)

# this class is shared by both the resource and technology foreign advisors
class CvExoticForeignAdvisor (CvForeignAdvisor.CvForeignAdvisor):
	"Exotic Foreign Advisor Screen"

	def __init__(self):
		CvForeignAdvisor.CvForeignAdvisor.__init__ (self)

		self.GLANCE_HEADER = "ForeignAdvisorGlanceHeader"
		self.GLANCE_BUTTON = "ForeignAdvisorPlusMinus"
		self.X_LINK = 85
		self.Y_LINK = 726

		self.X_GLANCE_OFFSET = 10
		self.Y_GLANCE_OFFSET = 5
		self.GLANCE_BUTTON_SIZE = 48
		self.PLUS_MINUS_SIZE = 24
		self.bGlancePlus = True

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

		###################
		# General options #
		###################

		# Show the names of the leaders if 'True'
		self.SHOW_LEADER_NAMES = False

		# Show a border around the rows
		self.SHOW_ROW_BORDERS = True

		# Minimum space at the top and bottom of the screen.
		self.MIN_TOP_BOTTOM_SPACE = 60

		# Minimum space at the left and right end of the screen.
		self.MIN_LEFT_RIGHT_SPACE = 25

		# Extra border at the left and right ends of the column groups (import/export)
		self.GROUP_BORDER = 8

		# Extra space before the label of the column groups (import/export)
		self.GROUP_LABEL_OFFSET = "   "

		# Minimum space between the columns
		self.MIN_COLUMN_SPACE = 5

		# Minimum space between the rows
		self.MIN_ROW_SPACE = 1

		##########################
		# Resources view options #
		##########################

		# If 'True', the amount for each surplus resource is subtracted by one. So it shows how many you
		# can give away without losing the resource yourself. This value isn't affected by any default 
		# layout.
		self.RES_SHOW_EXTRA_AMOUNT = True

		# If 'True', the amount's are shown as an overlay on top of the lower left corner of the resources.
		# If 'False', the amount's are shown below the resources so you'll need to use a higher value for 
		# self.RES_SURPLUS_HEIGHT (see below).
		self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP = True

		# If 'True', the resource columns are grouped as import and export.
		self.RES_SHOW_IMPORT_EXPORT_HEADER = True

		# If 'True', two extra columns are used to display resources that are traded in active deals.
		self.RES_SHOW_ACTIVE_TRADE = True

		# Height of the panel showing the surplus resources. If self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP is 'False'
		# you'll need to set a higher value for this variable (110 is recommended).
		self.RES_SURPLUS_HEIGHT = 80

		self.RES_GOLD_COL_WIDTH = 25

		# Space between the two panels.
		self.RES_PANEL_SPACE = 0

		#############################
		# Technologies view options #
		#############################

		# If 'True', use icon size 32x32
		# If 'False', use icon size 64x64
		self.TECH_USE_SMALL_ICONS = True
		self.TECH_GOLD_COL_WITH = 60

		###############
		# End options #
		###############

		self.TITLE_HEIGHT = 24
 		self.TABLE_CONTROL_HEIGHT = 24
		self.RESOURCE_ICON_SIZE = 34
		self.SCROLL_TABLE_UP = 1
		self.SCROLL_TABLE_DOWN = 2
		self.SCROLL_GRANCE_UP = 3
		self.SCROLL_GRANCE_DOWN = 4

##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

		self.SCREEN_DICT = {
			"BONUS": 0,
			"TECH": 1,
			"RELATIONS": 2,
			"ACTIVE_TRADE": 3,
			"INFO": 4,
			"GLANCE": 5,
			"DIPLOMACY": 6,
			}

		self.REV_SCREEN_DICT = {}

		for key, value in self.SCREEN_DICT.items():
			self.REV_SCREEN_DICT[value] = key

		self.DRAW_DICT = {
			"BONUS": self.drawResourceDeals,
			"TECH": self.drawTechDeals,
			"RELATIONS": self.drawRelations,
			"ACTIVE_TRADE": self.drawActive,
			"INFO": self.drawInfo,
			"GLANCE": self.drawGlance,
			"DIPLOMACY": self.drawDiplomacy,
			}

		self.TXT_KEY_DICT = {
			"BONUS": "TXT_KEY_FOREIGN_ADVISOR_RESOURCES",
			"TECH": "TXT_KEY_FOREIGN_ADVISOR_TECHS",
			"RELATIONS": "TXT_KEY_FOREIGN_ADVISOR_RELATIONS",
			"ACTIVE_TRADE": "TXT_KEY_FOREIGN_ADVISOR_ACTIVE",
			"INFO": "TXT_KEY_FOREIGN_ADVISOR_INFO",
			"GLANCE": "TXT_KEY_FOREIGN_ADVISOR_GLANCE",
			"DIPLOMACY": "TXT_KEY_FOREIGN_ADVISOR_DIPLOMACY",
			}

		self.ORDER_LIST = ["RELATIONS", \
							"GLANCE", \
							"ACTIVE_TRADE", \
							"BONUS", \
							"INFO", \
							"TECH", \
							"DIPLOMACY"]

		self.iDefaultScreen = self.SCREEN_DICT["RELATIONS"]

		self.AttitudeFontMap = {
			AttitudeTypes.ATTITUDE_FURIOUS	: "<img=Art/Interface/Buttons/AttFonts/AttFont0%s.dds></img>",
			AttitudeTypes.ATTITUDE_ANNOYED	: "<img=Art/Interface/Buttons/AttFonts/AttFont1%s.dds></img>",
			AttitudeTypes.ATTITUDE_CAUTIOUS	: "<img=Art/Interface/Buttons/AttFonts/AttFont2%s.dds></img>",
			AttitudeTypes.ATTITUDE_PLEASED	: "<img=Art/Interface/Buttons/AttFonts/AttFont3%s.dds></img>",
			AttitudeTypes.ATTITUDE_FRIENDLY	: "<img=Art/Interface/Buttons/AttFonts/AttFont4%s.dds></img>",
		}

	def interfaceScreen (self, iScreen):

		self.ATTITUDE_DICT = {
			"COLOR_GREEN": re.sub(":", "|", localText.getText ("TXT_KEY_ATTITUDE_FRIENDLY", ())),
			"COLOR_CYAN" : re.sub(":", "|", localText.getText ("TXT_KEY_ATTITUDE_PLEASED", ())),
			"COLOR_MAGENTA" : re.sub(":", "|", localText.getText ("TXT_KEY_ATTITUDE_ANNOYED", ())),
			"COLOR_RED" : re.sub(":", "|", localText.getText ("TXT_KEY_ATTITUDE_FURIOUS", ())),
			}

		self.objTechTree = TechTree.TechTree()

		if (iScreen < 0):
			if (self.iScreen < 0):
				iScreen = self.iDefaultScreen
			else:
				iScreen = self.iScreen

		self.EXIT_TEXT = u"<font=4>%s</font>"%(localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper())
		self.SCREEN_TITLE = u"<font=4b>%s</font>"%(localText.getText("TXT_KEY_FOREIGN_ADVISOR_TITLE", ()).upper())

		if (self.iScreen != iScreen):
			self.killScreen()
			self.iScreen = iScreen

		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActiveLeader = CyGame().getActivePlayer()
		self.iSelectedLeader = self.iActiveLeader
		self.listSelectedLeaders = []
		#self.listSelectedLeaders.append(self.iSelectedLeader)

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()
		self.X_EXIT = self.W_SCREEN - 30
		self.DX_LINK = (self.X_EXIT - self.X_LINK) / len (self.SCREEN_DICT)

		self.Y_EXIT = self.H_SCREEN - 42
		self.Y_LINK = self.H_SCREEN - 42
		self.Y_BOTTOM_PANEL = self.H_SCREEN - 55

		#Adjust Screen Size
		self.X_LEADER_CIRCLE_TOP = self.W_SCREEN / 2
		if (self.W_SCREEN == 1280 and self.H_SCREEN == 1024):
			self.RADIUS_LEADER_ARC = self.H_SCREEN * 0.55
		else:
			self.RADIUS_LEADER_ARC = self.H_SCREEN * 0.65
		self.Y_LEGEND = self.H_SCREEN - 240

		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		screen.addDrawControl(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "BottomPanel", u"", u"", True, False, 0, self.Y_BOTTOM_PANEL, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################

		# Set the background and exit button, and show the screen
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		self.nWidgetCount = 0
		self.nLineCount = 0
		
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		CyInterface().setDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT, False)

		# Draw leader heads
		self.drawContents(True)

	# Drawing Leaderheads
	def drawContents(self, bInitial):

		if (self.iScreen < 0):
			return

		self.deleteAllWidgets()

		screen = self.getScreen()

		# Header...
		screen.setLabel(self.getNextWidgetName(), "", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
	
		if (self.REV_SCREEN_DICT.has_key(self.iScreen)):
			self.DRAW_DICT[self.REV_SCREEN_DICT[self.iScreen]] (bInitial)
		else:
			return

		# Link to other Foreign advisor screens
		xLink = self.X_LINK

		for i in xrange(len(self.ORDER_LIST)):
			szTextId = self.getNextWidgetName()
			szScreen = self.ORDER_LIST[i]
			if (self.iScreen != self.SCREEN_DICT[szScreen]):
				screen.setText (szTextId, "", u"<font=4>%s</font>"%(localText.getText (self.TXT_KEY_DICT[szScreen], ()).upper()), CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, self.SCREEN_DICT[szScreen], -1)
			else:
				screen.setText (szTextId, "", u"<font=4>%s</font>"%(localText.getColorText (self.TXT_KEY_DICT[szScreen], (), gc.getInfoTypeForString ("COLOR_YELLOW")).upper()), CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
			xLink += self.DX_LINK
	
	def drawActive (self, bInitial):
		CvForeignAdvisor.CvForeignAdvisor.drawActive (self)

	def drawInfo (self, bInitial):
#		ExoticForPrint ("Entered drawInfo")

		screen = self.getScreen()

		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)
		self.initInfoTable()

		# Put everything inside a main panel, so we get vertical scrolling
		mainPanelName = self.getNextWidgetName()
		gridX = self.MIN_LEFT_RIGHT_SPACE
		gridY = self.MIN_TOP_BOTTOM_SPACE
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2
		screen.addPanel(mainPanelName, "", "", True, True, gridX, gridY, gridWidth, gridHeight, PanelStyles.PANEL_STYLE_MAIN)

		self.InfoIconGrid.createGrid()
		self.InfoIconGrid.clearData()

		ltCivicOptions = range (gc.getNumCivicOptionInfos())
		currentRow = 0

		# loop through all players and display leaderheads
		# Their leaderheads
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive() and iLoopPlayer != self.iActiveLeader and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(playerActive.getTeam()) or gc.getGame().isDebugMode()) and not pLoopPlayer.isBarbarian() and not pLoopPlayer.isMinorCiv()):

				nPlayerReligion = pLoopPlayer.getStateReligion()
				objReligion = gc.getReligionInfo(nPlayerReligion)

				objLeaderHead = gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType())

				# Player panel
				self.InfoIconGrid.appendRow(pLoopPlayer.getName(), "")
				self.InfoIconGrid.addIcon(currentRow, 0, gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				# religion
				szPlayerReligion = ""
				if (nPlayerReligion != -1): # -1 == NO_RELIGON
					if (pLoopPlayer.hasHolyCity(nPlayerReligion)):
						szPlayerReligion = u"%c" %(objReligion.getHolyCityChar())
					elif objReligion:
						szPlayerReligion = u"%c" %(objReligion.getChar())

				self.InfoIconGrid.setText(currentRow, 1, szPlayerReligion)

				self.InfoIconGrid.setText(currentRow, 2, localText.getText("TXT_KEY_FOREIGN_ADVISOR_TRADE", (self.calculateTrade(self.iActiveLeader, iLoopPlayer), 0)))

				for nCivicOption in ltCivicOptions:
					nCivic = pLoopPlayer.getCivics(nCivicOption)
					self.InfoIconGrid.addIcon(currentRow, 3, gc.getCivicInfo(nCivic).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, nCivic)

				nFavoriteCivic = objLeaderHead.getFavoriteCivic()
				if (nFavoriteCivic != -1) and (not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RANDOM_PERSONALITIES)):
					self.InfoIconGrid.addIcon(currentRow, 5, gc.getCivicInfo(nFavoriteCivic).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, nFavoriteCivic)
					self.InfoIconGrid.setText(currentRow, 4, gc.getCivicOptionInfo(gc.getCivicInfo(nFavoriteCivic).getCivicOptionType()).getDescription())

				currentRow += 1
		self.InfoIconGrid.refresh()

	def initInfoTable(self):
		screen = self.getScreen()

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + 10
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - 20

		columns = (IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_TEXT_COLUMN, IconGrid.GRID_TEXT_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN, IconGrid.GRID_ICON_COLUMN)
		self.InfoIconGridName = self.getNextWidgetName()
		self.InfoIconGrid = IconGrid.IconGrid(self.InfoIconGridName, screen, gridX, gridY, gridWidth, gridHeight, columns, False, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)

		self.InfoIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.InfoIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.InfoIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.InfoIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		self.InfoIconGrid.setHeader(0, localText.getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()))
		self.InfoIconGrid.setHeader(1, localText.getText("TXT_KEY_FOREIGN_ADVISOR_STATE_RELIGION", ()))
		self.InfoIconGrid.setHeader(2, localText.getText("TXT_KEY_CONCEPT_TRADE", ()))
		self.InfoIconGrid.setHeader(3, localText.getText("TXT_KEY_CIVICS_SCREEN_TITLE", ()))
		self.InfoIconGrid.setHeader(4, localText.getText("TXT_KEY_PEDIA_FAV_CIVIC", ()))
		self.InfoIconGrid.setTextColWidth(1, 60)
		self.InfoIconGrid.setTextColWidth(2, 90)
		self.InfoIconGrid.setTextColWidth(4, 130)

		gridWidth = self.InfoIconGrid.getPrefferedWidth()
		gridHeight = self.InfoIconGrid.getPrefferedHeight()
		self.INFO_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.INFO_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.INFO_LEFT_RIGHT_SPACE + 10
		gridY = self.INFO_TOP_BOTTOM_SPACE + 10

		self.InfoIconGrid.setPosition(gridX, gridY)
		self.InfoIconGrid.setSize(gridWidth, gridHeight)

	def calculateTrade (self, nPlayer, nTradePartner):
		# Trade status...
		nTotalTradeProfit = 0

		pPlayer = gc.getPlayer(nPlayer)

		# Loop through the cities
		for iLoopCity in xrange(pPlayer.getNumCities()):
			pLoopCity = pPlayer.getCity(iLoopCity)

			# For each trade route possible
			for nTradeRoute in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
				# Get the next trade city
				pTradeCity = pLoopCity.getTradeCity(nTradeRoute)
				# Not quite sure what this does but it's in the MainInterface
				# and I pretty much C&Ped :p
				if (pTradeCity and pTradeCity.getOwner() >= 0):
					for j in xrange(YieldTypes.NUM_YIELD_TYPES ):
						nTradeProfit = pLoopCity.calculateTradeYield(j, pLoopCity.calculateTradeProfit(pTradeCity))

						# If the TradeProfit is greater than 0 and it to the total
						if ( nTradeProfit > 0 and pTradeCity.getOwner() == nTradePartner):
							nTotalTradeProfit += nTradeProfit

		return nTotalTradeProfit

	def drawGlance(self, bInitial):
#		ExoticForPrint ("Entered drawGlance")

		screen = self.getScreen()

		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)

		# loop through all players and display leaderheads
		# Their leaderheads
		if (bInitial):
			self.nRowOffset = 0
			self.nCount = 0
			self.ltPlayerRelations = [[0] * gc.getMAX_PLAYERS() for i in range (gc.getMAX_PLAYERS())]
			self.ltPlayerMet = [False] * gc.getMAX_PLAYERS()

			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(iLoopPlayer).isAlive() and (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()) and not gc.getPlayer(iLoopPlayer).isBarbarian() and not gc.getPlayer(iLoopPlayer).isMinorCiv()):

#					ExoticForPrint ("Player = %d" % iLoopPlayer)
					self.ltPlayerMet [iLoopPlayer] = True

					for nHost in xrange(gc.getMAX_PLAYERS()):
						if (gc.getPlayer(nHost).isAlive() and nHost != self.iActiveLeader and (gc.getTeam(gc.getPlayer(nHost).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()) and not gc.getPlayer(nHost).isBarbarian() and not gc.getPlayer(nHost).isMinorCiv()):
							nRelation = self.calculateRelations (nHost, iLoopPlayer)
							self.ltPlayerRelations [iLoopPlayer][nHost] = nRelation

					# Player panel
					self.nCount += 1

			self.nSpread = 64
			self.hSpread = 48

			self.iMaxCol = (self.W_SCREEN - 40 - self.nSpread)/self.nSpread
			self.iMaxRow = (self.H_SCREEN - 200)/(self.hSpread + 6)

		BackgroundPanel = self.getNextWidgetName()
		MatrixPanel = self.getNextWidgetName()
		MainPanel = self.getNextWidgetName()

		screen.addPanel(BackgroundPanel, "", "", False, False, 10, 55, self.W_SCREEN - 20, self.H_SCREEN - 110, PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(self.GLANCE_HEADER, "", "", False, False, 20, 65, self.W_SCREEN - 40, 60, PanelStyles.PANEL_STYLE_OUT)

		self.iAjustedHeight = self.iMaxRow * (self.hSpread + 6) + 6
		screen.addPanel(MatrixPanel, "", "", True, False, 20, 125, self.W_SCREEN - 40, self.iAjustedHeight, PanelStyles.PANEL_STYLE_EMPTY)

		screen.addScrollPanel(MainPanel, "", 20 + 59, 65, self.W_SCREEN - 54 - 40, self.H_SCREEN - 151, PanelStyles.PANEL_STYLE_EMPTY)

#		ExoticForPrint ("# players = %d" % self.nCount)

		nCount = 0
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			if self.ltPlayerMet[iLoopPlayer]:
				if (iLoopPlayer != self.iActiveLeader):
					szName = self.getNextWidgetName()
					screen.addCheckBoxGFCAt(MainPanel, szName, gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_GLANCE_OFFSET + (self.nSpread * nCount), 0, self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, self.iActiveLeader, ButtonStyles.BUTTON_STYLE_LABEL, False)
					if (self.iSelectedLeader == iLoopPlayer):
						screen.setState(szName, True)
					else:
						screen.setState(szName, False)

					nCount += 1

		if (self.bGlancePlus):
			nButtonStyle = ButtonStyles.BUTTON_STYLE_CITY_PLUS
		else:
			nButtonStyle = ButtonStyles.BUTTON_STYLE_CITY_MINUS
		screen.addCheckBoxGFCAt(self.GLANCE_HEADER, self.GLANCE_BUTTON, "", "", self.X_GLANCE_OFFSET , self.Y_GLANCE_OFFSET, self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, nButtonStyle, False)

		if (nCount >= self.iMaxRow):
			self.scrollGranceUp = self.getNextWidgetName()
			self.scrollGranceDown = self.getNextWidgetName()
			screen.setImageButton(self.scrollGranceUp, ArtFileMgr.getInterfaceArtInfo("SCROLL_UP_ARROW").getPath(), 30, self.H_SCREEN - 82, 20, 20, WidgetTypes.WIDGET_GENERAL, self.SCROLL_GRANCE_UP, -1)
			screen.setImageButton(self.scrollGranceDown, ArtFileMgr.getInterfaceArtInfo("SCROLL_DOWN_ARROW").getPath(), 55, self.H_SCREEN - 82, 20, 20, WidgetTypes.WIDGET_GENERAL, self.SCROLL_GRANCE_DOWN, -1)

			if (self.nRowOffset == 0):
				screen.enable(self.scrollGranceUp, False)
			if (self.nRowOffset >= self.nCount - self.iMaxRow):
				screen.enable(self.scrollGranceDown, False)

		self.drawGlanceRows(screen, MainPanel, MatrixPanel, self.iSelectedLeader != self.iActiveLeader, self.iSelectedLeader)

	def calculateRelations (self, nPlayer, nTarget):
		if (nPlayer != nTarget and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
			nAttitude = 0
			szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
			szAttitude = szAttitude.replace(gc.getPlayer(nPlayer).getName(),"")
			szAttitude = szAttitude.replace(gc.getPlayer(nTarget).getName(),"")
#			ExoticForPrint (("%d toward %d" % (nPlayer, nTarget)) + str(szAttitude))
			ltPlusAndMinuses = re.findall ("[-+][0-9]+", szAttitude)
#			ExoticForPrint ("Length: %d" % len (ltPlusAndMinuses))
			for i in range (len (ltPlusAndMinuses)):
				nAttitude += int (ltPlusAndMinuses[i])
#			ExoticForPrint ("Attitude: %d" % nAttitude)
		else:
			return None
		return nAttitude

	def drawGlanceRows (self, screen, MainPanel, MatrixPanel, bSorted = False, nPlayer = 1):

		ltSortedRelations = [(None,-1)] * gc.getMAX_PLAYERS()
#		ExoticForPrint ("MAX Players = %d" % gc.getMAX_PLAYERS())
		if bSorted:
			self.loadColIntoList(self.ltPlayerRelations, ltSortedRelations, nPlayer)
			ltSortedRelations.sort()
			if (self.bGlancePlus):
				ltSortedRelations.reverse()
		else:
			self.loadColIntoList (self.ltPlayerRelations, ltSortedRelations, nPlayer)

		# loop through all players and display leaderheads
		for nOffset in xrange(gc.getMAX_PLAYERS()):
			if ltSortedRelations[nOffset][1] != -1:
				break

		iStart = self.nRowOffset
		if (self.nCount > self.iMaxRow):
			iEnd = self.nRowOffset + self.iMaxRow
		else:
			iEnd = self.nCount

		iCount = 0
		for i in xrange(iStart, iEnd):
			iLoopPlayer = ltSortedRelations[nOffset + i][1]
#			ExoticForPrint ("iLoopPlayer = %d" % iLoopPlayer)

			playerPanelName = self.getNextWidgetName()
			screen.attachPanel(MatrixPanel, playerPanelName, "", "", False, True, PanelStyles.PANEL_STYLE_OUT)

			szName = self.getNextWidgetName()
			screen.attachCheckBoxGFC(playerPanelName, szName, gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, self.iActiveLeader, ButtonStyles.BUTTON_STYLE_LABEL)

			iLoopTeam = gc.getPlayer(iLoopPlayer).getTeam()
			nCount = 0
			iYOffset = int((self.hSpread + 6) * iCount) + int(self.hSpread /2) + 55
			for j in xrange(gc.getMAX_PLAYERS()):
				if (self.ltPlayerMet[j]):
					if (j != self.iActiveLeader):
						szName = self.getNextWidgetName()
						nAttitude = self.ltPlayerRelations[iLoopPlayer][j]
						iXOffset = self.X_GLANCE_OFFSET + self.GLANCE_BUTTON_SIZE/2 + (self.nSpread * nCount)
						if (nAttitude != None):
							szText = self.getAttitudeText(nAttitude, j, iLoopPlayer)
							screen.setTextAt(szName, MainPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, iXOffset - CyInterface().determineWidth(szText) / 2, iYOffset - 2, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, j, iLoopPlayer)
							if (gc.getTeam(gc.getPlayer(j).getTeam()).isVassal(gc.getPlayer(iLoopTeam).getTeam())):
								szText = localText.getText("TXT_KEY_MISC_VASSAL", ())
								color = gc.getInfoTypeForString("COLOR_RED")
								szText = localText.changeTextColor(szText, color)
								szName = self.getNextWidgetName()
								screen.setTextAt(szName, MainPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, iXOffset - CyInterface().determineWidth(szText) / 2, iYOffset -16, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, j, iLoopPlayer)
							elif (gc.getTeam(iLoopTeam).isVassal(gc.getPlayer(j).getTeam())):
								szText = localText.getText("TXT_KEY_MISC_MASTER", ())
								color = gc.getInfoTypeForString("COLOR_GREEN")
								szText = localText.changeTextColor(szText, color)
								szName = self.getNextWidgetName()
								screen.setTextAt(szName, MainPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, iXOffset - CyInterface().determineWidth(szText) / 2, iYOffset -16, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, j, iLoopPlayer)
						else:
							szText = "<font=4>-</font>"
							screen.setTextAt(szName, MainPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, iXOffset - CyInterface().determineWidth(szText) / 2, iYOffset - 5, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

						nCount += 1
			iCount += 1

		if (self.nCount < self.iMaxRow):
			for i in xrange(self.iMaxRow - self.nCount):
				playerPanelName = self.getNextWidgetName()
				screen.attachPanel(MatrixPanel, playerPanelName, "", "", False, True, PanelStyles.PANEL_STYLE_OUT)

				szName = self.getNextWidgetName()
				screen.attachSeparator(playerPanelName, szName, True, self.GLANCE_BUTTON_SIZE+4)

	def loadColIntoList (self, ltPlayers, ltTarget, nCol):
		nCount = 0
		for i in range (len (ltTarget)):
			if (self.ltPlayerMet[i]):
#				ExoticForPrint ("player met = %d; nCount = %d" % (i, nCount))
				ltTarget[nCount] = (ltPlayers[i][nCol], i)
				nCount += 1

	def getAttitudeText(self, nAttitude, nPlayer, nTarget):
		szText = str(nAttitude)
		if nAttitude > 0:
			szText = "+" + szText
#		ExoticForPrint ("Attitude String = %s" % szAttitude)
		if (gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isAtWar(gc.getPlayer(nTarget).getTeam())):
			szText = "<color=255,0,0>%s</color>"%(szText)
		szText = "%s<font=3>(%s)</font>"%(self.AttitudeFontMap[gc.getPlayer(nPlayer).AI_getAttitude(nTarget)], szText)
		if (gc.getPlayer(nPlayer).getWorstEnemyName() == gc.getPlayer(nTarget).getName()):
			szText = szText%("WE")
		else:
			szText = szText%("")
		return szText

	def handlePlusMinusToggle (self):
#		ExoticForPrint ("Entered handlePlusMinusToggle")

		self.bGlancePlus = not self.bGlancePlus
		self.drawContents(False)

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

	def initTradeTable(self):
		screen = self.getScreen()

		if (self.RES_SHOW_ACTIVE_TRADE):
			columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN )
		else:
			columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN )
		self.NUM_RESOURCE_COLUMNS = len(columns) - 1

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.RES_SURPLUS_HEIGHT + self.RES_PANEL_SPACE + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - self.RES_SURPLUS_HEIGHT - self.RES_PANEL_SPACE - self.TITLE_HEIGHT - 20

		self.resIconGridName = self.getNextWidgetName()
		self.resIconGrid = IconGrid.IconGrid( self.resIconGridName, screen, gridX, gridY, gridWidth, gridHeight
											, columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS )

		self.resIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.resIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.resIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.resIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		self.leaderCol = 0
		self.surplusCol = 1
		self.usedCol = 2
		self.willTradeCol = 3
		self.wontTradeCol = 4
		self.canPayCol = 5
		self.activeExportCol = 6
		self.activeImportCol = 7
		self.payingCol = 8

		self.resIconGrid.setHeader( self.leaderCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()) )
		self.resIconGrid.setHeader( self.surplusCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_SURPLUS", ()) )
		self.resIconGrid.setHeader( self.usedCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_USED", ()) )
		self.resIconGrid.setHeader( self.willTradeCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.wontTradeCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.canPayCol, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
		self.resIconGrid.setTextColWidth(self.canPayCol, self.RES_GOLD_COL_WIDTH)

		if (self.RES_SHOW_ACTIVE_TRADE):
			self.resIconGrid.setHeader( self.activeExportCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_EXPORT", ()) )
			self.resIconGrid.setHeader( self.activeImportCol, localText.getText("TXT_KEY_FOREIGN_ADVISOR_IMPORT", ()) )
			self.resIconGrid.setHeader( self.payingCol, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
			self.resIconGrid.setTextColWidth(self.payingCol, self.RES_GOLD_COL_WIDTH)
		if (self.RES_SHOW_IMPORT_EXPORT_HEADER):
			self.resIconGrid.createColumnGroup("", 1)
			self.resIconGrid.createColumnGroup(localText.getText("TXT_KEY_FOREIGN_ADVISOR_EXPORT", ()), 2)
			self.resIconGrid.createColumnGroup(localText.getText("TXT_KEY_FOREIGN_ADVISOR_IMPORT", ()), 3)
			if (self.RES_SHOW_ACTIVE_TRADE):
				self.resIconGrid.createColumnGroup(localText.getText("TXT_KEY_FOREIGN_ADVISOR_ACTIVE", ()), 3)

		gridWidth = self.resIconGrid.getPrefferedWidth()
		gridHeight = self.resIconGrid.getPrefferedHeight()
		self.RES_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.RES_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - self.RES_SURPLUS_HEIGHT - self.RES_PANEL_SPACE - self.TITLE_HEIGHT - 20) / 2
		gridX = self.RES_LEFT_RIGHT_SPACE + 10
		gridY = self.RES_TOP_BOTTOM_SPACE + self.RES_SURPLUS_HEIGHT + self.RES_PANEL_SPACE + self.TITLE_HEIGHT + 10

		self.resIconGrid.setPosition(gridX, gridY)
		self.resIconGrid.setSize(gridWidth, gridHeight)

	def calculateSurplusPanelLayout(self):
		self.SURPLUS_X = self.RES_LEFT_RIGHT_SPACE
		self.SURPLUS_Y = self.RES_TOP_BOTTOM_SPACE
		self.SURPLUS_WIDTH = self.W_SCREEN - 2 * self.RES_LEFT_RIGHT_SPACE

		self.SURPLUS_ICONS_X = self.SURPLUS_X + 10
		if (self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP):
			self.SURPLUS_TABLE_X = self.SURPLUS_ICONS_X + 15
			SURPLUS_VERTICAL_SPACING = (self.RES_SURPLUS_HEIGHT - self.RESOURCE_ICON_SIZE - self.TITLE_HEIGHT) / 2
			self.SURPLUS_ICONS_Y = self.SURPLUS_Y + SURPLUS_VERTICAL_SPACING + self.TITLE_HEIGHT
			self.SURPLUS_TABLE_Y = self.SURPLUS_ICONS_Y + (self.RESOURCE_ICON_SIZE - self.TABLE_CONTROL_HEIGHT) / 2 + 8
		else:
			self.SURPLUS_TABLE_X = self.SURPLUS_ICONS_X + 5
			SURPLUS_VERTICAL_SPACING = ( self.RES_SURPLUS_HEIGHT - self.RESOURCE_ICON_SIZE - self.TABLE_CONTROL_HEIGHT - self.TITLE_HEIGHT ) / 2 + 3
			self.SURPLUS_ICONS_Y = self.SURPLUS_Y + SURPLUS_VERTICAL_SPACING + self.TITLE_HEIGHT
			self.SURPLUS_TABLE_Y = self.SURPLUS_ICONS_Y + self.RESOURCE_ICON_SIZE

		self.SURPLUS_CIRCLE_X_START = self.SURPLUS_TABLE_X + 4
		self.SURPLUS_CIRCLE_Y = self.SURPLUS_TABLE_Y + 5

	def drawResourceDeals(self, bInitial):
		screen = self.getScreen()
		activePlayer = gc.getPlayer(self.iActiveLeader)
		self.initTradeTable()

		# Find all the surplus resources
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_RESOURCES
		listSurplus = []

		for iLoopBonus in xrange(gc.getNumBonusInfos()):
			tradeData.iData = iLoopBonus
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				currentPlayer = gc.getPlayer(iLoopPlayer)
				if (currentPlayer.isAlive() and not currentPlayer.isBarbarian()
					and not currentPlayer.isMinorCiv() 
					and gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam())
					and iLoopPlayer != self.iActiveLeader
					and activePlayer.canTradeItem(iLoopPlayer, tradeData, False)
					and activePlayer.getNumTradeableBonuses(iLoopBonus) > 1):
					listSurplus.append(iLoopBonus)
					break

		self.calculateSurplusPanelLayout()

		# Assemble the surplus panel
		self.mainAvailablePanel = self.getNextWidgetName()
		screen.addPanel( self.mainAvailablePanel, localText.getText("TXT_KEY_FOREIGN_ADVISOR_SURPLUS_RESOURCES", ()), ""
					   , False, False, self.SURPLUS_X, self.SURPLUS_Y, self.SURPLUS_WIDTH, self.RES_SURPLUS_HEIGHT
					   , PanelStyles.PANEL_STYLE_MAIN )

		self.availableMultiList = self.getNextWidgetName()
		screen.addMultiListControlGFC( self.availableMultiList, ""
									 , self.SURPLUS_ICONS_X, self.SURPLUS_ICONS_Y
									 , self.RESOURCE_ICON_SIZE * len(listSurplus), self.RESOURCE_ICON_SIZE
									 , 1, 32, 32, TableStyles.TABLE_STYLE_EMPTY )

		self.availableTable = self.getNextWidgetName()
		# add the circles behind the amounts
		if (self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP):
			for iIndex in range(len(listSurplus)):
				screen.addDDSGFC("%sCircle%d"%(self.availableTable, iIndex)
								 , ArtFileMgr.getInterfaceArtInfo("WHITE_CIRCLE_40").getPath()
								 , self.SURPLUS_CIRCLE_X_START + iIndex * self.RESOURCE_ICON_SIZE, self.SURPLUS_CIRCLE_Y
								 , 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# add the table showing the amounts
		screen.addTableControlGFC( self.availableTable, len(listSurplus)
							     , self.SURPLUS_TABLE_X, self.SURPLUS_TABLE_Y
							     , len(listSurplus) * self.RESOURCE_ICON_SIZE, self.TABLE_CONTROL_HEIGHT
							     , False, False, 16, 16, TableStyles.TABLE_STYLE_EMPTY )

		# Add the bonuses to the surplus panel with their amount
		for iIndex in xrange(len(listSurplus)):
			screen.appendMultiListButton( self.availableMultiList, gc.getBonusInfo(listSurplus[iIndex]).getButton(), 0
										, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, listSurplus[iIndex], -1, False )
			screen.setTableColumnHeader( self.availableTable, iIndex, u"", self.RESOURCE_ICON_SIZE )

			amount = activePlayer.getNumTradeableBonuses(listSurplus[iIndex])
			if (self.RES_SHOW_EXTRA_AMOUNT):
				amount = amount - 1

			if (self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP):
				amountStr = u"<font=2>%s</font>"%(localText.changeTextColor(str(amount), gc.getInfoTypeForString("COLOR_YELLOW")))
			else:
				amountStr = u"<font=3>%d</font>"%(amount)
			screen.setTableText( self.availableTable, iIndex, 0, amountStr, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 0 )

# 		# Assemble the panel that shows the trade table
		self.TABLE_PANEL_X = self.RES_LEFT_RIGHT_SPACE
		self.TABLE_PANEL_Y = self.SURPLUS_Y + self.RES_SURPLUS_HEIGHT + self.RES_PANEL_SPACE
		self.TABLE_PANEL_WIDTH = self.W_SCREEN - 2 * self.RES_LEFT_RIGHT_SPACE
		self.TABLE_PANEL_HEIGHT = self.H_SCREEN - self.TABLE_PANEL_Y - self.RES_TOP_BOTTOM_SPACE

		self.tradePanel = self.getNextWidgetName()
		screen.addPanel(self.tradePanel, localText.getText("TXT_KEY_FOREIGN_ADVISOR_TRADE_TABLE", ()), ""
					   , True, True, self.TABLE_PANEL_X, self.TABLE_PANEL_Y, self.TABLE_PANEL_WIDTH, self.TABLE_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)

		self.resIconGrid.createGrid()

		# find all players that need to be listed 
		self.resIconGrid.clearData()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_RESOURCES
		currentRow = 0

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			if ( currentPlayer.isAlive() and not currentPlayer.isBarbarian() and not currentPlayer.isMinorCiv()
				and gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam())
				and iLoopPlayer != self.iActiveLeader ):
				message = ""
				if ( not activePlayer.canTradeNetworkWith(iLoopPlayer) ):
					message = localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_CONNECTED", ())

				self.resIconGrid.appendRow(currentPlayer.getName(), message)
				self.resIconGrid.addIcon(currentRow, self.leaderCol, gc.getLeaderHeadInfo(currentPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				for iLoopBonus in xrange(gc.getNumBonusInfos()):
					if (gc.getTeam(activePlayer.getTeam()).isGoldTrading() or gc.getTeam(currentPlayer.getTeam()).isGoldTrading()):
						sAmount = str(gc.getPlayer(iLoopPlayer).AI_maxGoldPerTurnTrade(self.iActiveLeader))
						self.resIconGrid.setText(currentRow, self.canPayCol, sAmount)

					tradeData.iData = iLoopBonus
					if ( activePlayer.canTradeItem(iLoopPlayer, tradeData, False) ):
						if ( activePlayer.getNumTradeableBonuses(iLoopBonus) > 1 ): # surplus
							self.resIconGrid.addIcon(currentRow, self.surplusCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus)
						else: # used
							self.resIconGrid.addIcon(currentRow, self.usedCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus)
					elif (currentPlayer.canTradeItem(self.iActiveLeader, tradeData, False)):
						if (currentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL): # will trade
							self.resIconGrid.addIcon(currentRow, self.willTradeCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus)
						else: # won't trade
							self.resIconGrid.addIcon(currentRow, self.wontTradeCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus)
				if (self.RES_SHOW_ACTIVE_TRADE):
					amount = 0
					for iLoopDeal in xrange(gc.getGame().getIndexAfterLastDeal()):
						deal = gc.getGame().getDeal(iLoopDeal)
						if ( deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader and not deal.isNone() ):
							for iLoopTradeItem in range(deal.getLengthFirstTrades()):
								tradeData2 = deal.getFirstTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount += tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeImportCol
															, gc.getBonusInfo(tradeData2.iData).getButton()
															, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
							for iLoopTradeItem in xrange(deal.getLengthSecondTrades()):
								tradeData2 = deal.getSecondTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount -= tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeExportCol
															, gc.getBonusInfo(tradeData2.iData).getButton()
															, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )

						if ( deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader ):
							for iLoopTradeItem in xrange(deal.getLengthFirstTrades()):
								tradeData2 = deal.getFirstTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount -= tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeExportCol
															, gc.getBonusInfo(tradeData2.iData).getButton()
															, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
							for iLoopTradeItem in xrange(deal.getLengthSecondTrades()):
								tradeData2 = deal.getSecondTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount += tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeImportCol
															, gc.getBonusInfo(tradeData2.iData).getButton()
															, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
					if (amount != 0):
						self.resIconGrid.setText(currentRow, self.payingCol, str(amount))
				currentRow += 1
		self.resIconGrid.refresh()

	def scrollTradeTableUp(self, bPage):
		if (self.iScreen == self.SCREEN_DICT["BONUS"]):
			if (bPage):
				self.resIconGrid.PageUp()
			else:
				self.resIconGrid.scrollUp()
		elif (self.iScreen == self.SCREEN_DICT["TECH"]):
			if (bPage):
				self.techIconGrid.PageUp()
			else:
				self.techIconGrid.scrollUp()
		elif (self.iScreen == self.SCREEN_DICT["DIPLOMACY"]):
			if (bPage):
				self.DiploIconGrid.PageUp()
			else:
				self.DiploIconGrid.scrollUp()
		elif (self.iScreen == self.SCREEN_DICT["INFO"]):
			if (bPage):
				self.InfoIconGrid.PageUp()
			else:
				self.InfoIconGrid.scrollUp()

	def scrollTradeTableDown(self, bPage):
		if (self.iScreen == self.SCREEN_DICT["BONUS"]):
			if (bPage):
				self.resIconGrid.PageDown()
			else:
				self.resIconGrid.scrollDown()
		elif (self.iScreen == self.SCREEN_DICT["TECH"]):
			if (bPage):
				self.techIconGrid.PageDown()
			else:
				self.techIconGrid.scrollDown()
		elif (self.iScreen == self.SCREEN_DICT["DIPLOMACY"]):
			if (bPage):
				self.DiploIconGrid.PageDown()
			else:
				self.DiploIconGrid.scrollDown()
		elif (self.iScreen == self.SCREEN_DICT["INFO"]):
			if (bPage):
				self.InfoIconGrid.PageDown()
			else:
				self.InfoIconGrid.scrollDown()

	def drawTechDeals(self, bInitial):
		screen = self.getScreen()
		activePlayer = gc.getPlayer(self.iActiveLeader)
		self.initTechTable()
		
		# Assemble the panel
		TECH_PANEL_X = self.TECH_LEFT_RIGHT_SPACE
		TECH_PANEL_Y = self.TECH_TOP_BOTTOM_SPACE
		TECH_PANEL_WIDTH = self.W_SCREEN - 2 * self.TECH_LEFT_RIGHT_SPACE
		TECH_PANEL_HEIGHT = self.H_SCREEN - 2 * self.TECH_TOP_BOTTOM_SPACE
		
		self.tradePanel = self.getNextWidgetName()
		screen.addPanel( self.tradePanel, "", "", True, True
					   , TECH_PANEL_X, TECH_PANEL_Y, TECH_PANEL_WIDTH, TECH_PANEL_HEIGHT
					   , PanelStyles.PANEL_STYLE_MAIN )
		
		self.techIconGrid.createGrid()
		
		self.techIconGrid.clearData()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
		currentRow = 0
		
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			if ( currentPlayer.isAlive() and not currentPlayer.isBarbarian() and not currentPlayer.isMinorCiv() 
										 and gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam()) 
										 and iLoopPlayer != self.iActiveLeader ):
				message = ""
				if ( not gc.getTeam(activePlayer.getTeam()).isTechTrading() and not gc.getTeam(currentPlayer.getTeam()).isTechTrading() ):
					message = localText.getText("TXT_KEY_FOREIGN_ADVISOR_NO_TECH_TRADING", ())

				self.techIconGrid.appendRow(currentPlayer.getName(), message)
				self.techIconGrid.addIcon( currentRow, 0, gc.getLeaderHeadInfo(currentPlayer.getLeaderType()).getButton()
										 , WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer )
				
				if (gc.getTeam(activePlayer.getTeam()).isGoldTrading() or gc.getTeam(currentPlayer.getTeam()).isGoldTrading()):
					sAmount = str(gc.getPlayer(iLoopPlayer).AI_maxGoldTrade(self.iActiveLeader))
					self.techIconGrid.setText(currentRow, 3, sAmount)
				
				if (gc.getTeam(activePlayer.getTeam()).isTechTrading() or gc.getTeam(currentPlayer.getTeam()).isTechTrading() ):

					for iLoopTech in range(gc.getNumTechInfos()):
					
						tradeData.iData = iLoopTech
						if (activePlayer.canTradeItem(iLoopPlayer, tradeData, False) and activePlayer.getTradeDenial(iLoopPlayer, tradeData) == DenialTypes.NO_DENIAL): # wants
							self.techIconGrid.addIcon( currentRow, 1, gc.getTechInfo(iLoopTech).getButton()
																				 , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						elif currentPlayer.canResearch(iLoopTech, False):
							self.techIconGrid.addIcon( currentRow, 2, gc.getTechInfo(iLoopTech).getButton()
																			, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						if (currentPlayer.canTradeItem(self.iActiveLeader, tradeData, False)):
							if (currentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL): # will trade
								self.techIconGrid.addIcon( currentRow, 4, gc.getTechInfo(iLoopTech).getButton()
																					 , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
							else: # won't trade
								self.techIconGrid.addIcon( currentRow, 5, gc.getTechInfo(iLoopTech).getButton()
																					 , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						elif (gc.getTeam(currentPlayer.getTeam()).isHasTech(iLoopTech) and activePlayer.canResearch(iLoopTech, False)):
							self.techIconGrid.addIcon( currentRow, 5, gc.getTechInfo(iLoopTech).getButton()
																					 , WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )

				currentRow += 1
		self.techIconGrid.refresh()

	def drawDiplomacy(self, bInitial):
		screen = self.getScreen()
		pActivePlayer = gc.getPlayer(self.iActiveLeader)
		iActiveTeam = pActivePlayer.getTeam()
		pActiveTeam = gc.getTeam(iActiveTeam)
		self.initDiplomacyTable()

		# Assemble the panel
		DIPLO_PANEL_X = self.DIPLO_LEFT_RIGHT_SPACE
		DIPLO_PANEL_Y = self.DIPLO_TOP_BOTTOM_SPACE
		DIPLO_PANEL_WIDTH = self.W_SCREEN - 2 * self.DIPLO_LEFT_RIGHT_SPACE
		DIPLO_PANEL_HEIGHT = self.H_SCREEN - 2 * self.DIPLO_TOP_BOTTOM_SPACE

		self.diploPanel = self.getNextWidgetName()
		screen.addPanel(self.diploPanel, "", "", True, True, DIPLO_PANEL_X, DIPLO_PANEL_Y, DIPLO_PANEL_WIDTH, DIPLO_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)

		self.DiploIconGrid.createGrid()

		self.DiploIconGrid.clearData()
		tradeData = TradeData()
		currentRow = 0

		for iCurrentPlayer in xrange(gc.getMAX_PLAYERS()):
			pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
			iCurrentTeam = pCurrentPlayer.getTeam()
			pCurrentTeam = gc.getTeam(iCurrentTeam)

			if (pCurrentPlayer.isAlive() and not pCurrentPlayer.isBarbarian() and not pCurrentPlayer.isMinorCiv() and pCurrentTeam.isHasMet(iActiveTeam)
				and iCurrentPlayer != self.iActiveLeader):

				self.DiploIconGrid.appendRow(pCurrentPlayer.getName(), "")
				self.DiploIconGrid.addIcon(currentRow, 0, gc.getLeaderHeadInfo(pCurrentPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iCurrentPlayer)

				szWorstEnemyName = pCurrentPlayer.getWorstEnemyName()
				iWorstEnemy = -1
				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if (iCurrentPlayer == iLoopPlayer or not pLoopPlayer.isAlive() or pLoopPlayer.isBarbarian() or pLoopPlayer.isMinorCiv()):
						continue
					LoopTeam = pLoopPlayer.getTeam()
					if (gc.getTeam(iActiveTeam).isHasMet(LoopTeam) and pCurrentTeam.isHasMet(LoopTeam)):
						if (pLoopPlayer.getName() == szWorstEnemyName):
							iWorstEnemy = iLoopPlayer
						if (pCurrentTeam.isAtWar(LoopTeam)):
							self.DiploIconGrid.addIcon(currentRow, 2, gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)
						if (iLoopPlayer != self.iActiveLeader):
							if (pCurrentPlayer.canTradeWith(iLoopPlayer)):
								tradeData.iData = iLoopPlayer
								tradeData.ItemType = TradeableItems.TRADE_WAR
								if (pCurrentPlayer.canTradeItem(self.iActiveLeader, tradeData, False)):
									if (pCurrentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
										# will trade
										self.DiploIconGrid.addIcon(currentRow, 3, gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)
								tradeData.ItemType = TradeableItems.TRADE_PEACE
								if (pCurrentPlayer.canTradeItem(self.iActiveLeader, tradeData, True)):
									if (pCurrentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
										self.DiploIconGrid.addIcon(currentRow, 4, gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)
								tradeData.ItemType = TradeableItems.TRADE_EMBARGO
								if (pCurrentPlayer.canTradeItem(self.iActiveLeader, tradeData, True)):
									if (pCurrentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
										self.DiploIconGrid.addIcon(currentRow, 5, gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				tradeData.ItemType = TradeableItems.TRADE_CIVIC
				for iCivic in xrange(gc.getNumCivicInfos()):
					tradeData.iData = iCivic
					if (pCurrentPlayer.canTradeItem(self.iActiveLeader, tradeData, True)):
						if (pCurrentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
							self.DiploIconGrid.addIcon(currentRow, 6, gc.getCivicInfo(iCivic).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic)
				tradeData.ItemType = TradeableItems.TRADE_RELIGION
				for iReligion in xrange(gc.getNumReligionInfos()):
					tradeData.iData = iReligion
					if (pCurrentPlayer.canTradeItem(self.iActiveLeader, tradeData, True)):
						if (pCurrentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
							self.DiploIconGrid.addIcon(currentRow, 7, gc.getReligionInfo(iReligion).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iReligion)

				if (iWorstEnemy > -1):
					self.DiploIconGrid.addIcon(currentRow, 1, gc.getLeaderHeadInfo(gc.getPlayer(iWorstEnemy).getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iWorstEnemy)
				else:
					self.DiploIconGrid.addIcon(currentRow, 1, "", WidgetTypes.WIDGET_LEADERHEAD, -1)

				#Next player, increment row
				currentRow += 1
		self.DiploIconGrid.refresh()

	def initTechTable(self):
		screen = self.getScreen()

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + 10
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - 20

		columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
								, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN
								, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN )
		self.techIconGridName = self.getNextWidgetName()
		self.techIconGrid = IconGrid.IconGrid( self.techIconGridName, screen, gridX, gridY, gridWidth, gridHeight
											 , columns, self.TECH_USE_SMALL_ICONS, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS )

		self.techIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.techIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.techIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.techIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		self.techIconGrid.setHeader( 0, localText.getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()) )
		self.techIconGrid.setHeader( 1, localText.getText("TXT_KEY_FOREIGN_ADVISOR_WANTS", ()) )
		self.techIconGrid.setHeader( 2, localText.getText("TXT_KEY_FOREIGN_ADVISOR_CAN_RESEARCH", ()) )
		self.techIconGrid.setHeader( 3, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
		self.techIconGrid.setTextColWidth( 3, self.TECH_GOLD_COL_WITH )
		self.techIconGrid.setHeader( 4, localText.getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE_2", ()) )
		self.techIconGrid.setHeader( 5, localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE_2", ()) )

		gridWidth = self.techIconGrid.getPrefferedWidth()
		gridHeight = self.techIconGrid.getPrefferedHeight()
		self.TECH_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.TECH_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.TECH_LEFT_RIGHT_SPACE + 10
		gridY = self.TECH_TOP_BOTTOM_SPACE + 10

		self.techIconGrid.setPosition(gridX, gridY)
		self.techIconGrid.setSize(gridWidth, gridHeight)

	def initDiplomacyTable(self):
		screen = self.getScreen()

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + 10
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - 20

		columns = (IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_SMALL_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN)
		self.DiploIconGridName = self.getNextWidgetName()
		self.DiploIconGrid = IconGrid.IconGrid(self.DiploIconGridName, screen, gridX, gridY, gridWidth, gridHeight, columns, self.TECH_USE_SMALL_ICONS, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)

		self.DiploIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.DiploIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.DiploIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.DiploIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		self.DiploIconGrid.setHeader(0, localText.getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()))
		self.DiploIconGrid.setHeader(1, localText.getText("TXT_KEY_FOREIGN_ADVISOR_WORST_ENEMY", ()))
		self.DiploIconGrid.setHeader(2, localText.getText("TXT_KEY_FOREIGN_ADVISOR_ACTIVE_WAR", ()))
		self.DiploIconGrid.setHeader(3, localText.getText("TXT_KEY_TRADE_DECLARE_WAR_ON", ()))
		self.DiploIconGrid.setHeader(4, localText.getText("TXT_KEY_TRADE_MAKE_PEACE_WITH", ()))
		self.DiploIconGrid.setHeader(5, localText.getText("TXT_KEY_TRADE_STOP_TRADING_WITH", ()))
		self.DiploIconGrid.setHeader(6, localText.getText("TXT_KEY_TRADE_ADOPT", ()))
		self.DiploIconGrid.setHeader(7, localText.getText("TXT_KEY_TRADE_CONVERT", ()))

		gridWidth = self.DiploIconGrid.getPrefferedWidth()
		gridHeight = self.DiploIconGrid.getPrefferedHeight()
		self.DIPLO_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.DIPLO_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.DIPLO_LEFT_RIGHT_SPACE + 10
		gridY = self.DIPLO_TOP_BOTTOM_SPACE + 10

		self.DiploIconGrid.setPosition(gridX, gridY)
		self.DiploIconGrid.setSize(gridWidth, gridHeight)

##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################
	# Handles the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_LEADERHEAD):
				if (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
					self.iSelectedLeader = inputClass.getData1()
					self.drawContents(False)
				elif (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					self.getScreen().hideScreen()
			elif (inputClass.getFunctionName() == self.GLANCE_BUTTON):
				self.handlePlusMinusToggle()
############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.SCROLL_TABLE_UP):
					self.scrollTradeTableUp(CvEventInterface.getEventManager().bShift)
				elif (inputClass.getData1() == self.SCROLL_TABLE_DOWN):
					self.scrollTradeTableDown(CvEventInterface.getEventManager().bShift)
				elif (inputClass.getData1() == self.SCROLL_GRANCE_UP):
					if (CvEventInterface.getEventManager().bShift):
						self.nRowOffset -= self.iMaxRow
						if (self.nRowOffset < 0):
							self.nRowOffset = 0
						self.drawContents(False)
					else:
						if (self.nRowOffset > 0):
							self.nRowOffset -= 1
							self.drawContents(False)
				elif (inputClass.getData1() == self.SCROLL_GRANCE_DOWN):
					if (CvEventInterface.getEventManager().bShift):
						self.nRowOffset += self.iMaxRow
						if (self.nRowOffset > self.nCount - self.iMaxRow):
							self.nRowOffset = self.nCount - self.iMaxRow
						self.drawContents(False)
					else:
						if (self.nRowOffset < self.nCount - self.iMaxRow):
							self.nRowOffset += 1
							self.drawContents(False)
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS):
#				ExoticForPrint ("FOOOOOO!!!!")
				pass
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() + str(inputClass.getID()) == self.getWidgetName(self.DEBUG_DROPDOWN_ID)):
				print 'debug dropdown event'
				szName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActiveLeader = self.getScreen().getPullDownData(szName, iIndex)
				self.drawContents(False)
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID() 

		return 0
