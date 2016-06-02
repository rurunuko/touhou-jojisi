# Civ IV Gameplay Enhancements Debug Infomation Popup
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import CvConfigParser
import Popup as PyPopup
import CvUtil
import CvPath
import os.path
import version

gc = CyGlobalContext()
localText = CyTranslator()

class CGEDebug:

	def CGEWarning(self):
		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
		if (config != None):
			self.CFG_Debug_CGE = config.getboolean("Civ IV Gameplay Enhancements", "Debug", False)

		if (not self.CFG_Debug_CGE):
			popup = PyPopup.PyPopup(-1)
			popup.setHeaderString("Civ IV Gameplay Enhancements Setup Warning !!!")
			popup.setBodyString(localText.getText("TXT_KEY_CGE_CONFIG_WARNING", ()))
			popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

		# BtS本体のバージョンが違う場合に正常動作しないことに対する警告。
		if (gc.getDefineINT("CIV4_VERSION") != 319):
			popup = PyPopup.PyPopup(-1)
			popup.setHeaderString("Civ IV Gameplay Enhancements Version Warning !!!")
			popup.setBodyString("This Civ IV Gameplay Enhancements does not work with this BtS version.")
			popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

		if (version.CGETestVersion):
			Civconfig = CvConfigParser.CvConfigParser("CivilizationIV.ini")
			bShowPythonExceptions = Civconfig.getint("CONFIG", "HidePythonExceptions", 1)
			if (bShowPythonExceptions != 0):
				popup = PyPopup.PyPopup(CvUtil.EventTestWarning, EventContextTypes.EVENTCONTEXT_SELF)
				popup.setHeaderString("Civ IV Gameplay Enhancements Test Version Warning !!!")
				popup.setBodyString("Set \"HidePythonExceptions\" to 0 in CivilizationIV.ini.")
				popup.setBodyString("Please do not use this test version if you will not cooperate to test.")
				popup.launch(True, PopupStates.POPUPSTATE_QUEUED)
