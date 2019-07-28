# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/AvatarInputHandler/MapCaseMode.py
import weakref
import math
from ArtilleryEquipment import ArtilleryEquipment
from AvatarInputHandler import gun_marker_ctrl, mathUtils
from AvatarInputHandler.aih_constants import GUN_MARKER_TYPE, CTRL_MODE_NAME
from helpers import dependency
from helpers.CallbackDelayer import CallbackDelayer
from skeletons.gui.battle_session import IBattleSessionProvider
from AvatarInputHandler.DynamicCameras import StrategicCamera, ArcadeCamera
import BattleReplay
import BigWorld
import ResMgr
import CommandMapping
import GUI
import Keys
import Math
from Math import Vector2, Vector3
from AvatarInputHandler.control_modes import IControlMode
from AvatarInputHandler import AimingSystems
import SoundGroups
from constants import SERVER_TICK_LENGTH
from debug_utils import LOG_ERROR
from items import vehicles as vehs_core, artefacts
from constants import AIMING_MODE
from vehicle_systems.components.terrain_circle_component import readTerrainCircleSettings
_RAYCAST_HEIGHT = 500

class _DefaultStrikeSelector(CallbackDelayer):
    _TICK_DELAY = 0.1

    def __init__(self, position, equipment):
        CallbackDelayer.__init__(self)
        self.equipment = equipment
        self.delayCallback(self._TICK_DELAY, self.__tick)

    def destroy(self):
        CallbackDelayer.destroy(self)

    def setGUIVisible(self, isVisible):
        pass

    def onRecreateDevice(self):
        pass

    def processSelection(self, position, reset=False):
        return False

    def processHover(self, position, force=False):
        pass

    def processReplayHover(self):
        pass

    def tick(self):
        pass

    def __tick(self):
        self.tick()
        return self._TICK_DELAY


class _VehiclesSelector(object):

    def __init__(self, intersectChecker):
        self.__edgedVehicles = []
        self.__intersectChecker = intersectChecker
        BigWorld.player().onVehicleLeaveWorld += self.__onVehicleLeaveWorld

    def destroy(self):
        self.__intersectChecker = None
        self.__clearEdgedVehicles()
        BigWorld.player().onVehicleLeaveWorld -= self.__onVehicleLeaveWorld
        return

    def __onVehicleLeaveWorld(self, vehicle):
        if vehicle in self.__edgedVehicles:
            self.__edgedVehicles.remove(vehicle)
            vehicle.removeEdge(True)

    def __clearEdgedVehicles(self):
        for v in self.__edgedVehicles:
            if v is not None:
                v.removeEdge(True)

        self.__edgedVehicles = []
        return

    def highlightVehicles(self):
        self.__clearEdgedVehicles()
        vehicles = [ v for v in BigWorld.player().vehicles if v.isAlive() ]
        selected = self.__intersectChecker(vehicles)
        for v in selected:
            v.drawEdge(True)
            self.__edgedVehicles.append(v)


