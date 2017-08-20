## Sid Meier's Civilization 4'
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import sys

##### <written by F> #####
import SpellInfo
import TohoUnitList
import Functions
##### </written by F> #####
import codecs

# globals
gc = CyGlobalContext()
##### <written by F> #####
#�f�o�b�O�pprint��
#�����������E����MOD�ǋL
#�����͂悭�킩��Ȃ��G���[�ւ̑Ώ��B�L�q�����𗬗p���FfH Age of Ice�Ɠ���ɂ���
#�f�o�b�O�p�̂��ߕK�v�ɂȂ�����R�����g�A�E�g���O��
logInited = False
def initLog():
	global logInited
	#helpFile=file("debuglog.txt", "w")
	helpFile=codecs.open('debuglog.txt', 'w', 'shift_jis')
#	sys.stdout=helpFile
	sys.stdout.write("loaded\n")
#	sys.stdout.flush()
	logInited = True
def doprint(str):
	#cd sys.stderr.write(str)
	if not logInited:
		initLog()
	sys.stdout.write(str)
	sys.stdout.write("\n")
#	sys.stdout.flush()
##### </written by F> #####

class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self): 
		pass
	
	def isVictoryTest(self):
		if ( gc.getGame().getElapsedGameTurns() > 10 ):
			return True
		else:
			return False

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		#����MOD�ǋL
		#�g���ق̃��j�b�g�R�X�g��������
		pPlayer = gc.getPlayer(ePlayer)
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_KOUMAKAN")) == 1:
			return  -pPlayer.calculateUnitCost() /2
		#����MOD�ǋL�����܂�
		
		#����MOD�ǋL�����܂�
		return 0

	def createBarbarianCities(self):
		return False
		
	def createBarbarianUnits(self):
		return False
		
	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]
		return False
		
	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH
	
	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList
		return True
	
	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList
		#����MOD�ǋL
		#BC1000�N�𒴂���܂ł͐��z���s��
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_PEACE_OF_BC1000')):
			iGameTarn = gc.getGame().getGameTurn()
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				if iGameTarn < 250:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				if iGameTarn < 120:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				if iGameTarn < 75:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				if iGameTarn < 50:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				if iGameTarn < 43:
					return False
		#����MOD�ǋL�����܂�
		
		return True
	
	def skipProductionPopup(self,argsList):
		pCity = argsList[0]
		return False
		
	def showExamineCityButton(self,argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]		
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		
		##### <written by F> #####
		#�S�ẴA�N�V�����������ɂ��Ă�����ۂ��H
		#�X�y���A�N�V�����݂̂�߂܂��Ď��s������
		
#		doprint('cannotHandleAction In, ActionNumber:%i' %iAction)
		spell = SpellInfo.getSpellFromAction(iAction) #get the spell back from the number
#		doprint("action: %s %i %i %i"  %(gc.getActionInfo(iAction).getButton(),iAction,bTestVisible,CvMainInterface.g_checkingActive))
		if(spell == None):
			return False
		#doprint('This Action is spell, ActionNumber:%i' %iAction)
		#return bTestVisible
#		doprint('1')
		if(bTestVisible):
		#	doprint("spell is not visible")
			return spell.isInvisible()
#		doprint('2')
		#if(CvMainInterface.g_checkingActive):
		#	doprint('g_checkingActive is False')
		#	return spell.isDisabled()
#		doprint('3')
		doprint('Spell cast')
		spell.cast()
		doprint('cannotHandleAction In, ActionNumber:%i' %iAction)
		#for i in range(633):
		#	ActionInfo = gc.getActionInfo(i)
			#pActionInfo = ActionInfo(0)
			#doprint("button: %s" %(pActionInfo.getButton()))
			#doprint("for %i: %s" % (i,str(gc.getActionInfo(i))))
