## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvScreensInterface
import TechPrefs

PIXEL_INCREMENT = 7
BOX_INCREMENT_WIDTH = 27 # Used to be 33 #Should be a multiple of 3...
BOX_INCREMENT_HEIGHT = 9 #Should be a multiple of 3...
BOX_INCREMENT_Y_SPACING = 6 #Should be a multiple of 3...
BOX_INCREMENT_X_SPACING = 9 #Should be a multiple of 3...

TEXTURE_SIZE = 24
X_START = 6
X_INCREMENT = 27
Y_ROW = 32

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3

FLAVORS = [TechPrefs.FLAVOR_PRODUCTION, TechPrefs.FLAVOR_GOLD, TechPrefs.FLAVOR_SCIENCE, TechPrefs.FLAVOR_CULTURE, TechPrefs.FLAVOR_RELIGION]
UNIT_CLASSES = ["UNITCLASS_ENGINEER", "UNITCLASS_MERCHANT", "UNITCLASS_SCIENTIST", "UNITCLASS_ARTIST", "UNITCLASS_PROPHET"]
CFG_WIDE_TECH_SCREEN = True

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvTechChooser:
	"Tech Chooser Screen"

	def __init__(self):
		self.nWidgetCount = 0
		self.iCivSelected = 0
		self.aiCurrentState = []
		self.iCanResTech = -1

		# Advanced Start
		self.m_iSelectedTech = -1
		self.m_bSelectedTechDirty = False
		self.m_bTechRecordsDirty = False

	def hideScreen (self):

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Hide the screen
		screen.hideScreen()

	# Screen construction function
	def interfaceScreen(self):

		if ( CyGame().isPitbossHost() ):
			return

		# Create a new screen, called TechChooser, using the file CvTechChooser.py for input
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.hide("AddTechButton")
		screen.hide("ASPointsLabel")
		screen.hide("SelectedTechLabel")

		if ( CyGame().isDebugMode() ):
			screen.addDropDownBoxGFC( "CivDropDown", 22, 12, 192, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation( "CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			for j in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString( "CivDropDown", gc.getPlayer(j).getName(), j, j, False )
		else:
			screen.hide( "CivDropDown" )

		if ( screen.isPersistent() and self.iCivSelected == gc.getGame().getActivePlayer()):
			self.updateTechRecords(false)
			self.hideTechLBPanel()
			return

		self.nWidgetCount = 0
		self.iCivSelected = gc.getGame().getActivePlayer()
		self.aiCurrentState = []
		screen.setPersistent( True )

		# Advanced Start
		if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() >= 0):

			self.m_iSelectedTechDirty = True

			self.X_ADD_TECH_BUTTON = 10
			self.Y_ADD_TECH_BUTTON = 731
			self.W_ADD_TECH_BUTTON = 150
			self.H_ADD_TECH_BUTTON = 30
			self.X_ADVANCED_START_TEXT = self.X_ADVANCED_START_TEXT = self.X_ADD_TECH_BUTTON + self.W_ADD_TECH_BUTTON + 20

			szText = localText.getText("TXT_KEY_WB_AS_ADD_TECH", ())
			screen.setButtonGFC( "AddTechButton", szText, "", self.X_ADD_TECH_BUTTON, self.Y_ADD_TECH_BUTTON, self.W_ADD_TECH_BUTTON, self.H_ADD_TECH_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
			screen.hide("AddTechButton")

		# Here we set the background widget and exit button, and we show the screen
		XResolusion = screen.getXResolution()
		if (CFG_WIDE_TECH_SCREEN and XResolusion > 1024):
			self.iPanel_Width = XResolusion - 50
			self.iPanel_X = 25
		else:
			self.iPanel_Width = 1024
			self.iPanel_X = screen.centerX(0)
		screen.showWindowBackground( False )
		screen.setDimensions(self.iPanel_X, screen.centerY(0), self.iPanel_Width, 768)
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.iPanel_Width, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 48, self.iPanel_Width, 672, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.iPanel_Width, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText( "TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.iPanel_Width - 30, 726, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( "TechChooserExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

		# Header...
		szText = u"<font=4>"
		szText = szText + localText.getText("TXT_KEY_TECH_CHOOSER_TITLE", ()).upper()
		szText = szText + u"</font>"
		screen.setLabel( "TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, self.iPanel_Width/2, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Make the scrollable area for the city list...
		screen.addScrollPanel( "TechList", u"", 0, 64, self.iPanel_Width, 626, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.setActivation( "TechList", ActivationTypes.ACTIVATE_NORMAL )
		screen.hide( "TechList" )

		# Tech Light Blub Button
		screen.setImageButton("TechLBButton", "Art/Interface/Buttons/discoverGP.dds", self.iPanel_Width - 44, 8, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setActivation("TechLBButton", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

		# Place the tech blocks
		self.placeTechs()

		# Draw the arrows
		self.drawArrows()

		screen.moveToFront( "CivDropDown" )

		screen.moveToFront( "AddTechButton" )

	def placeTechs (self):

		iMaxX = 0
		iMaxY = 0

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Go through all the techs
		for i in xrange(gc.getNumTechInfos()):

			# Create and place a tech in its proper location
			iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
			iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5
			szTechRecord = "TechRecord" + str(i)

			if ( iMaxX < iX + self.getXStart() ):
				iMaxX = iX + self.getXStart()
			if ( iMaxY < iY + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ) ):
				iMaxY = iY + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT )

			screen.attachPanelAt( "TechList", szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6, iY - 6, self.getXStart() + 6, 12 + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_TREE, i, -1 )
			screen.setActivation( szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			screen.hide( szTechRecord )

			#reset so that it offsets from the tech record's panel
			iX = 6
			iY = 6

			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
				screen.setPanelColor(szTechRecord, 85, 150, 87)
				self.aiCurrentState.append(CIV_HAS_TECH)
			elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
				screen.setPanelColor(szTechRecord, 100, 104, 160)
				self.aiCurrentState.append(CIV_NO_RESEARCH)
			else:
				screen.setPanelColor(szTechRecord, 206, 65, 69)
				self.aiCurrentState.append(CIV_TECH_AVAILABLE)

			szTechID = "TechID" + str(i)
			szTechString = "<font=1>"
			if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				szTechString = szTechString + str(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "
			szTechString += gc.getTechInfo(i).getDescription() + "</font>"
			screen.setTextAt( szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
			screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

			szTechButtonID = "TechButtonID" + str(i)
			screen.addDDSGFCAt( szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False )

			fX = X_START

			# Unlockable units...
			for j in xrange( gc.getNumUnitClassInfos() ):
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
				if (eLoopUnit != -1):
					if (gc.getUnitInfo(eLoopUnit).getPrereqAndTech() == i):
						szUnitButton = "Unit" + str(j)
						screen.addDDSGFCAt( szUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, True )
						fX += X_INCREMENT

			# Unlockable Buildings...
			for j in xrange(gc.getNumBuildingClassInfos()):
				eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)

				if (eLoopBuilding != -1):
					if (gc.getBuildingInfo(eLoopBuilding).getPrereqAndTech() == i):
						szBuildingButton = "Building" + str(j)
						screen.addDDSGFCAt( szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True )
						fX += X_INCREMENT

			# Obsolete Buildings...
			for j in xrange(gc.getNumBuildingClassInfos()):
				eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(self.iCivSelected).getCivilizationType()).getCivilizationBuildings(j)

				if (eLoopBuilding != -1):
					if (gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == i):
						# Add obsolete picture here...
						szObsoleteButton = "Obsolete" + str(j)
						szObsoleteX = "ObsoleteX" + str(j)
						screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
						screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
						fX += X_INCREMENT

			# Obsolete Bonuses...
			for j in xrange(gc.getNumBonusInfos()):
				if (gc.getBonusInfo(j).getTechObsolete() == i):
					# Add obsolete picture here...
					szObsoleteButton = "ObsoleteBonus" + str(j)
					szObsoleteX = "ObsoleteXBonus" + str(j)
					screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
					screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
					fX += X_INCREMENT

			# Obsolete Monastaries...
			for j in xrange (gc.getNumSpecialBuildingInfos()):
				if (gc.getSpecialBuildingInfo(j).getObsoleteTech() == i):
						# Add obsolete picture here...
						szObsoleteSpecialButton = "ObsoleteSpecial" + str(j)
						szObsoleteSpecialX = "ObsoleteSpecialX" + str(j)
						screen.addDDSGFCAt( szObsoleteSpecialButton, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
						screen.addDDSGFCAt( szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
						fX += X_INCREMENT

			# Route movement change
			for j in xrange(gc.getNumRouteInfos()):
				if ( gc.getRouteInfo(j).getTechMovementChange(i) != 0 ):
					szMoveButton = "Move" + str(j)
					screen.addDDSGFCAt( szMoveButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False )
					fX += X_INCREMENT

			# Promotion Info
			for j in xrange( gc.getNumPromotionInfos() ):
				if ( gc.getPromotionInfo(j).getTechPrereq() == i ):
					szPromotionButton = "Promotion" + str(j)
					screen.addDDSGFCAt( szPromotionButton, szTechRecord, gc.getPromotionInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False )
					fX += X_INCREMENT

			# Free unit
			if ( gc.getTechInfo(i).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS ):
				szFreeUnitButton = "FreeUnit" + str(i)
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(i).getFirstFreeUnitClass())
				if (eLoopUnit != -1):
					screen.addDDSGFCAt( szFreeUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, i, False )
					fX += X_INCREMENT

			# Feature production modifier
			if ( gc.getTechInfo(i).getFeatureProductionModifier() != 0 ):
				szFeatureProductionButton = "FeatureProduction" + str(i)
				screen.addDDSGFCAt( szFeatureProductionButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False )
				fX += X_INCREMENT

			# Worker speed
			if ( gc.getTechInfo(i).getWorkerSpeedModifier() != 0 ):
				szWorkerModifierButton = "Worker" + str(i)
				screen.addDDSGFCAt( szWorkerModifierButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False )
				fX += X_INCREMENT

			# Trade Routes per City change
			if ( gc.getTechInfo(i).getTradeRoutes() != 0 ):
				szTradeRouteButton = "TradeRoutes" + str(i)
				screen.addDDSGFCAt( szTradeRouteButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False )
				fX += X_INCREMENT

			# Health Rate bonus from this tech...
			if ( gc.getTechInfo(i).getHealth() != 0 ):
				szHealthRateButton = "HealthRate" + str(i)
				screen.addDDSGFCAt( szHealthRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False )
				fX += X_INCREMENT

			# Happiness Rate bonus from this tech...
			if ( gc.getTechInfo(i).getHappiness() != 0 ):
				szHappinessRateButton = "HappinessRate" + str(i)
				screen.addDDSGFCAt( szHappinessRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False )
				fX += X_INCREMENT

			# Free Techs
			if ( gc.getTechInfo(i).getFirstFreeTechs() > 0 ):
				szFreeTechButton = "FreeTech" + str(i)
				screen.addDDSGFCAt( szFreeTechButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False )
				fX += X_INCREMENT

			# Line of Sight bonus...
			if ( gc.getTechInfo(i).isExtraWaterSeeFrom() ):
				szLOSButton = "LOS" + str(i)
				screen.addDDSGFCAt( szLOSButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False )
				fX += X_INCREMENT

			# Map Center Bonus...
			if ( gc.getTechInfo(i).isMapCentering() ):
				szMapCenterButton = "MapCenter" + str(i)
				screen.addDDSGFCAt( szMapCenterButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False )
				fX += X_INCREMENT

			# Map Reveal...
			if ( gc.getTechInfo(i).isMapVisible() ):
				szMapRevealButton = "MapReveal" + str(i)
				screen.addDDSGFCAt( szMapRevealButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False )
				fX += X_INCREMENT

			# Map Trading
			if ( gc.getTechInfo(i).isMapTrading() == True ):
				szMapTradeButton = "MapTrade" + str(i)
				screen.addDDSGFCAt( szMapTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False )
				fX += X_INCREMENT

			# Tech Trading
			if ( gc.getTechInfo(i).isTechTrading() ):
				szTechTradeButton = "TechTrade" + str(i)
				screen.addDDSGFCAt( szTechTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False )
				fX += X_INCREMENT

			# Gold Trading
			if ( gc.getTechInfo(i).isGoldTrading() ):
				szGoldTradeButton = "GoldTrade" + str(i)
				screen.addDDSGFCAt( szGoldTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False )
				fX += X_INCREMENT

			# Open Borders
			if ( gc.getTechInfo(i).isOpenBordersTrading() ):
				szOpenBordersButton = "OpenBorders" + str(i)
				screen.addDDSGFCAt( szOpenBordersButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False )
				fX += X_INCREMENT

			# Defensive Pact
			if ( gc.getTechInfo(i).isDefensivePactTrading() ):
				szDefensivePactButton = "DefensivePact" + str(i)
				screen.addDDSGFCAt( szDefensivePactButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False )
				fX += X_INCREMENT

			# Permanent Alliance
			if ( gc.getTechInfo(i).isPermanentAllianceTrading() ):
				szPermanentAllianceButton = "PermanentAlliance" + str(i)
				screen.addDDSGFCAt( szPermanentAllianceButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False )
				fX += X_INCREMENT

			# Vassal States
			if ( gc.getTechInfo(i).isVassalStateTrading() ):
				szVassalStateButton = "VassalState" + str(i)
				screen.addDDSGFCAt( szVassalStateButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False )
				fX += X_INCREMENT

			# Bridge Building
			if ( gc.getTechInfo(i).isBridgeBuilding() ):
				szBuildBridgeButton = "BuildBridge" + str(i)
				screen.addDDSGFCAt( szBuildBridgeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False )
				fX += X_INCREMENT

			# Irrigation unlocked...
			if ( gc.getTechInfo(i).isIrrigation() ):
				szIrrigationButton = "Irrigation" + str(i)
				screen.addDDSGFCAt( szIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False )
				fX += X_INCREMENT

			# Ignore Irrigation unlocked...
			if ( gc.getTechInfo(i).isIgnoreIrrigation() ):
				szIgnoreIrrigationButton = "IgnoreIrrigation" + str(i)
				screen.addDDSGFCAt( szIgnoreIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False )
				fX += X_INCREMENT


			# Coastal Work unlocked...
			if ( gc.getTechInfo(i).isWaterWork() ):
				szWaterWorkButton = "WaterWork" + str(i)
				screen.addDDSGFCAt( szWaterWorkButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False )
				fX += X_INCREMENT

			# Improvements
			for j in xrange(gc.getNumBuildInfos()):
				bTechFound = False

				if (gc.getBuildInfo(j).getTechPrereq() == -1):
					bTechFound = False
					for k in xrange(gc.getNumFeatureInfos()):
						if (gc.getBuildInfo(j).getFeatureTech(k) == i):
							bTechFound = True
				else:
					if (gc.getBuildInfo(j).getTechPrereq() == i):
						bTechFound = True

				if (bTechFound):
					szImprovementButton = "Improvement" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False )
					fX += X_INCREMENT

			# Domain Extra Moves
			for j in xrange( DomainTypes.NUM_DOMAIN_TYPES ):
				if (gc.getTechInfo(i).getDomainExtraMoves(j) != 0):
					szDomainExtraMovesButton = "DomainExtraMoves" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szDomainExtraMovesButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, j, False )
					fX += X_INCREMENT

			# Adjustments
			for j in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
				if (gc.getTechInfo(i).isCommerceFlexible(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isCommerceFlexible(j))):
					szAdjustButton = "AdjustButton" + str( ( i * 1000 ) + j )
					if ( j == CommerceTypes.COMMERCE_CULTURE ):
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
					elif ( j == CommerceTypes.COMMERCE_ESPIONAGE ):
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
					else:
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
					screen.addDDSGFCAt( szAdjustButton, szTechRecord, szFileName, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, j, False )
					fX += X_INCREMENT

			# Terrain opens up as a trade route
			for j in xrange( gc.getNumTerrainInfos() ):
				if (gc.getTechInfo(i).isTerrainTrade(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isTerrainTrade(j))):
					szTerrainTradeButton = "TerrainTradeButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
					fX += X_INCREMENT

			j = gc.getNumTerrainInfos()
			if (gc.getTechInfo(i).isRiverTrade() and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isRiverTrade())):
				szTerrainTradeButton = "TerrainTradeButton" + str( ( i * 1000 ) + j )
				screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
				fX += X_INCREMENT

			# Special buildings like monestaries...
			for j in xrange( gc.getNumSpecialBuildingInfos() ):
				if (gc.getSpecialBuildingInfo(j).getTechPrereq() == i):
					szSpecialBuilding = "SpecialBuildingButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szSpecialBuilding, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, j, False )
					fX += X_INCREMENT

			# Yield change
			for j in xrange( gc.getNumImprovementInfos() ):
				bFound = False
				for k in xrange( YieldTypes.NUM_YIELD_TYPES ):
					if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
						if ( bFound == False ):
							szYieldChange = "YieldChangeButton" + str( ( i * 1000 ) + j )
							screen.addDDSGFCAt( szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False )
							fX += X_INCREMENT
							bFound = True

			# Bonuses revealed
			for j in xrange( gc.getNumBonusInfos() ):
				if (gc.getBonusInfo(j).getTechReveal() == i):
					szBonusReveal = "BonusRevealButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szBonusReveal, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, j, False )
					fX += X_INCREMENT

			# Civic options
			for j in xrange( gc.getNumCivicInfos() ):
				if (gc.getCivicInfo(j).getTechPrereq() == i):
					szCivicReveal = "CivicRevealButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False )
					fX += X_INCREMENT

			# Projects possible
			for j in xrange( gc.getNumProjectInfos() ):
				if (gc.getProjectInfo(j).getTechPrereq() == i):
					szProjectInfo = "ProjectInfoButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
					fX += X_INCREMENT

			# Processes possible
			for j in xrange( gc.getNumProcessInfos() ):
				if (gc.getProcessInfo(j).getTechPrereq() == i):
					szProcessInfo = "ProcessInfoButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szProcessInfo, szTechRecord, gc.getProcessInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, j, False )
					fX += X_INCREMENT

			# Religions unlocked
			for j in xrange( gc.getNumReligionInfos() ):
				if ( gc.getReligionInfo(j).getTechPrereq() == i ):
					szFoundReligion = "FoundReligionButton" + str( ( i * 1000 ) + j )
					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
						szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
					else:
						szButton = gc.getReligionInfo(j).getButton()
					screen.addDDSGFCAt( szFoundReligion, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, j, False )
					fX += X_INCREMENT


			for j in xrange( gc.getNumCorporationInfos() ):
				if ( gc.getCorporationInfo(j).getTechPrereq() == i ):
					szFoundCorporation = "FoundCorporationButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szFoundCorporation, szTechRecord, gc.getCorporationInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, j, False )
					fX += X_INCREMENT

			screen.show( szTechRecord )

		screen.setViewMin( "TechList", iMaxX + 20, iMaxY + 20 )
		screen.show( "TechList" )
		screen.setFocus( "TechList" )


	# Will update the tech records based on color, researching, researched, queued, etc.
	def updateTechRecords (self, bForce):

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		abChanged = [False] * gc.getNumTechInfos()
		bAnyChanged = False
		pPlayer = gc.getPlayer(self.iCivSelected)
		pTeamHasTech = gc.getTeam(pPlayer.getTeam()).isHasTech

		# Go through all the techs
		for i in xrange(gc.getNumTechInfos()):
			if (pTeamHasTech(i)):
				if ( self.aiCurrentState[i] != CIV_HAS_TECH ):
					self.aiCurrentState[i] = CIV_HAS_TECH
					abChanged[i] = True
					bAnyChanged = True
			elif (pPlayer.getCurrentResearch() == i):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = True
					bAnyChanged = True
			elif (pPlayer.isResearchingTech(i)):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = True
					bAnyChanged = True
			elif (pPlayer.canEverResearch(i)):
				if ( self.aiCurrentState[i] != CIV_NO_RESEARCH ):
					self.aiCurrentState[i] = CIV_NO_RESEARCH
					abChanged[i] = 1
					bAnyChanged = True
			else:
				if ( self.aiCurrentState[i] != CIV_TECH_AVAILABLE ):
					self.aiCurrentState[i] = CIV_TECH_AVAILABLE
					abChanged[i] = 1
					bAnyChanged = True

		TechQueueList = []
		iXConst = ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT
		iYConst = BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT
		for i in xrange(gc.getNumTechInfos()):

			if (abChanged[i] or bForce or (bAnyChanged and pPlayer.isResearchingTech(i))):
				# Create and place a tech in its proper location
				szTechRecord = "TechRecord" + str(i)
				szTechID = "TechID" + str(i)
				szTechString = "<font=1>"

				if (pPlayer.isResearchingTech(i)):
					szTechString = szTechString + unicode(pPlayer.getQueuePosition(i)) + ". "

				iX = 36 + (gc.getTechInfo(i).getGridX() - 1) * iXConst + X_INCREMENT
				iY = ( gc.getTechInfo(i).getGridY() - 1 ) * iYConst + 11

				szTechString += gc.getTechInfo(i).getDescription()
				if (pPlayer.isResearchingTech(i)):
					szTechString += " (" + str(pPlayer.getResearchTurnsLeft(i, (pPlayer.getCurrentResearch() == i))) + ")"
				szTechString = szTechString + "</font>"
				screen.setTextAt( szTechID, "TechList", szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
				screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

				if (pTeamHasTech(i)):
					screen.setPanelColor(szTechRecord, 85, 150, 87)
				elif (pPlayer.getCurrentResearch() == i):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif (pPlayer.isResearchingTech(i)):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif (pPlayer.canEverResearch(i)):
					screen.setPanelColor(szTechRecord, 100, 104, 160)
				else:
					screen.setPanelColor(szTechRecord, 206, 65, 69)

			if (pPlayer.isResearchingTech(i)):
				szTechString = "%d. %s(%d)"%(pPlayer.getQueuePosition(i), gc.getTechInfo(i).getDescription(), pPlayer.getResearchTurnsLeft(i, (pPlayer.getCurrentResearch() == i)))
				TechQueueList.append([pPlayer.getQueuePosition(i), szTechString])

		if (pPlayer.getAdvancedStartPoints() < 0):
			TechQueueList.sort()
			FirstTech = True
			szTechQueue = u"<font=1>"
			for item in TechQueueList:
				if (FirstTech):
					szTechQueue +=  "%s: %s"%(localText.getText("TXT_KEY_CGE_TECH_QUEUE", ()), item[1])
					FirstTech = False
				else:
					szTechQueue += " -> %s"%(item[1])
			szTechQueue += "</font>"
			screen.addMultilineText("TechChooserQueue", szTechQueue, 10, 726, self.iPanel_Width - 104, 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	# Will draw the arrows
	def drawArrows (self):

		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		iLoop = 0
		self.nWidgetCount = 0

		ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()

		for i in xrange(gc.getNumTechInfos()):

			fX = (BOX_INCREMENT_WIDTH * PIXEL_INCREMENT) - 8

			for j in xrange( gc.getNUM_AND_TECH_PREREQS() ):

				eTech = gc.getTechInfo(i).getPrereqAndTechs(j)

				if ( eTech > -1 ):

					fX = fX - X_INCREMENT

					iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
					iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5

					szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
					screen.addDDSGFCAt( szTechPrereqID, "TechList", gc.getTechInfo(eTech).getButton(), iX + fX, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

			for j in xrange( gc.getNUM_OR_TECH_PREREQS() ):

				eTech = gc.getTechInfo(i).getPrereqOrTechs(j)

				if ( eTech > -1 ):

					iX = 24 + ( (gc.getTechInfo(eTech).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
					iY = ( gc.getTechInfo(eTech).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5

					# j is the pre-req, i is the tech...
					xDiff = gc.getTechInfo(i).getGridX() - gc.getTechInfo(eTech).getGridX()
					yDiff = gc.getTechInfo(i).getGridY() - gc.getTechInfo(eTech).getGridY()

					iXStart = iX + self.getXStart()
					iXWidth = self.getWidth(xDiff)

					if (yDiff == 0):
						screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(3), iXWidth, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff < 0):
						if ( yDiff == -6 ):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(1), iXWidth / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XY, iXStart + (iXWidth / 2), iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth / 2), iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XMY, iXStart + (iXWidth / 2), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth / 2), iY + self.getYStart(1) - self.getHeight(yDiff, 0), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif ( yDiff == -2 and xDiff == 2 ):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(2), iXWidth * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XY, iXStart + (iXWidth * 5 / 6), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth * 5 / 6), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XMY, iXStart + (iXWidth * 5 / 6), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth * 5 / 6), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(2), iXWidth / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XY, iXStart + (iXWidth / 2), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth / 2), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XMY, iXStart + (iXWidth / 2), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth / 2), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff > 0):
						if ( yDiff == 2 and xDiff == 2):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(4), iXWidth / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXMY, iXStart + (iXWidth / 6), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth / 6), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXY, iXStart + (iXWidth / 6), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth / 6), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) * 5 / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif ( yDiff == 4 and xDiff == 1):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(5), iXWidth / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXMY, iXStart + (iXWidth/ 3 ), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth/ 3 ), iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXY, iXStart + (iXWidth / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), ( self.getWidth(xDiff) * 2 / 3 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart, iY + self.getYStart(4), iXWidth / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXMY, iXStart + (iXWidth / 2), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, iXStart + (iXWidth / 2), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXY, iXStart + (iXWidth / 2), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, iXStart + 8 + (iXWidth / 2), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, iXStart + iXWidth, iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

		return

	def showTechLBPanel(self):
		screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)
		pPlayer = gc.getPlayer(self.iCivSelected)

		screen.addPanel("TechLBPanel", u"", u"", False, True, self.iPanel_Width - 612, 60, 600, 300, PanelStyles.PANEL_STYLE_MAIN)
		screen.setText( "TechLBClose", "TechLBPanel", u"<font=2>OK</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.iPanel_Width - 34, 335, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for (i, flavor) in enumerate(FLAVORS):
			pUnitInfo = gc.getUnitInfo(gc.getUnitClassInfo(gc.getInfoTypeForString(UNIT_CLASSES[i])).getDefaultUnitIndex())
			screen.addDDSGFC("GreatPerson" + str(flavor), pUnitInfo.getButton(), self.iPanel_Width - 592, 120 + i * 40, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)

		prefs = TechPrefs.TechPrefs()

		prefs.removeKnownTechs()

		screen.addScrollPanel("TechLBPanelNextTech", u"", self.iPanel_Width - 509, 70, 490, 240, PanelStyles.PANEL_STYLE_EMPTY)

		lCanResTechs = [iTech for iTech in range(gc.getNumTechInfos()) if pPlayer.canResearch(iTech, False)]
		self.iCanResTech = len(lCanResTechs)
		for (i, iTech) in enumerate(lCanResTechs):
			screen.addDDSGFCAt("GreatPersonResTech" + str(i), "TechLBPanelNextTech", gc.getTechInfo(iTech).getButton(), i * 40, 0, 32, 32, WidgetTypes.WIDGET_TECH_TREE, iTech, -1, False)

		for (i, flavor) in enumerate(FLAVORS):
			szButtonName = "GreatPersonTech" + str(flavor)

			pTech = prefs.getNextResearchableFlavorTech(flavor)
			if (pTech):
				screen.addDDSGFC(szButtonName, pTech.getInfo().getButton(), self.iPanel_Width - 552, 120 + i * 40, 32, 32, WidgetTypes.WIDGET_TECH_TREE, pTech.getID(), -1)
			else:
				screen.addDDSGFC(szButtonName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), self.iPanel_Width - 552, 120 + i * 40, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)

			for (j, iTech) in enumerate(lCanResTechs):
				szName = szButtonName + "_" + str(j)
				pLoopTech = prefs.getNextResearchableWithFlavorTech(flavor, set([prefs.getTech(iTech)]))
				if (pLoopTech):
					screen.addDDSGFCAt(szName, "TechLBPanelNextTech", pLoopTech.getInfo().getButton(), j * 40, 43 + i * 40, 32, 32, WidgetTypes.WIDGET_TECH_TREE, pLoopTech.getID(), -1, False)
				else:
					screen.addDDSGFCAt(szName, "TechLBPanelNextTech", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), j * 40, 43 + i * 40, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

	def hideTechLBPanel(self):
		screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)

		screen.hide("TechLBPanel")
		screen.hide("TechLBPanelNextTech")
		screen.hide("TechLBClose")

		for i in xrange(self.iCanResTech):
			screen.hide("GreatPersonResTech" + str(i))

		for flavor in FLAVORS:
			screen.hide("GreatPerson" + str(flavor))
			szButtonName = "GreatPersonTech" + str(flavor)
			screen.hide(szButtonName)
			for i in xrange(self.iCanResTech):
				screen.hide(szButtonName + "_" + str(i))

		self.iCanResTech = -1

	def TechRecord(self, inputClass):
		return 0

	# Clicked the parent?
	def ParentClick(self, inputClass):
		return 0

	def CivDropDown( self, inputClass ):

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
			iIndex = screen.getSelectedPullDownID("CivDropDown")
			self.iCivSelected = screen.getPullDownData("CivDropDown", iIndex)
			self.updateTechRecords(false)

	# Will handle the input for this screen...
	def handleInput(self, inputClass):

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Advanced Start Stuff

		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):

			# Add tech button
			if (inputClass.getFunctionName() == "AddTechButton"):
				if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iCivSelected, -1, -1, self.m_iSelectedTech, true)	#Action, Player, X, Y, Data, bAdd
					self.m_bTechRecordsDirty = True
					self.m_bSelectedTechDirty = True

			# Tech clicked on
			elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
				if (inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE):
					self.m_iSelectedTech = inputClass.getData1()
					self.updateSelectedTech()

		' Calls function mapped in TechChooserInputMap'
		# only get from the map if it has the key
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			self.CivDropDown( inputClass )
			return 1

		if (inputClass.getFunctionName() == "TechLBButton" and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.showTechLBPanel()
			return 1
		if (inputClass.getFunctionName() == "TechLBClose" and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.hideTechLBPanel()
			return 1

		return 0

	def getNextWidgetName(self):
		szName = "TechArrow" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def getXStart(self):
		return ( BOX_INCREMENT_WIDTH * PIXEL_INCREMENT )

	def getXSpacing(self):
		return ( BOX_INCREMENT_X_SPACING * PIXEL_INCREMENT )

	def getYStart(self, iY):
		return int((((BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ) / 6.0) * iY) - PIXEL_INCREMENT )

	def getWidth(self, xDiff):
		return ( ( xDiff * self.getXSpacing() ) + ( ( xDiff - 1 ) * self.getXStart() ) )

	def getHeight(self, yDiff, nFactor):
		return ( ( nFactor + ( ( abs( yDiff ) - 1 ) * 6 ) ) * PIXEL_INCREMENT )

	def update(self, fDelta):

		if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)

			if (self.m_bSelectedTechDirty):
				self.m_bSelectedTechDirty = False
				self.updateSelectedTech()

			if (self.m_bTechRecordsDirty):
				self.m_bTechRecordsDirty = False
				self.updateTechRecords(True)

			if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() < 0):
				# hide the screen
				screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
				screen.hide("AddTechButton")
				screen.hide("ASPointsLabel")
				screen.hide("SelectedTechLabel")

		return

	def updateSelectedTech(self):
		pPlayer = gc.getPlayer(CyGame().getActivePlayer())

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		szName = ""
		iCost = 0

		if (self.m_iSelectedTech != -1):
			szName = gc.getTechInfo(self.m_iSelectedTech).getDescription()
			iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.m_iSelectedTech, True)

		if iCost > 0:
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_SELECTED_TECH_COST", (iCost, pPlayer.getAdvancedStartPoints())) + u"</font>"
			screen.setLabel( "ASPointsLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.hide("ASPointsLabel")

		szText = u"<font=4>"
		szText += localText.getText("TXT_KEY_WB_AS_SELECTED_TECH", (szName,))
		szText += u"</font>"
		screen.setLabel( "SelectedTechLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT + 250, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Want to add
		if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, True) != -1):
			screen.show("AddTechButton")
		else:
			screen.hide("AddTechButton")

	def onClose(self):
		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, True)
		return 0

