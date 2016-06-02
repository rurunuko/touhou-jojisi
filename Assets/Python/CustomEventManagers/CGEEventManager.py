# CGE Event Manager
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import Popup as PyPopup
import CvUtil
import CvConfigParser
import AlertsLog
import TradeResourcePanel
import ExecutiveBriefing
import UnitPlacement
import CGEDebug
import CGEOptionControl
import CityInfoPanelPS
import UserPrefs
import CGEUtils
import SdToolKitAdvanced

gc = CyGlobalContext()
localText = CyTranslator()
addMessage = AlertsLog.AlertsLog().AlertsLogMessage

CFG_Alert_Interference = True
CFG_Alert_Obsolete = True
CFG_Alert_SpyStealTech = True

class CGEEventManager:

	def __init__(self, eventManager):
		CGEEvent(eventManager, self)

		self.reminders = []

		CGEEvents = {
			CvUtil.EventTRPOption : ('TRPOption', self.__eventTRPOptionApply, self.__eventTRPOptionBegin),
			CvUtil.EventReminderStore  : ('ReminderStore', self.__eventReminderStoreApply,  self.__eventReminderStoreBegin),
			CvUtil.EventReminderRecall : ('ReminderRecall', self.__eventReminderRecallApply, self.__eventReminderRecallBegin),
			CvUtil.EventSpyMoveToCity : ('SpyMoveToCity', self.__eventSpyMoveToCityApply, self.__eventSpyMoveToCityBegin),
			CvUtil.EventTestWarning : ('CGETestWarning', self.__eventCGETestWarningApply, self.__eventCGETestWarningBegin),
		}
		eventManager.Events.update(CGEEvents)

	def __eventTRPOptionBegin(self, argslist):
		return 0

	def __eventTRPOptionApply(self, playerID, userData, popupReturn):
		iOpt1 = popupReturn.getSelectedPullDownValue(0)
		iOpt2 = popupReturn.getSelectedPullDownValue(1)
		iOpt3 = popupReturn.getSelectedPullDownValue(2)
		iOpt4 = popupReturn.getSelectedPullDownValue(3)
		sOpt = set()
### >>> CGE-LE 1.01 - begin
		for i in range(4,6):
### >>> CGE-LE 1.01 - end
			iValue = popupReturn.getSelectedPullDownValue(i)
			if (iValue != -1):
				sOpt.add(iValue)
### >>> CGE-LE 1.01 - begin
		TradeResourcePanel.TradeResourcePanel().setTradeResourcePanelOption(iOpt1, iOpt2, iOpt3, iOpt4, sOpt)
### >>> CGE-LE 1.01 - end
		return 0

	def __eventReminderStoreBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventReminderStore, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setHeaderString(localText.getText('TXT_KEY_REMINDER_SET_REMINDER', ()))
		popup.createPullDown(2)
### >>> CGE-LE 1.03 - begin
		popup.addPullDownString(localText.getText("TXT_KEY_REMINDER_PRESET", ()), 0, 2)
		
		iActivePlayer = gc.getGame().getActivePlayer()
		pActiveTeam = gc.getTeam(gc.getPlayer(iActivePlayer).getTeam())
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			if (not currentPlayer.isAlive() or currentPlayer.isBarbarian() or currentPlayer.isMinorCiv()):
				continue
			currentTeam = currentPlayer.getTeam()
			if (iLoopPlayer != iActivePlayer and pActiveTeam.isHasMet(currentTeam)):
				popup.addPullDownString(currentPlayer.getName(), iLoopPlayer, 2)
		
#		for i, szString in enumerate(UserPrefs.reminderPreset):
#			popup.addPullDownString(szString, -i, 2)
### <<< CGE-LE 1.03 - end
		popup.createEditBox("", 1)
		popup.createSpinBox(0, "", 1, 1, 200, 0)
		popup.createPythonPullDownXY("",3, 50, 50)
### >>> CGE-LE 1.03 - begin
		for i in xrange(10,0,-1):
