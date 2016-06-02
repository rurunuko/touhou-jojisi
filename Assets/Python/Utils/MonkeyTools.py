## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## 
## Author 	: 12 Monkeys - Tool Collection
## Date 	: 24.03.2006
## version 	: 1.2
## 

from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()
localText = CyTranslator()

UpgradePath = dict()

######################################################
### 	small debug function (stolen from Stone-D's ToolKit)
######################################################

def debug(argsList):
	printToScr = True
	printToLog = True
	message = "%s" %(argsList)
	if (printToScr):
		CyInterface().addImmediateMessage(message,"")
	if (printToLog):
		CvUtil.pyPrint(message)
	return 0

######################################################
### 	Calculates index of an XP point
######################################################

def GetIdxOfXP(iXP):
	iLevel = 0
	iIdx = 0
	while iLevel <= iXP:
		iIdx += 1
		if iIdx == 1:
			iLevel = 2
		else:
			iLevel += (iIdx-1)*2+1
	return iIdx-1

######################################################
### 	Calculates the number of possible promotions between two XP values
######################################################

def GetPossiblePromotions(iXP1, iXP2):
	iIdx1 = GetIdxOfXP(iXP1)
	iIdx2 = GetIdxOfXP(iXP2)
	return iIdx2-iIdx1+1

######################################################
### 	creates a list of possible upgrades for a unit
######################################################

def getPossibleUpgrades(pUnit):
	return [i for i in range(gc.getNumUnitInfos()) if pUnit.canUpgrade(i, True)]

######################################################
### 	creates a list of possible promotions for a unit
######################################################

def getPossiblePromos(pUnit):
	iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
	return [i for i in range(gc.getNumPromotionInfos()) if (pUnit.canAcquirePromotion(i) and (not i == iPromoLeader))]

######################################################
### 	checks if there are any possible upgrade for the unit
######################################################

def checkAnyUpgrade(pUnit):
	#for i in xrange(gc.getNumUnitInfos()):
	if (pUnit.getOwner() !=  gc.getGame().getActivePlayer()):
		return False
	try:
		for i in UpgradePath[pUnit.getUnitType()]:
			if pUnit.canUpgrade(i, True):
				return True
	except KeyError:
		return False
	return False

def getUpgradePath(iUnitType):
	UpgradeUnitList = set()
	for i in xrange(gc.getNumUnitClassInfos()):
		iLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(i)
		if (gc.getUnitInfo(iUnitType).getUpgradeUnitClass(i)):
			UpgradeUnitList.add(iLoopUnit)
			tempList = getUpgradePath(iLoopUnit)
			if (len(tempList) > 0):
				UpgradeUnitList.update(tempList)
	return UpgradeUnitList

def InitUpgradePath():
	global UpgradePath

	UpgradePath = dict()

	for i in xrange(gc.getNumUnitClassInfos()):
		iLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(i)
		UpgradePath[iLoopUnit] = getUpgradePath(iLoopUnit)

	#for iLoopUnit, path in UpgradePath.items():
	#	szTempText = gc.getUnitInfo(iLoopUnit).getDescription() +" -> "
	#	for UnitType in path:
	#		szTempText += gc.getUnitInfo(UnitType).getDescription() + ", "
	#	CvUtil.pyPrint(szTempText)

######################################################
###		function returns a string which contains all the 
###		units characteristics the units get by promotions
######################################################

