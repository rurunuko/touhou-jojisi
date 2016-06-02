# Unit Placements
# This file is a part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

from CvPythonExtensions import *
from collections import deque
import CvUtil
import SdToolKitAdvanced

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

gOrderList = {}
gSignDict = {}
gID = -100
gAllCityID = -50
gAllUnitID = -25
gOverrideFiraxisBug = {}
UPData = {	"Order": {},	# gOrderList
			"Sign": {},		# gSignDict
			"SignID": -100,	# gID
			"FixBug": {},	# gOverrideFiraxisBug データにActivityTypesを含めるとエラーとなる。数値を直に入れること。
		}

class UnitPlacement:

	def startGame(self):
		global gOrderList
		global gSignDict
		global gID
		global gOverrideFiraxisBug

		#if (not SdToolKitAdvanced.sdObjectExists("CGEUnitPlacement", gc.getGame())):
		#	SdToolKitAdvanced.sdObjectInit("CGEUnitPlacement", gc.getGame(), UPData)
		gOrderList = {}
		gSignDict = {}
		gID = -100
		gOverrideFiraxisBug = {}
		# ID for All City
		#gOrderList[gAllCityID] = {'Unit': {}, 'Enable': True}

	def loadGame(self):
		global gOrderList
		global gSignDict
		global gID
		global gOverrideFiraxisBug

		if (SdToolKitAdvanced.sdObjectExists("CGEUnitPlacement", gc.getGame())):
			dData = SdToolKitAdvanced.sdObjectGetAll("CGEUnitPlacement", gc.getGame())
			gOrderList = dData["Order"]
			gSignDict = dData["Sign"]
			gID = dData["SignID"]
			gOverrideFiraxisBug = dData["FixBug"]
		else:
			#SdToolKitAdvanced.sdObjectInit("CGEUnitPlacement", gc.getGame(), UPData)
			gOrderList = {}
			gSignDict = {}
			gID = -100
			gOverrideFiraxisBug = {}

	def storeDataOnPreSave(self):
		if (len(gOrderList) == 0):
			return

		if (not SdToolKitAdvanced.sdObjectExists("CGEUnitPlacement", gc.getGame())):
			SdToolKitAdvanced.sdObjectInit("CGEUnitPlacement", gc.getGame(), UPData)
		dData = {	"Order": gOrderList,
					"Sign": gSignDict,
					"SignID": gID,
					"FixBug": gOverrideFiraxisBug
				}
		SdToolKitAdvanced.sdObjectSetAll("CGEUnitPlacement", gc.getGame(), dData)

	def InitOrderList(self):
		global gOrderList

		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		(pLoopCity, iter) = pActivePlayer.firstCity(False)
		while (pLoopCity):
			gOrderList[pLoopCity.getID()] = {'Unit': {}, 'Enable': True}
			(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

		# ID for All City
		gOrderList[gAllCityID] = {'Unit': {}, 'Enable': True}

	def resetOrder(self):
		global gOrderList
		global gSignDict
		global gID
		global gOverrideFiraxisBug

		gOrderList = {}
		gSignDict = {}
		gID = -100
		gOverrideFiraxisBug = {}

	def PurgeOrderList(self):
		global gOrderList

		iActivePlayer = gc.getGame().getActivePlayer()
		pActivePlayer = gc.getPlayer(iActivePlayer)

		lDelCityList = []
		for iCityID in gOrderList:
			if (iCityID != gAllCityID):
				pCity = pActivePlayer.getCity(iCityID)
				if (not (pCity and pCity.getOwner() == iActivePlayer)):
					lDelCityList.append(iCityID)
		for iDelCityID in lDelCityList:
			del gOrderList[iDelCityID]

		(pLoopCity, iter) = pActivePlayer.firstCity(False)
		while (pLoopCity):
			iLoopCityID = pLoopCity.getID()
			if (not gOrderList.has_key(iLoopCityID)):
				gOrderList[iLoopCityID] = {'Unit': {}, 'Enable': True}
			(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)
		
		for iLoopCityID in gOrderList:
			lDeleteUnitList = []
			if (iLoopCityID != gAllCityID):
				pLoopCity = pActivePlayer.getCity(iLoopCityID)
				for (LoopUnit, UnitOrder) in gOrderList[iLoopCityID]['Unit'].items():
					if (LoopUnit == gAllUnitID):
						continue
					if (not pLoopCity.canTrain(LoopUnit, False, True)):
						lDeleteUnitList.append(LoopUnit)
			else:
				UnitList = set()
				CivUnit = gc.getCivilizationInfo(pActivePlayer.getCivilizationType()).getCivilizationUnits
				(pTempCity, iter) = pActivePlayer.firstCity(False)
				while (pTempCity):
					for iLoopUnit in xrange(gc.getNumUnitClassInfos()):
						iUnitIndex = CivUnit(iLoopUnit)
						if (pTempCity.canTrain(iUnitIndex, False, True) and gc.getUnitInfo(iLoopUnit).getDomainType() != DomainTypes.DOMAIN_IMMOBILE):
							UnitList.add(iUnitIndex)
					(pTempCity, iter) = pActivePlayer.nextCity(iter, False)
				UnitList.add(gAllUnitID)
				for (LoopUnit, UnitOrder) in gOrderList[iLoopCityID]['Unit'].items():
					if (not LoopUnit in UnitList):
						lDeleteUnitList.append(LoopUnit)
			for LoopUnit in lDeleteUnitList:
				del gOrderList[iLoopCityID]['Unit'][LoopUnit]

		lDeleteList = []
		for (iCityID, CityOrder) in gOrderList.items():
			for (iUnit, LoopUnitList) in CityOrder['Unit'].items():
				queue = LoopUnitList['Queue']
				if (len(queue) > 0):
					newQueue = deque()
					for (iDestID, iNum1, iNum2, bFortify) in queue:
						pCity = pActivePlayer.getCity(iDestID)
						if (gSignDict.has_key(iDestID) or (pCity and pCity.getOwner() == iActivePlayer)):
							newQueue.append((iDestID, iNum1, iNum2, bFortify))
					gOrderList[iCityID]['Unit'][iUnit]['Queue'] = newQueue
					if (len(newQueue) == 0):
						lDeleteList.append((iCityID, iUnit))
		for (iCityID, iUnit) in lDeleteList:
			del gOrderList[iCityID]['Unit'][iUnit]

	def setOrder(self, iCityID, iUnit, iDestID, iNum, iPos, bFortify = False):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
		else:
			CityOrder = {'Unit': {}, 'Enable': True}

		if (len(CityOrder['Unit']) > 0):
			if (CityOrder['Unit'].has_key(iUnit)):
				UnitList = CityOrder['Unit'][iUnit]
			else:
				UnitList = {'Queue': deque(), 'Loop': False}
		else:
			UnitList = {'Queue': deque(), 'Loop': False}

		# (iDestCity: Destnation City ID, iNum: the number of repeat, iCounter: Counter of repeat, bFortify: Flag of Fortify)
		UnitQueue = UnitList['Queue']
		if (iPos == -1):
			UnitQueue.appendleft((iDestID, iNum, iNum, bFortify))
			#UnitList['Loop'] = bLoop
		else:
			UnitQueue.rotate(iPos)
			UnitQueue.pop()
			UnitQueue.append((iDestID, iNum, iNum, bFortify))
			UnitQueue.rotate(-iPos)

		CityOrder['Unit'][iUnit] = UnitList
		gOrderList[iCityID] = CityOrder
		#CvUtil.pyPrint("UnitList: " + str(len(UnitList)))

	def deleteOrder(self, iCityID, iUnit, iPos):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
		else:
			return

		if (len(CityOrder['Unit']) > 0):
			if (CityOrder['Unit'].has_key(iUnit)):
				UnitList = CityOrder['Unit'][iUnit]
			else:
				return
		else:
			return

		UnitQueue = UnitList['Queue']
		UnitQueue.rotate(iPos)
		UnitQueue.pop()
		UnitQueue.rotate(-iPos)

	def getUnitList(self, iCityID, iUnit):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
		else:
			return []

		if (CityOrder['Unit'].has_key(iUnit)):
			UnitList = CityOrder['Unit'][iUnit]
			#CvUtil.pyPrint("UnitList Return: " + str(len(UnitList)))
			return list(reversed(UnitList['Queue']))
		else:
			return []

	def getCityOrder(self, iCityID):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			#CvUtil.pyPrint("CityOrder Return: " + str(len(gOrderList.get(iCityID))))
			CityOrder = []
			for LoopUnit in gOrderList[iCityID]['Unit'].items():
				if (len(LoopUnit[1]['Queue']) > 0):
					CityOrder.append(LoopUnit[0])
			CityOrder.sort()
			CityOrder.reverse()
			return CityOrder
		else:
			return []

	def swapOrder(self, iCityID, iUnit, iPos, bUp):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
		else:
			return

		if (len(CityOrder['Unit']) > 0):
			if (CityOrder['Unit'].has_key(iUnit)):
				UnitList = CityOrder['Unit'][iUnit]
			else:
				return
		else:
			return

		UnitQueue = UnitList['Queue']
		if (bUp):
			UnitQueue.rotate(iPos - 1)
			tPrev = UnitQueue.pop()
			tNext = UnitQueue.pop()
			UnitQueue.append(tPrev)
			UnitQueue.append(tNext)
			UnitQueue.rotate(-(iPos - 1))
		else:
			UnitQueue.rotate(iPos)
			tPrev = UnitQueue.pop()
			tNext = UnitQueue.pop()
			UnitQueue.append(tPrev)
			UnitQueue.append(tNext)
			UnitQueue.rotate(-iPos)

	def isUnitLoop(self, iCityID, iUnit):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
			if (CityOrder['Unit'].has_key(iUnit)):
				UnitList = CityOrder['Unit'][iUnit]
				return UnitList['Loop']
		else:
			return False

	def setUnitLoop(self, iCityID, iUnit, bLoop):
		global gOrderList

		if (gOrderList.has_key(iCityID)):
			CityOrder = gOrderList[iCityID]
			if (CityOrder['Unit'].has_key(iUnit)):
				UnitList = CityOrder['Unit'][iUnit]
				UnitList['Loop'] = bLoop

	def doUnitOrder(self, pCity, pUnit):
		global gOrderList
		global gAllCityID
		global gAllUnitID
		global gOverrideFiraxisBug

		iCityID = pCity.getID()
		iUnit = pUnit.getUnitType()

		if (not gOrderList.has_key(iCityID)):
			# Update City List in gOrderList
			pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			(pLoopCity, iter) = pActivePlayer.firstCity(False)
			while (pLoopCity):
				iLoopCityID = pLoopCity.getID()
				if (not gOrderList.has_key(iLoopCityID)):
					gOrderList[iLoopCityID] = {'Unit': {}, 'Enable': True}
				(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

		if (not gOrderList.has_key(gAllCityID)):
			gOrderList[gAllCityID] = {'Unit': {}, 'Enable': True}

		OrderList = []
		for (iLoopCity, iLoopUnit) in [(iCityID, iUnit), (iCityID, gAllUnitID), (gAllCityID, iUnit), (gAllCityID, gAllUnitID)]:
			LoopCityOrder = gOrderList[iLoopCity]
			if (LoopCityOrder['Unit'].has_key(iLoopUnit)):
				UnitOrder = LoopCityOrder['Unit'][iLoopUnit]
				if (UnitOrder != None and len(UnitOrder['Queue']) != 0):
					OrderList.append((iLoopCity, iLoopUnit))

		if (len(OrderList) == 0):
			return

		UnitOrder = None
		UnitQueue = None
		tOrder = None
		DestDict = self.getSignDict()
		pUnitGrp = pUnit.getGroup()
		for (iLoopCity, iLoopUnit) in OrderList:
			UnitOrder = gOrderList[iLoopCity]['Unit']
			UnitQueue = UnitOrder[iLoopUnit]['Queue']
			bLoop = UnitOrder[iLoopUnit]['Loop']
			tOrder = UnitQueue.pop()
			if (not DestDict.has_key(tOrder[0])):
				iQueueSize = len(UnitQueue)
				if (iQueueSize > 0):
					for iLoopOrder in xrange(iQueueSize):
						tOrder = UnitQueue.pop()
						if (DestDict.has_key(tOrder[0])):
							break
						else:
							tOrder = None
				else:
					tOrder = None
			if (tOrder != None):
				tDest = DestDict[tOrder[0]]
				pDestPos = CyMap().plot(tDest[0], tDest[1])
				if (pUnitGrp.canMoveInto(pDestPos, False) or iCityID == tOrder[0]):
					break
				else:
					tOrder = None

		if (tOrder == None):
			return

		tDest = DestDict[tOrder[0]]
		iDestPosX = tDest[0]
		iDestPosY = tDest[1]
		pDestPos = CyMap().plot(iDestPosX, iDestPosY)
		#CyInterface().addImmediateMessage("U.P.: %s, %s = %s(%d, %d) = (%d, %d), canMoveInto = %s, Fortify = %s"%(pCity.getName(), pUnit.getName(), gc.getUnitInfo(iUnit).getText(), iDestPosX, iDestPosY, pDestPos.getX(), pDestPos.getY(), pUnitGrp.canMoveInto(pDestPos, False), tOrder[3]),"")

		if (iCityID != tOrder[0]):
			pUnitGrp.pushMoveToMission(iDestPosX, iDestPosY)
			#pUnitGrp.pushMission(MissionTypes.MISSION_MOVE_TO, iDestPosX, iDestPosY, 0, True, False, MissionAITypes.NO_MISSIONAI, pDestPos, pUnitGrp.getHeadUnit())
		if (tOrder[3]):
			if (pUnit.canAirPatrol(pDestPos)):
				pUnitGrp.pushMission(MissionTypes.MISSION_AIRPATROL, iDestPosX, iDestPosY, 0, True, False, MissionAITypes.NO_MISSIONAI, pDestPos, pUnitGrp.getHeadUnit())
				gOverrideFiraxisBug[pUnit.getID()] = (iDestPosX, iDestPosY, 5)#ActivityTypes.ACTIVITY_INTERCEPT
			elif (pUnit.canFortify(pDestPos)):
				pUnitGrp.pushMission(MissionTypes.MISSION_FORTIFY, iDestPosX, iDestPosY, 0, True, False, MissionAITypes.NO_MISSIONAI, pDestPos, pUnitGrp.getHeadUnit())
				gOverrideFiraxisBug[pUnit.getID()] = (iDestPosX, iDestPosY, 2)#ActivityTypes.ACTIVITY_SLEEP
			elif (pUnit.canSentry(pDestPos)):
				pUnitGrp.pushMission(MissionTypes.MISSION_SENTRY, iDestPosX, iDestPosY, 0, True, False, MissionAITypes.NO_MISSIONAI, pDestPos, pUnitGrp.getHeadUnit())
				gOverrideFiraxisBug[pUnit.getID()] = (iDestPosX, iDestPosY, 4)#ActivityTypes.ACTIVITY_SENTRY
		#CyInterface().addImmediateMessage("Unit Placement: " + pCity.getName() + ", " + pUnit.getName() + " -> " + tDest[2],"")

		if (tOrder[2] != 1):
			UnitQueue.append((tOrder[0], tOrder[1], tOrder[2] - 1, tOrder[3]))
		elif (bLoop):
			UnitQueue.appendleft((tOrder[0], tOrder[1], tOrder[1], tOrder[3]))

	def doOverrideFiraxisBug(self):
		global gOverrideFiraxisBug

		iActivePlayer = gc.getGame().getActivePlayer()
		pActivePlayer = gc.getPlayer(iActivePlayer)
		DeleteOrder = []
		for iLoopUnitID in gOverrideFiraxisBug:
			pLoopUnit = pActivePlayer.getUnit(iLoopUnitID)
			tOrder = gOverrideFiraxisBug[iLoopUnitID]
			if (pLoopUnit.getX() == tOrder[0] and pLoopUnit.getY() == tOrder[1]):
				pUnitGrp = pLoopUnit.getGroup()
				if (pUnitGrp.getActivityType() == ActivityTypes.ACTIVITY_HOLD):
					#pUnitGrp.pushMission(tOrder[2], tOrder[0], tOrder[1], 0, False, False, MissionAITypes.NO_MISSIONAI, CyMap().plot(tOrder[0], tOrder[1]), pUnitGrp.getHeadUnit())
					pUnitGrp.setActivityType(tOrder[2])
					DeleteOrder.append(iLoopUnitID)
				else:
					DeleteOrder.append(iLoopUnitID)

		for iLoopUnitID in DeleteOrder:
			del gOverrideFiraxisBug[iLoopUnitID]

	def addSignDict(self, iPosX, iPosY, szName):
		global gSignDict
		global gID

		gSignDict[gID] = (iPosX, iPosY, szName)
		gID -= 1

	def deleteSignDict(self, iPosX, iPosY):
		global gSignDict

		for item in gSignDict.items():
			if (item[1][0] == iPosX and item[1][1] == iPosY):
				del gSignDict[item[0]]

	def getSignDict(self):
		global gSignDict
		CityDict = dict()

		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		(pLoopCity, iter) = pActivePlayer.firstCity(False)
		while (pLoopCity):
			CityDict[pLoopCity.getID()] = (pLoopCity.getX(), pLoopCity.getY(), pLoopCity.getName())
			(pLoopCity, iter) = pActivePlayer.nextCity(iter, False)

		CityDict.update(gSignDict)
		return CityDict
