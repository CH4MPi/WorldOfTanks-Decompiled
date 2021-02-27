# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/battle_royale/page.py
import BigWorld
from shared_utils import CONST_CONTAINER
from arena_bonus_type_caps import ARENA_BONUS_TYPE_CAPS
from gui.Scaleform.daapi.view.battle.battle_royale.markers2d.manager import BattleRoyaleMarkersManager
from gui.Scaleform.daapi.view.battle.battle_royale.player_format import BattleRoyalePlayerFullNameFormatter
from gui.Scaleform.daapi.view.battle.battle_royale.spawned_bot_msg import SpawnedBotMsgPlayerMsgs
from gui.Scaleform.daapi.view.battle.battle_royale.minefield_player_messenger import MinefieldPlayerMessenger
from gui.Scaleform.daapi.view.meta.BattleRoyalePageMeta import BattleRoyalePageMeta
from gui.Scaleform.daapi.view.battle.classic.page import DynamicAliases
from gui.Scaleform.daapi.view.battle.epic import drone_music_player
from gui.Scaleform.daapi.view.battle.shared import period_music_listener, crosshair
from gui.Scaleform.daapi.view.battle.shared.page import ComponentsConfig
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.battle_control.battle_constants import BATTLE_CTRL_ID, VEHICLE_VIEW_STATE
from gui.battle_control.controllers.spawn_ctrl import ISpawnListener
from gui.battle_royale.br_effect_player import BRUpgradeEffectPlayer
from gui.game_control.br_battle_messages import ProgressionMessagesPlayer
from gui.game_control.br_battle_sounds import BRBattleSoundController, RadarSoundPlayer, LevelSoundPlayer, EnemiesAmountSoundPlayer, PhaseSoundPlayer, PostmortemSoundPlayer, InstallModuleSoundPlayer, EquipmentSoundPlayer
from gui.game_control.br_battle_sounds import SelectRespawnSoundPlayer, ArenaPeriodSoundPlayer

class _DynamicAliases(CONST_CONTAINER):
    SELECT_RESPAWN_SOUND_PLAYER = 'selectRespawnSoundPlayer'
    PROGRESSION_MESSAGES_PLAYER = 'progressionMessagesPlayer'
    RADAR_SOUND_PLAYER = 'radarSoundPlayer'
    LEVEL_SOUND_PLAYER = 'levelSoundPlayer'
    ENEMIES_AMOUNT_SOUND_PLAYER = 'enemiesAmountSoundPlayer'
    PHASE_SOUND_PLAYER = 'phaseSoundPlayer'
    POSTMORTEM_SOUND_PLAYER = 'postmortemSoundPlayer'
    INSTALL_MODULE_SOUND_PLAYER = 'installModuleSoundPlayer'
    ARENA_PERIOD_SOUND_PLAYER = 'arenaPeriodSoundPlayer'
    EQUIPMENT_SOUND_PLAYER = 'equipmentSoundPlayer'
    VEH_UPGRADE_EFFECT_PLAYER = 'vehicleUpgradeEffectPlayer'
    SPAWNED_BOT_MSG_PUBLISHER = 'SpawnedBotMsgPublisher'
    MINEFIELD_MSG_PUBLISHER = 'MinefieldMsgPublisher'


