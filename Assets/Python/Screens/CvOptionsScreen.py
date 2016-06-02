## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

# For Input see CvOptionsScreenCallbackInterface in Python\EntryPoints\

import CvUtil
from CvPythonExtensions import *
import CGEOptionControl
import Version
import CvConfigParser
import CvPath
import os.path
import sre

# globals
gc = CyGlobalContext()
UserProfile = CyUserProfile()
localText = CyTranslator()

removeColor = sre.compile(r'<color=.*?>|</color>')

class CvOptionsScreen:
	"Options Screen"

	def __init__(self):

		self.iScreenHeight = 50

		self.iGameOptionsTabID		= 0
		self.iGraphicOptionsTabID	= 1
		self.iAudioOptionsTabID		= 2
		self.iOtherOptionsTabID		= 3

		self.callbackIFace = "CvOptionsScreenCallbackInterface"

	def getTabControl(self):
		return self.pTabControl

	def getGameOptionsTabName(self):
		return self.szGameOptionsTabName
	def getGraphicOptionsTabName(self):
		return self.szGraphicsOptionsTabName
	def getAudioOptionsTabName(self):
		return self.szAudioOptionsTabName
	def getOtherOptionsTabName(self):
		return self.szOtherOptionsTabName

	def getCGEOptions1TabName(self):
		return self.szCGEOptions1TabName
	def getCGEOptions2TabName(self):
		return self.szCGEOptions2TabName
	def getCGEOptions3TabName(self):
		return self.szCGEOptions3TabName
	def getCGEOptions5TabName(self):
		return self.szCGEOptions5TabName
	def getCGEOptions6TabName(self):
		return self.szCGEOptions6TabName
	def getCGEOptions7TabName(self):
		return self.szCGEOptions7TabName
	def getCGEOptionsAboutTabName(self):
		return self.szCGEOptionsAboutTabName

	# Used by Callback Interface to set path via checkbox
	def getMusicPath(self):
		return self.getTabControl().getText("CustomMusicEditBox")
	def getCustomMusicCheckboxName(self):
		return self.szCustomMusicCheckboxName

	# Used by Callback Interface to set Alarm time via checkbox
	def getAlarmHour(self):
		return self.getTabControl().getText("AlarmHourEditBox")
	def getAlarmMin(self):
		return self.getTabControl().getText("AlarmMinEditBox")

	# Used by Callback Interface to get user defined profile names from editbox
	def setProfileEditCtrlText(self, szProfileName):
		szWideProfName = CvUtil.convertToUnicode(szProfileName)
		self.getTabControl().setText("ProfileNameEditBox", szWideProfName)
	def getProfileEditCtrlText(self):
		return self.getTabControl().getText("ProfileNameEditBox")

	# Called from C++ after a custom music path is selected via FileDialogBox
	def updateMusicPath (self, szMusicPath):

		self.getTabControl().setText("CustomMusicEditBox", szMusicPath)
		self.getTabControl().setValue(self.getCustomMusicCheckboxName(), true)

#########################################################################################
################################## SCREEN CONSTRUCTION ##################################
#########################################################################################

	def initText(self):

		self.szTabControlName = localText.getText("TXT_KEY_OPTIONS_TITLE", ())

		self.szGameOptionsTabName = localText.getText("TXT_KEY_OPTIONS_GAME", ())
		self.szGraphicsOptionsTabName = localText.getText("TXT_KEY_OPTIONS_GRAPHICS", ())
		self.szAudioOptionsTabName = localText.getText("TXT_KEY_OPTIONS_AUDIO", ())
		self.szOtherOptionsTabName = localText.getText("TXT_KEY_OPTIONS_SCREEN_OTHER", ())

		self.szCGEOptions1TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB1", ())
		self.szCGEOptions2TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB2", ())
		self.szCGEOptions3TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB3", ())
		self.szCGEOptions5TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB5", ())
		self.szCGEOptions6TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB6", ())
		self.szCGEOptions7TabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB7", ())
		self.szCGEOptionsAboutTabName = localText.getText("TXT_KEY_CGE_OPTSCR_TAB_ABOUT", ())

	def refreshScreen (self):

		#################### Game Options ####################

		szTab = self.getGameOptionsTabName()
		for iOptionLoop in range(PlayerOptionTypes.NUM_PLAYEROPTION_TYPES):
			szWidgetName = "GameOptionCheckBox_" + str(iOptionLoop)
			bOptionOn = UserProfile.getPlayerOption(iOptionLoop)
			self.pTabControl.setValue(szWidgetName, bOptionOn)

		# Languages Dropdown
		self.getTabControl().setValue("LanguagesDropdownBox", CyGame().getCurrentLanguage())

		#################### GRAPHICS ####################

		szTab = self.getGraphicOptionsTabName()

		# Graphics Dropdowns

		self.getTabControl().setValue(self.szResolutionComboBoxName, UserProfile.getResolution() )
		self.getTabControl().setValue("AntiAliasingDropdownBox", UserProfile.getAntiAliasing() )
		self.getTabControl().setValue("GraphicsLevelDropdownBox", UserProfile.getGraphicsLevel() )
		self.getTabControl().setValue("RenderQualityDropdownBox", UserProfile.getRenderQualityLevel() )
		self.getTabControl().setValue("GlobeViewDropdownBox", UserProfile.getGlobeViewRenderLevel() )
		self.getTabControl().setValue("MovieDropdownBox", UserProfile.getMovieQualityLevel() )
		self.getTabControl().setValue("MainMenuDropdownBox", UserProfile.getMainMenu() )

		# Graphic Option Checkboxes
		for iOptionLoop in range(GraphicOptionTypes.NUM_GRAPHICOPTION_TYPES):
			szWidgetName = "GraphicOptionCheckbox_" + str(iOptionLoop)
			bOptionOn = UserProfile.getGraphicOption(iOptionLoop)
			self.pTabControl.setValue(szWidgetName, bOptionOn)

		#################### AUDIO ####################

		szTab = self.getAudioOptionsTabName()

		iMax = UserProfile.getVolumeStops()

		# Volume Sliders and No Sound Checkboxes
		for iWidgetNum in range(6):
			if (iWidgetNum == 0):		# Master Volume
				iInitialVal = iMax-UserProfile.getMasterVolume()-1
				bNoSoundTrue = UserProfile.isMasterNoSound()
			elif (iWidgetNum == 1):		# Music Volume
				iInitialVal = iMax-UserProfile.getMusicVolume()-1
				bNoSoundTrue = UserProfile.isMusicNoSound()
			elif (iWidgetNum == 2):		# Sound Effects Volume
				iInitialVal = iMax-UserProfile.getSoundEffectsVolume()-1
				bNoSoundTrue = UserProfile.isSoundEffectsNoSound()
			elif (iWidgetNum == 3):		# Speech Volume
				iInitialVal = iMax-UserProfile.getSpeechVolume()-1
				bNoSoundTrue = UserProfile.isSpeechNoSound()
			elif (iWidgetNum == 4):		# Ambience Volume
				iInitialVal = iMax-UserProfile.getAmbienceVolume()-1
				bNoSoundTrue = UserProfile.isAmbienceNoSound()
			elif (iWidgetNum == 5):		# Interface Volume
				iInitialVal = iMax-UserProfile.getInterfaceVolume()-1
				bNoSoundTrue = UserProfile.isInterfaceNoSound()

			# Volume Slider
			szWidgetName = "VolumeSlider_" + str(iWidgetNum)
   			self.getTabControl().setValue(szWidgetName, iInitialVal)

			# Volume Checkbox
			szWidgetName = "VolumeNoSoundCheckbox_" + str(iWidgetNum)
			self.pTabControl.setValue(szWidgetName, bNoSoundTrue)

		# Voice Capture Dropdown
		self.getTabControl().setValue("CaptureDeviceDropdownBox", UserProfile.getCaptureDeviceIndex() )
		# Voice Capture Slider
#   		self.getTabControl().setValue("CaptureVolumeSlider", UserProfile.getMaxCaptureVolume() - UserProfile.getCaptureVolume())
   		self.getTabControl().setValue("CaptureVolumeSlider", UserProfile.getCaptureVolume())

		# Voice Playback Dropdown
		self.getTabControl().setValue("PlaybackDeviceDropdownBox", UserProfile.getPlaybackDeviceIndex() )
		# Voice Playback Slider
#   		self.getTabControl().setValue("PlaybackVolumeSlider", UserProfile.getMaxPlaybackVolume() - UserProfile.getPlaybackVolume())
   		self.getTabControl().setValue("PlaybackVolumeSlider", UserProfile.getPlaybackVolume())

		# Voice Chatting Checkbox
		self.getTabControl().setValue("VoiceChatCheckbox", UserProfile.useVoice())

		# Speaker config
		iInitialSelection = 0
		for iSpeakerConfigLoop in range(16):
			szActiveConfig = UserProfile.getSpeakerConfigFromList(iSpeakerConfigLoop)
			if (UserProfile.getSpeakerConfig() == szActiveConfig):
				iInitialSelection = iSpeakerConfigLoop

		# Speaker Config Dropdown
		self.getTabControl().setValue("SpeakerConfigDropdownBox", iInitialSelection )

		# Custom Music Path Checkbox
		bUseCustomMusicPath = false
		if (UserProfile.getMusicPath() != ""):
			bUseCustomMusicPath = true
		self.getTabControl().setValue(self.getCustomMusicCheckboxName(), bUseCustomMusicPath)

		# Custom Music Path Editbox
		szEditBoxDesc = ""
		if (UserProfile.getMusicPath() != ""):
			szEditBoxDesc = CvUtil.convertToUnicode(UserProfile.getMusicPath())
		self.getTabControl().setText("CustomMusicEditBox", szEditBoxDesc)

		#################### CLOCK ####################

		szTab = self.getOtherOptionsTabName()

		# Clock On Checkbox
		self.getTabControl().setValue("ClockOnCheckbox", UserProfile.isClockOn())

		# 24 Hour Clock Checkbox
		self.getTabControl().setValue("24HourClockCheckbox", UserProfile.is24Hours())

		# Alarm On Checkbox
		self.getTabControl().setValue("AlarmOnCheckbox", isAlarmOn())

		# Alarm Hours
		self.getTabControl().setText("AlarmHourEditBox", str(getAlarmHourLeft()))
		self.getTabControl().setText("AlarmMinEditBox", str(getAlarmMinLeft()))

		#################### PROFILE ####################

		# Profile Name Editbox
		self.getTabControl().setText("ProfileNameEditBox", CvUtil.convertToUnicode(UserProfile.getProfileName()))

		aszDropdownElements = ()
		for iProfileLoop in range(UserProfile.getNumProfileFiles()):
			szProfileFileName = UserProfile.getProfileFileName(iProfileLoop)
			# Cut off file path and extension
			szProfile = szProfileFileName[szProfileFileName.find("PROFILES\\")+9:-4]
			aszDropdownElements = aszDropdownElements + (szProfile,)
# >>> CYBERFRONT // profile:
#			if (UserProfile.getProfileName() == szProfile):
			if (UserProfile.getProfileName() == CvUtil.convertToStr(szProfile)):
