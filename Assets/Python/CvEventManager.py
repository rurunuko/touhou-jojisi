## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
##
## CvEventManager
## This class is passed an argsList from CvAppInterface.onEvent
## The argsList can contain anything from mouse location to key info
## The EVENTLIST that are being notified can be found


from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import CvGameUtils

# Civ IV Gameplay Enhancements
import CityInfoPanelPS
import CvConfigParser
import UnitPlacement

# Playability Utilities
import PlayerUtils
import CityUtils

#����MOD�p-FfH2���ڐA
import CustomFunctions

import UserPrefs
##### <written by F> #####
import TohoUnitList
import Functions
import SpellInfo

RangeList0 = [[0,0],]

RangeList1 = [	[-1,-1],[ 0,-1],[ 1,-1],
				[-1, 0],        [ 1, 0],
				[-1, 1],[ 0, 1],[ 1, 1], ]
##### </written by F> #####

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

bCityPlacementMode = False
bCityGrid = False

CFG_EnabledCitizensAutomated = True

# globals
###################################################
class CvEventManager:
	def __init__(self):
		global CFG_EnabledCitizensAutomated

		#################### ON EVENT MAP ######################
		#print "EVENTMANAGER INIT"

		self.bCtrl = False
		self.bShift = False
		self.bAlt = False
		self.bAllowCheats = False

		# OnEvent Enums
		self.EventLButtonDown=1
		self.EventLcButtonDblClick=2
		self.EventRButtonDown=3
		self.EventBack=4
		self.EventForward=5
		self.EventKeyDown=6
		self.EventKeyUp=7

		self.__LOG_MOVEMENT = 0
		self.__LOG_BUILDING = 0
		self.__LOG_COMBAT = 0
		self.__LOG_CONTACT = 0
		self.__LOG_IMPROVEMENT =0
		self.__LOG_CITYLOST = 0
		self.__LOG_CITYBUILDING = 0
		self.__LOG_TECH = 0
		self.__LOG_UNITBUILD = 0
		self.__LOG_UNITKILLED = 1
		self.__LOG_UNITLOST = 0
		self.__LOG_UNITPROMOTED = 0
		self.__LOG_UNITSELECTED = 0
		self.__LOG_UNITPILLAGE = 0
		self.__LOG_GOODYRECEIVED = 0
		self.__LOG_GREATPERSON = 0
		self.__LOG_RELIGION = 0
		self.__LOG_RELIGIONSPREAD = 0
		self.__LOG_GOLDENAGE = 0
		self.__LOG_ENDGOLDENAGE = 0
		self.__LOG_WARPEACE = 0
		self.__LOG_PUSH_MISSION = 0

		## EVENTLIST
		self.EventHandlerMap = {
			'mouseEvent'			: self.onMouseEvent,
			'kbdEvent' 				: self.onKbdEvent,
			'ModNetMessage'					: self.onModNetMessage,
			'Init'					: self.onInit,
			'Update'				: self.onUpdate,
			'UnInit'				: self.onUnInit,
			'OnSave'				: self.onSaveGame,
			'OnPreSave'				: self.onPreSave,
			'OnLoad'				: self.onLoadGame,
			'GameStart'				: self.onGameStart,
			'GameEnd'				: self.onGameEnd,
			'plotRevealed' 			: self.onPlotRevealed,
			'plotFeatureRemoved' 	: self.onPlotFeatureRemoved,
			'plotPicked'			: self.onPlotPicked,
			'nukeExplosion'			: self.onNukeExplosion,
			'gotoPlotSet'			: self.onGotoPlotSet,
			'BeginGameTurn'			: self.onBeginGameTurn,
			'EndGameTurn'			: self.onEndGameTurn,
			'BeginPlayerTurn'		: self.onBeginPlayerTurn,
			'EndPlayerTurn'			: self.onEndPlayerTurn,
			'endTurnReady'			: self.onEndTurnReady,
			'combatResult' 			: self.onCombatResult,
		  'combatLogCalc'	 		: self.onCombatLogCalc,
		  'combatLogHit'				: self.onCombatLogHit,
			'improvementBuilt' 		: self.onImprovementBuilt,
			'improvementDestroyed' 		: self.onImprovementDestroyed,
			'routeBuilt' 		: self.onRouteBuilt,
			'firstContact' 			: self.onFirstContact,
			'cityBuilt' 			: self.onCityBuilt,
			'cityRazed'				: self.onCityRazed,
			'cityAcquired' 			: self.onCityAcquired,
			'cityAcquiredAndKept' 	: self.onCityAcquiredAndKept,
			'cityLost'				: self.onCityLost,
			'cultureExpansion' 		: self.onCultureExpansion,
			'cityGrowth' 			: self.onCityGrowth,
			'cityDoTurn' 			: self.onCityDoTurn,
			'cityBuildingUnit'	: self.onCityBuildingUnit,
			'cityBuildingBuilding'	: self.onCityBuildingBuilding,
			'cityRename'				: self.onCityRename,
			'cityHurry'				: self.onCityHurry,
			'selectionGroupPushMission'		: self.onSelectionGroupPushMission,
			'unitMove' 				: self.onUnitMove,
			'unitSetXY' 			: self.onUnitSetXY,
			'unitCreated' 			: self.onUnitCreated,
			'unitBuilt' 			: self.onUnitBuilt,
			'unitKilled'			: self.onUnitKilled,
			'unitLost'				: self.onUnitLost,
			'unitPromoted'			: self.onUnitPromoted,
			'unitSelected'			: self.onUnitSelected,
			'UnitRename'				: self.onUnitRename,
			'unitPillage'				: self.onUnitPillage,
			'unitSpreadReligionAttempt'	: self.onUnitSpreadReligionAttempt,
			'unitGifted'				: self.onUnitGifted,
			'unitBuildImprovement'				: self.onUnitBuildImprovement,
			'goodyReceived'        	: self.onGoodyReceived,
			'greatPersonBorn'      	: self.onGreatPersonBorn,
			'buildingBuilt' 		: self.onBuildingBuilt,
			'projectBuilt' 			: self.onProjectBuilt,
			'techAcquired'			: self.onTechAcquired,
			'techSelected'			: self.onTechSelected,
			'religionFounded'		: self.onReligionFounded,
			'religionSpread'		: self.onReligionSpread,
			'religionRemove'		: self.onReligionRemove,
			'corporationFounded'	: self.onCorporationFounded,
			'corporationSpread'		: self.onCorporationSpread,
			'corporationRemove'		: self.onCorporationRemove,
			'goldenAge'				: self.onGoldenAge,
			'endGoldenAge'			: self.onEndGoldenAge,
			'chat' 					: self.onChat,
			'victory'				: self.onVictory,
			'vassalState'			: self.onVassalState,
			'changeWar'				: self.onChangeWar,
			'setPlayerAlive'		: self.onSetPlayerAlive,
			'playerChangeStateReligion'		: self.onPlayerChangeStateReligion,
			'playerGoldTrade'		: self.onPlayerGoldTrade,
			#����MOD�ǋL����
			'delayedDeath' 			: self.onDelayedDeath,
			# BULL events
			'playerRevolution'		: self.onPlayerRevolution,
			'combatWithdrawal'		: self.onCombatWithdrawal,
			'combatRetreat'			: self.onCombatRetreat,
			'combatLogCollateral'	: self.onCombatLogCollateral,
			'combatLogFlanking'		: self.onCombatLogFlanking,
			#����MOD�ǋL���������܂�
			'windowActivation'		: self.onWindowActivation,
			'gameUpdate'			: self.onGameUpdate,		# sample generic event
		}

		################## Events List ###############################
		#
		# Dictionary of Events, indexed by EventID (also used at popup context id)
		#   entries have name, beginFunction, applyFunction [, randomization weight...]
		#
		# Normal events first, random events after
		#
		################## Events List ###############################
		self.Events={
			CvUtil.EventEditCityName : ('EditCityName', self.__eventEditCityNameApply, self.__eventEditCityNameBegin),
			CvUtil.EventEditCity : ('EditCity', self.__eventEditCityApply, self.__eventEditCityBegin),
			CvUtil.EventPlaceObject : ('PlaceObject', self.__eventPlaceObjectApply, self.__eventPlaceObjectBegin),
			CvUtil.EventAwardTechsAndGold: ('AwardTechsAndGold', self.__eventAwardTechsAndGoldApply, self.__eventAwardTechsAndGoldBegin),
			CvUtil.EventEditUnitName : ('EditUnitName', self.__eventEditUnitNameApply, self.__eventEditUnitNameBegin),
			CvUtil.EventWBAllPlotsPopup : ('WBAllPlotsPopup', self.__eventWBAllPlotsPopupApply, self.__eventWBAllPlotsPopupBegin),
			CvUtil.EventWBLandmarkPopup : ('WBLandmarkPopup', self.__eventWBLandmarkPopupApply, self.__eventWBLandmarkPopupBegin),
			CvUtil.EventWBScriptPopup : ('WBScriptPopup', self.__eventWBScriptPopupApply, self.__eventWBScriptPopupBegin),
			CvUtil.EventWBStartYearPopup : ('WBStartYearPopup', self.__eventWBStartYearPopupApply, self.__eventWBStartYearPopupBegin),
			CvUtil.EventShowWonder: ('ShowWonder', self.__eventShowWonderApply, self.__eventShowWonderBegin),
			CvUtil.EventSignPopup : ('SignPopup', self.__eventUnitPlacementAddSignEventPopupApply, self.__eventUnitPlacementAddSignEventPopupBegin),
			CvUtil.EventSitePopup : ('SitePopup', self.__eventPlayUtilsAddSiteEventPopupApply, self.__eventPlayUtilsAddSiteEventPopupBegin),
		}

		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
		if (config != None):
			CFG_EnabledCitizensAutomated = config.getboolean( "Citizens Automated", "Enabled", True)

		# �n��a�����z���p
		self.ChireidenOverflow = (-1, 0)
		# UB�ύX����
		self.oldCivBuildings = []

#################### EVENT STARTERS ######################
	def handleEvent(self, argsList):
		'EventMgr entry point'
		# extract the last 6 args in the list, the first arg has already been consumed
		self.origArgsList = argsList	# point to original
		tag = argsList[0]				# event type string
		idx = len(argsList)-6
		bDummy = false
		self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
		ret = 0
		if self.EventHandlerMap.has_key(tag):
			fxn = self.EventHandlerMap[tag]
			ret = fxn(argsList[1:idx])
		return ret

#################### EVENT APPLY ######################
	def beginEvent( self, context, argsList=-1 ):
		'Begin Event'
		entry = self.Events[context]
		return entry[2]( argsList )

	def applyEvent( self, argsList ):
		'Apply the effects of an event '
		context, playerID, netUserData, popupReturn = argsList

		if context == CvUtil.PopupTypeEffectViewer:
			return CvDebugTools.g_CvDebugTools.applyEffectViewer( playerID, netUserData, popupReturn )

		entry = self.Events[context]

		if ( context not in CvUtil.SilentEvents ):
			self.reportEvent(entry, context, (playerID, netUserData, popupReturn) )
		return entry[1]( playerID, netUserData, popupReturn )   # the apply function

	def reportEvent(self, entry, context, argsList):
		'Report an Event to Events.log '
		if (gc.getGame().getActivePlayer() != -1):
			message = "DEBUG Event: %s (%s)" %(entry[0], gc.getActivePlayer().getName())
			CyInterface().addImmediateMessage(message,"")
			CvUtil.pyPrint(message)
		return 0

#################### ON EVENTS ######################
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'

		eventType,key,mx,my,px,py = argsList
		game = gc.getGame()

		if (self.bAllowCheats):
			# notify debug tools of input to allow it to override the control
			argsList = (eventType,key,self.bCtrl,self.bShift,self.bAlt,mx,my,px,py,gc.getGame().isNetworkMultiPlayer())
			if ( CvDebugTools.g_CvDebugTools.notifyInput(argsList) ):
				return 0

		if ( eventType == self.EventKeyDown ):
			theKey=int(key)

			CvCameraControls.g_CameraControls.handleInput( theKey )

			global bCityGrid
			global bCityPlacementMode
			# Ctrl+K (City Grid)
			if (theKey == int(InputTypes.KB_K) and self.bCtrl):
				pPlayer = gc.getActivePlayer()
				message = "Handling ctrl-k"
				if (PlayerUtils.getGameOption(pPlayer, "CityGrid") < 1):
					PlayerUtils.setGameOption(pPlayer, "CityGrid", 1)
					bCityGrid = True
					PlayerUtils.colorizeCityPlots(pPlayer)
					gc.setDefineINT("USE_ON_UPDATE_CALLBACK", 1)
				else:
					PlayerUtils.setGameOption(pPlayer, "CityGrid", 0)
					bCityGrid = False
					CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
					if (not bCityPlacementMode):
						gc.setDefineINT("USE_ON_UPDATE_CALLBACK", 0)
				return 1

			# Ctrl+Shift+P (City Placement Mode)
			if (theKey == int(InputTypes.KB_P) and self.bCtrl):
				pPlot = CyInterface().getMouseOverPlot()
				if (self.bShift):
					bCityPlacementMode = not bCityPlacementMode
					if (bCityPlacementMode):
						message = localText.getText('TXT_KEY_CITY_PLACEMENT_MODE_ON', ())
						gc.setDefineINT("USE_ON_UPDATE_CALLBACK", 1)
						CityUtils.InitExistCityGrid()
					else:
						if (not bCityGrid):
							gc.setDefineINT("USE_ON_UPDATE_CALLBACK", 0)
						CityInfoPanelPS.CityInfoPanelPS().hideInfoPane()
						message = localText.getText('TXT_KEY_CITY_PLACEMENT_MODE_OFF', ())
						CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
					CyInterface().addMessage(gc.getActivePlayer().getID(),True,len(message),message,'',0,'',ColorTypes(8),pPlot.getX(),pPlot.getY(),False,False)
				else:
					pPlayer = gc.getActivePlayer()
					if (bCityPlacementMode):
						if(pPlot.isPeak() or pPlot.isWater() or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DUSTSEA") or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_CRATERRIM") or not pPlot.isRevealed(pPlayer.getTeam(), False)):
							pass
						else:
							bErase = False
							for iSign in xrange(CyEngine().getNumSigns()):
								pSign = CyEngine().getSignByIndex(iSign)
								pSignPlot = pSign.getPlot()
								if (pSignPlot.at(pPlot.getX(), pPlot.getY()) and pSign.getPlayerType() == pPlayer.getID()):
									bErase = True
									PlayerUtils.removeSiteFromList(pPlayer, pPlot)
									CyEngine().removeSign(pSignPlot, pPlayer.getID())
									break
							if (not bErase):
								self.__eventPlayUtilsAddSiteEventPopupBegin((pPlot.getX(), pPlot.getY(), pPlayer.getID()))

				return 1

			# Shift+Alt+P (Unit Placement Add Sign)
			if(theKey == int(InputTypes.KB_P) and self.bShift and self.bAlt):
				pPlayer = gc.getActivePlayer()
				pPlot = CyInterface().getMouseOverPlot()
				bErase = False
				for iSign in range(CyEngine().getNumSigns()):
					pSign = CyEngine().getSignByIndex(iSign)
					pSignPlot = pSign.getPlot()
					if (pSignPlot.at(pPlot.getX(), pPlot.getY()) and pSign.getPlayerType() == pPlayer.getID()):
						bErase = True
						UnitPlacement.UnitPlacement().deleteSignDict(pPlot.getX(), pPlot.getY())
						CyEngine().removeSign(pSignPlot, pPlayer.getID())
						break
				if (not bErase):
					if (pPlot.isRevealed(pPlayer.getTeam(), False)):
						self.__eventUnitPlacementAddSignEventPopupBegin((pPlot.getX(), pPlot.getY(), pPlayer.getID()))

				return 1

			if (self.bAllowCheats):
				# Shift - T (Debug - No MP)
				if (theKey == int(InputTypes.KB_T)):
					if ( self.bShift ):
						self.beginEvent(CvUtil.EventAwardTechsAndGold)
						#self.beginEvent(CvUtil.EventCameraControlPopup)
						return 1

				elif (theKey == int(InputTypes.KB_W)):
					if ( self.bShift and self.bCtrl):
						self.beginEvent(CvUtil.EventShowWonder)
						return 1

				# Shift - ] (Debug - currently mouse-overd unit, health += 10
				elif (theKey == int(InputTypes.KB_LBRACKET) and self.bShift ):
					unit = CyMap().plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = min( unit.maxHitPoints()-1, unit.getDamage() + 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				# Shift - [ (Debug - currently mouse-overd unit, health -= 10
				elif (theKey == int(InputTypes.KB_RBRACKET) and self.bShift ):
					unit = CyMap().plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = max( 0, unit.getDamage() - 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				elif (theKey == int(InputTypes.KB_F1)):
					if ( self.bShift ):
						CvScreensInterface.replayScreen.showScreen(False)
						return 1
					# don't return 1 unless you want the input consumed

				elif (theKey == int(InputTypes.KB_F2)):
					if ( self.bShift ):
						import CvDebugInfoScreen
						CvScreensInterface.showDebugInfoScreen()
						return 1

				elif (theKey == int(InputTypes.KB_F3)):
					if ( self.bShift ):
						CvScreensInterface.showDanQuayleScreen(())
						return 1

				elif (theKey == int(InputTypes.KB_F4)):
					if ( self.bShift ):
						CvScreensInterface.showUnVictoryScreen(())
						return 1

		return 0

	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'

		iData1, iData2, iData3, iData4, iData5 = argsList

		print("Modder's net message!")

		CvUtil.pyPrint( 'onModNetMessage' )

	def onInit(self, argsList):
		'Called when Civ starts up'
		CvUtil.pyPrint( 'OnInit' )

	def onUpdate(self, argsList):
		'Called every frame'
		fDeltaTime = argsList[0]

		# allow camera to be updated
		CvCameraControls.g_CameraControls.onUpdate( fDeltaTime )

		pPlayer = gc.getActivePlayer()

		global bCityGrid
		global bCityPlacementMode

		if (bCityGrid):
			if (not CyInterface().isCityScreenUp()):
				PlayerUtils.colorizeCityPlots(pPlayer)
			else:
				bCityGrid = False

		if (bCityPlacementMode):
			if (not CyInterface().isCityScreenUp()):
				PlayerUtils.colorizeCityPlots(pPlayer)
				PlayerUtils.colorizeCitySites(pPlayer)
				pPlot = CyInterface().getMouseOverPlot()
				CityUtils.colorizeCityGridForPlot(pPlot, pPlayer)
				CityInfoPanelPS.CityInfoPanelPS().showCityRadiusInfo(pPlot)
			else:
				CityInfoPanelPS.CityInfoPanelPS().hideInfoPane()
				bCityPlacementMode = False

		if (not bCityGrid and not bCityPlacementMode):
			PlayerUtils.setGameOption(pPlayer, "CityGrid", 0)
			CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
			gc.setDefineINT("USE_ON_UPDATE_CALLBACK", 0)

	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]

	def onUnInit(self, argsList):
		'Called when Civ shuts down'
		CvUtil.pyPrint('OnUnInit')

	def onPreSave(self, argsList):
		"called before a game is actually saved"
		CvUtil.pyPrint('OnPreSave')

	def onSaveGame(self, argsList):
		"return the string to be saved - Must be a string"
		return ""

	def setTraitUB(self):
		iNumPlayer = 19     # 19�ł����̂��ق�Ƃ�

		TraitBuildingclassBuildingList = [
			['TRAIT_BENBENLIST', 'BUILDINGCLASS_OBELISK', 'BUILDING_KISHINJOU_ETHIOPIAN_STELE'],
		]

		# ���ǂ�
		for it in self.oldCivBuildings:
			iCiv, ibC, idB = it
			pCiv = gc.getCivilizationInfo(iCiv)
			pCiv.setCivilizationBuildings(ibC, idB)

		for it in TraitBuildingclassBuildingList:
			trait, bclass, build = it
			found = False
			for i in range(iNumPlayer):
				pPlayer = gc.getPlayer(i)
				pCiv = gc.getCivilizationInfo( pPlayer.getCivilizationType() )
				ibC = gc.getInfoTypeForString(bclass)
				#���̎u���������
				if pPlayer.hasTrait(gc.getInfoTypeForString(trait)):
					iB = gc.getInfoTypeForString(build)
					# ���ڂ���
					self.oldCivBuildings.append( [pPlayer.getCivilizationType(), ibC, pCiv.getCivilizationBuildings(ibC)] )
					# ������
					pCiv.setCivilizationBuildings(ibC, iB)
				
		
	def onLoadGame(self, argsList):
		self.setTraitUB()
		return 0

	def onGameStart(self, argsList):
		'Called at the start of the game'

		# before Starting Popup Widget
		self.setTraitUB()
		
		if (gc.getGame().getGameTurnYear() == gc.getDefineINT("START_YEAR") and not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showDawnOfMan")
					popupInfo.addPopup(iPlayer)
		else:
			CyInterface().setSoundSelectionReady(true)

		if gc.getGame().isPbem():
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(true)
					popupInfo.addPopup(iPlayer)
																	
		
		##### <written by F> #####
		#�Q�[���J�n���̏���
		
		#�S�����̐��E���@�񐔂��P�ɃZ�b�g
		iNumPlayer = 19#gc.getGame().countCivPlayersAlive() + gc.getGame().countCivPlayersEverAlive()
		for i in range(iNumPlayer):
			ppPlayer = gc.getPlayer(i)
			ppPlayer.setNumWorldSpell(1)
		
			#�������j�b�g���Ə�����Z�b�g
			ppPlayer.setNumTohoUnitLimit(1)
			ppPlayer.setNumTohoUnit(0)
			
			#�~�X�e���E���̃t���O�����Z�b�g
			ppPlayer.setMysteryiumFlag(0)
			
			#AI�̓������[�g���Z�b�g
			iRandNum = gc.getGame().getSorenRandNum(100,"AI PROMOTION ROUTE")
			if iRandNum < 15:
				ppPlayer.setAIPromotionRoute(1)
			elif iRandNum < 30:
				ppPlayer.setAIPromotionRoute(2)
			elif iRandNum < 45:
				ppPlayer.setAIPromotionRoute(3)
			else:
				ppPlayer.setAIPromotionRoute(0)
			
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_SPELL_ONLY_AI')):
				ppPlayer.setAIPromotionRoute(3)
			
			#���̈��|�C���g�̃��Z�b�g
			ppPlayer.setNumMyLove(0)
			ppPlayer.setNumMadeMyLove(0)
			
			#���o���[�h���̃{�[�i�X
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')):# and ppPlayer.isHuman():
				GameSpeedList = [200,150,100,67,50]
				iGold = 30 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
				ppPlayer.changeGold(iGold)
				
				#�{�[�i�X�e�N�m���W�[�Ƃ��ČŗL�e�N�̂P�i�K�ڂ�^����
				iCiv = ppPlayer.getCivilizationType()
				pTeam = gc.getTeam(ppPlayer.getTeam())
				#�g���ق̂Ƃ�
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_ENGLAND'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_GOKUSAINODANMAKU'),True,i,True,True)
				
				#���ʘO
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_NEKOMATA'),True,i,True,True)
				
				#�X���A��
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_KURAYAMI'),True,i,True,True)
				
				#�i����
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_SUZURANNODOKU'),True,i,True,True)
				
				#�d���̎R
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_KAPPANOHATUMEI'),True,i,True,True)
				
				#����_��
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_MAHOU'),True,i,True,True)
				
				#�n��a
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_HASHIHIME'),True,i,True,True)
				
				#�l�Ԃ̗�
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
					iGold = 20 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
					ppPlayer.changeGold(iGold)
					
				#���@�D
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_TINY_CLEVER_COMMANDER'),True,i,True,True)
				
				#�_��_
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_TYOKUREI'),True,i,True,True)
				
				#�P�j��
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_JAKUSYANORAKUEN'),True,i,True,True)
				
				#���̓s
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
					pTeam.setHasTech(gc.getInfoTypeForString('TECH_MOON_WAR_FIRST'),True,i,True,True)
			
			##### </written by F> #####
			
		
		
	def onGameEnd(self, argsList):
		'Called at the End of the game'
		print("Game is ending")
		return

	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		
		##### <written by F> #####
		#�Q�[���^�[�����̏���
		
		#�������C������΂�����Ƃ��n�����i�H�j
		iMapWidth = gc.getMap().getGridWidth()
		iMapHeight = gc.getMap().getGridHeight()
		for iX in range(iMapWidth):
			for iY in range(iMapHeight):
				pPlot = gc.getMap().plot(iX,iY)
				if pPlot.getNumCirnoFreeze() > 0: #�����Ă���
					pPlot.setNumCirnoFreeze( pPlot.getNumCirnoFreeze()-1 )
					if pPlot.getNumCirnoFreeze() <= 0: #�n����������
						if pPlot.getNumUnits() == 0:
							pPlot.setTerrainType( pPlot.getOriginalTerrain(),True,True )
							pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_NONE'),1)
							pPlot.setBonusType( pPlot.getOriginalBounu() )
						else:
							pPlot.setNumCirnoFreeze(1)
							
				#�Q�̃^�[���o��
				if pPlot.getNumVortexTrun() > 0:
					pPlot.setNumVortexTrun( pPlot.getNumVortexTrun() - 1 )
					if pPlot.getNumVortexTrun() <= 0:
						pPlot.setFeatureType(-1,1)
		
		##### </written by F> #####
		
		#����MOD�ǋL����
		#BC1000�N���a�I�v�V�������A����^�[���Ń|�b�v�A�b�v�\��
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_PEACE_OF_BC1000')):
			iGameTarn = gc.getGame().getGameTurn()
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				if iGameTarn == 249:
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_PEACE_OF_BC1000",()),'')
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				if iGameTarn == 119:
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_PEACE_OF_BC1000",()),'')
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				if iGameTarn == 74:
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_PEACE_OF_BC1000",()),'')
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				if iGameTarn == 49:
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_PEACE_OF_BC1000",()),'')
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				if iGameTarn == 42:
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_PEACE_OF_BC1000",()),'')
		
		#����MOD�ǋL���������܂�
		
		CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]

