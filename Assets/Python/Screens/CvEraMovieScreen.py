## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string
import gc as garbageCollection

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEraMovieScreen:
	"Wonder Movie Screen"
	def interfaceScreen (self, iEra):

		self.X_SCREEN = 100
		self.Y_SCREEN = 40
		self.W_SCREEN = 775
		self.H_SCREEN = 720
		self.Y_TITLE = self.Y_SCREEN + 15

		self.X_EXIT = self.X_SCREEN + self.W_SCREEN/2 - 50
		self.Y_EXIT = self.Y_SCREEN + self.H_SCREEN - 40
		self.W_EXIT = 120
		self.H_EXIT = 30

		if (CyInterface().noTechSplash()):
			return 0

		screen = CyGInterfaceScreen( "EraMovieScreen%d"%(iEra), CvScreenEnums.ERA_MOVIE_SCREEN)
		screen.addPanel("EraMoviePanel", "", "", true, true, self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.H_SCREEN, PanelStyles.PANEL_STYLE_MAIN)

		screen.showWindowBackground(True)
		screen.setRenderInterfaceOnly(False);
		screen.setSound("AS2D_NEW_ERA")
		screen.showScreen(PopupStates.POPUPSTATE_MINIMIZED, False)

		# Header...
		szHeader = localText.getText("TXT_KEY_ERA_SPLASH_SCREEN", (gc.getEraInfo(iEra).getTextKey(), ))
		szHeaderId = "EraTitleHeader%d"%(iEra)
		screen.setText(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN + self.W_SCREEN / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("EraExit%d"%(iEra), localText.getText("TXT_KEY_MAIN_MENU_OK", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

		# Play the movie
		if iEra == 1:
			szMovie = "Art/Movies/Era/Era01-Classical.dds"
		elif iEra == 2:
			szMovie = "Art/Movies/Era/Era02-Medeival.dds"
		elif iEra == 3:
			szMovie = "Art/Movies/Era/Era03-Renaissance.dds"
		elif iEra == 4:
			szMovie = "Art/Movies/Era/Era04-Industrial.dds"
		else:
			szMovie = "Art/Movies/Era/Era05-Modern.dds"

		screen.addDDSGFC("EraMovieMovie%d"%(iEra), szMovie, self.X_SCREEN + 27, self.Y_SCREEN + 40, 720, 540, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		pPlayer = gc.getPlayer(CyGame().getActivePlayer())

		iEconomyRank = 0
		iIndustryRank = 0
		iLandAreaRank = 0
		iPopulationRank = 0
		iCultureRank = 0
		iTechnologyRank = 0

		aiGroupEconomy = []
		aiGroupIndustry = []
		aiGroupLandArea = []
		aiGroupPopulation = []
		aiGroupCulture = []
		aiGroupTechnology = []

		iEconomy = pPlayer.calculateTotalYield(YieldTypes.YIELD_COMMERCE) - pPlayer.calculateInflatedCosts()
		iIndustry = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
		iLandArea = pPlayer.getTotalLand()
		iPopulation = pPlayer.getTotalPopulation()
		iCulture = pPlayer.countTotalCulture()
		iTechnology = 0

		Economyappend = aiGroupEconomy.append
		Industryappend = aiGroupIndustry.append
		LandAreaappend = aiGroupLandArea.append
		Populationappend = aiGroupPopulation.append
		Cultureappend = aiGroupCulture.append
		for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
			pCurrPlayer = gc.getPlayer(iPlayerLoop)
			if (pCurrPlayer.isAlive() and not pCurrPlayer.isBarbarian()):
				Economyappend(pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_COMMERCE) - pCurrPlayer.calculateInflatedCosts())
				Industryappend(pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION))
				LandAreaappend(pCurrPlayer.getTotalLand())
				Populationappend(pCurrPlayer.getTotalPopulation())
				Cultureappend(pCurrPlayer.countTotalCulture())

				iPlayerTechs = 0
				for iTechLoop in xrange(gc.getNumTechInfos()):
					bPlayerHasTech = gc.getTeam(pCurrPlayer.getTeam()).isHasTech(iTechLoop)
					if (bPlayerHasTech):
						iPlayerTechs += gc.getTechInfo(iTechLoop).getResearchCost()
				if (iPlayerLoop == gc.getGame().getActivePlayer()):
					iTechnology = iPlayerTechs
				aiGroupTechnology.append(iPlayerTechs)

		aiGroupEconomy.sort()
		aiGroupIndustry.sort()
		aiGroupLandArea.sort()
		aiGroupPopulation.sort()
		aiGroupCulture.sort()
		aiGroupTechnology.sort()

		aiGroupEconomy.reverse()
		aiGroupIndustry.reverse()
		aiGroupLandArea.reverse()
		aiGroupPopulation.reverse()
		aiGroupCulture.reverse()
		aiGroupTechnology.reverse()

		iEconomyRank = aiGroupEconomy.index(iEconomy) + 1
		iIndustryRank = aiGroupIndustry.index(iIndustry) + 1
		iLandAreaRank = aiGroupLandArea.index(iLandArea) + 1
		iPopulationRank = aiGroupPopulation.index(iPopulation) + 1
		iCultureRank = aiGroupCulture.index(iCulture) + 1
		iTechnologyRank = aiGroupTechnology.index(iTechnology) + 1

		szIndustryText = "%s:"%(localText.getText("TXT_KEY_CGE_ERA_INFO_INDUSTRY", ()))
		szLandAreaText = "%s:"%(localText.getText("TXT_KEY_DEMO_SCREEN_LAND_AREA_TEXT", ()))
		szPopulationText = "%s:"%(localText.getText("TXT_KEY_DEMO_SCREEN_POPULATION_TEXT", ()))
		szEconomyText = "%s:"%(localText.getText("TXT_KEY_DEMO_SCREEN_ECONOMY_TEXT", ()))
		szCultureText = "%s:"%(localText.getObjectText("TXT_KEY_COMMERCE_CULTURE", 0))
		szTechnologyText = "%s:"%(localText.getText("TXT_KEY_CGE_ERA_INFO_ADVANCED", ()))
		szText = "<font=2>%s\n%s\n%s\n%s\n%s\n%s</font>"%(szEconomyText, szIndustryText, szLandAreaText, szPopulationText, szCultureText,szTechnologyText)
		screen.addMultilineText("EraInfoString1", szText, self.X_SCREEN + 25, 625, 110, 100,WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		szRank = localText.getText("TXT_KEY_DEMO_SCREEN_RANK_TEXT", ())
		szIndustryText = "%s %d"%(szRank, iIndustryRank)
		szLandAreaText = "%s %d(%.2f%%)"%(szRank, iLandAreaRank, (iLandArea * 100.0) / gc.getMap().getLandPlots())
		szPopulationText = "%s %d(%.2f%%)"%(szRank, iPopulationRank, (iPopulation * 100.0) / gc.getGame().getTotalPopulation())
		szEconomyText = "%s %d"%(szRank, iEconomyRank)
		szCultureText = "%s %d"%(szRank, iCultureRank)
		szTechnologyText = "%s %d"%(szRank, iTechnologyRank)
		szText = "<font=2>%s\n%s\n%s\n%s\n%s\n%s</font>"%(szEconomyText, szIndustryText, szLandAreaText, szPopulationText, szCultureText,szTechnologyText)
		screen.addMultilineText("EraInfoString2", szText, self.X_SCREEN + 127, 625, 105, 100,WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		szText = "<font=2>%s</font>"%(localText.getText("TXT_KEY_CGE_ERA_INFO_TECHNOLOGY", ()))
		screen.addMultilineText("EraInfoString3", szText, self.X_SCREEN + 227, 625, 415, 20,WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addPanel("EraInfoTech", "", "", false, true, self.X_SCREEN + 230, 645, 517, 70,PanelStyles.PANEL_STYLE_STANDARD)
		screen.hide("EraInfoTech")

		ActiveTeam = gc.getPlayer(gc.getGame().getActivePlayer()).getTeam()
		ActiveTeam1 = gc.getTeam(gc.getGame().getActivePlayer())
		for iLoopTech in xrange(gc.getNumTechInfos()):
			if (not ActiveTeam1.isHasTech(iLoopTech)):
				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					LoopTeam = gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam())
					if (not LoopTeam.isTechTrading()):
						break
					if (LoopTeam.isHasTech(iLoopTech) and LoopTeam.isHasMet(ActiveTeam)):
						screen.attachCheckBoxGFC("EraInfoTech", "", CyGlobalContext().getTechInfo(iLoopTech).getButton(), "", 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, iLoopTech, ButtonStyles.BUTTON_STYLE_IMAGE)
						break
		screen.show("EraInfoTech")

		garbageCollection.collect()
		return 0

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

	def update(self, fDelta):
		return
