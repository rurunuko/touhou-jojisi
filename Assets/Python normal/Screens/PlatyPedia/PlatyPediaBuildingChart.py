from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaBuildingChart:
	def __init__(self, main):
		self.top = main

	def interfaceScreen(self):		
		screen = self.top.getScreen()
		szTable = self.top.getNextWidgetName()
		iNumColumns = 8
		if self.top.iSortBChartType == 1:
			iNumColumns = YieldTypes.NUM_YIELD_TYPES * 2 + 2
		elif self.top.iSortBChartType == 2:
			iNumColumns = CommerceTypes.NUM_COMMERCE_TYPES * 2 + 2
		elif self.top.iSortBChartType == 3:
			iNumColumns = 7
		screen.addTableControlGFC(szTable, iNumColumns, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE + 6, self.top.W_ITEMS_PANE, self.top.H_ITEMS_PANE, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSort(szTable)
		screen.setTableColumnHeader(szTable, 0, "", self.top.W_ITEMS_PANE *3/10)
		iWidth = self.top.W_ITEMS_PANE *7/10 - 10
		iNumColumns -= 2
		if self.top.iSortBChartType == 0:
			screen.setTableColumnHeader(szTable, 1, CyTranslator().getText("[ICON_PRODUCTION]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 2, CyTranslator().getText("[ICON_HAPPY]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 3, CyTranslator().getText("[ICON_HEALTHY]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 4, CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 5, CyTranslator().getText("[ICON_DEFENSE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 6, CyTranslator().getText("[ICON_BAD_GOLD]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 7, "", 10)
		elif self.top.iSortBChartType == 1:
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				screen.setTableColumnHeader(szTable, 1 + j * 2, u"%c" % gc.getYieldInfo(j).getChar(), iWidth/iNumColumns)
				screen.setTableColumnHeader(szTable, 2 + j * 2, u"%c%%" % gc.getYieldInfo(j).getChar(), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, YieldTypes.NUM_YIELD_TYPES * 2 + 1, "", 10)
		elif self.top.iSortBChartType == 2:
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				screen.setTableColumnHeader(szTable, 1 + j * 2, u"%c" % gc.getCommerceInfo(j).getChar(), iWidth/iNumColumns)
				screen.setTableColumnHeader(szTable, 2 + j * 2, u"%c%%" % gc.getCommerceInfo(j).getChar(), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, CommerceTypes.NUM_COMMERCE_TYPES * 2 + 1, "", 10)
		elif self.top.iSortBChartType == 3:
			screen.setTableColumnHeader(szTable, 1, CyTranslator().getText("TXT_KEY_LOCAL", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 2, CyTranslator().getText("TXT_KEY_TERRAIN_COAST", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 3, CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 4, CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 5, CyTranslator().getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 6, "", 10)

		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isBuildingEverActive(i): continue
			Info = gc.getBuildingInfo(i)
			if self.top.iSortBChart == 0:
				if not isNationalWonderClass(Info.getBuildingClassType()): continue
			elif self.top.iSortBChart == 1:
				if not isTeamWonderClass(Info.getBuildingClassType()): continue
			elif self.top.iSortBChart == 2:
				if not isWorldWonderClass(Info.getBuildingClassType()): continue
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, u"<font=3>" + Info.getDescription() + u"</font>", Info.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, i, 1, CvUtil.FONT_LEFT_JUSTIFY)
			if self.top.iSortBChartType == 0:
				szCost = CyTranslator().getText("TXT_KEY_NON_APPLICABLE", ())
				iCost = Info.getProductionCost()
				if iCost > -1:
					szCost = str(iCost)
				screen.setTableInt(szTable, 1, iRow, u"<font=3>" + szCost + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 2, iRow, u"<font=3>" + self.colorCode(Info.getHappiness()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 3, iRow, u"<font=3>" + self.colorCode(Info.getHealth()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 4, iRow, u"<font=3>" + self.colorCode(Info.getGreatPeopleRateChange()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 5, iRow, u"<font=3>" + self.colorCode(Info.getDefenseModifier()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 6, iRow, u"<font=3>" + self.colorCode(Info.getMaintenanceModifier()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 1:
				for j in xrange(YieldTypes.NUM_YIELD_TYPES):
					screen.setTableInt(szTable, 1 + j * 2, iRow, u"<font=3>" + self.colorCode(Info.getYieldChange(j)) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
					screen.setTableInt(szTable, 2 + j * 2, iRow, u"<font=3>" + self.colorCode(Info. getYieldModifier(j)) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 2:
				for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					screen.setTableInt(szTable, 1 + j * 2, iRow, u"<font=3>" + self.colorCode(Info.getObsoleteSafeCommerceChange(j) + Info.getCommerceChange(j)) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
					screen.setTableInt(szTable, 2 + j * 2, iRow, u"<font=3>" + self.colorCode(Info.getCommerceModifier(j)) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 3:
				screen.setTableInt(szTable, 1, iRow, u"<font=3>" + self.colorCode(Info.getTradeRoutes()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 2, iRow, u"<font=3>" + self.colorCode(Info.getCoastalTradeRoutes()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 3, iRow, u"<font=3>" + self.colorCode(Info.getGlobalTradeRoutes()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 4, iRow, u"<font=3>" + self.colorCode(Info.getTradeRouteModifier ()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 5, iRow, u"<font=3>" + self.colorCode(Info.getForeignTradeRouteModifier()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

	def colorCode(self, iValue):
		sText = str(iValue)
		if iValue > 0:
			sText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + sText + "</color>"
		elif iValue < 0:
			sText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + sText + "</color>"
		return sText

	def handleInput (self, inputClass):
		return 0