#����MOD�ǋL����
	def BPTprocessTohoUnit(self, pUnit, argsList):
		iGameTurn, iPlayer = argsList
		#�������j�b�g�܂��̊Ǘ��E����
		#�ꕔ�̃L�����N�^�[�X�L���֘A��������
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		
		#��������m���ɓ������j�b�g�ł��邱�Ƃ��O��̏���
		#�������j�b�g�ł����Power��
		Gain = 0.015
		GainPer = 100
		for item in TohoUnitList.PowerGainPromotionList:
			if pUnit.isHasPromotion(gc.getInfoTypeForString(item[0])):
				Gain = Gain + item[1]
		for item in TohoUnitList.PowerGainPerPromotionList:
			if pUnit.isHasPromotion(gc.getInfoTypeForString(item[0])):
				GainPer = GainPer + item[1]
			
		Gain = Gain * GainPer / 100
			
		#����␳
		GainPer = 100
		for item in TohoUnitList.PowerGainPerEraList:
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString(item[0]):
				GainPer = GainPer + item[1]
			Gain = Gain * GainPer / 100
				
		#�Q�[���X�s�[�h�␳
		GainPer = 100
		for item in TohoUnitList.PowerGainPerGameSpeedList:
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString(item[0]):
				GainPer = item[1]
		Gain = Gain * GainPer / 100
				
		#AI�������[�h�ɂ��␳
		if gc.getPlayer(pUnit.getOwner()).isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
			Gain = Gain*2
		#���o���[�h�ɂ��␳
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(pUnit.getOwner()).isHuman():
			Gain = Gain*2
				
		pUnit.setPower(pUnit.getPower()+Gain)
		#pUnit.setPower(4)
		#���ӂꕪ��SDK���ŏ���
				
		#�������j�b�g�ł���΁A���m���Ōo���l���P�l��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'))==False:
			PerExperience = pUnit.countExpByTrun()
			while PerExperience > 0:
				if gc.getGame().getSorenRandNum(100, "Toho Unit gets Experience Percent") < PerExperience:
					pUnit.changeExperience(1,-1,false,false,false)
				PerExperience -= 100
		
		#���g������10���̃_���[�W���󂯂�
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN')):
			pUnit.changeDamage(10,iPlayer)
		
		#SpecialNumber�̏���
		#����񂾂����烊�Z�b�g
		if ( (gc.getInfoTypeForString('UNIT_RIN0') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_RIN6')) or
			(gc.getInfoTypeForString('UNIT_RIN_CATMODE0') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_RIN_CATMODE6')) ):
			pUnit.setSpecialNumber(0)
		#��ւ������烊�Z�b�g
		if  gc.getInfoTypeForString('UNIT_ICHIRIN0') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_ICHIRIN6'):
			pUnit.setSpecialNumber(0)
			
		#�����������烊�Z�b�g
		if  gc.getInfoTypeForString('UNIT_SEIRAN0') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_SEIRAN6'):
			pUnit.setSpecialNumber(0)
				
		#�X�y���̃u���[�N�^�C�������炷
		if pUnit.getNumSpellCardBreakTime > 0:
			pUnit.setNumSpellCardBreakTime(pUnit.getNumSpellCardBreakTime()-1)
		if pUnit.getNumSpellExtraBreakTime > 0:
			pUnit.setNumSpellExtraBreakTime(pUnit.getNumSpellExtraBreakTime()-1)
		if pUnit.getNumSpellPhantasmBreakTime > 0:
			pUnit.setNumSpellPhantasmBreakTime(pUnit.getNumSpellPhantasmBreakTime()-1)
				
		#�ЃX�L���ɂ�邨���Q�b�g
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SYOU_SKILL1')):
			iNumGold = gc.getGame().getSorenRandNum( pUnit.baseCombatStr()*5,"tora skill")
			if (pPlayer.getGold() > iNumGold):
				if gc.getGame().getSorenRandNum( 100,"tora skill") < 2:
					iNumGold = -iNumGold
			pPlayer.changeGold(iNumGold)
				
		#���e�B�X�L���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LETTY_SKILL1')):
			pPlot = pUnit.plot()
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_OASIS') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
				if pUnit.getDamage() == 0:
					pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
					pUnit.changeDamage(40,pUnit.getOwner())
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
				pUnit.changeDamage(-40,pUnit.getOwner())
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
				pUnit.changeDamage(-80,pUnit.getOwner())
		
		#���ގq�̃X�L��������΁A���͂̃��j�b�g���Q�Ԃ�
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KANAKO_SKILL1')) and pUnit.getUnitType() != gc.getInfoTypeForString('UNIT_KANAKO0'):
			pTeam = gc.getTeam(pUnit.getTeam())
			for iX in range(pUnit.getX()-1,pUnit.getX()+2):
				for iY in range(pUnit.getY()-1,pUnit.getY()+2):
					if Functions.isPlot(iX,iY):
						pPlot = gc.getMap().plot(iX,iY)
						for i in range(pPlot.getNumUnits()):
							if pTeam.isAtWar(pPlot.getUnit(i).getTeam()):
								if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
									if gc.getGame().getSorenRandNum(100, "kanako skill") < 5:
										RevivalUnit = pPlot.getUnit(i).getUnitType()
										plotX = pUnit.getX()
										plotY = pUnit.getY()
										iExperience = pPlot.getUnit(i).getExperience()
										iLevel = pPlot.getUnit(i).getLevel()
										newUnit1 = gc.getPlayer(pUnit.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										
										newUnit1.changeExperience(iExperience,-1,false,false,false)
										newUnit1.changeLevel(iLevel-1)
										
										#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
										PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
										PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
										PromotionNum = PromotionEnd - PromotionStart
										
										for iPromotion in range(PromotionNum):
											if pPlot.getUnit(i).isHasPromotion(iPromotion):
												newUnit1.setHasPromotion(iPromotion,True)
										newUnit1.finishMoves()
										pPlot.getUnit(i).changeDamage(100,iPlayer)
				
		#�Ă�̃X�L��������΁A���X�^�b�N�̃��j�b�g�ɂ���������d�|����B�����͊܂܂�Ȃ��B
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TEWI_SKILL1')):
			pPlot = pUnit.plot()
			for i in range(pPlot.getNumUnits()):
				if pUnit.getUnitType() != pPlot.getUnit(i).getUnitType():
					if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
						if gc.getGame().getSorenRandNum(100, "ITAZURA of TEWI") < 10:
							pPlot.getUnit(i).changeExperience(1,-1,False,False,False)
							pUnit.changeExperience(1,-1,False,False,False)
					else:
						if gc.getGame().getSorenRandNum(100, "ITAZURA of TEWI") < 30:  
							pPlot.getUnit(i).changeExperience(1,-1,False,False,False)
		
		#���[���̃X�L��������Γ��X�^�b�N����30��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EIRIN_SKILL1')):
			pPlot = pUnit.plot()
			iNumUnit = pPlot.getNumUnits()
			for i in range(iNumUnit):
				pPlot.getUnit(i).changeDamage(-30,iPlayer)
		
		#���f�B�̃X�L��������Γ��X�^�b�N���񕜂T��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MEDICIN_SKILL1')):
			pPlot = pUnit.plot()
			iNumUnit = pPlot.getNumUnits()
			for i in range(iNumUnit):
				pPlot.getUnit(i).changeDamage(-5,iPlayer)
		
		#�A���X�̃X�L��������΁A15���̊m���ŏ�C���� ���i��������x�󂯌p��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ALICE_SKILL1')) and pUnit.getUnitType() != gc.getInfoTypeForString('UNIT_ALICE0'):
			iSummonNum = 20# gc.getGame().getSorenRandNum(20, "summon SHANGHAI")
			#�Q�[�����x�ɂ��ω�
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				iSummonNum = iSummonNum * 50 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				iSummonNum = iSummonNum * 75 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				iSummonNum = iSummonNum * 150 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				iSummonNum = iSummonNum * 200 / 100
			if gc.getGame().getSorenRandNum(100, "summon SHANGHAI") < iSummonNum:
				iPlayer = pUnit.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iX = pUnit.getX()
				iY = pUnit.getY()
				if gc.getGame().getSorenRandNum(100,"Alice Skill") < 50:
					iNumNewUnit = pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_ALICE1') + gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')
				else:
					iNumNewUnit = pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_ALICE1') + gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')
				
				newUnit = pPlayer.initUnit(iNumNewUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT1')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT2')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT2'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT3')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT3'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT4')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT4'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT5')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT5'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT6')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT6'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL1')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL2')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL2'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL3')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL3'),True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL4')):
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL4'),True)
		
		#����MOD�ǋL����
		
		#����񂲂̃X�L��������Γ��X�^�b�N����15��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RINGO_SKILL1')):
			pPlot = pUnit.plot()
			iNumUnit = pPlot.getNumUnits()
			for i in range(iNumUnit):
				pPlot.getUnit(i).changeDamage(-30,iPlayer)
		
		#���Ƃ��Ƃ�i�R�s�[���j�̕ϐg����
		#�I���W�i�����瑽��������ς���
		
		if pUnit.getNumTransformTime() > 0:
			#���������ϐg���Ȃ�A�ϐg���Ԃ��؂ꂽ�猳�ɖ߂�
			if gc.getInfoTypeForString("UNIT_SUIKA_BIG1") <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA_BIG6"):
				pUnit.setNumTransformTime( pUnit.getNumTransformTime() - 1 )
				if pUnit.getNumTransformTime() <= 0:
					iDamage = pUnit.getDamage()
					TransformUnit = pUnit.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA_BIG1") + gc.getInfoTypeForString("UNIT_SUIKA1")
					newUnit1 = pPlayer.initUnit(TransformUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit1.convert(pUnit)
					#newUnit1.changeDamage(iDamage,pUnit.getOwner())
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),False )
		
		#����MOD�ǋL����
		#�����d���̎R�̕ϐg�I������
			if gc.getInfoTypeForString("UNIT_SUIKA_BIG1_YOUKAI") <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA_BIG6_YOUKAI"):
				pUnit.setNumTransformTime( pUnit.getNumTransformTime() - 1 )
				if pUnit.getNumTransformTime() <= 0:
					iDamage = pUnit.getDamage()
					TransformUnit = pUnit.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA_BIG1_YOUKAI") + gc.getInfoTypeForString("UNIT_SUIKA1_YOUKAI")
					newUnit1 = pPlayer.initUnit(TransformUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit1.convert(pUnit)
					#newUnit1.changeDamage(iDamage,pUnit.getOwner())
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),False )
					newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),False )
		#����MOD�ǋL���������܂�
		
		#���Ƃ�̕ϐg�^�C�����؂ꂽ�ꍇ�͏��i�����������Ȃ�
			if gc.getInfoTypeForString("UNIT_SATORI1") <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString("UNIT_SATORI6"):
				pUnit.setNumTransformTime( pUnit.getNumTransformTime() - 1 )
				if pUnit.getNumTransformTime() <= 0:
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),False )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),False )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),False )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),False )
			
		#�X�����E�̃J�E���g������������
		#�����������E����MOD�ǋL
		#���E�����I�v�V����False�̎��̂ݔ���
		#�X�ɒǋL�F���܂��ɓ������AI���s�����������ꂽ���̂ŏ��Ԃ�����ւ���
		
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_OUKA')) == False:
				if pUnit.getSinraDelayTurn() > 0:
					if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZIKI')):
						pUnit.setSinraDelayTurn( pUnit.getSinraDelayTurn() - ( 10 + pUnit.countCardAttackLevel() )*2)
					else:
						pUnit.setSinraDelayTurn(pUnit.getSinraDelayTurn() - 10 - pUnit.countCardAttackLevel())
				else:
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_OUKAKEKKAI'),True)
		
			#AI�̂Ƃ�
			if pPlayer.isHuman() == False:
				#�������[�g���I�����ꂢ�Ȃ���΁A�đI��
				if pUnit.getAIPromotionRoute()<1 or pUnit.getAIPromotionRoute()>3:
					if pPlayer.getAIPromotionRoute() > 0:
						pUnit.setAIPromotionRoute(pPlayer.getAIPromotionRoute())
					else:
						pUnit.setAIPromotionRoute( gc.getGame().getSorenRandNum(3,'PromotionRoute') + 1  )
				#�R���o�b�g���[�g�͂��傢�Ɠ���Ȃ̂ŁA�A�����ĂQ�񔻒������
				PromoList = TohoUnitList.getAIPromotionList[pUnit.getAIPromotionRoute()-1] + TohoUnitList.getAIPromotionList[pUnit.getAIPromotionRoute()-1]
				for sPromotion in PromoList:
					iExperience = pUnit.getExperience()
					iLevel = pUnit.getLevel()
					PromotionFlag = False
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CHARISMATIC')):
						if iExperience >= (iLevel*iLevel+1 + 1) *3 /4:
							PromotionFlag = True
					else:
						if iExperience >= iLevel*iLevel + 1:
							PromotionFlag = True
					
					if PromotionFlag == True:
						if pUnit.canAcquirePromotion(gc.getInfoTypeForString(sPromotion)):
							pUnit.changeLevel(1)
							pUnit.setHasPromotion(gc.getInfoTypeForString(sPromotion),True)
							pUnit.changeDamage(-(pUnit.getDamage() / 2),iPlayer);
							#print pUnit.getID()
							#print sPromotion
							
						#����CAL�A�b�v���i�Ȃ�΁A�o���l���Ȃ��Ȃ�܂Ŏ擾������
						if sPromotion == 'PROMOTION_CARD_ATTACK_LEVEL_UP':
							pUnit.setNumAcquisSpellPromotion(pUnit.getNumAcquisSpellPromotion()+1)
							pUnit.setHasPromotion(gc.getInfoTypeForString(sPromotion),False)
							while(1):
								iExperience = pUnit.getExperience()
								iLevel = pUnit.getLevel()
								PromotionFlag = False
								if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CHARISMATIC')):
									if iExperience >= (iLevel*iLevel+1 + 1) *3 /4:
										PromotionFlag = True
								else:
									if iExperience >= iLevel*iLevel + 1:
										PromotionFlag = True
								
								if PromotionFlag == True:
									pUnit.changeLevel(1)
									pUnit.changeDamage(-(pUnit.getDamage() / 2),iPlayer);
									pUnit.setNumAcquisSpellPromotion(pUnit.getNumAcquisSpellPromotion()+1)
								else:
									break
									
				#�X�y�����[�g��AI�������j�b�g�ɃX�y�����g�p������
				#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pUnit.getAIPromotionRoute() == 3 and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False:
				#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False:
				Functions.AISpellCast(pUnit)

		
		
		#CAL���P�U�ȏ�̎q�͊m���ō��Ԍ��E���l������
		#���߁F�����̂Ƃ���R�����g�A�E�g�g�����ǁA��肠�����c���Ă���
		#if pUnit.countCardAttackLevel() >= 16 :
		#	if gc.getGame().getSorenRandNum(100,"get oukakekkai") < pUnit.countCardAttackLevel():
		#		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_OUKAKEKKAI'),True)
		
		#���j�� PROMOTION_REKISHI�������Ă�q��������A������폜���邩�������
		#if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_EASY')):
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_EASY'),False)
		#if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_NORMAL')):
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_NORMAL'),False)
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_EASY'),True)
		#if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_HARD')):
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_HARD'),False)
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_NORMAL'),True)
		#if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_LUNATIC')):
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_LUNATIC'),False)
		#	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI_HARD'),True)
				
				
				
		#�������j�b�g�ł��邱�Ƃ��O��̏��������܂�
		
		
	def BPTprocessPromotions(self, pUnit, argsList):
		#�^�[���o�߂ŏ��ł���^�C�v�̃o�t�E�f�o�t���i�͂����ŏ�������
		iGameTurn, iPlayer = argsList
		
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		BarbarianFlag = False
		TurnPromoFlag = False
		#�قڑ�����ւ��ɋ߂�������邽�߁A�܊p�Ȃ̂Ńo�t�ƃf�o�t�ŕ�����
		#�o�t�n������
		#���Ƃ�X�y�J�ɂ�鏸�i�������Ă����ꍇ�A�P�����N��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR2')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR2'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR1'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR3')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR3'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR2'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR4')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR4'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR3'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR5')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR5'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TERRIBLE_SOUVEBNIR4'),True)
			
		#���[���X�y�J�E���i�e�B�b�N�K���̏���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		#���x��2
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV2_TURN1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV2_TURN1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV2_TURN2')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV2_TURN1'),True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV2_TURN2'),False)
		#���x��3
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN2')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN1'),True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN2'),False)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN3')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN2'),True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LUNATICGUN_LV3_TURN3'),False)
			
		#PROMOTION_NEKKYOU�������Ă�q��������A���i����
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NEKKYOU')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NEKKYOU'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		#PROMOTION_HOTARUNOHIKARI�������Ă�q��������A������폜
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HOTARUNOHIKARI')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HOTARUNOHIKARI'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)

		#�V���t�B�z�����̏���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SYLPHAEHORN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SYLPHAEHORN'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#���@��ǂ������Ă�q��������A���̏��i������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BARRIER')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BARRIER'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		#���̎��������Ă�q��������A���̏��i������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHIKINOSHIKI')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHIKINOSHIKI'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#�΂˂��݂̔�߂������Ă���Ώ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HINEZUMINOKAWAGOROMO')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HINEZUMINOKAWAGOROMO'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#PROMOTION_DOLLS_WAR�������Ă�q��������A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DOLLS_WAR')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DOLLS_WAR'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#���i�F�X�R�A�f�U�C�A�C�[�^�[�������Ă����ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SCORE_DESIRE')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCORE_DESIRE'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#���i�F�ǔ����������Ă����ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KABENUKE')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KABENUKE'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#����Ph�����L���Ă��郆�j�b�g�̏���
		#���Ɣ�������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_1TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_1TURN'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_2TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_2TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_1TURN'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_3TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_3TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_2TURN'),True)
		#���ƌ��͌p��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_1TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_1TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KODUCHI_HANDOU_3TURN'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_2TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_2TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_1TURN'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_3TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_3TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_2TURN'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_4TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_4TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_3TURN'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_5TURN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_5TURN'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_4TURN'),True)
			
		#�u�n���̃r�[�g�v�������Ă���ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PRISTINE_BEAT')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PRISTINE_BEAT'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#�u���@���v�������Ă���ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2'),True)
		
		#�u�X�s�[�h�X�g���C�N�v�������Ă���ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPEED_STRIKE')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPEED_STRIKE'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#���ߒ��̏��i������ꍇ�A����������������ߔ�����t�^
		#���ߔ����̏��i������ꍇ�A���������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TAME_KANRYOU')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TAME_KANRYOU'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TAMETYUU')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TAMETYUU'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TAME_KANRYOU'),True)
			
		
		#�o�t�n�����܂�
		
		#�f�o�t�n������
		
		#������̃f�B���C������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_1')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_1'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_2')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_2'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_1'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_3')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_3'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_2'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_4')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_4'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_3'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_5')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_5'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_4'),True)
		
		#PROMOTION_FREEZE�������Ă�q��������A�_���[�W��25���^���A�s���I���E�E�E�ł��Ȃ��@1/2�ŏ��i�폜
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FREEZE')):
			TurnPromoFlag = True
			#pUnit.changeDamage(25,iPlayer)
			#pUnit.finishMoves()
			#pUnit.changeMoves(-5)
			if gc.getGame().getSorenRandNum(100, "Toho Unit gets Experience Percent") < 50:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FREEZE'),False) 
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#PROMOTON_THEWORLD�n�������Ă���q��������A�_���[�W��^���Ă�����폜�@20%�ȉ��ɂ͂Ȃ�Ȃ��悤��
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_EASY')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_EASY'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			if 19 < (100-pUnit.getDamage()) and (100-pUnit.getDamage()) < 50:
				pUnit.setDamage(80,iPlayer)
			elif (100-pUnit.getDamage()) >= 40:
				pUnit.changeDamage(30,iPlayer)
			
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_NORMAL')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_NORMAL'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			if 19 < (100-pUnit.getDamage()) and (100-pUnit.getDamage()) < 60:
				pUnit.setDamage(80,iPlayer)
			elif (100-pUnit.getDamage()) >= 50:
				pUnit.changeDamage(40,iPlayer)
			
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_HARD')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_HARD'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			if 19 < (100-pUnit.getDamage()) and (100-pUnit.getDamage()) < 70:
				pUnit.setDamage(80,iPlayer)
			elif (100-pUnit.getDamage()) >= 60:
				pUnit.changeDamage(50,iPlayer)
			
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_LUNATIC')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_THEWORLD_LUNATIC'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			if 19 < (100-pUnit.getDamage()) and (100-pUnit.getDamage()) < 80:
				pUnit.setDamage(80,iPlayer)
			elif (100-pUnit.getDamage()) >= 70:
				pUnit.changeDamage(60,iPlayer)
			
		#PROMOTION_KURAYAMI�������Ă�q��������A20���̊m���ł��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KURAYAMI')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Remove PROMOTION_KURAYAMI") < 20:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KURAYAMI'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#PROMOTION_POISON�n�������Ă�q��������A���̂ɂ���ă_���[�W��^���Ă���30���̊m���ł��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON1')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Remove Poison1") < 30:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON1'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON2')):
			TurnPromoFlag = True
			pUnit.changeDamage(15,iPlayer)
			if gc.getGame().getSorenRandNum(100,"Remove Poison2") < 30:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON2'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON3')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Remove Poison3") < 30:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON3'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON4')):
			TurnPromoFlag = True
			pUnit.changeDamage(15,iPlayer)
			if gc.getGame().getSorenRandNum(100,"Remove Poison4") < 30:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISON4'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		#PROMOTION_CHARM�������Ă�q��������A�T�O���̊m���ł��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHARM')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Remove Charm") < 50:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHARM'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		#���C�������Ă�����m���ł��܂��܂ȍs�������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MADNESS')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 50:        #���C�ɖ߂�
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MADNESS'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 15:        #�ؑ���
				BarbarianFlag = True
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 25:        #�����ɌŒ�_���[�W
				iDamage =  gc.getGame().getSorenRandNum(41, "MADNESS damage") + 10
				pUnit.changeDamage(iDamage,pUnit.getOwner())
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 25:     #���X�^�b�N�Ƀ_���[�W
				UnitList = []
				pPlot = pUnit.plot()
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					if pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY') and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
						UnitList.append(pUnit)
				for i in range(5):
					if len(UnitList) > 0:
						iRandNum2 = gc.getGame().getSorenRandNum(len(UnitList), "MADNESS rand")
						iDamage =  gc.getGame().getSorenRandNum(6, "MADNESS damage") + 5
						UnitList[iRandNum2].changeDamage(iDamage,pUnit.getOwner())
						if UnitList[iRandNum2].getDamage >= 100:
							del UnitList[iRandNum2]
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 25: #���������
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHARM'),True)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 25: #�ϋv�͔���
				iDamage = (100-pUnit.getDamage()) / 2
				pUnit.changeDamage(iDamage,pUnit.getOwner())
			if gc.getGame().getSorenRandNum(100, "MADNESS") < 25:       #����ɕ���
				#����2�}�X�ŋ󂢂Ă�ꏊ��T���A�Ȃ���Γ����Ȃ�
				ClearPlotList = []
				for iX in range(pUnit.getX()-2,pUnit.getX()+3):
					for iY in range(pUnit.getY()-2,pUnit.getY()+3):
						if gc.getMap().plot(iX,iY).getNumUnits() == 0:
							ClearPlotList.append([iX,iY])
				if len(ClearPlotList)!=0:
					iNum = gc.getGame().getSorenRandNum(len(ClearPlotList), "create barbarian plot")
					pUnit.setXY(ClearPlotList[iNum][0],ClearPlotList[iNum][1],False,True,True)
				
		#�p���X�B�̃X�y�J�ɂ�鏸�i�A���i�S�������Ă����ꍇ�A�m���Ŕؑ���
		#���߁F�p���X�B�X�y�J�͓r���ŃO���[���A�C�h�����X�^�[�̕��ɂȂ肱�����͒��������Ǝv����
		#�ł��ꉞ�c���Ă������Ƃ�
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100, "SHITTOSHIN EASY") < 10:
				BarbarianFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100, "SHITTOSHIN NORMAL") < 10:
				BarbarianFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100, "SHITTOSHIN NORMAL") < 10:
				BarbarianFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL'),True)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_LUNATIC')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100, "SHITTOSHIN NORMAL") < 10:
				BarbarianFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_LUNATIC'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD'),True)
				
		#���ڂ������Ă�����A��������ŏ�������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TORIME')):
			TurnPromoFlag = True
			RangeList = [ [-1,-1],[ 0,-1],[ 1,-1],[-1, 0], [ 0, 0],[ 1, 0],[-1, 1],[ 0, 1],[ 1, 1], ]
			if Functions.checkUnit(pUnit.getX(),pUnit.getY(),RangeList,gc.getInfoTypeForString('UNIT_MYSTIA1'),gc.getInfoTypeForString('UNIT_MYSTIA6')) == False:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TORIME'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#�e�����E�������Ă����炷�������_���[�W���󂯂�
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DANMAKUKEKKAI')):
			TurnPromoFlag = True
			pUnit.setDanmakuKekkai( pUnit.getNowDanmakuKekkai()+1 , pUnit.getMaxDanmakuKekkai() )
			if (pUnit.getNowDanmakuKekkai() >= pUnit.getMaxDanmakuKekkai()):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANMAKUKEKKAI'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			iDamage = pUnit.getNowDanmakuKekkai() * 5 + 5
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				iDamage /= 2
			iDamage = iDamage *  (100 - pUnit.countSpellTolerance()) / 100
			pUnit.changeDamage(iDamage,pUnit.getOwner())
					
		#�u�X�^���v������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_STAN')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STAN'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#���C�̏��i�������Ă���΁A�n�`�ɉ����ď���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FROST')):
			TurnPromoFlag = True
			pPlot = pUnit.plot()
			if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_TUNDRA') and  pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_SNOW'):
				if gc.getGame().getSorenRandNum(100,"Letty Skill") < 50:
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FROST'),False)
					pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#�u�ǂ���Ԃ�v��25���̊m���ŏ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HEAVY_RAIN')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Kogasa Skill") < 25:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEAVY_RAIN'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#���i�F�]���r�̓ł������Ă����ꍇ�A25���ŏ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIE_POISON')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Remove ZombiePoison") < 25:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIE_POISON'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#�u���씽�]�v��25���̊m���ŏ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SOUSA_HANTEN_A')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Seija Skill") < 25:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SOUSA_HANTEN_A'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SOUSA_HANTEN_B')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Seija Skill") < 25:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SOUSA_HANTEN_B'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		#�u�㉺���]�v��50���̊m���ŏ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_JOUGE_HANTEN_A')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Seija Skill") < 50:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_JOUGE_HANTEN_A'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_JOUGE_HANTEN_B')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Seija Skill") < 50:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_JOUGE_HANTEN_B'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
		
		#�v���̖��������Ă���Ίm���ŏ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KUONNOYUME')):
			TurnPromoFlag = True
			if gc.getGame().getSorenRandNum(100,"Mima Skill") < 30:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KUONNOYUME'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
				
		#�т�����������Ă���Ώ���
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_OOPS')):
			TurnPromoFlag = True
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_OOPS'),False)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			
		#���i�F���΂������Ă����ꍇ�A�_���[�W��25���^�������50���ŏ���
		#���߁F����͕z�sEX�����������܂��Z�p�́E�m���s���Ŕ�r�I�ȒP�Ȃ��̂����o���Ȃ��������ߓ��������ȈՓI�Ȃ���
		#���ɒ������Ă��Č��݂́i�L�����m���Ȃ�j�g���Ă��Ȃ�
		#���A�����̖��ɗ���������Ȃ��̂Ŏ�肠�����R�����g�A�E�g�Œu���Ă���
		#if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HAKKA')):
		#	pUnit.changeDamage(25,iPlayer)
		#	if gc.getGame().getSorenRandNum(100,"Remove Hakka") < 50:
		#		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HAKKA'),False)
		
		#���i�F���|�������Ă����ꍇ�A��ʃ��j�b�g�Ȃ�50%�A�������j�b�g�Ȃ�100���ł��������
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FEAR')):
			TurnPromoFlag = True
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FEAR'),False)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)
			else:
				if gc.getGame().getSorenRandNum(100,"Remove Fear") < 50:
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FEAR'),False)
					pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() -1)

				
				

				
			#�f�o�t�n�����܂�
			#�Ȍ�͂��̑��̏��i������
				
		#�^�[���n���i�������Ă��Ȃ��ɂ��ւ�炸TurnPromo�̒l�������Ă���ꍇ�A���Z�b�g����
		if not TurnPromoFlag:
			pUnit.setNumTurnPromo(0)
				
		#�ؑ���
		#�����Ɍ����Ə��i�ł͂Ȃ����A�����ŏ������]�܂���
		if BarbarianFlag == True:
			BarBarianUnit = pUnit.getUnitType()
			plotX = pUnit.getX()
			plotY = pUnit.getY()
			iExperience = pUnit.getExperience()
			iLevel = pUnit.getLevel()
			
			#���͂P�}�X�ŋ󂢂Ă�ꏊ��T���A�Ȃ���Ώ���
			ClearPlotList = []
			for iX in range(plotX-1,plotX+2):
				for iY in range(plotY-1,plotY+2):
					if gc.getMap().plot(iX,iY).getNumUnits() == 0:
						ClearPlotList.append([iX,iY])
						
			if len(ClearPlotList)!=0:
				iNum = gc.getGame().getSorenRandNum(len(ClearPlotList), "create barbarian plot")
				iiX = ClearPlotList[iNum][0]
				iiY = ClearPlotList[iNum][1]
				newUnit1 = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(BarBarianUnit, iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
				newUnit1.changeExperience(iExperience,-1,false,false,false)
				newUnit1.changeLevel(iLevel-1)
				
				#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
				PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
				PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
				PromotionNum = PromotionEnd - PromotionStart
				
				for iPromotion in range(PromotionNum):
					if pUnit.isHasPromotion(iPromotion):
						newUnit1.setHasPromotion(iPromotion,True)
				newUnit1.setNumTurnPromo(pUnit.getNumTurnPromo())
				newUnit1.finishMoves()
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY'),False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL'),False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD'),False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_LUNATIC'),False)
				
			pUnit.changeDamage(100,pUnit.getOwner())
				
					
		
		
	def BPTprocessAITurn(self, argsList):
		iGameTurn, iPlayer = argsList
		#���AI���̏����iAI���E���@�Ȃǁj��Z�߂�Ƃ�
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		
		#print pPlayer.getID() + 1000
		#print pPlayer.getAIPromotionRoute()
		
		#�l�Ԃ̗��Ő��E���@���\�ȂƂ��A�����ɂ���Đ��E���@���g�p����
		iCiv = pPlayer.getCivilizationType()
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if pPlayer.getNumWorldSpell()>0:
				if gc.getGame().getGameTurn() > 50:
					pTeam = gc.getTeam(pPlayer.getTeam())
					iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
					for i in range(iNumTeam):
						ppTeam = gc.getTeam(i)
						if ppTeam.isBarbarian() == False:
							if pTeam.isAtWar(i):
								pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength())
								pPlayer.setNumWorldSpell(0)
								CyInterface().addImmediateMessage("&#20154;&#38291;&#12398;&#37324;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#40644;&#37329;&#26399;&#12364;&#30330;&#21205;&#12375;&#12414;&#12375;&#12383;","")
		
		#�A���Ő��E���@���\�ȂƂ��A�����ɂ���Đ��E���@���g�p����
		iCiv = pPlayer.getCivilizationType()
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
			if pPlayer.getNumWorldSpell()>0:
				if gc.getGame().getGameTurn() > 50:
					pTeam = gc.getTeam(pPlayer.getTeam())
					iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
					for i in range(iNumTeam):
						ppTeam = gc.getTeam(i)
						if ppTeam.isBarbarian() == False:
							if pTeam.isAtWar(i):
								#�����Ă��郆�j�b�g�͎���ˑ�
								iNumUnit = 5
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
									iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
									iNumUnit = 2
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL'):
									iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
									iNumUnit = 3
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
									iUnit = gc.getInfoTypeForString('UNIT_MACEMAN')
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE'):
									iUnit = gc.getInfoTypeForString('UNIT_MUSKETMAN')
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
									iUnit = gc.getInfoTypeForString('UNIT_RIFLEMAN')
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN'):
									iUnit = gc.getInfoTypeForString('UNIT_INFANTRY')
								if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE'):
									iUnit = gc.getInfoTypeForString('UNIT_MECHANIZED_INFANTRY')
								
								py = PyPlayer(iPlayer)
								for pPyCity in py.getCityList():
									pCity = pPlayer.getCity(pPyCity.getID())
									iNum = pCity.getPopulation() / iNumUnit
									if iNum < 1:
										iNum = 1
									if iNum > 3:
										iNum = 3
									for i in range(iNum):
										newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.changeExperience(gc.getGame().getSorenRandNum(6, "world spell rengou no kessoku"),-1,False,False,False)
								pPlayer.setNumWorldSpell(0)
								CyInterface().addImmediateMessage("&#22934;&#31934;&#12383;&#12385;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#37117;&#24066;&#12395;&#38598;&#32080;&#12375;&#12414;&#12375;&#12383;","")

		#����MOD�ǋL����
		#�P�j��̎����E���@���g�p�\�ȏꍇ�A���E���@���g�p����
		iCiv = pPlayer.getCivilizationType()
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
			if pPlayer.getNumWorldSpell()>0:
				if gc.getGame().getGameTurn() > 50:
					pTeam = gc.getTeam(pPlayer.getTeam())
					iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
					for i in range(iNumTeam):
						ppTeam = gc.getTeam(i)
						if ppTeam.isBarbarian() == False:
							if pTeam.isAtWar(i):
								TAIKOFlag = False
								TYUUSEIFlag = False
								KINDAIFlag = False
								
									#����ɂ���ĕ������郆�j�b�g��v�Z����ϓ�������
								if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL')):
									iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TAIKO')
									iNumCityCountKOU = 3
									TAIKOFlag = True
								if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE')):
									iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TYUUSEI')
									iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_TYUUSEI')
									iNumCityCountKOU = 5
									iNumCityCountOTU = 8
									TYUUSEIFlag = True
								if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE')):
									iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_KINDAI')
									iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_KINDAI')
									iNumCityCountKOU = 5
									iNumCityCountOTU = 8
									KINDAIFlag = True
									
								py = PyPlayer(iPlayer)
								for pPyCity in py.getCityList():
									pCity = pPlayer.getCity(pPyCity.getID())
								
									if TAIKOFlag == True:
										iNumKOU = pCity.getPopulation() / iNumCityCountKOU
										if iNumKOU > 2:
											iNumKOU = 2
										iNumOTU = 0
		
									elif TYUUSEIFlag == True:
										iNumKOU = pCity.getPopulation() / iNumCityCountKOU
										if iNumKOU < 1:
											iNumKOU = 1
										if iNumKOU > 3:
											iNumKOU = 3

										iNumOTU = pCity.getPopulation() / iNumCityCountOTU
										if iNumOTU > 1:
											iNumOTU = 1
		
									else:
										iNumKOU = pCity.getPopulation() / iNumCityCountKOU
										if iNumKOU < 1:
											iNumKOU = 1
										if iNumKOU > 3:
											iNumKOU = 3
			
										iNumOTU = pCity.getPopulation() / iNumCityCountOTU
										if iNumOTU < 1:
											iNumOTU = 1
										if iNumOTU > 3:
											iNumOTU = 3
		
									if iNumKOU >= 1:
										for i in range(iNumKOU):
											newUnit = pPlayer.initUnit(iUnitKOU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
									if iNumOTU >= 1:
										for i in range(iNumOTU):
											newUnit = pPlayer.initUnit(iUnitOTU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

								pPlayer.setNumWorldSpell(0)
								CyInterface().addImmediateMessage("&#36637;&#37341;&#22478;&#12398;&#21508;&#37117;&#24066;&#12391;&#20184;&#21930;&#31070;&#12364;&#22823;&#37327;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

	def BPTprocessCity(self, pCity, argsList):
		iGameTurn, iPlayer = argsList
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		
		#����MOD�ǋL����
		#���̃v���C���[�̎�s����
		pCapital = gc.getPlayer(pCity.getOwner()).getCapitalCity()
		
		#�P�j��̃��j�b�g������������
		## originai:king_richard_s_crusade ##
		
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU")):
			obsoleteTech = gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KISHINJOU")).getObsoleteTech()
			if ( pTeam.isHasTech(obsoleteTech) == false or obsoleteTech == -1 ):
				iX = pCity.getX()
				iY = pCity.getY()
				tyousaheidan = gc.getInfoTypeForString( 'UNIT_KOBITO_TYOUSAHEIDAN' )
				estiEnd = CyGame().getEstimateEndTurn()
				if ( estiEnd >= 1000 ):
					if ( iGameTurn % 12 ) == 0:
						pNewUnit = pPlayer.initUnit( tyousaheidan, iX, iY, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.NO_DIRECTION )
				elif ( estiEnd >= 700 ):
					if ( iGameTurn % 8 ) == 0:
						pNewUnit = pPlayer.initUnit( tyousaheidan, iX, iY, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.NO_DIRECTION )
				elif ( estiEnd >= 500 ):
					if ( iGameTurn % 6 ) == 0:
						pNewUnit = pPlayer.initUnit( tyousaheidan, iX, iY, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.NO_DIRECTION )

				elif ( estiEnd >= 300 ):
					if ( iGameTurn % 4 ) == 0:
						pNewUnit = pPlayer.initUnit( tyousaheidan, iX, iY, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.NO_DIRECTION )
				else:
					if ( iGameTurn % 4 ) == 0:
						pNewUnit = pPlayer.initUnit( tyousaheidan, iX, iY, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.NO_DIRECTION )

				basechance = 12
				estiEnd = CyGame().getEstimateEndTurn()
				if ( estiEnd >= 1000 ):
					basechance = basechance
				elif ( estiEnd >= 700 ):
					basechance = 6
				elif ( estiEnd >= 500 ):
					basechance = 4
				elif ( estiEnd >= 300 ):
					basechance = 2
				else:
					basechance = 1
			
		#����MOD�ǋL���������܂�
		
		#���P�̌ŗL�u���������
		if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KOGASALIST')):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SADESM'),1)
		
		#���o���[�h�ł����
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(pCity.getOwner()).isHuman():
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MUSOU_MODE'),1)
		
		
		#����MOD�ǋL����
		
		#�w���Ґ��ׂ������ȍ~�ɖ��������̗p���Ă�����A�������V�׋S�ݒu
		#����͈ڐA�s�A���̂܂ܒu���Ă�����������
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SEIJALIST')) and \
			pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_ANCIENT') and \
			pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_CLASSICAL') and \
			pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LEGAL')) == gc.getInfoTypeForString('CIVIC_BARBARISM') and \
			pCity.isCapital() and pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_AMANOJAKU")) == 0:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AMANOJAKU'),1)
		
		#�W���u�������ŁA����s�ɏW���u���{�[�i�X�������������ꍇ�͎����ݒu
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
			if pCapital.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CENTRALIZATION")) == False:
				pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CENTRALIZATION'),1)
			
		#����MOD�ǋL���������܂�
			
		#��̖���������A�|�n���j�b�g�������ꍇ�͏���
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_ENIGMATIC_CRY')):
			pPlot = pCity.plot()
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ENIGMATIC_CRY'),0)
					break
		
		
		#�s�s�ɓ���̌�����������A����̃��j�b�g�����Ȃ���Ό���������
		for BuildingList in TohoUnitList.TohoUnitBuildingList:
			sBuilding,sStartUnit,sEndUnit = BuildingList
			if pCity.isHasBuilding(gc.getInfoTypeForString(sBuilding)):
				if Functions.checkUnit(pCity.getX(),pCity.getY(),[[0,0],],gc.getInfoTypeForString(sStartUnit),gc.getInfoTypeForString(sEndUnit)) == False:
					if sBuilding == 'BUILDING_SUZURAN':
						if Functions.checkUnit(pCity.getX(),pCity.getY(),[[0,0],],gc.getInfoTypeForString('UNIT_MEDICINwithSU1'),gc.getInfoTypeForString('UNIT_MEDICINwithSU6')) == False:
							pCity.setNumRealBuilding(gc.getInfoTypeForString(sBuilding),0)
					if sBuilding == 'BUILDING_SHUEN':
						if Functions.checkUnit(pCity.getX(),pCity.getY(),[[0,0],],gc.getInfoTypeForString('UNIT_SUIKA1_YOUKAI'),gc.getInfoTypeForString('UNIT_SUIKA6_YOUKAI')) == False:
							pCity.setNumRealBuilding(gc.getInfoTypeForString(sBuilding),0)
					else:
						pCity.setNumRealBuilding(gc.getInfoTypeForString(sBuilding),0)
			
		#�s���̂���s�s������΁A���̓s�s�̐l�����̋��K�����ǂ񂰂��������镶���ɓ���
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_GYOUSHOU')):
			#���ǂ񂰃T�[�`
			flag = False
			for i in range(19): #�������̃}�W�b�N�i���o�[
				ppPlayer = gc.getPlayer(i)
				if ppPlayer.isBarbarian() == False and ppPlayer.isAlive() == True:
					ppy = PyPlayer(i)
					for pUnit in ppy.getUnitList():
						if gc.getInfoTypeForString('UNIT_REISEN0') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_REISEN6'):
							ppPlayer.changeGold(pCity.getPopulation() * ppPlayer.getCity(ppy.getCapitalCity().getID()).getTotalCommerceRateModifier(0) / 100)
							flag = True
							break
					if flag:
						break;
								
		#�~�X�e�B�A�R���T�[�g�̂���s�s������΁A�S���E�̃t�@���N���u�̐��ɂ��킹�ċ��K�����
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_MYSTIACONCERT')):
			#�S�s�s����
			iChange = 0
			for i in range(19):
				ppPlayer = gc.getPlayer(i)
				if ppPlayer.isBarbarian() == False and ppPlayer.isAlive() == True:
					ppy = PyPlayer(i)
					for ppyCity in ppy.getCityList():
						ppCity = ppPlayer.getCity(ppyCity.getID())
						if ppCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_MYSTIA_FANCLUB')):
							if pCity.getOwner() == ppCity.getOwner():
								iChange = iChange + 1
							if ppCity.hasBonus(gc.getInfoTypeForString('BONUS_YOSUZUNOUTA')):
								iChange = iChange + 1
			pCity.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_MYSTIACONCERT'),0,iChange)
		
		#�ς����̖�����������΁A����ɉ����ĎY�o�A�b�v
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_PATCHOULI_BOOK')):
			iAge = gc.getPlayer(pCity.getOwner()).getCurrentEra()
			pCity.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_PATCHOULI_BOOK'),1, (iAge+1) * 2 )
		
		#�X�y�����j�������g������΁A����ɉ����ĎY�o�A�b�v
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_SPELL_OBELISK')):
			iAge = gc.getPlayer(pCity.getOwner()).getCurrentEra()
			for i in range(3):
				if pCity.getBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),i) > 0:
					if i==0:
						pCity.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),i,(TohoUnitList.SpellistAIBonusList[(iAge)]+1)/2 )
					else:
						pCity.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),i,TohoUnitList.SpellistAIBonusList[iAge] )
			for i in range(4):
				if pCity.getBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),i) > 0:
					pCity.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),i,TohoUnitList.SpellistAIBonusList[iAge] )
			
		#�Ԕ�������ΐ���or�͉�
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE')):
			MeirinFlag = False
			for i in range(pCity.plot().getNumUnits()):
				if gc.getInfoTypeForString('UNIT_MEIRIN0') <= pCity.plot().getUnit(i).getUnitType() and pCity.plot().getUnit(i).getUnitType() <= gc.getInfoTypeForString('UNIT_MEIRIN6'):
					MeirinFlag = True
			if MeirinFlag:
				pCity.setFlowerGardenTurn( pCity.getFlowerGardenTurn()+1 )
			else:
				pCity.setFlowerGardenTurn( pCity.getFlowerGardenTurn()-1 )
			
			Growth = 0 #�O�Ȃ�ω������@�P�Ȃ琬���@�|�P�Ȃ�͉�
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				if pCity.getFlowerGardenTurn() >= 24:
					Growth = 1
				if pCity.getFlowerGardenTurn() <= 3:
					Growth = -1
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				if pCity.getFlowerGardenTurn() >= 22:
					Growth = 1
				if pCity.getFlowerGardenTurn() <= 4:
					Growth = -1
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				if pCity.getFlowerGardenTurn() >= 20:
					Growth = 1
				if pCity.getFlowerGardenTurn() <= 5:
					Growth = -1
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				if pCity.getFlowerGardenTurn() >= 18:
					Growth = 1
				if pCity.getFlowerGardenTurn() <= 6:
					Growth = -1
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				if pCity.getFlowerGardenTurn() >= 16:
					Growth = 1
				if pCity.getFlowerGardenTurn() <= 7:
					Growth = -1
			
			iNumHappy = pCity.getBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') )
			iNumHealth = pCity.getBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') )
			if Growth > 0:
				pCity.setFlowerGardenTurn(10)
				if gc.getGame().getSorenRandNum(100, "hanabatake") < 50:
					pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , iNumHappy + 1 )
				else:
					pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , iNumHealth + 1 )
			if Growth < 0:
				pCity.setFlowerGardenTurn(10)
				if iNumHappy + iNumHealth <= 1 :
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE'),0)
				else:
					if iNumHappy >= iNumHealth:
						pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , iNumHappy - 1 )
					else:
						pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , iNumHealth - 1 )
					if iNumHappy <= 0 and iNumHealth <= 0 :
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE'),0)
		
		
#����MOD�ǋL���������܂�

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList
		##### <written by F> #####
		#�^�[�����Ƃɍs���鏈���@
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		Limit = 1

		#�����낿��񃉃��_���u������
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_KOKOROLIST')):
			#�ŏ���1�^�[���ڂɊm���ɔ����A�ȍ~�̓����_��
			if iGameTurn == 0:
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TRAIT_KOKOROLIST_FIRSTTURN')
				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)
			elif CyGame().getSorenRandNum(1000, "Kokorolist") < 20:
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TRAIT_KOKOROLIST')
				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, iPlayer, -1, -1, -1, -1, -1)

		#�������j�b�g�g�̐ݒ�@�`�[����Ή��p
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and pPlayer.isHuman():
			if pTeam.isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')):
				Limit = 3
			if pTeam.isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')):
				Limit = 5
		else:
			if pTeam.isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')):
				Limit = 2
			if pTeam.isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')):
				Limit = 3
		pPlayer.setNumTohoUnitLimit( Limit)
		#AI�������[�h�ɂ��␳
		if pPlayer.isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
			pPlayer.setNumTohoUnitLimit( Limit + TohoUnitList.TohoNumList[Functions.getHandicap()] )
		#CyInterface().addImmediateMessage(gc.getHandicapInfo(pPlayer.getHandicapType()).getDescription(),"")
			
		#���̃v���C���[�̃��j�b�g�S�{��
		for pUnit in py.getUnitList():
			#�������j�b�g�̏���������
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				self.BPTprocessTohoUnit(pUnit, argsList)
			
			#�ꎞ���i�n�̏���������
			if pUnit.getNumTurnPromo() > 0:
				self.BPTprocessPromotions(pUnit, argsList)
			
			#�ȉ��͂ЂƂ܂������ŏ������邵���Ȃ�����
			#�������j�b�g�ȊO�ɂ������肷����̂����S
			#SPELL_CASTED�������Ă�q��������A��������� 
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False)
			
			#PROMOTION_ILLUSION�������Ă�q��������A���̎q���폜
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')):
				pUnit.changeDamage(100,iPlayer)
			
			#���R�񕜂�����Ή�
			if pUnit.countAutoHeal() > 0:
				pUnit.changeDamage(-pUnit.countAutoHeal(),iPlayer)
			
			#�A���퓬�̃J�E���g�����Z�b�g
			pUnit.setNumCombatCombo(0)
			
			#�Ă�g���b�v�̔�������
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_TRAP'):
				pTeam = gc.getTeam(pUnit.getTeam())
				SpyList = Functions.checkUnit(pUnit.getX(),pUnit.getY(),RangeList1,gc.getInfoTypeForString('UNIT_SPY'),gc.getInfoTypeForString('UNIT_SPY'),2)
				UnitList = Functions.checkUnit(pUnit.getX(),pUnit.getY(),RangeList1,gc.getInfoTypeForString('UNIT_SANAE0'),gc.getInfoTypeForString('UNIT_GREAT_SPY'),2)
				SpyList2 = []
				UnitList2 = []
				for pSpy in SpyList:
					if pTeam.isAtWar(pSpy.getTeam()) and pSpy.getDamage()<100:
						SpyList2.append(pSpy)
				for pUnit2 in UnitList:
					if pTeam.isAtWar(pUnit2.getTeam()):
						UnitList2.append(pUnit2)
			
				#�X�p�C������΃X�p�C�ƈ��������Ƀg���b�v����
				if len(SpyList2) > 0:
					SpyList2[0].changeDamage(100,pUnit.getOwner())
					pUnit.changeDamage(100,pUnit.getOwner())
					
					point = pUnit.plot().getPoint()
					CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
					CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
					
				else:
					#�X�p�C�����Ȃ��悤�Ȃ��
					if len(UnitList2) > 0:
						Functions.changeDamage(RangeList1,pUnit,0,20,0,True,False,False,True,-1,True,True,True,True,-1,False,0,4)
						pUnit.changeDamage(100,pUnit.getOwner())
						
						point = pUnit.plot().getPoint()
						CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
						CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		#AI�̂Ƃ�
		if pPlayer.isHuman() == False:
			self.BPTprocessAITurn(argsList)
		
		#���̃v���C���[�̓s�s�S����
		for pPyCity in py.getCityList():
			pCity = pPlayer.getCity(pPyCity.getID())
			self.BPTprocessCity(pCity, argsList)
		
		##### </written by F> #####
		
	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList
		
		##### <written by F> #####
		#�^�[���I�����s���鏈���@
		py = PyPlayer(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		
		#���̃v���C���[�̃��j�b�g�S����
		for pUnit in py.getUnitList():
			
			#�v���C���[�ɓ|���ꂽ�t���O���ւ��܂�
			pUnit.setbLoseByPlayer(False)
			
			#�X�y�����[�g��AI�������j�b�g�ɃX�y�����g�p������
			#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
			#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pUnit.getAIPromotionRoute() == 3 and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False:
			#if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False:
			if pUnit.isHuman() == False:
				Functions.AISpellCast(pUnit)
			
			#�퓬�͍Čv�Z
			pUnit.countCombatBonus()
			
		
		##### </wrritn by F> #####
		
		#����MOD�ǋL����
		
		#���̃v���C���[�̓s�s�S����
		for pPyCity in py.getCityList():
			pCity = pPlayer.getCity(pPyCity.getID())
			pCapital = gc.getPlayer(pCity.getOwner()).getCapitalCity()
			
		#�����낿���̎u���ω��ŘJ���u���������Ȃ����ꍇ�̏���
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_KOKOROLIST')):
				if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_LABORLIST')):
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_2'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_2'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),0)
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_HAKUREISIKI'),0)
				#�W���u���̏ꍇ�����l�ɏ���
				if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CENTRALIZATION'),0)
		
		
		#�W���u���u�[�X�g���������Z�b�g
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
				if pCapital.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CENTRALIZATION")) == False:
					if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CENTRALIZATION")) == True:
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CENTRALIZATION'),0)
		
		#����MOD�ǋL���������܂�
		
		if (gc.getGame().getElapsedGameTurns() == 1):
			if (gc.getPlayer(iPlayer).isHuman()):
				if (gc.getPlayer(iPlayer).canRevolution(0)):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetAdvisorNags()
		CvAdvisorUtils.endTurnFeats(iPlayer)

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]

	def onFirstContact(self, argsList):
		'Contact'
		iTeamX,iHasMetTeamY = argsList
		if (not self.__LOG_CONTACT):
			return
		CvUtil.pyPrint('Team %d has met Team %d' %(iTeamX, iHasMetTeamY))

	def onCombatResult(self, argsList):
		'Combat Result'
		pWinner,pLoser = argsList
		playerX = PyPlayer(pWinner.getOwner())
		unitX = PyInfo.UnitInfo(pWinner.getUnitType())
		playerY = PyPlayer(pLoser.getOwner())
		unitY = PyInfo.UnitInfo(pLoser.getUnitType())
		##### <written by F> #####
		#����̃X�L���������̂͘A���퓬���\�ɂȂ�B
		#�������A�^�[�����̏�����Ƃ��ă��x�����R�{�P ������Ă��烌�x��/2�{�P
		
		#����MOD�ǋL����
		#�A���U�����̌v�Z����ύX
		#�f�̘A���U���̓L�������x��/4+1�A�X�L���n�A���U���̓��x��/3+1�A���������Ă����烌�x��/3+3
		iNumRenzoku = 0
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RENZOKUKOUGEKI')):
			iNumRenzoku = iNumRenzoku+1
		if (pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REMILIA_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAN_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOUMU_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TENSHI_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YUKA_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BYAKUREN_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOSHIKA_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RAIKO_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YORIHIME_SKILL1')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHIKINOSHIKI')) ):
			iNumRenzoku = iNumRenzoku+2
		if iNumRenzoku >=3:
			if pWinner.getNumCombatCombo() < (pWinner.getLevel()/3 + 3):
				if gc.getPlayer(pWinner.getOwner()).isTurnActive(): #�A�N�e�B�u�^�[���Ȃ�
					pWinner.changeMoves(-50)
					pWinner.setMadeAttack(False)
					pWinner.setNumCombatCombo(pWinner.getNumCombatCombo()+1)
					#�A���퓬����������ƃ��b�Z�[�W���o��
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pWinner.getUnitType()).getDescription() + "&#12398;&#36899;&#32154;&#25126;&#38360;&#65281(" + str(pWinner.getNumCombatCombo()) + "/" + str(pWinner.getLevel()/3 + 3) + ")","")
		elif iNumRenzoku >=2:
			if pWinner.getNumCombatCombo() < (pWinner.getLevel()/3 + 1):
				if gc.getPlayer(pWinner.getOwner()).isTurnActive(): #�A�N�e�B�u�^�[���Ȃ�
					pWinner.changeMoves(-50)
					pWinner.setMadeAttack(False)
					pWinner.setNumCombatCombo(pWinner.getNumCombatCombo()+1)
					#�A���퓬����������ƃ��b�Z�[�W���o��
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pWinner.getUnitType()).getDescription() + "&#12398;&#36899;&#32154;&#25126;&#38360;&#65281(" + str(pWinner.getNumCombatCombo()) + "/" + str(pWinner.getLevel()/3 + 1) + ")","")
		elif iNumRenzoku >=1:
			if pWinner.getNumCombatCombo() < (pWinner.getLevel()/4 + 1):
				if gc.getPlayer(pWinner.getOwner()).isTurnActive(): #�A�N�e�B�u�^�[���Ȃ�
					pWinner.changeMoves(-50)
					pWinner.setMadeAttack(False)
					pWinner.setNumCombatCombo(pWinner.getNumCombatCombo()+1)
					#�A���퓬����������ƃ��b�Z�[�W���o��
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pWinner.getUnitType()).getDescription() + "&#12398;&#36899;&#32154;&#25126;&#38360;&#65281(" + str(pWinner.getNumCombatCombo()) + "/" + str(pWinner.getLevel()/4 + 1) + ")","")

		#���i�u�n���̃r�[�g�v���邢�́u�ł��o�̏��Ɓv�n��������Ă���ꍇ�A��x����̘A���퓬���\�Ƃ���
		if (pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PRISTINE_BEAT')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_5TURN')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_4TURN')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_3TURN')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_2TURN')) or
			pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UCHIDENO_KODUCHI_1TURN')) ):
			if pWinner.getNumCombatCombo() < 1:
				if gc.getPlayer(pWinner.getOwner()).isTurnActive(): #�A�N�e�B�u�^�[���Ȃ�
					pWinner.changeMoves(-50)
					pWinner.setMadeAttack(False)
					pWinner.setNumCombatCombo(pWinner.getNumCombatCombo()+1)
					#�A���퓬����������ƃ��b�Z�[�W���o��
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pWinner.getUnitType()).getDescription() + "&#12398;&#36899;&#32154;&#25126;&#38360;&#65281(" + str(pWinner.getNumCombatCombo()) + "/" + str( + 1) + ")","")
		
		
		#��x�퓬������ƃ��[���@�e�C��������
		pWinner.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAEVATEINN'),False)
		pLoser.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAEVATEINN'),False)
		
		#�i�Y�[�����̃}�[�N�ŋ��K�l��
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NAZRIN')):
			numChangeGold = (pWinner.getUnitType() - gc.getInfoTypeForString('UNIT_SANAE0'))%7 * 2 
			gc.getPlayer(pWinner.getOwner()).changeGold(numChangeGold)
		
		#����̃X�L���������̂́A�퓬�ɏ�������Ɛ퓬�͉�
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REMILIA_SKILL1')):
			pWinner.changeDamage(-10,pWinner.getOwner())
		
		#�ő������̗͉͑�
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')):
			pWinner.changeDamage(-5,pWinner.getOwner())
			
		#�ő��ƔM�������͒ǉ��ŉ񕜁��o���l�l��
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')) and pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NEKKYOU')):
			pWinner.changeDamage(-5,pWinner.getOwner())
			pWinner.changeExperience(1,-1,False,False,False)
		
		#�M�������͏�����Ɋm�����ő����l��
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NEKKYOU')):
			if gc.getGame().getSorenRandNum(100, "nekkyou") < 50:
				pWinner.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU'),True)
		
		
		#�z�K�q�̃X�L�������́A�퓬������m���œG���Q�Ԃ�B
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUWAKO_SKILL1')):
			if pLoser.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				if gc.getGame().getSorenRandNum(100, "SUWAKO SKILL") < 25:
					RevivalUnit = pLoser.getUnitType()
					plotX = pWinner.getX()
					plotY = pWinner.getY()
					iExperience = pLoser.getExperience()
					iLevel = pLoser.getLevel()
					newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					
					newUnit1.changeExperience(iExperience,-1,false,false,false)
					newUnit1.changeLevel(iLevel-1)
					
					#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
					PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
					PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
					PromotionNum = PromotionEnd - PromotionStart
					
					for iPromotion in range(PromotionNum):
						if pLoser.isHasPromotion(iPromotion):
							newUnit1.setHasPromotion(iPromotion,True)
					newUnit1.finishMoves()
		
		
		#�ς����̃X�L�������́A�퓬������ɃS�[�����𐶐�����B
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PATCHOULI_SKILL1')):
			if pLoser.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				RevivalUnit = pLoser.getUnitType()
				plotX = pWinner.getX()
				plotY = pWinner.getY()
				newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM'),True)
				newUnit1.finishMoves()
		
		#�����̃X�L�������́A�퓬�����ɒǉ��̌o���l�Ƌ��K���l������
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KOMACHI_SKILL1')):
			pWinner.changeExperience(1,-1,False,False,False)
			gc.getPlayer(pWinner.getOwner()).changeGold(pLoser.getLevel()*5)

		#����MOD�ǋL����
		#���X�L�������́A�퓬�����ɒǉ��̋��K���l������
		
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SYOU_SKILL1')):
			iNumGold = gc.getGame().getSorenRandNum( pWinner.baseCombatStr(),"tora skill")
			gc.getPlayer(pWinner.getOwner()).changeGold(iNumGold)
		
		#����MOD�ǋL���������܂�
				
		#�`���m�̃X�L���������U�����ď��������ꍇ�A�s�҂̃X�^�b�N�Ƀ����_���œ����̏��i 
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CIRNO_SKILL1')):
			if gc.getPlayer(pWinner.getOwner()).isTurnActive():
				pPlot = gc.getMap().plot(pLoser.getX(),pLoser.getY())
				for i in range(pPlot.getNumUnits()):
					if gc.getGame().getSorenRandNum(100, "CIRNO SKILL") < 20:
						#�ړ��͂̃`�F�b�N
						unitInfo = gc.getUnitInfo(pPlot.getUnit(i).getUnitType())
						if unitInfo.getMoves() != 0 and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
							if pPlot.getUnit(i).getDamage() > 84:
								pPlot.getUnit(i).changeDamage( (100 - pPlot.getUnit(i).getDamage()) - 1 ,pWinner.getOwner())
							else:
								pPlot.getUnit(i).changeDamage(15,pWinner.getOwner())
							pPlot.getUnit(i).setHasPromotion(gc.getInfoTypeForString('PROMOTION_FREEZE'),True)
							
		
		#�X�L�������̂ɂƂ肪�G��|�����ꍇ�A�͓����{�������Ă���
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NITORI_SKILL1')):
			iPlayer = pWinner.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iX = pWinner.getX()
			iY = pWinner.getY()
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_HELICOPTER'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARMOR'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.finishMoves()
		
		#�������X�L�������͐퓬�ɏ�������Ƒ���̏��i�������_���Ń��[�j���O
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1')):
			CanLearningList = [
								'PROMOTION_COMBAT1',
								'PROMOTION_COMBAT2',
								'PROMOTION_COMBAT3',
								'PROMOTION_COMBAT4',
								'PROMOTION_COMBAT5',
								'PROMOTION_COMBAT6',
								'PROMOTION_TOHO_COMBAT1',
								'PROMOTION_TOHO_COMBAT2',
								'PROMOTION_TOHO_COMBAT3',
								'PROMOTION_TOHO_COMBAT4',
								'PROMOTION_TOHO_COMBAT5',
								'PROMOTION_TOHO_COMBAT6',
								'PROMOTION_DRILL1',
								'PROMOTION_DRILL2',
								'PROMOTION_DRILL3',
								'PROMOTION_DRILL4',
								'PROMOTION_TOHO_DRILL1',
								'PROMOTION_TOHO_DRILL2',
								'PROMOTION_TOHO_DRILL3',
								'PROMOTION_TOHO_DRILL4',
								'PROMOTION_ANTI_BOSS1',
								'PROMOTION_ANTI_BOSS2',
								'PROMOTION_MEDIC1',
								'PROMOTION_MEDIC2',
								'PROMOTION_MEDIC3',
								'PROMOTION_CITY_RAIDER1',
								'PROMOTION_CITY_RAIDER2',
								'PROMOTION_CITY_RAIDER3',
								'PROMOTION_CITY_GARRISON1',
								'PROMOTION_CITY_GARRISON2',
								'PROMOTION_CITY_GARRISON3',
								]
			PromotionList = []
			
			for i in range(len(CanLearningList)):
				if pWinner.isHasPromotion(gc.getInfoTypeForString(CanLearningList[i])) == False and pLoser.isHasPromotion(gc.getInfoTypeForString(CanLearningList[i])) == True:
					PromotionList.append(CanLearningList[i])
			if len(PromotionList) > 0:
				#����MOD�ǋL����
				#�������X�L���͔��茩�؂�擾�܂ł͊m������
				pTeam = gc.getTeam(pWinner.getTeam())
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')):
					iNumPromotion = gc.getGame().getSorenRandNum(len(PromotionList), "MARISA Learning")
					pWinner.setHasPromotion(gc.getInfoTypeForString(PromotionList[iNumPromotion]),True)
				else:
					if gc.getGame().getSorenRandNum(100, "Marisa SKILL") < 25:
						iNumPromotion = gc.getGame().getSorenRandNum(len(PromotionList), "MARISA Learning")
						pWinner.setHasPromotion(gc.getInfoTypeForString(PromotionList[iNumPromotion]),True)
				#����MOD�ǋL���������܂�
			
		#�s�������������������猳�ɖ߂�
		if ( pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE1') or
			pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE2') or
			pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE3') or
			pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE4') or
			pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE5') or
			pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_KOISHI_FADE6') ):
			
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE1"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI1")
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE2"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI2")
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE3"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI3")
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE4"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI4")
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE5"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI5")
			if pWinner.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE6"):
				RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI6")
			iExperience = pWinner.getExperience()
			iLevel = pWinner.getLevel()
			newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, pWinner.getX(), pWinner.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
			newUnit1.changeExperience(iExperience,-1,false,false,false)
			newUnit1.changeLevel(iLevel-1)
			
			#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
			PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
			PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
			PromotionNum = PromotionEnd - PromotionStart
			
			for iPromotion in range(PromotionNum):
				if pWinner.isHasPromotion(iPromotion):
					newUnit1.setHasPromotion(iPromotion,True)
	
			newUnit1.convert(pWinner)
			#newUnit1.setMoves(pWinner.getMoves()+50)
			newUnit1.finishMoves()
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True)
		
		
		#�v���C���[�ɓ|���ꂽAI���j�b�g�ɂ͂�������t���O������
		pLoser.setbLoseByPlayer(False)
		if pWinner.isHuman() and pLoser.isHuman() == False:
			pLoser.setbLoseByPlayer(True)
			
		#�䂩���X�L��������A����t���O�������Ă����HP����ւ���
		if pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YUKARI_SKILL1')):
			if pLoser.getSpecialNumber() > 0:
				#CvGameUtils.doprint("Auto Bomb Test Start")
			
				RevivalUnit = pLoser.getUnitType()
				plotX = pLoser.getX()
				plotY = pLoser.getY()
				iExperience = pLoser.getExperience()
				iLevel = pLoser.getLevel()
				newUnit1 = gc.getPlayer(pLoser.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
				newUnit1.changeExperience(iExperience,-1,false,false,false)
				newUnit1.changeLevel(iLevel-1)
				
				newUnit1.setNumCastSpellCard(pLoser.getNumCastSpellCard())
				newUnit1.setNumAcquisSpellPromotion(pLoser.getNumAcquisSpellPromotion())
				newUnit1.setSpecialNumber(pLoser.getSpecialNumber())
				newUnit1.setDanmakuKekkai(pLoser.getNowDanmakuKekkai(),pLoser.getMaxDanmakuKekkai() )
				
				newUnit1.setSinraDelayTurn(pLoser.getSinraDelayTurn())
				newUnit1.setNumTransformTime(pLoser.getNumTransformTime())
				
				newUnit1.setMoves(pLoser.getMoves())
				
				#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
				PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
				PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
				PromotionNum = PromotionEnd - PromotionStart
				
				for iPromotion in range(PromotionNum):
					if pLoser.isHasPromotion(iPromotion):
						newUnit1.setHasPromotion(iPromotion,True)

				newUnit1.changeDamage(pWinner.getDamage(),pLoser.getOwner())
				if pWinner.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
					pWinner.changeDamage(-100,pLoser.getOwner())
					pWinner.changeDamage(99,pLoser.getOwner())
				else:
					pWinner.changeDamage(100,pLoser.getOwner())
				
				CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pLoser.getUnitType()).getDescription() + "&#12364;&#29983;&#12392;&#27515;&#12398;&#22659;&#30028;&#12434;&#12356;&#12376;&#12426;&#12414;&#12375;&#12383;&#65281;","")

		#����MOD�ǋL������������
		
		#�_��_�L�����N�^�[�}�[�N�n�E�F��
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOSHIKA')):
			if gc.getGame().getSorenRandNum(100, "YOSHIKA SKILL") < 8:
				if pLoser.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
					RevivalUnit = pLoser.getUnitType()
					plotX = pWinner.getX()
					plotY = pWinner.getY()
					newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KYONSHII'),True)
					newUnit1.finishMoves()
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pLoser.getUnitType()).getDescription() + "&#12364;&#12461;&#12519;&#12531;&#12471;&#12540;&#12392;&#12375;&#12390;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�_��_�L�����N�^�[�}�[�N�n�E�M
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SEIGA')):
			if gc.getGame().getSorenRandNum(100, "SEIGA SKILL") < 12:
				if pLoser.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
					RevivalUnit = pLoser.getUnitType()
					plotX = pWinner.getX()
					plotY = pWinner.getY()
					newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KYONSHII'),True)
					newUnit1.finishMoves()
					CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pLoser.getUnitType()).getDescription() + "&#12364;&#12461;&#12519;&#12531;&#12471;&#12540;&#12392;&#12375;&#12390;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�_��_�L�����N�^�[�}�[�N�n�E�j����
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOJIKO')):
			if gc.getGame().getSorenRandNum(100, "TOJIKO SKILL") < 5:
				iPlayer = pWinner.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iX = pWinner.getX()
				iY = pWinner.getY()
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.finishMoves()
				CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�_��_�L�����N�^�[�}�[�N�n�E�z�s
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FUTO')):
			if gc.getGame().getSorenRandNum(100, "FUTO SKILL") < 10:
				iPlayer = pWinner.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iX = pWinner.getX()
				iY = pWinner.getY()
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.finishMoves()
				CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
				
		#�_��_�L�����N�^�[�}�[�N�n�E�_�q
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMIMIKO')):
			if gc.getGame().getSorenRandNum(100, "MIMIMIKO SKILL") < 10:
				iPlayer = pWinner.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iX = pWinner.getX()
				iY = pWinner.getY()
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.finishMoves()
				CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
			elif pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMIMIKO_SKILL1')):
				if gc.getGame().getSorenRandNum(100, "MIMIMIKO SKILL PLUS") < 15:
					iPlayer = pWinner.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					iX = pWinner.getX()
					iY = pWinner.getY()
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.finishMoves()
					CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�W�܂�_��1�������Ă����ꍇ
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ATUMARU_SHINREI1')):
			if pWinner.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
				if gc.getGame().getSorenRandNum(100, "ATUMARU SHINREI1") < 2:
					iPlayer = pWinner.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					iX = pWinner.getX()
					iY = pWinner.getY()
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.finishMoves()
					CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�W�܂�_��2�������Ă����ꍇ
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ATUMARU_SHINREI2')):
			if pWinner.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
				if gc.getGame().getSorenRandNum(100, "ATUMARU SHINREI2") < 4:
					iPlayer = pWinner.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					iX = pWinner.getX()
					iY = pWinner.getY()
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.finishMoves()
					CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")
		
		#�����̎g���ɂ�铮���Q�Ԃ菈��
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KASENLIST_DOUBUTU')):
			iPlayer = pWinner.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iX = pWinner.getX()
			iY = pWinner.getY()
			if pLoser.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_LION'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GETLION'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_BEAR'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GETBEAR'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_PANTHER'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GETPANTHER'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pLoser.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_WOLF'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GETWOLF'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.finishMoves()
		
		#���|�̂낭��񏈗�
		if pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SEKIBANKILIST_FEAR')):
			pPlot = gc.getMap().plot(pWinner.getX(),pWinner.getY())
			for i in range(pPlot.getNumUnits()):
				if gc.getGame().getSorenRandNum(100, "ROKUROKUBI") < 10:
					if pWinner.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
						pPlot.getUnit(i).setHasPromotion(gc.getInfoTypeForString('PROMOTION_FEAR'),True)
						pPlot.getUnit(i).setNumTurnPromo(pUnit.getNumTurnPromo() +1)
		
		#�����X�L���̕����h�䌸������
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATUHASHI_SKILL1')):
			pPlot2 = pLoser.plot()
			if pPlot2.isCity():
				pCity2 = pPlot2.getPlotCity()
				pPlayer = gc.getPlayer(pWinner.getOwner())
				if gc.getTeam(pPlayer.getTeam()).isAtWar(gc.getPlayer(pCity2.getOwner()).getTeam()):
					pCity2.changeDefenseDamage(15)
		
		#���ۃX�L���̉���������
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RAIKO_SKILL1')):
			if gc.getGame().getSorenRandNum(100, "RAIKO_SKILL") < 5:
				pPlayer = gc.getPlayer(pWinner.getOwner())
				pPlayer.changeGoldenAgeTurns(+1)
		
		#�u�ő����v�������G�����j�������A�m���Łu�[�����̂ǂ��v����
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_INCLUSION')):
			if pLoser.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				iPlayer = pWinner.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iX = pWinner.getX()
				iY = pWinner.getY()
				if gc.getGame().getSorenRandNum(100, "Deepone Inclusion") < 20:
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(3)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(5)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(7)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(8)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(13)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(17)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
					if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE'):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DEEPONE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setSpecialNumber(23)
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
						newUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
						newUnit.finishMoves()
		
		#�ǂ�݃X�L���������Ă���ꍇ�A�������j�b�g�ɖ��I�`�t�^
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DOREMY_SKILL1')):
			pPlot = gc.getMap().plot(pWinner.getX(),pWinner.getY())
			for i in range(pPlot.getNumUnits()):
				if gc.getGame().getSorenRandNum(100, "Yumeoti") < 10:
					if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY") and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
						pPlot.getUnit(i).setHasPromotion(gc.getInfoTypeForString('PROMOTION_DOREMY_YUMEOTI'),True)
		
		#�T�O���X�L���������Ă���ꍇ�A�T�O����UG�i�K�ɉ����ĒT�m�^�@������
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAGUME_SKILL1')):
			iPlayer = pWinner.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iX = pWinner.getX()
			iY = pWinner.getY()
			if gc.getGame().getSorenRandNum(100, "Tantigata kirai") < 15:
				if pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME1') or \
				pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME2'):
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_2'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
				if pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME3') or \
				pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME4'):
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_3'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
				if pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME5') or \
				pWinner.getUnitType() == gc.getInfoTypeForString('UNIT_SAGUME6'):
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		#�퓬������Power��
		#�Ȍケ��Power�񕜂͊�{�I�Ɉꕔ�������j�b�g�̃L�����N�^�[�X�L���������͓�����
		if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAGUME_SKILL1')) or \
		pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PATCHOULI_SKILL1')) or \
		pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1')) or \
		pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BYAKUREN_SKILL1')):
			pWinner.setPower(pWinner.getPower() + 0.03)
		
		
		#����MOD�ǋL���������܂�
		
		#���ꂼ��̃��j�b�g�ɂ��Power�񕜂��v�Z
		#WinnerTohoUnitList = Functions.searchTeamTohoUnit(pWinner.plot(),pWinner)
		#for i in range(len(WinnerTohoUnitList)):
		#	WinnerTohoUnitList[i].setPower( WinnerTohoUnitList[i].getPower() + (0.01 / len(WinnerTohoUnitList)) )
		#
		#LoserTohoUnitList = Functions.searchTeamTohoUnit(pLoser.plot(),pLoser)
		#for i in range(len(LoserTohoUnitList)):
		#	LoserTohoUnitList[i].setPower( LoserTohoUnitList[i].getPower() + (0.003 / len(LoserTohoUnitList)) )
		#
		#if pWinner.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
		#	pWinner.setPower(pWinner.getPower() + 0.03)

		
		##### </written by F> #####
		
		if (not self.__LOG_COMBAT):
			return
		if playerX and playerX and unitX and playerY:
			CvUtil.pyPrint('Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s'
				%(playerX.getID(), playerX.getCivilizationName(), unitX.getDescription(),
				playerY.getID(), playerY.getCivilizationName(), unitY.getDescription()))

	def onCombatLogCalc(self, argsList):
		'Combat Result'
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iCombatOdds = genericArgs[2]
		CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)

	def onCombatLogHit(self, argsList):
		'Combat Message'
		global gCombatMessages, gCombatLog
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]

		if (iIsAttacker == 0):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (gc.getPlayer(cdDefender.eOwner).getNameKey(), cdDefender.sUnitName, iDamage, cdDefender.iCurrHitPoints, cdDefender.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdDefender.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (gc.getPlayer(cdAttacker.eOwner).getNameKey(), cdAttacker.sUnitName, gc.getPlayer(cdDefender.eOwner).getNameKey(), cdDefender.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
		elif (iIsAttacker == 1):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (gc.getPlayer(cdAttacker.eOwner).getNameKey(), cdAttacker.sUnitName, iDamage, cdAttacker.iCurrHitPoints, cdAttacker.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdAttacker.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (gc.getPlayer(cdDefender.eOwner).getNameKey(), cdDefender.sUnitName, gc.getPlayer(cdAttacker.eOwner).getNameKey(), cdAttacker.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)

#����MOD�ǋL����
# BULL events
	def onCombatWithdrawal(self, argsList):
		"""Fired when a unit withdraws from combat after doing maximum damage."""
		pAttacker, pDefender = argsList
		
		#�u�q�g�T�m�^�@���v���G�����j�i�����ɂ����Ə����ދp�j�������A���g������
		if ( pAttacker.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_1') or
			pAttacker.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_2') or
			pAttacker.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_3') or
			pAttacker.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4') ):
			pAttacker.changeDamage(100,pAttacker.getOwner())
		
		#BugUtil.debug("%s withdraws from %s", 
		#		pAttacker.getName(), pDefender.getName())
	
	def onCombatRetreat(self, argsList):
		"""Fired when a unit retreats from combat, escaping death."""
		pAttacker, pDefender = argsList
		
		#BugUtil.debug("%s retreats from %s", 
		#		pAttacker.getName(), pDefender.getName())
	
	def onCombatLogCollateral(self, argsList):
		"""Fired when a unit inflicts collateral damage to another unit."""
		#���߁FCollateral�Ƃ͌������ǎ��ۂ̓J�m���C���U�镺��ɂ�镛���ł͂Ȃ�
		#�����@�Ȃǂŗ^���镛���œ��삷��͗l�B�����Ŋm�F
		pAttacker, pDefender, iDamage = argsList
		
		#BugUtil.debug("%s bombards %s for %d HP", 
		#		pAttacker.getName(), pDefender.getName(), iDamage)
	
	def onCombatLogFlanking(self, argsList):
		"""Fired when a unit inflicts flanking damage to another unit."""
		pAttacker, pDefender, iDamage = argsList
		
		#BugUtil.debug("%s flanks %s for %d HP", 
		#		pAttacker.getName(), pDefender.getName(), iDamage)

#����MOD�ǋL���������܂�

	def onImprovementBuilt(self, argsList):
		'Improvement Built'
		iImprovement, iX, iY = argsList
		
		#�����������E����MOD�ǋL
		#���̓s�e���t�H�[�~���O����
		if(iImprovement==gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN_COMPLETE')):
			pPlot = CyMap().plot(iX, iY)
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			pPlot.setImprovementType(-1)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_PLAIN_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/plains.dds',ColorTypes(8),iX,iY,True,True)
		
		if(iImprovement==gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS_COMPLETE')):
			pPlot = CyMap().plot(iX, iY)
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			pPlot.setImprovementType(-1)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_GRASS_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(8),iX,iY,True,True)
		
		if(iImprovement==gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL_COMPLETE')):
			pPlot = CyMap().plot(iX, iY)
			pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
			pPlot.setImprovementType(-1)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_HILL_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/hill.dds',ColorTypes(8),iX,iY,True,True)
		
		if(iImprovement==gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND_COMPLETE')):
			pPlot = CyMap().plot(iX, iY)
			pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
			pPlot.setImprovementType(-1)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FLATLAND_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(8),iX,iY,True,True)
		
		if(iImprovement==gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FOREST_COMPLETE')):
			pPlot = CyMap().plot(iX, iY)
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_REGENERATION_FOREST'), 1)
			pPlot.setImprovementType(-1)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FOREST_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/terrainfeatures/forest.dds',ColorTypes(8),iX,iY,True,True)
		
		
		
		#�����������E����MOD�ǋL�����܂�
		
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was built at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onImprovementDestroyed(self, argsList):
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was Destroyed at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onRouteBuilt(self, argsList):
		'Route Built'
		iRoute, iX, iY = argsList
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Route %s was built at %d, %d'
			%(gc.getRouteInfo(iRoute).getDescription(), iX, iY))

	def onPlotRevealed(self, argsList):
		'Plot Revealed'
		pPlot = argsList[0]
		iTeam = argsList[1]

	def onPlotFeatureRemoved(self, argsList):
		'Plot Revealed'
		pPlot = argsList[0]
		iFeatureType = argsList[1]
		pCity = argsList[2] # This can be null

	def onPlotPicked(self, argsList):
		'Plot Picked'
		pPlot = argsList[0]
		CvUtil.pyPrint('Plot was picked at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onNukeExplosion(self, argsList):
		'Nuke Explosion'
		pPlot, pNukeUnit = argsList
		CvUtil.pyPrint('Nuke detonated at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onGotoPlotSet(self, argsList):
		'Nuke Explosion'
		pPlot, iPlayer = argsList

	def onBuildingBuilt(self, argsList):
		'Building Completed'
		pCity, iBuildingType = argsList
		game = gc.getGame()
		if ((not gc.getGame().isNetworkMultiPlayer()) and (pCity.getOwner() == gc.getGame().getActivePlayer()) and isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType())):
			# If this is a wonder...
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setData1(iBuildingType)
			popupInfo.setData2(pCity.getID())
			popupInfo.setData3(0)
			popupInfo.setText(u"showWonderMovie")
			popupInfo.addPopup(pCity.getOwner())
		
		
		##### <written by > #####
		#�����������݂��ꂽ�Ƃ��̒ǉ�����
		
		#���@���͂U�łP�Z�b�g
		if iBuildingType == gc.getInfoTypeForString('BUILDING_MEIRENJI1'):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI2'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI3'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI4'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI5'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI6'),1)
			
		##### </written by > #####
		
		#����MOD�ǋL����
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		#�j�����@�[�i�͌��Ă��s�s�̐��E��Y�̐��ɂ���ďo�͕ω�
		if iBuildingType == gc.getInfoTypeForString('BUILDING_NIRVANA'):
			iWonders = pCity.getNumWorldWonders()
			pCity.setBuildingYieldChange (gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_NIRVANA")).getBuildingClassType(), YieldTypes.YIELD_PRODUCTION, iWonders*5)
		
		#�i�������݂ň�Y1�ɂ���Z���ʎs��2�l�̃{�[�i�X
		if iBuildingType == gc.getInfoTypeForString('BUILDING_EIENTEI'):
			iWonders = pCity.getNumWorldWonders()
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_CITIZEN"), iWonders*2)
		
		#�j�����@�[�i�A�y�щi�����ɒǉ��ň�Y�����Ă��ꍇ�A�X�ɏo�͑���
		if isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
			if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString("BUILDINGCLASS_NIRVANA")) == 1:
				if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_NIRVANA")) == True:
					iWonders = pCity.getNumWorldWonders()
					pCity.setBuildingYieldChange (gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_NIRVANA")).getBuildingClassType(), YieldTypes.YIELD_PRODUCTION, iWonders*5)
			
			if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString("BUILDINGCLASS_EIENTEI")) == 1:
				if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_EIENTEI")) == True:
					pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_CITIZEN"), 2)

		#�_��_�@�����̈̐l�ϊ�����
		if iBuildingType == gc.getInfoTypeForString('BUILDING_HOURYUUJI'):
			iPRIEST = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST"))
			iARTIST = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ARTIST"))
			iSCIENTIST = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SCIENTIST"))
			iMERCHANT = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_MERCHANT"))
			iENGINEER = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ENGINEER"))
			iGENERAL = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL"))
			iSPY = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SPY"))
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST"), -iPRIEST)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST_HOURYUUJI"), iPRIEST)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ARTIST"), -iARTIST)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ARTIST_HOURYUUJI"), iARTIST)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SCIENTIST"), -iSCIENTIST)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SCIENTIST_HOURYUUJI"), iSCIENTIST)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_MERCHANT"), -iMERCHANT)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_MERCHANT_HOURYUUJI"), iMERCHANT)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ENGINEER"), -iENGINEER)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ENGINEER_HOURYUUJI"), iENGINEER)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL"), -iGENERAL)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL_HOURYUUJI"), iGENERAL)
			
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SPY"), -iSPY)
			pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SPY_HOURYUUJI"), iSPY)

		#�A���R�[�����b�g���ݎ��A�فX�X�y��������������΋����łɐ؂�ւ�
		if iBuildingType == gc.getInfoTypeForString('BUILDING_ANGKOR_WAT'):
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_GION_SYOUJA_A")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GION_SYOUJA_B'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GION_SYOUJA_A'),0)
		
		#���ۂ̎��@-�튮�����A���쐬�Ȃ�叫�R����
		if iBuildingType == gc.getInfoTypeForString('BUILDING_RAIKO_MAGIC_A'):
			if pPlayer.getMysteryiumFlag() == 0:
				iX = pCity.getX()
				iY = pCity.getY()
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GREAT_GENERAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		#���ۂ̎��@-���������A���ɂȂ錚���������ꂼ���UB�Q�֎����ϊ�
		#�古�l�����ۂ������ɔ���
		#���Ȃ݂ɂ��������̘b�A�̐l��������̓~�X�e���E���p�ϐ��ő�p�B
		#�`�[����ŉi�����Ƒg�񂾎��ȊO�͑�����薳���͂���
		if iBuildingType == gc.getInfoTypeForString('BUILDING_RAIKO_MAGIC_B'):
			py = PyPlayer(iPlayer)
			if pPlayer.getMysteryiumFlag() == 0:
				iX = pCity.getX()
				iY = pCity.getY()
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCHANT'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for pPyCity in py.getCityList():
				ppCity = pPlayer.getCity(pPyCity.getID())
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_GROCER")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GROCER'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CASTLE")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CUSTOM_HOUSE")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_FACTORY")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FACTORY'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_COAL_PLANT")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_SUPERMARKET")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET'),0)
		
		#�������فX���X�g�[���w���W�����݂����ꍇ�A����X�g�[���w���W�Ɏ����ϊ�
		#if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_BENBENLIST")):
		#	if iBuildingType == gc.getInfoTypeForString('BUILDING_STONEHENGE'):
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_STONEHENGE'),0)
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BENBEN_STONEHENGE'),1)
		
		#���ǐ_�Ђ����݂����s�s�̎���2�}�X�����ɔ_�ꂨ��ѕۈ��т���������ϊ�������
		if iBuildingType == gc.getInfoTypeForString('BUILDING_TSUKUYOMI_SHRINE'):
			pTeam = gc.getTeam(pPlayer.getTeam())
			# �͈͂̒�`
			RangeListCity2 = [        [-1,-2],[ 0,-2],[ 1,-2],
							  [-2,-1],[-1,-1],[ 0,-1],[ 1,-1],[ 2,-1],
							  [-2, 0],[-1, 0],        [ 1, 0],[ 2, 0],
							  [-2, 1],[-1, 1],[ 0, 1],[ 1, 1],[ 2, 1],
							          [-1, 2],[ 0, 2],[ 1, 2],        ]
			# �s�s(pCity)�𒆐S�Ƃ���RangeListCity2�̂͂񂢂ɂȂ񂩂���
			for sq in RangeListCity2:
				iX = pCity.getX() + sq[0]
				iY = pCity.getY() + sq[1]
				if Functions.isPlot(iX,iY):
					pPlot = gc.getMap().plot(iX,iY)
					if pPlayer.getTeam() == pPlot.getTeam():
						if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
							pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MARS_FARM'))
						if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FOREST_PRESERVE'):
							pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MOONBASE'))
			#iX = pCity.getX()
			#iY = pCity.getY()
			#for iiX in range(iX-2,iX+3):
			#	for iiY in range(iY-2,iY+3):
			#		if Functions.isPlot(iiX,iiY):
			#			pPlot = gc.getMap().plot(iiX,iiY)
			#			if pPlayer.getTeam() == pPlot.getTeam():
			#				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
			#					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MARS_FARM'))
			#				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FOREST_PRESERVE'):
			#					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MOONBASE'))
	
		#����MOD�ǋL���������܂�

		CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

		if (not self.__LOG_BUILDING):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(PyInfo.BuildingInfo(iBuildingType).getDescription(), pCity.getOwner(), gc.getPlayer(pCity.getOwner()).getCivilizationDescription(0)))

	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList
		game = gc.getGame()
		if ((not gc.getGame().isNetworkMultiPlayer()) and (pCity.getOwner() == gc.getGame().getActivePlayer())):
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setData1(iProjectType)
			popupInfo.setData2(pCity.getID())
			popupInfo.setData3(2)
			popupInfo.setText(u"showWonderMovie")
			popupInfo.addPopup(pCity.getOwner())
		
		##### <written by > #####
		
		if iProjectType == gc.getInfoTypeForString('PROJECT_ORENOYOME'):
			pPlayer = gc.getPlayer(pCity.getOwner())
			pPlayer.setNumMadeMyLove( pPlayer.getNumMadeMyLove()+1  )
			pPlayer.setNumMyLove( pPlayer.getNumMyLove()+1  )
			
		##### </written by > #####
		#����MOD�ǋL����
		## originai:AI Build Projects Automatically Start ##
		##AI�Ƀ_�~�[�v���W�F�N�g���쐬�����邽�߂̓�������##
		##XML���ł͊��m1�������L�Z�p�̋��L�ƂȂ��Ă��邽�߁A����𑦍��ɒ���������##
		if gc.getProjectInfo(iProjectType).getTechShare() == 1:
			pPlayer = gc.getPlayer(pCity.getOwner())
			pTeam = gc.getTeam(pPlayer.getTeam())
			pTeam.changeTechShareCount(0, -1)
		## originai:AI Build Projects Automatically End ##

		#����MOD�ǋL����
		##�n��a�쐬���A��Ȋw��2�l���̃r�[�J�[�擾##
		## originai:CGEs�X�[�p�[�R���s���[�^�[ ##
		if iProjectType == gc.getInfoTypeForString("PROJECT_CHIREIDEN"):
			iPlayer = pCity.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			pTeam = gc.getTeam(iTeam)
			
			##�����͑����l
			unitResearchPercent = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getUnitDiscoverPercent()
			iResearch = 4500 * unitResearchPercent / 100
                        
			##�����̌����𔻒f
			pResearch = pPlayer.getCurrentResearch ()

			##���������Ă��Ȃ��ꍇ�A��������v�[�����A�������Ǝ��̌�����I�Ԃ悤�ɑ���
			##see also onTechSelected().
			if(pResearch == gc.getInfoTypeForString('NO_TECH')):
				self.ChireidenOverflow = (iPlayer, iResearch)
				pPlayer.chooseTech(0, "&#22320;&#38666;&#27583;&#12364;&#23436;&#25104;&#12375;&#12414;&#12375;&#12383;&#65281;&#30740;&#31350;&#12377;&#12427;&#12486;&#12463;&#12494;&#12525;&#12472;&#12540;&#12434;&#36984;&#25246;&#12375;&#12390;&#12367;&#12384;&#12373;&#12356;&#12290;", true)

			##�����łȂ��ꍇ�A������Ă錤������������
			else:
				pTeam.changeResearchProgress(pResearch,iResearch,iPlayer)

			CyInterface().addImmediateMessage("&#21476;&#26126;&#22320;&#12373;&#12392;&#12426;&#12364;&#22519;&#31558;&#12375;&#12383;&#26360;&#29289;&#12398;&#35299;&#35501;&#12395;&#12424;&#12426;&#12289;&#22320;&#38666;&#27583;&#25991;&#26126;&#12398;&#30740;&#31350;&#12364;&#22823;&#24133;&#12395;&#36914;&#12415;&#12414;&#12375;&#12383;&#65281;","")

		## originai:CGEs�X�[�p�[�R���s���[�^�[ ##
		#����MOD�ǋL���������܂�
		
		
	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]

		if (not self.__LOG_PUSH_MISSION):
			return
		if pHeadUnit:
			CvUtil.pyPrint("Selection Group pushed mission %d" %(eMission))

	def onUnitMove(self, argsList):
		'unit move'
		pPlot,pUnit,pOldPlot = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return
		if player and unitInfo:
			CvUtil.pyPrint('Player %d Civilization %s unit %s is moving to %d, %d'
				%(player.getID(), player.getCivilizationName(), unitInfo.getDescription(),
				pUnit.getX(), pUnit.getY()))

	def onUnitSetXY(self, argsList):
		'units xy coords set manually'
		pPlot,pUnit = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return

	def onUnitCreated(self, argsList):
		'Unit Completed'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		##### <written by F> #####
		
		#�������j�b�g�����ꂽ��J�E���g����
		if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			pPlayer = gc.getPlayer(unit.getOwner())
			pPlayer.setNumTohoUnit(pPlayer.getNumTohoUnit()+1)
			
			#���i���[�g�̑I��
			if pPlayer.getAIPromotionRoute() > 0:
				unit.setAIPromotionRoute(pPlayer.getAIPromotionRoute())
			else:
				unit.setAIPromotionRoute( gc.getGame().getSorenRandNum(3,'PromotionRoute') + 1  )
			
			#Power1.0�ȉ��Ȃ�1.0�ɂ���
			if unit.getPower()<1.0:
				unit.setPower(1.0)
			
		#���o�Ȃ�Ύ��@��^����
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(unit.getOwner()).isHuman():
			if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ZIKI'),True)
		
		#�h�q�u���Ń{�X���j�b�g�Ȃ�΋����P��ǉ�
		if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_PROTECTIVE')):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL1'),True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'),True)
		
		#�ɂƂ�̎u��������Ή͓����{�ɐ퓬�p�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_NITORILIST')):
			if gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_EASY') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'),True)
		
		#�䂬�u��������΂䂬�Ɋ�{����P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_YUGILIST')):
			if gc.getInfoTypeForString('UNIT_YUGI0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_YUGI6'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT1'),True)
		
		#�������u��������Η��D������
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_MARISALIST')):
			if gc.getInfoTypeForString('UNIT_MARISA0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_MARISA6'):
				#����MOD�ǋL�F�X�L����^���ă��x��+1
				unit.changeLevel(1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISALIST_PILLAGE'),True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1'),True)
				#����MOD�ǋL�����܂�
		
		#�A���X�u��������΁A��C�ɒ���
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_ALICELIST')):
			if gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHOKKATSU'),True)
		
		#�䂤���̎u��������΃X�y�V�����i���o�[���{�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_YUKALIST')):
			if gc.getInfoTypeForString('UNIT_YUKA1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKA6'):
				unit.setSpecialNumber(1)
		
		#�Ă�̎u��������΃X�L����^���ă��x���{�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_TEWILIST')):
			if gc.getInfoTypeForString('UNIT_TEWI0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_TEWI6'):
				unit.changeLevel(1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TEWI_SKILL1'),True)
		
		#��ւ̎u��������΃X�L����^���ă��x���{�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_ICHIRINLIST')):
			if gc.getInfoTypeForString('UNIT_ICHIRIN0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_ICHIRIN6'):
				unit.changeLevel(1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1'),True)

		#����MOD�ǋL������������
		
		#�����̎u��������΃X�L����^���ă��x���{�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_MIMALIST')):
			if gc.getInfoTypeForString('UNIT_MIMA0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_MIMA6'):
				unit.changeLevel(1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMA_SKILL1'),True)
		
		#�M�̎u��������΃X�L����^���ă��x���{�P
		if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_SEIGALIST')):
			if gc.getInfoTypeForString('UNIT_SEIGA0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_SEIGA6'):
				unit.changeLevel(1)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SEIGA_SKILL1'),True)
		
		#����MOD�ǋL���������܂�
		
		#AI�������[�h�̂Ƃ��ɒǉ����i��^����
		if gc.getPlayer(unit.getOwner()).isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
			if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				for i in range(len(TohoUnitList.CreateTohoAddPromoList[Functions.getHandicap()])):
					unit.setHasPromotion(gc.getInfoTypeForString((TohoUnitList.CreateTohoAddPromoList[Functions.getHandicap()])[i]),True)
			else:
				for i in range(len(TohoUnitList.CreateGeneAddPromoList[Functions.getHandicap()])):
					unit.setHasPromotion(gc.getInfoTypeForString((TohoUnitList.CreateGeneAddPromoList[Functions.getHandicap()])[i]),True)

		
		#���f�B�����ꂽ�ہA�w���҂����f�B�Ȃ�X�[����ɕω�
		if gc.getInfoTypeForString('UNIT_MEDICIN0') == unit.getUnitType():
			if gc.getPlayer(unit.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_MEDICINLIST')):
				if gc.getInfoTypeForString('UNIT_MEDICIN0') == unit.getUnitType():
					#�֋X�㌻���������j�b�g�̐����}�C�i�X�P�i�����͕ω������j
					pPlayer.setNumTohoUnit(pPlayer.getNumTohoUnit()-1)
				RevivalUnit = gc.getInfoTypeForString('UNIT_MEDICINwithSU0') + unit.getUnitType() - gc.getInfoTypeForString('UNIT_MEDICIN0')
				newUnit1 = gc.getPlayer(unit.getOwner()).initUnit(RevivalUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit1.convert(unit)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUSAN'),True)
				#if newUnit1.getUnitType() != gc.getInfoTypeForString('UNIT_MEDICINwithSU0'):
				#	newUnit1.finishMoves()
				unit = newUnit1
				#�������̓s����AUG�ɂ�郆�j�b�g�ϊ���SDK�ֈڐA
				
				iModExperience = 25
				if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
					iModExperience = 40
				if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
					iModExperience = 30
			
				iExperience = 0
				if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
					iExperience = iExperience + iModExperience
				
				iModExperience = 10
				if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
					iModExperience = 20
				if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
					iModExperience = 15
				
				if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
					iExperience = iExperience + iModExperience
				
				
				iModPower = 1.0;
				if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
					iModPower = iModPower + 1
				if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
					iModPower = iModPower + 1
					
				#AI�������[�h�ɂ��␳
				if gc.getPlayer(unit.getOwner()).isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
					iExperience = iExperience * TohoUnitList.CreateExpBonusList[Functions.getHandicap()] / 100
					iModPower = iModPower + 1
				
				#���o���[�h�ɂ��␳
				if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(unit.getOwner()).isHuman():
					iExperience = iExperience * 2
					iModPower = iModPower + 1
				
				unit.changeExperience(iExperience,-1,False,False,False)
				unit.setPower(iModPower)
		
		#�X�[��������f�B�����ꂽ�Ȃ�΁A�X�[����̏��i��ǉ�
		if gc.getInfoTypeForString('UNIT_MEDICINwithSU0') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_MEDICINwithSU6'):
			unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUSAN'),True)
		
		
		
		
		##### </written by F> #####
		
		if (not self.__LOG_UNITBUILD):
			return

	def onUnitBuilt(self, argsList):
		'Unit Completed'
		city = argsList[0]
		unit = argsList[1]
		player = PyPlayer(city.getOwner())
		pPlayer = gc.getPlayer(unit.getOwner())
		
		##### <written by F> #####
		#�����e�N�������Ă����Ԃō��ꂽ�������j�b�g�ɂ͒ǉ��̌o���l���^������
		
		if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			
			iModExperience = 25
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				iModExperience = 40
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				iModExperience = 30
		
			iExperience = 0
			if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
				iExperience = iExperience + iModExperience
			
			iModExperience = 10
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				iModExperience = 20
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				iModExperience = 15
			
			if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				iExperience = iExperience + iModExperience
			
			iModPower = 1.0;
			if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
				iModPower = iModPower + 1
			if gc.getTeam(unit.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				iModPower = iModPower + 1
			
			#AI�������[�h�ɂ��␳
			if gc.getPlayer(unit.getOwner()).isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
				iExperience = iExperience * TohoUnitList.CreateExpBonusList[Functions.getHandicap()] / 100
				iModPower = iModPower + 1
			
			#���o���[�h�ɂ��␳
			if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(unit.getOwner()).isHuman():
				iExperience = iExperience * 2
				iModPower = iModPower + 1
			
			unit.changeExperience(iExperience,-1,False,False,False)
			unit.setPower(iModPower)
		
		##### </written by F> #####
		
		#����MOD�ǋL����
		#���Ƃ̖���or���͗���ݒu���Ă���ꍇ�A���j�b�g���Y��2�{
		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_KODUTINOMARYOKU')):
			eTeam = gc.getTeam(pPlayer.getTeam())
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_STEAM_POWER')) == True:
				if unit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
					newUnit = pPlayer.initUnit(unit.getUnitType(), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.changeExperience(unit.getExperience(),-1,False,False,False)
		if city.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGIC_STORM')):
			if unit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				newUnit = pPlayer.initUnit(unit.getUnitType(), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.changeExperience(unit.getExperience(),-1,False,False,False)
		
		#�h�q�u���ŋ@�֏e�������Ɠs�s����1�E����1����
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_PROTECTIVE")):
			if unit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_MACHINE_GUN'):
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'),True)
				unit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'),True)
		
		CvAdvisorUtils.unitBuiltFeats(city, unit)

		if (not self.__LOG_UNITBUILD):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	def onUnitKilled(self, argsList):
		'Unit Killed'
		unit, iAttacker = argsList
		player = PyPlayer(unit.getOwner())
		pPlayer = gc.getPlayer(unit.getOwner())
		attacker = PyPlayer(iAttacker)
		iUnit = unit.getUnitType()
		
		##### <written by F> #####
		
		#���X�^�b�N�̃��j�b�g�ւ�Power��
		TohoUnitList_ = Functions.searchTeamTohoUnit(unit.plot(),unit)
		for pUnit in TohoUnitList_:
			pUnit.setPower(pUnit.getPower() + (0.005 / len(TohoUnitList_)))
		
		
		#�䂩���X�L���������HP����ւ��t���O�p�̔��肪����
		if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YUKARI_SKILL1')):
			if gc.getGame().getSorenRandNum(100, "YUKARI SKILL") < 25:
				unit.setSpecialNumber(1)
				if (not self.__LOG_UNITKILLED):
					return
				CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d' 
					%(player.getID(), player.getCivilizationName(), PyInfo.UnitInfo(unit.getUnitType()).getDescription(), attacker.getID()))
				return
			else:
				unit.setSpecialNumber(0)
		
		#�X�L����������񂪋߂��ɂ���Ώ����t�Ōo���l���l��
		RangeList = [ [-1,-1],[ 0,-1],[ 1,-1],[-1, 0], [ 0, 0],[ 1, 0],[-1, 1],[ 0, 1],[ 1, 1], ]
		if Functions.checkUnit(unit.getX(),unit.getY(),RangeList,gc.getInfoTypeForString('UNIT_RIN0'),gc.getInfoTypeForString('UNIT_RIN_CATMODE6')):
			pUnit = Functions.checkUnit(unit.getX(),unit.getY(),RangeList,gc.getInfoTypeForString('UNIT_RIN0'),gc.getInfoTypeForString('UNIT_RIN_CATMODE6'),1)
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RIN_SKILL1')) :
				if gc.getGame().getSorenRandNum(100, "orin skill") < 25:
					if pUnit.getSpecialNumber() < pUnit.getLevel():
						pUnit.changeExperience(1,-1,False,False,False)
						pUnit.setSpecialNumber(pUnit.getSpecialNumber()+1)
		
		
		#�]���r�t�F�A���[�̏��i�������Ă���΂��̏�ŕ�������\��
		if  unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY')) and gc.getGame().getSorenRandNum(100,"zombie fairy") < 15 :
			
			newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			#�s���I�������A�_���[�W
			newUnit1.finishMoves()
			iPlayer = unit.getOwner()
			newUnit1.changeDamage(99,iPlayer)
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY'),False)
		
		
		#���j�򂢂̏��i�������Ă���΂��̏�ŕ���
		elif (  unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI1')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI2')) or 
				unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI3')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI4')) or
				unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI5')) or unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI6'))  ):
			
			newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REVIVAL'),False)
			
			#�s���I�������A���i�ɂ��킹�ă_���[�W
			newUnit1.finishMoves()
			iPlayer = unit.getOwner()
			if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI6')):
				newUnit1.changeDamage(75,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI6'),False)
			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI5')):
				newUnit1.changeDamage(80,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI5'),False)
			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI4')):
				newUnit1.changeDamage(85,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI4'),False)
			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI3')):
				newUnit1.changeDamage(90,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI3'),False)
			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI2')):
				newUnit1.changeDamage(95,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI2'),False)
			elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI1')):
				newUnit1.changeDamage(99,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI1'),False)
			
		#���I�`�������Ă���ꍇ�A�̗�50���̏�Ԃŕ���
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DOREMY_YUMEOTI')):
			if gc.getGame().getSorenRandNum(100, "Yumeoti Hukkatu") < 25:
				newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				Functions.RevivalUnit(newUnit1,unit)
				iPlayer = unit.getOwner()
				newUnit1.changeDamage(50,iPlayer)
				newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DOREMY_YUMEOTI'),False)
		
			
		#�����̏��i�������Ă���΂��̏�ŕ����@����ɍs���\
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REVIVAL')):
			
			newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REVIVAL'),False)
		
		#���剻�������ł���΁A���ɖ߂�
		elif unit.getNumTransformTime() > 0 and gc.getInfoTypeForString("UNIT_SUIKA_BIG1") <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA_BIG6"):
			TransformUnit = unit.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA_BIG1") + gc.getInfoTypeForString("UNIT_SUIKA1")
			newUnit1 = gc.getPlayer(unit.getOwner()).initUnit(TransformUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			newUnit1.setDamage(99,unit.getOwner())
			newUnit1.finishMoves()
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),False )
		
		#����MOD�ǋL����
		#�����d���̎R�̕ϐg�I������
		
		elif unit.getNumTransformTime() > 0 and gc.getInfoTypeForString("UNIT_SUIKA_BIG1_YOUKAI") <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA_BIG6_YOUKAI"):
			TransformUnit = unit.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA_BIG1_YOUKAI") + gc.getInfoTypeForString("UNIT_SUIKA1_YOUKAI")
			newUnit1 = gc.getPlayer(unit.getOwner()).initUnit(TransformUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			newUnit1.setDamage(99,unit.getOwner())
			newUnit1.finishMoves()
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),False )
			newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),False )
		
		#���Ԍ��E�������Ă����Ԃł���΂��̂܂ܕ���
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_OUKAKEKKAI')):
			
			newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			#�Q�[�����x�ɂ��ω�
			SinraDelayTurn = 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				SinraDelayTurn = SinraDelayTurn * 150 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				SinraDelayTurn = SinraDelayTurn * 125 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				SinraDelayTurn = SinraDelayTurn * 75 / 100
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				SinraDelayTurn = SinraDelayTurn * 50 / 100
			newUnit1.setSinraDelayTurn(SinraDelayTurn)
			newUnit1.setNumTransformTime(unit.getNumTransformTime())

			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_OUKAKEKKAI'),False)
			newUnit1.finishMoves()
			newUnit1.changeDamage(99,unit.getOwner())
			
			CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(unit.getUnitType()).getDescription() + "&#12364;&#26862;&#32645;&#32080;&#30028;&#12391;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;","")

		
		#  #�X�y���J�[�h�ƃI�[�g�{���������Ă����Ԃł���΂��̂܂ܕ���
		#elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KESSIKEKKAI')) and unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLCARD')):
		
		#�������E��Power1.00�ȏオ����Ε���
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KESSIKEKKAI')) and unit.getPower() >= 1:
			newUnit1 = pPlayer.initUnit(iUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			Functions.RevivalUnit(newUnit1,unit)
			
			newUnit1.changeDamage(50,newUnit1.getOwner())
			#newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLCARD'),False)
			newUnit1.setPower(newUnit1.getPower()-1.00)
			newUnit1.finishMoves()
			
			CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(unit.getUnitType()).getDescription() + "&#12364;&#27770;&#27515;&#32080;&#30028;&#12391;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;","")
			
			#CvGameUtils.doprint("Auto Bomb Test End")
		
		
		
		#���g�⌶�e�������Ă��Ȃ���΁A���������	
		elif unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN')) == False and unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')) == False and  ( unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY')  ) :
			
			#�����L�������|���ꂽ�ꍇ�A��̉����Ă��̕����̎�s�ŕ�������
			#���ꂽ�̂������L�������ǂ����̃`�F�b�N�A���łɕ������j�b�g�̎w��
			RevivalUnit = None
			if unit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') and unit.getUnitType()%7 != 0:
				RevivalUnit = unit.getUnitType() - (unit.getUnitType()%7)
			#�ꕔ���j�b�g�̏ꍇ�͕������j�b�g��-7
			if gc.getInfoTypeForString('UNIT_KOISHI_FADE1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI_FADE6'):
				RevivalUnit = RevivalUnit - 7
			if gc.getInfoTypeForString('UNIT_RIN_CATMODE1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_RIN_CATMODE6'):
				RevivalUnit = RevivalUnit - 7
			if gc.getInfoTypeForString('UNIT_HAKUTAKUKEINE1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_HAKUTAKUKEINE6'):
				RevivalUnit = RevivalUnit - 21
			
			#���ꂽ�̂������L�����̏ꍇ�A���̕����̎�s�Ɍo���l�R�����A���i���Z�b�g�ŕ���
			if (RevivalUnit != None):
				CityList = player.getCityList()
				for pcity in CityList:
					if pcity.isCapital():
						city = pcity
				newUnit1 = pPlayer.initUnit(RevivalUnit, city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
				
				#�o���l�␳ �ꕔ������
				iExpHosei = 100
				if pPlayer.isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
					iExpHosei = TohoUnitList.ExpPenaList[Functions.getHandicap()]
				#	if unit.getbLoseByPlayer():
				#		iExpHosei = TohoUnitList.ExpPenaList[Functions.getHandicap()]
				#	else:
				#		iExpHosei = TohoUnitList.ExpPenaList[Functions.getHandicap()]

				#������̃X�L�������Ȃ�30���J�b�g
				if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHEN_SKILL1')):
					iExpHosei = iExpHosei - 30
					
				#���@�������50%�J�b�g
				if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZIKI')):
					iExpHosei = iExpHosei - 50
					
				#�Ă񂱃X�L���������100%�J�b�g
				if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TENSHI_SKILL1')):
					iExpHosei = iExpHosei - 100
				
				#�ǂ�݃X�L���������100%�J�b�g
				if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DOREMY_SKILL1')):
					iExpHosei = iExpHosei - 100
					
				if iExpHosei < 0:
					iExpHosei = 0
					
					
				ExpPena = unit.getExperience() *30 /100 * iExpHosei /100
				newExperience = unit.getExperience() - ExpPena
				newUnit1.changeExperience(newExperience,-1,false,false,false)
				#CvGameUtils.doprint("newExperience:%i" %newExperience)
				
				#�֋X�㌻���������j�b�g�̐����}�C�i�X�P�i�����͕ω������j
				pPlayer.setNumTohoUnit(pPlayer.getNumTohoUnit()-1)
				
				#��������̃��j�b�g�ɂ̓f�B���C���i������
				if pPlayer.isHuman():
					newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_4'),True)
					newUnit1.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
				elif  pPlayer.isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
					newUnit1.setHasPromotion(gc.getInfoTypeForString(TohoUnitList.RevivalPromoList[Functions.getHandicap()]),True)
					newUnit1.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
				else:
					newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RETURN_DELAY1_5'),True)
					newUnit1.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
				
				#�X�L���������Ă����玝���z�������x���{�P
				#����MOD�ǋL�F��{�I�Ɉ����p����AI���̂�
				#�������u���Y���ォ�烆�j�b�g�X�L�����L�̌ŗL�u���v���������g�̓������j�b�g���o���Ă���ꍇ�́A����I�Ƀv���C���[���ł������p����
				iNumSkill = gc.getInfoTypeForString('PROMOTION_SAGUME_SKILL1') - gc.getInfoTypeForString('PROMOTION_SANAE_SKILL1') + 1
				if pPlayer.isHuman() == False:
					for i in range(iNumSkill):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SANAE_SKILL1') + i):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SANAE_SKILL1') + i,True)
							newUnit1.changeLevel(1)
				if pPlayer.isHuman() == True:
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_TEWILIST')):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TEWI_SKILL1')):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TEWI_SKILL1'),True)
					#		newUnit1.changeLevel(1)
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ICHIRINLIST')):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1')):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1'),True)
					#		newUnit1.changeLevel(1)
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_MIMALIST')):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMA_SKILL1')):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMA_SKILL1'),True)
					#		newUnit1.changeLevel(1)
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SEIGALIST')):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SEIGA_SKILL1')):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SEIGA_SKILL1'),True)
					#		newUnit1.changeLevel(1)
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_MARISALIST')):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1')):
							newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1'),True)
					#		newUnit1.changeLevel(1)
				
				#���̉ŃV�X�e���ɂ�鋭���������p��
				for i in range(3):
					newUnit1.setNumPowerUp(i,unit.getNumPowerUp(i));
				
				
				#���������X�L�������œ|���ꂽ�ꍇ�A���т��������c��
				#����MOD�ǋL�F����̓v���C���[���̂݁BAI���͔������Ȃ��悤��
				#�d���̎R�̏ꍇ���Y�ꂸ��
				if pPlayer.isHuman():
					if gc.getInfoTypeForString('UNIT_SUIKA1') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_SUIKA6'):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUIKA_SKILL1')):
							RevivalUnit = unit.getUnitType() - gc.getInfoTypeForString('UNIT_SUIKA1') + gc.getInfoTypeForString('UNIT_SUIKA_SMALL1')
							for i in range(3):
								newUnit = pPlayer.initUnit(RevivalUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE1'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE2'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE3'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'),True)
					
					elif gc.getInfoTypeForString('UNIT_SUIKA1_YOUKAI') <= unit.getUnitType() and unit.getUnitType() <= gc.getInfoTypeForString('UNIT_SUIKA6_YOUKAI'):
						if unit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUIKA_SKILL1')):
							RevivalUnit = unit.getUnitType() - gc.getInfoTypeForString('UNIT_SUIKA1_YOUKAI') + gc.getInfoTypeForString('UNIT_SUIKA_SMALL1_YOUKAI')
							for i in range(3):
								newUnit = pPlayer.initUnit(RevivalUnit, unit.getX(), unit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE1'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE2'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_BARRAGE3'),True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'),True)
								
				#�����J�E���g��ǉ��@
				newUnit1.setPower(unit.getPower() - 0.2)
				if newUnit1.getPower() < 1.0:
					newUnit1.setPower(1.0)
				
				newUnit1.setNumLoseCount( unit.getNumLoseCount()+1 )
		
		
			
		##### </written by F> #####
		if (not self.__LOG_UNITKILLED):
			return
		CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d'
			%(player.getID(), player.getCivilizationName(), PyInfo.UnitInfo(unit.getUnitType()).getDescription(), attacker.getID()))

	def onUnitLost(self, argsList):
		'Unit Lost'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		
		##### <written by F> #####
		
		#���@�D���|���ꂽ�Ƃ��͎�s�Ō������Ƃ��ĕ���
		if unit.getUnitType() == gc.getInfoTypeForString('UNIT_SEIRENSEN'):
			pCity = gc.getPlayer(unit.getOwner()).getCapitalCity()
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI1'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI2'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI3'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI4'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI5'),1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI6'),1)
			
		##### </written by F> #####
		
		if (not self.__LOG_UNITLOST):
			return
		CvUtil.pyPrint('%s was lost by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	#�����������E����MOD�ǋL
	#onDelayedDeath�̏���
	#���ߗ��āE�C�m���̏�����spellinfo.py�݂̂ł��̂͐F�X�ƕs���艻����\�������邽�߁A�n�`�����݂̂�����ɓ�����
	def onDelayedDeath(self, argsList):
		x, y = argsList
		CvGameUtils.doprint("onDelayedDeath: (%d, %d)" %(x,y))
		if Functions.isPlot(x,y):
			pPlot = CyMap().plot(x, y)
			if pPlot.getOriginalTerrain() == 512:
				pPlot.setTerrainType(gc.getInfoTypeForString("TERRAIN_PLAINS"),True,True)
			if pPlot.getOriginalTerrain() == 513:
				pPlot.setPlotType(PlotTypes.PLOT_OCEAN,True,True)
		
	def onUnitPromoted(self, argsList):
		'Unit Promoted'
		pUnit, iPromotion = argsList
		player = PyPlayer(pUnit.getOwner())
		
		##### <written by F> #####
		#�b�`���x���p�̏��i���l������ƁA�����ɏ������Ăb�`���x�����グ��
		
		if iPromotion == gc.getInfoTypeForString('PROMOTION_CARD_ATTACK_LEVEL_UP'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CARD_ATTACK_LEVEL_UP'),False)
			pUnit.setNumAcquisSpellPromotion(pUnit.getNumAcquisSpellPromotion()+1)
		
		#�X�y���J�[�h�̏��i���l��������APower��0.5�񕜂����ď���
		if iPromotion == gc.getInfoTypeForString('PROMOTION_SPELLCARD'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELLCARD'),False)
			pUnit.setPower( pUnit.getPower() + 0.5 )
		
		
		#�}���`�␳����Ex��Phan���擾�����烌�x���A�b�v
		#if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
		#	if iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_EXTRA') or iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM'):
		#		pUnit.changeLevel(1)
		
		#Hard�`Phan���Ƃ����烌�x���{�P
		if ( iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_EXTRA') or iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM') or 
			 iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_HARD') or iPromotion == gc.getInfoTypeForString('PROMOTION_MODE_LUNATIC') ):
			pUnit.changeLevel(1)
		
		##### </written by F> #####
		if (not self.__LOG_UNITPROMOTED):
			return
		CvUtil.pyPrint('Unit Promotion Event: %s - %s' %(player.getCivilizationName(), pUnit.getName(),))

	def onUnitSelected(self, argsList):
		'Unit Selected'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITSELECTED):
			return
		CvUtil.pyPrint('%s was selected by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))

	def onUnitRename(self, argsList):
		'Unit is renamed'
		pUnit = argsList[0]
		if (pUnit.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditUnitNameBegin(pUnit)

	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
		pPlot = CyMap().plot(iPlotX, iPlotY)

		#����MOD�ǋL������������
		#���j�b�g�F�����L�����N�^�[�X�L���������Ă���ꍇ�A���D�ő̗͉�

		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOSHIKA_SKILL1')):
			pUnit.changeDamage(-25,pUnit.getOwner())
		
		#����MOD�ǋL���������܂�

		if (not self.__LOG_UNITPILLAGE):
			return
		CvUtil.pyPrint("Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
			%(iOwner, PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(), iImprovement, iRoute, iPlotX, iPlotY))

	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList

		iX = pUnit.getX()
		iY = pUnit.getY()
		pPlot = CyMap().plot(iX, iY)
		pCity = pPlot.getPlotCity()

	def onUnitGifted(self, argsList):
		'Unit is gifted from one player to another'
		pUnit, iGiftingPlayer, pPlotLocation = argsList

	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList

	def onGoodyReceived(self, argsList):
		'Goody received'
		iPlayer, pPlot, pUnit, iGoodyType = argsList
		if (not self.__LOG_GOODYRECEIVED):
			return
		CvUtil.pyPrint('%s received a goody' %(gc.getPlayer(iPlayer).getCivilizationDescription(0)),)

	def onGreatPersonBorn(self, argsList):
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		if pUnit.isNone() or pCity.isNone():
			return
		if (not self.__LOG_GREATPERSON):
		
		#����MOD�ǋL������������

		#����΂ݎu���̃n�Q����������

			pPlayer = gc.getPlayer(iPlayer)
			iCiv = pPlayer.getCivilizationType()
			eTeam = gc.getTeam(pPlayer.getTeam())
			if pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_PROPHET"):
				if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_ALCHOL")):
					#�Q�[�����x�ɂ��ω�
					if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
						pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()/2+1)
					if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
						pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()/2+1)
					if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
						pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()/2+1)
					if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
						pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()/2+1)
					if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
						pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()/2)
				
				#�_��_�������A�̐l�������ɒǉ��̐_���in�n�Q�����₪������
				
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
					CityList = player.getCityList()
					for pcity in CityList:
						if pcity.isCapital():
							city = pcity
					#�\�������@�̗p���ɍX�ɒǉ��̐_���
					if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT')) == gc.getInfoTypeForString('CIVIC_ZYUUSHICHIZYO_KENPOU')) == True:
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					#�ŏI�ŗL�e�N�擾�ōX�ɒǉ��̐_���
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HOSIHURU_SHINREIBYOU')) == True:
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
			#�_��_�������A�̐l�������ɒǉ��̐_���in�ʏ펞
			if (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_ARTIST")) or (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SCIENTIST")) or (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_MERCHANT")) or (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_ENGINEER")) or (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_GREAT_SPY")):
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
					CityList = player.getCityList()
					for pcity in CityList:
						if pcity.isCapital():
							city = pcity
					#�\�������@�̗p���ɍX�ɒǉ��̐_���
					if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT')) == gc.getInfoTypeForString('CIVIC_ZYUUSHICHIZYO_KENPOU')) == True:
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					#�ŏI�ŗL�e�N�擾�ōX�ɒǉ��̐_���
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HOSIHURU_SHINREIBYOU')) == True:
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		

		#����MOD�ǋL���������܂�

			return
		CvUtil.pyPrint('A %s was born for %s in %s' %(pUnit.getName(), player.getCivilizationName(), pCity.getName()))

	def onTechAcquired(self, argsList):
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object

		# Show tech splash when applicable
		if (iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash()):
			if (gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode()):
				if ((not gc.getGame().isNetworkMultiPlayer()) and (iPlayer == gc.getGame().getActivePlayer())):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iTechType)
					popupInfo.setText(u"showTechSplash")
					popupInfo.addPopup(iPlayer)
		
		##### <written by F> #####
		#�����e�N���l�����ꂽ�瓌�����j�b�g�g��ǉ�����
		
		pPlayer = gc.getPlayer(iPlayer)
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and pPlayer.isHuman():
			if iTechType == gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2'):
				pPlayer.setNumTohoUnitLimit(pPlayer.getNumTohoUnitLimit()+2)
			if iTechType == gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3'):
				pPlayer.setNumTohoUnitLimit(pPlayer.getNumTohoUnitLimit()+2)
		else:
			if iTechType == gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2'):
				pPlayer.setNumTohoUnitLimit(pPlayer.getNumTohoUnitLimit()+1)
			if iTechType == gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3'):
				pPlayer.setNumTohoUnitLimit(pPlayer.getNumTohoUnitLimit()+1)
			
		
		#�������̔�����V�̓Ђ��������ꂽ��A�������������������݈̂̐l�o�[���Z�b�g
		if iTechType == gc.getInfoTypeForString('TECH_BISHAMON_TIGER'):
			pPlayer.resetGreatPeopleThreshold()
		
		#�������̖��@�̋������������ꂽ��A�S�s�s�̐l������
		#����MOD�ǋL�c�����l��10����5�֌���
		if iTechType == gc.getInfoTypeForString('TECH_TEACHING_OF_MEIREN'):
			py = PyPlayer(iPlayer)
			for pPyCity in py.getCityList():
				pCity = pPlayer.getCity(pPyCity.getID())
				pCity.changePopulation(5)
		
		#����MOD�ǋL������������
		
		#�_��_�ŏI�ŗL�e�N���擾�����ꍇ�A�S��ނ̈̐l�l��
		if iTechType == gc.getInfoTypeForString('TECH_HOSIHURU_SHINREIBYOU'):
			py = PyPlayer(iPlayer)
			CityList = py.getCityList()
			for pcity in CityList:
				if pcity.isCapital():
					city = pcity
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARTIST'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SCIENTIST'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCHANT'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ENGINEER'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GREAT_GENERAL'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GREAT_SPY'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addImmediateMessage("&#32854;&#20154;&#23436;&#20840;&#24489;&#27963;&#12398;&#22577;&#12434;&#32862;&#12365;&#12388;&#12369;&#12289;&#19990;&#30028;&#12398;&#21517;&#31435;&#12383;&#12427;&#20553;&#20154;&#12364;&#31070;&#38666;&#24287;&#12434;&#30446;&#25351;&#12375;&#32154;&#12293;&#12392;&#24187;&#24819;&#20837;&#12426;&#12375;&#12390;&#12356;&#12414;&#12377;&#65281;","")
		
		#�M�L���擾�����ꍇ�A�~�G���ڏ���
		if iTechType == gc.getInfoTypeForString('TECH_WRITING'):
			py = PyPlayer(iPlayer)
			for pPyCity in py.getCityList():
				pCity = pPlayer.getCity(pPyCity.getID())
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_MIERUME')) == True:
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MIERUME'),0)
		
		#����or����or�{�Yor�_���`�̂����ꂩ���擾�����ꍇ�A��r�����w����
		if iTechType == gc.getInfoTypeForString('TECH_BRONZE_WORKING') or iTechType == gc.getInfoTypeForString('TECH_POTTERY') or iTechType == gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY') or iTechType == gc.getInfoTypeForString('TECH_MYSTICISM'):
			py = PyPlayer(iPlayer)
			for pPyCity in py.getCityList():
				pCity = pPlayer.getCity(pPyCity.getID())
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_HIKAKUBUTURIGAKU')) == True:
					pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HIKAKUBUTURIGAKU'),0)
		
		#����MOD�ǋL���������܂�
		
		##### </written by F> #####
		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was finished by Team %d'
			%(PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam))

	def onTechSelected(self, argsList):
		'Tech Selected'
		iTechType, iPlayer = argsList

		chiPlayer, chiProgress = self.ChireidenOverflow

		# �v�[�����ꂽ�����͂������āA���ꂪ�����̂��̂ł���Ȃ�A���I�񂾋Z�p�ɂ�����
		if(iPlayer == chiPlayer and chiProgress > 0):
			pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
			pTeam.changeResearchProgress(iTechType,chiProgress,iPlayer)
			self.ChireidenOverflow = (-1, 0)
			
		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was selected by Player %d' %(PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer))

	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList
		player = PyPlayer(iFounder)

		iCityId = gc.getGame().getHolyCity(iReligion).getID()
		if (gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode()):
			if ((not gc.getGame().isNetworkMultiPlayer()) and (iFounder == gc.getGame().getActivePlayer())):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iReligion)
				popupInfo.setData2(iCityId)
				popupInfo.setData3(1)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iFounder)

		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getReligionInfo(iReligion).getDescription()))

	def onReligionSpread(self, argsList):
		'Religion Has Spread to a City'
		iReligion, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))

	def onReligionRemove(self, argsList):
		'Religion Has been removed from a City'
		iReligion, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))

	def onCorporationFounded(self, argsList):
		'Corporation Founded'
		iCorporation, iFounder = argsList
		player = PyPlayer(iFounder)

		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getCorporationInfo(iCorporation).getDescription()))

	def onCorporationSpread(self, argsList):
		'Corporation Has Spread to a City'
		iCorporation, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getCorporationInfo(iCorporation).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))

	def onCorporationRemove(self, argsList):
		'Corporation Has been removed from a City'
		iCorporation, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))

	def onGoldenAge(self, argsList):
		'Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_GOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s has begun a golden age'
			%(iPlayer, player.getCivilizationName()))

	def onEndGoldenAge(self, argsList):
		'End Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_ENDGOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s golden age has ended'
			%(iPlayer, player.getCivilizationName()))

	def onChangeWar(self, argsList):
		'War Status Changes'
		bIsWar = argsList[0]
		iTeam = argsList[1]
		iRivalTeam = argsList[2]
		if (not self.__LOG_WARPEACE):
			return
		if (bIsWar):
			strStatus = "declared war"
		else:
			strStatus = "declared peace"
		CvUtil.pyPrint('Team %d has %s on Team %d'
			%(iTeam, strStatus, iRivalTeam))

	def onChat(self, argsList):
		'Chat Message Event'
		chatMessage = "%s" %(argsList[0],)

	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayerID = argsList[0]
		bNewValue = argsList[1]
		CvUtil.pyPrint("Player %d's alive status set to: %d" %(iPlayerID, int(bNewValue)))
		
		#����MOD�ǋL����
		#FfH2���ڐA�B�w���ҖŖS�����b�Z�[�W
		if bNewValue == False:
			pPlayer = gc.getPlayer(iPlayerID)
			#���b�Z�[�W��AI���Ɍ��肷��
			if pPlayer.isHuman() == False:
				#�g����
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_REMILIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_REMILIA",()),'art/interface/popups/remiria_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FLAN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_FLAN",()),'art/interface/popups/flandore_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SAKUYA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SAKUYA",()),'art/interface/popups/sakuya_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MEIRIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MEIRIN",()),'art/interface/popups/meirin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOA",()),'art/interface/popups/koa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LITTLE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LITTLE",()),'art/interface/popups/little_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_PATCHOULI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_PATCHOULI",()),'art/interface/popups/patchouli_defeated.dds')
				#���ʘO
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YOUMU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YOUMU",()),'art/interface/popups/youmu_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKARI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YUKARI",()),'art/interface/popups/yukari_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUYUKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YUYUKO",()),'art/interface/popups/yuyuko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RAN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RAN",()),'art/interface/popups/ran_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CHEN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_CHEN",()),'art/interface/popups/chen_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LILYW'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LILYW",()),'art/interface/popups/lilyw_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LILYB'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LILYB",()),'art/interface/popups/lilyb_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LUNASA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LUNASA",()),'art/interface/popups/lunasa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MERLIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MERLIN",()),'art/interface/popups/marlin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LYRICA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LYRICA",()),'art/interface/popups/lyrica_defeated.dds')
				#�i����
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_REISEN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_REISEN",()),'art/interface/popups/reisen_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TEWI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_TEWI",()),'art/interface/popups/tewi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KAGUYA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KAGUYA",()),'art/interface/popups/kaguya_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EIRIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_EIRIN",()),'art/interface/popups/eirin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MEDICIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MEDICIN",()),'art/interface/popups/medicine_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WATAHIME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_WATAHIME",()),'art/interface/popups/toyohime_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YORIHIME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YORIHIME",()),'art/interface/popups/yorihime_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_REISEN2'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_REISEN2",()),'art/interface/popups/reisen2_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KAGEROU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KAGEROU",()),'art/interface/popups/kagerou_defeated.dds')
				#�d���̎R
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_IKU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_IKU",()),'art/interface/popups/iku_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_NITORI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_NITORI",()),'art/interface/popups/nitori_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SANAE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SANAE",()),'art/interface/popups/sanae_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KANAKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KANAKO",()),'art/interface/popups/kanako_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MINORIKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MINORIKO",()),'art/interface/popups/minoriko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SIZUHA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SIZUHA",()),'art/interface/popups/sizuha_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AYA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_AYA",()),'art/interface/popups/aya_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MOMIZI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MOMIZI",()),'art/interface/popups/momizi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HATATE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_HATATE",()),'art/interface/popups/hatate_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUWAKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SUWAKO",()),'art/interface/popups/suwako_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TENSHI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_TENSHI",()),'art/interface/popups/tenshi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HINA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_HINA",()),'art/interface/popups/hina_defeated.dds')
				#�n��a
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_PARSEE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_PARSEE",()),'art/interface/popups/parsee_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUGI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YUGI",()),'art/interface/popups/yugi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SATORI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SATORI",()),'art/interface/popups/satori_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RIN",()),'art/interface/popups/rin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_UTSUHO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_UTSUHO",()),'art/interface/popups/utsuho_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOISHI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOISHI",()),'art/interface/popups/koishi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KISUME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KISUME",()),'art/interface/popups/kisume_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YAMAME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YAMAME",()),'art/interface/popups/yamame_defeated.dds')
				#���@�D
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_NAZRIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_NAZRIN",()),'art/interface/popups/nazrin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ICHIRIN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_ICHIRIN",()),'art/interface/popups/ichirin_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MINAMITSU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MINAMITSU",()),'art/interface/popups/murasa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SYOU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SYOU",()),'art/interface/popups/syou_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BYAKUREN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_BYAKUREN",()),'art/interface/popups/byakuren_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_NUE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_NUE",()),'art/interface/popups/nue_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KYOUKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KYOUKO",()),'art/interface/popups/kyouko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAMIZOU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MAMIZOU",()),'art/interface/popups/mamizou_defeated.dds')
				#�X���A��
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RUMIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RUMIA",()),'art/interface/popups/rumia_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LETTY'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LETTY",()),'art/interface/popups/letty_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WRIGGLE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_WRIGGLE",()),'art/interface/popups/wriggle_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MYSTIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MYSTIA",()),'art/interface/popups/mystia_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CIRNO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_CIRNO",()),'art/interface/popups/cirno_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DAIYOUSEI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_DAIYOUSEI",()),'art/interface/popups/daiyousei_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOGASA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOGASA",()),'art/interface/popups/kogasa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LUNA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LUNA",()),'art/interface/popups/luna_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_STAR'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_STAR",()),'art/interface/popups/star_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUNNY'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SUNNY",()),'art/interface/popups/sunny_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WAKASAGIHIME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_WAKASAGIHIME",()),'art/interface/popups/wakasagihime_defeated.dds')
				#����_��
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_REIMU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_REIMU",()),'art/interface/popups/reimu_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KYUUREIMU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KYUUREIMU",()),'art/interface/popups/kyuureimu_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TOKIKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_TOKIKO",()),'art/interface/popups/tokiko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RINNOSUKE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RINNOSUKE",()),'art/interface/popups/rinnosuke_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ALICE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_ALICE",()),'art/interface/popups/alice_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MARISA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MARISA",()),'art/interface/popups/marisa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUIKA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SUIKA",()),'art/interface/popups/suika_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MIMA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MIMA",()),'art/interface/popups/mima_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SHINKI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SHINKI",()),'art/interface/popups/shinki_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KASEN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KASEN",()),'art/interface/popups/kasen_defeated.dds')
				#�l�Ԃ̗�
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YUKA",()),'art/interface/popups/yuka_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EIKI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_EIKI",()),'art/interface/popups/eiki_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MERRY'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MERRY",()),'art/interface/popups/maribel_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RENKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RENKO",()),'art/interface/popups/renko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AKYU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_AKYU",()),'art/interface/popups/akyu_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEINE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KEINE",()),'art/interface/popups/keine_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HAKUTAKU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_HAKUTAKU",()),'art/interface/popups/hakutaku_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MOKOU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MOKOU",()),'art/interface/popups/mokou_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOMACHI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOMACHI",()),'art/interface/popups/komachi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOSUZU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOSUZU",()),'art/interface/popups/kosuzu_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SEKIBANKI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SEKIBANKI",()),'art/interface/popups/sekibanki_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUMIREKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SUMIREKO",()),'art/interface/popups/sumireko_defeated.dds')
				#�_��_
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YOSHIKA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YOSHIKA",()),'art/interface/popups/yoshika_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SEIGA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SEIGA",()),'art/interface/popups/seiga_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TOJIKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_TOJIKO",()),'art/interface/popups/toziko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FUTO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_FUTO",()),'art/interface/popups/futo_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MIMIMIKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_MIMIMIKO",()),'art/interface/popups/miko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CHIYURI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_CHIYURI",()),'art/interface/popups/chiyuri_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUMEMI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YUMEMI",()),'art/interface/popups/yumemi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOKORO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KOKORO",()),'art/interface/popups/kokoro_defeated.dds')
				#�P�j��
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YATUHASHI'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_YATUHASHI",()),'art/interface/popups/yatsuhashi_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BENBEN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_BENBEN",()),'art/interface/popups/benben_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SEIJA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SEIJA",()),'art/interface/popups/seija_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SHINMYOUMARU'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SHINMYOUMARU",()),'art/interface/popups/shinmyoumaru_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RAIKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RAIKO",()),'art/interface/popups/raiko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KYUUMARISA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_KYUUMARISA",()),'art/interface/popups/kyuumarisa_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_LOLISE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_LOLISE",()),'art/interface/popups/lolise_defeated.dds')
				#����`�i����A���̓s�j
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SEIRAN'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SEIRAN",()),'art/interface/popups/seiran_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RINGO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_RINGO",()),'art/interface/popups/ringo_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DOREMY'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_DOREMY",()),'art/interface/popups/doremy_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SAGUME'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_SAGUME",()),'art/interface/popups/sagume_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CLOWNPIECE'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_CLOWNPIECE",()),'art/interface/popups/clownpiece_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_JUNKO'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_JUNKO",()),'art/interface/popups/junko_defeated.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HECATIA'):
					cf.addPopup(CyTranslator().getText("TXT_KEY_POPUP_DEFEATED_HECATIA",()),'art/interface/popups/hecatia_defeated.dds')

	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList

	def onPlayerGoldTrade(self, argsList):
		'Player Trades gold to another player'
		iFromPlayer, iToPlayer, iGoldAmount = argsList

