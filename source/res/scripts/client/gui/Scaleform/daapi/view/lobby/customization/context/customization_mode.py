# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/customization/context/customization_mode.py
import logging
from copy import copy, deepcopy
from functools import partial
import typing
from gui import SystemMessages
from gui.Scaleform.daapi.view.lobby.customization.shared import OutfitInfo, getItemAppliedCount, isItemLimitReached, getComponentFromSlot, getItemInventoryCount, getPurchaseLimit, CustomizationTabs, getItemFromSlot, getSlotDataFromSlot, getCurrentVehicleAvailableRegionsMap, fitOutfit, ITEM_TYPE_TO_SLOT_TYPE, removeItemsFromOutfit
from gui.Scaleform.locale.SYSTEM_MESSAGES import SYSTEM_MESSAGES
from gui.customization.constants import CustomizationModes, CustomizationModeSource
from gui.customization.shared import SeasonType, C11nId
from gui.shared.utils.decorators import process
from helpers import dependency
from shared_utils import first, nextTick
from skeletons.gui.customization import ICustomizationService
from skeletons.gui.shared import IItemsCache
if typing.TYPE_CHECKING:
    from gui.hangar_vehicle_appearance import AnchorParams
    from gui.customization.shared import PurchaseItem
    from gui.shared.gui_items.customization.c11n_items import Customization
    from items.customizations import SerializableComponent
    from gui.Scaleform.daapi.view.lobby.customization.context.context import CustomizationContext
    from vehicle_outfit.containers import SlotData
    from vehicle_outfit.outfit import Outfit
_logger = logging.getLogger(__name__)