#		return True
		return False
		
		##### </written by F> #####
		
		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		pTeam = gc.getTeam(pPlayer.getTeam())

		#����MOD�ǋL����

		#AI���n�`���P���l������ہA�{�����ݏo���Ȃ�����UI���l���ɓ���Ă��邩������Ȃ�
		#�Ȃ̂ŃV�X�e����A�ǂ��撣���Ă�������UI�ȊO�͌��ݏo���Ȃ��悤�ɂ���
		#�ǋL�F�R�[�h�ύX�B����Ă鎖���̂͂قړ��������A���ꂼ���UI�̌��ɂȂ�n�`���P��NG�ɁB
		#���ʂ����邩�ǂ����͒m���
		
		#�i���������Ȃ��Ă����v���Ƃ͎v�����A�O�ׁ̈j�e���t�H�[�~���O�n�_�~�[�r���h�͑S��python����NG��
		if gc.getInfoTypeForString('BUILD_TERRAFORM_PLAIN') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TERRAFORM_FLOOD'):
			return 0
		
		#�g���ق̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ENGLAND'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_EIENTEI_FOREST_PRESERVE'):
				return 0
			if gc.getInfoTypeForString('BUILD_HAKUGYOKUROU_QUARRY') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FARM'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINERY'):
				return 0

		#���ʘO�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
				return 0
			if gc.getInfoTypeForString('BUILD_NINGENNOSATO_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_QUARRY'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINDMILL'):
				return 0

		#�X���A���̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HAKUREIJINJA_PLANTATION'):
				return 0
			if gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FORT') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_LUMBERMILL'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_PASTURE'):
				return 0

		#�i�����̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
			if gc.getInfoTypeForString('BUILD_KOUMAKAN_WINERY') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KISHINJOU_WINERY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_PLANTATION'):
				return 0

		#�d���̎R�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HYOUSEIRENGOU_PASTURE'):
				return 0
			if gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FORT'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_FARM'):
				return 0

		#����_�Ђ̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_NINGENNOSATO_WATERMILL'):
				return 0
			if gc.getInfoTypeForString('BUILD_HYOUSEIRENGOU_LUMBERMILL') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FOREST_PRESERVE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_PLANTATION'):
				return 0

		#�n��a�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
				return 0
			if gc.getInfoTypeForString('BUILD_SEIRENSEN_MINE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WELL'):
				return 0

		#���@�D�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_CHIREIDEN_WELL'):
				return 0
			if gc.getInfoTypeForString('BUILD_SHINREIBYOU_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_MINE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_CAMP'):
				return 0

		#�_��_�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_SEIRENSEN_CAMP'):
				return 0
			if gc.getInfoTypeForString('BUILD_KISHINJOU_WORKSHOP') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			

		#�P�j��̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_SHINREIBYOU_ROAD'):
				return 0
			if gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINERY'):
				return 0
				
		#���̓s�̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KISHINJOU_WINERY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_QUARRY'):
				return 0

		#�l�Ԃ̗��̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HAKUGYOKUROU_WINDMILL'):
				return 0
			if gc.getInfoTypeForString('BUILD_HAKUREIJINJA_FOREST_PRESERVE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WATERMILL'):
				return 0
			
		#�ؑ��̏ꍇ
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0

		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def CheckPureSake(self, pPlayer, argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlot = gc.getMap().plot(iX,iY)
		if pPlayer.getTeam() == pPlot.getTeam():
			#�ȉ��S��UI�̏ꍇ�܂�
			if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
				#����
				if iBuild == gc.getInfoTypeForString('BUILD_NINGENNOSATO_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_SHINREIBYOU_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_TOWN')):
						return 1
				#�_��
				if iBuild == gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3')):
						if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_4'):
							return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YOUKAINOYAMA_FARM'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
						return 1
				#�H�[
				if iBuild == gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CHIREIDEN_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_WORKSHOP'):
						return 1
			if pPlot.isCity():
				#�_��
				if iBuild == gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3')):
						if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_4'):
							return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YOUKAINOYAMA_FARM'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
						return 1
				#�H�[
				if iBuild == gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CHIREIDEN_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_WORKSHOP'):
						return 1
		
		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can
		
		#����MOD�ǋL����

	def cannotFoundCity(self,argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False

	def cannotSelectionListMove(self,argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]
		return False

	def canResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		
		##### <written by F> #####
		#AI���{���������Ă͂����Ȃ����̂��������Ă���C������
		#�������ƂɁA���ꂼ��̕����ȊO�̓����e�N�͌����ł��Ȃ��悤�ɂ���
		
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		
		#�g���ق̂Ƃ�
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ENGLAND'):
			if gc.getInfoTypeForString('TECH_HAKUGYOKUROU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#���ʘO
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_AKAIKIRI'):
				return True
			if gc.getInfoTypeForString('TECH_HYOUSEIRENGOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#�X���A��
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_BORDER_OF_LIFE'):
				return True
			if gc.getInfoTypeForString('TECH_EIENTEI') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#�i����
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_SIZENNOKYOUI'):
				return True
			if gc.getInfoTypeForString('TECH_YOUKAINOYAMA') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#�d���̎R
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TUKIKARANOSISHA'):
				return True
			if gc.getInfoTypeForString('TECH_HAKUREIJINJA') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#����_��
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_MORIYANOOUKOKU'):
				return True
			if gc.getInfoTypeForString('TECH_CHIREIDEN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#�n��a
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_HAKUREIDAIKEKKAI'):
				return True
			if gc.getInfoTypeForString('TECH_SEIRENSEN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#���@�D
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO'):
				return True
			if gc.getInfoTypeForString('TECH_SHINREIBYOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#�_��_
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TEACHING_OF_MEIREN'):
				return True
			if gc.getInfoTypeForString('TECH_KISHINJOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#�P�j��
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_HOSIHURU_SHINREIBYOU'):
				return True
			if gc.getInfoTypeForString('TECH_TUKI_NO_MIYAKO') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#���̓s
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_MUGENNOTIKARA'):
				return True
			if gc.getInfoTypeForString('TECH_KEINENOIRAI') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#�l�Ԃ̗�
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TUKI_NO_MIYAKO'):
				return True
		
		##### </written by F> #####
		
		return False

	def canDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		
		#����MOD�ǋL����
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		pTeam = gc.getTeam(pPlayer.getTeam())
		#�w���҂킩�����P�̏ꍇ�A���w�擾�Ő[�C�̋��x�z�ҍ̗p�\
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_WAKASAGIHIMELIST')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_OPTICS')):
				if eCivic == gc.getInfoTypeForString('CIVIC_FAITH_CTHULHU'):
					return True
		
		#�W���u���̏ꍇ�A�����ȍ~�ɓ���Ɩ������Ŋ������̗p�\
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
			if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_ANCIENT'):
				if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_CLASSICAL'):
					if eCivic == gc.getInfoTypeForString('CIVIC_BUREAUCRACY'):
						return True
		
		#����MOD�ǋL���������܂�
		
		return False

	def cannotDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		
		#����MOD�ǋL����
		
		#�s������
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		eTeam = gc.getTeam(pPlayer.getTeam())
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_PYRAMID")) == 1:
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
				return False

			elif eCivic == gc.getInfoTypeForString('CIVIC_ZYUUSHICHIZYO_KENPOU'):
				return True
		
		#�S�[���f���������\����
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_SHWEDAGON_PAYA")) == 1:
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
				return False
			elif eCivic == gc.getInfoTypeForString('CIVIC_PURE_SAKE'):
				return True
		
		#����MOD�ǋL���������܂�
		
		return False
		
	def canTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		
		#����MOD�ǋL����
		
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eUnitClass = gc.getUnitInfo(eUnit).getUnitClassType()
		#�w���҉e�T�̏ꍇ�A�j�z���I�I�J�~�쐬�\����
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_KAGEROULIST')):
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_NIHONOOKAMI'):
				return True
		
		#�n��a���݌�A��O�̊�쐬�\����
		if pTeam.getProjectCount(gc.getInfoTypeForString("PROJECT_CHIREIDEN")) == 1:
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_3RDEYE'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_3RDEYE')) < 1:
					return True
		
		#���񖳂��I�v�V�����̏ꍇ�A�������͘J���҂��쐬�ł���悤��
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_ESPIONAGE')):
			iCiv = pPlayer.getCivilizationType()
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_WORKER'):
					return True
		
		#�P�j��E���ۂ̎��@-��̏���
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_STEEL')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_KOREAN_HWACHA'):
						return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				if not (pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUNPOWDER'))):
					if pCity.hasBonus(gc.getInfoTypeForString('BONUS_HORSE')) and pCity.hasBonus(gc.getInfoTypeForString('BONUS_IRON')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_BYZANTINE_CATAPHRACT'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_RIFLING')):
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_ENGLISH_REDCOAT'):
						return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
					if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_ADVANCED_FLIGHT')):
						if pCity.hasBonus(gc.getInfoTypeForString('BONUS_HORSE')):
							if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_RUSSIA_COSSACK'):
								return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ROBOTICS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
					if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_MECH'):
							return True
		
		#�Ԍ���n���Z���^�[�����݂����s�s�ł͓���j���Y�\��
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CHIKACENTER")):
			if gc.getGame().isNukesValid() == True:
				if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_UTSUHO_2'):
							return True
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_TACTICAL_UTSUHO_2'):
							return True
		
		return False

	def cannotTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		
		#����MOD�ǋL����
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eUnitClass = gc.getUnitInfo(eUnit).getUnitClassType()
		
		#�P�j��E���ۂ̎��@-��̏���
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_CATAPULT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KNIGHT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_RIFLING')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_RIFLEMAN'):
					return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_CAVALRY'):
						return True
		
		#�u���͂̉�����v�擾�ŏ��l�������c���쐬�s�\��
		#�}���`�␳�I�v�V���������쐬�s��
		if pTeam.isHasTech(gc.getInfoTypeForString('TECH_KAISYUUKI')) or gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KOBITO_TYOUSAHEIDAN'):
				return True
		
		#�Ԍ���n���Z���^�[�����݂����s�s�ł͒ʏ�j�����X�g���珜���悤��
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CHIKACENTER")):
			if gc.getGame().isNukesValid() == True:
				if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_ICBM'):
							return True
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_TACTICAL_NUKE'):
							return True
		
		#���������w���҂͎��g�̓������j�b�g�̗D�搶�Y��������
		for i in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(i)
			iCiv = pPlayer.getCivilizationType()
		
		#���̏���
		#�u����_�Ђ����v���������ɂ���ꍇ�A�d���̎R�ł������Y�֎~
			if eUnit == gc.getInfoTypeForString('UNIT_SUIKA0_YOUKAI'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUIKA')) == True:
					return True
		#�u�d���̎R�����v���������ɂ���ꍇ�A����_�Ђł������Y�֎~
			if eUnit == gc.getInfoTypeForString('UNIT_SUIKA0'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUIKA')) == True:
					return True
		
		#���̏���
		#�u���ʘO�̎��v���������ɂ���ꍇ�A����_�Ђł͎����Y�֎~
			if eUnit == gc.getInfoTypeForString('UNIT_YUKARI0_HAKUREI'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKARI')) == True:
					return True
		#�u����_�Ђ̎��v���������ɂ���ꍇ�A���ʘO�ł͎����Y�֎~
			if eUnit == gc.getInfoTypeForString('UNIT_YUKARI0'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKARI')) == True:
					return True
		
		return False

	def canConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		
		#����MOD�ǋL����
		
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
		
		# �쐬���̌������̓O���[�A�E�g
		if not bTestVisible and not bContinue:
			if pCity.getFirstBuildingOrder(eBuilding) != -1:
				return False

		#�P�j��E���ۂ̎��@-���̏���
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
				if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_GROCER')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_PERSIAN_APOTHECARY'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ENGINEERING')):
				obsoleteTech = gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KISHINJOU_SPANISH_CITADEL")).getObsoleteTech()
				if ( pTeam.isHasTech(obsoleteTech) == false or obsoleteTech == -1 ):
					if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_WALL_ISSUN')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_CASTLE')):
							if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL')):
								if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_SPANISH_CITADEL'):
									return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ECONOMICS')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_HARBOR')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_PORTUGAL_FEITORIA'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
				if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_FACTORY')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_GERMAN_ASSEMBLY_PLANT'):
							return True
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_JAPANESE_SHALE_PLANT'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_REFRIGERATION')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_AMERICAN_MALL'):
								return True
			#�����Ɛ���/�������쐬�\��
			#���łɍH�ƒc�n��
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_INDUSTRIALISM')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_INDUSTRIAL_PARK')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_INDUSTRIAL_PARK'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_PLASTICS')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_HYDRO_PLANT')):
						pPlot = pCity.plot()
						if pPlot.isRiver ():
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_HYDRO_PLANT'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_NUCLEAR_PLANT')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_NUCLEAR_PLANT'):
							return True
			
		
		#�فX�̓��j�������g�̑���ɃX�e���쐬�\