#����MOD�ǋL����
# BULL events
#�Љ�x�n�̒ǉ����������͈Ȍ�S��������ɈڐA
	def onPlayerRevolution(self, argsList):
		ePlayer, iAnarchyTurns, leOldCivics, leNewCivics = argsList
		civics = []
		py = PyPlayer(ePlayer)
		pPlayer = gc.getPlayer(ePlayer)
		
		for eOldCivic, eNewCivic in zip(leOldCivics, leNewCivics):
			if eOldCivic != eNewCivic:
				for pPyCity in py.getCityList():
					pCity = pPlayer.getCity(pPyCity.getID())
					pCapital = gc.getPlayer(pCity.getOwner()).getCapitalCity()
					#�M�֘A�ǉ�
					if eNewCivic == gc.getInfoTypeForString('CIVIC_FAITH_SHINTO'):
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORII'),1)
					if eNewCivic == gc.getInfoTypeForString('CIVIC_FAITH_BUDDHISM'):
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUTUZOU'),1)
						if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_SYOGYOU_MUJOU_A")) == True:
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_A'),0)
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_B'),1)
					if eNewCivic == gc.getInfoTypeForString('CIVIC_FAITH_TAOISM'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SENTAN'),1)
						if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_ONMYOURYOU2")) == True:
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU1'),1)
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2'),0)
					if eNewCivic == gc.getInfoTypeForString('CIVIC_FAITH_CTHULHU'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CTHULHU'),1)
					#�M�֘A���Z�b�g
					if eOldCivic == gc.getInfoTypeForString('CIVIC_FAITH_SHINTO'):
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORII'),0)
					if eOldCivic == gc.getInfoTypeForString('CIVIC_FAITH_BUDDHISM'):
						pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUTUZOU'),0)
						if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_SYOGYOU_MUJOU_B")) == True:
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_A'),1)
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_B'),0)
					if eOldCivic == gc.getInfoTypeForString('CIVIC_FAITH_TAOISM'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SENTAN'),0)
						if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_ONMYOURYOU1")) == True:
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU1'),0)
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2'),1)
					if eOldCivic == gc.getInfoTypeForString('CIVIC_FAITH_CTHULHU'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CTHULHU'),0)
					#�J���u������
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_LABORLIST')):
					#�J���u���֘A�ǉ�
						if eNewCivic == gc.getInfoTypeForString('CIVIC_TRIBALISM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),1)
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_2'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_SERFDOM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_CASTE_SYSTEM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),1)
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_2'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_EMANCIPATION'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_SISHANOOUKOKU'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),1)
						if eNewCivic == gc.getInfoTypeForString('CIVIC_HAKUREISIKI'):
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_HAKUREISIKI'),1)
					#�J���u���֘A���Z�b�g
						if eOldCivic == gc.getInfoTypeForString('CIVIC_TRIBALISM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),0)
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_2'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_SERFDOM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_CASTE_SYSTEM'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),0)
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_2'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_EMANCIPATION'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_SISHANOOUKOKU'):
							pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),0)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_HAKUREISIKI'):
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_HAKUREISIKI'),0)
					#���̑�
					#��҂̊y��
					if eNewCivic == gc.getInfoTypeForString('CIVIC_JAKUSYANORAKUEN'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_JAKUSYANORAKUEN'),1)
					if eOldCivic == gc.getInfoTypeForString('CIVIC_JAKUSYANORAKUEN'):
						pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_JAKUSYANORAKUEN'),0)
					#�w���Ґ��ׂ������ȍ~�ɖ��������̗p�����ꍇ
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SEIJALIST')):
						if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_ANCIENT'):
							if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_CLASSICAL'):
								if eNewCivic == gc.getInfoTypeForString('CIVIC_BARBARISM'):
									pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AMANOJAKU'),1)
								if eOldCivic == gc.getInfoTypeForString('CIVIC_BARBARISM'):
									pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AMANOJAKU'),0)
					#�w���҃����X���z�ꐧ���̗p�����ꍇ�A��s�Ɏ���ł����H�ݒu
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_LOLISELIST')):
						if eNewCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SINDEKURERU'),1)
						if eOldCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
							pCapital.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SINDEKURERU'),0)
				civics.append(gc.getCivicInfo(eNewCivic).getDescription())
		#BugUtil.debug("Revolution for %s, %d turns: %s", gc.getPlayer(ePlayer).getName(), iAnarchyTurns, ", ".join(civics))

#����MOD�ǋL���������܂�

	def onCityBuilt(self, argsList):
		'City Built'
		city = argsList[0]
		pPlayer = gc.getPlayer(city.getOwner())
		
		##### <written by F> #####
		
		#���o���[�h�ł����
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MUSOU')) and gc.getPlayer(city.getOwner()).isHuman():
			#if city.isCapital():
				#newUnit1 = gc.getPlayer(city.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_WARRIOR'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				#newUnit1 = gc.getPlayer(city.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_WARRIOR'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MUSOU_MODE'),1)
			

		#����MOD�ǋL����
		#�l�Ԃ̗���AI�̏ꍇ�Ɍ���A��s�ɑS�s�s�r�[�J�[-10%�������ݒu
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if pPlayer.isHuman() == False:
				if city.isCapital():
					city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AI_NINGENNOSATO'),1)

		#����̎u�����������ꍇ�A�s�s���ݎ��Ɍ�������ǉ�
		
		#�����[
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_MERRYLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MIERUME'),1)
		
		#�����₳��
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_SAKUYALIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIDOCHOUNOSHIKI'),1)
		
		#�p�`�F
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_PATCHOULIST')):
			if city.isCapital():
				iAge = gc.getPlayer(city.getOwner()).getCurrentEra()
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_PATCHOULI_BOOK'),1)
				city.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_PATCHOULI_BOOK'),1, (iAge+1) * 2 )
		
		#���ǂ�
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_REISENLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TELEMESMELISM'),1)
		
		#�Ă�
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_TENSHILIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TENSHINOTANOSHIMI'),1)
		
		#���������
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_AKYULIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HIEDARYUUKIOKUJUTU'),1)
		
		#����MOD�ǋL������������
		
		#������
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KISUMELIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISUMENOOKE'),1)
		#������
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_STARLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HOSHINOHIKARI'),1)
		#���傤�������
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KYOUKOLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_YAMABIKO'),1)
		
		#�j����
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_TOJIKOLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_IMOKONOHAKA'),1)
		
		#����
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KOSUZULIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUZUNAAN'),1)
		
		#�����
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_CHIYURILIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_YUMEDOKEI'),1)
		
		#����
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_YUMEMILIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HIKAKUBUTURIGAKU'),1)
		
		#�����낿���
		#�ŗL�u���̌��͈�V�ɔ�������
		#if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_KOKOROLIST')):
		#	if city.isCapital():
		#		city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KOUYOU'),1)
		
		#�����͓s�s���݂��Ƃɑ�����������i�K�ځ�����-50%������
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_YATUHASHILIST')):
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ECHO_CHAMBER'),1)
			#������������i�K�ڏ���
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				city.changeCulture(city.getOwner(),30,True)
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				city.changeCulture(city.getOwner(),15,True)
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				city.changeCulture(city.getOwner(),10,True)
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				city.changeCulture(city.getOwner(),5,True)
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				city.changeCulture(city.getOwner(),5,True)
		
		#���[���͎�s���݂Ɠ����ɖ����̒T���ƃQ�b�g
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SEIRANLIST')):
			if city.isCapital():
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EXPLORER'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		#��񂲂����̎�s�^�C���͐H��+1
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_RINGOLIST')):
			if city.isCapital():
				#�������̏ꍇ�͏��O
				pPlot = city.plot()
				if pPlot.getBonusType(pPlayer.getTeam()) == -1:
					gc.getGame().setPlotExtraYield(city.getX(),city.getY(),0,1)
		
		#�ǂ��
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOREMYLIST')):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_THISWOMAN'),1)
		
		#����΂ݎu���̍��𖳏��{�[�i�X
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_ALCHOL")):
			iStateReligion = pPlayer.getStateReligion()
			if iStateReligion > -1:
				city.setHasReligion(iStateReligion,True,True,True)
		
		#�g���u���͌ÓT����ȍ~�Ől��2�X�^�[�g
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_EXPANSIVE")):
			if not pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
				city.changePopulation(1)
		
		#�W���u���̏���
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_CENTRALIZATION")):
			if city.isCapital():
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CENTRALIZATION'),1)
		#�_�����̗p���Ă���ꍇ�A�s�s�ɒ�����������
		if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_SHINTO')) == True:
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORII'),1)
		#�������̗p���Ă���ꍇ�A�s�s�ɕ�����������
		if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_BUDDHISM')) == True:
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUTUZOU'),1)
		#�J���u���������Ă��邩�ǂ���
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_LABORLIST')):
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_TRIBALISM')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),1)
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SLAVERY')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),1)
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SERFDOM')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),1)
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_CASTE_SYSTEM')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),1)
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_EMANCIPATION')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),1)
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SISHANOOUKOKU')) == True:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),1)
		
		#����MOD�ǋL���������܂�
		
		#AI�ɂ�閂�@�u��
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_SPELLIST')):
			if gc.getPlayer(city.getOwner()).isHuman() == False:
				city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SPELL_OBELISK'),1)
				for i in range(2):
					iBonus = gc.getGame().getSorenRandNum(7, "Spellist AI bonus")
					iAge = gc.getPlayer(city.getOwner()).getCurrentEra()
					if iBonus == 0: 
						city.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),iBonus, (TohoUnitList.SpellistAIBonusList[(iAge)]+1)/2 )
					elif iBonus <= 2:
						city.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),iBonus, TohoUnitList.SpellistAIBonusList[iAge] )
					else:
						city.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_SPELL_OBELISK'),iBonus-3, TohoUnitList.SpellistAIBonusList[iAge] )
		
		#���Ȃ��̎u��������Ε����u��
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KANAKOLIST')):
			if city.isCapital():
				city.plot().setPlotType(PlotTypes.PLOT_HILLS,True,True)
				city.plot().setTerrainType(gc.getInfoTypeForString("TERRAIN_PLAINS"),True,True)
		
		#���P�̌ŗL�u��������΂��ł��ނ����@�����Ō��݂����ȊO�̓s�s�ł́A�^�[�����o�߂��邽�悤�ɂȂ�
		if gc.getPlayer(city.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KOGASALIST')):
			city.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SADESM'),1)
		
		#CvGameUtils.doprint("test---------------")
		#iDamage = city.getDefenseDamage()
		#iDamage = gc.getDefineINT("CITY_DEFENSE_DAMAGE_HEAL_RATE")
		#CvGameUtils.doprint("%i" %iDamage)
		
		##### </written by F> #####
		
		if (city.getOwner() == gc.getGame().getActivePlayer()):
			city.setCitizensAutomated(CFG_EnabledCitizensAutomated)
			self.__eventEditCityNameBegin(city, False)
		CvUtil.pyPrint('City Built Event: %s' %(city.getName()))

	def onCityRazed(self, argsList):
		'City Razed'
		city, iPlayer = argsList
		iOwner = city.findHighestCulture()

		# Partisans!
		if city.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
			owner = gc.getPlayer(iOwner)
			if not owner.isBarbarian() and owner.getNumCities() > 0:
				if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
					if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
						if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent)< 0:
							triggerData = owner.initTriggeredData(iEvent, true, -1, city.getX(), city.getY(), iPlayer, city.getID(), -1, -1, -1, -1)

		CvUtil.pyPrint("City Razed Event: %s" %(city.getName(),))

	def onCityAcquired(self, argsList):
		'City Acquired'
		iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList
		CvUtil.pyPrint('City Acquired Event: %s' %(pCity.getName()))

	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner,pCity = argsList
		
		##### <written by F> #####
		
		#�������̎u��������Δ����R����
		if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_KOISHILIST')):
			if pCity.isCapital():
				pCity.changeOccupationTimer( -(pCity.getOccupationTimer()*3/10)  )
		
		#����MOD�ǋL������������
		
		#����΂ݎu��������Δ�������
		if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_ALCHOL')):
				pCity.changeOccupationTimer( -(pCity.getOccupationTimer()/2)  )
		
		#�s�s���̂����v���C���[�����ۂ̎��@-���������Ă���ꍇ�A�������ϊ�����
		if gc.getPlayer(pCity.getOwner()).countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")) == 1:
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_GROCER")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GROCER'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CASTLE")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CUSTOM_HOUSE")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_FACTORY")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FACTORY'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_COAL_PLANT")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_SUPERMARKET")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET'),0)
		
		#�����łȂ��ꍇ�͋t�̏������s��
		else:
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_PERSIAN_APOTHECARY")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GROCER'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_SPANISH_CITADEL")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_PORTUGAL_FEITORIA")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FACTORY'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT'),0)
			
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_AMERICAN_MALL")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL'),0)
		
		#�Љ�x�n����������U���Z�b�g
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORII'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUTUZOU'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SENTAN'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_2'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_2'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_HAKUREISIKI'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_JAKUSYANORAKUEN'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AMANOJAKU'),0)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SINDEKURERU'),0)
		
		#�فX���w���W�t���s�s���̂����ꍇ�͓���w���W�ɕϊ�
		#if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_BENBENLIST')):
		#	if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_STONEHENGE")):
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_STONEHENGE'),0)
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BENBEN_STONEHENGE'),1)
		#�t�ɕفX�ȊO������w���W�s�s���̂����ꍇ�̓m�[�}���w���W�ɕϊ�
		#if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_BENBEN_STONEHENGE")):
		#	if not gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_BENBENLIST')):
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BENBEN_STONEHENGE'),0)
		#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_STONEHENGE'),1)
		
		#�_�����̗p���Ă���ꍇ�A�s�s�ɒ�����������
		if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_SHINTO')) == True:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TORII'),1)
		#�������̗p���Ă���ꍇ�A�s�s�ɕ�����������
		if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_BUDDHISM')) == True:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUTUZOU'),1)
		#�������̗p���Ă���ꍇ�A�A�z���𑊌ݕϊ�
		if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_TAOISM')) == True:
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_ONMYOURYOU2")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU1'),1)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2'),0)
		else:
			if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_ONMYOURYOU1")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU1'),0)
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2'),1)
		#�J���u���������Ă��邩�ǂ���
		if gc.getPlayer(pCity.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_LABORLIST')):
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_TRIBALISM')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_TRIBALISM'),1)
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SLAVERY')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SLAVERY_1'),1)
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SERFDOM')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SERFDOM'),1)
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_CASTE_SYSTEM')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_CASTE_1'),1)
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_EMANCIPATION')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_EMANCIPATION'),1)
			if (gc.getPlayer(pCity.getOwner()).getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_SISHANOOUKOKU')) == True:
				pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LABORLIST_SISHANOOUKOKU'),1)
		
		#����MOD�ǋL���������܂�
		
		##### </written by F> #####
		CvUtil.pyPrint('City Acquired and Kept Event: %s' %(pCity.getName()))

	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		player = PyPlayer(city.getOwner())
		if (not self.__LOG_CITYLOST):
			return
		CvUtil.pyPrint('City %s was lost by Player %d Civilization %s'
			%(city.getName(), player.getID(), player.getCivilizationName()))

	def onCultureExpansion(self, argsList):
		'City Culture Expansion'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("City %s's culture has expanded" %(pCity.getName(),))

	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("%s has grown" %(pCity.getName(),))

	def onCityDoTurn(self, argsList):
		'City Production'
		pCity = argsList[0]
		iPlayer = argsList[1]

		CvAdvisorUtils.cityAdvise(pCity, iPlayer)

	def onCityBuildingUnit(self, argsList):
		'City begins building a unit'
		pCity = argsList[0]
		iUnitType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription()))

	def onCityBuildingBuilding(self, argsList):
		'City begins building a Building'
		pCity = argsList[0]
		iBuildingType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription()))

	def onCityRename(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		if (pCity.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditCityNameBegin(pCity, True)

	def onCityHurry(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		iHurryType = argsList[1]

	def onVictory(self, argsList):
		'Victory'
		iTeam, iVictory = argsList
		if (iVictory >= 0 and iVictory < gc.getNumVictoryInfos()):
			victoryInfo = gc.getVictoryInfo(int(iVictory))
			CvUtil.pyPrint("Victory!  Team %d achieves a %s victory"
				%(iTeam, victoryInfo.getDescription()))

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList

		if (bVassal):
			CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"
				%(iVassal, iMaster))
		else:
			CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"
				%(iVassal, iMaster))

	def onGameUpdate(self, argsList):
		'sample generic event, called on each game turn slice'
		genericArgs = argsList[0][0]	# tuple of tuple of my args
		turnSlice = genericArgs[0]

	def onMouseEvent(self, argsList):
		'mouse handler - returns 1 if the event was consumed'
		eventType,mx,my,px,py,interfaceConsumed,screens = argsList
		if ( px!=-1 and py!=-1 ):
			if ( eventType == self.EventLButtonDown ):
				if (self.bAllowCheats and self.bCtrl and self.bAlt and CyMap().plot(px,py).isCity() and not interfaceConsumed):
					# Launch Edit City Event
					self.beginEvent( CvUtil.EventEditCity, (px,py) )
					return 1

				elif (self.bAllowCheats and self.bCtrl and self.bShift and not interfaceConsumed):
					# Launch Place Object Event
					self.beginEvent( CvUtil.EventPlaceObject, (px, py) )
					return 1

		if ( eventType == self.EventBack ):
			return CvScreensInterface.handleBack(screens)
		elif ( eventType == self.EventForward ):
			return CvScreensInterface.handleForward(screens)

		global bCityPlacementMode

		if (bCityPlacementMode):
			pPlayer = gc.getActivePlayer()
			CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
			pPlot = CyInterface().getMouseOverPlot()
			iGrid = PlayerUtils.getGameOption(pPlayer, "CityGrid")
			if (iGrid == 1):
				PlayerUtils.colorizeCityPlots(pPlayer)
			if (pPlot.isPeak() or pPlot.isWater() or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DUSTSEA") or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_CRATERRIM") or not pPlot.isRevealed(pPlayer.getTeam(), False)):
				pass
			else:
				bErase = False
				for iSign in xrange(CyEngine().getNumSigns()):
					pSign = CyEngine().getSignByIndex(iSign)
					pSignPlot = pSign.getPlot()
					if (pSignPlot.at(pPlot.getX(), pPlot.getY()) and pSign.getPlayerType() == pPlayer.getID()):
						bErase = True
						PlayerUtils.removeSiteFromList(pPlayer, pPlot)
						CyEngine().removeSign(pSignPlot, pPlayer.getID())
						break
				if (not bErase):
					self.__eventPlayUtilsAddSiteEventPopupBegin((pPlot.getX(), pPlot.getY(), pPlayer.getID()))

		return 0


