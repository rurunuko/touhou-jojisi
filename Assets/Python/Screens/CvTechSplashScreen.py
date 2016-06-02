#---changes by SirRethcir: Techanzeige hinzugef・t
## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import string

gc = CyGlobalContext()
localText = CyTranslator()

class CvTechSplashScreen:
	"Splash screen for techs"
	def __init__(self, iScreenID):
		self.nScreenId = iScreenID

		self.iTech = -1
		self.nWidgetCount = 0

		# widget names
		self.WIDGET_ID = "TechSplashScreenWidget"
		self.SCREEN_NAME = "TechSplashScreen"
		self.EXIT_ID = "TechSplashExit"

		self.X_SCREEN = 17
		self.Y_SCREEN = 27
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Z_BACKGROUND = -1.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.Z_HELP_AREA = self.Z_CONTROLS - 2
		self.W_HELP_AREA = 200

		# Panels
		self.iMarginSpace = 15

		self.X_MAIN_PANEL = 17
		self.Y_MAIN_PANEL = 55
		self.W_MAIN_PANEL = 996
		self.H_MAIN_PANEL = 670

		# Upper Panel
		self.X_UPPER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_UPPER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_UPPER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_UPPER_PANEL = 320

		self.X_TITLE = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2)
		self.Y_TITLE = self.Y_UPPER_PANEL + 14

		self.W_ICON = 128
		self.H_ICON = 128

		self.X_ICON_PANEL = self.X_UPPER_PANEL + self.iMarginSpace + 2
		self.Y_ICON_PANEL = self.Y_UPPER_PANEL + self.iMarginSpace + 33
		self.W_ICON_PANEL = 140
		self.H_ICON_PANEL = 135

		self.X_ICON = self.X_ICON_PANEL + self.W_ICON_PANEL / 2 - self.W_ICON / 2 + 10
		self.Y_ICON = self.Y_ICON_PANEL + self.H_ICON_PANEL / 2 - self.H_ICON / 2 + 12

		self.X_QUOTE = self.X_UPPER_PANEL + self.W_ICON_PANEL + (self.iMarginSpace * 2)
		self.Y_QUOTE = self.Y_ICON_PANEL
		self.W_QUOTE = 790
		self.H_QUOTE = self.H_UPPER_PANEL - (self.Y_QUOTE - self.Y_UPPER_PANEL) - (self.iMarginSpace * 2)

#---Ge舅dert START - siehe original Datei -----------------
		# Lower Panel
		self.X_LOWER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_LOWER_PANEL = self.Y_UPPER_PANEL + self.H_UPPER_PANEL
		self.W_LOWER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_LOWER_PANEL = 330

		self.X_SPECIAL_PANEL = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_SPECIAL_PANEL = self.Y_LOWER_PANEL + self.iMarginSpace + 20
		self.W_SPECIAL_PANEL = self.W_LOWER_PANEL/2 - self.iMarginSpace
		self.H_SPECIAL_PANEL = int(self.H_LOWER_PANEL / 2.5)

		self.X_ALLOWS_PANELSIR = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_ALLOWS_PANELSIR = self.Y_SPECIAL_PANEL + self.H_SPECIAL_PANEL+ self.iMarginSpace + 13
		self.W_ALLOWS_PANELSIR = self.W_LOWER_PANEL/2 - (self.iMarginSpace)
		self.H_ALLOWS_PANELSIR = 80

		self.X_ALLOWS_PANEL = self.X_LOWER_PANEL + self.iMarginSpace + self.W_SPECIAL_PANEL
		self.Y_ALLOWS_PANEL = self.Y_SPECIAL_PANEL
		self.W_ALLOWS_PANEL = self.W_LOWER_PANEL/2 - (self.iMarginSpace)
		self.H_ALLOWS_PANEL = 80
		self.Y_ALLOWS_PANEL2 = self.Y_SPECIAL_PANEL + self.H_ALLOWS_PANEL
		self.Y_ALLOWS_PANEL3 = self.Y_SPECIAL_PANEL + self.H_ALLOWS_PANEL*2
