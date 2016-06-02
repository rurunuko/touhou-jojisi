## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
import CvUtil
#import CvEventManager
#import sys
#import CvGreatPersonScreen
import RandomNameUtils

# Change the value to enable or disable the features from the Great Person Mod.
# Default value is true
#g_bGreatPersonModFeaturesEnabled = True

gc = CyGlobalContext()

# globals
###################################################
class CvGreatPersonModEventManager:

	def __init__(self, eventManager):

		GreatPerson(eventManager)

class AbstractGreatPerson(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractGreatPerson, self).__init__(*args, **kwargs)

class GreatPerson(AbstractGreatPerson):

	def __init__(self, eventManager, *args, **kwargs):
		super(GreatPerson, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)

		self.eventMgr = eventManager

	# GreatPerson Mod -------- begin
	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		player = gc.getPlayer(iPlayer)

		#if (not g_bGreatPersonModFeaturesEnabled):
		#	return

		# Check if we should even show the popup:
		if (pUnit.isNone() or pCity.isNone()):
			return

		#If Person doesn't have unique name, give him a random one
		if (len(pUnit.getNameNoDesc()) == 0):
			iCivilizationType = player.getCivilizationType()
			pUnit.setName(RandomNameUtils.getRandomCivilizationName(iCivilizationType))

		#Show fancy lil popup if a human got the great person:
		if (iPlayer == gc.getGame().getActivePlayer() and player.isHuman()):
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setData1(iPlayer)
			popupInfo.setData2(pUnit.getID())
			popupInfo.setData3(pCity.getID())
			popupInfo.setText(u"showGreatPersonScreen")
			popupInfo.addPopup(iPlayer)