class _ArtilleryStrikeSelector(_DefaultStrikeSelector, _VehiclesSelector):

    def __init__(self, position, equipment):
        _DefaultStrikeSelector.__init__(self, position, equipment)
        _VehiclesSelector.__init__(self, self.__intersected)
        self.hitPosition = position
        myTeam = BigWorld.player().team
        udos = BigWorld.userDataObjects.values()
        myArtyEquipment = [ x for x in udos if isinstance(x, ArtilleryEquipment) and x.team == myTeam ]
        if len(myArtyEquipment) > 1:
            LOG_ERROR('This map has multiple (%d) UDO of ArtilleryEquipment for team %d' % (len(myArtyEquipment), myTeam))
        myArtyEquipment = myArtyEquipment[0]
        self.__marker = self._createMarker(myArtyEquipment, self.equipment.areaRadius)
        self.__marker.setPosition(position)
        self.__marker.create()
        self.__marker.enable()
        self.processHover(position)
        self.writeStateToReplay()

    def destroy(self):
        _DefaultStrikeSelector.destroy(self)
        _VehiclesSelector.destroy(self)
        if self.__marker is not None:
            self.__marker.disable()
            self.__marker.destroy()
            self.__marker = None
        return

    def setGUIVisible(self, isVisible):
        if self.__marker:
            self.__marker.setVisible(isVisible)

    def onRecreateDevice(self):
        if self.__marker:
            self.__marker.onRecreateDevice()

    def processSelection(self, position, reset=False):
        self.hitPosition = position
        if reset:
            return True
        BigWorld.player().setEquipmentApplicationPoint(self.equipment.id[1], self.hitPosition, Vector2(0, 1))
        return True

    def _createMarker(self, myArtyEquipment, areaRadius):
        return gun_marker_ctrl.createArtyHit(myArtyEquipment, areaRadius)

    def __markerForceUpdate(self):
        self.__marker.update(GUN_MARKER_TYPE.CLIENT, self.hitPosition, Vector3(0.0, 0.0, 1.0), (10.0, 10.0), 1000.0, None)
        return

    def processHover(self, position, force=False):
        if position is None:
            return
        else:
            if force:
                position = AimingSystems.getDesiredShotPoint(Math.Vector3(position[0], _RAYCAST_HEIGHT, position[2]), Math.Vector3(0.0, -1.0, 0.0), True, True, True)
                self.__marker.setPosition(position)
                BigWorld.callback(SERVER_TICK_LENGTH, self.__markerForceUpdate)
            else:
                self.__marker.update(GUN_MARKER_TYPE.CLIENT, position, Vector3(0.0, 0.0, 1.0), (10.0, 10.0), SERVER_TICK_LENGTH, None)
            self.hitPosition = position
            self.writeStateToReplay()
            return

    def tick(self):
        self.highlightVehicles()

    def processReplayHover(self):
        replayCtrl = BattleReplay.g_replayCtrl
        _, self.hitPosition, _ = replayCtrl.getGunMarkerParams(self.hitPosition, Math.Vector3(0.0, 0.0, 0.0))
        self.__marker.update(GUN_MARKER_TYPE.CLIENT, self.hitPosition, Vector3(0.0, 0.0, 1.0), (10.0, 10.0), SERVER_TICK_LENGTH, None)
        return

    def writeStateToReplay(self):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            if self.hitPosition is not None:
                replayCtrl.setConsumablesPosition(self.hitPosition)
        return

    def __intersected(self, vehicles):
        vPositions = [ v.position for v in vehicles ]
        pointsInside = self.__marker.getPointsInside(vPositions)
        for v, isInside in zip(vehicles, pointsInside):
            if isInside:
                yield v


_DEFAULT_STRIKE_DIRECTION = Vector3(1, 0, 0)

class _AreaStrikeSelector(_DefaultStrikeSelector):

    def __init__(self, position, equipment, direction=_DEFAULT_STRIKE_DIRECTION):
        _DefaultStrikeSelector.__init__(self, position, equipment)
        self.area = BigWorld.player().createEquipmentSelectedArea(position, direction, equipment)
        self.area.setOverTerrainOffset(10.0)
        self.direction = direction
        self.__sightUpdateActivity = None
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            self.__sightUpdateActivity = BigWorld.callback(0.0, self.__areaUpdate)
            self.__lastUpdateTime = BigWorld.time()
        self.writeStateToReplay()
        return

    def destroy(self):
        _DefaultStrikeSelector.destroy(self)
        if self.area is not None:
            self.area.destroy()
            self.area = None
        if self.__sightUpdateActivity is not None:
            BigWorld.cancelCallback(self.__sightUpdateActivity)
            self.__sightUpdateActivity = None
        return

    def setGUIVisible(self, isVisible):
        if self.area is not None:
            self.area.setGUIVisible(isVisible)
        return

    def processSelection(self, position, reset=False):
        if reset:
            return True
        direction = Vector2(self.direction.x, self.direction.z)
        direction.normalise()
        BigWorld.player().setEquipmentApplicationPoint(self.equipment.id[1], self.area.position, direction)
        self.writeStateToReplay()
        return True

    def processHover(self, position, force=False):
        self.area.relocate(position, self.direction)
        self.writeStateToReplay()

    def processReplayHover(self):
        replayCtrl = BattleReplay.g_replayCtrl
        _, hitPosition, direction = replayCtrl.getGunMarkerParams(self.area.position, self.direction)
        self.area.setNextPosition(hitPosition, direction)

    def __areaUpdate(self):
        currentTime = BigWorld.time()
        deltaTime = BigWorld.time() - self.__lastUpdateTime
        self.__lastUpdateTime = currentTime
        self.area.update(deltaTime)
        self.__sightUpdateActivity = BigWorld.callback(0.0, self.__areaUpdate)

    def writeStateToReplay(self):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setConsumablesPosition(self.area.position, self.direction)


