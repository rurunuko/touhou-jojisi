from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CvGameUtils
import SpellInfo
import TohoUnitList
import Functions

import CvScreenEnums

import math

PyInfo = PyHelpers.PyInfo
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()

def SpellCast(argsList):

	pUnit,iNum = argsList
	
	#Spell = SpellInfo.spells[iNum-5]
	#CvGameUtils.doprint(Spell.getName())
	name = gc.getAutomateInfo(iNum).getType()
	CvGameUtils.doprint("SpellCast: " + name)
	Spells = filter(lambda s: s.getName()==name, SpellInfo.getSpells())
	if Spells:
		Spell = Spells[0]
		if Spell.isVisible(pUnit) and Spell.isAbled(pUnit):
			if Spell.cast(pUnit): #cast�ɐ��������
		
				#szName = "TohoJojisiTestPanel"
				#screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				#screen.addPanel( szName, u"", u"", True, False, 300, 300, 700, 700, PanelStyles.PANEL_STYLE_HUD_HELP )
				#screen.setText( szName, "Background", u"&#24382;&#24149;&#12399;&#12497;&#12527;&#12540;&#12384;&#12380;", CvUtil.FONT_RIGHT_JUSTIFY, 380, 220, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, 1, -1 )
				#screen.hide( szName )
				#screen.show( szName )
			
				#szName = "TohoJojisiTestPanel2"
				#screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				#screen.addPanel( szName, u"", u"", True, False, 200, 200, 400, 400, PanelStyles.PANEL_STYLE_HUD_HELP )
				#screen.setImageButton( szName, gc.getUnitInfo(gc.getInfoTypeForString('UNIT_MARISA1')).getButton(), 200, 200, 56, 56, WidgetTypes.WIDGET_RESEARCH, gc.getInfoTypeForString('UNIT_MARISA1'), -1 )
				#screen.hide( szName )
				#screen.show( szName )
			
				#screen.setTextBackgroundPane( szName, gc.getInfoTypeForString("COLOR_BLACK") )
				#screen.setTextColor( szName, gc.getInfoTypeForString("COLOR_BLACK"))
		
				if iNum <= gc.getInfoTypeForString("SPELLCARD_SAGUME1_2"): #�X�y�J�ł����
					pUnit.setNumCastSpellCard( pUnit.getNumCastSpellCard() + 1 )
					if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
						pUnit.setNumSpellCardBreakTime( 2 )
						#CyInterface().addImmediateMessage(gc.getUnitInfo(pUnit.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;","")
				
					szBuffer = gc.getUnitInfo(pUnit.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;"
				for i in range(gc.getMAX_CIV_PLAYERS()):
					CyInterface().addMessage(i,True,25,szBuffer,'AS3D_spell_use',InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, gc.getUnitInfo(pUnit.getUnitType()).getButton() ,ColorTypes(0),pUnit.getX(),pUnit.getY(),True,True)
				

### p�Ŏn�܂�[p***]�͂������ɑ�����
### p�Ŏn�܂�Ȃ�[s**]��[z**]��dll���ɒu���Ă��Ă��邯��
### ����Ԃ������Ɉړ�����������ق������₷���C�͂���
### �������Ă����BXML��SPELL�����_HELP�Ǝw�肳��Ă�����̂ŁA
### []�ň͂܂�Ă��镔���̒��g��szText�ɓn���Ă���̂ŁA���߂��Đ����ŕԂ��΂悢
def getTextToSpellInt(argsList):
	
	szText, pUnit, CAL, iNum = argsList

	# [p***]�Ŏn�܂��Ă�����(���Q�[�����o�R�̂Ƃ�)�����Spellcast�̋߂��܂ł��炢�܂킵����
	if szText[0] == "p": 
		name = gc.getAutomateInfo(iNum).getType()
		CvGameUtils.doprint("getTextToSpellInt: " + name)
		Spells = filter(lambda s: s.getName()==name, SpellInfo.getSpells())
		if Spells:
			Spell = Spells[0]
			return Spell.getHelpText(szText[1:], pUnit, CAL)
		
	# ���܂ł̕\�L���ꉞ�ڐA���Ă����Ŏ󂯕t����
	elif szText[0] == "s":
		#�����n
		if CAL<17:
			output = (CAL+1)/2
		elif CAL<21:
			output = (CAL-16)+8
		elif CAL<26:
			output = (CAL-20)*2 + 12
		else:
			output = 24

		if szText[1] == "z":
			output *= int(szText[2])
		else:
			output += int(szText[1:3])
		return output
	elif szText[0] == "z":
		#�ʌn
		### (�]���̕��@�ł͂Q������������Ȃ��̂Œn����99������������)
		case = szText[1:3]
		
		if case == "01": #�������X�y�J
			output = (CAL - 8 ) *5
		elif case == "02": #�P�������X�y�J�̃n���}�[
			output = (CAL + 4 ) / 8 + 1
		elif case == "03": #�������[�˃X�y�J
			output = CAL*CAL *3 /2
		elif case == "04": #�������X�y�J�_���[�W
			output = CAL *3 /2 + 10
		elif case == "05": #�p�`�F�X�y�J�̌��ʔ͈�
			if pUnit:
				output = pUnit.getLevel()
			else:
				output = 1
		elif case == "06": #���ǂ񂰃X�y�J�̐����m��
			output = CAL *15 /2 +25
		elif case == "07": #�����X�y�J�̃_���[�W
			output = (int)(CAL * 2)
		elif case == "08": #�Ă�Phan�X�y���̃_���[�W
			if CAL<17:
				output = (output+1)/2
			elif output<21:
				output = (output-16)+ 8
			elif output<26:
				output = (output-20)*2 + 12
			else:
				output = 24
			output *= 2
			output += 10
		elif case == "09": #������Ex�X�y���̖{��
			if pUnit:
				output = pUnit.getExperience()/2
			else:
				output = 0
		elif case == "10": #�P�������Phan�X�y���̕���
			output = CAL * CAL
		elif case == "11": #�䂬Phan�X�y���̈ړ��͑�����
			output = CAL /8
			if output == 0:
				output = 1
		elif case == "12": #������Ex�X�y���̃i�C�t�̐�
			if pUnit:
				output = int(CAL * (1.5 + pUnit.getLevel()*0.1))
			else:
				output = int(CAL * (1.5 + 10*0.1))
		elif case == "13": #������Phan�X�y���̒���|�C���g
			output = int(100 * math.pow(1.3,CAL-16))
		elif case == "14": #����Phan�X�y���̃_���[�W��
			if pUnit:
				pPlayer = gc.getPlayer(pUnit.getOwner())
				output = int( pPlayer.getGold() * (CAL * 0.05) )
			else:
				output = int( 100 * (CAL * 0.05) )
		elif case == "15": #�����X�y�J�̃_���[�W��
			if pUnit:
				iZombieCount = 0
				pPlot = pUnit.plot()
				for i in range(pPlot.getNumUnits()):
					if pPlot.getUnit(i).isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY')):
						iZombieCount += 1
				if iZombieCount < 1:
					iZombieCount = 1

				output = int(  CAL * 2 *  ( 1 + math.log10(iZombieCount))  )
			else:
				output = CAL*2
		elif case == "16": #�������X�y�J�̃_���[�W�ʁi�o���l10�j
			output = int( ( CAL * 0.1 + 1 ) * 10 )
		elif case == "17": #���[�~�APhan�X�y��
			output = int(  CAL * 10 )
		elif case == "18": #�P�������X�y�J�̔�
			output = (CAL + 4 ) / 8 
		elif case == "19": #�~�X�e�B�A�X�y�J�̓s�s�����^�[��
			output = (CAL / 4 ) -2 
		elif case == "20": #��փX�L���̗d�������Ґ�
			if pUnit:
				output = pUnit.getLevel() / 4 +1
			else:
				output = 1
			if output < 0: output = 0
		elif case == "21": #����MOD�ǋL�����E��փX�y���̃_���[�W
			output =  100 - (CAL * 3 )
		elif case == "22": #�ʂ��X�y�J
			output = CAL *2 /3
		elif case == "23": #�ʂ�Ex�X�y��
			output = CAL *4 /3
		return output
	elif szText[0] == "w": #10�̈ʂŊ����ĂP�̈ʂ𑫂�
		return CAL / int(szText[1]) + int(szText[2])
	else: #�_���[�W�n�p	 [abc] ab + c*CAL
		return int(szText[0:2]) + int(szText[2])*CAL;

	return -8149


# // ���̂�������ȍ~�̎q������Python���ɓ����Ă��܂�������
# // �Ƃ肠�����ێ����ău���b�V���A�b�v��������
# ���������B
# else if(szText[0] == 's'){ //���Ҍn�p

#     if(szText[1] == 'z'){ //

#         output = CAL;
#         if(output<17){
#             output = (output+1)/2;
#         }
#         else if(output<21){
#             output = (output-16)+ 8;
#         }
#         else if(output<26){
#             output = (output-20)*2 + 12;
#         }
#         else{
#             output = 24;
#         }
#         output *= strtol(szText+2,&endstr,10);
#     }
#     else{

#         output = CAL;
#         if(output<17){
#             output = (output+1)/2;
#         }
#         else if(output<21){
#             output = (output-16)+ 8;
#         }
#         else if(output<26){
#             output = (output-20)*2 + 12;
#         }
#         else{
#             output = 24;
#         }
#         output += strtol(szText+1,&endstr,10);
#     }

# }
# else if(szText[0] == 'z'){ //���̑�

#     double iZombieCount = 0;

#     switch( strtol(szText+1,&endstr,10) ){
#     case 1: //�������X�y�J
#         output = (CAL - 8 ) *5;
#         break;
#     case 2: //�P�������X�y�J�̃n���}�[
#         output = (CAL + 4 ) / 8 + 1;
#         break;
#     case 3: //�������[�˃X�y�J
#         output = CAL*CAL *3 /2;
#         break;
#     case 4: //�������X�y�J�_���[�W
#         output = CAL *3 /2 + 10;
#         break;
#     case 5: //�p�`�F�X�y�J�̌��ʔ͈�
#         if (pUnit == NULL)
#             output = 1;
#         else
#             output = pUnit->getLevel();
#         break;
#     case 6: //���ǂ񂰃X�y�J�̐����m��
#         output = CAL *15 /2 +25;
#         break;
#     case 7: //�����X�y�J�̃_���[�W
#         output = (int)(CAL * 2);
#         break;
#     case 8: //�Ă�Phan�X�y���̃_���[�W
#         output = CAL;
#         if(output<17){
#             output = (output+1)/2;
#         }
#         else if(output<21){
#             output = (output-16)+ 8;
#         }
#         else if(output<26){
#             output = (output-20)*2 + 12;
#         }
#         else{
#             output = 24;
#         }
#         output *= 2;
#         output += 10;
#         break;
#     case 9: //������Ex�X�y���̖{��
#         if (pUnit == NULL)
#             output = 0;
#         else
#             output = pUnit->getExperience()/2;
#         break;
#     case 10: //�P�������Phan�X�y���̕���
#         output = CAL * CAL;
#         break;
#     case 11: //�䂬Phan�X�y���̈ړ��͑�����
#         output = CAL /8;
#         if(output == 0)
#             output = 1;
#         break;
#     case 12: //������Ex�X�y���̃i�C�t�̐�
#         if (pUnit == NULL)
#             output = (int)(CAL * (1.5 + 10*0.1));
#         else
#             output = (int)(CAL * (1.5 + pUnit->getLevel()*0.1));
#         break;
#     case 13: //������Phan�X�y���̒���|�C���g
#         output = (int)(100 * pow(1.3,(double)CAL-16));
#         break;
#     case 14: //����Phan�X�y���̃_���[�W��
#         if (pUnit == NULL)
#             output = (int)( 100 * (CAL * 0.05) );
#         else
#             output = (int)( GET_PLAYER(pUnit->getOwner()).getGold() * (CAL * 0.05) );
#         break;
#     case 15: //�����X�y�J�̃_���[�W��
#         if (pUnit == NULL){
#             output = CAL*2;
#         }else{
#             for (int k = 0; k < pUnit->plot()->getNumUnits();k++){
#                 if (pUnit->plot()->getUnitByIndex(k)->isHasPromotion((PromotionTypes)GC.getInfoTypeForString("PROMOTION_ZOMBIEFAIRY")) )
#                     iZombieCount++;
#             }
#             if (iZombieCount < 1)
#                 iZombieCount = 1;

#             output = (int)(  CAL * 2 *  ( 1 + log10(iZombieCount))  );
#         }
#         break;
#     case 16: //�������X�y�J�̃_���[�W�ʁi�o���l10�j
#         output = (int)( ( CAL * 0.1 + 1 ) * 10 );
#         break;
#     case 17: //���[�~�APhan�X�y��
#         output = (int)(  CAL * 10 );
#         break;
#     case 18: //�P�������X�y�J�̔�
#         output = (CAL + 4 ) / 8 ;
#         break;
#     case 19: //�~�X�e�B�A�X�y�J�̓s�s�����^�[��
#         output = (CAL / 4 ) -2 ;
#         break;
#     case 20: //��փX�L���̗d�������Ґ�
#         if (pUnit == NULL){
#             output = 1;
#         }else{
#             output = pUnit->getLevel() / 4 +1;
#         }
#         if (output < 0) output = 0;
#         break;
#     case 21: //����MOD�ǋL�����E��փX�y���̃_���[�W
#         output =  100 - (CAL * 3 );
#         break;
#     case 22: //�ʂ��X�y�J
#         output = CAL *2 /3;
#         break;
#     case 23: //�ʂ�Ex�X�y��
#         output = CAL *4 /3;
#         break;
#     default:
#         break;
# 	}
       
# }
# else if(szText[0] == L'w'){ //10�̈ʂŊ����ĂP�̈ʂ𑫂�
# 	char s[4];
# 	strncpy(s, szText, 3);
# 	s[3] = '\0';
#     output = CAL / (strtol(s+1,&endstr,10)/10) + strtol(s+2,&endstr,10);
# }
# else{ //�_���[�W�n�p  [abc] ab + c*CAL
# 	char s[4];
# 	strncpy(s, szText, 3);
# 	s[3] = '\0';
#     output = strtol(s,&endstr,10)/10 + strtol(s+2,&endstr,10)*CAL;
# }

