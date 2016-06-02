## Copyright (c) 2005-2006, Gillmer J. Derge.

## This file is part of Civilization IV Alerts mod.
##
## Civilization IV Alerts mod is free software; you can redistribute
## it and/or modify it under the terms of the GNU General Public
## License as published by the Free Software Foundation; either
## version 2 of the License, or (at your option) any later version.
##
## Civilization IV Alerts mod is distributed in the hope that it will
## be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Civilization IV Alerts mod; if not, write to the Free
## Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA

__version__ = "$Revision: 1.2 $"
# $Source: /usr/local/cvsroot/Civ4lerts/src/main/python/Civ4lerts.py,v $

## Civ4lerts
## This class extends the built in event manager and overrides various
## event handlers to display alerts about important game situations.
##
## [*] = Already implemented in the Civ4lerts mod
## [o] = Partially implemented in the Civ4lerts mod
## [x] = Already implemented in CivIV
## [?] = Not sure if this applies in CivIV
## 
## Golden Age turns left
## At Year 1000 B.C. (QSC Save Submission)
## Within 10 tiles of domination limit
## There is new technology for sale
## There is a new luxury resource for sale
## There is a new strategic resource for sale
## There is a new bonus resource for sale
## We can sell a technology
## We can sell a luxury resource
## We can sell a strategic resource
## We can sell a bonus resource
## [*] Rival has lots of cash
## [*] Rival has lots of cash per turn
## [x] Rival has changed civics
## Rival has entered a new Era
## Trade deal expires next turn
## [o] Enemy at war is willing to negotiate
## [x] There are foreign units in our territory
## City is about to riot or rioting
## [*] City has grown or shrunk
## City has shrunk
## [*] City is unhealthy
## [*] City is angry
## City specialists reassigned
## [*] City is about to grow
## City is about to starve
## [*] City is about to grow into unhealthyness
## [*] City is about to grow into anger
## City is in resistance
## [?] City is wasting food
## City is working unimproved tiles
## Disconnected resources in our territory
## City is about to produce a great person
## 
## Other:
## City is under cultural pressure


class Civ4lerts:

	def __init__(self, eventManager):
		Civ4lertsEvent(eventManager)
		GoldTrade(eventManager)
		GoldPerTurnTrade(eventManager)

from CvPythonExtensions import ColorTypes
from CvPythonExtensions import CyGlobalContext
from CvPythonExtensions import CyInterface
from CvPythonExtensions import CyTranslator
import CvConfigParser
import AlertsLog

#global
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
CFG_PendingGrowth = config.getboolean("City Pending Growth", "Enabled", False)
CFG_PendingUnhealthy = config.getboolean("City Pending Unhealthy", "Enabled", True)
CFG_PendingAngry = config.getboolean("City Pending Angry", "Enabled", True)
CFG_CityGrowth = config.getboolean("City Growth", "Enabled", True)
CFG_GrowthUnhealthy = config.getboolean("City Growth Unhealthy", "Enabled", False)
CFG_GrowthAngry = config.getboolean("City Growth Angry", "Enabled", False)
CFG_GoldTrade = config.getboolean("Gold Trade", "Enabled", True)
CFG_GoldPerTurnTrade = config.getboolean("Gold Per Turn Trade", "Enabled", True)
CFG_GoldTradeThreshold = config.getint("Gold Trade", "Threshold", 50)
CFG_GoldPerTurnTradeThreshold = config.getint("Gold Per Turn Trade", "Threshold", 3)
addMessage = AlertsLog.AlertsLog().AlertsLogMessage

class AbstractAlert(object):

	"""Provides a base class and several convenience functions for 
	implementing an alert.

	"""

	gc = CyGlobalContext()

	localText = CyTranslator()

	#config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractAlert, self).__init__(*args, **kwargs)

class AbstractStatefulAlert(AbstractAlert):

	"""Provides a base class and several convenience functions for 
	implementing an alert that retains state information between turns.

	"""

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractStatefulAlert, self).__init__(eventManager, *args, **kwargs)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)

	def onGameStart(self, argsList):
		"""Called at the start of the game"""
		self._reset()

	def onLoadGame(self, argsList):
		self._reset()
		return 0

	def _reset(self):
		"""Override this method to reset any turn state information."""
		pass