def getPromotionInfoText(pUnit):
	szPromotionInfo = u""
	bBlitz = False
	bAmphib = False
	bRiver = False
	bEnemyRoads = False
	bAlwaysHeal = False
	bHillsDoubleMove = False
	bImmuneToFirstStrikes = False
	lFeatureDoubleMove = set()
	iVisibilityChange = 0
	iMovesChange = 0
	iMoveDiscountChange = 0
	iWithdrawalChange = 0
	iCollateralDamageChange = 0
	iBombardRateChange = 0
	iFirstStrikesChange = 0
	iChanceFirstStrikesChange = 0
	iEnemyHealChange = 0
	iNeutralHealChange = 0
	iFriendlyHealChange = 0
	iSameTileHealChange = 0
	iAdjacentTileHealChange = 0
	iCombatPercent = 0
	iCityAttackPercent = 0
	iCityDefensePercent = 0
	iHillsDefensePercent = 0
	lFeatureDefensePercent = [0]*gc.getNumFeatureInfos()
	lUnitCombatModifierPercent = [0]*gc.getNumUnitCombatInfos()
	GetText = localText.getText
	for i in xrange(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(i):
			PromoInfo = gc.getPromotionInfo(i)
			if PromoInfo.isBlitz():
				bBlitz = True
			if PromoInfo.isAmphib():
				bAmphib = True
			if PromoInfo.isRiver():
				bRiver = True
			if PromoInfo.isEnemyRoute():
				bEnemyRoads = True
			if PromoInfo.isAlwaysHeal():
				bAlwaysHeal = True
			if PromoInfo.isHillsDoubleMove():
				bHillsDoubleMove = True
			if PromoInfo.isImmuneToFirstStrikes():
				bImmuneToFirstStrikes = True
			lFeatureDoubleMove.update([ii for ii in range(gc.getNumFeatureInfos()) if (PromoInfo.getFeatureDoubleMove(ii))])
			iVisibilityChange += PromoInfo.getVisibilityChange()
			iMovesChange += PromoInfo.getMovesChange()
			iMoveDiscountChange += PromoInfo.getMoveDiscountChange()
			iWithdrawalChange += PromoInfo.getWithdrawalChange()
			iCollateralDamageChange += PromoInfo.getCollateralDamageChange()
			iBombardRateChange += PromoInfo.getBombardRateChange()
			iFirstStrikesChange += PromoInfo.getFirstStrikesChange()
			iChanceFirstStrikesChange += PromoInfo.getChanceFirstStrikesChange()
			iEnemyHealChange += PromoInfo.getEnemyHealChange()
			iNeutralHealChange += PromoInfo.getNeutralHealChange()
			iFriendlyHealChange += PromoInfo.getFriendlyHealChange()
			iSameTileHealChange += PromoInfo.getSameTileHealChange()
			iAdjacentTileHealChange += PromoInfo.getAdjacentTileHealChange()
			iCombatPercent += PromoInfo.getCombatPercent()
			iCityAttackPercent += PromoInfo.getCityAttackPercent()
			iCityDefensePercent += PromoInfo.getCityDefensePercent()
			iHillsDefensePercent += PromoInfo.getHillsDefensePercent()
			for ii in xrange(gc.getNumFeatureInfos()):
				iTemp = PromoInfo.getFeatureDefensePercent(ii)
				if (iTemp > 0):
					lFeatureDefensePercent[ii] += iTemp
			for ii in xrange(gc.getNumUnitCombatInfos()):
				if (PromoInfo.getUnitCombat(ii)):
					iTemp = PromoInfo.getUnitCombatModifierPercent(ii)
					if (iTemp > 0):
						lUnitCombatModifierPercent[ii] += iTemp

	if bBlitz:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_BLITZ_TEXT", ()) + u"\n"
	if bAmphib:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_AMPHIB_TEXT", ()) + u"\n"
	if bRiver:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_RIVER_ATTACK_TEXT", ()) + u"\n"
	if bEnemyRoads:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_ENEMY_ROADS_TEXT", ()) + u"\n"
	if bAlwaysHeal:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_ALWAYS_HEAL_TEXT", ()) + u"\n"
	if bImmuneToFirstStrikes:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_IMMUNE_FIRST_STRIKES_TEXT", ()) + u"\n"

	szTemp = u""
	if (bHillsDoubleMove):
		szTemp += gc.getTerrainInfo(8).getDescription() # TerrainTypes.TERRAIN_HILL = 8
	for ii in lFeatureDoubleMove:
		if (len(szTemp) > 0):
			szTemp += u", "
		szTemp += gc.getFeatureInfo(ii).getDescription()
	if len(szTemp) > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT", (szTemp, )) + u"\n"
	if iVisibilityChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_VISIBILITY_TEXT", (iVisibilityChange, )) + u"\n"
	if iMovesChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_MOVE_TEXT", (iMovesChange, )) + u"\n"
	if iMoveDiscountChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_MOVE_DISCOUNT_TEXT", (iMoveDiscountChange, )) + u"\n"
	if iWithdrawalChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_WITHDRAWAL_TEXT", (iWithdrawalChange, )) + u"\n"
	if iCollateralDamageChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_COLLATERAL_DAMAGE_TEXT", (iCollateralDamageChange, )) + u"\n"
	if iBombardRateChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_BOMBARD_TEXT", (iBombardRateChange, )) + u"\n"
	if iFirstStrikesChange == 1:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_FIRST_STRIKE_TEXT", (iFirstStrikesChange, )) + u"\n"
	if iFirstStrikesChange > 1:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_FIRST_STRIKES_TEXT", (iFirstStrikesChange, )) + u"\n"
	if iChanceFirstStrikesChange == 1:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_FIRST_STRIKE_CHANCE_TEXT", (iChanceFirstStrikesChange, )) + u"\n"
	if iChanceFirstStrikesChange > 1:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_FIRST_STRIKES_CHANCE_TEXT", (iChanceFirstStrikesChange, )) + u"\n"
	if iEnemyHealChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iEnemyHealChange, )) + GetText("TXT_KEY_PROMOTION_ENEMY_LANDS_TEXT", ()) + u"\n"
	if iNeutralHealChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iNeutralHealChange, )) + GetText("TXT_KEY_PROMOTION_NEUTRAL_LANDS_TEXT", ()) + u"\n"
	if iFriendlyHealChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iFriendlyHealChange, )) + GetText("TXT_KEY_PROMOTION_FRIENDLY_LANDS_TEXT", ()) + u"\n"
	if iSameTileHealChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HEALS_SAME_TEXT", (iSameTileHealChange, )) + GetText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT", ()) + u"\n"
	if iAdjacentTileHealChange > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HEALS_ADJACENT_TEXT", (iAdjacentTileHealChange, )) + GetText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT", ()) + u"\n"
	if iCombatPercent > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_STRENGTH_TEXT", (iCombatPercent, )) + u"\n"
	if iCityAttackPercent > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_CITY_ATTACK_TEXT", (iCityAttackPercent, )) + u"\n"
	if iCityDefensePercent > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_CITY_DEFENSE_TEXT", (iCityDefensePercent, )) + u"\n"
	if iHillsDefensePercent > 0:
		szPromotionInfo += GetText("TXT_KEY_PROMOTION_HILLS_DEFENSE_TEXT", (iHillsDefensePercent, )) + u"\n"
	for ii in xrange(gc.getNumFeatureInfos()):
		iTemp = lFeatureDefensePercent[ii]
		if iTemp > 0:
			szPromotionInfo += GetText("TXT_KEY_PROMOTION_DEFENSE_TEXT", (iTemp, gc.getFeatureInfo(ii).getDescription(), )) + u"\n"
	for ii in xrange(gc.getNumUnitCombatInfos()):
		iTemp = lUnitCombatModifierPercent[ii]
		if iTemp > 0:
			szPromotionInfo += GetText("TXT_KEY_PROMOTION_VERSUS_TEXT", (iTemp, gc.getUnitCombatInfo(ii).getDescription(), )) + u"\n"
	return u"<font=2>" + szPromotionInfo + u"</font>"