class _BattleRoyaleComponentsConfig(ComponentsConfig):

    def __init__(self):
        super(_BattleRoyaleComponentsConfig, self).__init__(((BATTLE_CTRL_ID.ARENA_PERIOD, (BATTLE_VIEW_ALIASES.BATTLE_TIMER,
           BATTLE_VIEW_ALIASES.PREBATTLE_TIMER,
           BATTLE_VIEW_ALIASES.BATTLE_END_WARNING_PANEL,
           BATTLE_VIEW_ALIASES.HINT_PANEL,
           DynamicAliases.DRONE_MUSIC_PLAYER,
           DynamicAliases.PERIOD_MUSIC_LISTENER,
           BATTLE_VIEW_ALIASES.RADAR_BUTTON,
           _DynamicAliases.ARENA_PERIOD_SOUND_PLAYER,
           _DynamicAliases.SELECT_RESPAWN_SOUND_PLAYER)),
         (BATTLE_CTRL_ID.TEAM_BASES, (BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL, DynamicAliases.DRONE_MUSIC_PLAYER)),
         (BATTLE_CTRL_ID.DEBUG, (BATTLE_VIEW_ALIASES.DEBUG_PANEL,)),
         (BATTLE_CTRL_ID.BATTLE_FIELD_CTRL, (BATTLE_VIEW_ALIASES.BATTLE_TEAM_PANEL, DynamicAliases.DRONE_MUSIC_PLAYER)),
         (BATTLE_CTRL_ID.PROGRESSION_CTRL, (BATTLE_VIEW_ALIASES.BATTLE_LEVEL_PANEL,
           BATTLE_VIEW_ALIASES.UPGRADE_PANEL,
           _DynamicAliases.PROGRESSION_MESSAGES_PLAYER,
           _DynamicAliases.LEVEL_SOUND_PLAYER,
           _DynamicAliases.PHASE_SOUND_PLAYER,
           _DynamicAliases.INSTALL_MODULE_SOUND_PLAYER,
           _DynamicAliases.VEH_UPGRADE_EFFECT_PLAYER,
           _DynamicAliases.SPAWNED_BOT_MSG_PUBLISHER,
           _DynamicAliases.MINEFIELD_MSG_PUBLISHER)),
         (BATTLE_CTRL_ID.ARENA_LOAD_PROGRESS, (DynamicAliases.DRONE_MUSIC_PLAYER,)),
         (BATTLE_CTRL_ID.GAME_MESSAGES_PANEL, (BATTLE_VIEW_ALIASES.GAME_MESSAGES_PANEL,)),
         (BATTLE_CTRL_ID.MAPS, (BATTLE_VIEW_ALIASES.MINIMAP,)),
         (BATTLE_CTRL_ID.RADAR_CTRL, (BATTLE_VIEW_ALIASES.RADAR_BUTTON, _DynamicAliases.RADAR_SOUND_PLAYER)),
         (BATTLE_CTRL_ID.SPAWN_CTRL, (BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN, _DynamicAliases.SELECT_RESPAWN_SOUND_PLAYER)),
         (BATTLE_CTRL_ID.VEHICLES_COUNT_CTRL, (BATTLE_VIEW_ALIASES.FRAG_PANEL,
           BATTLE_VIEW_ALIASES.FULL_STATS,
           _DynamicAliases.ENEMIES_AMOUNT_SOUND_PLAYER,
           _DynamicAliases.PHASE_SOUND_PLAYER,
           _DynamicAliases.POSTMORTEM_SOUND_PLAYER,
           _DynamicAliases.ARENA_PERIOD_SOUND_PLAYER,
           _DynamicAliases.EQUIPMENT_SOUND_PLAYER))), ((DynamicAliases.PERIOD_MUSIC_LISTENER, period_music_listener.PeriodMusicListener),
         (DynamicAliases.DRONE_MUSIC_PLAYER, drone_music_player.DroneMusicPlayer),
         (_DynamicAliases.SELECT_RESPAWN_SOUND_PLAYER, SelectRespawnSoundPlayer),
         (_DynamicAliases.PROGRESSION_MESSAGES_PLAYER, ProgressionMessagesPlayer),
         (_DynamicAliases.RADAR_SOUND_PLAYER, RadarSoundPlayer),
         (_DynamicAliases.LEVEL_SOUND_PLAYER, LevelSoundPlayer),
         (_DynamicAliases.ENEMIES_AMOUNT_SOUND_PLAYER, EnemiesAmountSoundPlayer),
         (_DynamicAliases.PHASE_SOUND_PLAYER, PhaseSoundPlayer),
         (_DynamicAliases.POSTMORTEM_SOUND_PLAYER, PostmortemSoundPlayer),
         (_DynamicAliases.INSTALL_MODULE_SOUND_PLAYER, InstallModuleSoundPlayer),
         (_DynamicAliases.ARENA_PERIOD_SOUND_PLAYER, ArenaPeriodSoundPlayer),
         (_DynamicAliases.VEH_UPGRADE_EFFECT_PLAYER, BRUpgradeEffectPlayer),
         (_DynamicAliases.EQUIPMENT_SOUND_PLAYER, EquipmentSoundPlayer),
         (_DynamicAliases.SPAWNED_BOT_MSG_PUBLISHER, SpawnedBotMsgPlayerMsgs),
         (_DynamicAliases.MINEFIELD_MSG_PUBLISHER, MinefieldPlayerMessenger)))