# 		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_BENBENLIST")):
# 			obsoleteTech = gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KISHINJOU_ETHIOPIAN_STELE")).getObsoleteTech()
# 			if ( pTeam.isHasTech(obsoleteTech) == false or obsoleteTech == -1 ):
# 				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')):
# 					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_OBELISK')):
# 						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_ETHIOPIAN_STELE')):
# 							if eBuilding == gc.getInfoTypeForString('BUILDING_KISHINJOU_ETHIOPIAN_STELE'):
# # #							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_ETHIOPIAN_STELE'):
# 								return True
		
		#�Љ�x�ύX���c�����I�v�V�������͓��ꍑ�A���݉\��
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_CIVIC_CHANGE_RESOLUTION')):
			if gc.getGame().isVictoryValid(gc.getInfoTypeForString('VICTORY_DIPLOMATIC')) == True:
				if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString("BUILDINGCLASS_UNITED_NATIONS_OPTION")) == 0:
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MASS_MEDIA')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_UNITED_NATIONS_OPTION'):
							return True
		
		return False

	def cannotConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		
		#����MOD�ǋL����
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
	
		#�ؑ��͌ŗL�����������݂ł��Ȃ��悤��
		#XML�ł��o���Ȃ��͂Ȃ����A�����������Ŏw�肷������ȒP��
		
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
			if gc.getInfoTypeForString('BUILDING_MONBAN') <= eBuilding and eBuilding <= gc.getInfoTypeForString('BUILDING_MAGIC_STORM'):
				return True
	
		#�P�j��E���ۂ̎��@-���̏���
		#�u��v�����ݏo���Ȃ��Ȃ鏈����������
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_GROCER'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ENGINEERING')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CASTLE'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ECONOMICS')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CUSTOM_HOUSE'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_FACTORY'):
					return True
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_COAL_PLANT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_REFRIGERATION')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_SUPERMARKET'):
					return True
					
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
				return True
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
				return True
		
		#�P�j��E���ۂ̎��@-����푈���Ŏ����Ă��܂����ꍇ�Ȃǂ̏���
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_GROCER'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CASTLE'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CUSTOM_HOUSE'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_FACTORY'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_COAL_PLANT'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_SUPERMARKET'):
				return True
		
		#�P�j��E���ۂ̎��@-��̏���
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
				return True
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
				return True
		
		#�فX�̓m�[�}�����j���쐬�s��
		# if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_BENBENLIST")):
		# 	if eBuilding == gc.getInfoTypeForString('BUILDING_OBELISK'):
		# 		return True
		
		#�A�z���i�~�j���s�s�ɑ��݂��Ă���ꍇ�A�A�z���i���j�͍쐬�s��
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_ONMYOURYOU1'):
				return True
		
		#�������̗p���Ă��Ȃ��ꍇ�A�A�z�����ݕs��
		if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_TAOISM')) == False:
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_ONMYOURYOU1'):
				return True
		
		#�Љ�x�ύX���c�����I�v�V�������͒ʏ퍑�A���ݕs��
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_CIVIC_CHANGE_RESOLUTION')):
			if gc.getGame().isVictoryValid(gc.getInfoTypeForString('VICTORY_DIPLOMATIC')) == True:
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_UNITED_NATIONS'):
					return True
		
		return False

	def canCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		
		#����MOD�ǋL����
		#�i�v�����I�v�V�������A�v���W�F�N�g�n��a�͍쐬�s��
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_PERMANENT_ALLIANCES')):
			if eProject == gc.getInfoTypeForString('PROJECT_CHIREIDEN'):
				return True
		
		#�}���n�b�^���֎~�I�v�V�������A�}���n�b�^���v��쐬�s��
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_MANHATTAN')):
			if eProject == gc.getInfoTypeForString('PROJECT_MANHATTAN_PROJECT'):
				return True
		
		return False

	def canMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		
		#�u�З��̔��h�v������s�s�͒���|�C���g���Y���\
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KATAYOKU')):
			if eProcess == gc.getInfoTypeForString('PROCESS_KATAYOKU_SPY'):
				return True
		
		return False

	def cannotMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def AI_chooseTech(self,argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		
		##### <written by F> #####
		#�����e�N��D��擾������
		
		if bFree == False:
			pTeam = gc.getTeam(gc.getPlayer(ePlayer).getTeam())
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_METAL_CASTING')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')) == False:
				return gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUNPOWDER')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')) == False:
				return gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')
		
		##### </written by F> #####
		
		return TechTypes.NO_TECH

	def AI_chooseProduction(self,argsList):
		pCity = argsList[0]
		
		##### <written by F> #####
		#�ǂ����`�h�̓��j�b�g�O����肽����Ȃ��̂ŁA�����I�ɍ�点��
		
		#doprint("AI_TEst")
		List = []
		for sTohoUnit in TohoUnitList.TohoUnitList0:
			#doprint("can AI Create %s" %sTohoUnit)
			if pCity.canTrain(gc.getInfoTypeForString(sTohoUnit),false,false):
				List.append(sTohoUnit)
		if len(List) > 0:
			iNum = gc.getGame().getSorenRandNum(len(List), "choose toho unit")
			iUnit = CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),List[iNum])
			pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, False, True)
			#doprint("AI_Created:%s" %sTohoUnit)
			
			return True
		
		##### </written by F> #####
		
		return False

	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
		return False

	def AI_doWar(self,argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self,argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]
		
		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(), gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

	def doHolyCity(self):
		return False

	def doHolyCityTech(self,argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self,argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]
		return False

	def doProduction(self,argsList):
		pCity = argsList[0]
		return False

	def doCulture(self,argsList):
		pCity = argsList[0]
		return False

	def doPlotCulture(self,argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self,argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]
		return False
	
	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False
	
	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]
		
		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")

		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100
		
		return iPillageGold
	
	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		
		pOldCity = argsList[0]
		
		iCaptureGold = 0
		
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")
		
		return iCaptureGold
	
	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList
		return True
		
	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList
		return False
		
	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		
		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		
		return iFoundValue
		
	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return true
		
	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		pPlayer = gc.getPlayer(iPlayer)
		
		#����MOD�ǋL����
		#���ς̎u���Ŕ����R�X�g-15%
		iMod = 100
		iUnitCombatType = gc.getUnitInfo(iUnit).getUnitCombatType()
		
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_JUNKOLIST')):
			if iUnitCombatType == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
				iMod -= 15
		
		return iMod
		
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)
		
		#����MOD�ǋL����
		#���ۂ̎��@�R�X�g��������
		iMod = 100
		iBuildingClass = gc.getBuildingInfo(iBuilding).getBuildingClassType()
		
		if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
			if pPlayer.getMysteryiumFlag() >= 1:
				iMod += 50*(pPlayer.getMysteryiumFlag())
		
		if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
			if pPlayer.getMysteryiumFlag() >= 1:
				iMod += 50*(pPlayer.getMysteryiumFlag())
		
		#�W���u�������͎�s�̈�ʌ����������ƈ�Y�R�X�g25%����
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
			eBuildingInfo = gc.getBuildingInfo(iBuilding)
			if not isWorldWonderClass(eBuildingInfo.getBuildingClassType()):
				if pCity.isCapital():
					iMod -= 25
		
		#����MOD�ǋL���������܂�
		return iMod
		
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod
		
	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		
		bCanUpgradeAnywhere = 0
		
		return bCanUpgradeAnywhere
		
	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
