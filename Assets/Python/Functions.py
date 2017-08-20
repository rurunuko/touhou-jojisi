##### <written by F> #####
#�����g���p�֐��Q

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import math
import SpellInfo

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

RangeList0 = [[0,0],]

RangeList1 = [	[-1,-1],[ 0,-1],[ 1,-1],
				[-1, 0],        [ 1, 0],
				[-1, 1],[ 0, 1],[ 1, 1], ]

#�w�肳�ꂽ�ꏊ���L����plot�ł��邩�ǂ����𔻕�
#�f�t�H�̂��ƃ��[�v��������肭�����Ȃ��̂Ŏ��O�Ŏ���
def isPlot(iX,iY):
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	#X���L���͈͓����ǂ����`�F�b�N
	bFlagX = False
	if -1<iX and iX<iWidth:
		bFlagX = True
	else:
		if pMap.isWrapX():
			bFlagX = True
	
	#Y���L���͈͓����ǂ����`�F�b�N
	bFlagY = False
	if -1<iY and iY<iHeight:
		bFlagY = True
	else:
		if pMap.isWrapY():
			bFlagY = True
	
	if bFlagX and bFlagY:
		return True
	
	return False


#�͈͓��Ɏw�肳�ꂽ���j�b�g�����邩�ǂ������`�F�b�N����
def checkUnit(iX,iY,squeaList,iStartUnit,iEndUnit,returnUnitFlag = 0):
	UnitList = []
	for squea in squeaList:
		iiX = iX + squea[0]
		iiY = iY + squea[1]
		if isPlot(iiX,iiY):
			pPlot = gc.getMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if iStartUnit <= pUnit.getUnitType() and pUnit.getUnitType() <= iEndUnit:
					if returnUnitFlag == 1:
						return pUnit
					elif returnUnitFlag == 2:
						UnitList.append(pUnit)
					else:
						return True
	if returnUnitFlag == 2:
		return UnitList
	else:
		return False


#���X�^�b�N�̖����������j�b�g��T���ă��X�g��Ԃ�
def searchTeamTohoUnit(pPlot,unit):
	UnitList=[]
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			if unit.getTeam() == pUnit.getTeam():
				UnitList.append(pUnit)
	
	return UnitList



#�X�y�J��req�֐��̔ėp�֐�
def req_SpellCard(bTestVisible,caster,iStartCAL,iEndCAL,sStartUnit,sEndUnit,cost=0):

	if bTestVisible:
		if iStartCAL <= caster.countCardAttackLevel() and caster.countCardAttackLevel() <= iEndCAL:
			if gc.getInfoTypeForString(sStartUnit) <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString(sEndUnit):
				return True
			if gc.getInfoTypeForString('UNIT_SATORI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_SATORI6'):
				RangeList = [ [-1,-1],[ 0,-1],[ 1,-1],[-1, 0], [ 0, 0],[ 1, 0],[-1, 1],[ 0, 1],[ 1, 1], ]
				if checkUnit(caster.getX(),caster.getY(),RangeList,gc.getInfoTypeForString(sStartUnit),gc.getInfoTypeForString(sEndUnit)):
					return True
	else:
		#if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELLCARD")):
		if caster.getPower() >= cost:
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if caster.getPower() >= cost:
					if caster.getNumSpellCardBreakTime() <= 0:
						return True
				
	return False

#�X�y����req�֐��̔ėp�֐�
def req_Spell(bTestVisible,caster,sPromotion,sStartUnit,sEndUnit,cost=0):

	if bTestVisible:
		if gc.getInfoTypeForString(sStartUnit) <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString(sEndUnit):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString(sPromotion)):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and caster.getPower() >= cost:
				if sPromotion == 'PROMOTION_MODE_EXTRA' and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
					return True
				if sPromotion == 'PROMOTION_MODE_PHANTASM' and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
					return True
				if sPromotion == 'PROMOTION_FLAN':
					return True
				if sPromotion == 'PROMOTION_ICHIRIN_SKILL1':
					return True
				if sPromotion == 'PROMOTION_BYAKUREN_SKILL1':
					return True
				if sPromotion == 'PROMOTION_YORIHIME_SKILL1':
					return True
	return False



