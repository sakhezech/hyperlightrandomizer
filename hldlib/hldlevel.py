import os
import re
from hldlib.hldobjects import HLDObj
from dataclasses import dataclass
from enum import Enum


@dataclass
class HLDLevel:

    name: str
    date: float
    layer_names: dict
    room_settings: dict
    object_list: list[HLDObj]
    dir_: str = ""

    @classmethod
    def from_file(cls, path: str):  # TODO: CLEAN THIS
        layer_names = {}
        object_list = []
        date = None
        room_settings = None
        name = os.path.basename(path)
        dir_ = os.path.basename(os.path.dirname(path))
        with open(path) as f:
            file = f.readlines()
        for line in file:
            if re.search(r"obj,.*?,.*?,", line):
                object_list.append(HLDObj.from_line(line))
            elif match_obj := re.search(r"layerName,(.*?),(.*?),", line):
                layer_names[match_obj.group(1)] = match_obj.group(2)
            elif match_obj := re.search(r"(?:DATE|VERSION),(.*?),", line):
                date = float(match_obj.group(1))
            elif re.search(r"bg,", line):
                room_settings = {}
                bline = line.strip().split(",")[:-1]
                bline = list(map(HLDObj._int_float_str_convert, bline))
                sketch = bline[-4:]
                bline = bline[:-4]
                while bline:
                    room_settings[bline[0]] = bline[1]
                    bline.pop(0)
                    bline.pop(0)
                room_settings[sketch[0]] = [sketch[1], sketch[2], sketch[3]]
        if date is None or room_settings is None: raise ValueError("Corrupted Level")
        return cls(date=date, layer_names=layer_names, room_settings=room_settings, object_list=object_list, name=name, dir_=dir_)

    def dump_level(self, path="") -> None:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, self.name), "w") as file:
            file.write(f"DATE,{self.date},")
            file.write("\n\t " + "\n\t ".join([f"layerName,{key},{value}," for key, value in self.layer_names.items()]))
            file.write("\n\t " + ",".join([f"{key},{value}" for key, value in self.room_settings.items() if key != "sketchalpha"])
                       + f",sketchalpha,{','.join(list(map(str, self.room_settings['sketchalpha'])))},")
            file.write("".join([obj.get_line() for obj in self.object_list]))

    class Names(str, Enum):
        def __str__(self):
            return self.value
        RM_NC_CLIFFCAMPFIRE = "rm_NC_CliffCampfire.lvl"
        RM_NC_CRUSHARENA = "rm_NC_CrushArena.lvl"
        RM_NC_NPCHATCHERY = "rm_NC_NPCHatchery.lvl"
        RM_NL_ALTARTHRONE = "rm_NL_AltarThrone.lvl"
        RM_NL_CAVEVAULT = "rm_NL_CaveVAULT.lvl"
        RM_NL_CRUSHARENA = "rm_NL_CrushArena.lvl"
        RM_NL_CRUSHARENAVAULT = "rm_NL_CrushArenaVAULT.lvl"
        RM_NL_CRUSHBACKLOOP = "rm_NL_CrushBackLoop.lvl"
        RM_NL_CRUSHTRANSITION = "rm_NL_CrushTransition.lvl"
        RM_NL_CRUSHWARPHALL = "rm_NL_CrushWarpHall.lvl"
        RM_NL_DROPARENA = "rm_NL_DropArena.lvl"
        RM_NL_DROPARENAVAULT = "rm_NL_DropArenaVAULT.lvl"
        RM_NL_DROPBLOCKCULTFIGHT = "rm_NL_DropBlockCultFight.lvl"
        RM_NL_DROPPITS = "rm_NL_DropPits.lvl"
        RM_NL_DROPSPIRALOPEN = "rm_NL_DropSpiralOpen.lvl"
        RM_NL_ENTRANCEPATH = "rm_NL_EntrancePath.lvl"
        RM_NL_GAPHALLWAY = "rm_NL_GapHallway.lvl"
        RM_NL_GAPHALLWAYVAULT = "rm_NL_GapHallwayVAULT.lvl"
        RM_NL_GAPOPENING = "rm_NL_GapOpening.lvl"
        RM_NL_JERKPOPEVAULT = "rm_NL_JerkPopeVAULT.lvl"
        RM_NL_NPCHATCHERYVAULT = "rm_NL_NPCHatcheryVAULT.lvl"
        RM_NL_RISINGARENA = "rm_NL_RisingArena.lvl"
        RM_NL_RISINGARENAVAULT = "rm_NL_RisingArenaVAULT.lvl"
        RM_NL_SHRINEPATH2VAULT = "rm_NL_ShrinePath2VAULT.lvl"
        RM_NL_STAIRASCENT = "rm_NL_StairAscent.lvl"
        RM_NL_TOBROKENSHALLOWS = "rm_NL_ToBrokenShallows.lvl"
        RM_NL_WARPROOM = "rm_NL_WarpRoom.lvl"
        RM_NX_AFTERTITAN = "rm_NX_AfterTitan.lvl"
        RM_NX_CATHEDRALENTRANCE = "rm_NX_CathedralEntrance.lvl"
        RM_NX_CATHEDRALHALL = "rm_NX_CathedralHall.lvl"
        RM_NX_CAVE01 = "rm_NX_Cave01.lvl"
        RM_NX_GAPWIDE = "rm_NX_GapWide.lvl"
        RM_NX_JERKPOPE = "rm_NX_JerkPope.lvl"
        RM_NX_LIBRARIANTABLET = "rm_NX_LibrarianTablet.lvl"
        RM_NX_MOONCOURTYARD = "rm_NX_MoonCourtyard.lvl"
        RM_NX_NORTHHALL = "rm_NX_NorthHall.lvl"
        RM_NX_SHRINEPATH = "rm_NX_ShrinePath.lvl"
        RM_NX_SHRINEPATH_2 = "rm_NX_ShrinePath_2.lvl"
        RM_NX_SPIRALSTAIRCASE = "rm_NX_SpiralStaircase.lvl"
        RM_NX_STAIRS03 = "rm_NX_Stairs03.lvl"
        RM_NX_TITANVISTA = "rm_NX_TitanVista.lvl"
        RM_NX_TOWERLOCK = "rm_NX_TowerLock.lvl"
        RM_NX_TOWERNORTH_ELEVATOR = "rm_NX_TowerNorth_Elevator.lvl"
        RM_NX_TOWERNORTH_WELL = "rm_NX_TowerNorth_Well.lvl"
        RM_EA_BOGTEMPLECAMP = "rm_EA_BogTempleCamp.lvl"
        RM_EA_CAVERNTEST = "rm_EA_CavernTest.lvl"
        RM_EA_DOCKFIGHTLAB = "rm_EA_DockFightLab.lvl"
        RM_EA_EASTOPENING = "rm_EA_EastOpening.lvl"
        RM_EA_ENTRANCE = "rm_EA_Entrance.lvl"
        RM_EA_FROGBOSS = "rm_EA_FrogBoss.lvl"
        RM_EA_L_FUNDUN_LEFTSIDE = "rm_EA_L_Fundun_leftside.lvl"
        RM_EA_L_FUNDUN_TOPRIGHT = "rm_EA_L_Fundun_topright.lvl"
        RM_EA_L_SUNKENTEMPLE = "rm_EA_L_SunkenTemple.lvl"
        RM_EA_WATERTUNNELLAB = "rm_EA_WaterTunnelLAB.lvl"
        RM_EB_BOGSTREET = "rm_EB_BogStreet.lvl"
        RM_EB_BRIDGEMODULE = "rm_EB_BridgeModule.lvl"
        RM_EB_CLEANERSHOLE = "rm_EB_CleanersHole.lvl"
        RM_EB_DEADOTTERWALK = "rm_EB_DeadOtterWalk.lvl"
        RM_EB_FLAMEDEN = "rm_EB_FlameDen.lvl"
        RM_EB_FLAMEPITLAB = "rm_EB_FlamePitLAB.lvl"
        RM_EB_MELTYFROGKEYTOWN = "rm_EB_MeltyFrogKeyTown.lvl"
        RM_EB_MELTYLEAPERARENA = "rm_EB_MeltyLeaperArena.lvl"
        RM_EB_MELTYLEAPERLABOLD = "rm_EB_MeltyLeaperLabOLD.lvl"
        RM_EB_MELTYMASHARENA = "rm_EB_MeltyMashArena.lvl"
        RM_EB_UNDEROTTERBIGRIFLERUMBLE = "rm_EB_UnderOtterBigRifleRumble.lvl"
        RM_EC_BIGBOGLAB = "rm_EC_BigBogLAB.lvl"
        RM_EC_BOGLABSMALL = "rm_EC_BogLabSmall.lvl"
        RM_EC_DOCKSLAB = "rm_EC_DocksLab.lvl"
        RM_EC_DOCKSLABVAULT = "rm_EC_DocksLabVault.lvl"
        RM_EC_EASTLOOP = "rm_EC_EastLoop.lvl"
        RM_EC_LOOPLAB = "rm_EC_LoopLAB.lvl"
        RM_EC_LOOP_VAULT = "rm_EC_Loop_Vault.lvl"
        RM_EC_NPCDRUGDEN = "rm_EC_NPCDrugDen.lvl"
        RM_EC_PLAZAACCESSLAB = "rm_EC_PlazaAccessLAB.lvl"
        RM_EC_PLAZATODOCKS = "rm_EC_PlazaToDocks.lvl"
        RM_EC_PLAZATOLOOP = "rm_EC_PlazaToLoop.lvl"
        RM_EC_SWORDBRIDGE = "rm_EC_SwordBridge.lvl"
        RM_EC_TEMPLEISHVAULT = "rm_EC_TempleIshVault.lvl"
        RM_EC_THEPLAZA = "rm_EC_ThePlaza.lvl"
        RM_EL_BIGBOG_VAULT = "rm_EL_BigBog_Vault.lvl"
        RM_EL_EASTDRIFTERVAULT = "rm_EL_EastDrifterVault.lvl"
        RM_EL_FLAMEELEVATORENTER = "rm_EL_FlameElevatorEnter.lvl"
        RM_EL_FLAMEELEVATOREXIT = "rm_EL_FlameElevatorExit.lvl"
        RM_EL_FLAMEPIT_VAULT = "rm_EL_FlamePit_Vault.lvl"
        RM_EL_FROGARENA = "rm_EL_FrogArena.lvl"
        RM_EL_FROGARENA_VAULT = "rm_EL_FrogArena_Vault.lvl"
        RM_EL_MEGAHUGELAB = "rm_EL_MegaHugeLAB.lvl"
        RM_EL_PITTOMEGA_TRAN = "rm_EL_PitToMega_Tran.lvl"
        RM_EL_TRANSITIONFROMFROGARENA = "rm_EL_TransitionFromFrogArena.lvl"
        RM_EL_WATERTUNNEL_VAULT = "rm_EL_WaterTunnel_Vault.lvl"
        RM_EV_DOCKSBRIDGE = "rm_EV_DocksBridge.lvl"
        RM_EX_BATTLEHAL = "rm_EX_BattleHAL.lvl"
        RM_EX_DOCKSCAMPFIRE = "rm_EX_DocksCampfire.lvl"
        RM_EX_TOWEREAST = "rm_EX_TowerEast.lvl"
        RM_EX_TOWEREAST_WELL = "rm_EX_TowerEast_Well.lvl"
        RM_WATEST = "rm_WAtest.lvl"
        RM_WA_CAMPFIRE = "rm_WA_Campfire.lvl"
        RM_WA_CRSYTALDESCENT = "rm_WA_CrsytalDescent.lvl"
        RM_WA_DEADWOOD = "rm_WA_Deadwood.lvl"
        RM_WA_DEADWOODS1 = "rm_WA_DeadwoodS1.lvl"
        RM_WA_ENTRANCE = "rm_WA_Entrance.lvl"
        RM_WA_ENTSWITCH = "rm_WA_EntSwitch.lvl"
        RM_WA_GROTTOX = "rm_WA_GrottoX.lvl"
        RM_WA_GROTTO_BUFFINTRO = "rm_WA_Grotto_buffIntro.lvl"
        RM_WA_MULTIENTRANCELAB = "rm_WA_MultiEntranceLab.lvl"
        RM_WA_TANUKITROUBLEVAULT = "rm_WA_TanukiTroubleVAULT.lvl"
        RM_WA_TITANFALLS = "rm_WA_TitanFalls.lvl"
        RM_WA_TOWER = "rm_WA_Tower.lvl"
        RM_WA_TOWERENTER = "rm_WA_TowerEnter.lvl"
        RM_WA_TOWER_ELEVATOR = "rm_WA_Tower_elevator.lvl"
        RM_WA_TOWER_HYPERWELL = "rm_WA_Tower_Hyperwell.lvl"
        RM_WA_TOWER_PREELE = "rm_WA_Tower_PreEle.lvl"
        RM_WA_VALE = "rm_WA_Vale.lvl"
        RM_WB_BIGBATTLE = "rm_WB_BigBattle.lvl"
        RM_WB_CHARGERS = "rm_WB_Chargers.lvl"
        RM_WB_CRYSTALQUEEN = "rm_WB_CrystalQueen.lvl"
        RM_WB_CRYSTALQUEENHALL = "rm_WB_CrystalQueenHall.lvl"
        RM_WB_PRISONNEST = "rm_WB_PrisonNest.lvl"
        RM_WB_PUZZLEPALACE = "rm_WB_PuzzlePalace.lvl"
        RM_WB_TANUKITROUBLE = "rm_WB_TanukiTrouble.lvl"
        RM_WB_TREETREACHERY = "rm_WB_TreeTreachery.lvl"
        RM_WC_BIGMEADOW = "rm_WC_BigMeadow.lvl"
        RM_WC_BIGMEADOWVAULT = "rm_WC_BigMeadowVAULT.lvl"
        RM_WC_CAVEMEADOWOPEN = "rm_WC_CaveMeadowOpen.lvl"
        RM_WC_CAVERNSWITCH = "rm_WC_CavernSwitch.lvl"
        RM_WC_CLIFFSIDECELLSREDUX = "rm_WC_CliffsideCellsRedux.lvl"
        RM_WC_CRYSTALLAKE = "rm_WC_CrystalLake.lvl"
        RM_WC_CRYSTALLAKEVAULT = "rm_WC_CrystalLakeVault.lvl"
        RM_WC_GROTTONPC = "rm_WC_GrottoNPC.lvl"
        RM_WC_GROTTOSECRETS = "rm_WC_GrottoSecrets.lvl"
        RM_WC_GROTTOTEST = "rm_WC_GrottoTest.lvl"
        RM_WC_LAKEPRISONTELE = "rm_WC_LakePrisonTele.lvl"
        RM_WC_MEADOWCAVECROSSING = "rm_WC_MeadowCaveCrossing.lvl"
        RM_WC_MEADOWOODCORNER = "rm_WC_MeadowoodCorner.lvl"
        RM_WC_MINILAB = "rm_WC_MiniLab.lvl"
        RM_WC_PRISONHAL = "rm_WC_PrisonHAL.lvl"
        RM_WC_PRISONHALLEND = "rm_WC_PrisonHallEnd.lvl"
        RM_WC_PRISONHALLOPEN = "rm_WC_PrisonHallOpen.lvl"
        RM_WC_PRISONSTAIRSTRANSITION = "rm_WC_PrisonStairsTransition.lvl"
        RM_WC_RUINCLEARING = "rm_WC_RuinClearing.lvl"
        RM_WC_SIMPLEPATH = "rm_WC_SimplePath.lvl"
        RM_WC_SLOWLABOPEN = "rm_WC_SlowLabOpen.lvl"
        RM_WC_THINFOREST = "rm_WC_ThinForest.lvl"
        RM_WC_THINFORESTLOW = "rm_WC_ThinForestLow.lvl"
        RM_WC_THINFORESTLOWSECRET = "rm_WC_ThinForestLowSecret.lvl"
        RM_WC_TIMELABSWITCH = "rm_WC_TimeLabSwitch.lvl"
        RM_WC_WINDINGWOOD = "rm_WC_WindingWood.lvl"
        RM_WL_CLIFFSIDECELLSREDUXVAULT = "rm_WL_CliffsideCellsReduxVAULT.lvl"
        RM_WL_NPCTREEHOUSE = "rm_WL_NPCTreehouse.lvl"
        RM_WL_PRISONHALVAULT = "rm_WL_PrisonHALVAULT.lvl"
        RM_WL_SIMPLEPATHVAULT = "rm_WL_SimplePathVAULT.lvl"
        RM_WL_STAIRSSHORTCUT = "rm_WL_StairsShortcut.lvl"
        RM_WL_THEWOODVAULT = "rm_WL_TheWoodVAULT.lvl"
        RM_WL_TOWERVAULT = "rm_WL_TowerVAULT.lvl"
        RM_WL_TRANSTOCRYSTALS = "rm_WL_TransToCrystals.lvl"
        RM_WL_WESTDRIFTERVAULT = "rm_WL_WestDrifterVault.lvl"
        RM_WTESTING2048 = "rm_WTesting2048.lvl"
        RM_WT_CLIFFSIDECELLS = "rm_WT_CliffsideCells.lvl"
        RM_WT_CRYSTALDEPTHS = "rm_WT_CrystalDepths.lvl"
        RM_WT_PROTOGRID = "rm_WT_ProtoGrid.lvl"
        RM_WT_SLOWLAB = "rm_WT_SlowLab.lvl"
        RM_WT_THEWOOD = "rm_WT_TheWood.lvl"
        RM_WV_PRISONNEW = "rm_WV_PrisonNew.lvl"
        RM_WV_PUZZLEPALACENEW = "rm_WV_PuzzlePalaceNEW.lvl"
        RM_WX_BOSS = "rm_WX_Boss.lvl"
        RM_WX_TOWERWEST_ELEVATOR = "rm_WX_TowerWest_Elevator.lvl"
        RM_WX_TOWERWEST_WELL = "rm_WX_TowerWest_Well.lvl"
        RM_BENNYARROW = "rm_BennyArrow.lvl"
        RM_BOSSSOUTH = "rm_BossSouth.lvl"
        RM_CH_ACORNER = "rm_CH_ACorner.lvl"
        RM_CH_APILLARBIRD = "rm_CH_APillarBird.lvl"
        RM_CH_BDIRKDELUGE = "rm_CH_BDirkDeluge.lvl"
        RM_CH_BDIRKDEMOLITION = "rm_CH_BDirkDemolition.lvl"
        RM_CH_BDIRKOMMANDERSLAM = "rm_CH_BDirkommanderSlam.lvl"
        RM_CH_BFINAL = "rm_CH_BFinal.lvl"
        RM_CH_BFPS = "rm_CH_Bfps.lvl"
        RM_CH_BGUNDIRKDASH = "rm_CH_BGunDirkDash.lvl"
        RM_CH_BGUNPILLARS = "rm_CH_BGunPillars.lvl"
        RM_CH_BLEAPERFALL = "rm_CH_BLeaperFall.lvl"
        RM_CH_BMADDASH = "rm_CH_BMadDash.lvl"
        RM_CH_BPODS = "rm_CH_BPods.lvl"
        RM_CH_CBIGGGNS = "rm_CH_CBigggns.lvl"
        RM_CH_CENDHALL = "rm_CH_CEndHall.lvl"
        RM_CH_CGATEBLOCK = "rm_CH_CGateBlock.lvl"
        RM_CH_CSPAWNGROUND = "rm_CH_CSpawnGround.lvl"
        RM_CH_CSPIRAL = "rm_CH_CSpiral.lvl"
        RM_CH_CTEMPLATE = "rm_CH_CTemplate.lvl"
        RM_CH_CTURNHALL = "rm_CH_CTurnHall.lvl"
        RM_CH_GAUNTLETEND = "rm_CH_GauntletEnd.lvl"
        RM_CH_TABIGONE = "rm_CH_TABigOne.lvl"
        RM_CH_TBIRDSTANDOFF = "rm_CH_TBirdStandoff.lvl"
        RM_CH_TLONGESTROAD = "rm_CH_TLongestRoad.lvl"
        RM_COUNTALUCARD = "rm_CountAlucard.lvl"
        RM_SKYCITYVAULT = "rm_SkyCityVAULT.lvl"
        RM_SX_NPC = "rm_SX_NPC.lvl"
        RM_SX_RESUFACE = "rm_SX_ReSuface.lvl"
        RM_SX_SOUTHOPENING = "rm_SX_SouthOpening.lvl"
        RM_SX_TOWERSOUTH = "rm_SX_TowerSouth.lvl"
        RM_SX_TOWERSOUTH_ELEVATOR = "rm_SX_TowerSouth_Elevator.lvl"
        RM_SX_TOWERSOUTH_WELL = "rm_SX_TowerSouth_Well.lvl"
        RM_S_APILLARBIRDVAULT = "rm_S_APillarBirdVAULT.lvl"
        RM_S_BENNYARROW = "rm_S_BennyArrow.lvl"
        RM_S_BENNYARROWVAULT = "rm_S_BennyArrowVAULT.lvl"
        RM_S_BULLETBAKER = "rm_S_BulletBaker.lvl"
        RM_S_BULLETBAKERVAULT = "rm_S_BulletBakerVAULT.lvl"
        RM_S_CGATEBLOCKVAULT = "rm_S_CGateBlockVAULT.lvl"
        RM_S_COUNTACULARD = "rm_S_CountAculard.lvl"
        RM_S_COUNTACULARDVAULT = "rm_S_CountAculardVAULT.lvl"
        RM_S_GAUNTLETEND = "rm_S_GauntletEnd.lvl"
        RM_S_GAUNTLETLINKUP = "rm_S_GauntletLinkup.lvl"
        RM_S_GAUNTLETTITANFINALE = "rm_S_GauntletTitanFinale.lvl"
        RM_S_GAUNTLET_ELEVATOR = "rm_S_Gauntlet_Elevator.lvl"
        RM_S_MARKSCYTHE = "rm_S_MarkScythe.lvl"
        RM_S_MARKSCYTHEVAULT = "rm_S_MarkScytheVAULT.lvl"
        RM_S_TABIGONEVAULT = "rm_S_TABigOneVAULT.lvl"
        RM_CARENA = "rm_CArena.lvl"
        RM_C_BACKERTABLETX = "rm_C_BackerTabletX.lvl"
        RM_C_CENTRAL = "rm_C_Central.lvl"
        RM_C_DREGS_E = "rm_C_Dregs_E.lvl"
        RM_C_DREGS_N = "rm_C_Dregs_N.lvl"
        RM_C_DREGS_S = "rm_C_Dregs_S.lvl"
        RM_C_DREGS_W = "rm_C_Dregs_W.lvl"
        RM_C_DRIFTERWORKSHOP = "rm_C_DrifterWorkshop.lvl"
        RM_C_INTDRIFTERROOM = "rm_C_INTDrifterRoom.lvl"
        RM_C_NORTHDRIFTERROOM = "rm_C_NorthDrifterRoom.lvl"
        RM_C_VEN_APOTH = "rm_C_Ven_Apoth.lvl"
        RM_C_VEN_DASH = "rm_C_Ven_Dash.lvl"
        RM_C_VEN_GUN = "rm_C_Ven_Gun.lvl"
        RM_C_VEN_SDOJO = "rm_C_Ven_SDojo.lvl"
        RM_C_VEN_SPEC = "rm_C_Ven_Spec.lvl"
        RM_PAX_ARENA1 = "rm_PAX_arena1.lvl"
        RM_PAX_ARENA2 = "rm_PAX_arena2.lvl"
        RM_PAX_ARENAALL = "rm_PAX_arenaAll.lvl"
        RM_PAX_ARENAE = "rm_PAX_arenaE.lvl"
        RM_PAX_ARENAW = "rm_PAX_arenaW.lvl"
        RM_PAX_STAGING = "rm_PAX_Staging.lvl"
        RM_TELEVATORSHAFT = "rm_TelevatorShaft.lvl"
        RM_INL_SECRETS = "rm_INL_Secrets.lvl"
        RM_INL_SHOOTING = "rm_INL_Shooting.lvl"
        RM_INL_TRANSITIONCAMPFIRE = "rm_INL_TransitionCampfire.lvl"
        RM_IN_01_BROKENSHALLOWS = "rm_IN_01_brokenshallows.lvl"
        RM_IN_02_TUTORIAL = "rm_IN_02_Tutorial.lvl"
        RM_IN_03_TUT_COMBAT = "rm_IN_03_Tut_Combat.lvl"
        RM_IN_BACKERTABLET = "rm_IN_BackerTablet.lvl"
        RM_IN_BLACKWAITROOM = "rm_IN_BlackWaitRoom.lvl"
        RM_IN_DRIFTERFIRE = "rm_IN_Drifterfire.lvl"
        RM_IN_HALUCINATIONDEATH = "rm_IN_HalucinationDeath.lvl"
        RM_IN_HORIZONCLIFF = "rm_IN_HorizonCliff.lvl"
        RM_LIN_COMBAT = "rm_LIN_Combat.lvl"
        RM_LIN_GAPS = "rm_LIN_Gaps.lvl"
        RM_LIN_HEALTHREINFORCE = "rm_LIN_HealthReinforce.lvl"
        RM_LIN_LEAPERFIGHT = "rm_LIN_LeaperFight.lvl"
        RM_LIN_TUTHEALTH = "rm_LIN_tutHealth.lvl"
        RM_A_DOWNWARD = "rm_A_Downward.lvl"
        RM_A_DOWNWARDDEAD = "rm_A_DownwardDead.lvl"
        RM_A_DOWNWARDDEADREVISIT = "rm_A_DownwardDeadRevisit.lvl"
        RM_A_ELEVATORSHAFT = "rm_A_ElevatorShaft.lvl"
        RM_A_ELEVATORSHAFTUPPER = "rm_A_ElevatorShaftUpper.lvl"
        RM_A_EMBERROOM = "rm_A_EmberRoom.lvl"
        RM_A_PATH01 = "rm_A_path01.lvl"
        RM_A_PREDOWNWARD = "rm_A_PreDownward.lvl"