class CustomizationMode(object):
    modeId = CustomizationModes.NONE
    _tabs = ()
    _itemsCache = dependency.descriptor(IItemsCache)
    _service = dependency.descriptor(ICustomizationService)

    def __init__(self, ctx):
        self._ctx = ctx
        self._isInited = False
        self._tabId = None
        self._source = None
        self._originalOutfits = {}
        self._modifiedOutfits = {}
        self._state = {}
        self._selectedSlot = None
        self._selectedItem = None
        return

    @property
    def isInited(self):
        return self._isInited

    @property
    def tabId(self):
        return self._tabId

    @property
    def source(self):
        return self._source

    @property
    def season(self):
        return self._ctx.season

    @property
    def currentOutfit(self):
        return self._modifiedOutfits[self.season]

    @property
    def selectedSlot(self):
        return self._selectedSlot

    @property
    def selectedItem(self):
        return self._selectedItem

    @property
    def isRegion(self):
        return self.tabId in CustomizationTabs.REGIONS

    @property
    def slotType(self):
        return CustomizationTabs.SLOT_TYPES[self.tabId]

    @property
    def _events(self):
        return self._ctx.events

    def start(self, tabId=None, source=None):
        if tabId is not None and tabId not in self._tabs:
            tabId = None
            _logger.warning('Wrong tabId: %s for current customization mode: %s', tabId, self._ctx.modeId)
        self._tabId = tabId or first(self._tabs)
        self._source = source or CustomizationModeSource.UNDEFINED
        self._onStart()
        return

    def stop(self):
        self._onStop()

    def fini(self):
        self._originalOutfits.clear()
        self._modifiedOutfits.clear()
        self._state.clear()
        self._isInited = False
        self._ctx = None
        return

    def changeTab(self, tabId, itemCD=None):
        if tabId not in self._tabs:
            _logger.warning('Wrong tabId: %s for current customization mode: %s', tabId, self._ctx.modeId)
            return
        if self._tabId == tabId:
            return
        self.unselectItem()
        self.unselectSlot()
        self._tabId = tabId
        self._events.onTabChanged(tabId, itemCD)

    def selectSlot(self, slotId):
        if self._selectSlot(slotId):
            self._events.onSlotSelected(self.selectedSlot)

    def unselectSlot(self):
        if self._unselectSlot():
            self._events.onSlotUnselected()

    def selectItem(self, intCD, progressionLevel=-1):
        if self._selectItem(intCD, progressionLevel):
            self._events.onItemSelected(self.selectedItem.intCD)

    def unselectItem(self):
        if self._unselectItem():
            self._events.onItemUnselected()

    def installItem(self, intCD, slotId, season=None, component=None):
        item = self._service.getItemByCD(intCD)
        errors = self._validateItem(item, slotId, season)
        if errors:
            for error in errors:
                error()

            return False
        elif not self._installItem(intCD, slotId, season, component):
            return False
        else:
            self._ctx.refreshOutfit(season)
            component = self.getComponentFromSlot(slotId, season)
            if isItemLimitReached(item, self._modifiedOutfits, self):
                if component is None or component.isFilled():
                    self._events.onItemLimitReached(item)
            self._events.onItemInstalled(item, slotId, season, component)
            return True

    def removeItem(self, slotId, season=None, refresh=True):
        self._removeItem(slotId, season)
        if refresh:
            self._ctx.refreshOutfit(season)
            self._events.onItemsRemoved(slotId)

    def removeFromSlots(self, slotIds, season=None):
        season = season or self.season
        for slotId in slotIds:
            self.removeItem(slotId, season, refresh=False)

        self._ctx.refreshOutfit(season)
        self._events.onItemsRemoved()

    def removeItemsFromSeason(self, season=None, filterMethod=None, refresh=True):
        season = season or self.season
        outfit = self._modifiedOutfits[season]
        for intCD, _, regionIdx, container, _ in outfit.itemsFull():
            item = self._service.getItemByCD(intCD)
            if item.isHiddenInUI():
                continue
            if filterMethod is None or filterMethod(item):
                areaId = container.getAreaID()
                slotType = ITEM_TYPE_TO_SLOT_TYPE[item.itemTypeID]
                slotId = C11nId(areaId, slotType, regionIdx)
                self.removeItem(slotId, season, refresh=False)

        if refresh:
            self._ctx.refreshOutfit(season)
            self._events.onItemsRemoved()
        return

    def applyItems(self, purchaseItems, isModeChanged=False):
        purchaseItems = copy(purchaseItems)
        self._applyItems(purchaseItems, isModeChanged)

    def sellItem(self, intCD, count, _):
        if not count:
            return
        item = self._service.getItemByCD(intCD)
        self._sellItem(item, count)
        nextTick(self._ctx.refreshOutfit)()
        nextTick(partial(self._events.onItemSold, item=item, count=count))()

    def cancelChanges(self):
        self._cancelChanges()
        self._events.onChangesCanceled()

    def updateOutfits(self, preserve=False):
        if preserve:
            self._preserveState()
            self._fillOutfits()
            self._restoreState()
        else:
            self._fillOutfits()
        self._fitOutfits()

    def onVehicleChangeStarted(self):
        self._onVehicleChangeStarted()

    def getModifiedOutfit(self, season=None):
        season = season or self.season
        if season not in self._modifiedOutfits:
            _logger.warning('Wrong season %s', self.season)
            return None
        else:
            return self._modifiedOutfits[season]

    def getOriginalOutfit(self, season=None):
        season = season or self.season
        if season not in self._originalOutfits:
            _logger.warning('Wrong season %s', self.season)
            return None
        else:
            return self._originalOutfits[season]

    def getModifiedOutfits(self):
        return deepcopy(self._modifiedOutfits)

    def getOutfitsInfo(self):
        outfitsInfo = {}
        for season in SeasonType.COMMON_SEASONS:
            outfitsInfo[season] = OutfitInfo(self._originalOutfits[season], self._modifiedOutfits[season])

        return outfitsInfo

    def getItemInventoryCount(self, item, excludeBase=False):
        return getItemInventoryCount(item, self._modifiedOutfits)

    def getItemAppliedCount(self, item):
        return getItemAppliedCount(item, self._modifiedOutfits)

    def getPurchaseLimit(self, item):
        return getPurchaseLimit(item, self._modifiedOutfits)

    def getAppliedItems(self, isOriginal=True):
        return self._getAppliedItems(isOriginal)

    def isOutfitsEmpty(self):
        return self._isOutfitsEmpty()

    def isOutfitsModified(self):
        return self._isOutfitsModified()

    def getAnchorVOs(self):
        return self._getAnchorVOs()

    def getSlotDataFromSlot(self, slotId, season=None):
        season = season or self.season
        outfit = self._modifiedOutfits[season]
        return getSlotDataFromSlot(outfit, slotId)

    def getItemFromSlot(self, slotId, season=None):
        season = season or self.season
        outfit = self._modifiedOutfits[season]
        return getItemFromSlot(outfit, slotId)

    def getComponentFromSlot(self, slotId, season=None):
        season = season or self.season
        outfit = self._modifiedOutfits[season]
        return getComponentFromSlot(outfit, slotId)

    def getAnchorParams(self, slotId):
        anchorParams = self._service.getAnchorParams(slotId.areaId, slotId.slotType, slotId.regionIdx)
        return anchorParams

    @process('customizationApply')
    def _applyItems(self, modifiedOutfits, isModeChanged):
        raise NotImplementedError

    @process('sellItem')
    def _sellItem(self, item, count):
        raise NotImplementedError

    def _preserveState(self):
        self._state = deepcopy(self._modifiedOutfits)

    def _fillOutfits(self):
        raise NotImplementedError

    def _restoreState(self):
        self._modifiedOutfits = self._state
        self._state = {}

    def _selectSlot(self, slotId):
        raise NotImplementedError

    def _unselectSlot(self):
        raise NotImplementedError

    def _selectItem(self, intCD, progressionLevel):
        raise NotImplementedError

    def _unselectItem(self):
        raise NotImplementedError

    def _installItem(self, intCD, slotId, season=None, component=None):
        raise NotImplementedError

    def _removeItem(self, slotId, season=None):
        raise NotImplementedError

    def _onStart(self):
        if not self.isInited:
            self.updateOutfits()
            self._isInited = True

    def _onStop(self):
        pass

    def _cancelChanges(self):
        for season in SeasonType.COMMON_SEASONS:
            self._modifiedOutfits[season] = self._originalOutfits[season].copy()
            self._ctx.refreshOutfit(season)

    def _getAppliedItems(self, isOriginal=True):
        if isOriginal:
            outfits = self._originalOutfits
            seasons = SeasonType.COMMON_SEASONS
        else:
            outfits = self._modifiedOutfits
            seasons = (self._ctx.season,)
        appliedItems = set()
        for seasonType in seasons:
            outfit = outfits[seasonType]
            appliedItems.update((intCD for intCD in outfit.items()))

        return appliedItems

    def _validateItem(self, item, slotId, season):
        errors = []
        if isItemLimitReached(item, self._modifiedOutfits, self):
            error = partial(SystemMessages.pushI18nMessage, key=SYSTEM_MESSAGES.CUSTOMIZATION_PROHIBITED, type=SystemMessages.SM_TYPE.Warning, itemName=item.userName)
            errors.append(error)
        return errors

    def _removeHiddenFromOutfit(self, outfit, vehicleIntCD):
        toRemove = []
        for itemCD, count in outfit.itemsCounter.iteritems():
            item = self._service.getItemByCD(itemCD)
            if not item.isHidden or item.isStyleOnly or item.isHiddenInUI():
                continue
            if item.fullInventoryCount(vehicleIntCD) < count:
                toRemove.append(itemCD)

        if toRemove:
            removeItemsFromOutfit(outfit, filterMethod=lambda i: i.intCD in toRemove)

    def _isOutfitsEmpty(self):
        raise NotImplementedError

    def _isOutfitsModified(self):
        raise NotImplementedError

    def _getAnchorVOs(self):
        raise NotImplementedError

    def _onVehicleChangeStarted(self):
        pass

    def _fitOutfits(self, modifiedOnly=False):
        availableRegionsMap = getCurrentVehicleAvailableRegionsMap()
        for season in SeasonType.COMMON_SEASONS:
            fitOutfit(self._modifiedOutfits[season], availableRegionsMap)
            if not modifiedOnly:
                fitOutfit(self._originalOutfits[season], availableRegionsMap)