#�_���[�W�֐�
#�w�肳�ꂽ�͈͂ɐݒ肳�ꂽ��ނ̃��j�b�g�Ƀ_���[�W��^���� �v���C���[��`�h�݂̂Ɍ��ʂ����邩�H�@�X�y���ϐ����ђʂ��邩�ǂ����H
#�͈͂�caster����̑��΃p�X�@�_���[�W����Ƌ����ɂ��␳
#�_���[�W��^����ő僆�j�b�g���H�@�񕜂��ł���悤�ɁH
#�X�^���h�o�C���j�b�g�ɂ͌��ʂ��o�Ȃ��悤��
#iBorder�͈Ӗ��̂Ȃ��ϐ��@�������������ČĂяo���ۂɂ�₱�����Ă��傤���Ȃ������̂ŁA��؂蕶�������
#bTrialCalc��True�̂Ƃ��̓_���[�W��or�񕜗ʂ̍��v���v�Z���ĕԂ�
def changeDamage(squeaList,caster,minDamage,maxDamage,iLimitDamage,bPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,iDistanceCorrect,iSpecial=0,bTrialCalc = False,bSpell = False):
	iTrialCalcNum = 0
	damageUnitList = []
	
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if isPlot(iX,iY):
			iNumKOTohoUnit = 0
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
					iNumKOTohoUnit = iNumKOTohoUnit + 1
				pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
				pTeam = gc.getTeam(caster.getTeam())
				bFlag = False #�_���[�W��^���鏊���ł��邩�ǂ����̃`�F�b�N
				if bFriend and caster.getTeam() == pUnit.getTeam():
					bFlag = True
				if bNeutral and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == False:
					bFlag = True
				if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
					bFlag = True
				if bFlag:
					bFlag = False
					if pUnit.isHuman() and bPlayer:
						bFlag = True
					if pUnit.isHuman() == False and bAI:
						bFlag = True
					
					if iSpecial == 5: #�ނ炳�p�@�D�����j�b�g�ȊO�ɂ͖���
						if pUnit.getDomainType() != gc.getInfoTypeForString('DOMAIN_SEA'):
							bFlag = False
					
					if bFlag:
						bFlag = False
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if bToho and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
								bFlag = True
						else:
							if bGeneral:
								bFlag = True
								
						if bFlag: #�_���[�W�ʂ̌v�Z
							if minDamage == maxDamage:
								iDamage = minDamage
							else:
								if minDamage >= 0: #�_���[�W�̂Ƃ�
									iDamage = minDamage
									iDamage = iDamage + gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
								else: #�񕜂̂Ƃ�
									iDamage = maxDamage
									iDamage = iDamage - gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
							if iSpecial == 2: #�߁[���p
								iDamage -= pUnit.countAutoHeal()
							if iSpecial == 3: #�������p
								iDamage = int(pUnit.getExperience() * ( caster.countCardAttackLevel() * 0.1 + 1  ) )
							
							if bAntiSpellBarrier == False:
								iDamage = iDamage * (100 - countSpellTolerance(pUnit)) / 100
							
							#�����ɂ��␳
							if iDistanceCorrect == 1: #�ς����X�y�J�p
								#�g�p�҂ƑΏێ҂Ƃ̋��������[�N���b�h�����ŋ��߂�
								iDistance = math.sqrt(  (caster.getX()-pUnit.getX())**2 + (caster.getY()-pUnit.getY())**2 )
								iDamage = iDamage * (  ( math.sqrt( (caster.getLevel()**2) * 2) - iDistance  )  / math.sqrt( (caster.getLevel()**2) * 2)    )  
								iDamage = int(iDamage)
								
							if bPercent: #�����_���[�W���ǂ���
								if minDamage >= 0: #�_���[�W�̂Ƃ�
									iDamage = (100 - pUnit.getDamage()) * iDamage/100
								else:
									iDamage = pUnit.getDamage() * iDamage / 100
							
							if minDamage >= 0: #�_���[�W�̂Ƃ�
								if (100-pUnit.getDamage()) <= iLimitDamage:
									iDamage = 0
								if 100 - pUnit.getDamage() - iDamage <= iLimitDamage and (100-pUnit.getDamage()) >= iLimitDamage:
									iDamage = (100-pUnit.getDamage()) - iLimitDamage
							else: #�񕜂̂Ƃ�
								if (100-pUnit.getDamage()) >= iLimitDamage:
									iDamage = 0
								if 100 - pUnit.getDamage() - iDamage >= iLimitDamage and (100-pUnit.getDamage()) <= iLimitDamage:
									iDamage = (100-pUnit.getDamage()) - iLimitDamage
							
							if iSpecial == 4: #�Ă�g���b�v�p
								if gc.getGame().getSorenRandNum(100,"Tewi Trap") < 50:
									#pUnit.changeDamage(iDamage,caster.getOwner())
									damageUnitList.append( [pUnit,iDamage] )
							else:
								iTrialCalcNum = iTrialCalcNum + iDamage
								if bTrialCalc == False:
									#pUnit.changeDamage(iDamage,caster.getOwner())
									damageUnitList.append( [pUnit,iDamage] )
								
							if iSpecial == 1: #�����p
								if pUnit.getDamage() + iDamage >= 100:
									#caster.changeExperience(1,-1,False,False,False)
									gc.getPlayer(caster.getOwner()).changeGold(5)
	
	
	
	if bTrialCalc:
		if iTrialCalcNum < 0:
			iTrialCalcNum = 0 - iTrialCalcNum
		return iTrialCalcNum
	
	#���ۂ̃_���[�W�v�Z
	for item in damageUnitList:
		item[0].changeDamage(item[1],caster.getOwner())
	
	##caster�ւ�Power�Q�C�� �_���[�W�n�̂Ƃ��̂�
	#if minDamage >= 0 and maxDamage>=0:
	#	#����MOD�ǋL����
	#	#�����X�y���̏ꍇ�APower�͉񕜂��Ȃ��悤��
	#	if bFlag:
	#		if iSpecial == 1:
	#			iBase = 1
	#			caster.setPower( caster.getPower() + iBase  )
	#	
	#	#��l�̌v�Z
	#		else:
	#			iBase = (minDamage + maxDamage)/2 * 30.0
	#			if bSpell:
	#				iBase = iBase * 5
	#			if iBase == 0:
	#				iBase = 1
	#			caster.setPower( caster.getPower() + ( 0.5 * iTrialCalcNum / iBase  )  )
	
	
