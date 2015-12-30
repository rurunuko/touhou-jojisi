#TradeResourcePanel copyright (c) noraneko
# Modified for Civ IV Gameplay Enhancements
# Added: Display Options, Icon Size Option


from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import CvScreensInterface
import CvConfigParser
import Popup as PyPopup

# globals
gc = CyGlobalContext()
localText = CyTranslator()
ArtFileMgr = CyArtFileMgr()
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
ShowTradeResourcePanel = config.getboolean("Trade Resource Panel", "Show", True)
ShowTradeResourcePanel_Trade = config.getboolean("Trade Resource Panel", "Trade", True)
TRPOption1 = config.getint( "Trade Resource Panel", "Import and Export", 0)
TRPOption2 = config.getint( "Trade Resource Panel", "Technology and Resource", 0)
bCompressMode = config.getboolean("Trade Resource Panel", "Compress Mode", False)
bShowSingleResource = config.getboolean("Trade Resource Panel", "Show Single Resource", False)
civList = []
civName = dict()
techList = []
tempRemoveTechList = []
resourceList = []
bFirstShow = True
bHideScreen = False
bUpdateTech = True
iCivCount = 0
iCivNum = 0
MonopolyPanelList = []
TradePanelListFrom = []
TradePanelListTo = []
TradePanelResTo = []
TradePanelResFrom = []
AllBonus = set()
lBonusInfos = []
bGlobeView = False
TradeDic = dict()
PrevDic = dict()
sWatchList = set()
g_szMonoText = ""
goldList = dict()

# Small Font
bSmallFont =  config.getboolean("Trade Resource Panel", "SmallIcons", False)
szPreText = u""
szPostText = u""
iTextWidth = 120
iIconSize = 22
iTextHeight = iIconSize * 2

