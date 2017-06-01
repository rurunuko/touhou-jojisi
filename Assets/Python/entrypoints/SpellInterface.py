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
			if Spell.cast(pUnit): #castに成功すれば
		
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
		
				if iNum <= gc.getInfoTypeForString("SPELLCARD_SAGUME1_2"): #スペカであれば
					pUnit.setNumCastSpellCard( pUnit.getNumCastSpellCard() + 1 )
					if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
						pUnit.setNumSpellCardBreakTime( 2 )
						#CyInterface().addImmediateMessage(gc.getUnitInfo(pUnit.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;","")
				
					szBuffer = gc.getUnitInfo(pUnit.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;"
				for i in range(gc.getMAX_CIV_PLAYERS()):
					CyInterface().addMessage(i,True,25,szBuffer,'AS3D_spell_use',InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, gc.getUnitInfo(pUnit.getUnitType()).getButton() ,ColorTypes(0),pUnit.getX(),pUnit.getY(),True,True)
				

### pで始まる[p***]はこっちに送られる
### pで始まらない[s**]や[z**]はdll内に置いてきているけど
### ぜんぶこっちに移動しちゃったほうが見やすい気はする
def getTextToSpellInt(argsList):
	
	szText, pUnit, iNum = argsList

	# [ps***]で始まっていたらSpellcastの近くまでたらいまわしする
	if szText[0] == "s": 
		name = gc.getAutomateInfo(iNum).getType()
		CvGameUtils.doprint("getTextToSpellInt: " + name)
		Spells = filter(lambda s: s.getName()==name, SpellInfo.getSpells())
		if Spells:
			Spell = Spells[0]
			return Spell.getHelpText(szText[1:], pUnit)
	else:
		return 256