_BATTLE_ROYALE_CFG = _BattleRoyaleComponentsConfig()

class BattleRoyalePage(BattleRoyalePageMeta, ISpawnListener):
    __PANELS_FOR_SHOW_HIDE = [BATTLE_VIEW_ALIASES.CONSUMABLES_PANEL, BATTLE_VIEW_ALIASES.BATTLE_LEVEL_PANEL]

    def __init__(self, components=None):
        if components is None:
            components = _BATTLE_ROYALE_CFG
        self.__selectSpawnToggling = set()
        self.__brSoundControl = None
        self.__isFullStatsShown = False
        self.__panelsIsVisible = False
        super(BattleRoyalePage, self).__init__(components, external=(crosshair.CrosshairPanelContainer, BattleRoyaleMarkersManager))
        return

    def showSpawnPoints(self):
        visibleComponents = [BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN]
        if ARENA_BONUS_TYPE_CAPS.checkAny(BigWorld.player().arena.bonusType, ARENA_BONUS_TYPE_CAPS.SQUADS):
            visibleComponents.extend([BATTLE_VIEW_ALIASES.BATTLE_TEAM_PANEL, BATTLE_VIEW_ALIASES.BATTLE_MESSENGER])
        if not self.__selectSpawnToggling:
            self.__selectSpawnToggling.update(set(self.as_getComponentsVisibilityS()) - set(visibleComponents))
        self._setComponentsVisibility(visible=visibleComponents, hidden=self.__selectSpawnToggling)
        self.app.enterGuiControlMode(BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN)

    def closeSpawnPoints(self):
        if self.__selectSpawnToggling:
            self._setComponentsVisibility(visible=self.__selectSpawnToggling, hidden=[BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN])
            self.__selectSpawnToggling.clear()
            self.app.leaveGuiControlMode(BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN)

    def isFullStatsShown(self):
        return self.__isFullStatsShown

    def _canShowPostmortemTips(self):
        return not self.__isFullStatsShown and super(BattleRoyalePage, self)._canShowPostmortemTips()

    def _toggleFullStats(self, isShown, permanent=None, tabIndex=None):
        manager = self.app.containerManager
        if manager.isModalViewsIsExists():
            return
        else:
            self.__isFullStatsShown = isShown
            if permanent is None:
                permanent = set()
            permanent.add('minimap')
            if isShown:
                progressionWindow = self.__getProgressionWindowCtrl()
                if progressionWindow:
                    progressionWindow.closeWindow()
            if self.__selectSpawnToggling:
                return
            super(BattleRoyalePage, self)._toggleFullStats(isShown, permanent, tabIndex)
            return

    def _populate(self):
        super(BattleRoyalePage, self)._populate()
        progressionWindowCtrl = self.__getProgressionWindowCtrl()
        if progressionWindowCtrl:
            progressionWindowCtrl.onTriggered += self.__onConfWindowTriggered
        spawnCtrl = self.sessionProvider.dynamic.spawn
        if spawnCtrl:
            spawnCtrl.addRuntimeView(self)
        self.sessionProvider.getCtx().setPlayerFullNameFormatter(BattleRoyalePlayerFullNameFormatter())
        self.__brSoundControl = BRBattleSoundController()
        self.__brSoundControl.init()

    def _startBattleSession(self):
        super(BattleRoyalePage, self)._startBattleSession()
        vehStateCtrl = self.sessionProvider.shared.vehicleState
        if vehStateCtrl is not None:
            vehStateCtrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
        ammoCtrl = self.sessionProvider.shared.ammo
        if ammoCtrl is not None:
            ammoCtrl.onGunSettingsSet += self.__onGunSettingsSet
        return

    def _stopBattleSession(self):
        super(BattleRoyalePage, self)._stopBattleSession()
        vehStateCtrl = self.sessionProvider.shared.vehicleState
        if vehStateCtrl is not None:
            vehStateCtrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        ammoCtrl = self.sessionProvider.shared.ammo
        if ammoCtrl is not None:
            ammoCtrl.onGunSettingsSet -= self.__onGunSettingsSet
        return

    def _onRegisterFlashComponent(self, viewPy, alias):
        super(BattleRoyalePage, self)._onRegisterFlashComponent(viewPy, alias)
        if alias == BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN:
            self._setComponentsVisibility(hidden=[alias])

    def _toggleGuiVisible(self):
        componentsVisibility = self.as_getComponentsVisibilityS()
        if BATTLE_VIEW_ALIASES.BR_SELECT_RESPAWN in componentsVisibility:
            return
        super(BattleRoyalePage, self)._toggleGuiVisible()

    def _dispose(self):
        progressionWindowCtrl = self.__getProgressionWindowCtrl()
        if progressionWindowCtrl:
            progressionWindowCtrl.onTriggered -= self.__onConfWindowTriggered
        spawnCtrl = self.sessionProvider.dynamic.spawn
        if spawnCtrl:
            spawnCtrl.removeRuntimeView(self)
        if self.__brSoundControl is not None:
            self.__brSoundControl.destroy()
            self.__brSoundControl = None
        self.__selectSpawnToggling.clear()
        super(BattleRoyalePage, self)._dispose()
        return

    def _switchToPostmortem(self):
        BigWorld.player().setIsObserver()

    def __onConfWindowTriggered(self, isOpened):
        if isOpened:
            if not self.as_isComponentVisibleS(self._fullStatsAlias):
                self._fsToggling = set(self.as_getComponentsVisibilityS())
            self._setComponentsVisibility(visible=[], hidden=self._fsToggling)
        elif self._fsToggling:
            self._setComponentsVisibility(visible=self._fsToggling, hidden=[])

    def __getProgressionWindowCtrl(self):
        progression = self.sessionProvider.dynamic.progression
        return progression.getWindowCtrl() if progression else None

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.DEATHZONE_TIMER and value.level is None:
            vehicle = self.sessionProvider.shared.vehicleState.getControllingVehicle()
            isAlive = vehicle is not None and vehicle.isAlive()
            self.as_updateDamageScreenS(value.isCausingDamage and isAlive)
        elif state in (VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED):
            self.as_updateDamageScreenS(False)
        vehicle = BigWorld.player().getVehicleAttached()
        if vehicle is None or not vehicle.isAlive() and BigWorld.player().isObserver():
            if self.__panelsIsVisible:
                self._setComponentsVisibility(hidden=self.__PANELS_FOR_SHOW_HIDE)
                self.__panelsIsVisible = False
        elif not self.__panelsIsVisible:
            self._setComponentsVisibility(visible=self.__PANELS_FOR_SHOW_HIDE)
            self.__panelsIsVisible = True
        return

    def __onGunSettingsSet(self, _):
        progressionWindowCtrl = self.__getProgressionWindowCtrl()
        if progressionWindowCtrl and progressionWindowCtrl.isWindowOpened():
            isDualGunVehicle = self.sessionProvider.getArenaDP().getVehicleInfo().vehicleType.isDualGunVehicle
            dualGunAlias = BATTLE_VIEW_ALIASES.DUAL_GUN_PANEL
            if not isDualGunVehicle:
                if dualGunAlias in self._fsToggling:
                    self._fsToggling.remove(dualGunAlias)
