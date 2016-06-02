# CGE Utilities
# This file is a part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
import CvUtil
import AlertsLog
import CvConfigParser
import SdToolKitAdvanced
import UserPrefs

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

gSpyAlert = dict()
ObsoleteBonus = dict()
ObsoleteBuilding = dict()
gSpyMoveToList = []
gSpyMovingList = dict()
gEspionagePoint = dict()
gAutoRecon = dict()
gAutoReconUnit = -1
gAutoReconSetMode = False
gAutoReconDest = (-1, -1)
gWonderPrereqBuilding = dict()
gWonderPrereqBuildingSet = set()
gAutoOrder = False
gAutoOrderCombatTypeList = dict()
gAUtoOrderUnitClassList = dict()

config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
CFG_Spy_Detect = config.getboolean('Spy Detect', 'Enabled', False)

class CGEUtils:

	def resetCGEUtils(self):
		global gSpyAlert
		global ObsoleteBonus
		global ObsoleteBuilding
		global gEspionagePoint
		global gAutoRecon
		global gAutoReconUnit
		global gAutoReconSetMode
		global gAutoReconDest
		global gWonderPrereqBuilding
		global gWonderPrereqBuildingSet
		global gAutoOrder
		global gAutoOrderCombatTypeList
		global gAUtoOrderUnitClassList

		# initiate spy alert
		gSpyAlert = dict()

		# initiate auto recon
		gAutoRecon = dict()
		gAutoReconUnit = -1
		gAutoReconSetMode = False
		gAutoReconDest = (-1, -1)

		# initiate Obsolete alert
		ObsoleteBonus = dict()
		ObsoleteBuilding = dict()

		for iBonus in xrange(gc.getNumBonusInfos()):
			iTech = gc.getBonusInfo(iBonus).getTechObsolete()
			if (iTech > -1):
				if (not ObsoleteBonus.has_key(iTech)):
					ObsoleteBonus[iTech] = set()
				ObsoleteBonus[iTech].add(iBonus)

		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		ActiveLeaderInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
		lBuilding = set()
		for iTrait in xrange(gc.getNumTraitInfos()):
			if (ActiveLeaderInfo.hasTrait(iTrait)):
				for iBuilding in xrange(gc.getNumBuildingInfos()):
					if (gc.getBuildingInfo(iBuilding).getHappinessTraits(iTrait) > 0):
						lBuilding.add(iBuilding)

		for iBuilding in lBuilding:
			iTech = gc.getBuildingInfo(iBuilding).getObsoleteTech()
			if (iTech > -1):
				if (not ObsoleteBuilding.has_key(iTech)):
					ObsoleteBuilding[iTech] = set()
				ObsoleteBuilding[iTech].add(iBuilding)

		# for Debug
		#for (iTech, lBonus) in ObsoleteBonus.items():
		#	szText = ""
		#	for iBonus in lBonus:
		#		szText += ", " + gc.getBonusInfo(iBonus).getDescription()
		#	CvUtil.pyPrint("Obsolete Tech(%s): "%(gc.getTechInfo(iTech).getDescription()) + szText)
		#for (iTech, lBuilding) in ObsoleteBuilding.items():
		#	szText = ""
		#	for iBuilding in lBuilding:
		#		szText += ", " + gc.getBuildingInfo(iBuilding).getDescription()
		#	CvUtil.pyPrint("Obsolete Tech(%s): "%(gc.getTechInfo(iTech).getDescription()) + szText)

		gEspionagePoint = dict()
		for iLoopTeam in xrange(gc.getMAX_CIV_TEAMS()):
			gEspionagePoint[iLoopTeam] = 0

		gWonderPrereqBuilding = dict()
		gWonderPrereqBuildingSet = set()
		getBuildingVal = gc.getCivilizationInfo(pActivePlayer.getCivilizationType()).getCivilizationBuildings
		for iBuilding in xrange(gc.getNumBuildingClassInfos()):
			iLoopBuilding = getBuildingVal(iBuilding)
			if (isLimitedWonderClass(gc.getBuildingInfo(iLoopBuilding).getBuildingClassType())):
				for iI in xrange(gc.getNumBuildingClassInfos()):
					iNumPrereq = pActivePlayer.getBuildingClassPrereqBuilding(iLoopBuilding, iI, 0)
					if (iNumPrereq > 0):
						iTempBuilding = getBuildingVal(iI)
						iCount = pActivePlayer.getBuildingClassCount(iI)
						#CvUtil.pyPrint("Wonder: %s(%s, %d/%d)"%(gc.getBuildingInfo(iLoopBuilding).getDescription(), gc.getBuildingInfo(iTempBuilding).getDescription(), iCount, iNumPrereq))
						if (iCount < iNumPrereq):
							gWonderPrereqBuildingSet.add(iTempBuilding)
							gWonderPrereqBuilding[iLoopBuilding] = (iTempBuilding, iNumPrereq)

		gAutoOrder = UserPrefs.EnableAutoOrder
		gAutoOrderCombatTypeList = dict()
		dConvertDict = {"UNITCOMBAT_OtherType": -1}
		for i in xrange(gc.getNumUnitCombatInfos()):
			dConvertDict[gc.getUnitCombatInfo(i).getType()] = i
		for (szCombatType, szOrder) in UserPrefs.AutoOrderCombatType.items():
			iCombatType = dConvertDict.setdefault("UNITCOMBAT_" + szCombatType)
			if (iCombatType != None):
				gAutoOrderCombatTypeList[iCombatType] = szOrder
				#CvUtil.pyPrint("AutoOrder: %d -> %s, %s"%(iCombatType, szOrder, gc.getDefineINT("UNITCOMBAT_" + szCombatType)))

		gAUtoOrderUnitClassList = dict()
		dConvertDict = dict()
		for i in xrange(gc.getNumUnitClassInfos()):
			dConvertDict[gc.getUnitClassInfo(i).getType()] = i
			#CvUtil.pyPrint("AutoOrder: %d -> %s"%(i, gc.getUnitClassInfo(i).getType()))
		for (szClass, szOrder) in UserPrefs.AutoOrderUnitClass.items():
			iUnitClass = dConvertDict.setdefault("UNITCLASS_" + szClass)
			if (iUnitClass != None):
				gAUtoOrderUnitClassList[iUnitClass] = szOrder
				CvUtil.pyPrint("AutoOrder: %d -> %s"%(iUnitClass, szOrder))

	def setSpyAlert(self, pUnit):
		global gSpyAlert
		pPlot = pUnit.plot()

		if (pUnit.getOwner() != gc.getGame().getActivePlayer() or not pUnit.canEspionage(pPlot)):
			return

		gSpyAlert[pUnit.getID()] = (pPlot.getX(), pPlot.getY())

	def isSpyAlert(self, pUnit):
		iID = pUnit.getID()
		if (gSpyAlert.has_key(iID)):
			if (pUnit.getX() == gSpyAlert[iID][0] and pUnit.getY() == gSpyAlert[iID][1]):
				return True
			else:
				del gSpyAlert[iID]
				return False
		else:
			return False

	def SpyMoveToCity(self, pUnit):
		global gSpyMoveToList

		gSpyMoveToList = [pUnit.getID()]
		pUnitGroup = pUnit.getGroup()
		CanMoveInto = pUnitGroup.canMoveInto
		GeneratePath = pUnitGroup.generatePath
		iActivePlayer = gc.getGame().getActivePlayer()
		pActivePlayer = gc.getPlayer(iActivePlayer)
		iActiveTeam = pActivePlayer.getTeam()
		pCapCity = pActivePlayer.getCapitalCity()
		pPosition = pUnitGroup.plot()
		iCapX = pCapCity.getX()
		iCapY = pCapCity.getY()

		popup=CyPopup(CvUtil.EventSpyMoveToCity, EventContextTypes.EVENTCONTEXT_ALL, True)
		popup.setHeaderString("Spy Move to City", CvUtil.FONT_CENTER_JUSTIFY)
		popup.createPullDown(0)

		iCount = 1
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (iLoopPlayer != iActivePlayer and pLoopPlayer.isAlive() and not pLoopPlayer.isMinorCiv() and not pLoopPlayer.isBarbarian()):
				(pLoopCity, iter) = pLoopPlayer.firstCity(False)
				while (pLoopCity):
					if (pLoopCity.isRevealed(iActiveTeam, False)):
						if (CanMoveInto(pLoopCity.plot(), False)):
							if (GeneratePath(pPosition, pLoopCity.plot(), 0, False, None)):
								popup.addPullDownString("%s(%s) - %d"%(pLoopCity.getName(), pLoopPlayer.getName(), plotDistance(iCapX, iCapY, pLoopCity.getX(), pLoopCity.getY())), iCount, 0)
								gSpyMoveToList.append((pLoopCity.getX(), pLoopCity.getY()))
								iCount += 1
					(pLoopCity, iter) = pLoopPlayer.nextCity(iter, False)
		if (iCount > 1):
			popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

	def SpyMoveToCityExec(self, iNum):
		global gSpyMoveToList
		global gSpyMovingList

		pUnit = gc.getPlayer(gc.getGame().getActivePlayer()).getUnit(gSpyMoveToList[0])
		pUnitGroup = pUnit.getGroup()
		(iDestX, iDestY) = gSpyMoveToList[iNum]
		pDest = CyMap().plot(iDestX, iDestY)

		pUnitGroup.pushMoveToMission(iDestX, iDestY)
		bCanSleep = pUnit.canSleep(pDest)
		if (bCanSleep):
			pUnitGroup.pushMission(MissionTypes.MISSION_SLEEP, iDestX, iDestY, 0, True, False, MissionAITypes.NO_MISSIONAI, pDest, pUnitGroup.getHeadUnit())

		gSpyMoveToList = []
		gSpyMovingList[pUnit.getID()] = (iDestX, iDestY)

	def checkSpyAlert(self):
		global gSpyAlert
		global gSpyMovingList

		pActivePlayer = gc.getActivePlayer()

		for (iID, (iX, iY)) in gSpyMovingList.copy().items():
			pLoopUnit = pActivePlayer.getUnit(iID)
			pLoopGroup = pLoopUnit.getGroup()
			if (pLoopGroup.getLengthMissionQueue() > 0):
				MissionData = pLoopGroup.getMissionFromQueue(0)
				if (MissionData.iData1 == iX and MissionData.iData2 == iY):
					continue
				else:
					del gSpyMovingList[iID]
			else:
				if (pLoopUnit.getX() == iX and pLoopUnit.getY() == iY):
					gSpyAlert[iID] = (iX, iY)
				del gSpyMovingList[iID]

		tempDict1 = gSpyAlert.copy()
		lTempUnitList = []
		gSpyAlert = dict()
		for (iID, (iX, iY)) in tempDict1.items():
			pLoopUnit = pActivePlayer.getUnit(iID)
			iUnitX = pLoopUnit.getX()
			iUnitY = pLoopUnit.getY()
			if (not pLoopUnit.isDead() and (iUnitX == iX and iUnitY == iY)):
				lTempUnitList.append((pLoopUnit.getID(), pLoopUnit.getFortifyTurns(), iUnitX, iUnitY))

		iMaxFortTurn = gc.getDefineINT("MAX_FORTIFY_TURNS") -1
		for (LoopID, iTurn, iUnitX, iUnitY) in lTempUnitList:
			if (iTurn < iMaxFortTurn):
				gSpyAlert[LoopID] = (iUnitX, iUnitY)
			else:
				# Alert !
				szString = localText.getText("TXT_KEY_CGE_ALERT_MAX_FORTIFY", (gc.getDefineINT("MAX_FORTIFY_TURNS"),))
				AlertsLog.AlertsLog().AlertsLogMessage(gc.getGame().getActivePlayer(), szString, gc.getMissionInfo(MissionTypes.MISSION_INFILTRATE).getButton(), gc.getInfoTypeForString("COLOR_TECH_TEXT"), iUnitX, iUnitY, 3, -1, -1, True, True)
				#pLoopUnit = gc.getPlayer(gc.getGame().getActivePlayer()).getUnit(LoopID)
				#pLoopGroup = pLoopUnit.getGroup()
				#pPlot = CyMap().plot(iUnitX, iUnitY)
				#if (pLoopUnit.canEspionage(pPlot)):
				#	pLoopGroup.pushMission(MissionTypes.MISSION_ESPIONAGE, EspionageMissionTypes.NO_ESPIONAGEMISSION, -1, 0, True, False, MissionAITypes.NO_MISSIONAI, pPlot, pLoopGroup.getHeadUnit())

	def checkTechObsoleteAlert(self):
		pActivePlayer = gc.getActivePlayer()

		currentReseachTech = pActivePlayer.getCurrentResearch()

		bHasBonus = ObsoleteBonus.has_key(currentReseachTech)
		bHasBuilding = ObsoleteBuilding.has_key(currentReseachTech)

		if (not (bHasBonus or bHasBuilding)):
			return

		if (pActivePlayer.isAnarchy() or currentReseachTech == -1):
			return

		if (pActivePlayer.getResearchTurnsLeft(currentReseachTech, True) == 3):
			(pLoopCity, iter) = pActivePlayer.firstCity(False)
			while (pLoopCity):
				iHappiness = pLoopCity.happyLevel() - pLoopCity.unhappyLevel(0)
				if (iHappiness > -1):
					szText = u""
					iBonusHappiness = 0
					if (bHasBonus):
						for iBonus in ObsoleteBonus[currentReseachTech]:
							if (pLoopCity.hasBonus(iBonus)):
								iLoopHappiness = pLoopCity.getBonusHappiness(iBonus)
								if (iLoopHappiness > 0):
									iBonusHappiness += iLoopHappiness
									szText += ", " + gc.getBonusInfo(iBonus).getDescription()
					iBuildingHappiness = 0
					if (bHasBuilding):
						for iBuilding in ObsoleteBuilding[currentReseachTech]:
							if (pLoopCity.getNumBuilding(iBuilding) > 0):
								if (pLoopCity.getNumActiveBuilding(iBuilding) > 0):
									iLoopHappiness = pLoopCity.getBuildingHappiness(iBuilding)
									if (iLoopHappiness > 0):
										iBuildingHappiness += iLoopHappiness
										szText += ", " + gc.getBuildingInfo(iBuilding).getDescription()

					iHappiness = iHappiness - (iBonusHappiness + iBuildingHappiness)
					if (iHappiness < 0):
						szText = localText.getText("TXT_KEY_CGE_ALERT_OBSOLETE_TECH_ANGRY", (gc.getTechInfo(currentReseachTech).getDescription(), szText[2:], pLoopCity.getName()))
						AlertsLog.AlertsLog().AlertsLogMessage(gc.getGame().getActivePlayer(), szText, "Art/Interface/mainscreen/cityscreen/angry_citizen.dds", gc.getInfoTypeForString("COLOR_WARNING_TEXT"), pLoopCity.getX(), pLoopCity.getY(), 1, pLoopCity.getID(), -1, True, True)

				(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

	def FullLoadUnits(self, pHeadUnit):
		iActPlayer = gc.getGame().getActivePlayer()
		pPlot = pHeadUnit.plot()

		UnitList = []
		getPlotUnit = CyInterface().getInterfacePlotUnit
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = getPlotUnit(pPlot, i)
			if (pLoopUnit):
				UnitList.append(pLoopUnit)

		loadableUnits = []
		lastUnitType = None
		selectedGroup = pHeadUnit.getGroup()
		for i in xrange(selectedGroup.getNumUnits()):
			pSelectUnit = selectedGroup.getUnitAt(i)
			iUnitType = pSelectUnit.getUnitType()

			if (lastUnitType != iUnitType):
				loadableUnits = []
				for pLoopUnit in UnitList:
					if (not pLoopUnit.isCargo() and pLoopUnit.canLoadUnit(pSelectUnit, pPlot)):
						loadableUnits.append(pLoopUnit)
				lastUnitType = iUnitType

			iUnit = pSelectUnit.getID()
			for j in xrange(pSelectUnit.cargoSpace() - pSelectUnit.getCargo()):
				try:
					pLoopUnit = loadableUnits.pop(0)
				except IndexError:
					break
				pLoopUnit.doCommand(CommandTypes.COMMAND_LOAD_UNIT, iActPlayer, iUnit)

	def UpdateEspionagePoint(self):
		global gEspionagePoint

		gEspionagePoint = dict()
		ActiveTeam = gc.getGame().getActiveTeam()
		for iLoopTeam in xrange(gc.getMAX_CIV_TEAMS()):
			gEspionagePoint[iLoopTeam] = gc.getTeam(iLoopTeam).getEspionagePointsAgainstTeam(ActiveTeam)

	def isSpendEspionagePoint(self, iTeam, iEspPoint):
		if (not CFG_Spy_Detect):
			return False

		if (iEspPoint < gEspionagePoint[iTeam]):
			return True
		else:
			return False

	def AutoReconSetMode(self, iUnitID, bEnable):
		global gAutoReconUnit
		global gAutoReconSetMode

		if (bEnable):
			gAutoReconUnit = iUnitID
			gAutoReconSetMode = True
		else:
			gAutoReconUnit = -1
			gAutoReconSetMode = False

	def cancelAutoReconMode(self, iUnitID):
		global gAutoRecon

		if (gAutoRecon.has_key(iUnitID)):
			del gAutoRecon[iUnitID]
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, True)
			CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

	def isAutoReconSetMode(self):
		return gAutoReconSetMode

	def isAutoReconUnit(self, iUnitID):
		global gAutoRecon

		return gAutoRecon.has_key(iUnitID)

	def showAutoReconTargetPlot(self, iUnitID):
		global gAutoRecon
		global gAutoReconDest

		if (gAutoRecon.has_key(iUnitID)):
			CyEngine().addColoredPlotAlt(gAutoRecon[iUnitID][2], gAutoRecon[iUnitID][3], PlotStyles.PLOT_STYLE_DOT_TARGET, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER, "COLOR_BLUE", .5)
			gAutoReconDest = (gAutoRecon[iUnitID][2], gAutoRecon[iUnitID][3])
		else:
			CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)

	def setAutoRecon(self, iOwner, iMission, iUnitID):
		global gAutoRecon
		global gAutoReconUnit
		global gAutoReconSetMode

		if (iOwner != gc.getGame().getActivePlayer() or iUnitID != gAutoReconUnit):
			gAutoReconUnit = -1
			gAutoReconSetMode = False
			return

		if (iMission != MissionTypes.MISSION_RECON):
			del gAutoRecon[iUnitID]
			gAutoReconUnit = -1
			gAutoReconSetMode = False
			return

		pUnit = gc.getPlayer(iOwner).getUnit(iUnitID)
		pTargetPlot = CyInterface().getMouseOverPlot()

		gAutoRecon[iUnitID] = (pUnit.getX(), pUnit.getY(), pTargetPlot.getX(), pTargetPlot.getY())
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_WORLD_BUILDER)
		#CyInterface().addImmediateMessage("Auto Recon: %s(%d,%d) -> (%d,%d)"%(pUnit.getName(), pUnit.getX(), pUnit.getY(), pTargetPlot.getX(), pTargetPlot.getY()),"")

		gAutoReconUnit = -1
		gAutoReconSetMode = False

	def doAutoRecon(self):
		global gAutoRecon

		iActivePlayer = gc.getGame().getActivePlayer()
		pActivePlayer = gc.getPlayer(iActivePlayer)
		for (iID, (iX, iY, iTargetX, iTargetY)) in gAutoRecon.copy().items():
			pLoopUnit = pActivePlayer.getUnit(iID)
			if (not pLoopUnit or pLoopUnit.getOwner() != iActivePlayer):
				del gAutoRecon[iID]
				continue
			if (pLoopUnit.getX() != iX or pLoopUnit.getY() != iY):
				del gAutoRecon[iID]
				continue
			pUnitGroup = pLoopUnit.getGroup()
			if (pUnitGroup.getActivityType() > ActivityTypes.ACTIVITY_SLEEP or pUnitGroup.getLengthMissionQueue() > 0):
				del gAutoRecon[iID]
				continue
			if (pUnitGroup.canStartMission(MissionTypes.MISSION_RECON, iTargetX, iTargetY, pLoopUnit.plot(), False)):
				pTarget = CyMap().plot(iTargetX, iTargetY)
				pUnitGroup.pushMission(MissionTypes.MISSION_RECON, iTargetX, iTargetY, 0, True, False, MissionAITypes.NO_MISSIONAI, pTarget, pLoopUnit)

	def getAutoReconUnitsList(self):
		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		unitList = [pActivePlayer.getUnit(iID) for iID in gAutoRecon.keys()]
		return unitList

	def getTargetPlot(self, iUnitID):
		if (gAutoRecon.has_key(iUnitID)):
			return (gAutoRecon[iUnitID][2], gAutoRecon[iUnitID][3])
		else:
			return None

	def checkWonderPrereqBuildingAlert(self, iBuilding):
		global gWonderPrereqBuilding
		global gWonderPrereqBuildingSet

		if (iBuilding not in gWonderPrereqBuildingSet):
			return

		iDelete = 0
		iSame = 0
		iCount = gc.getPlayer(gc.getGame().getActivePlayer()).getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType())
		for (iWonder, (iLoopBuilding, iPrereq)) in gWonderPrereqBuilding.copy().items():
			if (iBuilding == iLoopBuilding):
				if (iPrereq <= iCount):
					szString = localText.getText("TXT_KEY_WONDER_PREREQ_BUILDING_ALERT", (gc.getBuildingInfo(iWonder).getDescription(), gc.getBuildingInfo(iLoopBuilding).getDescription(), str(iPrereq)))
					AlertsLog.AlertsLog().AlertsLogMessage(gc.getGame().getActivePlayer(), szString, None, gc.getInfoTypeForString("COLOR_TECH_TEXT"), 0, 0, 2, -1, -1, False, False)
					del gWonderPrereqBuilding[iWonder]
					iDelete += 1
					iSame += 1
				else:
					iSame += 1
		if (iSame > 0 and iDelete > 0 and iSame == iDelete):
			gWonderPrereqBuildingSet.remove(iBuilding)

	def insertBuildingOrderQueue(self, pCity, iBuildingType):
		if (not SdToolKitAdvanced.sdObjectExists("CGEAutoInsertQueue", pCity)):
			return

		OrderQueue = SdToolKitAdvanced.sdObjectGetVal("CGEAutoInsertQueue", pCity, "InsertQueue")

		bDelete = False
		for (iBuilding, iTrigger, bTop) in OrderQueue.copy().values():
			if (pCity.getNumBuilding(iBuilding) > 0):
				del OrderQueue[iBuilding]
				bDelete = True
			else:
				if (iBuildingType == iTrigger):
					pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT, iBuilding, -1, False, False, not bTop, False)
					del OrderQueue[iBuilding]
					bDelete = True
				elif (pCity.getNumBuilding(iTrigger) > 0):
					del OrderQueue[iBuilding]
					bDelete = True

		if (bDelete):
			SdToolKitAdvanced.sdObjectSetVal("CGEAutoInsertQueue", pCity, "InsertQueue", OrderQueue)

	def executeAutoOrder(self, pUnit):
		szOrder = None
		pUnitGroup = pUnit.getGroup()

		if (gAUtoOrderUnitClassList.has_key(pUnit.getUnitClassType())):
			szOrder = gAUtoOrderUnitClassList[pUnit.getUnitClassType()]
		elif (gAutoOrderCombatTypeList.has_key(pUnit.getUnitCombatType())):
			szOrder = gAutoOrderCombatTypeList[pUnit.getUnitCombatType()]

		# Order
		if (szOrder == "NONE"):
			return
		elif (szOrder == "SLEEP"):
			pUnitGroup.setActivityType(ActivityTypes.ACTIVITY_SLEEP)
		elif (szOrder == "INTERCEPT"):
			if (pUnit.canAirPatrol(pUnit.plot())):
				pUnitGroup.setActivityType(ActivityTypes.ACTIVITY_INTERCEPT)

	def isAutoOrder(self):
		return gAutoOrder

	def setAutoOrder(self, bValue):
		global gAutoOrder

		gAutoOrder = bValue

class CGEUtilsOption:

	def setCGEOption(self, Section, Key, Value):
		global CFG_Spy_Detect

		if (Section == 'Spy Detect'):
			if (Key == 'Enabled'):
				CFG_Spy_Detect = Value
