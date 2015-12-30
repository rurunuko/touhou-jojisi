## HOF MOD V1.61.001
## Based upon Gillmer J. Derge's Civ4lerts.py

from CvPythonExtensions import *
import CvUtil
import CvConfigParser
import Popup as PyPopup
import CvCameraControls
import AlertsLog

cam = CvCameraControls.CvCameraControls()

gc = CyGlobalContext()
localText = CyTranslator()

#
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
CFG_Enabled = config.getboolean('More Civ4lerts', 'Enabled', False)
CFG_PopThreshold = config.getfloat('More Civ4lerts', 'PopThreshold', 1.0)
CFG_LandThreshold = config.getfloat('More Civ4lerts', 'LandThreshold', 1.0)
CFG_CheckForCityBorderExpansion = config.getboolean('More Civ4lerts', 'CheckForCityBorderExpansion', False)
CFG_CheckForNewTrades = config.getboolean('More Civ4lerts', 'CheckForNewTrades', False)
CFG_CheckForDomPopVictory = config.getboolean('More Civ4lerts', 'CheckForDomPopVictory', False)
CFG_CheckForDomLandVictory = config.getboolean('More Civ4lerts', 'CheckForDomLandVictory', False)
addMessage = AlertsLog.AlertsLog().AlertsLogMessage

class MoreCiv4lerts:

	def __init__(self, eventManager):
		## Init event handlers
		MoreCiv4lertsEvent(eventManager)

class AbstractMoreCiv4lertsEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super( AbstractMoreCiv4lertsEvent, self).__init__(*args, **kwargs)