#���i�t�^�֐�
def setPromotion(squeaList,caster,sPromotion,bSet,iPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,onEffect=0,iSpecial=0,bGain=False,bSpell=False,iBorder3=0,iTurnPromo=0):
	iPromotion = gc.getInfoTypeForString(sPromotion)
	iUnitNum = 0
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if isPlot(iX,iY):
			iNumKOTohoUnit = 0
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
					iNumKOTohoUnit = iNumKOTohoUnit + 1
				pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
				pTeam = gc.getTeam(caster.getTeam())
				bFlag = False #���i��^���鏊���ł��邩�ǂ����̃`�F�b�N
				if bFriend and caster.getTeam() == pUnit.getTeam():
					bFlag = True
				if bNeutral and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == False:
					bFlag = True
				if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
					bFlag = True
				if bFlag:
					bFlag = False
					if pUnit.isHuman() and bPlayer:
						bFlag = True
					if pUnit.isHuman() == False and bAI:
						bFlag = True
					
					if bFlag:
						bFlag = False
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if bToho and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
								bFlag = True
						else:
							if bGeneral:
								bFlag = True

						if bFlag: #�m���ŏ��i�̕t�^or���D
							
							iPer = iPercent
							if bAntiSpellBarrier == False:
								iPer = iPercent * (100 - countSpellTolerance(pUnit)) / 100
							
							if iSpecial == 4: #���e�BPhan�X�y���p
								if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
									iPer = iPer * 3
								if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
									iPer = iPer * 2
							
							if gc.getGame().getSorenRandNum(100, "spellcard cast") < iPer:
								if iSpecial == 3: #�����Phan�X�y���p
									if ( (gc.getInfoTypeForString('UNIT_CIRNO1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_CIRNO6')  ) or
										pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN')  ):
										pUnit.setHasPromotion(iPromotion,bSet)
								else:
									pUnit.setHasPromotion(iPromotion,bSet)
									iUnitNum = iUnitNum+1
								if onEffect == 1:
									point = pUnit.plot().getPoint()
									CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
									CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
								if iSpecial == 1: #���~���APhan�X�y���p
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')):
										pUnit.changeDamage(-caster.countCardAttackLevel()/2,caster.getOwner())
								if iSpecial == 2: #�䂩���X�y�J�p
									pUnit.setDanmakuKekkai(0,caster.countCardAttackLevel()/4 + 1)
									pUnit.setImmobileTimer(1)
								if iSpecial == 5: #�������X�y�J�p
									pUnit.finishMoves()
								if iSpecial == 6: #�Ƃ�Ђ�Phan�X�y���p
									pUnit.setImmobileTimer(1)
								#�����������E����MOD�ǋL
								#���Ȃ݂ɑ��������������ŊǗ�����������̗p
								if iTurnPromo >= 0:
									pUnit.setNumTurnPromo( pUnit.getNumTurnPromo() + iTurnPromo )
	
	#caster�ւ�Power�Q�C��
	#���̍ۂ���������bGain�͑S��False�ɂ���H
	if bGain: 
		#��l�̌v�Z
		iBase = iPercent * 30.0 / 100.0
		if bSpell:
			iBase = iBase * 5
		caster.setPower( caster.getPower() + ( 0.5 * iUnitNum / iBase  )  )


#�e���ϐ����J�E���g
def countSpellTolerance(pUnit):
	
	return pUnit.countSpellTolerance()

#AI�̓�Փx�␳�����߂�
def getHandicap():
	
	Handi = 0;
	for i in range(19):
		pPlayer = gc.getPlayer(i)
		if pPlayer.isHuman() == True:
			if Handi < pPlayer.getHandicapType():
				Handi = pPlayer.getHandicapType()
	return Handi


#AI�̃X�y���g�p
def AISpellCast(caster):
	
	CAL = caster.countCardAttackLevel()
	
	if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_AI_NOT_SPEL_CAST')):
		return False
	
	#AI�ɂ��X�y�J�g�p
	
	Spells = SpellInfo.spells
	canSpellList = []
	
	#�g�p�\���]���O�ȏ�̃X�y���𔲂��o��
	for i in range( len(Spells) ):
		Spell = Spells[i]
		if Spell.isVisible(caster) and Spell.isAbled(caster):
			EstimatePoint = Spell.estimate(caster) #�]���l���g�p�m��
			if EstimatePoint > 0:
			
				#Power�̎c�ʂ⏸�i���[�g�ɂ���ĕ]���l�𑝌�����
				if caster.getPower()<2:
					EstimatePoint = EstimatePoint * 0.7
				elif caster.getPower()<3:
					EstimatePoint = EstimatePoint * 0.8
				elif caster.getPower()<4:
					EstimatePoint = EstimatePoint * 0.9
				
				if caster.getAIPromotionRoute() == 1: #COMBAT
					EstimatePoint = EstimatePoint * 0.15
				if caster.getAIPromotionRoute() == 2: #STG
					EstimatePoint = EstimatePoint * 0.30
				
				canSpellList.append([i,EstimatePoint])
	
	#�]���l�ō~���Ƀ\�[�g
	for i in range( len(canSpellList) ):
		for j in range(i+1,len(canSpellList)):
			if canSpellList[i][1] < canSpellList[j][1]:
				temp = canSpellList[i]
				canSpellList[i] = canSpellList[j]
				canSpellList[j] = temp
	
	#�]���l�̍������Ɏg�p����
	for i in range(len(canSpellList)):
		if gc.getGame().getSorenRandNum(100,"AI Spell cast") < canSpellList[i][1]:
			if Spells[ canSpellList[i][0] ].cast(caster):
				#�����������E����MOD�ǋL
				#�X�y���̏����ύX�ɔ��������ύX@gforest_shade������
				#iNum = canSpellList[i][0]+5
				iNum = gc.getInfoTypeForString( Spells[ canSpellList[i][0] ].getName() )
			#	if iNum <= gc.getInfoTypeForString("SPELLCARD_MIMIMIKO1_2"): #�X�y�J�ł����
				caster.setNumCastSpellCard( caster.getNumCastSpellCard() + 1 )
				if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
					caster.setNumSpellCardBreakTime( 2 )
				CyInterface().addImmediateMessage(gc.getUnitInfo(caster.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;","")
				
				return True



	
#�ėp�����֐�(��s�����͂����ň���Ȃ�)
def RevivalUnit(pRevivalUnit,pKilledUnit):
	
	
	pRevivalUnit.changeExperience(pKilledUnit.getExperience(),-1,false,false,false)
	pRevivalUnit.changeLevel(pKilledUnit.getLevel()-1)
	
	pRevivalUnit.setNumCastSpellCard(pKilledUnit.getNumCastSpellCard())
	pRevivalUnit.setNumAcquisSpellPromotion(pKilledUnit.getNumAcquisSpellPromotion())
	pRevivalUnit.setSinraDelayTurn(pKilledUnit.getSinraDelayTurn())
	pRevivalUnit.setNumTransformTime(pKilledUnit.getNumTransformTime())
	pRevivalUnit.setSpecialNumber(pKilledUnit.getSpecialNumber())
	
	pRevivalUnit.setDanmakuKekkai(pKilledUnit.getNowDanmakuKekkai(),pKilledUnit.getMaxDanmakuKekkai() )
	pRevivalUnit.setAIPromotionRoute(pKilledUnit.getAIPromotionRoute())
	pRevivalUnit.setPower( pKilledUnit.getPower())
	
	for i in range(3):
		pRevivalUnit.setNumPowerUp(i,pKilledUnit.getNumPowerUp(i));
	
	
	#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if pKilledUnit.isHasPromotion(iPromotion):
			pRevivalUnit.setHasPromotion(iPromotion,True)



#���镶�����ؑ��ȊO�̕����Ɛ푈��Ԃɂ��邩�ǂ������`�F�b�N
def isWar(iPlayer):

	pTeam = gc.getTeam(iPlayer)
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	for i in range(iNumTeam):
		ppTeam = gc.getTeam(i)
		if ppTeam.isBarbarian() == False:
			if pTeam.isAtWar(i):
				return True
	
	return False

#�����������E����MOD�ǋL
#�n�`���P�̃A�b�v�O���[�h����

def isImprovementUpgrade(caster,pPlot):
	
	iX = pPlot.getX()
	iY = pPlot.getY()
	spellFlag = False

	if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ):
		#�e���t�H�[�~���O�n��
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_PLAIN_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/plains.dds',ColorTypes(11),iX,iY,True,True)
	
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_GRASS_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
		
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL'):
			pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_HILL_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/hill.dds',ColorTypes(11),iX,iY,True,True)
			
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND'):
			pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FLATLAND_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
			
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FOREST'):
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_REGENERATION_FOREST'), 1)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FOREST_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/terrainfeatures/forest.dds',ColorTypes(11),iX,iY,True,True)

	if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
		#�e���t�H�[�~���O�n��
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_PLAIN_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/plains.dds',ColorTypes(11),iX,iY,True,True)
	
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_GRASS_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
		
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL'):
			pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_HILL_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/hill.dds',ColorTypes(11),iX,iY,True,True)
			
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND'):
			pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FLATLAND_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
			
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FOREST'):
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_REGENERATION_FOREST'), 1)
			pPlot.setImprovementType(-1)
			spellFlag = True
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FOREST_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/terrainfeatures/forest.dds',ColorTypes(11),iX,iY,True,True)

		#�����n��
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_COTTAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_HAMLET'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_HAMLET'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_VILLAGE'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_VILLAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TOWN'))
			spellFlag = True
		
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_COTTAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_VILLAGE'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_VILLAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_TOWN'))
			spellFlag = True

		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_COTTAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_HAMLET'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_HAMLET'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_VILLAGE'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_VILLAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_TOWN'))
			spellFlag = True
		
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_COTTAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_HAMLET'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_HAMLET'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_VILLAGE'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_VILLAGE'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_TOWN'))
			spellFlag = True
	
		#�Ԓd
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_2'))
			spellFlag = True
		elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_2'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3'))
			spellFlag = True
		
		#����
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RYUKETU'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_DAIRYUKETU'))
			spellFlag = True
	
	if spellFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False )
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False )

##### </written by F> #####