######################################################
### 	calculates the heal factor per round for a unit. 
###		Takes consideration of city-buildings and 
###		units incl. their promotions on the actual and 
###		adjacent plots. Does only work for player units.
######################################################

def getPlotHealFactor(pUnit):

	# heal rates for certain areas. They are usually stored in the GlobalDefines.XML but can't be read out with a standard API function.
	# So I placed them here as constants.
	ENEMY_HEAL_RATE		= 5
	NEUTRAL_HEAL_RATE	= 10
	FRIENDLY_HEAL_RATE	= 15
	CITY_HEAL_RATE		= 20

	# set/reset some variables
	pPlot = pUnit.plot()
	iSameTileHealFactor 	= 0
	iAdjacentTileHealFactor = 0
	iBuildingHealFactor 	= 0
	iSelfHealFactor 		= 0
	iPromotionHealFactor 	= 0
	iTileHealFactor 		= 0
	iActivePlayer 			= CyGame().getActivePlayer()
	pActivePlayer 			= gc.getPlayer(iActivePlayer)
	iActivePlayerTeam 		= pActivePlayer.getTeam()
	eDomain 				= gc.getUnitInfo(pUnit.getUnitType()).getDomainType()

	# a sea or air unit in a city, behaves like a land unit
	if pPlot.isCity():
		eDomain = DomainTypes.DOMAIN_LAND

	# calculate the adjacent-tile heal-factor caused by other units (only the unit with the highest factor counts)
	for dx in xrange(-1, 2):
		for dy in xrange(-1, 2):
			# ignore same tile. Adjacent-tile healing does not work on the same tile.
			if not (dx == 0 and dy == 0):
				pLoopPlot = CyMap().plot(pPlot.getX()+dx, pPlot.getY()+dy)
				# loop through all units on the plot
				for i in xrange(pLoopPlot.getNumUnits()):
					pLoopUnit = pLoopPlot.getUnit(i)
					eLoopUnitDomain = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
					# a sea or air unit in a city, behaves like a land unit
					if pLoopPlot.isCity():
						eLoopUnitDomain = DomainTypes.DOMAIN_LAND
					# adjacent-tile heal does only work if the units have the same domain type
					if (eDomain == eLoopUnitDomain):
						if (pLoopUnit.getTeam() == iActivePlayerTeam):
							if (pLoopUnit.getAdjacentTileHeal() > iAdjacentTileHealFactor):
								iAdjacentTileHealFactor = pLoopUnit.getAdjacentTileHeal()

	# calculate the same-tile heal-factor caused by other or same unit (only the unit with the highest factor counts)
	# the same-tile healing is also a kind of self-healing. Means : the promotion Medic I has also effect on the owner unit
	for i in xrange(pPlot.getNumUnits()):
		pLoopUnit = pPlot.getUnit(i)
		eLoopUnitDomain = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
		# a sea or air unit in a city, behaves like a land unit
		if pLoopPlot.isCity():
			eLoopUnitDomain = DomainTypes.DOMAIN_LAND
		# same tile heal does only work if the units are of the same domain type
		if (eDomain == eLoopUnitDomain):
			if (pLoopUnit.getTeam() == iActivePlayerTeam):
				if (pLoopUnit.getSameTileHeal() > iSameTileHealFactor):
					iSameTileHealFactor = pLoopUnit.getSameTileHeal()

	# only the highest value counts
	iTileHealFactor = max(iAdjacentTileHealFactor, iSameTileHealFactor)

	# calculate the self heal factor by the location and promotion
	iTeam = pPlot.getTeam()
	pTeam = gc.getTeam(iTeam)
	iSelfHealFactor = NEUTRAL_HEAL_RATE
	iPromotionHealFactor = pUnit.getExtraNeutralHeal()
	if pPlot.isCity():
		iSelfHealFactor 		= CITY_HEAL_RATE
		iPromotionHealFactor 	= pUnit.getExtraFriendlyHeal()
	elif (iTeam == iActivePlayerTeam):
		iSelfHealFactor 		= FRIENDLY_HEAL_RATE
		iPromotionHealFactor 	= pUnit.getExtraFriendlyHeal()
	elif (iTeam != TeamTypes.NO_TEAM):
		if (pTeam.isAtWar(iActivePlayerTeam)):
			iSelfHealFactor 		= ENEMY_HEAL_RATE
			iPromotionHealFactor 	= pUnit.getExtraEnemyHeal()

	# calculate the heal factor by city buildings
	if pPlot.isCity():
		if (pPlot.getTeam() == iActivePlayerTeam):
			pCity = pPlot.getPlotCity()
			# loop for all buldings
			for iBuilding in xrange(gc.getNumBuildingClassInfos()):
				# check if city has that building
				if (pCity.getNumBuilding(iBuilding) != 0):
					# sum up all heal rates 
					iBuildingHealFactor += gc.getBuildingInfo(iBuilding).getHealRateChange()

	# return the sum of all heal factors
	return iTileHealFactor + iBuildingHealFactor + iSelfHealFactor + iPromotionHealFactor