class _DirectionalAreaStrikeSelector(_AreaStrikeSelector):

    def __init__(self, position, equipment):
        _AreaStrikeSelector.__init__(self, position, equipment)
        self.selectingPosition = True

    def destroy(self):
        _AreaStrikeSelector.destroy(self)

    def processSelection(self, position, reset=False):
        if reset:
            if self.selectingPosition:
                return True
            self.selectingPosition = True
            self.direction = _DEFAULT_STRIKE_DIRECTION
            _AreaStrikeSelector.processHover(self, position)
            self.area.setSelectingDirection(False)
            return False
        else:
            if self.selectingPosition:
                self.area.relocate(position, self.direction)
            else:
                return _AreaStrikeSelector.processSelection(self, position)
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isRecording:
                if position is not None:
                    replayCtrl.setConsumablesPosition(self.area.position, self.direction)
            self.selectingPosition = False
            self.area.setSelectingDirection(True)
            return False

    def processHover(self, position, force=False):
        if self.selectingPosition:
            _AreaStrikeSelector.processHover(self, position)
        else:
            self.direction = position - self.area.position
            if self.direction.lengthSquared <= 0.001:
                self.direction = Vector3(0, 0, 1)
            _AreaStrikeSelector.processHover(self, self.area.position)


class _BomberStrikeSelector(_DirectionalAreaStrikeSelector, _VehiclesSelector):

    def __init__(self, position, equipment):
        _DirectionalAreaStrikeSelector.__init__(self, position, equipment)
        _VehiclesSelector.__init__(self, self.__intersected)

    def destroy(self):
        _DirectionalAreaStrikeSelector.destroy(self)
        _VehiclesSelector.destroy(self)

    def tick(self):
        self.highlightVehicles()

    def __intersected(self, vehicles):
        for v in vehicles:
            if self.area.pointInside(v.position):
                yield v


class _ArcadeBomberStrikeSelector(_AreaStrikeSelector, _VehiclesSelector):

    def __init__(self, position, equipment):
        _AreaStrikeSelector.__init__(self, position, equipment)
        _VehiclesSelector.__init__(self, self.__intersected)
        self.__updateDirection(position)

    def destroy(self):
        _AreaStrikeSelector.destroy(self)
        _VehiclesSelector.destroy(self)

    def processSelection(self, position, reset=False):
        return _AreaStrikeSelector.processSelection(self, position, reset)

    def processHover(self, position, force=False):
        _AreaStrikeSelector.processHover(self, position)
        self.__updateDirection(position)

    def tick(self):
        self.highlightVehicles()

    def __updateDirection(self, position):
        self.direction = position - BigWorld.player().vehicle.position
        if self.direction.lengthSquared <= 0.001:
            self.direction = Vector3(0, 0, 1)

    def __intersected(self, vehicles):
        for v in vehicles:
            if self.area.pointInside(v.position):
                yield v


class _ReconStrikeSelector(_AreaStrikeSelector, _VehiclesSelector):

    def __init__(self, position, equipment):
        arenaType = BigWorld.player().arena.arenaType
        reconDirection = arenaType.recon.flyDirections[BigWorld.player().team]
        _AreaStrikeSelector.__init__(self, position, equipment, reconDirection)
        _VehiclesSelector.__init__(self, self.__intersected)
        self.selectingPosition = True
        self.area.setConstrainToArenaBounds(True)

    def destroy(self):
        _AreaStrikeSelector.destroy(self)
        _VehiclesSelector.destroy(self)

    def tick(self):
        self.highlightVehicles()

    def __intersected(self, vehicles):
        for v in vehicles:
            if self.area.pointInside(v.position):
                yield v


class _SmokeStrikeSelector(_DirectionalAreaStrikeSelector, _VehiclesSelector):

    def __init__(self, position, equipment):
        _DirectionalAreaStrikeSelector.__init__(self, position, equipment)
        _VehiclesSelector.__init__(self, self.__intersected)

    def destroy(self):
        _DirectionalAreaStrikeSelector.destroy(self)
        _VehiclesSelector.destroy(self)

    def tick(self):
        self.highlightVehicles()

    def __intersected(self, vehicles):
        for v in vehicles:
            if self.area.pointInside(v.position):
                yield v


