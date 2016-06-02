# Unit Placements Screen
# This file is a part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import ScreenInput
import CvScreenEnums
import ScreenInput
import CvUtil
import UnitPlacement

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvUnitPlacementScreen:

	def __init__(self):

		self.SCREEN_NAME = "UnitPlacementScreen"
		self.BACKGROUND = "UnitPlacementBackground"
		self.TITLE_NAME = "UnitPlacementTitleHeader"
		self.EXIT_NAME = "UnitPlacementExit"
		self.CITYLIST = "UnitPlacementCityList"
		self.SETORDER = "UnitPlacementSetOrder"
		self.UNITLIST = "UnitPlacementUnitList"
		self.UNITQUEUE = "UnitPlacementUnitQueue"
		self.UNITQUEUELOOP = "UnitPlacementSetOrderLoop"
		self.SETORDERUNITLIST = "UnitPlacementSetOrderUnitList"
		self.SETORDERDESTLIST = "UnitPlacementSetOrderDestList"
		self.SETORDERUNITNUM = "UnitPlacementSetOrderUnitNum"
		self.SETORDERAUTOFORTIFY = "UnitPlacementSetOrderAutoFortify"
		self.SETORDERDELETE = "UnitPlacementSetOrderDelete"
		self.SETORDERADD = "UnitPlacementSetOrderAdd"
		self.SETORDERMODIFY = "UnitPlacementSetOrderModify"
		self.SETORDERUP = "UnitPlacementSetOrderUp"
		self.SETORDERDOWN = "UnitPlacementSetOrderDown"

		self.MaxUnitNum = 30

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.X_CANCEL = 552
		self.Y_CANCEL = 726

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.Y_TITLE = 8

		self.X_CITY_LIST = 10
		self.Y_CITY_LIST = 60
		self.W_CITY_LIST = 200
		self.H_CITY_LIST = 650

		self.X_UNIT_LIST = 230
		self.Y_UNIT_LIST = self.Y_CITY_LIST
		self.W_UNIT_LIST = 250
		self.H_UNIT_LIST = 430

		self.X_UNIT_QUEUE = 500
		self.Y_UNIT_QUEUE = self.Y_CITY_LIST
		self.W_UNIT_QUEUE = self.W_SCREEN - self.X_UNIT_QUEUE - 20
		self.H_UNIT_QUEUE = 475

		self.X_SET_ORDER = self.X_UNIT_QUEUE
		self.Y_SET_ORDER = 555#510
		self.W_SET_ORDER = self.W_SCREEN - self.X_SET_ORDER - 20
		self.H_SET_ORDER = 155#200

		self.X_MINIMAP = self.X_UNIT_LIST
		self.Y_MINIMAP = 510
		self.W_MINIMAP = self.W_UNIT_LIST
		self.H_MINIMAP = 200

		self.start = None
		self.dest = None
		self.currentCity = None
		self.lUnitListIndex = []
		self.currentUnit = -1
		self.currentOrderNum = -1

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.UNIT_PLACEMENTS_SCREEN)

	def interfaceScreen(self):
		screen = self.getScreen()
		if (screen.isActive()):
			return

		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"

		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setText(self.TITLE_NAME, "Background", u"<font=4b>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_SCREEN_TITLE", ()).upper()), CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# unit list panel
		screen.addPanel(self.UNITLIST + "Background", "", "", True, True, self.X_UNIT_LIST, self.Y_UNIT_LIST, self.W_UNIT_LIST, self.H_UNIT_LIST, PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel("", self.BACKGROUND,  u"<font=3>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_UNIT_LIST", ())), CvUtil.FONT_CENTER_JUSTIFY, self.X_UNIT_LIST + self.W_UNIT_LIST/2, self.Y_UNIT_LIST + 15, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# unit queue panel
		screen.addPanel(self.UNITQUEUE + "Background", "", "", True, True, self.X_UNIT_QUEUE, self.Y_UNIT_QUEUE, self.W_UNIT_QUEUE, self.H_UNIT_QUEUE, PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel("", self.BACKGROUND,  u"<font=3>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_UNIT_QUEUE", ())), CvUtil.FONT_CENTER_JUSTIFY, self.X_UNIT_QUEUE + self.W_UNIT_QUEUE/2, self.Y_UNIT_QUEUE + 15, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# unit queue loop checkbox
		screen.addCheckBoxGFC(self.UNITQUEUELOOP, "Art/Interface/Buttons/unchecked.dds", "", self.X_UNIT_QUEUE +30, self.Y_UNIT_QUEUE + self.H_UNIT_QUEUE - 40, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setText(self.UNITQUEUELOOP + "Text", "Background", localText.getText("TXT_KEY_UNIT_PLACEMENT_LOOP", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_UNIT_QUEUE + 60, self.Y_UNIT_QUEUE + self.H_UNIT_QUEUE - 37, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Up Button
		screen.setImageButton(self.SETORDERUP, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_UPARROW").getPath(), self.X_UNIT_QUEUE + 420, self.Y_UNIT_QUEUE + self.H_UNIT_QUEUE - 40, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# Down Button
		screen.setImageButton(self.SETORDERDOWN, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_DOWNARROW").getPath(), self.X_UNIT_QUEUE + 450, self.Y_UNIT_QUEUE + self.H_UNIT_QUEUE - 40, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.enable(self.SETORDERUP, False)
		screen.enable(self.SETORDERDOWN, False)

		# set order panel
		screen.addPanel(self.SETORDER + "Background", "", "", True, True, self.X_SET_ORDER, self.Y_SET_ORDER, self.W_SET_ORDER, self.H_SET_ORDER, PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel("", self.BACKGROUND,  u"<font=3>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_SET_ORDER", ())), CvUtil.FONT_CENTER_JUSTIFY, self.X_SET_ORDER + self.W_SET_ORDER/2, self.Y_SET_ORDER + 15, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Minimap panel
		screen.addPanel( "", u"", "", False, False, self.X_MINIMAP, self.Y_MINIMAP, self.W_MINIMAP, self.H_MINIMAP, PanelStyles.PANEL_STYLE_MAIN )
		self.initMinimap()

		self.showCityList()

		UnitPlacement.UnitPlacement().PurgeOrderList()

	def initMinimap(self):
		screen = self.getScreen()

		screen.initMinimap( self.X_MINIMAP + 20, self.X_MINIMAP + self.W_MINIMAP - 20, self.Y_MINIMAP + 20, self.Y_MINIMAP + self.H_MINIMAP - 20, self.Z_CONTROLS)

		screen.updateMinimapSection(False, False)

		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

	def refreshMinimap(self):
		screen = self.getScreen()
		screen.minimapClearAllFlashingTiles()

		iColorStart = gc.getInfoTypeForString("COLOR_GREEN")
		iColorDest = gc.getInfoTypeForString("COLOR_RED")

		if (self.start != None):
			screen.minimapFlashPlot(self.start[0], self.start[1], iColorStart, -1)
		if (self.dest != None):
			screen.minimapFlashPlot(self.dest[0], self.dest[1], iColorDest, -1)

	def showCityList(self):

		screen = self.getScreen()

		screen.addPanel(self.CITYLIST + "Background", "", "", True, True, self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel("", self.BACKGROUND,  u"<font=3>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_CITY_LIST", ())), CvUtil.FONT_CENTER_JUSTIFY, self.X_CITY_LIST + 100, self.Y_CITY_LIST + 15, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.addListBoxGFC(self.CITYLIST, "", self.X_CITY_LIST +20, self.Y_CITY_LIST +40, self.W_CITY_LIST -40, self.H_CITY_LIST -60, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.CITYLIST, True)
		screen.setStyle(self.CITYLIST, "Table_StandardCiv_Style")

		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		(pLoopCity, iter) = pActivePlayer.firstCity(False)
		while (pLoopCity):
			screen.appendListBoxStringNoUpdate(self.CITYLIST, u"<font=3>%s</font>"%(pLoopCity.getName()), WidgetTypes.WIDGET_GENERAL, pLoopCity.getID(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

		screen.appendListBoxStringNoUpdate(self.CITYLIST, u"<font=3>%s</font>"%(localText.getText("TXT_KEY_UNIT_PLACEMENT_ALL_CITIES", ())), WidgetTypes.WIDGET_GENERAL, UnitPlacement.gAllCityID, UnitPlacement.gAllCityID, CvUtil.FONT_LEFT_JUSTIFY )
		screen.updateListBox(self.CITYLIST)

	def showCityQueue(self, iCityID):
		screen = self.getScreen()

		screen.addTableControlGFC(self.UNITLIST, 1, self.X_UNIT_LIST + 20, self.Y_UNIT_LIST + 40, self.W_UNIT_LIST - 40, self.H_UNIT_LIST - 60, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.UNITLIST, True)
		screen.setStyle(self.UNITLIST, "Table_StandardCiv_Style")
		screen.setTableColumnHeader(self.UNITLIST, 0, "", self.W_UNIT_LIST - 40)

		CityOrder = UnitPlacement.UnitPlacement().getCityOrder(iCityID)
		self.lUnitListIndex = []
		for iLoopUnit in CityOrder:
			iRow = screen.appendTableRow(self.UNITLIST)
			if (iLoopUnit == UnitPlacement.gAllUnitID):
				szUnitName = localText.getText("TXT_KEY_UNIT_PLACEMENT_ALL_UNITS", ())
				szButtonFile = ""
			else:
				szUnitName = gc.getUnitInfo(iLoopUnit).getText()
				szButtonFile = gc.getUnitInfo(iLoopUnit).getButton()
			screen.setTableText(self.UNITLIST, 0, iRow, u"<font=3>%s</font>"%(szUnitName), szButtonFile, WidgetTypes.WIDGET_GENERAL, iLoopUnit, iLoopUnit, CvUtil.FONT_LEFT_JUSTIFY)
			self.lUnitListIndex.append(iLoopUnit)
			#CvUtil.pyPrint("showCityQueue: " + gc.getUnitInfo(iUnit).getText() + str(iUnit))

		self.showSetOrder(iCityID)
		self.showUnitQueueHeader()
		if (iCityID != UnitPlacement.gAllCityID):
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(iCityID)
			self.start = (pCity.getX(), pCity.getY())
		else:
			self.start = None

	def showUnitQueueHeader(self):
		screen = self.getScreen()

		screen.addTableControlGFC(self.UNITQUEUE, 5, self.X_UNIT_QUEUE + 20, self.Y_UNIT_QUEUE + 40, self.W_UNIT_QUEUE - 40, self.H_UNIT_QUEUE - 90, True, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(self.UNITQUEUE, 0, "#", 40)
		screen.setTableColumnHeader(self.UNITQUEUE, 1, localText.getText("TXT_KEY_UNIT_PLACEMENT_DESTINATION", ()), 300)
		screen.setTableColumnHeader(self.UNITQUEUE, 2, localText.getText("TXT_KEY_UNIT_PLACEMENT_AUTO_FORTIFY_HEAD", ()), 44)
		screen.setTableColumnHeader(self.UNITQUEUE, 3, localText.getText("TXT_KEY_UNIT_PLACEMENT_NUM_OF_UNITS", ()), 80)
		screen.setStyle(self.UNITQUEUE, "Table_StandardCiv_Style")
		screen.enableSelect(self.UNITQUEUE, True)

	def showUnitQueue(self, iCityID, iUnit):
		screen = self.getScreen()

		self.showUnitQueueHeader()

		# Debug Info
		#szText = "SelectedCity: " + pCity.getName() + str(iUnit)
		#screen.setText("UPTestString", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 100, 10, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		UnitList = UnitPlacement.UnitPlacement().getUnitList(iCityID, iUnit)
		DestDict = UnitPlacement.UnitPlacement().getSignDict()
		iLoopPos = 1
		for item in UnitList:
			if (DestDict.has_key(item[0])):
				tDest = DestDict.get(item[0])
				szDestName = tDest[2]
				if (iCityID == item[0]):
					szDestName = localText.getText("TXT_KEY_UNIT_PLACEMENT_STAY_HERE", ())
			else:
				szDestName = "<color=255,0,0>Not Available Destination</color>"
				UnitPlacement.UnitPlacement().deleteOrder(self.currentCity, iUnit, iLoopPos - 1)
				continue
			iLoopNum = item[1]
			iLoopCounter = item[2]
			if (iLoopNum == 0):
				szLoopNum = "*"
			elif (iLoopNum == iLoopCounter):
				 szLoopNum = str(iLoopNum)
			else:
				szLoopNum = "%d/%d"%(iLoopCounter, iLoopNum)
			if (item[3]):
				szFortify = u"On"
			else:
				szFortify = u"Off"
			iRow = screen.appendTableRow(self.UNITQUEUE)
			screen.setTableText(self.UNITQUEUE, 0, iRow, u"<font=3>%s</font>"%(iLoopPos), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableText(self.UNITQUEUE, 1, iRow, u"<font=3>%s</font>"%(szDestName), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(self.UNITQUEUE, 2, iRow, u"<font=3>%s</font>"%(szFortify), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt(self.UNITQUEUE, 3, iRow, u"<font=3>%s</font>"%(szLoopNum), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			iLoopPos += 1

		bLoop = UnitPlacement.UnitPlacement().isUnitLoop(iCityID, iUnit)
		if (bLoop):
			screen.changeImageButton(self.UNITQUEUELOOP, "Art/Interface/Buttons/checked.dds")
			screen.setState(self.UNITQUEUELOOP, True)
		else:
			screen.changeImageButton(self.UNITQUEUELOOP, "Art/Interface/Buttons/unchecked.dds")
			screen.setState(self.UNITQUEUELOOP, False)

		screen.enable(self.SETORDERUP, False)
		screen.enable(self.SETORDERDOWN, False)

	def showSetOrder(self, iCityID, iUnit = -1, iDestCity = -1, iOrderNum = -1, bFortify = False):
		screen = self.getScreen()

		iPlayer = gc.getGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)

		if (iCityID != UnitPlacement.gAllCityID):
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(iCityID)

		# Debug Info
		#if (iUnit != -1):
		#	szText = "ShowSetOrder: " + pCity.getName() + ", " + gc.getUnitInfo(iUnit).getText() + ", " + str(iOrderNum)
		#else:
		#	szText = "ShowSetOrder: " + pCity.getName() + ", " + str(iOrderNum)
		#screen.setText("UPTestString", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 100, 10, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Unit List
		screen.setText(self.SETORDERUNITLIST+"String", "Background", localText.getText("TXT_KEY_UNIT_PLACEMENT_SET_ORDER_UNIT", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_SET_ORDER + 20, self.Y_SET_ORDER + 40, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDropDownBoxGFC(self.SETORDERUNITLIST, self.X_SET_ORDER + 20, self.Y_SET_ORDER + 65, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(self.SETORDERUNITLIST, localText.getText("TXT_KEY_UNIT_PLACEMENT_SET_ORDER_UNIT_TEXT", ()), -1, -1, False)

		AllCityID = UnitPlacement.gAllCityID
		if (iCityID != AllCityID):
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(iCityID)
			for iLoopUnit in xrange(gc.getNumUnitClassInfos()):
				info = gc.getUnitInfo(iLoopUnit)
				iUnitIndex = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iLoopUnit)
				UnitDomainType = info.getDomainType()
				if (pCity.canTrain(iUnitIndex, False, True) and UnitDomainType != DomainTypes.DOMAIN_IMMOBILE):
					if (iUnitIndex == iUnit):
						bSelected = True
					else:
						bSelected = False
					screen.addPullDownString(self.SETORDERUNITLIST, gc.getUnitInfo(iUnitIndex).getText(), iCityID, iUnitIndex, bSelected)

			# for all unit of city
			if (iUnit == UnitPlacement.gAllUnitID):
				bSelected = True
			else:
				bSelected = False
			screen.addPullDownString(self.SETORDERUNITLIST, localText.getText("TXT_KEY_UNIT_PLACEMENT_ALL_UNITS", ()), iCityID, UnitPlacement.gAllUnitID, bSelected)
		else:
			UnitList = set()
			(pLoopCity, iter) = pPlayer.firstCity(False)
			while (pLoopCity):
				for iLoopUnit in xrange(gc.getNumUnitClassInfos()):
					info = gc.getUnitInfo(iLoopUnit)
					iUnitIndex = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iLoopUnit)
					UnitDomainType = info.getDomainType()
					if (pLoopCity.canTrain(iUnitIndex, False, True) and UnitDomainType != DomainTypes.DOMAIN_IMMOBILE):
						UnitList.add(iUnitIndex)
				(pLoopCity, iter) = pPlayer.nextCity(iter, False)

			for iLoopUnit in UnitList:
				if (iLoopUnit == iUnit):
					bSelected = True
				else:
					bSelected = False
				screen.addPullDownString(self.SETORDERUNITLIST, gc.getUnitInfo(iLoopUnit).getText(), AllCityID, iLoopUnit, bSelected)

			# for all unit of city
			if (iUnit == UnitPlacement.gAllUnitID):
				bSelected = True
			else:
				bSelected = False
			screen.addPullDownString(self.SETORDERUNITLIST, localText.getText("TXT_KEY_UNIT_PLACEMENT_ALL_UNITS", ()), AllCityID, UnitPlacement.gAllUnitID, bSelected)

		# Destination List
		screen.setText(self.SETORDERDESTLIST+"String", "Background", localText.getText("TXT_KEY_UNIT_PLACEMENT_SET_ORDER_DESTINATION", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_SET_ORDER + 190, self.Y_SET_ORDER + 40, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDropDownBoxGFC(self.SETORDERDESTLIST, self.X_SET_ORDER + 190, self.Y_SET_ORDER + 65, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		if (iUnit == -1):
			screen.addPullDownString(self.SETORDERDESTLIST, localText.getText("TXT_KEY_UNIT_PLACEMENT_DESTINATION", ()), -1, -1, True)
		else:
			self.setDestCityList(iCityID, iUnit, iDestCity)

		# The Number of unit
		screen.setText(self.SETORDERUNITNUM+"String", "Background", localText.getText("TXT_KEY_UNIT_PLACEMENT_SET_ORDER_NUMBER", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_SET_ORDER + 410, self.Y_SET_ORDER + 40, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDropDownBoxGFC(self.SETORDERUNITNUM, self.X_SET_ORDER + 410, self.Y_SET_ORDER + 65, 60, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for iNum in xrange(self.MaxUnitNum + 1):
			screen.addPullDownString(self.SETORDERUNITNUM, str(iNum), iNum, iNum, (iNum == iOrderNum))

		# Auto Fortify or sentry
		screen.addCheckBoxGFC(self.SETORDERAUTOFORTIFY, "Art/Interface/Buttons/unchecked.dds", "", self.X_SET_ORDER + 20, self.Y_SET_ORDER + 110, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setText(self.SETORDERAUTOFORTIFY + "Text", "Background", localText.getText("TXT_KEY_UNIT_PLACEMENT_AUTO_FORTIFY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_SET_ORDER + 50, self.Y_SET_ORDER + 113, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		if (bFortify):
			screen.changeImageButton(self.SETORDERAUTOFORTIFY, "Art/Interface/Buttons/checked.dds")
			screen.setState(self.SETORDERAUTOFORTIFY, True)
		else:
			screen.changeImageButton(self.SETORDERAUTOFORTIFY, "Art/Interface/Buttons/unchecked.dds")
			screen.setState(self.SETORDERAUTOFORTIFY, False)

		# Add Button
		screen.setButtonGFC(self.SETORDERADD, localText.getText("TXT_KEY_UNIT_PLACEMENT_ADD", ()), "", self.X_SET_ORDER + 280, self.Y_SET_ORDER + 110, 60, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Modify Button
		screen.setButtonGFC(self.SETORDERMODIFY, localText.getText("TXT_KEY_UNIT_PLACEMENT_MODIFY", ()), "", self.X_SET_ORDER + 350, self.Y_SET_ORDER + 110, 60, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# delete Button
		screen.setButtonGFC(self.SETORDERDELETE, localText.getText("TXT_KEY_UNIT_PLACEMENT_DELETE", ()), "", self.X_SET_ORDER + 420, self.Y_SET_ORDER + 110, 60, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

	def setUnitOrder(self, iCityID, iUnit, iDestID, iNum, iOrderNum, bFortify, bDelete = False):
		screen = self.getScreen()

		#szText = "Unit Name: " + gc.getUnitInfo(iUnit).getText() + ", Dest City: " + pDestCity.getName() + ", Number: " + str(iNum)
		#screen.setText("UPTestUnitOrder", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_SET_ORDER + 10, self.Y_SET_ORDER + 130, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		if (bDelete):
			UnitPlacement.UnitPlacement().deleteOrder(self.currentCity, iUnit, iOrderNum)
		else:
			UnitPlacement.UnitPlacement().setOrder(self.currentCity, iUnit, iDestID, iNum, iOrderNum, bFortify)

		screen.addTableControlGFC(self.UNITLIST, 1, self.X_UNIT_LIST + 20, self.Y_UNIT_LIST + 40, self.W_UNIT_LIST - 40, self.H_UNIT_LIST - 60, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.UNITLIST, True)
		screen.setStyle(self.UNITLIST, "Table_StandardCiv_Style")
		screen.setTableColumnHeader(self.UNITLIST, 0, "", self.W_UNIT_LIST - 40)

		CityOrder = UnitPlacement.UnitPlacement().getCityOrder(iCityID)
		iCounter = 0
		iSelectedUnit = -1
		self.lUnitListIndex = []
		for iLoopUnit in CityOrder:
			iRow = screen.appendTableRow(self.UNITLIST)
			if (iLoopUnit == UnitPlacement.gAllUnitID):
				szUnitName = localText.getText("TXT_KEY_UNIT_PLACEMENT_ALL_UNITS", ())
				szButtonFile = ""
			else:
				szUnitName = gc.getUnitInfo(iLoopUnit).getText()
				szButtonFile = gc.getUnitInfo(iLoopUnit).getButton()
			screen.setTableText(self.UNITLIST, 0, iRow, u"<font=3>%s</font>"%(szUnitName), szButtonFile, WidgetTypes.WIDGET_GENERAL, iLoopUnit, iLoopUnit, CvUtil.FONT_LEFT_JUSTIFY)
			self.lUnitListIndex.append(iLoopUnit)
			#CvUtil.pyPrint("set Unit Order: " + str(iLoopUnit) + gc.getUnitInfo(iLoopUnit).getText())
			if (iLoopUnit == iUnit):
				iSelectedUnit = iCounter
			iCounter += 1

		if (iSelectedUnit != -1):
			screen.selectRow(self.UNITLIST, iSelectedUnit, True)

		self.showUnitQueue(iCityID, iUnit)

	def setDestCityList(self, iCityID, iUnit, iDest = -1):
		screen = self.getScreen()

		screen.addDropDownBoxGFC(self.SETORDERDESTLIST, self.X_SET_ORDER + 190, self.Y_SET_ORDER + 65, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)

		for LoopSign in UnitPlacement.UnitPlacement().getSignDict().items():
			szText = LoopSign[1][2]
			bSelected = False
			if (iCityID == LoopSign[0]):
				szText = localText.getText("TXT_KEY_UNIT_PLACEMENT_STAY_HERE", ())
			if (iDest != -1):
				if (LoopSign[0] == iDest):
					bSelected = True
			else:
				if (iCityID == LoopSign[0]):
					bSelected = True
			screen.addPullDownString(self.SETORDERDESTLIST, szText, LoopSign[0], LoopSign[0], bSelected)

	# Will handle the input for this screen...
	def handleInput(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getFunctionName() == self.CITYLIST and inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			iIndex = inputClass.getData2()
			self.currentCity = iIndex
			self.showCityQueue(self.currentCity)
			self.dest = None
			self.refreshMinimap()
			return 1

		if (inputClass.getFunctionName() == self.UNITLIST and inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (len(self.lUnitListIndex) == 0):
				return
			iIndex = inputClass.getData()
			iSelectedUnit = self.lUnitListIndex[iIndex]
			self.currentUnit = iSelectedUnit
			self.currentOrderNum = 0
			self.showUnitQueue(self.currentCity, iSelectedUnit)
			return 1

		if (inputClass.getFunctionName() == self.UNITQUEUE and inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			iIndex = inputClass.getData()
			UnitQueue = UnitPlacement.UnitPlacement().getUnitList(self.currentCity, self.currentUnit)
			if (len(UnitQueue) == 0):
				return
			self.currentOrderNum = iIndex
			DestList = UnitPlacement.UnitPlacement().getSignDict()
			DestPlot = DestList[UnitQueue[iIndex][0]]
			self.dest = (DestPlot[0], DestPlot[1])
			self.refreshMinimap()
			self.showSetOrder(self.currentCity, self.currentUnit, UnitQueue[iIndex][0], UnitQueue[iIndex][1], UnitQueue[iIndex][3])
			if (len(UnitQueue) > 1):
				screen.enable(self.SETORDERUP, True)
				screen.enable(self.SETORDERDOWN, True)
			else:
				screen.enable(self.SETORDERUP, False)
				screen.enable(self.SETORDERDOWN, False)
			if (iIndex == 0):
				screen.enable(self.SETORDERUP, False)
			if (iIndex == len(UnitQueue)-1):
				screen.enable(self.SETORDERDOWN, False)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERDESTLIST and inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			iIndex = screen.getSelectedPullDownID(self.SETORDERDESTLIST)
			DestList = UnitPlacement.UnitPlacement().getSignDict().items()
			DestPlot = DestList[iIndex]
			self.dest = (DestPlot[1][0], DestPlot[1][1])
			self.refreshMinimap()
			return 1

		if (inputClass.getFunctionName() == self.SETORDERUNITLIST and inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			self.setDestCityList(self.currentCity, iSelectedUnit)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERADD and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			iSelectedDest = screen.getSelectedPullDownID(self.SETORDERDESTLIST)
			DestList = UnitPlacement.UnitPlacement().getSignDict().items()
			iDestID = DestList[iSelectedDest][0]
			iSelectedNum = screen.getSelectedPullDownID(self.SETORDERUNITNUM)
			self.currentUnit = iSelectedUnit
			bFortify = screen.getCheckBoxState(self.SETORDERAUTOFORTIFY)
			if (iSelectedUnit != -1 and iDestID != -1):
				self.setUnitOrder(self.currentCity, iSelectedUnit, iDestID, iSelectedNum, -1, bFortify, False)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERMODIFY and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iOrderNum = self.currentOrderNum
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			iSelectedDest = screen.getSelectedPullDownID(self.SETORDERDESTLIST)
			DestList = UnitPlacement.UnitPlacement().getSignDict().items()
			iDestID = DestList[iSelectedDest][0]
			iSelectedNum = screen.getSelectedPullDownID(self.SETORDERUNITNUM)
			self.currentUnit = iSelectedUnit
			bFortify = screen.getCheckBoxState(self.SETORDERAUTOFORTIFY)
			self.setUnitOrder(self.currentCity, iSelectedUnit, iDestID, iSelectedNum, iOrderNum, bFortify, False)
			self.showSetOrder(self.currentCity)
			for i in xrange(len(UnitPlacement.UnitPlacement().getUnitList(self.currentCity, self.currentUnit))):
				screen.selectRow(self.UNITQUEUE, i, False)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERDELETE and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iOrderNum = self.currentOrderNum
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			iSelectedDest = screen.getSelectedPullDownID(self.SETORDERDESTLIST)
			DestList = UnitPlacement.UnitPlacement().getSignDict().items()
			iDestID = DestList[iSelectedDest][0]
			iSelectedNum = screen.getSelectedPullDownID(self.SETORDERUNITNUM)
			self.currentUnit = iSelectedUnit
			self.setUnitOrder(self.currentCity, iSelectedUnit, iDestID, iSelectedNum, iOrderNum, False, True)
			self.showSetOrder(self.currentCity)
			for i in xrange(len(UnitPlacement.UnitPlacement().getUnitList(self.currentCity, self.currentUnit))):
				screen.selectRow(self.UNITQUEUE, i, False)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERUP and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.currentOrderNum == -1 or self.currentCity == None):
				return 1
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iOrderNum = self.currentOrderNum
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			self.currentUnit = iSelectedUnit
			UnitPlacement.UnitPlacement().swapOrder(self.currentCity, iSelectedUnit, iOrderNum, True)
			self.showUnitQueue(self.currentCity, iSelectedUnit)
			UnitQueue = UnitPlacement.UnitPlacement().getUnitList(self.currentCity, self.currentUnit)
			if (iOrderNum == 0):
				iOrderNum = len(UnitQueue)
			iOrderNum -= 1
			self.currentOrderNum = iOrderNum
			screen.selectRow(self.UNITQUEUE, iOrderNum, True)
			if (len(UnitQueue) > 1):
				screen.enable(self.SETORDERUP, True)
				screen.enable(self.SETORDERDOWN, True)
			else:
				screen.enable(self.SETORDERUP, False)
				screen.enable(self.SETORDERDOWN, False)
			if (iOrderNum == 0):
				screen.enable(self.SETORDERUP, False)
			if (iOrderNum == len(UnitQueue)-1):
				screen.enable(self.SETORDERDOWN, False)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERDOWN and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.currentOrderNum == -1 or self.currentCity == None):
				return 1
			iIndex = screen.getSelectedPullDownID(self.SETORDERUNITLIST)
			iOrderNum = self.currentOrderNum
			iSelectedUnit = screen.getPullDownData(self.SETORDERUNITLIST, iIndex)
			self.currentUnit = iSelectedUnit
			UnitPlacement.UnitPlacement().swapOrder(self.currentCity, iSelectedUnit, iOrderNum, False)
			self.showUnitQueue(self.currentCity, iSelectedUnit)
			UnitQueue = UnitPlacement.UnitPlacement().getUnitList(self.currentCity, self.currentUnit)
			if (iOrderNum == len(UnitQueue) - 1):
				iOrderNum = -1
			iOrderNum += 1
			self.currentOrderNum = iOrderNum
			screen.selectRow(self.UNITQUEUE, iOrderNum, True)
			if (len(UnitQueue) > 1):
				screen.enable(self.SETORDERUP, True)
				screen.enable(self.SETORDERDOWN, True)
			else:
				screen.enable(self.SETORDERUP, False)
				screen.enable(self.SETORDERDOWN, False)
			if (iOrderNum == 0):
				screen.enable(self.SETORDERUP, False)
			if (iOrderNum == len(UnitQueue)-1):
				screen.enable(self.SETORDERDOWN, False)
			return 1

		if (inputClass.getFunctionName() == self.UNITQUEUELOOP):
			if (self.currentUnit == -1 or self.currentCity == None):
				return 1
			bLoop = screen.getCheckBoxState(self.UNITQUEUELOOP)
			if (bLoop):
				screen.changeImageButton(self.UNITQUEUELOOP, "Art/Interface/Buttons/checked.dds")
			else:
				screen.changeImageButton(self.UNITQUEUELOOP, "Art/Interface/Buttons/unchecked.dds")
			UnitPlacement.UnitPlacement().setUnitLoop(self.currentCity, self.currentUnit, bLoop)
			return 1

		if (inputClass.getFunctionName() == self.SETORDERAUTOFORTIFY):
			bAutoFortify = screen.getCheckBoxState(self.SETORDERAUTOFORTIFY)
			if (bAutoFortify):
				screen.changeImageButton(self.SETORDERAUTOFORTIFY, "Art/Interface/Buttons/checked.dds")
			else:
				screen.changeImageButton(self.SETORDERAUTOFORTIFY, "Art/Interface/Buttons/unchecked.dds")
			return 1

		return 0

	def update(self, fDelta):
		return