## Platypedia ##
		if eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 6781:
				if iData2 == -2:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ())
				elif iData2 == -1:
					return CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ())
				else:
					return gc.getUnitCombatInfo(iData2).getDescription()
			elif iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 6783:
				return CyTranslator().getText("TXT_KEY_MISC_RIVERS", ())
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6786:
				return gc.getVictoryInfo(iData2).getDescription()
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
			elif iData1 == 6789:
				return gc.getTraitInfo(iData2).getDescription()
			elif iData1 == 6791:
				return gc.getCultureLevelInfo(iData2).getDescription()
			elif iData1 == 6792:
				return gc.getGameSpeedInfo(iData2).getDescription()
			elif iData1 == 6793:
				return gc.getHandicapInfo(iData2).getDescription()
			elif iData1 == 6795:
				return gc.getEraInfo(iData2).getDescription()
			elif iData1 == 6796:
				if iData2 == 999:
					return CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return gc.getUpkeepInfo(iData2).getDescription()
			elif iData1 == 6797:
				return gc.getWorldInfo(iData2).getDescription()
## Tech Help Text ##
			elif iData1 == 7800:
				return gc.getTechInfo(iData2).getHelp()
## Religion Widget Text##
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
## Ultrapack ##
		return u""
		
	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList
		
		##### <written by F> #####
		#�������j�b�g�����̂t�f��p
		#�����̂��тɂ����������X�g���Ē�`����̂����ق炵���̂ŁA
		#����̍X�V��TohoUnitList.py�̕��Ƀ��X�g���ڂ��\��B
		pPlayer = gc.getPlayer(iPlayer)
		pUnit = pPlayer.getUnit(iUnitID)
		
		if gc.getInfoTypeForString('UNIT_SANAE0') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_SAGUME6') and ( gc.getInfoTypeForString('UNITCOMBAT_BOSS') == pUnit.getUnitCombatType() or gc.getInfoTypeForString('UNITCOMBAT_STANDBY') == pUnit.getUnitCombatType()):
		
			#�A�b�v�O���[�h�R�X�g�̃��X�g�@�����̐�����������΂t�f�R�X�g���ύX�\
			#�ȉ��̃R�X�g�́A�u���̃��j�b�g�ɂȂ�̂ɕK�v�ȋ��z�v�ł���A
			#�e���j�b�g��0�Ԗڂɂ͂t�f�ł��Ȃ��̂ŃR�X�g-1�ƂȂ��Ă���
			#�`�h�̏ꍇ�i�K��΂��t�f�ɂ��t�f�R�X�g�������ƂȂ��Ă��܂��̂����A
			#�܂������s���łt�f�ł��Ȃ��Ȃ��Ă����邵�A�Ƃ肠��������̓n���f�Ƃ������Ƃŕ��u
			#�L�����N�^�[�}�[�N�ɂ��t�f���z�␳�͖�������A������̋��z���D�悳���͗l
			CostList = [
						-1,  20,  20,  25,  40,  60, 90,   #���c
						-1,  20,  20,  25,  40,  60, 90,   #���~���A
						-1,  20,  20,  25,  40,  60, 90,   #������
						-1,  20,  20,  25,  40,  60, 90,   #���O��
						-1,  20,  20,  25,  40,  60, 90,   #�Ă�
						-1,  30,  20,  25,  40,  60, 90,   #�ɂƂ�
						-1,  20,  20,  25,  40,  60, 90,   #������
						-1,  20,  20,  25,  40,  60, 90,   #�t����
						-1,  20,  20,  25,  40,  60, 90,   #�悤��
						-1,  20,  20,  25,  40,  60, 90,   #�`���m
						-1,  20,  20,  25,  40,  60, 90,   #���[���
						-1,  30,  20,  25,  40,  60, 90,   #�z�K�q
						-1,  20,  20,  25,  40,  60, 90,   #�A���X
						-1,  30,  40,  50,  60,  70, 100,   #����
						-1,  30,  40,  50,  60,  70, 100,   #���[��
						-1,  20,  20,  25,  40,  60, 90,   #�p���X�B
						-1,  20,  20,  25,  40,  60, 90,   #�䂬
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #�������[�ˁ@���ۂɂt�f�͏o���Ȃ����A�֋X�ナ�X�g�ɓo�^
						-1,  20,  20,  25,  40,  60, 90,   #���
						-1,  20,  20,  25,  40,  60, 90,   #��䂱
						-1,  20,  20,  25,  40,  60, 90,   #���[�~�A
						-1,  20,  20,  25,  40,  60, 90,   #�_�ގq
						-1,  20,  20,  25,  40,  60, 90,   #�얲
						-1,  30,  40,  50,  60,  70, 100,   #�䂤��
						-1,  20,  20,  25,  40,  60, 90,   #���f�B
						-1,  20,  20,  25,  40,  60, 90,   #������
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #�����������@��������l
						-1,  20,  20,  25,  40,  60, 90,   #�ς����[
						-1,  30,  20,  25,  40,  60, 90,   #���
						-1,  20,  20,  25,  40,  60, 90,   #���ǂ�
						-1,  20,  20,  25,  40,  60, 90,   #�������[��
						-1,  20,  20,  25,  40,  60, 90,   #���Ƃ�
						-1,  20,  20,  25,  40,  60, 90,   #�~�X�e�B�A
						-1,  20,  20,  25,  40,  60, 90,   #������
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #��������
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #���т�����
						-1,  20,  20,  25,  40,  60, 90,   #�R������
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #�R��������
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #�R���т�����
						-1,  30,  40,  50,  60,  70, 100,   #����
						-1,  20,  20,  25,  40,  60, 90,   #�X�[����t���߂��
						-1,  20,  20,  25,  40,  60, 90,   #�߁[���
						-1,  30,  20,  25,  40,  60, 90,   #�䂩���
						-1,  30,  20,  25,  40,  60, 90,   #�_�Ђ䂩���
						-1,  20,  20,  25,  40,  60, 90,   #������
						-1,  20,  20,  25,  40,  60, 90,   #�Ă�
						-1,  20,  20,  25,  40,  60, 90,   #�����
						-1,  20,  20,  25,  40,  60, 90,   #�˂������
						-1,  20,  20,  25,  40,  60, 90,   #���e�B
						-1,  20,  20,  25,  40,  60, 90,   #�݂�
						-1,  30,  40,  50,  60,  70, 100,   #������
						-1,  20,  20,  25,  40,  60, 90,   #�Ȃ�
						-1,  20,  20,  25,  40,  60, 90,   #���P
						-1,  20,  20,  25,  40,  60, 90,   #���
						-1,  20,  20,  25,  40,  60, 90,   #�݂������
						-1,  20,  20,  25,  40,  60, 90,   #��
						-1,  30,  40,  50,  60,  70, 100,   #�Ђ����
						-1,  20,  20,  25,  40,  60, 90,   #�ʂ�����
						-1,  20,  20,  25,  40,  60, 90,   #�F��
						-1,  30,  20,  25,  40,  60, 90,   #�M
						-1,  20,  20,  25,  40,  60, 90,   #�j����
						-1,  20,  20,  25,  40,  60, 90,   #�z�s
						-1,  20,  20,  25,  40,  60, 90,   #�_�q
						-1,  20,  20,  25,  40,  60, 90,   #����
						-1,  20,  20,  25,  40,  60, 90,   #�ׂ�ׂ�
						-1,  20,  20,  25,  40,  60, 90,   #����
						-1,  20,  20,  25,  40,  60, 90,   #����݂傤�܂�
						-1,  30,  40,  50,  60,  70, 100,   #����
						-1,  40,  60,  80,  100,  150, 200,   #�˕P�����������j�b�g���UG���
						-1,  40,  60,  80,  100,  150, 200,   #�L�P�����������j�b�g���UG���
						-1,  20,  20,  25,  40,  60, 90,   #���[���
						-1,  20,  20,  25,  40,  60, 90,   #�����
						-1,  20,  20,  25,  40,  60, 90,   #�ǂ��
						-1,  20,  20,  25,  40,  60, 90,   #�T�O��
						]
			
			#���ゲ�Ƃ̂t�f�R�X�g�␳�@�����́��\�L�ŁA�㔼�̎���قǍ��z�ɂȂ�
			#�ꉞ�ݒ肵�����ǖ����܂ōs�����Ƃ͑��������񂶂�Ȃ����ȁE�E�E
			EraCorrectList = [
								100,  #�Ñ�
								120,  #�ÓT
								150,  #����
								200,  #���l�T���X
								300,  #�H�Ɖ�
								500,  #����
								800,  #����
							]
			
			#�Q�[�����x���Ƃ̂t�f�R�X�g�␳�@���\�L
			#��ʃ��j�b�g�̓n���}�[������ɂȂ��Ă���̂Ŗ��Ȃ��̂����A���̂܂܂��Ƒ��x�Ɋ֌W�Ȃ��ꗥ�ɂȂ邽��
			GameSpeedList = [
								200,  #�}���\��
								150,  #�D��
								100,  #����
								 67,  #�v��
								 50,  #�V��
							]
			
			#���i�ɂ��t�f�R�X�g�␳
			#�Ƃ肠������{�����10���A������5���̊���
			PromotionList = [
								['PROMOTION_TOHO_COMBAT1',10],
								['PROMOTION_TOHO_COMBAT2',10],
								['PROMOTION_TOHO_COMBAT3',10],
								['PROMOTION_TOHO_COMBAT4',10],
								['PROMOTION_TOHO_COMBAT5',10],
								['PROMOTION_TOHO_COMBAT6',10],
								['PROMOTION_TOHO_DRILL1',5],
								['PROMOTION_TOHO_DRILL2',5],
								['PROMOTION_TOHO_DRILL3',5],
								['PROMOTION_TOHO_DRILL4',5],
							]
			iNumPromotionCost = 100
			for i in range(len(PromotionList)):
				if pUnit.isHasPromotion(gc.getInfoTypeForString(PromotionList[i][0])):
					iNumPromotionCost = iNumPromotionCost - PromotionList[i][1]
			
			
			iLose = pUnit.getNumLoseCount()
			if iLose > 5:
				iLose = 5
			iNum = iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_SANAE0')
			iEra = pPlayer.getCurrentEra()
			iSpeed = gc.getGame().getGameSpeedType()
			
			
			lastUGCost =  CostList[iNum] * EraCorrectList[iEra] * GameSpeedList[iSpeed] * (120**iLose) / (100**iLose) / 100 * iNumPromotionCost / 100 / 100
			
			
			#AI�������[�h�ɂ��␳
			if pPlayer.isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
				lastUGCost = lastUGCost * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			if lastUGCost<0:
				lastUGCost = 1
				
			return lastUGCost
		
		#��C�̂t�f�R�X�g
		elif gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6') and gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <=  pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6'):
			#�������j�b�g�ƈႢ�A�ʏ�̃��j�b�g�Ɠ����悤�Ȍv�Z���@�ȉ��̃��X�g�̓n���}�[�R�X�g
			ShanghaiCost = [
								30,
								40,
								60,
								80,
								110,
								140,
							]
			
			#�Q�[�����x���Ƃ̃n���}�[�R�X�g�␳�@���\�L
			GameSpeedList = [
								200,  #�}���\��
								150,  #�D��
								100,  #����
								 67,  #�v��
								 50,  #�V��
							]
			
			#doprint('Shanghai Numberr: %i \n' %(pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')))
						
			DisHummer = ShanghaiCost[iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')] - ShanghaiCost[pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')]
			if pPlayer.isHuman() == False :
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100 * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			else:
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
		
		#�H���̂t�f�R�X�g
		elif gc.getInfoTypeForString('UNIT_HOURAI_DOLL1') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_HOURAI_DOLL6') and gc.getInfoTypeForString('UNIT_HOURAI_DOLL1') <=  pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_HOURAI_DOLL6'):
			#�������j�b�g�ƈႢ�A�ʏ�̃��j�b�g�Ɠ����悤�Ȍv�Z���@�ȉ��̃��X�g�̓n���}�[�R�X�g
			HOURAICost = [
								30,
								40,
								60,
								80,
								110,
								140,
							]
			
			#�Q�[�����x���Ƃ̃n���}�[�R�X�g�␳�@���\�L
			GameSpeedList = [
								200,  #�}���\��
								150,  #�D��
								100,  #����
								 67,  #�v��
								 50,  #�V��
							]
			
			#doprint('HOURAI Numberr: %i \n' %(pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')))
						
			DisHummer = HOURAICost[iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')] - HOURAICost[pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')]
			if pPlayer.isHuman() == False :
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100 * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			else:
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
		
		##### </written by F> #####
		
		return -1	# Any value 0 or above will be used
	
	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		
		iExperienceNeeded = 0

		# regular epic game experience		
		iExperienceNeeded = iLevel * iLevel + 1

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP
			
		return iExperienceNeeded
		