class TechChooserMaps:

	TechChooserInputMap = {
		'TechRecord'			: CvTechChooser().TechRecord,
		'TechID'				: CvTechChooser().ParentClick,
		'TechPane'				: CvTechChooser().ParentClick,
		'TechButtonID'			: CvTechChooser().ParentClick,
		'TechButtonBorder'		: CvTechChooser().ParentClick,
		'Unit'					: CvTechChooser().ParentClick,
		'Building'				: CvTechChooser().ParentClick,
		'Obsolete'				: CvTechChooser().ParentClick,
		'ObsoleteX'				: CvTechChooser().ParentClick,
		'Move'					: CvTechChooser().ParentClick,
		'FreeUnit'				: CvTechChooser().ParentClick,
		'FeatureProduction'		: CvTechChooser().ParentClick,
		'Worker'				: CvTechChooser().ParentClick,
		'TradeRoutes'			: CvTechChooser().ParentClick,
		'HealthRate'			: CvTechChooser().ParentClick,
		'HappinessRate'			: CvTechChooser().ParentClick,
		'FreeTech'				: CvTechChooser().ParentClick,
		'LOS'					: CvTechChooser().ParentClick,
		'MapCenter'				: CvTechChooser().ParentClick,
		'MapReveal'				: CvTechChooser().ParentClick,
		'MapTrade'				: CvTechChooser().ParentClick,
		'TechTrade'				: CvTechChooser().ParentClick,
		'OpenBorders'			: CvTechChooser().ParentClick,
		'BuildBridge'			: CvTechChooser().ParentClick,
		'Irrigation'			: CvTechChooser().ParentClick,
		'Improvement'			: CvTechChooser().ParentClick,
		'DomainExtraMoves'		: CvTechChooser().ParentClick,
		'AdjustButton'			: CvTechChooser().ParentClick,
		'TerrainTradeButton'	: CvTechChooser().ParentClick,
		'SpecialBuildingButton'	: CvTechChooser().ParentClick,
		'YieldChangeButton'		: CvTechChooser().ParentClick,
		'BonusRevealButton'		: CvTechChooser().ParentClick,
		'CivicRevealButton'		: CvTechChooser().ParentClick,
		'ProjectInfoButton'		: CvTechChooser().ParentClick,
		'ProcessInfoButton'		: CvTechChooser().ParentClick,
		'FoundReligionButton'	: CvTechChooser().ParentClick,
		'CivDropDown'			: CvTechChooser().CivDropDown,
		}
