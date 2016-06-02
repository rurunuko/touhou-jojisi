# Alerts Log Panel
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums
import re
import CvConfigParser

ArtFileMgr = CyArtFileMgr()

# globals
gc = CyGlobalContext()
localText = CyTranslator()

AlertLogEventList = []
AlertLogButtonNotify = 10
removeColor = re.compile(r'<color=.*?>|</color>')
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
AlertMessageTime1 = config.getint("Alerts Log", "Level1 Alert Message Time", 4)
AlertMessageTime2 = config.getint("Alerts Log", "Level2 Alert Message Time", 4)
AlertMessageTime3 = config.getint("Alerts Log", "Level3 Alert Message Time", 4)

class AlertsLog:

	def __init__(self):
		self.EXIT_NAME = "AlertsLogExit"
		self.BACKGROUND = "AlertsLogBackground"
		self.RED_BUTTON = "AlertsLogRedButton"
		self.YELLOW_BUTTON = "AlertsLogYellowButton"
		self.GREEN_BUTTON = "AlertsLogGreenButton"
		self.ALERTS_LOG_TEXT = "AlertsLogText"

		self.X_TEXT = 20
		self.Y_TEXT = 100
		self.W_TEXT = 600
		self.H_TEXT = 320
		self.X_EXIT = 600
		self.Y_EXIT = 440

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 640
		self.H_SCREEN = 480
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2

	def AlertsLogMessage(self, ePlayer, szString, szIcon, iColor, iFlashX, iFlashY, iLevel, iCityID, iLeaderID, bOffArrow, bOnArrow):
		global AlertLogEventList
		global AlertLogButtonNotify

		AlertLogEventList.append((iLevel, iCityID, iLeaderID, szString))

		if (iLevel == 1):
			iTime = AlertMessageTime1 * 5
		elif (iLevel == 2):
			iTime = AlertMessageTime2 * 5
		elif (iLevel == 3):
			iTime = AlertMessageTime3 * 5
		CyInterface().addMessage(ePlayer, True, iTime, szString, None, 0, szIcon, iColor, iFlashX, iFlashY, bOffArrow, bOnArrow)

		if (AlertLogButtonNotify > iLevel):
			CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).changeImageButton("AlertsLogButton1", "Art/Interface/Buttons/AlertsLog" + str(iLevel) + ".dds")
			AlertLogButtonNotify = iLevel

	def AlertsLogStartTurn(self):
		global AlertLogEventList
		global AlertLogButtonNotify

		AlertLogEventList = []

		if (AlertLogButtonNotify):
			CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).changeImageButton("AlertsLogButton1", "Art/Interface/Buttons/AlertsLog.dds")
		AlertLogButtonNotify = 10

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("AlertsLogScreen", CvScreenEnums.ALERTS_LOG_SCREEN)
		if (screen.isActive()):
			return

		screen.setRenderInterfaceOnly(False)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"

		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel("TechBottomPanel", u"", u"", True, False, 0, 425, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		# Header...
		screen.setText("AlertsLogTitle", "Background", u"<font=4b>ALERTS LOG</font>", CvUtil.FONT_CENTER_JUSTIFY, 320, 8, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel("AlertsButtonPanel", u"", u"", True, False, 50, 56, 128, 43, PanelStyles.PANEL_STYLE_OUT)
		screen.setText("AlertsButtonPanelText", "Background", "Alert Level", CvUtil.FONT_LEFT_JUSTIFY, 55, 48, self.Z_CONTROLS, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addCheckBoxGFC(self.RED_BUTTON, "Art/Interface/Buttons/AlertsLogR.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 58, 66, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.addCheckBoxGFC(self.YELLOW_BUTTON, "Art/Interface/Buttons/AlertsLogY.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 98, 66, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.addCheckBoxGFC(self.GREEN_BUTTON, "Art/Interface/Buttons/AlertsLogG.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 138, 66, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setState(self.RED_BUTTON, False)
		screen.setState(self.YELLOW_BUTTON, False)
		screen.setState(self.GREEN_BUTTON, False)

		bLevel1 = False
		bLevel2 = False
		bLevel3 = False
		for item in AlertLogEventList:
			iLoopLevel = item[0]
			if (iLoopLevel == 1):
				bLevel1 = True
			elif (iLoopLevel == 2):
				bLevel2 = True
			elif (iLoopLevel == 3):
				bLevel3 = True

		screen.enable(self.RED_BUTTON, bLevel1)
		screen.enable(self.YELLOW_BUTTON, bLevel2)
		screen.enable(self.GREEN_BUTTON, bLevel3)

		# Alerts Log Text
		screen.addListBoxGFC(self.ALERTS_LOG_TEXT, "", self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.ALERTS_LOG_TEXT, True)

		iLevel = 0
		if (bLevel1):
			iLevel = 1
			screen.setState(self.RED_BUTTON, True)
		elif (bLevel2):
			iLevel = 2
			screen.setState(self.YELLOW_BUTTON, True)
		elif (bLevel3):
			iLevel = 3
			screen.setState(self.GREEN_BUTTON, True)

		self.ShowAlertLogText(iLevel)

	def ShowAlertLogText(self, iLevel):
		screen = CyGInterfaceScreen("AlertsLogScreen", CvScreenEnums.ALERTS_LOG_SCREEN)

		screen.clearListBoxGFC(self.ALERTS_LOG_TEXT)

		bLevel1 = False
		bLevel2 = False
		bLevel3 = False
		for item in AlertLogEventList:
			if (item[0] == iLevel):
				szAlertText = unichr(CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + removeColor.sub("", item[3])
				if (item[1] != -1):
					szCityName = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(item[1]).getName()
					szAlertText = szAlertText.replace(szCityName, "<color=255,0,0>" + szCityName + "</color>")
					screen.appendListBoxStringNoUpdate(self.ALERTS_LOG_TEXT, szAlertText, WidgetTypes.WIDGET_ZOOM_CITY, gc.getPlayer(gc.getGame().getActivePlayer()).getCity(item[1]).getOwner(), item[1], CvUtil.FONT_LEFT_JUSTIFY)
				elif (item[2] != -1):
					szCivName = gc.getPlayer(item[2]).getName()
					szAlertText = szAlertText.replace(szCivName, "<color=255,0,0>" + szCivName + "</color>")
					screen.appendListBoxStringNoUpdate(self.ALERTS_LOG_TEXT, szAlertText, WidgetTypes.WIDGET_CONTACT_CIV, item[2], -1, CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.appendListBoxStringNoUpdate(self.ALERTS_LOG_TEXT, szAlertText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(self.ALERTS_LOG_TEXT)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("AlertsLogScreen", CvScreenEnums.ALERTS_LOG_SCREEN)
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.RED_BUTTON):
				screen.setState(self.RED_BUTTON, True)
				screen.setState(self.YELLOW_BUTTON, False)
				screen.setState(self.GREEN_BUTTON, False)
				self.ShowAlertLogText(1)
				return 1
			elif (inputClass.getFunctionName() == self.YELLOW_BUTTON):
				screen.setState(self.RED_BUTTON, False)
				screen.setState(self.YELLOW_BUTTON, True)
				screen.setState(self.GREEN_BUTTON, False)
				self.ShowAlertLogText(2)
				return 1
			elif (inputClass.getFunctionName() == self.GREEN_BUTTON):
				screen.setState(self.RED_BUTTON, False)
				screen.setState(self.YELLOW_BUTTON, False)
				screen.setState(self.GREEN_BUTTON, True)
				self.ShowAlertLogText(3)
				return 1
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getData1() != -1):
				screen.hideScreen()
				if (inputClass.getData2() != -1):
					CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True)
				#else:
				#	gc.getPlayer(gc.getGame().getActivePlayer()).contact(inputClass.getData1())
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showAlertsLogScreen")
					popupInfo.addPopup(inputClass.getData1())
		return 0

	def update(self, fDelta):
		return

	def setCGEOption(self, Section, Key, Value):
		global AlertMessageTime1
		global AlertMessageTime2
		global AlertMessageTime3

		if (Key == 'Level1 Alert Message Time'):
			AlertMessageTime1 = Value
		elif (Key == 'Level2 Alert Message Time'):
			AlertMessageTime2 = Value
		elif (Key == 'Level3 Alert Message Time'):
			AlertMessageTime3 = Value