#---Ge舅dert ENDE ------------------------------------------

		# Contents
		self.X_EXIT = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2) - 55
		self.Y_EXIT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL - 45
		self.W_EXIT = 120
		self.H_EXIT = 30

	def interfaceScreen(self, iTech):
		self.nTechs = gc.getNumTechInfos()
		self.iTech = iTech
		self.nWidgetCount = 0

		# Create screen

		screen = self.getScreen()

		techInfo = gc.getTechInfo(self.iTech)

		screen.setSound(techInfo.getSound())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds(False)

		screen.showWindowBackground(False)
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		# Create panels

		# Main Panel
		szMainPanel = "TechSplashMainPanel"
		screen.addPanel(szMainPanel, "", "", True, True, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN)

		# Top Panel
		szHeaderPanel = "TechSplashHeaderPanel"
		screen.addPanel(szHeaderPanel, "", "", True, True, self.X_UPPER_PANEL, self.Y_UPPER_PANEL, self.W_UPPER_PANEL, self.H_UPPER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM)
		screen.setStyle(szHeaderPanel, "Panel_DawnBottom_Style")

		# Icon Panel
		szIconPanel = "IconPanel"
		screen.addPanel(szIconPanel, "", "", True, True, self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_UPPER_PANEL-(self.iMarginSpace * 2), self.H_UPPER_PANEL-(self.iMarginSpace * 4), PanelStyles.PANEL_STYLE_MAIN_TAN15)
		screen.setStyle(szIconPanel, "Panel_TechDiscover_Style")

		# Icon Panel
		szIconPanel = "IconPanelGlow"
		screen.addPanel(szIconPanel, "", "", True, True, self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_ICON_PANEL, self.H_ICON_PANEL, PanelStyles.PANEL_STYLE_MAIN_TAN15)
		screen.setStyle(szIconPanel, "Panel_TechDiscoverGlow_Style")

		# Bottom Panel
		szTextPanel = "TechSplashTextPanel"
		screen.addPanel(szTextPanel, "", "", True, True, self.X_LOWER_PANEL+self.iMarginSpace, self.Y_LOWER_PANEL, self.W_LOWER_PANEL-(self.iMarginSpace * 2), self.H_LOWER_PANEL, PanelStyles.PANEL_STYLE_MAIN)
		screen.setStyle(szTextPanel, "Panel_TanT_Style")

		# Exit Button
		screen.setButtonGFC("Exit", localText.getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Special Panel
		szSpecialPanel = "TechSplashSpecialPanel"
		screen.addPanel(szSpecialPanel, "", "", True, True, self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL, self.W_SPECIAL_PANEL-(self.iMarginSpace * 2), self.H_SPECIAL_PANEL, PanelStyles.PANEL_STYLE_IN)
		screen.setStyle(szSpecialPanel, "Panel_Black25_Style")

#---Eingef・t START - kann komplett gelcht werden-----------------
		# Allows PanelSIR
		panelNameSIR = "SIR"
		screen.addPanel(panelNameSIR, "", "", False, True, self.X_ALLOWS_PANELSIR+self.iMarginSpace, self.Y_ALLOWS_PANELSIR, self.W_ALLOWS_PANELSIR-(self.iMarginSpace * 2), self.H_ALLOWS_PANELSIR, PanelStyles.PANEL_STYLE_IN)
		screen.setStyle(panelNameSIR, "Panel_Black25_Style")
#---Eingef・t ENDE -------------------------------------------------

		# Allows Panel
		panelName = self.getNextWidgetName()
		screen.addPanel(panelName, "", "", False, True, self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelName, "Panel_Black25_Style")

#---Eingef・t START - kann komplett gelcht werden-----------------
		# Allows Panel2
		panelName2 = "SIR2"
		screen.addPanel(panelName2, "", "", False, True, self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL2, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN)
		screen.setStyle(panelName2, "Panel_Black25_Style")

		# Allows Panel3
		panelName3 = "SIR3"
		screen.addPanel(panelName3, "", "", False, True, self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL3, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN)
		screen.setStyle(panelName3, "Panel_Black25_Style")
#---Eingef・t ENDE -------------------------------------------------

		# Add Contents

		# Title
		szTech = techInfo.getDescription()
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>%s</font>"%(szTech.upper()), CvUtil.FONT_CENTER_JUSTIFY,self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Tech Icon
		screen.addDDSGFC(self.getNextWidgetName(), techInfo.getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, self.iTech, -1)

		# Tech Quote
		screen.addMultilineText("Text", techInfo.getQuote() + "\n\n" + techInfo.getCivilopedia(), self.X_QUOTE, self.Y_QUOTE + self.iMarginSpace*2, self.W_QUOTE - (self.iMarginSpace * 2), self.H_QUOTE - (self.iMarginSpace * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		# Special
		szSpecialTitle = u"<font=3b>%s</font>"%(localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()))
		szSpecialTitleWidget = "SpecialTitle"
		screen.setText(szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		listName = self.getNextWidgetName()

		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, True, -1)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANEL+10, self.Y_SPECIAL_PANEL+5, self.W_SPECIAL_PANEL-20, self.H_SPECIAL_PANEL-20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

#---Eingef・t START - kann komplett gelcht werden --------------
		# Allows -> LeadsTo
		szAllowsTitleDescSIR = u"<font=3b>%s:</font>"%(localText.getText("TXT_KEY_PEDIA_LEADS_TO", ()))
		szAllowsTitleWidgetSIR = "AllowsTitleSIR"
		screen.setText(szAllowsTitleWidgetSIR, "", szAllowsTitleDescSIR, CvUtil.FONT_LEFT_JUSTIFY, self.X_ALLOWS_PANELSIR+self.iMarginSpace, self.Y_ALLOWS_PANELSIR - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iNumOrPrereq = gc.getDefineINT("NUM_OR_TECH_PREREQS")
		iNumAndPrereq = gc.getDefineINT("NUM_AND_TECH_PREREQS")
		for j in xrange(gc.getNumTechInfos()):
			TechInfo = gc.getTechInfo(j)
			for k in xrange(iNumOrPrereq):
				iPrereq = TechInfo.getPrereqOrTechs(k)
				if (iPrereq == self.iTech):
					screen.attachCheckBoxGFC(panelNameSIR, "", TechInfo.getButton(), "", 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, ButtonStyles.BUTTON_STYLE_IMAGE)
			for k in xrange(iNumAndPrereq):
				iPrereq = TechInfo.getPrereqAndTechs(k)
				if (iPrereq == self.iTech):
					screen.attachCheckBoxGFC(panelNameSIR, "", TechInfo.getButton(), "", 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, ButtonStyles.BUTTON_STYLE_IMAGE)

#---Eingef・t ENDE ------------------------------------------------
		# Allows
		szAllowsTitleDesc = u"<font=3b>%s:</font>"%(localText.getText("TXT_KEY_PEDIA_ALLOWS", ()))
		szAllowsTitleWidget = "AllowsTitle"
		screen.setText(szAllowsTitleWidget, "", szAllowsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY, self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		CivInfo = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType())
		for j in xrange(gc.getNumUnitClassInfos()):
			eLoopUnit = CivInfo.getCivilizationUnits(j)
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit)):
					screen.attachImageButton(panelName, "", gc.getActivePlayer().getUnitButton(eLoopUnit), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False)

		for j in xrange(gc.getNumBuildingClassInfos()):
			eLoopBuilding = CivInfo.getCivilizationBuildings(j)
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding)):
					screen.attachImageButton(panelName2, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False)

		for j in xrange(gc.getNumProjectInfos()):
			if (isTechRequiredForProject(self.iTech, j)):
				screen.attachImageButton(panelName3, "", gc.getProjectInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False)

		for j in xrange(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(j).getTechPrereq() == self.iTech):
				screen.attachImageButton(panelName3, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False)