_STRIKE_SELECTORS = {artefacts.RageArtillery: _ArtilleryStrikeSelector,
 artefacts.RageBomber: _BomberStrikeSelector,
 artefacts.EpicArtillery: _ArtilleryStrikeSelector,
 artefacts.EpicBomber: _BomberStrikeSelector,
 artefacts.EpicRecon: _ReconStrikeSelector,
 artefacts.EpicSmoke: _SmokeStrikeSelector,
 artefacts.EventBomber: _ArcadeBomberStrikeSelector,
 artefacts.EventArcadeBomber: _ArcadeBomberStrikeSelector,
 artefacts.EventRecon: _ReconStrikeSelector,
 artefacts.EventArcadeArtillery: _ArcadeBomberStrikeSelector,
 artefacts.EventMinefield: _ArcadeBomberStrikeSelector}

class MapCaseControlModeBase(IControlMode, CallbackDelayer):
    guiSessionProvider = dependency.descriptor(IBattleSessionProvider)
    isEnabled = property(lambda self: self.__isEnabled)
    camera = property(lambda self: self.__cam)
    aimingMode = property(lambda self: self.__aimingMode)
    equipmentID = property(lambda self: self.__equipmentID)
    prevCtlMode = None
    deactivateCallback = None
    _PREFERED_POSITION = 0
    _MODE_NAME = 1
    _AIM_MODE = 2

    def __init__(self, dataSection, avatarInputHandler, permanentTick=False):
        CallbackDelayer.__init__(self)
        self.__cam = self._createCamera(dataSection['camera'])
        self.__preferredPos = Vector3(0, 0, 0)
        self.__aih = weakref.proxy(avatarInputHandler)
        self.__isEnabled = False
        self.__updateInterval = 0.1
        self.__activeSelector = _DefaultStrikeSelector(Vector3(0, 0, 0), None)
        self.__equipmentID = None
        self.__aimingMode = 0
        self.__aimingModeUserDisabled = False
        self.__permanentTick = permanentTick
        self.__class__.prevCtlMode = [Vector3(0, 0, 0), '', 0]
        return

    def create(self):
        self._initCamera()
        self.disable()

    def destroy(self):
        CallbackDelayer.destroy(self)
        self.disable()
        if self.__activeSelector is not None:
            self.__activeSelector.destroy()
            self.__activeSelector = None
        self.__cam.destroy()
        self.__aih = None
        return

    def enable(self, **args):
        SoundGroups.g_instance.changePlayMode(2)
        overridePreferredPosition = self.guiSessionProvider.shared.equipments.consumePreferredPosition()
        if any((cls == type(overridePreferredPosition) for cls in (Vector3, tuple))):
            targetPos = overridePreferredPosition
        else:
            targetPos = args.get('preferredPos', Vector3(0, 0, 0))
        self.__cam.enable(targetPos, args.get('saveDist', True))
        self.__aimingMode = args.get('aimingMode', self.__aimingMode)
        self.__aimingModeUserDisabled = self.getAimingMode(AIMING_MODE.USER_DISABLED)
        self.__aimingMode |= AIMING_MODE.USER_DISABLED
        self.__isEnabled = True
        equipmentID = args.get('equipmentID', None)
        if equipmentID is None:
            self.__activeSelector = _DefaultStrikeSelector(Vector3(0, 0, 0), None)
        else:
            self.activateEquipment(equipmentID)
        self.setGUIVisible(self.__aih.isGuiVisible)
        if BigWorld.player().gunRotator is not None:
            BigWorld.player().gunRotator.clientMode = False
            BigWorld.player().gunRotator.stopTrackingOnServer()
        if self.__permanentTick:
            self.delayCallback(0.0, self._tick)
        return

    def disable(self):
        if not self.__isEnabled:
            return
        else:
            self.__isEnabled = False
            self.__cam.disable()
            self.__activeSelector.destroy()
            self.__activeSelector = _DefaultStrikeSelector(Vector3(0, 0, 0), None)
            self.setGUIVisible(False)
            self.__cam.writeUserPreferences()
            if BigWorld.player().gunRotator is not None:
                BigWorld.player().gunRotator.clientMode = True
            if self.__permanentTick:
                self.stopCallback(self._tick)
            return

    def handleKeyEvent(self, isDown, key, mods, event=None):
        cmdMap = CommandMapping.g_instance
        if key == Keys.KEY_LEFTMOUSE and isDown:
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying:
                return True
            shouldClose = self.__activeSelector.processSelection(self.__getDesiredShotPoint())
            if shouldClose:
                self.turnOff()
            return True
        elif key == Keys.KEY_RIGHTMOUSE and mods != Keys.MODIFIER_CTRL and isDown:
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying:
                return True
            shouldClose = self.__activeSelector.processSelection(self.__getDesiredShotPoint(), True)
            if shouldClose:
                self.turnOff()
            return True
        elif cmdMap.isFired(CommandMapping.CMD_CM_ALTERNATE_MODE, key) and isDown:
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying:
                self.__aih.onControlModeChanged('arcade')
                arcadeMode = BigWorld.player().inputHandler.ctrls.get('arcade', None)
                arcadeMode.showGunMarker(False)
                return True
            self.turnOff()
            return True
        elif cmdMap.isFiredList((CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT,
         CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT,
         CommandMapping.CMD_CM_CAMERA_ROTATE_UP,
         CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN,
         CommandMapping.CMD_CM_INCREASE_ZOOM,
         CommandMapping.CMD_CM_DECREASE_ZOOM), key):
            dx = dy = dz = 0.0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT):
                dx = -1.0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT):
                dx = 1.0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_UP):
                dy = -1.0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN):
                dy = 1.0
            if cmdMap.isActive(CommandMapping.CMD_CM_INCREASE_ZOOM):
                dz = 1.0
            if cmdMap.isActive(CommandMapping.CMD_CM_DECREASE_ZOOM):
                dz = -1.0
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying and replayCtrl.isControllingCamera:
                return True
            self.__cam.update(dx, dy, dz, False if dx == dy == dz == 0.0 else True)
            if not self.__permanentTick:
                if dx == dy == dz == 0.0:
                    self.stopCallback(self._tick)
                else:
                    self.delayCallback(0.0, self._tick)
            return True
        else:
            if cmdMap.isFired(CommandMapping.CMD_CM_FREE_CAMERA, key):
                replayCtrl = BattleReplay.g_replayCtrl
                if replayCtrl.isPlaying:
                    return True
                if not isDown:
                    self.__class__.prevCtlMode[self._AIM_MODE] &= -1 - AIMING_MODE.USER_DISABLED
                else:
                    self.__class__.prevCtlMode[self._AIM_MODE] |= AIMING_MODE.USER_DISABLED
            return False

    def handleMouseEvent(self, dx, dy, dz):
        GUI.mcursor().position = Math.Vector2(0, 0)
        self.__cam.update(dx, dy, dz)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            return True
        self.__activeSelector.processHover(self.__getDesiredShotPoint())
        return True

    def onMinimapClicked(self, worldPos):
        self.__cam.teleport(worldPos)
        self.__activeSelector.processHover(worldPos, True)

    def setAimingMode(self, enable, mode):
        if mode == AIMING_MODE.USER_DISABLED:
            self.__aimingModeUserDisabled = enable
            return
        if mode == AIMING_MODE.TARGET_LOCK and not enable:
            self.__class__.prevCtlMode[self._AIM_MODE] &= -1 - mode
        if enable:
            self.__aimingMode |= mode
        else:
            self.__aimingMode &= -1 - mode

    def getAimingMode(self, mode):
        return self.__aimingMode & mode == mode

    def getDesiredShotPoint(self, ignoreAimingMode=False):
        return self.__getDesiredShotPoint() if self.__aimingMode == 0 or ignoreAimingMode else None

    def _createCamera(self, data):
        raise NotImplementedError

    def _initCamera(self):
        raise NotImplementedError

    def _getCameraDesiredShotPoint(self):
        raise NotImplementedError

    def _getPreferedPositionOnQuit(self):
        raise NotImplementedError

    def __getDesiredShotPoint(self):
        defaultPoint = self._getCameraDesiredShotPoint()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            _, hitPosition, _ = replayCtrl.getGunMarkerParams(defaultPoint, Math.Vector3(0.0, 0.0, 1.0))
            return hitPosition
        return defaultPoint

    def onRecreateDevice(self):
        self.__activeSelector.onRecreateDevice()

    def setGUIVisible(self, isVisible):
        self.__activeSelector.setGUIVisible(isVisible)

    def isManualBind(self):
        return True

    def updateGunMarker(self, markerType, pos, direction, size, relaxTime, collData):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            self.__activeSelector.processReplayHover()

    def turnOff(self, sendStopEquipment=True):
        if sendStopEquipment and self.__class__.deactivateCallback is not None:
            self.__class__.deactivateCallback()
            self.__class__.deactivateCallback = None
        prevMode = self.__class__.prevCtlMode
        if not self.__aimingModeUserDisabled:
            self.__aimingMode &= -1 - AIMING_MODE.USER_DISABLED
        pos = self._getPreferedPositionOnQuit()
        self.__aih.onControlModeChanged(prevMode[self._MODE_NAME], preferredPos=pos, aimingMode=self.__aimingMode, saveDist=False, saveZoom=True)
        self.stopCallback(self._tick)
        self.__cam.update(0.0, 0.0, 0.0, False)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setEquipmentID(-1)
        return

    def activateEquipment(self, equipmentID, preferredPos=None):
        equipment = vehs_core.g_cache.equipments()[equipmentID]
        strikeSelectorConstructor = _STRIKE_SELECTORS.get(type(equipment))
        if strikeSelectorConstructor is None:
            LOG_ERROR('Cannot use equipment with id', equipmentID)
            return
        else:
            self.__activeSelector.destroy()
            pos = preferredPos or self.__getDesiredShotPoint()
            self.__activeSelector = strikeSelectorConstructor(pos, equipment)
            self.__equipmentID = equipmentID
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isRecording:
                replayCtrl.setEquipmentID(equipmentID)
            if not isinstance(BigWorld.player().inputHandler.ctrl, MapCaseControlModeBase):
                self.setGUIVisible(False)
            return

    def _tick(self):
        self.__activeSelector.processHover(self.__getDesiredShotPoint())