class GoldTrade(AbstractStatefulAlert):

	"""Displays an alert when a civilization has a significant increase
	in gold available for trade since the last alert."""

	def __init__(self, eventManager, *args, **kwargs):
		super(GoldTrade, self).__init__(eventManager, *args, **kwargs)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)

	def onEndGameTurn(self, argsList):
		if (not CFG_GoldTrade):
			return
		player = self.gc.getGame().getActivePlayer()
		team = self.gc.getTeam(self.gc.getPlayer(player).getTeam())
		for rival in xrange(self.gc.getMAX_PLAYERS()):
			if (rival == player): continue
			rivalPlayer = self.gc.getPlayer(rival)
			rivalTeam = self.gc.getTeam(rivalPlayer.getTeam())
			# TODO: does this need to check for war or trade denial?
			if (team.isHasMet(rivalPlayer.getTeam()) and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
				oldMaxGoldTrade = self.maxGoldTrade[player][rival]
				newMaxGoldTrade = rivalPlayer.AI_maxGoldTrade(player)
				deltaMaxGoldTrade = newMaxGoldTrade - oldMaxGoldTrade
				if (deltaMaxGoldTrade >= CFG_GoldTradeThreshold):
					message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_GOLD_TRADE", (self.gc.getTeam(rival).getName(), newMaxGoldTrade))
					addMessage(player, message, None, self.gc.getInfoTypeForString("COLOR_YIELD_COMMERCE"), 0, 0, 2, -1, -1, True, True)
					self.maxGoldTrade[player][rival] = newMaxGoldTrade
				else:
					self.maxGoldTrade[player][rival] = min(oldMaxGoldTrade, newMaxGoldTrade)

	def _reset(self, *args, **kwargs):
		super(GoldTrade, self)._reset(*args, **kwargs)
		self.maxGoldTrade = {}
		for player in xrange(self.gc.getMAX_PLAYERS()):
			self.maxGoldTrade[player] = {}
			for rival in range(self.gc.getMAX_PLAYERS()):
				self.maxGoldTrade[player][rival] = 0

class GoldPerTurnTrade(AbstractStatefulAlert):

	"""Displays an alert when a civilization has a significant increase
	in gold per turn available for trade since the last alert.

	"""

	def __init__(self, eventManager, *args, **kwargs): 
		super(GoldPerTurnTrade, self).__init__(eventManager, *args, **kwargs)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)

	def onEndGameTurn(self, argsList):
		if (not CFG_GoldPerTurnTrade):
			return
		player = player = self.gc.getGame().getActivePlayer()
		team = self.gc.getTeam(self.gc.getPlayer(player).getTeam())
		for rival in xrange(self.gc.getMAX_PLAYERS()):
			if (rival == player):
				continue
			rivalPlayer = self.gc.getPlayer(rival)
			rivalTeam = self.gc.getTeam(rivalPlayer.getTeam())
			# TODO: does this need to check for war or trade denial?
			if (team.isHasMet(rivalPlayer.getTeam()) and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
				oldMaxGoldPerTurnTrade = self.maxGoldPerTurnTrade[player][rival]
				newMaxGoldPerTurnTrade = rivalPlayer.AI_maxGoldPerTurnTrade(player)
				deltaMaxGoldPerTurnTrade = newMaxGoldPerTurnTrade - oldMaxGoldPerTurnTrade
				if (deltaMaxGoldPerTurnTrade >= CFG_GoldPerTurnTradeThreshold):
					message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_GOLD_PER_TURN_TRADE", (self.gc.getTeam(rival).getName(), newMaxGoldPerTurnTrade))
					addMessage(player, message, None, self.gc.getInfoTypeForString("COLOR_YIELD_COMMERCE"), 0, 0, 2, -1, -1, True, True)
					self.maxGoldPerTurnTrade[player][rival] = newMaxGoldPerTurnTrade
				else:
					self.maxGoldPerTurnTrade[player][rival] = min(oldMaxGoldPerTurnTrade, newMaxGoldPerTurnTrade)

	def _reset(self, *args, **kwargs):
		super(GoldPerTurnTrade, self)._reset(*args, **kwargs)
		self.maxGoldPerTurnTrade = {}
		for player in range(self.gc.getMAX_PLAYERS()):
			self.maxGoldPerTurnTrade[player] = {}
			for rival in range(self.gc.getMAX_PLAYERS()):
				self.maxGoldPerTurnTrade[player][rival] = 0

class Civ4lertsEvent(AbstractAlert):

	def __init__(self, eventManager, *args, **kwargs):
		super(Civ4lertsEvent, self).__init__(eventManager, *args, **kwargs)
		eventManager.addEventHandler("cityDoTurn", self.onCityDoTurn)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)

	def onCityDoTurn(self, argsList):
		city, player = argsList
		#NoGrowthEmphasis = 5

		if (player != self.gc.getGame().getActivePlayer()):
			return

		if ((city.getFoodTurnsLeft() == 1) and not city.isFoodProduction() and (not city.AI_isEmphasize(5)) and (city.foodDifference(True) > 0)):
			szCityNeme = city.getName()
			iCityPop = city.getPopulation()

			# Pending Growth
			if (CFG_PendingGrowth):
				message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_GROWTH", (szCityNeme, iCityPop + 1))
				icon = "Art/Interface/Symbols/Food/food05.dds"
				addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_YIELD_FOOD"), city.getX(), city.getY(), 2, city.getID(), -1, True, True)

			# Pending Unhealthy
			if (CFG_PendingUnhealthy):
				if (city.goodHealth() <= city.badHealth(False)):
					message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHEALTHY", (szCityNeme, iCityPop))
					icon = "Art/Interface/Buttons/General/unhealthy_person.dds"
					addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_WARNING_TEXT"), city.getX(), city.getY(), 2, city.getID(), -1, True, True)

			# Pending Angry
			if (CFG_PendingAngry):
				if (city.happyLevel() <= city.unhappyLevel(0)):
					message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_ANGRY", (szCityNeme, iCityPop))
					icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
					addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_WARNING_TEXT"), city.getX(), city.getY(), 1, city.getID(), -1, True, True)

	def onCityGrowth(self, argsList):
		city, player = argsList
		szCityNeme = city.getName()
		iCityPop = city.getPopulation()

		if (player != self.gc.getGame().getActivePlayer()):
			return

		# City Growth
		if (CFG_CityGrowth):
			message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_GROWTH", (szCityNeme, iCityPop))
			icon = "Art/Interface/Symbols/Food/food05.dds"
			addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_YIELD_FOOD"), city.getX(), city.getY(), 2, city.getID(), -1, True, True)

		# Growth Unhealthy
		if (CFG_GrowthUnhealthy):
			if (city.healthRate(False, 0) < 0):
				message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_UNHEALTHY", (szCityNeme, iCityPop))
				icon = "Art/Interface/Buttons/General/unhealthy_person.dds"
				addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_WARNING_TEXT"), city.getX(), city.getY(), 2, city.getID(), -1, True, True)

		# Growth Angry
		if (CFG_GrowthAngry):
			if (city.angryPopulation(0) > 0):
				message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_ANGRY", (szCityNeme, iCityPop))
				icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
				addMessage(player, message, icon, self.gc.getInfoTypeForString("COLOR_WARNING_TEXT"), city.getX(), city.getY(), 1, city.getID(), -1, True, True)