#################### TRIGGERED EVENTS ##################

	def __eventEditCityNameBegin(self, city, bRename):
		popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((city.getID(), bRename))
		popup.setHeaderString(localText.getText("TXT_KEY_NAME_CITY", ()))
		popup.setBodyString(localText.getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
		popup.createEditBox(city.getName())
		popup.setEditBoxMaxCharCount( 15 )
		if (city.isCitizensAutomated()):
			szText = u"\n<font=2> %s</font>"%(localText.getText("TXT_KEY_CITIZENS_AUTOMATED_ON", ()))
		else:
			szText = u"\n<font=2> %s</font>"%(localText.getText("TXT_KEY_CITIZENS_AUTOMATED_OFF", ()))
		popup.setBodyString(szText)

		popup.launch()

	def __eventEditCityNameApply(self, playerID, userData, popupReturn):
		'Edit City Name Event'
		iCityID = userData[0]
		bRename = userData[1]
		player = gc.getPlayer(playerID)
		city = player.getCity(iCityID)
		cityName = popupReturn.getEditBoxString(0)
		if (len(cityName) > 30):
			cityName = cityName[:30]
		city.setName(cityName, not bRename)

	def __eventEditCityBegin(self, argsList):
		'Edit City Event'
		px,py = argsList
		CvWBPopups.CvWBPopups().initEditCity(argsList)

	def __eventEditCityApply(self, playerID, userData, popupReturn):
		'Edit City Event Apply'
		if (getChtLvl() > 0):
			CvWBPopups.CvWBPopups().applyEditCity( (popupReturn, userData) )

	def __eventPlaceObjectBegin(self, argsList):
		'Place Object Event'
		CvDebugTools.CvDebugTools().initUnitPicker(argsList)

	def __eventPlaceObjectApply(self, playerID, userData, popupReturn):
		'Place Object Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyUnitPicker( (popupReturn, userData) )

	def __eventAwardTechsAndGoldBegin(self, argsList):
		'Award Techs & Gold Event'
		CvDebugTools.CvDebugTools().cheatTechs()

	def __eventAwardTechsAndGoldApply(self, playerID, netUserData, popupReturn):
		'Award Techs & Gold Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyTechCheat( (popupReturn) )

	def __eventShowWonderBegin(self, argsList):
		'Show Wonder Event'
		CvDebugTools.CvDebugTools().wonderMovie()

	def __eventShowWonderApply(self, playerID, netUserData, popupReturn):
		'Wonder Movie Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyWonderMovie( (popupReturn) )

	def __eventEditUnitNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pUnit.getID(),))
		popup.setBodyString(localText.getText("TXT_KEY_RENAME_UNIT", ()))
		popup.createEditBox(pUnit.getNameNoDesc())
		popup.launch()

	def __eventEditUnitNameApply(self, playerID, userData, popupReturn):
		'Edit Unit Name Event'
		iUnitID = userData[0]
		unit = gc.getPlayer(playerID).getUnit(iUnitID)
		newName = popupReturn.getEditBoxString(0)
		if (len(newName) > 25):
			newName = newName[:25]
		unit.setName(newName)

	def __eventWBAllPlotsPopupBegin(self, argsList):
		CvScreensInterface.getWorldBuilderScreen().allPlotsCB()
		return
	def __eventWBAllPlotsPopupApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() >= 0):
			CvScreensInterface.getWorldBuilderScreen().handleAllPlotsCB(popupReturn)
		return

	def __eventWBLandmarkPopupBegin(self, argsList):
		CvScreensInterface.getWorldBuilderScreen().setLandmarkCB("")
		#popup = PyPopup.PyPopup(CvUtil.EventWBLandmarkPopup, EventContextTypes.EVENTCONTEXT_ALL)
		#popup.createEditBox(localText.getText("TXT_KEY_WB_LANDMARK_START", ()))
		#popup.launch()
		return

	def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
		if (popupReturn.getEditBoxString(0)):
			szLandmark = popupReturn.getEditBoxString(0)
			if (len(szLandmark)):
				CvScreensInterface.getWorldBuilderScreen().setLandmarkCB(szLandmark)
		return

	def __eventWBScriptPopupBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventWBScriptPopup, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(localText.getText("TXT_KEY_WB_SCRIPT", ()))