class MapCaseControlMode(MapCaseControlModeBase):

    def _createCamera(self, config):
        return StrategicCamera.StrategicCamera(config)

    def _initCamera(self):
        self.camera.create(None)
        self.camera.setMaxDist()
        return

    def _getCameraDesiredShotPoint(self):
        return self.camera.aimingSystem.getDesiredShotPoint(True)

    def _getPreferedPositionOnQuit(self):
        prevMode = self.__class__.prevCtlMode
        return prevMode[self._PREFERED_POSITION]


def readVisualSettings():
    xmlTag = 'EquipmentCircleRestrictionVisual'
    filePath = 'scripts/dynamic_objects.xml'
    xmlSection = ResMgr.openSection(filePath)
    if xmlSection is None:
        LOG_ERROR("initSettings: Could not open section '{}' in file {}".format(xmlTag, filePath))
        return
    else:
        xmlCtx = (None, filePath)
        return readTerrainCircleSettings(xmlSection, xmlCtx, xmlTag)


g_circleVisualSettings = readVisualSettings()

class ArcadeMapCaseControlMode(MapCaseControlModeBase):
    _DEFAULT_CAMERA_PIVOT_MIN = Math.Vector3(0, 25, -15)
    _DEFAULT_CAMERA_PIVOT_MAX = Math.Vector3(0, 85, -15)

    def __init__(self, dataSection, avatarInputHandler):
        MapCaseControlModeBase.__init__(self, dataSection, avatarInputHandler, permanentTick=True)

    def enable(self, **args):
        MapCaseControlModeBase.enable(self, **args)
        if self._showCircle() != 0:
            vehicle = BigWorld.player().getVehicleAttached()
            if vehicle:
                vehicle.appearance.showTerrainCircle(self._getApplyMaxRadius(), g_circleVisualSettings)

    def disable(self):
        if self._showCircle() != 0:
            vehicle = BigWorld.player().getVehicleAttached()
            if vehicle:
                vehicle.appearance.hideTerrainCircle()
        MapCaseControlModeBase.disable(self)

    def _createCamera(self, config):
        return ArcadeCamera.ArcadeCamera(config, Math.Vector2())

    def _initCamera(self):
        self.camera.create(self._DEFAULT_CAMERA_PIVOT_MIN)

    def _getCameraDesiredShotPoint(self):
        position = self.camera.aimingSystem.getDesiredShotPoint()
        vehiclePosition = BigWorld.player().getVehicleAttached().position
        applyMinRadius = self._getApplyMinRadius()
        applyMaxRadius = self._getApplyMaxRadius()
        if applyMaxRadius != 0:
            delta = position - vehiclePosition
            deltaLength = delta.length
            if deltaLength > applyMaxRadius:
                position = self._clampPosition(delta, vehiclePosition, applyMaxRadius)
            if deltaLength < applyMinRadius:
                position = self._clampPosition(delta, vehiclePosition, applyMinRadius)
        return position

    def _tick(self):
        pitch = self.camera.angles[1]
        halfPi = math.pi / 2
        k = mathUtils.clamp(0, 1, pitch / halfPi + 1)
        pivotPosMin = self._getCameraPivotPosMin() or self._DEFAULT_CAMERA_PIVOT_MIN
        pivotPosMax = self._getCameraPivotPosMax() or self._DEFAULT_CAMERA_PIVOT_MAX
        pivotPos = mathUtils.lerp(pivotPosMin, pivotPosMax, k)
        self.camera.aimingSystem.setPivotSettings(pivotPos.y, pivotPos.z)
        return MapCaseControlModeBase._tick(self)

    def _clampPosition(self, delta, vehiclePosition, distance):
        delta.normalise()
        position = vehiclePosition + delta * distance
        position = AimingSystems.getDesiredShotPoint(Math.Vector3(position[0], _RAYCAST_HEIGHT, position[2]), Math.Vector3(0.0, -1.0, 0.0), True, True, True, True)
        return position

    def _getPreferedPositionOnQuit(self):
        inputHandler = BigWorld.player().inputHandler
        return inputHandler.ctrl.camera.aimingSystem.getDesiredShotPoint()

    def _showCircle(self):
        return self._getApplyMinRadius() != self._getApplyMaxRadius()

    def _getApplyMinRadius(self):
        equipment = self._getEquipment()
        return getattr(equipment, 'minApplyRadius', 0) if equipment else 0

    def _getApplyMaxRadius(self):
        equipment = self._getEquipment()
        return getattr(equipment, 'maxApplyRadius', 0) if equipment else 0

    def _getCameraPivotPosMin(self):
        equipment = self._getEquipment()
        return getattr(equipment, 'cameraPivotPosMin', None) if equipment else None

    def _getCameraPivotPosMax(self):
        equipment = self._getEquipment()
        return getattr(equipment, 'cameraPivotPosMax', None) if equipment else None

    def _getEquipment(self):
        return vehs_core.g_cache.equipments()[self.equipmentID] if self.equipmentID else None


