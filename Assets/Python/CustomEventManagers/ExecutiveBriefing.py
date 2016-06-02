## ExecutiveBriefing by Spocko
## Inspired by Dr Jiggle's Civ4Lerts mod
##

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvCameraControls
import CvConfigParser
import AlertsLog

# globals
gc = CyGlobalContext()
localText = CyTranslator()
config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
EnabledExecutiveBriefing = config.getboolean( "Executive Briefing", "Enabled", True)
addMessage = AlertsLog.AlertsLog().AlertsLogMessage

class ExecutiveBriefing:

	def setCGEOption(self, Section, Key, Value):
		global EnabledExecutiveBriefing

		if (Key == "Enabled"):
			EnabledExecutiveBriefing = Value

	def onCityDoTurn(self, argsList):
		pCity = argsList[0]
		iPlayer = argsList[1]
		iturn = gc.getGame().getGameTurn()
		activePlayer = CyGame().getActivePlayer()
		iCityX = pCity.getX()
		iCityY = pCity.getY()
		eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")

		if (EnabledExecutiveBriefing and (not CyGame().isNetworkMultiPlayer()) and (pCity.getOwner() == activePlayer) and (not gc.getPlayer(iPlayer).isAnarchy())):

			# City is about to grow and not because of it finishing producing a unit (settler or worker) using food
			#NoGrowthEmphasis = 5

			# Give a periodic status report on which cities are unhappy
			if ((iturn % 4) == 0):
				if (pCity.angryPopulation(0) > 0):
					addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_ANGRY', ()) %(pCity.getName()), 'Art/Interface/Population Heads/angrycitizen.dds', ColorTypes(7), iCityX, iCityY, 1, pCity.getID(), -1, True, True)

				# Give a periodic report on cities that have a long wait before finishing their current production
				if ((iturn % 20) == 0):
					if (pCity.getGeneralProductionTurnsLeft() > 30):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_TURNS_TO_BUILD', ()) %(pCity.getName(),pCity.getProductionName(),pCity.getGeneralProductionTurnsLeft()), 'Art/Interface/Symbols/Production/production05.dds', ColorTypes(78), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

				# Give a periodic report on cities that are unproductive
				if ((iturn % 16) == 0):
					if ((pCity.getPopulation() > 3) and (pCity.getPopulation() > (pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION)*1.5))):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_UNPRODUCTIVE', ()) %(pCity.getName(),pCity.getProductionName()), 'Art/Interface/Symbols/Production/production05.dds', ColorTypes(11), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

			# Give a periodic status report on which cities are unhealthy
			elif (((iturn + 1) % 4) == 0):
				if (pCity.healthRate(False, 0) < 0):
					addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_NOT_GOOD_HEALTH', ()) %(pCity.getName()), 'Art/Interface/Buttons/General/unhealthy_person.dds', ColorTypes(10), iCityX, iCityY, 2, pCity.getID(), -1, True, True)

			# Give a periodic status report on which cities have evenly split health/unhealthy (and the city is not about to grow - handled elsewhere)
			if ((iturn % 5) == 0):
				if ((pCity.getFoodTurnsLeft() != 1) and (pCity.goodHealth() == pCity.badHealth(0))):
					addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_GOOD_AND_BAD_HEALTH', ()) %(pCity.getName()), 'Art/Interface/Buttons/General/unhealthy_person.dds', ColorTypes(13), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

				# Give a periodic report on cities that have a long wait before growing
				if ((iturn % 15) == 0):
					if ((pCity.getFoodTurnsLeft() > 30) and not pCity.isFoodProduction() and (not pCity.AI_isEmphasize(5)) and (pCity.getPopulation() > 3) and (pCity.getPopulation() < 9)):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_TURNS_TO_GROW', ()) %(pCity.getName(),(pCity.getPopulation() + 1),pCity.getFoodTurnsLeft()), 'Art/Interface/Buttons/Units/Settler.dds', ColorTypes(7), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

			# Give a periodic status report on which cities have evenly split happy/unhappy (and the city is not about to grow - handled elsewhere)
			elif ((iturn +1 % 5) == 0):
				if ((pCity.getFoodTurnsLeft() != 1) and (pCity.happyLevel() == pCity.unhappyLevel(0))):
					addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_HAPPY_AND_UNHAPPY', ()) %(pCity.getName()), 'Art/Interface/Buttons/General/resistance.dds', ColorTypes(12), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

			# Give a periodic status report on which cities are either starving or close to it
			if (((iturn - 1) % 3) == 0):
				if (pCity.foodDifference(True) < 0):
					addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_NEED_FOOD', ()) %(pCity.getName()), 'Art/Interface/Symbols/Food/food05.dds', ColorTypes(7), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

			# Give a periodic report on small cities that would benefit from Hurrying production
			if (((iturn + 1) % 7) == 0):
				if ((pCity.getGeneralProductionTurnsLeft() > 30)):
					szCost = u""
					if (pCity.canHurry(0, False)):
						szCost = localText.getText("TXT_KEY_MISC_HURRY_POP", (pCity.hurryPopulation(0),))[1:]
					elif (pCity.canHurry(1, False)):
						szCost = localText.getText("TXT_KEY_MISC_HURRY_GOLD", (pCity.hurryGold(1),))[1:]
					if (szCost != u""):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_HURRY_UP_PRODUCTION', ()) %(pCity.getName(),pCity.getProductionName(), szCost), 'Art/Interface/Symbols/Production/production05.dds', ColorTypes(11), iCityX, iCityY, 2, pCity.getID(), -1, True, True)

			# Give a periodic status report on which cities are set to emphasize NO GROWTH
			elif (((iturn - 2) % 7) == 0):
				if (pCity.AI_isEmphasize(5)):
					if (pCity.happyLevel() - pCity.unhappyLevel(0) > 0):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_NO_GROWTH_POLICY_BUT_CAN_REGROWTH', ()) %(pCity.getName()), 'Art/Interface/Buttons/Units/Settler.dds', ColorTypes(8), iCityX, iCityY, 1, pCity.getID(), -1, True, True)
					else:
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_NO_GROWTH_POLICY', ()) %(pCity.getName()), 'Art/Interface/Buttons/Units/Settler.dds', ColorTypes(12), iCityX, iCityY, 3, pCity.getID(), -1, True, True)

			# Give a periodic report on cities that are not connected to the civ trade network
			if ((iturn % 9) == 0):
				if (not pCity.isCapital()):
					if (not pCity.isConnectedToCapital(activePlayer)):
						addMessage(activePlayer, localText.getText('TXT_EXECUTIVE_BRIEFING_NOT_CONNECT_CAPITAL_CITY', ()) %(pCity.getName()), 'Art/Interface/Buttons/Governor/commerce.dds', ColorTypes(13), iCityX, iCityY, 1, pCity.getID(), -1, True, True)