# <<< CYBERFRONT
				iInitialSelection = iProfileLoop

		self.getTabControl().changeDropdownContents("ProfilesDropdownBox", aszDropdownElements)

		# Profile List Dropdown
		self.getTabControl().setValue("ProfilesDropdownBox", iInitialSelection)

		#################### PROFILE ####################

		# Broadband Radio Button
   		self.getTabControl().setValue("BroadbandSelection", not gc.getGame().isModem())

		# Modem Checkbox
   		self.getTabControl().setValue("ModemSelection", gc.getGame().isModem())

		# CGE Refresh Option Screen
		getValue = CGEOptionControl.CGEOptionControl().getValue
		setValue = self.getTabControl().setValue

		# CGE1
		szTab = self.getCGEOptions1TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 1):
				Value = getValue(Option[0])
				self.getTabControl().setValue(Option[0], Value)

		# CGE2
		szTab = self.getCGEOptions2TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 2):
				Value = getValue(Option[0])
				self.getTabControl().setValue(Option[0], Value)

		# CGE3
		szTab = self.getCGEOptions3TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 3):
				Value = getValue(Option[0])
				if (str(Value).startswith("COLOR_")):
					Value = gc.getInfoTypeForString(Value) - 2
				self.getTabControl().setValue(Option[0], Value)

		# CGE5
		szTab = self.getCGEOptions5TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 5):
				Value = getValue(Option[0])
				self.getTabControl().setValue(Option[0], Value)

		# CGE6
		szTab = self.getCGEOptions6TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 6):
				Value = getValue(Option[0])
				if (str(Value).startswith("COLOR_")):
					Value = gc.getInfoTypeForString(Value) - 2
				self.getTabControl().setValue(Option[0], Value)

		# CGE7
		szTab = self.getCGEOptions7TabName()

		for Option in CGEOptionControl.gOptionDict.items():
			if (Option[1]['Tab'] == 7):
				Value = getValue(Option[0])
				self.getTabControl().setValue(Option[0], Value)

	def interfaceScreen (self):
		"Initial creation of the screen"
		self.initText()

		self.pTabControl = CyGTabCtrl(self.szTabControlName, False, False)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(890,695)
		self.pTabControl.setControlsExpanding(False)
		self.pTabControl.setColumnLength(self.iScreenHeight)

		# Set Tabs
		self.pTabControl.attachTabItem("GameForm", self.szGameOptionsTabName)
		self.pTabControl.attachTabItem("GraphicsForm", self.szGraphicsOptionsTabName)
		self.pTabControl.attachTabItem("AudioForm", self.szAudioOptionsTabName)
		self.pTabControl.attachTabItem("OtherForm", self.szOtherOptionsTabName)

		self.pTabControl.attachTabItem("CGE1Form", self.szCGEOptions1TabName)
		self.pTabControl.attachTabItem("CGE6Form", self.szCGEOptions6TabName)
		self.pTabControl.attachTabItem("CGE5Form", self.szCGEOptions5TabName)
		self.pTabControl.attachTabItem("CGE2Form", self.szCGEOptions2TabName)
		self.pTabControl.attachTabItem("CGE3Form", self.szCGEOptions3TabName)

		#try:
		#	if (gc.isCGEBuild()):
		#		self.pTabControl.attachTabItem("CGE7Form", self.szCGEOptions7TabName)
		#except:
		#	pass

		self.pTabControl.attachTabItem("CGEAboutForm", self.szCGEOptionsAboutTabName)

		self.drawGameOptionsTab()
		self.drawGraphicOptionsTab()
		self.drawAudioOptionsTab()
		self.drawOtherTab()

		CGEOptionControl.CGEOptionControl().InitValue()
		self.drawCGE1Tab()
		self.drawCGE2Tab()
		self.drawCGE3Tab()
		self.drawCGE5Tab()
		self.drawCGE6Tab()
		#try:
		#	if (gc.isCGEBuild()):
		#		self.drawCGE7Tab()
		#except:
		#	pass
		self.drawCGEAboutTab()

	def drawGameOptionsTab(self):

		tab = self.pTabControl

		tab.attachVBox("GameForm", "GameVBox")

		# Add Game Options

		tab.attachPanel("GameVBox", "GamePanelCenter")
		tab.setStyle("GamePanelCenter", "Panel_Tan15_Style")
		tab.setLayoutFlag("GamePanelCenter", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("GamePanelCenter", "LAYOUT_SIZE_VEXPANDING")

		tab.attachScrollPanel("GamePanelCenter", "GamePanel")
		tab.setLayoutFlag("GamePanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("GamePanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("GamePanel", "GameHBox")
		tab.setLayoutFlag("GameHBox", "LAYOUT_SIZE_HEXPANDING")

		tab.attachVBox("GameHBox", "GameVBox1")
		tab.setLayoutFlag("GameVBox1", "LAYOUT_SIZE_HEXPANDING")
		#tab.attachVSeparator("GameHBox", "GameHBoxSeparator")
		tab.attachVBox("GameHBox", "GameVBox2")
		tab.setLayoutFlag("GameVBox2", "LAYOUT_SIZE_HEXPANDING")

		i = 0
		for iOptionLoop in range(PlayerOptionTypes.NUM_PLAYEROPTION_TYPES):

			bContinue = true

			if (iOptionLoop == PlayerOptionTypes.PLAYEROPTION_MODDER_1):
				if (gc.getDefineINT("USE_MODDERS_PLAYEROPTION_1") == 0):
					bContinue = false
			elif (iOptionLoop == PlayerOptionTypes.PLAYEROPTION_MODDER_2):
				if (gc.getDefineINT("USE_MODDERS_PLAYEROPTION_2") == 0):
					bContinue = false
			elif (iOptionLoop == PlayerOptionTypes.PLAYEROPTION_MODDER_3):
				if (gc.getDefineINT("USE_MODDERS_PLAYEROPTION_3") == 0):
					bContinue = false

			if (bContinue):

				szOptionDesc = gc.getPlayerOptionsInfoByIndex(iOptionLoop).getDescription()
				szHelp = gc.getPlayerOptionsInfoByIndex(iOptionLoop).getHelp()
				szCallbackFunction = "handleGameOptionsClicked"
				szWidgetName = "GameOptionCheckBox_" + str(iOptionLoop)
				bOptionOn = UserProfile.getPlayerOption(iOptionLoop)#gc.getPlayer(gc.getGame().getActivePlayer()).isOption(iOptionLoop)
				if ((i+1) <= (PlayerOptionTypes.NUM_PLAYEROPTION_TYPES+1)/2):
					vbox = "GameVBox1"
				else:
					vbox = "GameVBox2"
				tab.attachCheckBox(vbox, szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bOptionOn)
				tab.setToolTip(szWidgetName, szHelp)
				i += 1


		tab.attachSpacer("GamePanelCenter")

		tab.attachHBox("GamePanelCenter", "LangHBox")

		# Languages Dropdown
		tab.attachLabel("LangHBox", "LangLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_LANGUAGE", ()))	# Label
		szDropdownDesc = "LanguagesDropdownBox"

		tab.attachSpacer("LangHBox")

		aszDropdownElements = ()
		for i in range(CvGameText().getNumLanguages()):
			szKey = "TXT_KEY_LANGUAGE_%d" % i
			aszDropdownElements = aszDropdownElements + (localText.getText(szKey, ()),)

		szCallbackFunction = "handleLanguagesDropdownBoxInput"
		szWidgetName = "LanguagesDropdownBox"
		iInitialSelection = CyGame().getCurrentLanguage()
		tab.attachDropDown("LangHBox", szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_LEFT")

		########## Lower Panel

		tab.attachHSeparator("GameVBox", "GameExitSeparator")

		tab.attachHBox("GameVBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleGameReset"
		szWidgetName = "GameOptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "GameOptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

	def drawGraphicOptionsTab(self):

		tab = self.pTabControl

		tab.attachVBox("GraphicsForm", "GraphicsVBox")

		tab.attachScrollPanel("GraphicsVBox", "GraphicsPanel")
		tab.setLayoutFlag("GraphicsPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("GraphicsPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("GraphicsPanel", "GraphicsPanelHBox")
		tab.setLayoutFlag("GraphicsPanelHBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("GraphicsPanelHBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")


		####### RESOLUTION

		tab.attachVBox("GraphicsPanelHBox", "ResVBox")
		tab.setLayoutFlag("ResVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("ResVBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("ResVBox", "ResPanel")
		tab.setStyle("ResPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("ResPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("ResPanel", "LAYOUT_SIZE_VEXPANDING")

		hbox = "ResPanelHBox"
		tab.attachHBox("ResPanel", hbox)
		tab.setLayoutFlag(hbox, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(hbox, "LAYOUT_SIZE_VEXPANDING")


		vbox = "ResPanelVBox"
		tab.attachVBox(hbox, vbox)
		tab.setLayoutFlag(vbox, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(vbox, "LAYOUT_SIZE_VEXPANDING")

		# Screen Image
		tab.attachPanel(vbox, "ResScreenPanel")
		tab.setLayoutFlag("ResScreenPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setStyle("ResScreenPanel", "Panel_Black25_Style")

		tab.attachHBox(vbox, "ResHBox")

		vbox1 = "ResVBox1"
		vbox2 = "ResVBox2"
		tab.attachVBox("ResHBox", vbox1)
		tab.attachVBox("ResHBox", vbox2)

		# Screen Resolution Dropdown
		tab.attachLabel(vbox1, "ResLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_RES", ()))	# Label
		tab.setControlFlag("ResLabel", "CF_LABEL_DEFAULTSIZE")
		szDropdownDesc = "ResolutionDropdownBox"
		aszDropdownElements = ()
		for iResLoop in range(UserProfile.getResolutionMaxModes()):
			aszDropdownElements = aszDropdownElements + (UserProfile.getResolutionString(iResLoop),)
		szCallbackFunction = "handleResolutionDropdownInput"
		szWidgetName = self.szResolutionComboBoxName = "ResolutionDropdownBox"
		iInitialSelection = UserProfile.getResolution()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Anti-Aliasing Dropdown
		tab.attachLabel(vbox1, "AALabel", localText.getText("TXT_KEY_OPTIONS_ANTIALIAS", ()))
		tab.setControlFlag("AALabel", "CF_LABEL_DEFAULTSIZE")
		szDropdownDesc = "AntiAliasingDropdownBox"
		aszDropdownElements = ()
		for iAALoop in range(UserProfile.getAntiAliasingMaxMultiSamples()+1):
			if (iAALoop == 0):
				aszDropdownElements = aszDropdownElements + (u"0",)
			elif (iAALoop == 1):
				aszDropdownElements = aszDropdownElements + (u"2",)
			elif (iAALoop == 2):
				aszDropdownElements = aszDropdownElements + (u"4",)
			elif (iAALoop == 3):
				aszDropdownElements = aszDropdownElements + (u"8",)
			elif (iAALoop == 4):
				aszDropdownElements = aszDropdownElements + (u"16",)

		szCallbackFunction = "handleAntiAliasingDropdownInput"
		szWidgetName = "AntiAliasingDropdownBox"
		iInitialSelection = UserProfile.getAntiAliasing()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_LEFT")

		# Graphics Level
		tab.attachLabel(vbox1, "GraphicsLevelLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_GRAPHICS_LEVEL", ()))	# Label
		tab.setControlFlag("GraphicsLevelLabel", "CF_LABEL_DEFAULTSIZE")
		szDropdownDesc = "GraphicsLevelDropdownBox"
		aszDropdownElements = (localText.getText("TXT_KEY_SEALEVEL_HIGH", ()), localText.getText("TXT_KEY_SEALEVEL_MEDIUM", ()), localText.getText("TXT_KEY_SEALEVEL_LOW", ()))
		szCallbackFunction = "handleGraphicsLevelDropdownBoxInput"
		szWidgetName = szDropdownDesc
		iInitialSelection = UserProfile.getGraphicsLevel()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Render Quality level
		tab.attachLabel(vbox1, "GraphicsQualityLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_RENDER_QUALITY_LEVEL", ()))	# Label
		tab.setControlFlag("GraphicsQualityLabel", "CF_LABEL_DEFAULTSIZE")
		szDropdownDesc = "RenderQualityDropdownBox"
		aszDropdownElements = (localText.getText("TXT_KEY_SEALEVEL_HIGH", ()), localText.getText("TXT_KEY_SEALEVEL_MEDIUM", ()), localText.getText("TXT_KEY_SEALEVEL_LOW", ()))
		szCallbackFunction = "handleRenderQualityDropdownBoxInput"
		szWidgetName = self.szRenderQualityDropdownBoxName = "RenderQualityDropdownBox"
		iInitialSelection = UserProfile.getRenderQualityLevel()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Globe view rendering level
		tab.attachLabel(vbox1, "GlobeViewLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_GLOBE", ()))	# Label
		tab.setControlFlag("GlobeViewLabel", "CF_LABEL_DEFAULTSIZE")

		szDropdownDesc = "GlobeViewDropdownBox"
		aszDropdownElements = (localText.getText("TXT_KEY_SEALEVEL_HIGH", ()), localText.getText("TXT_KEY_SEALEVEL_MEDIUM", ()), localText.getText("TXT_KEY_SEALEVEL_LOW", ()))
		szCallbackFunction = "handleGlobeViewDropdownBoxInput"
		szWidgetName = self.szGlobeViewDropdownBoxName = "GlobeViewDropdownBox"
		iInitialSelection = UserProfile.getGlobeViewRenderLevel()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Movies
		tab.attachLabel(vbox1, "MovieLabel", localText.getText("TXT_KEY_GRAPHICS_SETTINGS_MOVIE_QUALITY", ()))
		tab.setControlFlag("MovieLabel", "CF_LABEL_DEFAULTSIZE")

		szDropdownDesc = "MovieDropdownBox"
		aszDropdownElements = (localText.getText("TXT_KEY_SEALEVEL_HIGH", ()), localText.getText("TXT_KEY_SEALEVEL_MEDIUM", ()), localText.getText("TXT_KEY_SEALEVEL_LOW", ()))
		szCallbackFunction = "handleMovieDropdownBoxInput"
		szWidgetName = self.szMovieDropdownBoxName = "MovieDropdownBox"
		iInitialSelection = UserProfile.getMovieQualityLevel()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Main menu
		tab.attachLabel(vbox1, "MainMenuLabel", localText.getText("TXT_KEY_OPENING_MENU", ()))	# Label
		tab.setControlFlag("MainMenuLabel", "CF_LABEL_DEFAULTSIZE")

		szDropdownDesc = "MainMenuDropdownBox"
		aszDropdownElements = ()
		for iMainMenuLoop in range(gc.getNumMainMenus()):
			aszDropdownElements = aszDropdownElements + (gc.getMainMenus(iMainMenuLoop).getDescription(),)
		szCallbackFunction = "handleMainMenuDropdownBoxInput"
		szWidgetName = self.szMainMenuDropdownBoxName = "DropdownBox"
		iInitialSelection = UserProfile.getMainMenu()
		tab.attachDropDown(vbox2, szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		####### GAME GRAPHICS

		tab.attachVSeparator(hbox, "GfxSeparator")
		tab.setLayoutFlag("GfxSeparator", "LAYOUT_LEFT")

		vbox = "GfxPanelVBox"
		tab.attachVBox(hbox, vbox)
		tab.setLayoutFlag(vbox, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(vbox, "LAYOUT_SIZE_VEXPANDING")
		tab.setLayoutFlag(vbox, "LAYOUT_SPACING_NONE")

		# Checkboxes
		for iOptionLoop in range(GraphicOptionTypes.NUM_GRAPHICOPTION_TYPES):
			szOptionDesc = gc.getGraphicOptionsInfoByIndex(iOptionLoop).getDescription()
			szHelp = gc.getGraphicOptionsInfoByIndex(iOptionLoop).getHelp()
			szCallbackFunction = "handleGraphicOptionsClicked"
			szWidgetName = "GraphicOptionCheckbox_" + str(iOptionLoop)
			bOptionOn = UserProfile.getGraphicOption(iOptionLoop)
			tab.attachCheckBox(vbox, szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bOptionOn)
			tab.setToolTip(szWidgetName, szHelp)

		########## EXIT

		tab.attachHSeparator("GraphicsVBox", "GraphicsExitSeparator")

		tab.attachHBox("GraphicsVBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleGraphicsReset"
		szWidgetName = "GraphicOptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "GraphicOptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

	def drawAudioOptionsTab(self):

		tab = self.pTabControl

		tab.attachVBox("AudioForm", "AudioVBox")

		tab.attachScrollPanel("AudioVBox", "AudioPanel")
		tab.setLayoutFlag("AudioPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("AudioPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("AudioPanel", "AudioPanelVBox")
		tab.setLayoutFlag("AudioPanelHBox", "LAYOUT_SPACING_FORM")
		tab.setLayoutFlag("AudioPanelHBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("AudioPanelHBox", "LAYOUT_SIZE_VEXPANDING")


		######################### Create the 6 volume slider/checkboxes #########################

		tab.attachVBox("AudioPanelVBox", "VolumeVBox")
		tab.setLayoutFlag("VolumeVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("VolumeVBox", "LAYOUT_SIZE_VEXPANDING")

		#tab.attachLabel("VolumeVBox", "VolumeLabel", "VOLUME")

		tab.attachPanel("VolumeVBox", "VolumePanel")
		tab.setStyle("VolumePanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("VolumePanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("VolumePanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("VolumePanel", "VolumePanelVBox")
		tab.setLayoutFlag("VolumePanelVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("VolumePanelVBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachScrollPanel("VolumePanelVBox", "VolumeScrollPanel")
		tab.setLayoutFlag("VolumeScrollPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("VolumeScrollPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("VolumeScrollPanel", "VolumePanelHBox")
		tab.setLayoutFlag("VolumePanelHBox", "LAYOUT_HEVENSTRETCH")
		tab.setLayoutFlag("VolumePanelHBox", "LAYOUT_SIZE_VEXPANDING")

		for iWidgetNum in range(6):

			# SLIDER

			if (iWidgetNum == 0):		# Master Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_MASTERVOLUME", ())
				iInitialVal = 20-UserProfile.getMasterVolume()-1
				bNoSoundTrue = UserProfile.isMasterNoSound()
			elif (iWidgetNum == 1):		# Music Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_MUSICVOLUME", ())
				iInitialVal = 20-UserProfile.getMusicVolume()-1
				bNoSoundTrue = UserProfile.isMusicNoSound()
			elif (iWidgetNum == 2):		# Sound Effects Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_EFFECTSVOLUME", ())
				iInitialVal = 20-UserProfile.getSoundEffectsVolume()-1
				bNoSoundTrue = UserProfile.isSoundEffectsNoSound()
			elif (iWidgetNum == 3):		# Speech Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_SPEECHVOLUME", ())
				iInitialVal = 20-UserProfile.getSpeechVolume()-1
				bNoSoundTrue = UserProfile.isSpeechNoSound()
			elif (iWidgetNum == 4):		# Ambience Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_AMBIENCEVOLUME", ())
				iInitialVal = 20-UserProfile.getAmbienceVolume()-1
				bNoSoundTrue = UserProfile.isAmbienceNoSound()
			elif (iWidgetNum == 5):		# Interface Volume
				szWidgetDesc = localText.getText("TXT_KEY_OPTIONS_INTERFACEVOLUME", ())
				iInitialVal = 20-UserProfile.getInterfaceVolume()-1
				bNoSoundTrue = UserProfile.isInterfaceNoSound()

			islider = str(iWidgetNum)

			vbox = "VolumeSliderVBox"+islider
			tab.attachVBox("VolumePanelHBox", vbox)

			# Volume Slider
			szSliderDesc = szWidgetDesc
			szWidgetName = "VolumeSliderLabel"+islider
			tab.attachLabel(vbox, szWidgetName, szSliderDesc)
			tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

			szCallbackFunction = "handleVolumeSlidersInput"
			szWidgetName = "VolumeSlider_" + str(iWidgetNum)
			iMin = 0
			iMax = UserProfile.getVolumeStops()
			# iInitialVal set above
			tab.attachVSlider(vbox, szWidgetName, self.callbackIFace, szCallbackFunction, szWidgetName, iMin, iMax, iInitialVal)
			tab.setLayoutFlag(szWidgetName, "LAYOUT_SIZE_VEXPANDING")
			tab.setControlFlag(szWidgetName, "CF_SLIDER_FILL_DOWN")

			# CHECKBOX

			szOptionDesc = localText.getText("TXT_KEY_OPTIONS_NO_SOUND", ())
			szCallbackFunction = "handleVolumeCheckboxesInput"
			szWidgetName = "VolumeNoSoundCheckbox_" + str(iWidgetNum)
			# bNoSoundTrue set above
			tab.attachCheckBox(vbox, szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bNoSoundTrue)
			tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")


		tab.attachHSeparator("VolumePanelVBox", "SoundSeparator")

		tab.attachHBox("VolumePanelVBox", "SoundPanelHBox")
		tab.setLayoutFlag("SoundPanelHBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("SoundPanelHBox", "LAYOUT_SIZE_VPREFERRED")

		######################### Voice Config Section #########################

		tab.attachVBox("SoundPanelHBox", "VoiceVBox")

		# Checkbox
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_VOICE", ())
		szCallbackFunction = "handleVoiceCheckboxInput"
		self.szVoiceCheckboxName = "VoiceCheckbox"
		szWidgetName = "VoiceChatCheckbox"
		bUseVoice = UserProfile.useVoice()
		tab.attachCheckBox("VoiceVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bUseVoice)

		# Capture Device Dropdown
		tab.attachLabel("VoiceVBox", "VoiceCaptureLabel", localText.getText("TXT_KEY_OPTIONS_CAPTURE_DEVICE", ()))
		szDropdownDesc = "CaptureDeviceDropdownBox"
		aszDropdownElements = ()
		for iCaptureDevice in range(UserProfile.getNumCaptureDevices()):
			aszDropdownElements = aszDropdownElements + (UserProfile.getCaptureDeviceDesc(iCaptureDevice),)
		szCallbackFunction = "handleCaptureDeviceDropdownInput"
		szWidgetName = "CaptureDeviceDropdownBox"
		iInitialSelection = UserProfile.getCaptureDeviceIndex()
		tab.attachDropDown("VoiceVBox", szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Capture Volume Slider
		szSliderDesc = localText.getText("TXT_KEY_OPTIONS_CAPTUREVOLUME", ())
		szCallbackFunction = "handleCaptureVolumeSliderInput"
		szWidgetName = "CaptureVolumeSlider"
		iMin = 0
		iMax = UserProfile.getMaxCaptureVolume()
#		iInitialVal = iMax - UserProfile.getCaptureVolume()
		iInitialVal = UserProfile.getCaptureVolume()
		tab.attachHSlider("VoiceVBox", szWidgetName, self.callbackIFace, szCallbackFunction, szWidgetName, iMin, iMax, iInitialVal)
		tab.setControlFlag(szWidgetName, "CF_SLIDER_FILL_UP")

		# Playback Device Dropdown
		tab.attachLabel("VoiceVBox", "VoicePlaybackLabel", localText.getText("TXT_KEY_OPTIONS_PLAYBACK_DEVICE", ()))	# Label
		szDropdownDesc = "PlaybackDeviceDropdownBox"
		aszDropdownElements = ()
		for iPlaybackDevice in range(UserProfile.getNumPlaybackDevices()):
			aszDropdownElements = aszDropdownElements + (UserProfile.getPlaybackDeviceDesc(iPlaybackDevice),)
		szCallbackFunction = "handlePlaybackDeviceDropdownInput"
		szWidgetName = "PlaybackDeviceDropdownBox"
		iInitialSelection = UserProfile.getPlaybackDeviceIndex()
		tab.attachDropDown("VoiceVBox", szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Playback Volume Slider
		szSliderDesc = localText.getText("TXT_KEY_OPTIONS_PLAYBACKVOLUME", ())
		szCallbackFunction = "handlePlaybackVolumeSliderInput"
		szWidgetName = "PlaybackVolumeSlider"
		iMin = 0
		iMax = UserProfile.getMaxPlaybackVolume()
#		iInitialVal = iMax - UserProfile.getPlaybackVolume()
		iInitialVal = UserProfile.getPlaybackVolume()
		tab.attachHSlider("VoiceVBox", szWidgetName, self.callbackIFace, szCallbackFunction, szWidgetName, iMin, iMax, iInitialVal)
		tab.setControlFlag(szWidgetName, "CF_SLIDER_FILL_UP")

		######################### Speaker Config Dropdown #########################

		tab.attachVSeparator("SoundPanelHBox", "SoundVSeparator")

		tab.attachVBox("SoundPanelHBox", "SoundConfigVBox")

		tab.attachImage("SoundConfigVBox", "SoundBlasterLogo", CyArtFileMgr().getMiscArtInfo("SOUND_BLASTER_LOGO").getPath())

		tab.attachLabel("SoundConfigVBox", "SpeakerConfigLabel", localText.getText("TXT_KEY_OPTIONS_SPEAKERS", ()))	# Label
		szDropdownDesc = "SpeakerConfigDropdownBox"
		aszDropdownElements = ()
		iInitialSelection = 0
		for iSpeakerConfigLoop in range(15):
			szActiveConfigKey = UserProfile.getSpeakerConfigFromList(iSpeakerConfigLoop)
			szActiveConfig = localText.getText(szActiveConfigKey, ())
			aszDropdownElements = aszDropdownElements + (szActiveConfig,)
			if (UserProfile.getSpeakerConfig() == szActiveConfigKey):
				iInitialSelection = iSpeakerConfigLoop

		szCallbackFunction = "handleSpeakerConfigDropdownInput"
		szWidgetName = "SpeakerConfigDropdownBox"
		# iInitialSelection set above
		tab.attachDropDown("SoundConfigVBox", szWidgetName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_SIZE_HFIXEDEXPANDING")
		tab.setLayoutFlag(szWidgetName, "LAYOUT_LEFT")

		######################### Custom Audio Path #########################

		tab.attachHSeparator("SoundConfigVBox", "SoundSeparator")

		tab.attachHBox("SoundConfigVBox", "CustomPanelHBox")
		tab.setLayoutFlag("CustomPanelHBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CustomPanelHBox", "LAYOUT_SIZE_VPREFERRED")

		# Checkbox
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_CUSTOM_MUSIC", ())
		szCallbackFunction = "handleCustomMusicPathCheckboxInput"
		self.szCustomMusicCheckboxName = "CustomMusicPathCheckbox"
		szWidgetName = CvUtil.convertToStr(self.szCustomMusicCheckboxName)
		bUseCustomMusicPath = false
		if (UserProfile.getMusicPath() != ""):
			bUseCustomMusicPath = true
		tab.attachCheckBox("CustomPanelHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bUseCustomMusicPath)

		tab.attachHBox("CustomPanelHBox", "AudioPathHBox")
		tab.setLayoutFlag("AudioPathHBox", "LAYOUT_SIZE_HFIXEDEXPANDING")

		# Browse Button
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_BROWSE", ())
		szCallbackFunction = "handleCustomMusicPathButtonInput"
		szWidgetName = "CustomMusicPathButton"
		tab.attachButton("AudioPathHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		# Edit Box
		szEditBoxDesc = u""
		if (UserProfile.getMusicPath() != ""):
			szEditBoxDesc = CvUtil.convertToUnicode(UserProfile.getMusicPath())
		szWidgetName = "CustomMusicEditBox"
		szCallbackFunction = "DummyCallback"

		tab.attachEdit("AudioPathHBox", szWidgetName, szEditBoxDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		########## EXIT

		tab.attachHSeparator("AudioVBox", "AudioExitSeparator")

		tab.attachHBox("AudioVBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleAudioReset"
		szWidgetName = "AudioOptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "AudioOptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")


	def drawOtherTab(self):

		tab = self.pTabControl

		tab.attachVBox("OtherForm", "OtherVBox")

		tab.attachScrollPanel("OtherVBox", "OtherPanel")
		tab.setLayoutFlag("OtherPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("OtherPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("OtherPanel", "OtherPanelHBox")
		tab.setLayoutFlag("OtherPanelHBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("OtherPanelHBox", "LAYOUT_SIZE_HEXPANDING")


		########### CLOCK

		tab.attachVBox("OtherPanelHBox", "ClockVBox")
		tab.setLayoutFlag("ClockVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("ClockVBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("ClockVBox", "ClockLabel", localText.getText("TXT_KEY_OPTIONS_CLOCK", ()).upper() )

		tab.attachPanel("ClockVBox", "ClockPanel")
		tab.setStyle("ClockPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("ClockPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("ClockPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("ClockPanel", "ClockPanelVBox")
		tab.setLayoutFlag("ClockPanelVBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("ClockPanelVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Clock On Checkbox
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_CLOCK_ON", ())
		szCallbackFunction = "handleClockOnCheckboxInput"
		szWidgetName = "ClockOnCheckbox"
		bClockOn = UserProfile.isClockOn()
		tab.attachCheckBox("ClockPanelVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bClockOn)

		# 24 Hour Clock Checkbox
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_24CLOCK", ())
		szCallbackFunction = "handle24HourClockCheckboxInput"
		szWidgetName = "24HourClockCheckbox"
		b24HourClock = UserProfile.is24Hours()
		tab.attachCheckBox("ClockPanelVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, b24HourClock)

		# Edit Box Hours
		tab.attachLabel("ClockPanelVBox", "HoursLabel", localText.getText("TXT_KEY_OPTIONS_HOURS", ()))	# Label
		szEditBoxDesc = str(getAlarmHourLeft())
		szCallbackFunction = "DummyCallback"
		szWidgetName = "AlarmHourEditBox"
		tab.attachEdit("ClockPanelVBox", szWidgetName, szEditBoxDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		# Edit Box Mins
		tab.attachLabel("ClockPanelVBox", "MinsLabel", localText.getText("TXT_KEY_OPTIONS_MINS", ()))	# Label
		szEditBoxDesc = str(getAlarmMinLeft())
		szCallbackFunction = "DummyCallback"
		szWidgetName = "AlarmMinEditBox"
		tab.attachEdit("ClockPanelVBox", szWidgetName, szEditBoxDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		# Alarm On Checkbox
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_ALARMON", ())
		szCallbackFunction = "handleAlarmOnCheckboxInput"
		szWidgetName = "AlarmOnCheckbox"
		bAlarmOn = isAlarmOn()
		tab.attachCheckBox("ClockPanelVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName, bAlarmOn)


		########### PROFILE

		UserProfile.loadProfileFileNames()

		tab.attachVBox("OtherPanelHBox", "ProfileVBox")
		tab.setLayoutFlag("ProfileVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("ProfileVBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("ProfileVBox", "ProfileLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_PROFILES", ()).upper() )

		tab.attachPanel("ProfileVBox", "ProfilePanel")
		tab.setStyle("ProfilePanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("ProfilePanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("ProfilePanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("ProfilePanel", "ProfilePanelVBox")
		tab.setLayoutFlag("ProfilePanelVBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("ProfilePanelVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")


		# Profiles Dropdown

		tab.attachLabel("ProfilePanelVBox", "ProfileComboLabel", localText.getText("TXT_KEY_OPTIONS_SCREEN_PROFILES", ()))

		szDropdownDesc = "ProfilesDropdownBox"
		aszDropdownElements = ()
		iInitialSelection = 0
		for iProfileLoop in range(UserProfile.getNumProfileFiles()):
			szProfileFileName = UserProfile.getProfileFileName(iProfileLoop)

			# Cut off file path and extension
			szProfile = szProfileFileName[szProfileFileName.find("PROFILES\\")+9:-4]

			aszDropdownElements = aszDropdownElements + (szProfile,)

# >>> CYBERFRONT // profile:
#			if (UserProfile.getProfileName() == szProfile):
			if (UserProfile.getProfileName() == CvUtil.convertToStr(szProfile)):
# <<< CYBERFRONT
				iInitialSelection = iProfileLoop

		szCallbackFunction = "handleProfilesDropdownInput"
		szWidgetName = "ProfilesDropdownBox"
		# iInitialSelection set above
		tab.attachDropDown("ProfilePanelVBox",szWidgetName,szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szWidgetName, iInitialSelection)

		# Edit Box ProfileName
		tab.attachLabel("ProfilePanelVBox","ProfilesName",localText.getText("TXT_KEY_OPTIONS_SCREEN_PROFILE_NAME", ()))	# Label


		#szCallbackIFace = ""
		szEditBoxDesc = UserProfile.getProfileName()
		szCallbackFunction = "DummyCallback"
		szWidgetName = "ProfileNameEditBox"
		szWideEditBoxDesc = CvUtil.convertToUnicode(szEditBoxDesc)
		tab.attachEdit("ProfilePanelVBox", szWidgetName, szWideEditBoxDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		# New Profile Button
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_NEW_PROFILE", ())
		szCallbackFunction = "handleNewProfileButtonInput"
		szWidgetName = "NewProfileButton"
		tab.attachButton("ProfilePanelVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		# Delete Profile Button
		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_DELETE_PROFILE", ())
		szCallbackFunction = "handleDeleteProfileButtonInput"
		szWidgetName = "DeleteProfileButton"
		tab.attachButton("ProfilePanelVBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)


		########## NETWORKING

		tab.attachVBox("OtherPanelHBox", "NetVBox")
		tab.setLayoutFlag("NetVBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("NetVBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("NetVBox", "NetLabel", localText.getText("TXT_KEY_OPTIONS_NETWORK", ()).upper() )

		tab.attachPanel("NetVBox", "NetPanel")
		tab.setStyle("NetPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("NetPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("NetPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("NetPanel", "NetPanelVBox")
		tab.setLayoutFlag("NetPanelVBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("NetPanelVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Radio Buttons
		tab.attachLabel("NetPanelVBox", "NetBandwidthLabel", localText.getText("TXT_KEY_OPTIONS_BANDWIDTH_DESC", ()) )

		bIsModem = gc.getGame().isModem()
		szCallbackFunction = "handleBroadbandSelected"
		szWidgetName = "BroadbandSelection"
		szWidgetLbl = localText.getText("TXT_KEY_OPTIONS_BROADBAND_LBL", ())
		tab.attachRadioButton("NetPanelVBox", szWidgetName, szWidgetLbl, self.callbackIFace, szCallbackFunction, str(szWidgetName), (not bIsModem))

		szCallbackFunction = "handleModemSelected"
		szWidgetName = "ModemSelection"
		szWidgetLbl = localText.getText("TXT_KEY_OPTIONS_MODEM_LBL", ())
		tab.attachRadioButton("NetPanelVBox", szWidgetName, szWidgetLbl, self.callbackIFace, szCallbackFunction, str(szWidgetName), bIsModem)


		########## EXIT

		tab.attachHSeparator("OtherVBox", "OtherExitSeparator")

		tab.attachHBox("OtherVBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleOtherReset"
		szWidgetName = "OtherOptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "OtherOptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE1Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE1Form", "CGE1VBox")
		tab.attachScrollPanel("CGE1VBox", "CGE1Panel")
		tab.setLayoutFlag("CGE1Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE1Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("CGE1Panel", "CGE1PanelHBox")
		tab.setLayoutFlag("CGE1PanelHBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE1PanelHBox", "LAYOUT_SIZE_HEXPANDING")

		# Mod On/Off
		tab.attachVBox("CGE1PanelHBox", "CGE1OPT1VBox")
		tab.setLayoutFlag("CGE1OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE1OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE1OPT1VBox", "OPT1Label", localText.getText("TXT_KEY_CGE_OPTSCR_MOD_ONOFF", ()))

		tab.attachPanel("CGE1OPT1VBox", "CGE1OPT1Panel")
		tab.setStyle("CGE1OPT1Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE1OPT1Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE1OPT1Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Civ Name Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_CIVNAME", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECivName"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Master Name Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_MASTERNAME", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMasterName"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Info Panel Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_CITYINFOPANEL", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECityInfoPS"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Diplomacy Attitude Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_DIPROMACYATTITUDE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEDiplomacyAttitude"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Combat Experience Counter Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_COMBATEXPERIENCECOUNTER", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECombatExperienceCounter"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Game Turn Bar Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_GAMETURNBAR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEGameTurnBar"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Great Person Bar Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_GREATPERSONBAR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEGreatPersonBar"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Top Culture Cities Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_TOPCULTURECITIES", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETopCultureCities"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Spy Detect Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_SPYDETECT", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGESpyDetect"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		#try:
		#	if (CyGlobalContext().isCGEBuild()):
		#		tab.attachHSeparator("CGE1OPT1Panel", "CGEOptionSeparator")
		#		#tab.attachLabel("CGE1OPT1Panel", "DLLOptionLabel", "DLL Options")	# Label

		#		# Winamp GUI Checkbox
		#		#szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_WINAMPGUI", ())
		#		#szCallbackFunction = "CGESetOptionCheckBoxInput"
		#		#szOptionName = "CGEWinampGUI"
		#		#Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		#		#tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		#		# Display Current Civics Checkbox
		#		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_DISPLAY_CURRENT_CIVICS", ())
		#		szCallbackFunction = "CGESetOptionCheckBoxInput"
		#		szOptionName = "CGEDisplayCurrentCivics"
		#		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		#		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		#		# Display Additional city help Checkbox
		#		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ADDITIONAL_CITY_HELP", ())
		#		szCallbackFunction = "CGESetOptionCheckBoxInput"
		#		szOptionName = "CGEDisplayAdditionalCityHelp"
		#		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		#		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		#		# Display City rank on production menu Checkbox
		#		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_RANK_ON_PRODUCTION_MENU", ())
		#		szCallbackFunction = "CGESetOptionCheckBoxInput"
		#		szOptionName = "CGEDisplayCityRankOnProductionMenu"
		#		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		#		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		#		# Total Yield From City Fat Cross Checkbox
		#		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TOTAL_YIELD_FROM_CITY_FAT_CROSS", ())
		#		szCallbackFunction = "CGESetOptionCheckBoxInput"
		#		szOptionName = "CGETotalYieldFromCityFatCross"
		#		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		#		tab.attachCheckBox("CGE1OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)


		#except:
		#	pass

		# Trade Resource Panel
		tab.attachVBox("CGE1PanelHBox", "CGE1OPT2VBox")
		tab.setLayoutFlag("CGE1OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE1OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE1OPT2VBox", "CGE1OPT21VBox")
		tab.setLayoutFlag("CGE1OPT21VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE1OPT21VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE1OPT21VBox", "TRPLabel", "Trade Resource Panel")

		tab.attachPanel("CGE1OPT21VBox", "CGE1TRPPanel")
		tab.setStyle("CGE1TRPPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE1TRPPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE1TRPPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("CGE1TRPPanel", "CGE1TRPPanelVBox")
		tab.setLayoutFlag("CGE1TRPPanelVBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE1TRPPanelVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Show
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRP_SHOW", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETRPShow"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1TRPPanelVBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Each  Civilization Trade
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRP_SHOW_EACH_TRADE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETRPShowEachTrade"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1TRPPanelVBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Small Icons
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRP_SMALL", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETRPSmallIcons"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1TRPPanelVBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Compress Mode
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRP_COMPRESS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETRPCompressMode"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1TRPPanelVBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Imports and Exports
		tab.attachLabel("CGE1TRPPanelVBox", "TRPImportsExportsLabel", localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION1", ()))	# Label
		szDropdownDesc = "TRPImportsExportsDropdownBox"

		aszDropdownElements = ()
		for i in range(3):
			aszDropdownElements += (localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION1_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "TRPImportsExports"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE1TRPPanelVBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Technologies and Resources
		tab.attachLabel("CGE1TRPPanelVBox", "TRPTechResLabel", localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION2", ()))	# Label
		szDropdownDesc = "TRPTechResDropdownBox"

		aszDropdownElements = ()
		for i in range(4):
			aszDropdownElements += (localText.getText("TXT_KEY_TRADE_REDSOURCE_OPTION2_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "TRPTechRes"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE1TRPPanelVBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Dead Civ Scoreboard
		tab.attachVBox("CGE1OPT2VBox", "CGE1OPT22VBox")
		tab.setLayoutFlag("CGE1OPT22VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE1OPT22VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE1OPT22VBox", "OPT122Label", "Dead Civ Scoreboard")

		tab.attachPanel("CGE1OPT22VBox", "CGE1OPT22Panel")
		tab.setStyle("CGE1OPT22Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE1OPT22Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE1OPT22Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Hide Dead Civilizations
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_HIDE_DEAD_CIV", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEHideDeadCivilizations"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Grey Out Dead Civilizations
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_GREYOUT_DEAD_CIV", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEGreyOutDeadCivilizations"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Dead Tag
		szOptionDesc =localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_DEAD_TAG", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowDeadTag"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE1OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		########## EXIT

		tab.attachHSeparator("CGE1VBox", "CGE1ExitSeparator")

		tab.attachHBox("CGE1VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions1Reset"
		szWidgetName = "CGE1OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE1OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE2Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE2Form", "CGE2VBox")
		tab.attachScrollPanel("CGE2VBox", "CGE2Panel")
		tab.setLayoutFlag("CGE2Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE2Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("CGE2Panel", "CGE2PanelHBox")
		tab.setLayoutFlag("CGE2PanelHBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE2PanelHBox", "LAYOUT_SIZE_HEXPANDING")

		tab.attachVBox("CGE2PanelHBox", "CGE2OPT2VBox")
		tab.setLayoutFlag("CGE2OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE2OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		# Alerts Log
		tab.attachLabel("CGE2OPT2VBox", "OPT223Label", "Alerts Log")

		tab.attachPanel("CGE2OPT2VBox", "CGE2OPT3Panel")
		tab.setStyle("CGE2OPT3Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE2OPT3Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE2OPT3Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		tab.attachHBox("CGE2OPT3Panel", "CGE2OPT3HBox")

		tab.attachVBox("CGE2OPT3HBox", "CGE2OPT3VBox1")
		tab.setLayoutFlag("CGE2OPT3VBox1", "LAYOUT_SIZE_HEXPANDING")
		tab.attachVSeparator("CGE2OPT3Panel", "CGE2OPT3PanelSeparator")
		tab.attachVBox("CGE2OPT3HBox", "CGE2OPT3VBox2")
		tab.setLayoutFlag("CGE2OPT3VBox2", "LAYOUT_SIZE_HEXPANDING")
		tab.attachVSeparator("CGE2OPT3Panel", "CGE2OPT4PanelSeparator")
		tab.attachVBox("CGE2OPT3HBox", "CGE2OPT3VBox3")
		tab.setLayoutFlag("CGE2OPT3VBox3", "LAYOUT_SIZE_HEXPANDING")

		tab.attachLabel("CGE2OPT3VBox1", "AlertsLogTime1Label", localText.getText("TXT_KEY_CGE_OPTSCR_ALERTSLOG_DISPLAY_TIME", (1,)))	# Label
		szDropdownDesc = "AlertsLogTime1DropdownBox"

		aszDropdownElements = ("0", "5", "10", "15", "20", "25")

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "AlertsLogDisplayTime1"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE2OPT3VBox1", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Cut Level
		tab.attachLabel("CGE2OPT3VBox2", "AlertsLogTime2Label", localText.getText("TXT_KEY_CGE_OPTSCR_ALERTSLOG_DISPLAY_TIME", (2,)))	# Label
		szDropdownDesc = "AlertsLogTime1DropdownBox"
		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "AlertsLogDisplayTime2"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE2OPT3VBox2", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Display Time
		tab.attachLabel("CGE2OPT3VBox3", "AlertsLogTime3Label", localText.getText("TXT_KEY_CGE_OPTSCR_ALERTSLOG_DISPLAY_TIME", (3,)))	# Label
		szDropdownDesc = "AlertsLogTime1DropdownBox"
		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "AlertsLogDisplayTime3"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE2OPT3VBox3", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Civ4lerts
		tab.attachLabel("CGE2OPT2VBox", "OPT22Label", "Civ4lerts")

		tab.attachPanel("CGE2OPT2VBox", "CGE2OPT2Panel")
		tab.setStyle("CGE2OPT2Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE2OPT2Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE2OPT2Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		tab.attachHBox("CGE2OPT2Panel", "CGE2OPT2HBox")

		tab.attachVBox("CGE2OPT2HBox", "CGE2OPT2VBox1")
		tab.setLayoutFlag("CGE2OPT2VBox1", "LAYOUT_SIZE_HEXPANDING")
		tab.attachVSeparator("CGE2OPT2Panel", "CGE2OPT2PanelSeparator")
		tab.attachVBox("CGE2OPT2HBox", "CGE2OPT2VBox2")
		tab.setLayoutFlag("CGE2OPT2VBox2", "LAYOUT_SIZE_HEXPANDING")

		# City Pending Growth Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_PENDING_GROWTH", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityPendingGrowth"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Pending Unhealthy Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_PENDING_UNHEALTHY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityPendingUnhealthy"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Pending Angry Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_PENDING_ANGRY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityPendingAngry"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Growth Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_GROWTH", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityGrowth"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Growth Unhealthy Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_GROWTH_UNHEALTHY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityGrowthUnhealthy"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# City Growth Angry Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CITY_GROWTH_ANGRY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsCityGrowthAngry"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox1", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Gold Trade Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_GOLD_TRADE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsGoldTrade"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox2", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachLabel("CGE2OPT2VBox2", "GoldTradeThresholdLabel", localText.getText("TXT_KEY_CGE_OPTSCR_GOLD_TRADE_THRESHOLD", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGECiv4lertsGoldTradeThreshold"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE2OPT2VBox2", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)

		# Gold Per Turn Trade Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_GOLD_PER_TURN_TRADE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECiv4lertsGoldPerTurnTrade"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT2VBox2", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachLabel("CGE2OPT2VBox2", "GoldTradeThresholdLabel", localText.getText("TXT_KEY_CGE_OPTSCR_GOLD_PER_TURN_TRADE_THRESHOLD", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGECiv4lertsGoldPerTurnTradeThreshold"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE2OPT2VBox2", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setLayoutFlag(szOptionName, "LAYOUT_SIZE_HPREFERREDEXPANDING")

		# Alerts
		tab.attachLabel("CGE2OPT2VBox", "OPT224Label", "Alerts")

		tab.attachPanel("CGE2OPT2VBox", "CGE2OPT4Panel")
		tab.setStyle("CGE2OPT4Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE2OPT4Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE2OPT4Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		tab.attachVBox("CGE2OPT4Panel", "CGE2OPT4VBox")

		# Interfere
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALERT_INTERFERE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlertsInterference"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT4VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Obsolete Angry
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALERT_OBSOLETE_ANGRY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlertsObsolete"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT4VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Steal Tech
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALERT_SPY_STEAL_TECH", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlertsSpyStealTech"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT4VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Executive Briefing On/Off
		tab.attachVBox("CGE2PanelHBox", "CGE2OPT1VBox")
		tab.setLayoutFlag("CGE2OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE2OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE2OPT1VBox", "CGE2OPT21VBox")
		tab.setLayoutFlag("CGE2OPT21VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE2OPT21VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE2OPT21VBox", "OPT21Label", "Executive Briefing")

		tab.attachPanel("CGE2OPT21VBox", "CGE2OPT21Panel")
		tab.setStyle("CGE2OPT21Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE2OPT1Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE2OPT1Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Executive Briefing Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_EXECUTIVE_BRIEFING", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEExecutiveBriefing"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT21Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# More Civ4lerts On/Off
		tab.attachVBox("CGE2OPT1VBox", "CGE2OPT22VBox")
		tab.setLayoutFlag("CGE2OPT22VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE2OPT22VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE2OPT22VBox", "OPT22Label", "MoreCiv4lerts")

		tab.attachPanel("CGE2OPT22VBox", "CGE2OPT22Panel")
		tab.setStyle("CGE2OPT22Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE2OPT22Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE2OPT22Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# More Civ4lerts Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MORE_CIV4LERTS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMoreCiv4lerts"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# More Civ4lerts CheckForDomPopVictory Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CHECK_DOM_POP_VICTORY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMoreCiv4lertsCheckForDomPopVictory"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachLabel("CGE2OPT22Panel", "PopThresholdLabel", localText.getText("TXT_KEY_CGE_OPTSCR_POP_THRESHOLD", ()))	# Label
		szCallbackFunction = "CGESetOptionEditFloatBoxInput"
		szOptionName = "CGEMoreCiv4lertsPopThreshold"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE2OPT22Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)

		# More Civ4lerts CheckForDomLandVictory Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CHECK_DOM_LAND_VICTORY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMoreCiv4lertsCheckForDomLandVictory"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachLabel("CGE2OPT22Panel", "LandThresholdLabel", localText.getText("TXT_KEY_CGE_OPTSCR_LAND_THRESHOLD", ()))	# Label
		szCallbackFunction = "CGESetOptionEditFloatBoxInput"
		szOptionName = "CGEMoreCiv4lertsLandThreshold"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE2OPT22Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)

		# More Civ4lerts CheckForCityBorderExpansion Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CHECK_CITY_BORDER_EXPANSION", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMoreCiv4lertsCheckForCityBorderExpansion"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# More Civ4lerts CheckForNewTrades Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_CHECK_NEW_TRADES", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEMoreCiv4lertsCheckForNewTrades"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE2OPT22Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		########## EXIT

		tab.attachHSeparator("CGE2VBox", "CGE2ExitSeparator")

		tab.attachHBox("CGE2VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions2Reset"
		szWidgetName = "CGE2OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE2OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE3Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE3Form", "CGE3VBox")
		tab.attachScrollPanel("CGE3VBox", "CGE3Panel")
		tab.setLayoutFlag("CGE3Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("CGE3Panel", "CGE3PanelHBox")
		tab.setLayoutFlag("CGE3PanelHBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE3PanelHBox", "LAYOUT_SIZE_HEXPANDING")

		# Mod On/Off
		tab.attachVBox("CGE3PanelHBox", "CGE3OPT1VBox")
		tab.setLayoutFlag("CGE3OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE3OPT1VBox", "OPT3Label", "APL General")

		tab.attachPanel("CGE3OPT1VBox", "CGE3OPT1Panel")
		tab.setStyle("CGE3OPT1Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE3OPT1Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT1Panel", "LAYOUT_SIZE_VEXPANDING")

		# APL Enabled Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_APL_ENABLED", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLEnabled"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Stack Mode
		tab.attachLabel("CGE3OPT1Panel", "APLStackModeLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_STACK_MODE", ()))	# Label
		szDropdownDesc = "APLStackModeDropdownBox"

		aszDropdownElements = (localText.getText("TXT_KEY_APL_MODE_MULTILINE", ()),
								localText.getText("TXT_KEY_APL_MODE_STACK_VERT", ()),
								localText.getText("TXT_KEY_APL_MODE_STACK_HORIZ", ()))

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "APLStackMode"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE3OPT1Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Compress Mode Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_APL_COMPRESS_MODE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLCompress"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Mission Info Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MISSION_INFO", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLMissionInfo"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Health Bar Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_HEALTH_BAR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLHealthBar"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Upgrade Indicator Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_UPGRADE_INDICATOR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLUpgradeIndicator"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Promotion Indicator Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_PROMOTION_INDICATOR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLPromotionIndicator"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Wounded Indicator Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_WOUNDED_INDICATOR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLWoundedIndicator"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Warlord Indicator Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_WARLORD_INDICATOR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAPLWarlordIndicator"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE3OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Info Panel
		tab.attachVBox("CGE3PanelHBox", "CGE3OPT3VBox")
		tab.setLayoutFlag("CGE3OPT3VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT3VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE3OPT3VBox", "OPT33Label", "APL Info Panel")

		tab.attachPanel("CGE3OPT3VBox", "CGE3OPT3Panel")
		tab.setStyle("CGE3OPT3Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE3OPT3Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT3Panel", "LAYOUT_SIZE_VEXPANDING")

		# x position
		tab.attachLabel("CGE3OPT3Panel", "XPotitionLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_X_POSITION", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEXPosition"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE3OPT3Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# y position
		tab.attachLabel("CGE3OPT3Panel", "YPotitionLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_Y_POSITION", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEYPosition"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE3OPT3Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# x Size
		tab.attachLabel("CGE3OPT3Panel", "XSizeLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_X_SIZE", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEXSize"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE3OPT3Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Pixel Per Line Type 1
		tab.attachLabel("CGE3OPT3Panel", "PixelPerLineType1Label", localText.getText("TXT_KEY_CGE_OPTSCR_APL_PIXEL_PER_LINE1", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEPixelPerLineType1"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE3OPT3Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Pixel Per Line Type 2
		tab.attachLabel("CGE3OPT3Panel", "PixelPerLineType2Label", localText.getText("TXT_KEY_CGE_OPTSCR_APL_PIXEL_PER_LINE2", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEPixelPerLineType2"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE3OPT3Panel", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Info Pane Colors
		tab.attachVBox("CGE3PanelHBox", "CGE3OPT2VBox")
		tab.setLayoutFlag("CGE3OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE3OPT2VBox", "OPT32Label", "APL Info Pane Colors")

		tab.attachPanel("CGE3OPT2VBox", "CGE3OPT2Panel")
		tab.setStyle("CGE3OPT2Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE3OPT2Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT2Panel", "LAYOUT_SIZE_VEXPANDING")

		# Unit Name Color
		tab.attachLabel("CGE3OPT2Panel", "APLUnitNameColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_UNIT_NAME_COLOR", ()))	# Label
		szDropdownDesc = "APLUnitNameColorDropdownBox"

		aszDropdownElements = CGEOptionControl.CGEOptionControl().getColorIndex()

		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLUnitNameColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT2Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Upgrade Possible Color
		tab.attachLabel("CGE3OPT2Panel", "APLUpgradePossibleColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_UPGRADE_POSSIBLE_COLOR", ()))	# Label
		szDropdownDesc = "APLUpgradePossibleColorDropdownBox"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLUpgradePossibleColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT2Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Upgrade Not Possible Color
		tab.attachLabel("CGE3OPT2Panel", "APLUpgradeNotPossibleColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_UPGRADE_NOT_POSSIBLE_COLOR", ()))	# Label
		szDropdownDesc = "APLUpgradeNotPossibleColorDropdownBox"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLUpgradeNotPossibleColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT2Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Promotion Specialties Color
		tab.attachLabel("CGE3OPT2Panel", "APLPromotionSpecialtiesColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_PROMOTION_SPECIALITIES_COLOR", ()))	# Label
		szDropdownDesc = "APLPromotionSpecialtiesColorDropdownBox"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLPromotionSpecialtiesColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT2Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Unit Type Specialties Color
		tab.attachLabel("CGE3OPT2Panel", "APLUnitTypeSpecialtiesColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_UNIT_TYPE_SPECIALITIES_COLOR", ()))	# Label
		szDropdownDesc = "APLUnitTypeSpecialtiesColorDropdownBox"

		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLUnitTypeSpecialtiesColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT2Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# APL Stacked Bar Colors
		tab.attachVBox("CGE3PanelHBox", "CGE3OPT4VBox")
		tab.setLayoutFlag("CGE3OPT4VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE3OPT4VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE3OPT4VBox", "OPT34Label", "APL Stacked Bar Colors")

		tab.attachPanel("CGE3OPT4VBox", "CGE3OPT4Panel")
		tab.setStyle("CGE3OPT4Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE3OPT4Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE3OPT4Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Health Color
		tab.attachLabel("CGE3OPT4Panel", "APLHealthColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_HEALTH_COLOR", ()))	# Label
		szDropdownDesc = "APLUnitHealthColorDropdownBox"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLHealthColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT4Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Wounded Color
		tab.attachLabel("CGE3OPT4Panel", "APLWoundedColorLabel", localText.getText("TXT_KEY_CGE_OPTSCR_APL_WOUNDED_COLOR", ()))	# Label
		szDropdownDesc = "APLUnitHealthColorDropdownBox"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "APLWoundedColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE3OPT4Panel", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		########## EXIT

		tab.attachHSeparator("CGE3VBox", "CGE3ExitSeparator")

		tab.attachHBox("CGE3VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions3Reset"
		szWidgetName = "CGE3OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE3OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE5Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE5Form", "CGE5VBox")
		tab.attachScrollPanel("CGE5VBox", "CGE5Panel")
		tab.setLayoutFlag("CGE5Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("CGE5Panel", "CGE5PanelHBox")
		#tab.setStyle("CGE5Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE5PanelHBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE5PanelHBox", "LAYOUT_SIZE_HEXPANDING")

		tab.attachVBox("CGE5PanelHBox", "CGE5OPT1VBox")
		tab.setLayoutFlag("CGE5OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE5OPT1VBox", "OPT51Label", localText.getText("TXT_KEY_CGE_OPTSCR_MOD_ONOFF", ()))

		tab.attachPanel("CGE5OPT1VBox", "CGE5OPT1Panel")
		tab.setStyle("CGE5OPT1Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE5OPT1Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE5OPT1Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		# Raw Commerce Display Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_RAWCOMMERECEDISPLAY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGERawCommerceDisplay"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Citizens Automated Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_CITIZENS_AUTOMATED", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGECitizensAutomated"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Bottom Container Icon
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_BOTTOM_CONTAINER_ICON", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEBottomContainerIcon"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT1Panel", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachVBox("CGE5PanelHBox", "CGE5OPT2VBox")
		tab.setLayoutFlag("CGE5OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGE5OPT2VBox", "OPT52Label", "Specialist Stacker")

		tab.attachPanel("CGE5OPT2VBox", "CGE5OPT2Panel")
		tab.setStyle("CGE5OPT2Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE5OPT2Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE5OPT2Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("CGE5OPT2Panel", "CGE5OPT2HBox")
		tab.setLayoutFlag("CGE5OPT2HBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5OPT2HBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE5OPT2HBox", "CGE5OPT21VBox")
		tab.setLayoutFlag("CGE5OPT21VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5OPT21VBox", "LAYOUT_SIZE_VEXPANDING")

		# Enabled
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SPECIALIST_STACKER_ENABLED", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGESpecialistStackerEnabled"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT21VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Specialist Stack Width
		tab.attachLabel("CGE5OPT21VBox", "SpecialistStackWidthLabel", localText.getText("TXT_KEY_CGE_OPTSCR_SPECIALIST_STACK_WIDTH", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGESpecialistStackWidth"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE5OPT21VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_SPECIALIST_STACK_WIDTH", ()))

		# Highlight Forced Specialists
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_HIGHLIGHT_FORCED_SPECIALISTS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEHighlightForcedSpecialists"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT21VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Stack Super Specialists
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_STACK_SUPER_SPECIALISTS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEStackSuperSpecialists"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT21VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Max Super Specialist Buttons
		tab.attachLabel("CGE5OPT21VBox", "MaxSuperSpecialistButtons", localText.getText("TXT_KEY_CGE_OPTSCR_MAX_SUPER_SPECIALIST_BUTTONS", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEMaxSuperSpecialistButtons"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE5OPT21VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Super Specialist Stack Width
		tab.attachLabel("CGE5OPT21VBox", "SuperSpecialistStackWidth", localText.getText("TXT_KEY_CGE_OPTSCR_SUPER_SPECIALIST_STACK_WIDTH", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGESuperSpecialistStackWidth"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE5OPT21VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# 
		tab.attachVSeparator("CGE5OPT2HBox", "CGE5PanelHBoxSeparator")
		tab.attachVBox("CGE5OPT2HBox", "CGE5OPT22VBox")
		tab.setLayoutFlag("CGE5OPT22VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE5OPT22VBox", "LAYOUT_SIZE_VEXPANDING")

		# Display Unique Super Specialists Only
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_DISPLAY_UNIUE_SUPER_SPECIALISTS_ONLY", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEDisplayUniqueSuperSpecialistsOnly"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT22VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Dynamic Super Specialists Spacing
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_DYNAMIC_SUPER_SPECIALISTS_SPACING", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEDynamicSuperSpecialistsSpacing"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT22VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Stack Angry Citizens
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_STACK_ANGRY_CITIZENS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEStackAngryCitizens"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT22VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Max Angry Citizen Buttons
		tab.attachLabel("CGE5OPT22VBox", "MaxAngryCitizenButtons", localText.getText("TXT_KEY_CGE_OPTSCR_MAX_ANGRY_CITIZEN_BUTTONS", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEMaxAngryCitizenButtons"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE5OPT22VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Angry Citizen Stack Width
		tab.attachLabel("CGE5OPT22VBox", "AngryCitizenStackWidth", localText.getText("TXT_KEY_CGE_OPTSCR_ANGRY_CITIZEN_STACK_WIDTH", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEAngryCitizenStackWidth"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE5OPT22VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Dynamic Angry Citizen Spacing
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_DYNAMIC_ANGRY_CITIZEN_SPACING", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEDynamicAngryCitizenSpacing"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE5OPT22VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Dummy
		#tab.attachVBox("CGE5PanelHBox", "CGE5OPT3VBox")
		#tab.setLayoutFlag("CGE5OPT3VBox", "LAYOUT_SIZE_HEXPANDING")
		#tab.setLayoutFlag("CGE5OPT3VBox", "LAYOUT_SIZE_VEXPANDING")

		#tab.attachLabel("CGE5OPT3VBox", "OPT53Label", "                              ")

		#tab.attachPanel("CGE5OPT3VBox", "CGE5OPT3Panel")
		#tab.setStyle("CGE5OPT3Panel", "Panel_Tan15_Style")
#		tab.setLayoutFlag("CGE5OPT3Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
#		tab.setLayoutFlag("CGE5OPT3Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		########## EXIT

		tab.attachHSeparator("CGE5VBox", "CGE5ExitSeparator")

		tab.attachHBox("CGE5VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions5Reset"
		szWidgetName = "CGE5OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE5OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE6Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE6Form", "CGE6VBox")
		tab.attachScrollPanel("CGE6VBox", "CGE6Panel")
		tab.setLayoutFlag("CGE6Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE6Panel", "CGE6OPT0VBox")
		tab.setLayoutFlag("CGE6OPT0VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT0VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT0VBox", "LAYOUT_SIZE_VEXPANDING")
		tab.attachLabel("CGE6OPT0VBox", "OPT6Label", "Not Just Another Game Clock Mod")

		tab.attachPanel("CGE6OPT0VBox", "CGE6OPT0Panel")
		tab.setStyle("CGE6OPT0Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE6OPT0Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE6OPT0Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("CGE6OPT0Panel", "CGE6OPTPanel")
		tab.setLayoutFlag("CGE6OPTPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPTPanel", "LAYOUT_SIZE_VEXPANDING")

		# APL Info Pane Colors
		tab.attachVBox("CGE6OPTPanel", "CGE6OPT1VBox")
		tab.setLayoutFlag("CGE6OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		# Alternate Time Text
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATE_TIME_TEXT", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlternateTimeText"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Alternating Time
		tab.attachLabel("CGE6OPT1VBox", "AlternatingTimeLabel", localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATING_TIME", ()))	# Label
		szCallbackFunction = "CGESetOptionEditIntBoxInput"
		szOptionName = "CGEAlternatingTime"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachEdit("CGE6OPT1VBox", szOptionName, str(Value), self.callbackIFace, szCallbackFunction, szOptionName)

		# Show Turns
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_TURNS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowTurns"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Game Clock
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_GAME_CLOCK", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowGameClock"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Game Completed Percent
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_GAME_COMPLETED_PERCENT", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowGameCompletedPercent"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Game Completed Turns
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_GAME_COMPLETED_TURNS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowGameCompletedTurns"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Alternate Show Turns
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATE_SHOW_TURNS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlternateShowTurns"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Alternate Show Game Clock
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATE_SHOW_GAME_CLOCK", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlternateShowGameClock"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Alternate Show Game Completed Percent
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATE_SHOW_GAME_COMPLETED_PERCENT", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlternateShowGameCompletedPercent"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Alternate Show Game Completed Turns
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_ALTERNATE_SHOW_GAME_COMPLETED_TURNS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEAlternateShowGameCompletedTurns"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Era Colors
		tab.attachVSeparator("CGE6OPTPanel", "CGE6PanelHBoxSeparator1")

		tab.attachVBox("CGE6OPTPanel", "CGE6OPT2VBox")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE6OPT2VBox", "CGE6OPT21VBox")
		tab.setLayoutFlag("CGE6OPT21VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT21VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT21VBox", "LAYOUT_SIZE_VEXPANDING")

		# Show Era
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_ERA", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowEra"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT21VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Reflect Era In Turn Color
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_REFLECT_ERA_IN_TURN_COLOR", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowReflectEraInTurnColor"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE6OPT21VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachHBox("CGE6OPT2VBox", "CGE6OPT22HBox")
		tab.setLayoutFlag("CGE6OPT22HBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT22HBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT22HBox", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE6OPT22HBox", "CGE6OPT2VBox")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

		# color value = index + 2
		aszDropdownElements = CGEOptionControl.CGEOptionControl().getColorIndex()

		# Ancient Era Color
		tab.attachLabel("CGE6OPT2VBox", "AncientEraColorLabel", gc.getEraInfo(0).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Ancient Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "AncientEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT2VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Classical Era Color
		tab.attachLabel("CGE6OPT2VBox", "ClassicalEraColorLabel", gc.getEraInfo(1).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Classical Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "ClassicalEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT2VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Medieval Era Color
		tab.attachLabel("CGE6OPT2VBox", "MedievalEraColorLabel", gc.getEraInfo(2).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Medieval Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "MedievalEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT2VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Renaissance Era Color
		tab.attachLabel("CGE6OPT2VBox", "RenaissanceEraColorLabel", gc.getEraInfo(3).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Renaissance Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "RenaissanceEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT2VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		#tab.attachVSeparator("CGE6PanelHBox", "CGE6PanelHBoxSeparator2")
		tab.attachVBox("CGE6OPT22HBox", "CGE6OPT3VBox")
		tab.setLayoutFlag("CGE6OPT3VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE6OPT3VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE6OPT3VBox", "LAYOUT_SIZE_VEXPANDING")

		# Industrial Era Color
		tab.attachLabel("CGE6OPT3VBox", "IndustrialEraColorLabel", gc.getEraInfo(4).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Industrial Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "IndustrialEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Modern Era Color
		tab.attachLabel("CGE6OPT3VBox", "ModernEraColorLabel", gc.getEraInfo(5).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Modern Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "ModernEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Future Era Color
		tab.attachLabel("CGE6OPT3VBox", "FutureEraColorLabel", gc.getEraInfo(6).getDescription() + localText.getText("TXT_KEY_CGE_OPTSCR_ERA_COLOR", ()))	# Label
		szDropdownDesc = "Future Era Color"
		szCallbackFunction = "CGESetOptionColorDropdownInput"
		szOptionName = "FutureEraColor"
		Value = gc.getInfoTypeForString(CGEOptionControl.CGEOptionControl().getValue(szOptionName)) -2
		tab.attachDropDown("CGE6OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Dummy

		########## EXIT

		tab.attachHSeparator("CGE6VBox", "CGE6ExitSeparator")

		tab.attachHBox("CGE6VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions6Reset"
		szWidgetName = "CGE6OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE6OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGE7Tab(self):

		tab = self.pTabControl

		tab.attachVBox("CGE7Form", "CGE7VBox")
		tab.attachScrollPanel("CGE7VBox", "CGE7Panel")
		tab.setLayoutFlag("CGE7Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachVBox("CGE7Panel", "CGE7OPT0VBox")
		tab.setLayoutFlag("CGE7OPT0VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE7OPT0VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7OPT0VBox", "LAYOUT_SIZE_VEXPANDING")
		tab.attachLabel("CGE7OPT0VBox", "OPT7Label", "Unit Statistics MOD")

		tab.attachPanel("CGE7OPT0VBox", "CGE7OPT0Panel")
		tab.setStyle("CGE7OPT0Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGE7OPT0Panel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("CGE7OPT0Panel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("CGE7OPT0Panel", "CGE7OPTPanel")
		tab.setLayoutFlag("CGE7OPTPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7OPTPanel", "LAYOUT_SIZE_VEXPANDING")

		# Unit Statistics MOD
		tab.attachVBox("CGE7OPTPanel", "CGE7OPT1VBox")
		tab.setLayoutFlag("CGE7OPT1VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7OPT1VBox", "LAYOUT_SIZE_VEXPANDING")

		# Unit Statistics Checkbox
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_MODNAME_UNITSTATISTICS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEUnitStatistics"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Help
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_HELP", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowHelp"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Global High Score
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_GLOBAL_HIGH_SCORE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEGlobalHighScore"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track All Players
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_ALL_PLAYERS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackAllPlayers"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Turn Information
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_TURN_INFORMATION", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackTurnInformation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Unit High Score
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_UNIT_HIGH_SCORE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackUnitHighScore"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Unit Movement
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_UNIT_MOVEMENTS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackUnitMovement"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Non-Combat Units
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_NON_COMBAT_UNITS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackNonCombatUnits"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Goody Received
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_GOODY_RECEIVED", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackGoodyReceived"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Track Unit Promotions
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_TRACK_UNIT_PROMOTIONS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGETrackUnitPromotions"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT1VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Information
		tab.attachVSeparator("CGE7OPTPanel", "CGE7PanelHBoxSeparator1")

		tab.attachVBox("CGE7OPTPanel", "CGE7OPT2VBox")
		tab.setLayoutFlag("CGE7OPT2VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE7OPT2VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7OPT2VBox", "LAYOUT_SIZE_VEXPANDING")

#		tab.attachVBox("CGE7OPT2VBox", "CGE7OPT21VBox")
#		tab.setLayoutFlag("CGE7OPT21VBox", "LAYOUT_SPACING_INNERFORM")
#		tab.setLayoutFlag("CGE7OPT21VBox", "LAYOUT_SIZE_HEXPANDING")
#		tab.setLayoutFlag("CGE7OPT21VBox", "LAYOUT_SIZE_VEXPANDING")

		# Show All Players
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_ALL_PLAYERS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowAllPlayers"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Combat Count
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_COMBAT_COUNT", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowCombatCount"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Damage Information
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_DAMAGE_INFORMATION", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowDamageInformation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Unit Service Information
		tab.attachLabel("CGE7OPT2VBox", "ShowUnitServiceInformationLabel", localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_UNIT_SERVICE_INFORMATION", ()))	# Label
		szDropdownDesc = "ShowUnitServiceInformationDropdownBox"

		aszDropdownElements = ()
		for i in range(5):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_UNIT_SERVICE_INFORMATION_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEShowUnitServiceInformation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT2VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		#tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_TIP_CHANGE_CAUTION", ()))

		# Show Odds
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_ODDS", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowOdds"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Experience
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_EXPERIENCE", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowExperience"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Unit Event Log
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_UNIT_EVENT_LOG", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowUnitEventLog"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Log Turn Information
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_LOG_TURN_INFORMATION", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowLogTurnInformation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Log Date Information
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_LOG_DATE_INFORMATION", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowLogDateInformation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Show Log Turn Information First
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_SHOW_LOG_TURN_INFORMATION_FIRST", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEShowLogTurnInformationFirst"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT2VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		# Unit Naming
		tab.attachVSeparator("CGE7OPTPanel", "CGE7PanelHBoxSeparator2")

		tab.attachVBox("CGE7OPTPanel", "CGE7OPT3VBox")
		tab.setLayoutFlag("CGE7OPT3VBox", "LAYOUT_SPACING_INNERFORM")
		tab.setLayoutFlag("CGE7OPT3VBox", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGE7OPT3VBox", "LAYOUT_SIZE_VEXPANDING")

#		tab.attachVBox("CGE7OPT3VBox", "CGE7OPT31VBox")
#		tab.setLayoutFlag("CGE7OPT31VBox", "LAYOUT_SPACING_INNERFORM")
#		tab.setLayoutFlag("CGE7OPT31VBox", "LAYOUT_SIZE_HEXPANDING")
#		tab.setLayoutFlag("CGE7OPT31VBox", "LAYOUT_SIZE_VEXPANDING")

		# Unit Naming
		tab.attachLabel("CGE7OPT3VBox", "ShowUnitNamingLabel", localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAMING", ()))	# Label
		szDropdownDesc = "UnitNamingDropdownBox"

		aszDropdownElements = ()
		for i in range(4):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAMING_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEUnitNaming"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")
		tab.setToolTip(szOptionName, localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAMING_TOOL_TIP", ()))

		# Unit Name Recycling
		szOptionDesc = localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_RECYCLING", ())
		szCallbackFunction = "CGESetOptionCheckBoxInput"
		szOptionName = "CGEUnitNameRecycling"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachCheckBox("CGE7OPT3VBox", szOptionName, szOptionDesc, self.callbackIFace, szCallbackFunction, szOptionName, Value)

		tab.attachHSeparator("CGE7OPT3VBox", "CGE7OPT3VBoxSeparator1")
		tab.attachLabel("CGE7OPT3VBox", "CustomName3OptionLabel", localText.getText("TXT_KEY_CGE_OPTSCR_CUSTOM_NAME3_OPTION", ()))	# Label

		# Unit Name Number
		tab.attachLabel("CGE7OPT3VBox", "ShowUnitNameNumberLabel", localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_NUMBER", ()))	# Label
		szDropdownDesc = "UnitNameNumberDropdownBox"

		aszDropdownElements = ()
		for i in range(2):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_NUMBER_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEUnitNameNumber"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Unit Name Abreviation
		tab.attachLabel("CGE7OPT3VBox", "UnitNameAbreviationLabel", localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_ABREVIATION", ()))	# Label
		szDropdownDesc = "UnitNameAbreviationDropdownBox"

		aszDropdownElements = ()
		for i in range(2):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_ABREVIATION_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEUnitNameAbreviation"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Unit Name Spacing
		tab.attachLabel("CGE7OPT3VBox", "UnitNameSpacingLabel", localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAMESPACING", ()))	# Label
		szDropdownDesc = "UnitNameSpacingDropdownBox"

		aszDropdownElements = ()
		for i in range(2):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_SPACING_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEUnitNameSpacing"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Unit Name Desc
		tab.attachLabel("CGE7OPT3VBox", "UnitNameDescLabel", localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_DESC", ()))	# Label
		szDropdownDesc = "UnitNameDescDropdownBox"

		aszDropdownElements = ()
		for i in range(2):
			aszDropdownElements += (localText.getText("TXT_KEY_CGE_OPTSCR_UNIT_NAME_DESC_%d"%(i+1), ()),)

		szCallbackFunction = "CGESetOptionDropdownInput"
		szOptionName = "CGEUnitNameDesc"
		Value = CGEOptionControl.CGEOptionControl().getValue(szOptionName)
		tab.attachDropDown("CGE7OPT3VBox", szOptionName, szDropdownDesc, aszDropdownElements, self.callbackIFace, szCallbackFunction, szOptionName, Value)
		tab.setLayoutFlag(szOptionName, "LAYOUT_LEFT")

		# Dummy

		########## EXIT

		tab.attachHSeparator("CGE7VBox", "CGE7ExitSeparator")

		tab.attachHBox("CGE7VBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_OPTIONS_RESET", ())
		szCallbackFunction = "handleCGEOptions7Reset"
		szWidgetName = "CGE7OptionsResetButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGE7OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def drawCGEAboutTab(self):

		tab = self.pTabControl

		tab.attachVBox("CGEAboutForm", "CGEAboutVBox")
		tab.attachPanel("CGEAboutVBox", "CGEAbout0Panel")
		tab.setStyle("CGEAbout0Panel", "Panel_Tan15_Style")
		tab.setLayoutFlag("CGEAbout0Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGEAbout0Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachScrollPanel("CGEAbout0Panel", "CGEAbout1Panel")
		tab.setLayoutFlag("CGEAbout1Panel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("CGEAbout1Panel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachHBox("CGEAbout1Panel", "CGEAboutHBox")
		tab.setLayoutFlag("CGEAboutHBox", "LAYOUT_SIZE_HEXPANDING")

		tab.attachVBox("CGEAboutHBox", "CGEAboutV0Box")
		tab.setLayoutFlag("CGEAboutV0Box", "LAYOUT_SIZE_VEXPANDING")

		tab.attachLabel("CGEAboutV0Box", "CGEName", "Civ IV Gameplay Enhancements for BtS")	# Label
		tab.attachLabel("CGEAboutV0Box", "CGEVersion", "     Version: " + Version.CGEVersion)
		if (Version.CGETestVersion):
			for (i, szString) in enumerate(removeColor.sub("", localText.getText("TXT_KEY_CGE_TEST_VERSION_WARNING", ())).split('\n')):
				tab.attachLabel("CGEAboutV0Box", "CGEWarning" + str(i), szString)

		tab.attachLabel("CGEAboutV0Box", "CGESpace1", " ")
		tab.attachHSeparator("CGEAboutV0Box", "CGEAboutSeparator")
		tab.attachLabel("CGEAboutV0Box", "CGESpace2", " ")

		tab.attachLabel("CGEAboutV0Box", "CGEDebug1", "Civ IV Gameplay Enhancements Debug Infomation:")

		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
		if (config != None):
			CFG_Debug_CGE = config.getboolean("Civ IV Gameplay Enhancements", "Debug", False)
		if (CFG_Debug_CGE):
			tab.attachLabel("CGEAboutV0Box", "CGEDebug2", "     Civ IV Gameplay Enhancements Config.ini ... Found.")
			for (i, szString) in enumerate(self.splitCGEPath("     Path: " + config.getINIFileName())):
				tab.attachLabel("CGEAboutV0Box", "CGEDebug3_" + str(i), szString)
		else:
			tab.attachLabel("CGEAboutV0Box", "CGEDebug2", "     Civ IV Gameplay Enhancements Config.ini ... Not found.")

		tab.attachLabel("CGEAboutV0Box", "CGESpace3", " ")
		filenames = [os.path.join(os.path.dirname(dir), "Civ IV Gameplay Enhancements Config.ini") for dir in CvPath.assetsPath]
		filenames.reverse()
		tab.attachLabel("CGEAboutV0Box", "CGEDebug4", "Civ IV Gameplay Enhancements Config.ini Path List:")
		i = 1
		for file in filenames:
			for (j, szString) in enumerate(self.splitCGEPath("     Path %d: %s"%(i, file))):
				tab.attachLabel("CGEAboutV0Box", "CGEDebug" + str(4+i) + "_" + str(j), szString)
			i += 1

		tab.attachLabel("CGEAboutV0Box", "CGESpace4", " ")

		try:
			import cvGPArtPath
			szArtPath = cvGPArtPath.greatPersonArtPath
		except:
			szArtPath = CvPath.getPath("art\\GreatPeople", "Great Person.dds")
		tab.attachLabel("CGEAboutV0Box", "CGEDebug10", "Great Person Art Path:")
		for (i, szString) in enumerate(self.splitCGEPath("     " + szArtPath)):
			tab.attachLabel("CGEAboutV0Box", "CGEDebug11" + str(i), szString)

		tab.attachLabel("CGEAboutV0Box", "CGESpace5", " ")
		try:
			if (CyGlobalContext().isCGEBuild()):
				tab.attachLabel("CGEAboutV0Box", "CGEDebug12", "CvGameCore.DLL is Civ IV Gameplay Enhancements version")
		except:
			tab.attachLabel("CGEAboutV0Box", "CGEDebug12", "CvGameCoreDLL is Firaxis original version")

		########## EXIT

		tab.attachHSeparator("CGEAboutVBox", "CGEAboutExitSeparator")

		tab.attachHBox("CGEAboutVBox", "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")

		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleExitButtonInput"
		szWidgetName = "CGEAboutOptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def getCGEOptionEditBox(self, szBoxName):
		return self.getTabControl().getText(szBoxName)

	def splitCGEPath(self, szPath):
		szReturn = []
		szTemp = ""
		for szString in szPath.split("\\"):
			if (len(szTemp + szString) > 100):
				szReturn.append(szTemp + "\\")
				szTemp = "                " + szString
			else:
				if (szTemp != ""):
					szTemp += "\\"
				szTemp += szString
		szReturn.append(szTemp)

		return szReturn