### <<< CGE-LE 1.03 - end
			popup.addPullDownString(str(i) + localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()), i, 3)
		popup.addButton("Ok")
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventReminderStoreApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() == 0):
			iSpinValue = popupReturn.getSpinnerWidgetValue(0)
			if (iSpinValue != 1):
				reminderTurn = iSpinValue + gc.getGame().getGameTurn()
			else:
				reminderTurn = popupReturn.getSelectedPullDownValue(3) + gc.getGame().getGameTurn()
			iPreset = popupReturn.getSelectedPullDownValue(2)
### >>> CGE-LE 1.03 - begin
			if (iPreset > 0):
				reminderText = gc.getPlayer(iPreset).getName()
			elif (iPreset < 0):
				reminderText = UserPrefs.reminderPreset[iPreset]
### <<< CGE-LE 1.03 - end
			else:
				reminderText = popupReturn.getEditBoxString(1)
			newEntry = (reminderTurn, reminderText)
			self.reminders.append(newEntry)
		self._reminderStoreData()

	def __eventReminderRecallBegin(self, argsList):
		thisTurn = gc.getGame().getGameTurn() + 1

		szMsg = u""
		for (iTurn, message) in self.reminders:
			if (iTurn == thisTurn):
				CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)
				szMsg += message + "\n"

		if (szMsg != ""):
			popup = PyPopup.PyPopup(CvUtil.EventReminderRecall, EventContextTypes.EVENTCONTEXT_SELF)
			popup.setHeaderString(localText.getText('TXT_KEY_REMINDER_REMINDER', ()) + "!")
			popup.setBodyString(szMsg)
			popup.launch(True)

			queue = self.reminders[:]
			self.reminders = []
			reminderRestore = self.reminders.append
			for (iTurn, message) in queue:
				if (iTurn > thisTurn):
					reminderRestore((iTurn, message))
			self._reminderStoreData()

	def __eventReminderRecallApply(self, playerID, userData, popupReturn):
		message = "eventReminderRecallApply"

	def __eventCGETestWarningBegin(self, argsList):
		#CGEDebug.CGEDebug().CGETestWarning()
		pass

	def __eventCGETestWarningApply(self, playerID, userData, popupReturn):
		#CyInterface().exitingToMainMenu("", False)
		pass

	def __eventSpyMoveToCityBegin(self, argslist):
		return 0

	def __eventSpyMoveToCityApply(self, playerID, userData, popupReturn):
		iOpt1 = popupReturn.getSelectedPullDownValue(0)

		CGEUtils.CGEUtils().SpyMoveToCityExec(iOpt1)
		return 0

	def reminderInit(self):
		#if (not SdToolKitAdvanced.sdObjectExists("CGEReminder", gc.getGame())):
		#	SdToolKitAdvanced.sdObjectInit("CGEReminder", gc.getGame(), {"Reminder": []})
		self.reminders = []

	def reminderLoad(self):
		if (SdToolKitAdvanced.sdObjectExists("CGEReminder", gc.getGame())):
			self.reminders = SdToolKitAdvanced.sdObjectGetVal("CGEReminder", gc.getGame(), "Reminder")
		else:
			#SdToolKitAdvanced.sdObjectInit("CGEReminder", gc.getGame(), {"Reminder": []})
			self.reminders = []

	def _reminderStoreData(self):
		if (not SdToolKitAdvanced.sdObjectExists("CGEReminder", gc.getGame())):
			SdToolKitAdvanced.sdObjectInit("CGEReminder", gc.getGame(), {"Reminder": []})
		SdToolKitAdvanced.sdObjectSetVal("CGEReminder", gc.getGame(), "Reminder", self.reminders)

class AbstractCGEEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractCGEEvent, self).__init__(*args, **kwargs)