# >>> CYBERFRONT // text: script
#		popup.createEditBox(CvScreensInterface.getWorldBuilderScreen().getCurrentScript())
		popup.createEditBox(CvUtil.convertToUnicode(CvScreensInterface.getWorldBuilderScreen().getCurrentScript()))
# <<< CYBERFRONT
		popup.launch()
		return

	def __eventWBScriptPopupApply(self, playerID, userData, popupReturn):
		if (popupReturn.getEditBoxString(0)):
			szScriptName = popupReturn.getEditBoxString(0)
# >>> CYBERFRONT // text: script
#			CvScreensInterface.getWorldBuilderScreen().setScriptCB(szScriptName)
			CvScreensInterface.getWorldBuilderScreen().setScriptCB(CvUtil.convertToStr(szScriptName))
# <<< CYBERFRONT
		return

	def __eventWBStartYearPopupBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventWBStartYearPopup, EventContextTypes.EVENTCONTEXT_ALL)
		popup.createSpinBox(0, "", gc.getGame().getStartYear(), 1, 5000, -5000)
		popup.launch()
		return

	def __eventWBStartYearPopupApply(self, playerID, userData, popupReturn):
		iStartYear = popupReturn.getSpinnerWidgetValue(int(0))
		CvScreensInterface.getWorldBuilderScreen().setStartYearCB(iStartYear)
		return

	def __eventPlayUtilsAddSiteEventPopupBegin(self, argsList):
		' Add city marker popup '
		popup = PyPopup.PyPopup(CvUtil.EventSitePopup, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData(argsList)
		popup.setHeaderString(localText.getText("TXT_KEY_CITY_PLACEMENT_MODE_HEADER", ()))
		message = localText.getText("TXT_KEY_CITY_PLACEMENT_MODE_BODY", ())
		popup.setBodyString( message )
		popup.createEditBox(UserPrefs.cityPlacementMakerPreset)#localText.getText("TXT_KEY_CITY_PLACEMENT_MODE_MARKER_TEXT", ()))
		popup.setEditBoxMaxCharCount( 21 )
		popup.launch(False, PopupStates.POPUPSTATE_QUEUED)

	def __eventPlayUtilsAddSiteEventPopupApply(self, playerID, netUserData, popupReturn):
		sCaption = popupReturn.getEditBoxString(0)
		pPlot = gc.getMap().plot(netUserData[0], netUserData[1])
		CyEngine().addSign(pPlot, playerID, sCaption)
		PlayerUtils.addSiteToList(gc.getPlayer(playerID), pPlot)

	def __eventUnitPlacementAddSignEventPopupBegin(self, argsList):
		' Add landmark sign popup '
		popup = PyPopup.PyPopup(CvUtil.EventSignPopup, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData(argsList)
		popup.setHeaderString(localText.getText("TXT_KEY_UNIT_PLACEMENT_MARKER_TITLE", ()))
		message = localText.getText("TXT_KEY_UNIT_PLACEMENT_MARKER_BODY", ())
		popup.setBodyString(message)
		popup.createEditBox(UserPrefs.unitPlacementsMakerPreset)#"U.P.: ")
		popup.setEditBoxMaxCharCount(15)
		popup.launch(False, PopupStates.POPUPSTATE_QUEUED)

	def __eventUnitPlacementAddSignEventPopupApply(self, playerID, netUserData, popupReturn):
		sCaption = popupReturn.getEditBoxString(0) 
		pPlot = gc.getMap().plot(netUserData[0], netUserData[1])
		CyEngine().addSign(pPlot, playerID, sCaption)
		UnitPlacement.UnitPlacement().addSignDict(netUserData[0], netUserData[1], sCaption)