#---Eingef・t START - kann komplett gelcht werden --------------

		# Improvements
		iNumFreture = gc.getNumFeatureInfos()
		for j in xrange(gc.getNumBuildInfos()):
			bTechFound = False
			BuildInfo = gc.getBuildInfo(j)
			if (BuildInfo.getTechPrereq() == -1):
				for k in xrange(iNumFreture):
					if (BuildInfo.getFeatureTech(k) == self.iTech):
						bTechFound = True
						break
			else:
				if (BuildInfo.getTechPrereq() == self.iTech):
					bTechFound = True

			if (bTechFound):
				if (BuildInfo.getImprovement() == -1):
					screen.attachImageButton(panelName3, "", BuildInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IMPROVEMENT, j, 1, False)
				else:
					screen.attachImageButton(panelName3, "", BuildInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, BuildInfo.getImprovement(), 1, False)

		# Bonuses
		for j in xrange(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(j).getTechReveal() == self.iTech):
				screen.attachImageButton(panelName3, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, j, 1, False)

		# Civic
		for j in xrange(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(j).getTechPrereq() == self.iTech):
				screen.attachCheckBoxGFC(panelName3, "", gc.getCivicInfo(j).getButton(), "", 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, j, 1, ButtonStyles.BUTTON_STYLE_IMAGE)
#---Eingef・t ENDE ------------------------------------------------

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount * self.nTechs + self.iTech)
		self.nWidgetCount += 1
		return szName

	# returns a unique ID for this screen
	def getScreen(self):
		screen = CyGInterfaceScreen(self.SCREEN_NAME + str(self.iTech), self.nScreenId)
		return screen

	def handleInput(self, inputClass):
		if (inputClass.getData() == int(InputTypes.KB_RETURN)):
			self.getScreen().hideScreen()
			return 1
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.EXIT_ID):
				self.getScreen().hideScreen()
			return 1
		return 0

	def update(self, fDelta):
		return