class TradeResourcePanel:

	def Init(self):
		global civList
		global civName
		global techList
		global tempRemoveTechList
		global resourceList
		global bFirstShow
		global iCivNum
		global AllBonus
		global szPreText
		global szPostText
		global iTextWidth
		global iIconSize
		global iTextHeight
		global g_szMonoText
		global goldList

		g_szMonoText = ""

		bFirstShow = True
		civList = []
		techList = []
		goldList = dict()

		civListappend = civList.append
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			eGetLoopPlayer = gc.getPlayer(iLoopPlayer)
			if(eGetLoopPlayer.isAlive() and not eGetLoopPlayer.isBarbarian() and not eGetLoopPlayer.isMinorCiv()):
				civListappend(iLoopPlayer)
				goldList[iLoopPlayer] = (0, 0)
		iCivNum = len(civList)

		tempRemoveTechList = []
		techListappend = techList.append
		ActiveTeam = gc.getPlayer(gc.getGame().getActivePlayer()).getTeam()
		bNotCanTrade = not gc.getTeam(ActiveTeam).isTechTrading()
		for iLoopTech in xrange(gc.getNumTechInfos()):
			iHasTech = 0
			iHasMet = 0
			for iLoopPlayer in civList:
				LoopTeam = gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam())
				if (LoopTeam.isHasTech(iLoopTech)):
					iHasTech += 1
				if (LoopTeam.isHasMet(ActiveTeam)):
					iHasMet += 1
			if (iHasTech < iCivNum):
				techListappend(iLoopTech)
			else:
				if (iHasMet < iCivNum or bNotCanTrade):
					techListappend(iLoopTech)
					tempRemoveTechList.append(iLoopTech)

		AllBonus = set(range(gc.getNumBonusInfos()))

		if (bSmallFont):
			szPreText = u"<font=2>"
			szPostText = u"</font>"
			iTextWidth = 47
			iIconSize = 17
		else:
			szPreText = u""
			szPostText = u""
			iTextWidth = 55
			iIconSize = 22

	def StartTurn(self):
		global TradeDic
		global PrevDic

		PrevDic = TradeDic.copy()

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			TradeDic[iLoopPlayer] = set()

	def FirstContact(self):
		global bFirstShow

		bFirstShow = True

	def UpdateList(self):
		global civList
		global resourceList
		global bFirstShow
		global bUpdateTech
		global bShowSingleResource
		bChanged = False

		if (bFirstShow):
			bFirstShow = False
			return True

		if (bUpdateTech):
			bUpdateTech = False
			return True
		else:
			iActivePlayer = gc.getGame().getActivePlayer()
			pActivePlayer = gc.getPlayer(iActivePlayer)
			iActiveTeam = pActivePlayer.getTeam()
			tradeItem = TradeData()
			metCivList = []
			for iLoopPlayer in civList:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				pLoopTeam = gc.getTeam(pLoopPlayer.getTeam())
				if (iLoopPlayer != iActivePlayer and pLoopPlayer.isAlive() and pLoopTeam.isHasMet(iActiveTeam)):
					metCivList.append((iLoopPlayer, pLoopPlayer))

			if (TRPOption2 == 0):
				for (iLoopPlayer, pLoopPlayer) in metCivList:
					if (goldList[iLoopPlayer] != (pLoopPlayer.AI_maxGoldTrade(iActivePlayer), pLoopPlayer.AI_maxGoldPerTurnTrade(iActivePlayer))):
						return True

			tradeItem.ItemType = TradeableItems.TRADE_RESOURCES
			ResFrom = []
			ResTo = []
			NumActivePlayerTradeBonus = pActivePlayer.getNumTradeableBonuses
			BonusImport = pActivePlayer.getBonusImport
			for i in xrange(gc.getNumBonusInfos()):
				iNum = NumActivePlayerTradeBonus(i)
				if (bShowSingleResource and iNum > 0 or iNum > 1):
					ResTo.append(i)
				elif (iNum == 0 and BonusImport(i) == 0):
					ResFrom.append(i)
			pActivePlayerCanTradeItem = pActivePlayer.canTradeItem
			for (iLoopPlayer, pLoopPlayer) in metCivList:
				pPlayerCanTradeItem = pLoopPlayer.canTradeItem
				pPlayerNumTradeableBonuses = pLoopPlayer.getNumTradeableBonuses
				sPlayerFrom = set([iBonus for (iPlayer, iBonus) in TradePanelResFrom if (iPlayer == iLoopPlayer)])
				for iBonus in ResFrom:
					if (pPlayerNumTradeableBonuses(iBonus) == 0):
						if (iBonus in sPlayerFrom):
							return True
						else:
							continue
					tradeItem.iData = iBonus
					if (pPlayerCanTradeItem(iActivePlayer, tradeItem, True)):
						if (iBonus not in sPlayerFrom):
							return True
					else:
						if (iBonus in sPlayerFrom):
							return True
				sPlayerTo = set([iBonus for (iPlayer, iBonus) in TradePanelResTo if (iPlayer == iLoopPlayer)])
				for iBonus in ResTo:
					if (pPlayerNumTradeableBonuses(iBonus) > 0):
						if (iBonus in sPlayerTo):
							return True
						else:
							continue
					tradeItem.iData = iBonus
					if (pActivePlayerCanTradeItem(iLoopPlayer, tradeItem, True)):
						if (iBonus not in sPlayerTo):
							return True
					else:
						if (iBonus in sPlayerTo):
							return True

			tradeItem.ItemType = TradeableItems.TRADE_TECHNOLOGIES
			ActiveTeamHasTech = gc.getTeam(iActiveTeam).isHasTech
			notHasTechList = [iTech for iTech in techList if (not ActiveTeamHasTech(iTech))]
			for (iLoopPlayer, pLoopPlayer) in metCivList:
				PlayerTechFrom = [(iTech, bEnable) for (iPlayer, iTech, bEnable) in TradePanelListFrom if (iPlayer == iLoopPlayer)]
				sPlayerTechFromOK = set([iTech for (iTech, bEnable) in PlayerTechFrom if (bEnable)])
				sPlayerTechFromDenial = set([iTech for (iTech, bEnable) in PlayerTechFrom if (not bEnable)])

				pPlayerCanTradeItem = pLoopPlayer.canTradeItem
				pPlayerGetTradeDenial = pLoopPlayer.getTradeDenial
				LoopTeamHasTech = gc.getTeam(pLoopPlayer.getTeam()).isHasTech
				for iLoopTech in [iTech for iTech in notHasTechList if (LoopTeamHasTech(iTech))]:
					tradeItem.iData = iLoopTech

					if (pPlayerCanTradeItem(iActivePlayer, tradeItem, False)):
						if (pPlayerGetTradeDenial(iActivePlayer, tradeItem) == DenialTypes.NO_DENIAL):
							if (iLoopTech not in sPlayerTechFromOK):
								return True
						else:
							if (iLoopTech not in sPlayerTechFromDenial):
								return True

		return False

	def UpdateTechList(self, iPlayer, iTech):
		global civList
		global techList
		global tempRemoveTechList
		global bUpdateTech
		global bFirstShow
		global iCivNum

		iHasTech = 0
		iHasMet = 0
		ActiveTeam = gc.getPlayer(gc.getGame().getActivePlayer()).getTeam()
		for iLoopPlayer in civList:
			LoopTeam = gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam())
			if (LoopTeam.isHasTech(iTech)):
					iHasTech += 1
			if (LoopTeam.isHasMet(ActiveTeam)):
					iHasMet += 1

		if (iHasTech >= iCivNum and not bFirstShow):
			if (iHasMet == iCivNum and gc.getTeam(ActiveTeam).isTechTrading()):
				techList.remove(iTech)
				for iLoopTech in tempRemoveTechList:
					try:
						techList.remove(iLoopTech)
					except ValueError:
						Cvutil.pyPrint("TRP Error: %s has %s and remove %s"%(gc.getPlayer(iPlayer).getName(), gc.getTechInfo(iTech).getDescription(), gc.getTechInfo(iLoopTech).getDescription()))
						pass
				#CyInterface().addImmediateMessage("%s is removed from TechList(%d >= %d)"%(gc.getTechInfo(iTech).getDescription(), iHasTech, len(civList)),"")
				# Delete Widget
				screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				screen.deleteWidget("MonopolyButton" + str(iTech))
				for iLoopPlayer in civList:
					szName = "TradeResourceTechButton" + str(iLoopPlayer) + "_"
					screen.deleteWidget(szName + str(iTech))
					for iLoopTech in tempRemoveTechList:
						screen.deleteWidget(szName + str(iLoopTech))
				tempRemoveTechList = []
			else:
				tempRemoveTechList.append(iTech)

		bUpdateTech = True

	def ResetPanel(self, argsList):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screenhide = screen.hide

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			szLoopPlayer = str(iLoopPlayer)
			szName = "TradeResourceTechButton" + szLoopPlayer + "_"
			for iLoopTech in xrange(gc.getNumTechInfos()):
				screenhide(szName + str(iLoopTech))

			for szComponentName in ["TradeResourceFrom", "TradeResourceTo"]:
				screenhide(szComponentName + "CivText" + szLoopPlayer)
				screenhide(szComponentName + "ResourceText" + szLoopPlayer)

		screenhide("TradeResourceFromBackgroundPanel")
		screenhide("TradeResourceToBackgroundPanel")

		if (argsList[1]):
			iPlayer = argsList[0]
			pPlayer = gc.getPlayer(iPlayer)
			szButton = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()

			if (bSmallFont):
				iFontSize = 16
			else:
				iFontSize = 20

			for szComponentName in ["TradeResourceFrom", "TradeResourceTo"]:
				szName = "%sCivText%d"%(szComponentName, iPlayer)
				screen.setImageButton(szName, szButton, 0, 0, iFontSize, iFontSize, WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1)
				screen.hide(szName)

	def isShow(self):
		return ShowTradeResourcePanel

	def getTechList(self):
		global techList

		return techList

	def ToggleTradeResourcePanel(self):
		global ShowTradeResourcePanel
		if (ShowTradeResourcePanel):
			self.hideTradeResourcePanel()
			ShowTradeResourcePanel = False
		else:
			self.showTradeResourcePanel()
			ShowTradeResourcePanel = True

	def ToggleTradeResourcePanel_Trade(self):
		global ShowTradeResourcePanel_Trade
		if (ShowTradeResourcePanel_Trade):
			ShowTradeResourcePanel_Trade = False
			self.hideTradeResourcePanel_Trade()
		else:
			ShowTradeResourcePanel_Trade = True
			self.showTradeResourcePanel()

	def showTradeResourcePanelConfig(self):
		global TRPOption1, TRPOption2, bCompressMode, bShowSingleResource

		popup=CyPopup(CvUtil.EventTRPOption, EventContextTypes.EVENTCONTEXT_ALL, True)
		popup.setHeaderString(localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION_TITLE", ()), CvUtil.FONT_CENTER_JUSTIFY)

		popup.addSeparator()
		popup.setBodyString(localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION1", ()), CvUtil.FONT_CENTER_JUSTIFY)
		popup.createPullDown(0)
		for i in range(3):
			strText = localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION1_%d"%(i+1), ())
			popup.addPullDownString(strText, i, 0)
		popup.setSelectedPulldownID(TRPOption1, 0)

		popup.addSeparator()
		popup.setBodyString(localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION2", ()), CvUtil.FONT_CENTER_JUSTIFY)
		popup.createPullDown(1)
		for i in range(4):
			strText = localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION2_%d"%(i+1), ())
			popup.addPullDownString(strText, i, 1)
		popup.setSelectedPulldownID(TRPOption2, 1)

		popup.addSeparator()
		popup.createPullDown(2)
		for i in range(2):
			strText = localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION3_%d"%(i+1), ())
			popup.addPullDownString(strText, i, 2)
		popup.setSelectedPulldownID(int(bCompressMode), 2)

		popup.addSeparator()
		popup.createPullDown(3)
		for i in range(2):
			strText = localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION4_%d"%(i+1), ())
			popup.addPullDownString(strText, i, 2)
		popup.setSelectedPulldownID(int(bShowSingleResource), 3)

		lCivList = []
		iActivePlayer = gc.getGame().getActivePlayer()
		iActiveTeam =gc.getPlayer(iActivePlayer).getTeam()
		for iLoopPlayer in civList:
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			pLoopTeam = pLoopPlayer.getTeam()
			if (iLoopPlayer != iActivePlayer and pLoopPlayer.isAlive() and gc.getTeam(pLoopTeam).isHasMet(iActiveTeam) and iActiveTeam != pLoopTeam):
				lCivList.append(iLoopPlayer)

		popup.addSeparator()
		popup.setBodyString(localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION3", ()), CvUtil.FONT_CENTER_JUSTIFY)
		for i in range(4,6):
			popup.createPullDown(i)
			popup.addPullDownString(localText.getText("TXT_KEY_TRADE_REDSOURCE_NONE", ()), -1, i)
			for iLoopPlayer in lCivList:
				popup.addPullDownString(gc.getPlayer(iLoopPlayer).getCivilizationAdjective(0), iLoopPlayer, i)

		iGroup = 3
		for iLoopPlayer in sWatchList:
			if (iLoopPlayer != -1):
				popup.setSelectedPulldownID(iLoopPlayer, iGroup)
				iGroup += 1

		#popup.setBodyString("Civ Num: %d"%(len(civList)), CvUtil.FONT_CENTER_JUSTIFY)
		#for item in civList:
		#	popup.setBodyString("%s"%(gc.getPlayer(item).getName()), CvUtil.FONT_CENTER_JUSTIFY)
		#iNumTech = 0
		#for item in techList:
		#	iNumTech += 1
		#	iHasTech = 0
		#	iLoopPlayer = 0
		#	for iLoopPlayer in civList:
		#		if (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasTech(item)):
		#			iHasTech += 1
		#	popup.setBodyString("%s: %d"%(gc.getTechInfo(item).getDescription(), iHasTech), CvUtil.FONT_CENTER_JUSTIFY)
		#popup.setBodyString("Tech Num: %d"%(iNumTech), CvUtil.FONT_CENTER_JUSTIFY)

		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

	def setTradeResourcePanelOption(self, option1, option2, option3, option4, watchList):
		global TRPOption1
		global TRPOption2
		global bCompressMode
		global bShowSingleResource
		global ShowTradeResourcePanel_Trade
		global sWatchList

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		TRPOption1 = option1 # 0: Both, 1: Export, 2: Import
		TRPOption2 = option2 # 0: Both, 1: 1 line, 2: Technology, 3: Resource
		bCompressMode = bool(option3) # Compress Mode 0: off, 1: on
		bShowSingleResource = bool(option4) # Show Single Resource 0: off, 1: on
		sWatchList = watchList.copy()

		i = 0
		for iPlayer in watchList:
			screen.changeImageButton("TradeResourceWatchCiv" + str(i), gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getButton())
			i += 1

		ShowTradeResourcePanel_Trade =True
		self.hideTradeResourcePanel_Trade()
		self.updateTradeResourcePanels(True)

	def setCGEOption(self, Section, Key, Value):
		global TRPOption1
		global TRPOption2
		global ShowTradeResourcePanel
		global ShowTradeResourcePanel_Trade
		global bCompressMode
		global bShowSingleResource

		if (Key == "Show"):
			ShowTradeResourcePanel = Value
			if (Value):
				self.showTradeResourcePanel()
			else:
				self.hideTradeResourcePanel()
			return
		elif (Key == "Trade"):
			ShowTradeResourcePanel_Trade = Value
		elif (Key == "Import and Export"):
			TRPOption1 = Value
		elif (Key == "Technology and Resource"):
			TRPOption2 = Value
		elif (Key == "Compress Mode"):
			bCompressMode = Value
		elif (Key == "Show Single Resource"):
			bShowSingleResource = Value
		if (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			self.hideTradeResourcePanel_Trade()
			self.updateTradeResourcePanels(True)

	def showTradeResourcePanel(self):
		self.updateTradeResourcePanels(True)

	def hideTradeResourcePanel_Trade(self):
		global civList
		global TradePanelListFrom
		global TradePanelListTo
		global TradePanelResTo
		global TradePanelResFrom

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		szTech = "TradeResourceTechButton"
		for item in TradePanelListFrom + TradePanelListTo:
			szTechName = szTech + str(item[0]) + "_" + str(item[1])
			screen.hide(szTechName)
			screen.hide(szTechName + "Counter")

		szRes = "TradeResourceResButton"
		iActivePlayer = gc.getGame().getActivePlayer()
		for item in TradePanelResFrom + TradePanelResTo:
			szResName = szRes + str(item[0]) + "_" + str(item[1])
			screen.hide(szResName)
			if (item[0] == iActivePlayer):
				screen.hide(szResName + "Counter")

		for szComponentName in ["TradeResourceFrom", "TradeResourceTo"]:
			for iLoopPlayer in civList:
				screen.hide(szComponentName + "CivText" + str(iLoopPlayer))
				screen.hide(szComponentName + "ResourceText" + str(iLoopPlayer))

			screen.hide(szComponentName + "Title")
			screen.hide(szComponentName + "BackgroundPanel")

		for i in xrange(3):
			screen.hide("TradeResourceWatchCiv" + str(i))

		TradePanelListFrom = []
		TradePanelListTo = []
		TradePanelResTo = []
		TradePanelResFrom = []

	def hideTradeResourcePanel(self):
		global MonopolyPanelList

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		for iLoopTech in MonopolyPanelList:
			screen.hide("MonopolyButton" + str(iLoopTech))

		MonopolyPanelList = []
		screen.hide("MonopolyText")

		self.hideTradeResourcePanel_Trade()

	#資源、テクノロジのパネル作成
	def createTradeResourcePanels(self):
		global TradeDic
		global PrevDic
		global sWatchList
		global TradePanelListFrom
		global TradePanelListTo
		global TradePanelResTo
		global TradePanelResFrom
		global MonopolyPanelList

		self.Init()

		TradePanelListFrom = []
		TradePanelListTo = []
		TradePanelResTo = []
		TradePanelResFrom = []
		MonopolyPanelList = []

		sWatchList = set()
		TradeDic = dict()
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			TradeDic[iLoopPlayer] = set()
		PrevDic = TradeDic.copy()

		self.createMonopolyPanel()
		self.createTradeResourcePanel("TradeResourceFrom")
		self.createTradeResourcePanel("TradeResourceTo")
		self.createTradeResourceTechResButton()
		self.createTradeResourceWatchCiv()

		return 0

	def createTradeResourceWatchCiv(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		Xoffset = screen.getXResolution() - 20

		for i in xrange(3):
			szName = "TradeResourceWatchCiv" + str(i)
			screen.setImageButton(szName, "", Xoffset - 16 * i, 106, 14, 14, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.hide(szName)

	def createTradeResourceTechResButton(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		if (bSmallFont):
			iFontSize = 16
		else:
			iFontSize = 20

		iActivePlayer = gc.getGame().getActivePlayer()
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			if (iLoopPlayer == iActivePlayer):
				iSize = 22
			else:
				iSize = iFontSize
			#テクノロジのアイコン
			szName = "TradeResourceTechButton" + str(iLoopPlayer) + "_"
			for iLoopTech in techList:
				#クリックでペディアを開く(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH)
				#WidgetTypes.WIDGET_GENERALで何も起こらなくなる
				szTechName = szName + str(iLoopTech)
				screen.setImageButton(szTechName, gc.getTechInfo(iLoopTech).getButton(), 0, 0, iSize, iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1)
				screen.hide(szTechName)
			#資源のアイコン
			szName = "TradeResourceResButton" + str(iLoopPlayer) + "_"
			for iBonus in xrange(gc.getNumBonusInfos()):
				szResName = szName + str(iBonus)
				screen.setImageButton(szResName, gc.getBonusInfo(iBonus).getButton(), 0, 0, iSize+2, iSize+2, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1)
				screen.hide(szResName)

	#資源、テクノロジのパネル更新
	def updateTradeResourcePanels(self, bForce):
		global ShowTradeResourcePanel_Trade
		global TRPOption1
		global bHideScreen
		bHide = False

		if (bHideScreen or CyInterface().isCityScreenUp() or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL):
			bHide = True
		if (not bForce):
			if (not ShowTradeResourcePanel):
				return 0

		if (bHide):
			bChanged = True
		else:
			bChanged = self.UpdateList()

		if (bChanged or bForce or bHideScreen):
			self.updateMonopolyPanel()

			if (ShowTradeResourcePanel_Trade):
				hasResources = set()

				AvailableBonus = gc.getPlayer(gc.getGame().getActivePlayer()).getNumAvailableBonuses
				for iLoopBonus in xrange(gc.getNumBonusInfos()):
					if (AvailableBonus(iLoopBonus)):
						hasResources.add(iLoopBonus)
				# 個別取引画面を左右別々に表示する場合はself.updateTradeResourcePanelの引数を各自で設定してください。
				# 変更する必要のある引数は第1(y座標), 第4(左右)です。これ以外は変更しないでください。
				# y座標はパネル上部を決める座標になります。
				# 左右の指定はパネルを画面の左右どちらに表示するかです。
				# 設定例をそれぞれに示して置きますのでそれを参考に設定してください。
				# なお、左側に表示した場合、ヘルプテキストがパネルの下に表示され、非常に読みにくくなります。
				# 解決方法もわからないのでこれに関する苦情は一切受け付けません。
				if (TRPOption1 == 1): # Exportのみ表示
					self.updateTradeResourcePanel(80, hasResources, True, True) # right
				elif (TRPOption1 == 2): # Importのみ表示
					self.updateTradeResourcePanel(80, hasResources, False, True) # right
				else:
					if (bCompressMode):
						# 圧縮表示モード
						iHeight = self.updateCompressTradeResourcePanel(87, hasResources, False)
						self.updateCompressTradeResourcePanel(iHeight + 102, hasResources, True)
					else:
						# Export, Import両方
						# Import
						iHeight = self.updateTradeResourcePanel(80, hasResources, False, True) # right
						#iHeight = self.updateTradeResourcePanel(140, hasResources, False, False) # left
						# Export
						# iHeightは輸出画面のy座標を決定するのに必要ですので、両方スタックして表示する場合には必ずy座標に追加するようにしてください。
						self.updateTradeResourcePanel(iHeight + 80, hasResources, True, True) # right
						#self.updateTradeResourcePanel(iHeight + 140, hasResources, True, False) # left

			if (CyInterface().isCityScreenUp() or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL):
				bHideScreen = True
			else:
				bHideScreen = False

		return 0

	def updateTradeResourcePanelsWithGloveView(self):
		global bGlobeView

		if (bGlobeView != CyEngine().isGlobeviewUp()):
			bGlobeView = CyEngine().isGlobeviewUp()
			if (ShowTradeResourcePanel):
				self.updateTradeResourcePanels(True)

	#トレード可能な資源、テクノロジのパネル作成
	def createTradeResourcePanel(self, szComponentName):
		global civList
		global techList

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		szName = "%sBackgroundPanel"%(szComponentName)
		screen.addPanel(szName, u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP)
		screen.hide(szName)

		if (bSmallFont):
			iFontSize = 16
		else:
			iFontSize = 20

		iActivePlayer = gc.getGame().getActivePlayer()
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			if (iLoopPlayer != iActivePlayer):
				#文明の名前
				szName = "%sCivText%d"%(szComponentName, iLoopPlayer)
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if (pLoopPlayer.isAlive()):
					szButton = gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType()).getButton()
					screen.setImageButton(szName, szButton, 0, 0, iFontSize, iFontSize, WidgetTypes.WIDGET_CONTACT_CIV, iLoopPlayer, -1)
					screen.hide(szName)

				#資源のアイコン
				szName = "%sResourceText%d"%(szComponentName, iLoopPlayer)
				screen.setText(szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 0, 0, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.hide(szName)

		if (szComponentName == "TradeResourceFrom"):
			szText = "<font=1>" + localText.getText('TXT_KEY_TRADE_REDSOURCE_IMPORTS', ()) + "</font>"
		else:
			szText = "<font=1>" + localText.getText('TXT_KEY_TRADE_REDSOURCE_EXPORTS', ()) + "</font>"
		screen.setText(szComponentName + "Title", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, 0, 0, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide(szComponentName + "Title")

		return 0

	#トレード可能な資源、テクノロジのパネル更新
	def updateTradeResourcePanel(self, iBaseY, hasResources, bTradeTo, bRight):
		global civList
		global civName
		global techList
		global TRPOption2
		global TradePanelListFrom
		global TradePanelListTo
		global TradePanelResTo
		global TradePanelResFrom
		global goldList
		global bShowSingleResource

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screenhide = screen.hide
		screenshow = screen.show
		if (bTradeTo):
			TradePanelList = TradePanelListTo
			TradePanelResList = TradePanelResTo
			szComponentName = "TradeResourceTo"
		else:
			TradePanelList = TradePanelListFrom
			TradePanelResList = TradePanelResFrom
			szComponentName = "TradeResourceFrom"

		prevTechList = set([(iLoopPlayer, iLoopTech) for (iLoopPlayer, iLoopTech, bEnable) in TradePanelList])
		prevResList = set(TradePanelResList)

		for iLoopPlayer in civList:
			screen.hide(szComponentName + "CivText" + str(iLoopPlayer))
			screen.hide(szComponentName + "ResourceText" + str(iLoopPlayer))

		if (bTradeTo):
			TradePanelListTo = []
			TradePanelList = TradePanelListTo
			TradePanelResTo = []
			TradePanelResList = TradePanelResTo
		else:
			TradePanelListFrom = []
			TradePanelList = TradePanelListFrom
			TradePanelResFrom = []
			TradePanelResList = TradePanelResFrom

		iTotalPanelHeight = 18

		#表示すべき状態かチェック（都市画面、地球儀状態等）
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW and not CyEngine().isGlobeviewUp()):
			tradeTechData = TradeData()
			tradeResData = TradeData()
			tradeTechData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
			tradeResData.ItemType = TradeableItems.TRADE_RESOURCES

			#画面の大きさ
			xResolution = screen.getXResolution()

			#位置とか
			iMaxTech = 12
			iMaxCount = 0
			if (bRight):
				iSize = iIconSize
				iXoffset = xResolution - iTextWidth
				iXLeader = xResolution - iSize - 4
# CGE-LE - begin
				if (TRPOption2 == 1):
					iXGold = xResolution - iIconSize - 14
				else:
					iXGold = xResolution - iIconSize / 2
# CGE-LE - end
				iXTitle = iXoffset - 120
				iJustify = CvUtil.FONT_RIGHT_JUSTIFY
			else:
				iSize = -iIconSize
				iXoffset = iTextWidth - iIconSize
				iXLeader = 4
				iXGold = iIconSize/2
				iXTitle = 120
				iJustify = CvUtil.FONT_LEFT_JUSTIFY

			iActivePlayer = gc.getGame().getActivePlayer()
			eGetActivePlayer = gc.getPlayer(iActivePlayer)
			eGetActiveTeam = eGetActivePlayer.getTeam()

			if (bTradeTo):
				hasResList = hasResources
				pPlayerCanTradeItem = eGetActivePlayer.canTradeItem
				pSrcPlayerNumBonus = eGetActivePlayer.getNumTradeableBonuses
				pTeamHasTech = gc.getTeam(eGetActiveTeam).isHasTech
			else:
				global AllBonus
				hasResList = AllBonus.difference(hasResources)
				iDestPlayer = iActivePlayer

			for iLoopPlayer in civList:

				eGetLoopPlayer = gc.getPlayer(iLoopPlayer)
				eGetLoopTeam = eGetLoopPlayer.getTeam()
				szStringPlayer = str(iLoopPlayer)
				bGoldText = False

				if (bTradeTo):
					#自分から他の文明へ
					#iSourcePlayer = eGetActivePlayer
					iDestPlayer = iLoopPlayer
				else:
					#他の文明から自分へ
					#iSourcePlayer = iLoopPlayer
					pSrcPlayerNumBonus = eGetLoopPlayer.getNumTradeableBonuses
					pPlayerCanTradeItem = eGetLoopPlayer.canTradeItem
					pTeamHasTech = gc.getTeam(eGetLoopTeam).isHasTech

				#自分自身、未接触、蛮族、小文明は除外
				if (iLoopPlayer != iActivePlayer and eGetLoopPlayer.isAlive() and gc.getTeam(eGetLoopTeam).isHasMet(eGetActiveTeam)):
					szText = u""

					#チームメイトは除外
					if(eGetActiveTeam == eGetLoopTeam):
						continue

					szName = szComponentName + "CivText" + szStringPlayer
					iY = iBaseY + iTotalPanelHeight

					screen.moveItem(szName, iXLeader, iY, -0.3)
					screenshow(szName)

					iTechCount = 0
					if (not (TRPOption2 == 3)):
						#トレード可能なテクノロジを表示
						szTemp = "TradeResourceTechButton" + szStringPlayer + "_"
						for iLoopTech in [iTech for iTech in techList if (pTeamHasTech(iTech))]:
							tradeTechData.iData = iLoopTech

							if (pPlayerCanTradeItem(iDestPlayer, tradeTechData, False)):
								#かならず1行目に表示
								szName = szTemp + str(iLoopTech)
								iX = iXoffset - iTechCount * iSize
								iY = iBaseY + iTotalPanelHeight
								screen.moveItem(szName, iX, iY, -0.3)
								bEnable = True
								if (not bTradeTo and eGetLoopPlayer.getTradeDenial(iActivePlayer, tradeTechData) != DenialTypes.NO_DENIAL):
									bEnable = False
								screen.enable(szName, bEnable)
								if ((iLoopPlayer, iLoopTech) in prevTechList):
									prevTechList.remove((iLoopPlayer, iLoopTech))
								screenshow( szName )
								TradePanelList.append((iLoopPlayer, iLoopTech, bEnable))
								iTechCount += 1
							if (iTechCount >= iMaxTech):
								break

					szText = u""
# CGE-LE - begin
					if ((TRPOption2 == 0 or TRPOption2 == 1) and not bTradeTo):
						if (gc.getTeam(eGetActiveTeam).isGoldTrading() or gc.getTeam(eGetLoopTeam).isGoldTrading()):
							if (TRPOption2 == 1):
								szText += u" <font=1>%d(%d)</font>"%(eGetLoopPlayer.AI_maxGoldTrade(iActivePlayer), eGetLoopPlayer.AI_maxGoldPerTurnTrade(iActivePlayer))
							else:
								szText += u" <font=1>%d(%d)%c</font>"%(eGetLoopPlayer.AI_maxGoldTrade(iActivePlayer), eGetLoopPlayer.AI_maxGoldPerTurnTrade(iActivePlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
# CGE-LE - end
							bGoldText = True
							goldList[iLoopPlayer] = (eGetLoopPlayer.AI_maxGoldTrade(iActivePlayer), eGetLoopPlayer.AI_maxGoldPerTurnTrade(iActivePlayer))

					if (bGoldText):
						szText = szPreText + szText + szPostText
						if (bRight):
							iX = xResolution - iSize * 1.5 - CyInterface().determineWidth(szText)
						else:
							iX = iXGold + CyInterface().determineWidth(szText)
					else:
						iX = iXoffset
					iY = iBaseY + iTotalPanelHeight

					#トレード可能なテクノロジがあるなら2行目に、ないなら1行目に表示
					if (iTechCount > 0):
						if (TRPOption2 == 1):
							iX = iXoffset - iTechCount * iSize
						else:
							iY += iIconSize - 2
					elif (bGoldText):
# CGE-LE - begin
						if (TRPOption2 == 1):
							iX = iXoffset
						else:
							iY += iIconSize - 2
# CGE-LE - end
					iBonusCount = 0
					if (not (TRPOption2 == 2)):
						#トレード可能な資源を表示

						szTemp = "TradeResourceResButton" + szStringPlayer + "_"
						for iLoopBonus in hasResList:
							#資源を独占しているとかなりの数になるから２つ以上ある場合に限定した方が良い？
							iResCount = 2
							if (bShowSingleResource):
								iResCount = 1
							if (pSrcPlayerNumBonus(iLoopBonus) >= iResCount):
								tradeResData.iData = iLoopBonus
								if (pPlayerCanTradeItem(iDestPlayer, tradeResData, True)):
									szName = szTemp + str(iLoopBonus)
									screen.moveItem(szName, iX - iBonusCount * iSize, iY, -0.3)
									if ((iLoopPlayer, iLoopBonus) in prevResList):
										prevResList.remove((iLoopPlayer, iLoopBonus))
									screenshow(szName)
									TradePanelResList.append((iLoopPlayer, iLoopBonus))
									iBonusCount += 1
							if (iBonusCount >= iMaxTech):
								break

						if (bGoldText):
# CGE-LE - begin
							if (TRPOption2 == 1):
								iX = iXGold - iTechCount * iSize - iBonusCount * iSize
								iY += 2
							else:
								iX = iXGold
# CGE-LE - end
						else:
							iX = iXoffset
						if (bGoldText):
							szName = szComponentName + "ResourceText" + szStringPlayer
							screen.setHelpLabel(szName, "Background", szPreText + szText + szPostText, iJustify, iX, iY -1, -0.3, FontTypes.SMALL_FONT, "")
							screenshow(szName)

					#トレード可能な資源とテクノロジがあるなら2行。ないなら1行進める。
# CGE-LE - begin
					if (((iBonusCount > 0 and iTechCount > 0) or bGoldText) and (not (TRPOption2 == 1))):
# CGE-LE - end
						iTotalPanelHeight += iIconSize * 2
					else:
						iTotalPanelHeight += iIconSize
						if ((iTechCount + iBonusCount) >iMaxCount):
							iMaxCount = iTechCount + iBonusCount

			szName = szComponentName + "Title"
			iY = iBaseY + 2
			screen.moveItem(szName, iXTitle, iY - 3, -0.3)
			screenshow(szName)
			#背景パネルを表示
			if (TRPOption2 == 1):
				if (iMaxCount > iMaxTech):
					iMaxTech = iMaxCount - 1
				iSpaceWidth = 15
			else:
				iMaxTech = iMaxTech
				iSpaceWidth = 8
			iTotalPanelHeight += 12
			szName = szComponentName + "BackgroundPanel"
			if (bRight):
				iX = iXoffset - (iIconSize * iMaxTech) - iSpaceWidth + 6
			else:
				iX = 0
			iY = iBaseY - 8
			iWidth = iTextWidth + iIconSize * iMaxTech + iSpaceWidth
			iHeight = iTotalPanelHeight
			screen.setPanelSize(szName, iX, iY, iWidth, iHeight)
			screenshow(szName)
		else:
			screenhide(szComponentName + "BackgroundPanel")
			screenhide(szComponentName + "Title")

		for item in prevTechList:
			screen.hide("TradeResourceTechButton" + str(item[0]) + "_" + str(item[1]))
		for item in prevResList:
			screen.hide("TradeResourceResButton" + str(item[0]) + "_" + str(item[1]))

		return iTotalPanelHeight

	#独占している技術のボタンを作成
	def createMonopolyPanel(self):
		global techList

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		for iLoopTech in techList:
			#アイコンはテクノロジ。クリックでペディアを開く
			#WidgetTypes.WIDGET_GENERALで何も起こらなくなる
			szName = "MonopolyButton" + str(iLoopTech)
			screen.setImageButton(szName, gc.getTechInfo(iLoopTech).getButton(), 0, 0, 20, 20, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1)
			screen.hide(szName)

		return 0

	#独占している技術のボタンを更新
	def updateMonopolyPanel(self):
		# x方向のmaxは487
		global civList
		global techList
		global MonopolyPanelList
		global g_szMonoText

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		prevMonoPanel = set(MonopolyPanelList)
		MonopolyPanelList = []

		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			xResolution = screen.getXResolution()

			#独占技術！
			szString = localText.getText('TXT_KEY_MONOPOLY_TECHNOLOGY', ()) + ":"
			if (CyGame().getCurrentLanguage() != 5):
				szString = "<font=2>" + szString + "</font>"
			iXOffset = 323 + ((xResolution - 1024) / 2)
			if (szString != g_szMonoText):
				screen.setText("MonopolyText", "Background", szString, CvUtil.FONT_LEFT_JUSTIFY, iXOffset, 25, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				g_szMonoText = szString
			screen.show("MonopolyText")

			iTextWidth = CyInterface().determineWidth(szString)
			iXOffset += 5 + iTextWidth
			iMaxTech = (376 - iTextWidth)/22

			tradeData = TradeData()
			tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES

			iTechCount = 0

			eGetActivePlayer = gc.getGame().getActivePlayer()
			eGetActiveTeam = gc.getPlayer(eGetActivePlayer).getTeam()
			pActiveTeam = gc.getTeam(eGetActiveTeam)
			pActiveCanTradeItem = gc.getPlayer(eGetActivePlayer).canTradeItem

			for iLoopTech in techList:
				#全ての技術から自分が持っているテクノロジを対象にする
				if(pActiveTeam.isHasTech(iLoopTech)):
					bMonopoly = True
					for iLoopPlayer in civList:
						eGetLoopPlayer = gc.getPlayer(iLoopPlayer)
						eGetLoopTeam = eGetLoopPlayer.getTeam()
						pLoopTeam = gc.getTeam(eGetLoopTeam)
						#自分自身、未接触、蛮族、小文明は除外
						if (iLoopPlayer != eGetActivePlayer and eGetLoopPlayer.isAlive() and pLoopTeam.isHasMet(eGetActiveTeam)):

							#チームメイトは除外
							if ((eGetActiveTeam == eGetLoopTeam) or (not pActiveTeam.isTechTrading() and not pLoopTeam.isTechTrading()) or (not pLoopTeam.isHasTech(iLoopTech))):
								continue

							#テクノロジを持っている文明の中でトレード不可能な文明があるなら独占ではない
							tradeData.iData = iLoopTech
							if (not pActiveCanTradeItem(iLoopPlayer, tradeData, False)):
								bMonopoly = False
								break

					if (bMonopoly):
						szName = "MonopolyButton" + str(iLoopTech)
						screen.moveItem(szName, iXOffset + 22 * iTechCount, 28, -0.3)
						if (iLoopTech in prevMonoPanel):
							prevMonoPanel.remove(iLoopTech)
						screen.show(szName)
						MonopolyPanelList.append(iLoopTech)
						iTechCount += 1
					if(iTechCount >= iMaxTech):
						break
		else:
			screen.hide("MonopolyText")

		for iLoopTech in prevMonoPanel:
			screen.hide("MonopolyButton" + str(iLoopTech))

		return 0

	def updateCompressTradeResourcePanel(self, iBaseY, hasResources, bTradeTo):
		global civList
		global civName
		global techList
		global TRPOption2
		global bShowSingleResource
		global TradePanelListFrom
		global TradePanelListTo
		global TradePanelResTo
		global TradePanelResFrom

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screenhide = screen.hide
		screenshow = screen.show
		iActivePlayer = gc.getGame().getActivePlayer()

		#先に全てのオブジェクトを非表示にする
		if (bTradeTo):
			TradePanelList = TradePanelListTo
			TradePanelResList = TradePanelResTo
			szComponentName = "TradeResourceTo"
		else:
			TradePanelList = TradePanelListFrom
			TradePanelResList = TradePanelResFrom
			szComponentName = "TradeResourceFrom"
			for i in xrange(3):
				screenhide("TradeResourceWatchCiv" + str(i))
		szTechName = "TradeResourceTechButton" + str(iActivePlayer) + "_"
		szResName = "TradeResourceResButton" + str(iActivePlayer) + "_"

		for item in TradePanelList:
			screenhide(szTechName + str(item[1]))
			screenhide(szTechName + str(item[1]) + "Counter")
		for item in TradePanelResList:
			screenhide(szResName + str(item[1]))
			screenhide(szResName + str(item[1]) + "Counter")

		screenhide(szComponentName + "Title")

		if (bTradeTo):
			TradePanelListTo = []
			TradePanelList = TradePanelListTo
			TradePanelResTo = []
			TradePanelResList = TradePanelResTo
		else:
			TradePanelListFrom = []
			TradePanelList = TradePanelListFrom
			TradePanelResFrom = []
			TradePanelResList = TradePanelResFrom

		screenhide(szComponentName + "BackgroundPanel")

		#位置とか
		iMaxCount = 11
		iIconSize = 36

		iTotalPanelHeight = 0

		#表示すべき状態かチェック（都市画面、地球儀状態等）
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW and not CyEngine().isGlobeviewUp()):
			tradeTechData = TradeData()
			tradeResData = TradeData()
			tradeTechData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
			tradeResData.ItemType = TradeableItems.TRADE_RESOURCES

			iXoffset = screen.getXResolution() - 24

			eGetActivePlayer = gc.getPlayer(iActivePlayer)
			eGetActiveTeam = eGetActivePlayer.getTeam()

			if (bTradeTo):
				hasResList = hasResources
				pPlayerCanTradeItem = eGetActivePlayer.canTradeItem
				pSrcPlayerNumBonus = eGetActivePlayer.getNumTradeableBonuses
			else:
				global AllBonus
				hasResList = AllBonus.difference(hasResources)
				iDestPlayer = iActivePlayer
				for i in xrange(len(sWatchList)):
					screenshow("TradeResourceWatchCiv" + str(i))

			lCivList = []
			for iLoopPlayer in civList:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				pLoopTeam = pLoopPlayer.getTeam()
				if (iLoopPlayer != iActivePlayer and pLoopPlayer.isAlive() and gc.getTeam(pLoopTeam).isHasMet(eGetActiveTeam) and eGetActiveTeam != pLoopTeam):
					lCivList.append(iLoopPlayer)

			iTechCount = 0
			for iLoopTech in techList:
				tradeTechData.iData = iLoopTech
				iNumHasTechCiv = 0
				szHelpText = gc.getTechInfo(iLoopTech).getText() + u":"
				szCivImage = u""
				bWatchCiv = False

				for iLoopPlayer in lCivList:
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if (bTradeTo):
						iDestPlayer = iLoopPlayer
					else:
						pPlayerCanTradeItem = pLoopPlayer.canTradeItem


					if (pPlayerCanTradeItem(iDestPlayer, tradeTechData, True)):
						if (iNumHasTechCiv < 3):
							szCivImage += "<img=" + gc.getCivilizationInfo(pLoopPlayer.getCivilizationType()).getButton() + " size=12></img>"
						iNumHasTechCiv += 1
						szHelpText += u"\n<color=%d,%d,%d,%d>%s</color>"%(pLoopPlayer.getPlayerTextColorR(), pLoopPlayer.getPlayerTextColorG(), pLoopPlayer.getPlayerTextColorB(), pLoopPlayer.getPlayerTextColorA(), pLoopPlayer.getName())
						if (iLoopPlayer in sWatchList):
							bWatchCiv = True

				if (iNumHasTechCiv > 0):
					szName = szTechName + str(iLoopTech)
					iX = iXoffset - iTechCount * iIconSize
					iY = iBaseY + iTotalPanelHeight
					screen.moveItem(szName, iX, iY, -0.3)
					screenshow(szName)
					if (iNumHasTechCiv > 3):
						szText = "<font=1>%d</font>"%(iNumHasTechCiv)
						if (bWatchCiv):
							szText = "<color=255,0,0>" + szText + "</color>"
						screen.setHelpLabel(szName + "Counter", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, iX + 10, iY + 20, -0.3, FontTypes.SMALL_FONT, szHelpText)
					else:
						screen.setHelpLabel(szName + "Counter", "Background", szCivImage, CvUtil.FONT_CENTER_JUSTIFY, iX + 10, iY + 19, -0.3, FontTypes.SMALL_FONT, szHelpText)
					screenshow(szName + "Counter")
					TradePanelList.append((iActivePlayer, iLoopTech, True))
					iTechCount += 1

			if (iTechCount > 0):
				iTotalPanelHeight += 30

			iBonusCount = 0
			for iLoopBonus in hasResList:
				tradeResData.iData = iLoopBonus
				iNumHasResCiv = 0
				szHelpText = gc.getBonusInfo(iLoopBonus).getText() + u":"
				szCivImage = u""
				bWatchCiv = False

				for iLoopPlayer in lCivList:
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if (bTradeTo):
						iDestPlayer = iLoopPlayer
					else:
						pSrcPlayerNumBonus = pLoopPlayer.getNumTradeableBonuses
						pPlayerCanTradeItem = pLoopPlayer.canTradeItem

					if (pPlayerCanTradeItem(iDestPlayer, tradeResData, True)):
						iResCount = 2
						if (bShowSingleResource):
							iResCount = 1
						if (pSrcPlayerNumBonus(iLoopBonus) >= iResCount):
							if (iNumHasResCiv < 3):
								szCivImage += "<img=" + gc.getCivilizationInfo(pLoopPlayer.getCivilizationType()).getButton() + " size=8></img>"
							iNumHasResCiv += 1
							szHelpText += u"\n<color=%d,%d,%d,%d>%s</color>"%(pLoopPlayer.getPlayerTextColorR(), pLoopPlayer.getPlayerTextColorG(), pLoopPlayer.getPlayerTextColorB(), pLoopPlayer.getPlayerTextColorA(), pLoopPlayer.getName())
							if (iLoopPlayer in sWatchList):
								bWatchCiv = True


				if (iNumHasResCiv > 0):
					szName = szResName + str(iLoopBonus)
					iX = iXoffset - iBonusCount * iIconSize
					iY = iBaseY + iTotalPanelHeight
					screen.moveItem(szName, iX, iY, -0.3)
					screenshow(szName)
					if (iNumHasResCiv > 3):
						szText = "<font=1>%d</font>"%(iNumHasResCiv)
						if (bWatchCiv):
							szText = "<color=255,0,0>" + szText + "</color>"
						screen.setHelpLabel(szName + "Counter", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, iX + 10, iY + 18, -0.3, FontTypes.SMALL_FONT, szHelpText)
					else:
						screen.setHelpLabel(szName + "Counter", "Background", szCivImage, CvUtil.FONT_CENTER_JUSTIFY, iX + 10, iY + 16, -0.3, FontTypes.SMALL_FONT, szHelpText)
					screenshow(szName + "Counter")
					TradePanelResList.append((iActivePlayer, iLoopBonus))
					iBonusCount += 1

			szName = szComponentName + "Title"
			iX = iXoffset - 120
			iY = iBaseY - 14
			screen.moveItem(szName, iX, iY, -0.3)
			screenshow(szName)
			#背景パネルを表示
			if (iTechCount > iMaxCount):
				iMaxCount = iTechCount
			if (iBonusCount > iMaxCount):
				iMaxCount = iBonusCount
			szName = szComponentName + "BackgroundPanel"
			iX = iXoffset - iIconSize * (iMaxCount - 1) - 7
			iY = iBaseY - 12
			iWidth = iIconSize * iMaxCount + 8
			if (iBonusCount > 0):
				iTotalPanelHeight += 30
			else:
				iTotalPanelHeight += 2

			iHeight = iTotalPanelHeight + 16
			screen.setPanelSize(szName, iX, iY, iWidth, iHeight)
			screenshow(szName)

		return iTotalPanelHeight