def activateMapCase(equipmentID, deactivateCallback, isArcadeCamera=False):
    inputHandler = BigWorld.player().inputHandler
    controlMode = ArcadeMapCaseControlMode if isArcadeCamera else MapCaseControlMode
    if isinstance(inputHandler.ctrl, controlMode):
        if controlMode.deactivateCallback is not None:
            controlMode.deactivateCallback()
            controlMode.deactivateCallback = deactivateCallback
        mapCaseCtrl = inputHandler.ctrl
        preferredPos = None if mapCaseCtrl.isEnabled else mapCaseCtrl.getDesiredShotPoint(ignoreAimingMode=True)
        inputHandler.ctrl.activateEquipment(equipmentID, preferredPos)
    else:
        controlMode.deactivateCallback = deactivateCallback
        pos = inputHandler.getDesiredShotPoint()
        if pos is None:
            camera = getattr(inputHandler.ctrl, 'camera', None)
            if camera is not None:
                pos = camera.aimingSystem.getDesiredShotPoint()
            if pos is None:
                pos = Vector3(0.0, 0.0, 0.0)
        modeName = CTRL_MODE_NAME.MAP_CASE_ARCADE if isArcadeCamera else CTRL_MODE_NAME.MAP_CASE
        controlMode.prevCtlMode = [pos, inputHandler.ctrlModeName, inputHandler.ctrl.aimingMode]
        inputHandler.onControlModeChanged(modeName, preferredPos=pos, aimingMode=inputHandler.ctrl.aimingMode, equipmentID=equipmentID, saveDist=False)
    return


def turnOffMapCase(equipmentID, isArcadeCamera=False):
    controlMode = ArcadeMapCaseControlMode if isArcadeCamera else MapCaseControlMode
    inputHandler = BigWorld.player().inputHandler
    if isinstance(inputHandler.ctrl, controlMode):
        if inputHandler.ctrl.equipmentID == equipmentID:
            controlMode.deactivateCallback = None
            inputHandler.ctrl.turnOff(False)
    return