class MoreCiv4lertsEvent(AbstractMoreCiv4lertsEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(MoreCiv4lertsEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("EndGameTurn", self.OnEndGameTurn)
		eventManager.addEventHandler("cityAcquired", self.OnCityAcquired)
		eventManager.addEventHandler("cityBuilt", self.OnCityBuilt)
		eventManager.addEventHandler("cityRazed", self.OnCityRazed)
		eventManager.addEventHandler("cityLost", self.OnCityLost)
		eventManager.addEventHandler("techAcquired", self.OnTechAcquired)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)

		self.eventMgr = eventManager
		self.CurrAvailTechTrades = {}
		self.PrevAvailTechTrades = {}
		self.AvailVassals = []
		self.lastDomLimitMsgTurn = 0
		self.lastPopCount = 0
		self.lastLandCount = 0
		self.TechList = []

## -----------------------------------------------------------

	def OnEndGameTurn(self, argsList):
		iGameTurn = argsList[0]
		if (not CFG_Enabled):
			return
		if (not (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory or CFG_CheckForCityBorderExpansion or CFG_CheckForNewTrades)):
			return
		iPlayer = gc.getGame().getActivePlayer()
		self.CheckForAlerts(iPlayer, gc.getPlayer(iPlayer).getTeam(), True)

	def OnCityAcquired(self, argsList):
		owner,playerType,city,bConquest,bTrade = argsList
		iPlayer = city.getOwner()
		if (not (CFG_Enabled and CFG_CheckForDomPopVictory)):
			return
		if (iPlayer == gc.getGame().getActivePlayer()):
			self.CheckForAlerts(iPlayer, gc.getPlayer(iPlayer).getTeam(), False)

	def OnCityBuilt(self, argsList):
		city = argsList[0]
		iPlayer = city.getOwner()
		if (not (CFG_Enabled and (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory))):
			return
		if (iPlayer == gc.getGame().getActivePlayer()):
			self.CheckForAlerts(iPlayer, gc.getPlayer(iPlayer).getTeam(), False)

	def OnCityRazed(self, argsList):
		city, iPlayer = argsList
		if (not (CFG_Enabled and (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory))):
			return
		if (iPlayer == gc.getGame().getActivePlayer()):
			self.CheckForAlerts(iPlayer, gc.getPlayer(iPlayer).getTeam(), False)

	def OnCityLost(self, argsList):
		city = argsList[0]
		iPlayer = city.getOwner()
		if (not (CFG_Enabled and (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory))):
			return
		if (iPlayer == gc.getGame().getActivePlayer()):
			self.CheckForAlerts(iPlayer, gc.getPlayer(iPlayer).getTeam(), False)

	def OnTechAcquired(self, argsList):
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object

		if (iPlayer == gc.getGame().getActivePlayer() and len(self.TechList) > 0):
			try:
				self.TechList.remove(iTechType)
			except ValueError:
				pass

	def onGameStart(self, argsList):
		"""Called at the start of the game"""
		self.OnStartInitTechList()

	def onLoadGame(self, argsList):
		self.OnStartInitTechList()
		return 0

	def OnStartInitTechList(self):
		self.TechList = []
		TechListappend = self.TechList.append
		ActiveTeam = gc.getTeam(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam())
		for iLoopTech in xrange(gc.getNumTechInfos()):
			if (not ActiveTeam.isHasTech(iLoopTech)):
				TechListappend(iLoopTech)

	def CheckForAlerts(self, iPlayer, iActiveTeam, BeginTurn):
	##Added "else: pass" code to diagnose strange results - might be related to indent issues
		ourPop = 0
		ourLand = 0
		totalPop = 0
		totalLand = 0
		LimitPop =0
		LimitLand = 0
		DomVictory = 3
		popGrowthCount = 0
		currentTurn = gc.getGame().getGameTurn()
		pActiveTeam = gc.getTeam(iActiveTeam)
		bCheckDLV = CFG_Enabled and CFG_CheckForDomLandVictory
		bCheckCBE = CFG_Enabled and CFG_CheckForCityBorderExpansion
		bCheckCulExpBeginTurn = BeginTurn and (bCheckDLV or bCheckCBE)

		if ((CFG_Enabled and CFG_CheckForDomPopVictory) or bCheckCulExpBeginTurn):
			# Check for cultural expansion
			team = gc.getGame().getActiveTeam()
			iPlayerCount = 0
			for loopPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
				pLoopPlayer = gc.getPlayer(loopPlayer)
				if (not pLoopPlayer.isNone() and pLoopPlayer.isAlive()):
					if (pLoopPlayer.getTeam() == team):
						iPlayerCount += 1

			iNumCulLvl = gc.getNumCultureLevelInfos() - 1
			for loopPlayer in xrange(iPlayerCount):
				pLoopPlayer = gc.getPlayer(loopPlayer)
				for loopCity in xrange(pLoopPlayer.getNumCities()):
					city = pLoopPlayer.getCity(loopCity)
					if ((city.getFoodTurnsLeft() == 1 and not city.isFoodProduction()) and not city.AI_isEmphasize(5) and city.foodDifference(True) > 0):
						popGrowthCount += 1
					if (bCheckCulExpBeginTurn):
						if (city.getCultureLevel() != iNumCulLvl):
							if ((city.getCulture(loopPlayer) + city.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) >= city.getCultureThreshold()
							and (city.getCulture(loopPlayer) < city.getCultureThreshold())):
								message = localText.getText("TXT_KEY_MORECIV4LERTS_CITY_TO_EXPAND", (city.getName(),))
								icon = "Art/Interface/Buttons/Process/processculture.dds"
								addMessage(iPlayer, message, icon, gc.getInfoTypeForString("COLOR_CULTURE_RATE"), city.getX(), city.getY(), 3, city.getID(), -1, True, True)

		# Check Domination Limit
		if ((CFG_Enabled and (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory)) and gc.getGame().isVictoryValid(DomVictory)):

			# Population Limit
			if (CFG_Enabled and CFG_CheckForDomPopVictory):
				VictoryPopPercent = 0.0
				VictoryPopPercent = gc.getGame().getAdjustedPopulationPercent(DomVictory) * 1.0
				totalPop = gc.getGame().getTotalPopulation()
				LimitPop = int((totalPop * VictoryPopPercent) / 100.0)
				ourPop = pActiveTeam.getTotalPopulation()
				if (totalPop > 0):
					popPercent = (ourPop * 100.0) / totalPop
					NextpopPercent = ((ourPop + popGrowthCount) * 100.0) / totalPop
				else:
					popPercent = 0.0
					NextpopPercent = 0.0

				if (totalPop > 1 and (currentTurn != self.lastDomLimitMsgTurn or (ourPop + popGrowthCount) != self.lastPopCount)):
					self.lastPopCount = ourPop + popGrowthCount
					if (popPercent >= VictoryPopPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_EXCEEDS_LIMIT",
								(ourPop, (u"%.2f%%" % popPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)

					elif (popGrowthCount > 0 and NextpopPercent >= VictoryPopPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_EXCEEDS_LIMIT",
								(ourPop, popGrowthCount, (u"%.2f%%" % NextpopPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)

					elif (popGrowthCount > 0 and (VictoryPopPercent - NextpopPercent < CFG_PopThreshold)):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_CLOSE_TO_LIMIT",
								(ourPop, popGrowthCount, (u"%.2f%%" % NextpopPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)

					elif (popGrowthCount > 0 and (VictoryPopPercent - popPercent < CFG_PopThreshold)):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_CLOSE_TO_LIMIT",
								(ourPop, (u"%.2f%%" % popPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)

			# Land Limit
			if (bCheckDLV):
				VictoryLandPercent = 0.0
				VictoryLandPercent = gc.getGame().getAdjustedLandPercent(DomVictory) * 1.0
				totalLand = gc.getMap().getLandPlots()
				LimitLand = int((totalLand * VictoryLandPercent) / 100.0)
				ourLand = pActiveTeam.getTotalLand()
				if (totalLand > 0):
					landPercent = (ourLand * 100.0) / totalLand
				else:
					landPercent = 0.0
				if (BeginTurn or currentTurn != self.lastDomLimitMsgTurn or ourLand != self.lastLandCount):
					self.lastLandCount = ourLand
					if (landPercent > VictoryLandPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_EXCEEDS_LIMIT",
								(ourLand, (u"%.2f%%" % landPercent), LimitLand, (u"%.2f%%" % VictoryLandPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)
					elif (VictoryLandPercent - landPercent < CFG_LandThreshold):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_CLOSE_TO_LIMIT",
								(ourLand, (u"%.2f%%" % landPercent), LimitLand, (u"%.2f%%" % VictoryLandPercent)))
						addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), 0, 0, 3, -1, -1, False, False)

		#save turn num
		if ((CFG_Enabled and (CFG_CheckForDomPopVictory or CFG_CheckForDomLandVictory))):
		    self.lastDomLimitMsgTurn = currentTurn

		# new trades
		if (BeginTurn and (CFG_Enabled and CFG_CheckForNewTrades)):
			PlayerHasTech = ""
			self.getTechForTrade(iPlayer, pActiveTeam)
			for iLoopPlayer, CurrTechCanTrade in self.CurrAvailTechTrades.iteritems():
				#Did he have trades avail last turn
				if (self.PrevAvailTechTrades.has_key(iLoopPlayer)):
					PrevTechCanTrade = self.PrevAvailTechTrades.get(iLoopPlayer)
					#Any trades this turn?
					if (CurrTechCanTrade):
						#compare this turn's vs last turn's trades
						if (len(CurrTechCanTrade.difference(PrevTechCanTrade)) > 0):
							if (PlayerHasTech != ""):
								PlayerHasTech += ", "
							PlayerHasTech += gc.getPlayer(iLoopPlayer).getName()
				#nothing last turn, how about this turn?
				elif (CurrTechCanTrade):
					if (PlayerHasTech != ""):
						PlayerHasTech += ", "
					PlayerHasTech += gc.getPlayer(iLoopPlayer).getName()

				#save curr trades for next time
				self.PrevAvailTechTrades[iLoopPlayer] = CurrTechCanTrade

			if (PlayerHasTech != ""):
				message = localText.getText("TXT_KEY_MORECIV4LERTS_NEW_TECH_AVAIL", (PlayerHasTech,))
				addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_TECH_TEXT"), 0, 0, 2, -1, -1, False, False)

			PlayerTradeVassal = ""

			for iLoopPlayer in self.AvailVassals:

				if (PlayerTradeVassal != ""):
					PlayerTradeVassal += ", "
				PlayerTradeVassal += gc.getPlayer(iLoopPlayer).getName()

			if (PlayerTradeVassal != ""):
				message = localText.getText("TXT_KEY_MORECIV4LERTS_VASSAL_AVAIL", (PlayerTradeVassal,))
				addMessage(iPlayer, message, None, gc.getInfoTypeForString("COLOR_PLAYER_BLUE_TEXT"), 0, 0, 2, -1, -1, False, False)

	def getTechForTrade(self, iPlayer, pActiveTeam):
		iActiveTeam = pActiveTeam.getID()
		tradeTech = TradeData()
		tradeTech.ItemType = TradeableItems.TRADE_TECHNOLOGIES
		tradeVassal = TradeData()
		tradeVassal.ItemType = TradeableItems.TRADE_VASSAL
		self.CurrAvailTechTrades.clear
		self.AvailVassals = []
		AvailVassalappend = self.AvailVassals.append

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			currentTeam = currentPlayer.getTeam()

			TechCanTrade = set()
			TechCanTradeappend = TechCanTrade.add
			if (not currentPlayer.isAlive() or currentPlayer.isBarbarian() or currentPlayer.isMinorCiv()):
				continue
			if (iLoopPlayer != iPlayer):
				if (gc.getTeam(currentTeam).isHasMet(iActiveTeam)):
					if (pActiveTeam.isTechTrading() or gc.getTeam(currentTeam).isTechTrading()):
						for iLoopTech in self.TechList:
							tradeTech.iData = iLoopTech
							if (currentPlayer.canTradeItem(iPlayer, tradeTech, False)):
								if (currentPlayer.getTradeDenial(iPlayer, tradeTech) == DenialTypes.NO_DENIAL): # will trade
									TechCanTradeappend(iLoopTech)
					self.CurrAvailTechTrades[iLoopPlayer] = TechCanTrade

					if (currentPlayer.canTradeItem(iPlayer, tradeVassal, False)):
						if (currentPlayer.getTradeDenial(iPlayer, tradeVassal) == DenialTypes.NO_DENIAL): # will trade
							AvailVassalappend(iLoopPlayer)

		return

class MoreCiv4lertsOption:

	def setCGEOption(self, Section, Key, Value):
		global CFG_Enabled
		global CFG_PopThreshold
		global CFG_LandThreshold
		global CFG_CheckForCityBorderExpansion
		global CFG_CheckForNewTrades
		global CFG_CheckForDomPopVictory
		global CFG_CheckForDomLandVictory

		if (Key == 'Enabled'):
			CFG_Enabled = Value
		elif (Key == 'PopThreshold'):
			CFG_PopThreshold = Value
		elif (Key == 'LandThreshold'):
			CFG_LandThreshold = Value
		elif (Key == 'CheckForCityBorderExpansion'):
			CFG_CheckForCityBorderExpansion = Value
		elif (Key == 'CheckForNewTrades'):
			CFG_CheckForNewTrades = Value
		elif (Key == 'CheckForDomPopVictory'):
			CFG_CheckForDomPopVictory = Value
		elif (Key == 'CheckForDomLandVictory'):
			CFG_CheckForDomLandVictory = Value