class CGEEvent(AbstractCGEEvent):

	def __init__(self, eventManager, CGEManager, *args, **kwargs):
		super(CGEEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("techAcquired", self.onTechAcquired)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("setPlayerAlive", self.onSetPlayerAlive)
		eventManager.addEventHandler("cityDoTurn", self.onCityDoTurn)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("victory", self.onVictory)
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("EndGameTurn", self.OnEndGameTurn)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("firstContact", self.onFirstContact)
		eventManager.addEventHandler("selectionGroupPushMission", self.onSelectionGroupPushMission)
		eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)

		self.eventMgr = eventManager
		self.CGEManager = CGEManager

		global CFG_Alert_Interference
		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
		if (config != None):
			CFG_Alert_Interference = config.getboolean("CGE Alerts", "Interference", True)
			CFG_Alert_Obsolete = config.getboolean("CGE Alerts", "Obsolete", True)
			CFG_Alert_SpyStealTech = config.getboolean("CGE Alerts", "SpyStealTech", True)

		self.hasCGEDLL = False
		try:
			if (gc.isCGEBuild()):
				self.hasCGEDLL = True
		except:
			pass
		self.iStealTechMission = -1

	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		eventType,key,mx,my,px,py = argsList

		if (eventType == 6): # self.EventKeyDown=6
			theKey=int(key)

			# Ctrl+F4 (Toggle TradeResourcePanel)
			if (theKey == int(InputTypes.KB_F4) and self.eventMgr.bCtrl):
				#CyInterface().addImmediateMessage("KeyEvent: Ctrl+F4","")
				TradeResourcePanel.TradeResourcePanel().ToggleTradeResourcePanel()
				return 1

			# J (City Info Panel)
			if (theKey == int(InputTypes.KB_J)):
				pPlot = CyInterface().getSelectionPlot()
				if (pPlot.isCity()):
					pCity = pPlot.getPlotCity()
					#szCityName = pCity.getName()
					#CyInterface().addImmediateMessage("KeyEvent: J -> %s"%(szCityName),"")
					if (self.eventMgr.bShift):
						CityInfoPanelPS.CityInfoPanelPS().showCityTerrainInfo(pCity)
					else:
						CityInfoPanelPS.CityInfoPanelPS().toggleCityInfoPanelPS(pCity)
				return 1

			# Alt+M creates a reminder
			if (theKey == int(InputTypes.KB_M) and self.eventMgr.bAlt):
				self.eventMgr.beginEvent(CvUtil.EventReminderStore)
				return 1

		return 0

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList
		if (gc.getPlayer(iPlayer).isHuman()):
			AlertsLog.AlertsLog().AlertsLogStartTurn()
			# for APL compress mode
			if (CyInterface().getNumVisibleUnits() > 10 and gc.getTeam(gc.getGame().getActiveTeam()).getAtWarCount(False) == 0):
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			# Unit Placement Override Firaxis Bug
			UnitPlacement.UnitPlacement().doOverrideFiraxisBug()
			CGEUtils.CGEUtils().UpdateEspionagePoint()

	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList

		pPlayer = gc.getPlayer(iPlayer)
		if (iPlayer > -1 and not pPlayer.isBarbarian() and not pPlayer.isMinorCiv()):
			if (CFG_Alert_Interference):
				iActivePlayer = gc.getGame().getActivePlayer()
				pActiveTeam = gc.getTeam(gc.getPlayer(iActivePlayer).getTeam())
				iPlayerTeam = pPlayer.getTeam()
				if (pActiveTeam.isHasMet(iPlayerTeam)):
					szWar = u""
					szTrade = u""
					tradeData = TradeData()
					iPlayerCanTradeItem = pPlayer.canTradeItem
					iPlayerGetTradeDenial = pPlayer.getTradeDenial
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						currentPlayer = gc.getPlayer(iLoopPlayer)
						if (not currentPlayer.isAlive() or currentPlayer.isBarbarian() or currentPlayer.isMinorCiv()):
							continue
						currentTeam = currentPlayer.getTeam()
						if (iLoopPlayer != iPlayer and iLoopPlayer != iActivePlayer and pActiveTeam.isHasMet(currentTeam)):
							if (gc.getTeam(iPlayerTeam).isHasMet(currentTeam) and pPlayer.canTradeWith(iLoopPlayer)):
								tradeData.iData = iLoopPlayer
								tradeData.ItemType = TradeableItems.TRADE_WAR
								if (iPlayerCanTradeItem(iActivePlayer, tradeData, True)):
									if (iPlayerGetTradeDenial(iActivePlayer, tradeData) == DenialTypes.NO_DENIAL):
										if (szWar != ""):
											szWar += ", "
										szWar += currentPlayer.getName()
								tradeData.ItemType = TradeableItems.TRADE_EMBARGO
								if (iPlayerCanTradeItem(iActivePlayer, tradeData, True)):
									if (iPlayerGetTradeDenial(iActivePlayer, tradeData) == DenialTypes.NO_DENIAL):
										if (szTrade != ""):
											szTrade += ", "
										szTrade += currentPlayer.getName()

					szString = u""
					if (szWar != ""):
						szString = localText.getText('TXT_KEY_TRADE_DECLARE_WAR_ON', ()) + ": " + szWar
					if (szTrade != ""):
						if (szString != ""):
							szString += ", "
						szString += localText.getText('TXT_KEY_TRADE_STOP_TRADING_WITH', ()) + ": " + szTrade
					if (szString != ""):
						szString = localText.getText('TXT_KEY_INTERFERE_ALERTS_MESSAGE', (pPlayer.getName(), szString))
						AlertsLog.AlertsLog().AlertsLogMessage(iActivePlayer, szString, None, 53, 0, 0, 2, -1, iPlayer, False, False)

		if (pPlayer.isHuman()):
			self.eventMgr.beginEvent(CvUtil.EventReminderRecall)

	def OnEndGameTurn(self, argsList):
		iGameTurn = argsList[0]

		if (CFG_Alert_SpyStealTech):
			iActPlayer = gc.getGame().getActivePlayer()
			pActPlayer = gc.getPlayer(iActPlayer)
			EspDict = dict()
			(loopUnit, iter) = pActPlayer.firstUnit(false)
			lUnit = []
			while (loopUnit):
				if (not loopUnit.isDead() and gc.getUnitInfo(loopUnit.getUnitType()).isSpy()):
					pPlot = loopUnit.plot()
					iTarget = pPlot.getOwner()
					if (loopUnit.canEspionage(pPlot) and iTarget != iActPlayer):
						lUnit.append((pPlot, iTarget))
						EspDict[iTarget] = set()
				(loopUnit, iter) = pActPlayer.nextUnit(iter, false)

			dTechDict = {}
			if (len(lUnit) > 0):
				ActiveTeam = gc.getTeam(pActPlayer.getTeam())
				lTechList = [iTech for iTech in range(gc.getNumTechInfos()) if (not ActiveTeam.isHasTech(iTech))]
				for iTarget in EspDict:
					TargetTeam = gc.getTeam(gc.getPlayer(iTarget).getTeam())
					dTechDict[iTarget] = [iTech for iTech in lTechList if (TargetTeam.isHasTech(iTech))]

			canDoEspMission = pActPlayer.canDoEspionageMission
			for (pPlot, iTarget) in lUnit:
				if (canDoEspMission(self.iStealTechMission, iTarget, pPlot, -1)):
					for iTech in dTechDict[iTarget]:
						if (canDoEspMission(self.iStealTechMission, iTarget, pPlot, iTech)):
							EspDict[iTarget].add(iTech)

			for (iTarget, items) in EspDict.items():
				if (len(items) == 0):
					continue
				szString = localText.getText("TXT_KEY_CGE_ALERT_STEAL_TECH", (gc.getPlayer(iTarget).getName(),))
				szTemp = ""
				for iTech in items:
					szTemp += ", " + gc.getTechInfo(iTech).getDescription()
				szString += szTemp[1:]
				AlertsLog.AlertsLog().AlertsLogMessage(iActPlayer, szString, None, gc.getInfoTypeForString("COLOR_TECH_TEXT"), 0, 0, 2, -1, iTarget, False, False)

		if (CFG_Alert_Obsolete):
			CGEUtils.CGEUtils().checkTechObsoleteAlert()

		CGEUtils.CGEUtils().checkSpyAlert()
		CGEUtils.CGEUtils().doAutoRecon()

		if (CGEUtils.CGEUtils().isAutoOrder()):
			iActPlayer = gc.getGame().getActivePlayer()
			pActPlayer = gc.getPlayer(iActPlayer)
			if (not (UserPrefs.DisableAutoOrderAtWar and gc.getTeam(pActPlayer.getTeam()).getAtWarCount(False) > 0)):
				(pLoopUnit, iter) = pActPlayer.firstUnit(False)
				while (pLoopUnit):
					if (iActPlayer == pLoopUnit.getOwner()):
						pUnitGroup = pLoopUnit.getGroup()
						if (pUnitGroup.getActivityType() <= ActivityTypes.ACTIVITY_AWAKE and pUnitGroup.getAutomateType() == AutomateTypes.NO_AUTOMATE):
							CGEUtils.CGEUtils().executeAutoOrder(pLoopUnit)
					(pLoopUnit, iter) = pActPlayer.nextUnit(iter, False)

	def onTechAcquired(self, argsList):
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object

		if (iPlayer > -1 and not gc.getPlayer(iPlayer).isBarbarian() and not gc.getPlayer(iPlayer).isMinorCiv()):
			TradeResourcePanel.TradeResourcePanel().UpdateTechList(iPlayer, iTechType)

	def onUnitBuilt(self, argsList):
		'Unit Completed'
		city = argsList[0]
		unit = argsList[1]

		# Unit Placement
		if (city.getOwner() == CyGame().getActivePlayer()):
			if (CGEUtils.CGEUtils().isAutoOrder()):
				if (not (UserPrefs.DisableAutoOrderAtWar and gc.getTeam(gc.getGame().getActiveTeam()).getAtWarCount(False) > 0)):
					CGEUtils.CGEUtils().executeAutoOrder(unit)
			UnitPlacement.UnitPlacement().doUnitOrder(city, unit)

	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'

		TradeResourcePanel.TradeResourcePanel().Init()
		TradeResourcePanel.TradeResourcePanel().ResetPanel(argsList)

	def onCityDoTurn(self, argsList):
		'City Production'

		ExecutiveBriefing.ExecutiveBriefing().onCityDoTurn(argsList)

	def onLoadGame(self, argsList):
		self.CGEManager.reminderLoad()
		CGEDebug.CGEDebug().CGEWarning()
		CityInfoPanelPS.CityInfoPanelPS().resetVictory()
		CGEOptionControl.CGEOptionControl().setCGEDLLOptions()
		UnitPlacement.UnitPlacement().loadGame()
		CGEUtils.CGEUtils().resetCGEUtils()
		self.getStealTechMissionNum()
		return 0

	def onGameStart(self, argsList):
		'Called at the start of the game'
		self.CGEManager.reminderInit()
		CGEDebug.CGEDebug().CGEWarning()
		CGEOptionControl.CGEOptionControl().setCGEDLLOptions()
		CityInfoPanelPS.CityInfoPanelPS().resetVictory()
		UnitPlacement.UnitPlacement().startGame()
		CGEUtils.CGEUtils().resetCGEUtils()
		self.getStealTechMissionNum()

	def onVictory(self, argsList):
		'Victory'
		iTeam, iVictory = argsList
		if (iVictory >= 0 and iVictory < gc.getNumVictoryInfos()):
			CityInfoPanelPS.CityInfoPanelPS().setVictory()

	def onPreSave(self, argsList):
		"called before a game is actually saved"
		UnitPlacement.UnitPlacement().storeDataOnPreSave()

	def getStealTechMissionNum(self):
		for iLoopEsp in xrange(gc.getNumEspionageMissionInfos()):
			MissionInfo = gc.getEspionageMissionInfo(iLoopEsp)
			if (not MissionInfo.isPassive()):
				if (MissionInfo.isTwoPhases() and MissionInfo.getBuyTechCostFactor() > 0):
					self.iStealTechMission = iLoopEsp

	def onFirstContact(self, argsList):
		'Contact'
		#iTeamX,iHasMetTeamY = argsList
		TradeResourcePanel.TradeResourcePanel().FirstContact()

	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]

		if (CGEUtils.CGEUtils().isAutoReconSetMode()):
			CGEUtils.CGEUtils().setAutoRecon(eOwner, eMission, listUnitIds[0])

	def onBuildingBuilt(self, argsList):
		'Building Completed'
		pCity, iBuildingType = argsList

		if (pCity.getOwner() == gc.getGame().getActivePlayer()):
			CGEUtils.CGEUtils().checkWonderPrereqBuildingAlert(iBuildingType)
			CGEUtils.CGEUtils().insertBuildingOrderQueue(pCity, iBuildingType)

class CGEEventOption:

	def setCGEOption(self, Section, Key, Value):
		global CFG_Alert_Interference

		if (Key == 'Interference'):
			CFG_Alert_Interference = Value
		if (Key == 'Obsolete'):
			CFG_Alert_Obsolete = Value
		if (Key == 'SpyStealTech'):
			CFG_Alert_SpyStealTech = Value