class Civ4lertsOption:

	def setCGEOption(self, Section, Key, Value):
		global CFG_PendingGrowth
		global CFG_PendingUnhealthy
		global CFG_PendingAngry
		global CFG_CityGrowth
		global CFG_GrowthUnhealthy
		global CFG_GrowthAngry
		global CFG_GoldTrade
		global CFG_GoldPerTurnTrade
		global CFG_GoldTradeThreshold
		global CFG_GoldPerTurnTradeThreshold

		if (Section == "City Pending Growth"):
			CFG_PendingGrowth = Value
		elif (Section == "City Pending Unhealthy"):
			CFG_PendingUnhealthy = Value
		elif (Section == "City Pending Angry"):
			CFG_PendingAngry = Value
		elif (Section == "City Growth"):
			CFG_CityGrowth = Value
		elif (Section == "City Growth Unhealthy"):
			CFG_GrowthUnhealthy = Value
		elif (Section == "City Growth Angry"):
			CFG_GrowthAngry = Value
		elif (Section == "Gold Trade"):
			if (Key == "Enabled"):
				CFG_GoldTrade = Value
			elif (Key == "Threshold"):
				CFG_GoldTradeThreshold = Value
		elif (Section == "Gold Per Turn Trade"):
			if (Key == "Enabled"):
				CFG_GoldPerTurnTrade = Value
			elif (Key == "Threshold"):
				CFG_GoldPerTurnTradeThreshold = Value