######################################################
### 	calculates the upgrade price for a unit 
###		nMode is :
###			0 : only the actual unit
###			1 : all units of the same type in the same selection group
###			2 : all units of the same type on the same plot
###			3 : all player units of the same type all over the map
######################################################

def getUpgradePrice(pUnit, iToUnitType, nMode):
	pUnitType = pUnit.getUnitType()
	# single unit
	if nMode == 0:
		return pUnit.upgradePrice(iToUnitType)
	# selection group
	elif nMode == 1:
		pPlot = pUnit.plot()
		iPrice = 0
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			if (pLoopUnit.getGroupID() == pUnit.getGroupID()) and (pLoopUnit.getUnitType() == pUnitType):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	# same plot
	elif nMode == 2:
		pPlot = pUnit.plot()
		iPrice = 0
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			if (pLoopUnit.getUnitType() == pUnitType):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	# all players unit
	elif nMode == 3:
		pActPlayer = gc.getActivePlayer()
		iPrice = 0
		for i in xrange(pActPlayer.getNumUnits()):
			pLoopUnit = pActPlayer.getUnit(i)
			if (pLoopUnit.getUnitType() == pUnitType):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	return -1

######################################################
### 	END 
######################################################

def getDoEspionageText(pUnit):
	pPlot = pUnit.plot()

	if (not pUnit.canEspionage(pPlot)):
		return u""

	szText = u""
	bulletIcon = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
	pPlayer = gc.getPlayer(pUnit.getOwner())
	iTarget = pPlot.getOwner()
	iTargetTeam = gc.getPlayer(iTarget).getTeam()
	pTargetTeam = gc.getTeam(iTargetTeam)

	for iLoopEsp in xrange(gc.getNumEspionageMissionInfos()):
		MissionInfo = gc.getEspionageMissionInfo(iLoopEsp)
		if (not MissionInfo.isPassive()):
			if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, -1)):
				if (MissionInfo.isTwoPhases()):
					szText += bulletIcon + MissionInfo.getDescription() + u"\n"
					if (MissionInfo.getDestroyBuildingCostFactor() > 0):
						pCity = pPlot.getPlotCity()
						if (pCity):
							CostList = []
							for iBuilding in xrange(gc.getNumBuildingInfos()):
								if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, iBuilding)):
									if (pCity.getNumRealBuilding(iBuilding) > 0):
										CostList.append(pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, iBuilding))
							CostList.sort()
							szText += u"     %d - %d%c\n"%(CostList[0], CostList[-1], gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
					#elif (MissionInfo.getDestroyUnitCostFactor() > 0):
					#	CostList = []
					#	for iLoopUnit in xrange(pPlot().getNumUnits()):
					#		pLoopUnit = pPlot().getUnit(iLoopUnit)
					#		if (pLoopUnit):
					#			if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, pLoopUnit.getUnitType())):
					#				if (pLoopUnit.getTeam() == iTargetTeam):
					#					CostList.append(pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, pLoopUnit.getUnitType()))
					#	CostList.sort()
					#	szText += u"     %d - %d%c\n"%(CostList[0], CostList[-1], gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
					elif (MissionInfo.getBuyTechCostFactor() > 0):
						szTemp = u""
						for iTech in xrange(gc.getNumTechInfos()):
							if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, iTech)):
								szTemp += u", " + localText.getText("TXT_KET_ESPIONAGE_MISSION_COST", (gc.getTechInfo(iTech).getTextKey(), pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, iTech)))
						szText += u"    " + szTemp[1:] + u"\n"
					elif (MissionInfo.getSwitchCivicCostFactor() > 0):
						szTemp = u""
						for iCivic in xrange(gc.getNumCivicInfos()):
							if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, iCivic)):
								szTemp += u", " + localText.getText("TXT_KET_ESPIONAGE_MISSION_COST", (gc.getCivicInfo(iCivic).getDescription(), pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, iCivic)))
						szText += u"    " + szTemp[1:] + u"\n"
					elif (MissionInfo.getSwitchReligionCostFactor() > 0):
						szTemp = u""
						for iReligion in xrange(gc.getNumReligionInfos()):
							if (pPlayer.canDoEspionageMission(iLoopEsp, iTarget, pPlot, iReligion)):
								szTemp += u", " + localText.getText("TXT_KET_ESPIONAGE_MISSION_COST", (gc.getReligionInfo(iReligion).getDescription(), pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, iReligion)))
						szText += u"    " + szTemp[1:] + u"\n"
				else:
					iCost = pPlayer.getEspionageMissionCost(iLoopEsp, iTarget, pPlot, -1)
					if (iCost > 0):
						szText += bulletIcon + localText.getText("TXT_KET_ESPIONAGE_MISSION_COST", (MissionInfo.getTextKey(), iCost)) + u"\n"

	return szText
