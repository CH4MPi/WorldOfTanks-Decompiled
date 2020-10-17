# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/server_events/awards_formatters.py
import logging
from collections import namedtuple
from math import ceil
import typing
from constants import LOOTBOX_TOKEN_PREFIX, PREMIUM_ENTITLEMENTS, RESOURCE_TOKEN_PREFIX
from gui.Scaleform.genConsts.SLOT_HIGHLIGHT_TYPES import SLOT_HIGHLIGHT_TYPES
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.Scaleform.settings import ICONS_SIZES
from gui.impl import backport
from gui.impl.gen import R
from gui.ranked_battles.constants import YEAR_POINTS_TOKEN
from gui.server_events.formatters import parseComplexToken, TOKEN_SIZES
from gui.server_events.recruit_helper import getRecruitInfo
from gui.shared.formatters import text_styles
from gui.shared.gui_items import GUI_ITEM_TYPE, getItemIconName
from gui.shared.gui_items.Tankman import getRoleUserName
from gui.shared.gui_items.badge import Badge
from gui.shared.gui_items.crew_skin import localizedFullName, Rarity
from gui.shared.gui_items.customization import CustomizationTooltipContext
from gui.shared.money import Currency
from gui.shared.utils.functions import makeTooltip
from gui.shared.utils.requesters import REQ_CRITERIA
from helpers import time_utils, i18n, dependency
from items.tankmen import RECRUIT_TMAN_TOKEN_PREFIX
from personal_missions import PM_BRANCH
from shared_utils import CONST_CONTAINER, findFirst
from skeletons.gui.customization import ICustomizationService
from skeletons.gui.game_control import IEventProgressionController
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.shared import IItemsCache
if typing.TYPE_CHECKING:
    from typing import Callable
    from gui.goodies.goodie_items import Booster
    from gui.server_events.bonuses import SimpleBonus, CrystalBonus, GoodiesBonus, PlusPremiumDaysBonus
    from gui.server_events.cond_formatters.formatters import ConditionFormatter
    from gui.shared.gui_items.crew_book import CrewBook
_logger = logging.getLogger(__name__)
EPIC_AWARD_SIZE = 's360x270'

class AWARDS_SIZES(CONST_CONTAINER):
    SMALL = 'small'
    BIG = 'big'


class COMPLETION_TOKENS_SIZES(CONST_CONTAINER):
    SMALL = 'small'
    BIG = 'big'
    HUGE = 'huge'


class LABEL_ALIGN(CONST_CONTAINER):
    RIGHT = 'right'
    CENTER = 'center'


PACK_RENT_VEHICLES_BONUS = 'packRentVehicleBonus'
BATTLE_BONUS_X5_TOKEN = 'battle_bonus_x5'
AWARD_IMAGES = {AWARDS_SIZES.SMALL: {Currency.CREDITS: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CREDITS,
                      Currency.GOLD: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_GOLD,
                      Currency.CRYSTAL: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CRYSTAL,
                      Currency.EVENT_COIN: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_EVENTCOIN,
                      'creditsFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CREDITS,
                      'freeXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP,
                      'freeXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP,
                      'tankmenXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_TANKMENXP,
                      'tankmenXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_TANKMENXP,
                      'xp': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_EXP,
                      'xpFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_EXP,
                      'dailyXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP},
 AWARDS_SIZES.BIG: {Currency.CREDITS: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CREDITS,
                    Currency.GOLD: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_GOLD,
                    Currency.CRYSTAL: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CRYSTAL,
                    Currency.EVENT_COIN: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_EVENTCOIN,
                    'creditsFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CREDITS,
                    'freeXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP,
                    'freeXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP,
                    'tankmenXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_TANKMENXP,
                    'tankmenXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_TANKMENXP,
                    'xp': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_EXP,
                    'xpFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_EXP,
                    'dailyXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP}}

def _getMultiplierFormatter(formatter):

    def wrapper(text):
        return formatter('x{}'.format(text))

    return wrapper


TEXT_FORMATTERS = {Currency.CREDITS: text_styles.credits,
 Currency.GOLD: text_styles.gold,
 Currency.CRYSTAL: text_styles.crystal,
 Currency.EVENT_COIN: text_styles.eventCoin,
 'creditsFactor': _getMultiplierFormatter(text_styles.credits),
 'freeXP': text_styles.expText,
 'freeXPFactor': _getMultiplierFormatter(text_styles.expText),
 'tankmenXP': text_styles.expText,
 'tankmenXPFactor': _getMultiplierFormatter(text_styles.expText),
 'xp': text_styles.expText,
 'xpFactor': _getMultiplierFormatter(text_styles.expText),
 'dailyXPFactor': _getMultiplierFormatter(text_styles.expText),
 'vehicles': text_styles.gold,
 'tmanToken': text_styles.stats}
TEXT_ALIGNS = {'creditsFactor': LABEL_ALIGN.RIGHT,
 'freeXPFactor': LABEL_ALIGN.RIGHT,
 'tankmenXPFactor': LABEL_ALIGN.RIGHT,
 'dailyXPFactor': LABEL_ALIGN.RIGHT,
 'xpFactor': LABEL_ALIGN.RIGHT}

def getCompensationFormattersMap():
    return {'vehicles': VehiclesCompensationFormatter(),
     'crewSkins': CrewSkinsCompensationFormatter()}


def getDefaultFormattersMap():
    simpleBonusFormatter = SimpleBonusFormatter()
    tokenBonusFormatter = TokenBonusFormatter()
    countableIntegralBonusFormatter = CountableIntegralBonusFormatter()
    return {'strBonus': simpleBonusFormatter,
     Currency.GOLD: simpleBonusFormatter,
     Currency.CREDITS: simpleBonusFormatter,
     Currency.CRYSTAL: simpleBonusFormatter,
     Currency.EVENT_COIN: simpleBonusFormatter,
     'freeXP': simpleBonusFormatter,
     'xp': simpleBonusFormatter,
     'tankmenXP': simpleBonusFormatter,
     'xpFactor': simpleBonusFormatter,
     'creditsFactor': simpleBonusFormatter,
     'freeXPFactor': simpleBonusFormatter,
     'tankmenXPFactor': simpleBonusFormatter,
     'dailyXPFactor': simpleBonusFormatter,
     PREMIUM_ENTITLEMENTS.BASIC: PremiumDaysBonusFormatter(),
     PREMIUM_ENTITLEMENTS.PLUS: PremiumDaysBonusFormatter(),
     'vehicles': VehiclesBonusFormatter(),
     'meta': simpleBonusFormatter,
     'tokens': tokenBonusFormatter,
     'tankwomanBonus': TankwomanBonusFormatter(),
     'battleToken': tokenBonusFormatter,
     'tankmen': TankmenBonusFormatter(),
     'customizations': CustomizationsBonusFormatter(),
     'goodies': GoodiesBonusFormatter(),
     'items': ItemsBonusFormatter(),
     'dossier': DossierBonusFormatter(),
     'progressionXPToken': tokenBonusFormatter,
     'blueprints': BlueprintBonusFormatter(),
     'blueprintsAny': BlueprintBonusFormatter(),
     'finalBlueprints': BlueprintBonusFormatter(),
     'crewSkins': CrewSkinsBonusFormatter(),
     'crewBooks': CrewBooksBonusFormatter(),
     'slots': countableIntegralBonusFormatter,
     'berths': countableIntegralBonusFormatter,
     'entitlements': EntitlementFormatter(),
     'rankedDailyBattles': countableIntegralBonusFormatter,
     'rankedBonusBattles': countableIntegralBonusFormatter}


def getEpicFormattersMap():
    return {Currency.CRYSTAL: CrystalEpicBonusFormatter(),
     'goodies': GoodiesEpicBonusFormatter(),
     'crewBooks': CrewBooksEpicBonusFormatter(),
     PREMIUM_ENTITLEMENTS.PLUS: PremiumDaysEpicBonusFormatter(),
     'items': ItemsEpicBonusFormatter(),
     'blueprints': BlueprintGroupEpicBonusFormatter()}


def getEventBoardsFormattersMap():
    mapping = getDefaultFormattersMap()
    mapping.update({'dossier': EventBoardsDossierBonusFormatter(),
     'badgesGroup': BadgesGroupBonusFormatter()})
    return mapping


def getLinkedSetFormattersMap():
    tokenBonusFormatter = LinkedSetTokenBonusFormatter()
    mapping = getDefaultFormattersMap()
    mapping.update({'battleToken': tokenBonusFormatter,
     'tokens': tokenBonusFormatter,
     'items': LinkedSetItemsBonusFormatter(),
     PREMIUM_ENTITLEMENTS.BASIC: LinkedSetPremiumDaysBonusFormatter(),
     PREMIUM_ENTITLEMENTS.PLUS: LinkedSetPremiumDaysBonusFormatter(),
     'vehicles': LinkedSetVehiclesBonusFormatter(),
     'customizations': LinkedSetCustomizationsBonusFormatter()})
    return mapping


def getEpicSetFormattersMap():
    mapping = getDefaultFormattersMap()
    tokenBonusFormatter = EpicTokensFormatter()
    mapping.update({'abilityPts': EpicAbilityPtsFormatter(),
     'tokens': tokenBonusFormatter,
     'battleToken': tokenBonusFormatter,
     'items': EpicItemsBonusFormatter(),
     'dossier': EpicDossierBonusFormatter()})
    return mapping


def getPackRentVehiclesFormattersMap():
    mapping = getDefaultFormattersMap()
    mapping.update({'vehicles': RentVehiclesBonusFormatter()})
    return mapping


def getLootboxesFormatterMap():
    mapping = getDefaultFormattersMap()
    mapping.update({'vehicles': RentVehiclesBonusFormatter(),
     'tmanToken': TmanTemplateBonusFormatter()})
    return mapping


def getPostBattleFormatterMap():
    mapping = getLootboxesFormatterMap()
    mapping.update({'blueprints': BlueprintGroupBonusFormatter(),
     'finalBlueprints': BlueprintGroupBonusFormatter()})
    return mapping


def getRankedFormatterMap():
    tokenBonusFormatter = RankedPointFormatter()
    mapping = getDefaultFormattersMap()
    mapping.update({'tokens': tokenBonusFormatter,
     'battleToken': tokenBonusFormatter,
     'vehicles': RankedVehiclesBonusFormatter(),
     'items': RankedItemsBonusFormatter()})
    return mapping


def getBattlePassFormatterMap():
    mapping = getDefaultFormattersMap()
    mapping.update({'blueprints': BlueprintGroupBonusFormatter(),
     'finalBlueprints': BlueprintGroupBonusFormatter(),
     'items': EpicItemsBonusFormatter(),
     PREMIUM_ENTITLEMENTS.BASIC: BattlePassPremiumDaysBonusFormatter(),
     PREMIUM_ENTITLEMENTS.PLUS: BattlePassPremiumDaysBonusFormatter()})
    return mapping


def getRoyaleFormatterMap():
    simpleBonusFormatter = SimpleBonusFormatter()
    return {Currency.GOLD: simpleBonusFormatter,
     Currency.CREDITS: simpleBonusFormatter,
     Currency.CRYSTAL: simpleBonusFormatter,
     PREMIUM_ENTITLEMENTS.BASIC: PremiumDaysBonusFormatter(),
     PREMIUM_ENTITLEMENTS.PLUS: PremiumDaysBonusFormatter(),
     'customizations': CustomizationsBonusFormatter(),
     'dossier': DossierBonusFormatter()}


def getDefaultAwardFormatter():
    return AwardsPacker(getDefaultFormattersMap())


def getEpicAwardFormatter():
    return AwardsPacker(getEpicFormattersMap())


def getEpicViewAwardPacker():
    return AwardsPacker(getEpicSetFormattersMap())


def getLinkedSetAwardPacker():
    return AwardsPacker(getLinkedSetFormattersMap())


def getEventBoardsAwardPacker():
    return AwardsPacker(getEventBoardsFormattersMap())


def getPackRentVehiclesAwardPacker():
    return AwardsPacker(getPackRentVehiclesFormattersMap())


def getLootboxesAwardsPacker():
    return AwardsPacker(getLootboxesFormatterMap())


def getPostBattleAwardsPacker():
    return AwardsPacker(getPostBattleFormatterMap())


def getRankedAwardsPacker():
    return AwardsPacker(getRankedFormatterMap())


def getRoyaleAwardsPacker():
    return AwardsPacker(getRoyaleFormatterMap())


def getPersonalMissionAwardPacker():
    mapping = getDefaultFormattersMap()
    mapping.update({'completionTokens': CompletionTokensBonusFormatter(),
     'freeTokens': FreeTokensBonusFormatter()})
    return AwardsPacker(mapping)


def getOperationPacker():
    mapping = getDefaultFormattersMap()
    mapping.update({'customizations': OperationCustomizationsBonusFormatter(),
     'battleToken': CustomizationUnlockFormatter()})
    return AwardsPacker(mapping)


def getAnniversaryPacker():
    formattersMap = getDefaultFormattersMap()
    formattersMap['dossier'] = LoyalServiceBonusFormatter()
    return AwardsPacker(formattersMap)


def getBattlePassAwardsPacker():
    return AwardsPacker(getBattlePassFormatterMap())


def formatCountLabel(count, defaultStr=''):
    return 'x{}'.format(count) if count > 1 else defaultStr


def formatTimeLabel(hours):
    time = hours
    if hours >= time_utils.HOURS_IN_DAY:
        time = ceil(hours / time_utils.HOURS_IN_DAY)
        timeMetric = i18n.makeString('#menu:header/account/premium/days')
    else:
        timeMetric = i18n.makeString('#menu:header/account/premium/hours')
    return str(int(time)) + ' ' + timeMetric


_PreformattedBonus = namedtuple('_PreformattedBonus', 'bonusName label userName images tooltip labelFormatter areTokensPawned specialArgs specialAlias isSpecial isCompensation align highlightType overlayType highlightIcon overlayIcon compensationReason postProcessTags')

class PostProcessTags(CONST_CONTAINER):
    IS_SUFFIX_BADGE = 'isSuffixBadge'
    IS_PREFIX_BADGE = 'isPrefixBadge'

    @classmethod
    def getBadgeTag(cls, badge):
        return cls.IS_SUFFIX_BADGE if badge.isSuffixLayout() else cls.IS_PREFIX_BADGE


class PreformattedBonus(_PreformattedBonus):

    def getImage(self, size):
        return self.images.get(size, '')

    def getFormattedLabel(self, formatter=None):
        formatter = formatter or self.labelFormatter
        return formatter(self.label) if formatter and self.label else self.label

    def getHighlightType(self, size):
        types = self.highlightType
        return types and types.get(size, SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT) or SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT

    def getOverlayType(self, size):
        types = self.overlayType
        return types and types.get(size, SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT) or SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT

    def getHighlightIcon(self, size):
        icons = self.highlightIcon
        return icons and icons.get(size, SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT) or SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT

    def getOverlayIcon(self, size):
        icons = self.overlayIcon
        return icons and icons.get(size, SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT) or SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT


PreformattedBonus.__new__.__defaults__ = (None,
 None,
 None,
 None,
 None,
 None,
 False,
 None,
 None,
 False,
 False,
 LABEL_ALIGN.CENTER,
 None,
 None,
 None,
 None,
 None,
 tuple())

class QuestsBonusComposer(object):

    def __init__(self, awardsFormatter=None):
        self.__bonusFormatter = awardsFormatter or getDefaultAwardFormatter()

    def getPreformattedBonuses(self, bonuses):
        return self.__bonusFormatter.format(bonuses)

    def getFormattedBonuses(self, bonuses, size=AWARDS_SIZES.SMALL):
        preformattedBonuses = self.getPreformattedBonuses(bonuses)
        return self._packBonuses(preformattedBonuses, size)

    def _packBonuses(self, preformattedBonuses, size):
        result = []
        for b in preformattedBonuses:
            result.append(self._packBonus(b, size))

        return result

    def _packBonus(self, bonus, size=AWARDS_SIZES.SMALL):
        return {'label': bonus.getFormattedLabel(),
         'imgSource': bonus.getImage(size),
         'tooltip': bonus.tooltip,
         'isSpecial': bonus.isSpecial,
         'specialAlias': bonus.specialAlias,
         'specialArgs': bonus.specialArgs,
         'align': bonus.align,
         'userName': bonus.userName}


class AwardsPacker(object):

    def __init__(self, formatters=None):
        self.__formatters = formatters or {}

    def format(self, bonuses):
        preformattedBonuses = []
        for b in bonuses:
            if b.isShowInGUI():
                bonusName = b.getName()
                formatter = self._getBonusFormatter(bonusName)
                if formatter:
                    preformattedBonuses.extend(formatter.format(b))
                else:
                    _logger.warn('No formatter found for %s', bonusName)

        return preformattedBonuses

    def getFormatters(self):
        return self.__formatters

    def _getBonusFormatter(self, bonusName):
        return self.__formatters.get(bonusName)


class AwardFormatter(object):

    def format(self, bonus):
        return self._format(bonus)

    def _format(self, bonus):
        return None


class SimpleBonusFormatter(AwardFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), label=self._getLabel(bonus), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus), highlightType=self._getHighlightType(bonus), overlayType=self._getOverlayType(bonus), highlightIcon=self._getHighlightIcon(bonus), overlayIcon=self._getOverlayIcon(bonus), compensationReason=self._getCompensationReason(bonus))]

    @classmethod
    def _getUserName(cls, bonus):
        return i18n.makeString(QUESTS.getBonusName(bonus.getName()))

    @classmethod
    def _getLabel(cls, bonus):
        return bonus.formatValue()

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return TEXT_FORMATTERS.get(bonus.getName(), text_styles.stats)

    @classmethod
    def _getLabelAlign(cls, bonus):
        return TEXT_ALIGNS.get(bonus.getName(), LABEL_ALIGN.CENTER)

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = AWARD_IMAGES.get(size, {}).get(bonus.getName())

        return result

    @classmethod
    def _isCompensation(cls, bonus):
        return bonus.isCompensation()

    @classmethod
    def _getHighlightType(cls, item):
        return {}

    @classmethod
    def _getOverlayType(cls, item):
        return {}

    @classmethod
    def _getHighlightIcon(cls, item):
        return {}

    @classmethod
    def _getOverlayIcon(cls, item):
        return {}

    @classmethod
    def _getCompensationReason(cls, bonus):
        compensationReasonBonus = bonus.getCompensationReason()
        if compensationReasonBonus is not None:
            bonusName = compensationReasonBonus.getName()
            bonusFormatter = getCompensationFormattersMap().get(bonusName)
            if bonusFormatter is not None:
                formattedReason = bonusFormatter.format(compensationReasonBonus)
                if formattedReason:
                    return formattedReason[0]
                return
        return


class CrystalEpicBonusFormatter(SimpleBonusFormatter):

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.textEpic

    @classmethod
    def _getImages(cls, bonus):
        size = EPIC_AWARD_SIZE
        return {size: RES_ICONS.getBonusIcon(size, bonus.getName())}


class CountableIntegralBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), label=formatCountLabel(bonus.getValue()), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.stats

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, bonus.getName())

        return result


class CompletionTokensBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        uniqueName = self._getUniqueName(bonus)
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(uniqueName), label=formatCountLabel(bonus.getCount()), images=self._getImages(uniqueName), tooltip=self._getTooltip(uniqueName), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT)]

    @classmethod
    def _getUserName(cls, nameID):
        return i18n.makeString(QUESTS.getBonusName(nameID))

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in COMPLETION_TOKENS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result

    @classmethod
    def _getTooltip(cls, tooltipID):
        header = i18n.makeString(TOOLTIPS.getAwardHeader(tooltipID))
        body = i18n.makeString(TOOLTIPS.getAwardBody(tooltipID))
        return makeTooltip(header or None, body or None) if header or body else ''

    @classmethod
    def _getUniqueName(cls, bonus):
        context = bonus.getContext()
        operationID = context['operationID']
        chainID = context['chainID']
        return '%s_%s_%s' % (bonus.getName(), operationID, chainID)


class FreeTokensBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        areTokensPawned = bonus.areTokensPawned()
        ctx = bonus.getContext()
        if areTokensPawned:
            specialAlias = TOOLTIPS_CONSTANTS.FREE_SHEET_USED
            specialArgs = [ctx.get('campaignID')]
        else:
            specialAlias = TOOLTIPS_CONSTANTS.FREE_SHEET
            specialArgs = [ctx.get('campaignID')]
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(bonus), label=formatCountLabel(bonus.getCount()), images=self._getImages(bonus.getImageFileName()), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT, isCompensation=bonus.isCompensation(), isSpecial=True, specialAlias=specialAlias, specialArgs=specialArgs, areTokensPawned=areTokensPawned)]

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result


class PremiumDaysBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            imgPath = RES_ICONS.getPremiumDaysAwardIcon(size, bonus.getName(), bonus.getValue())
            if imgPath is None:
                imgPath = RES_ICONS.getPremiumDaysAwardIcon(size, bonus.getName(), 'universal')
            result[size] = imgPath

        return result


class PremiumDaysEpicBonusFormatter(PremiumDaysBonusFormatter):

    @classmethod
    def _getImages(cls, bonus):
        size = EPIC_AWARD_SIZE
        return {size: RES_ICONS.getPremiumDaysAwardIcon(size, bonus.getName(), bonus.getValue())}


class BattlePassPremiumDaysBonusFormatter(SimpleBonusFormatter):
    __PREMIUM_DAYS_ICONS = (1, 2, 3, 7, 14, 30, 90, 180, 360)

    def _format(self, bonus):
        count = bonus.getValue()
        hasOwnIcon = count in self.__PREMIUM_DAYS_ICONS
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(bonus), label=formatCountLabel(1 if hasOwnIcon else bonus.getValue()), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT, images=self._getImages(bonus, hasIcon=hasOwnIcon), tooltip=bonus.getTooltip(), isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getImages(cls, bonus, hasIcon=False):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getPremiumDaysAwardIcon(size, bonus.getName(), bonus.getValue() if hasIcon else 1)

        return result


class LinkedSetPremiumDaysBonusFormatter(PremiumDaysBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(label=formatTimeLabel(bonus.getValue() * time_utils.HOURS_IN_DAY), bonusName=bonus.getName(), userName=self._getUserName(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), isCompensation=self._isCompensation(bonus))]


class TokenBonusFormatter(SimpleBonusFormatter):
    eventsCache = dependency.descriptor(IEventsCache)
    itemsCache = dependency.descriptor(IItemsCache)
    _eventProgressionController = dependency.descriptor(IEventProgressionController)

    @staticmethod
    def getBattleBonusX5Tooltip(*args):
        return makeTooltip(header=backport.text(R.strings.tooltips.quests.bonuses.token.battle_bonus_x5.header()), body=backport.text(R.strings.tooltips.quests.bonuses.token.battle_bonus_x5.body()))

    def _format(self, bonus):
        result = []
        for tokenID, token in bonus.getTokens().iteritems():
            formatted = self._getFormattedBonus(tokenID, token, bonus)
            if formatted is not None:
                result.append(formatted)
            if self._eventProgressionController.isAvailable() and self._eventProgressionController.getProgressionXPTokenID() and tokenID.startswith(self._eventProgressionController.getProgressionXPTokenID()):
                formatted = self._formatProgressionXPToken(token, bonus)
                if formatted is not None:
                    result.append(formatted)

        return result

    def _getFormattedBonus(self, tokenID, token, bonus):
        formatted = None
        complexToken = parseComplexToken(tokenID)
        if complexToken.isDisplayable:
            formatted = self._formatComplexToken(complexToken, token, bonus)
        elif tokenID.startswith(LOOTBOX_TOKEN_PREFIX):
            formatted = self._formatLootBoxToken(tokenID, token, bonus)
        elif tokenID.startswith(BATTLE_BONUS_X5_TOKEN):
            formatted = self._formatBattleBonusToken(token, bonus)
        elif tokenID.startswith(RESOURCE_TOKEN_PREFIX):
            formatted = self._formatResource(token, bonus)
        return formatted

    def _formatBonusLabel(self, count):
        return formatCountLabel(count)

    def _getUserName(self, styleID):
        webCache = self.eventsCache.prefetcher
        return i18n.makeString(webCache.getTokenInfo(styleID))

    def _getTokenImages(self, styleID):
        result = {}
        webCache = self.eventsCache.prefetcher
        for awardSizeKey, awardSizeValue in AWARDS_SIZES.getIterator():
            for tokenSizeKey, tokenSizeValue in TOKEN_SIZES.getIterator():
                if awardSizeKey == tokenSizeKey:
                    result[awardSizeValue] = webCache.getTokenImage(styleID, tokenSizeValue)

        return result

    def _formatComplexToken(self, complexToken, token, bonus):
        userName = self._getUserName(complexToken.styleID)
        tooltip = makeTooltip(i18n.makeString(TOOLTIPS.QUESTS_BONUSES_TOKEN_HEADER, userName=userName), i18n.makeString(TOOLTIPS.QUESTS_BONUSES_TOKEN_BODY))
        return PreformattedBonus(bonusName=bonus.getName(), images=self._getTokenImages(complexToken.styleID), label=self._formatBonusLabel(token.count), userName=self._getUserName(complexToken.styleID), labelFormatter=self._getLabelFormatter(bonus), tooltip=tooltip, align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus))

    def _formatResource(self, token, bonus):
        images = {}
        tooltip = ''
        header = ''
        if hasattr(R.strings.tooltips.quests.bonuses.token.resource, bonus.resourceName):
            header = backport.text(getattr(R.strings.tooltips.quests.bonuses.token.resource, bonus.resourceName).header())
            tooltip = makeTooltip(header, backport.text(getattr(R.strings.tooltips.quests.bonuses.token.resource, bonus.resourceName).body()))
        for size in AWARDS_SIZES.ALL():
            images[size] = RES_ICONS.getResource(size, bonus.resourceName)

        return PreformattedBonus(bonusName=bonus.resourceName, images=images, label=self._formatBonusLabel(token.count), userName=header, labelFormatter=self._getLabelFormatter(bonus), tooltip=tooltip, align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus))

    def _formatLootBoxToken(self, tokenID, token, bonus):
        lootBox = self.itemsCache.items.tokens.getLootBoxByTokenID(tokenID)
        if lootBox is None or token.count <= 0:
            return
        else:
            images = {}
            for size in AWARDS_SIZES.ALL():
                images[size] = RES_ICONS.getLootBoxBonusIcon(size, lootBox.getType())

            return PreformattedBonus(label=self._formatBonusLabel(token.count), userName=lootBox.getUserName(), labelFormatter=self._getLabelFormatter(bonus), images=images, tooltip=makeTooltip(header=lootBox.getUserName(), body=''), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))

    def _formatBattleBonusToken(self, token, bonus):
        return None if token.count <= 0 else PreformattedBonus(bonusName=bonus.getName(), label=self._formatBonusLabel(token.count), userName=bonus.getUserName(), labelFormatter=self._getLabelFormatter(bonus), images=self.__getBattleBonusX5Images(), tooltip=self.getBattleBonusX5Tooltip(), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))

    def _formatProgressionXPToken(self, token, bonus):
        if token.count <= 0:
            return
        else:
            images = {}
            for size in AWARDS_SIZES.ALL():
                steelHunterPointRes = R.images.gui.maps.icons.quests.bonuses.dyn(size).dyn('steelHunterPoint')
                images[size] = backport.image(steelHunterPointRes()) if steelHunterPointRes else None

            header = backport.text(R.strings.tooltips.quests.bonuses.token.progressionExperience.header())
            body = backport.text(R.strings.tooltips.quests.bonuses.token.progressionExperience.body())
            return PreformattedBonus(bonusName=bonus.getName(), label=str(token.count), userName=header, labelFormatter=self._getLabelFormatter(bonus), images=images, tooltip=makeTooltip(header=header, body=body), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))

    @staticmethod
    def __getBattleBonusX5Images():
        images = {}
        for size in AWARDS_SIZES.ALL():
            bonusBattleTaskRes = R.images.gui.maps.icons.quests.bonuses.dyn(size).dyn('bonus_battle_task')
            images[size] = backport.image(bonusBattleTaskRes()) if bonusBattleTaskRes else None

        return images


class RankedPointFormatter(TokenBonusFormatter):

    def _format(self, bonus):
        result = []
        for tokenID, token in bonus.getTokens().iteritems():
            if tokenID.startswith(YEAR_POINTS_TOKEN):
                formatted = self.__formatRankedPointToken(tokenID, token, bonus)
                if formatted is not None:
                    result.append(formatted)

        return result

    @classmethod
    def _getUserName(cls, bonus):
        return backport.text(R.strings.tooltips.rankedBattleView.scorePoint.short.header())

    def __formatRankedPointToken(self, tokenID, token, bonus):
        images = {}
        for size in AWARDS_SIZES.ALL():
            rankedPointRes = R.images.gui.maps.icons.quests.bonuses.dyn(size).dyn('rankedPoint')
            images[size] = backport.image(rankedPointRes()) if rankedPointRes else None

        return PreformattedBonus(label=self._formatBonusLabel(token.count), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=images, tooltip=makeTooltip(header=backport.text(R.strings.tooltips.rankedBattleView.scorePoint.header()), body=backport.text(R.strings.tooltips.rankedBattleView.scorePoint.body())), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))

    @classmethod
    def _getLabelAlign(cls, bonus):
        return LABEL_ALIGN.RIGHT


class EpicTokensFormatter(TokenBonusFormatter):

    def _format(self, bonus):
        result = []
        for tokenID, token in bonus.getTokens().iteritems():
            if tokenID.startswith(self._eventProgressionController.rewardPointsTokenID):
                formatted = self.__formatRewardPointToken(tokenID, token, bonus)
                if formatted is not None:
                    result.append(formatted)
            if self._eventProgressionController.isAvailable() and self._eventProgressionController.getProgressionXPTokenID() and tokenID.startswith(self._eventProgressionController.getProgressionXPTokenID()):
                formatted = self._formatProgressionXPToken(token, bonus)
                if formatted is not None:
                    result.append(formatted)
            formatted = self._getFormattedBonus(tokenID, token, bonus)
            if formatted is not None:
                result.append(formatted)

        return result

    def __formatRewardPointToken(self, tokenID, token, bonus):
        images = {}
        for size in AWARDS_SIZES.ALL():
            res = R.images.gui.maps.icons.quests.bonuses.dyn(size).dyn('epicRewardPoint')
            if res:
                images[size] = backport.image(res())

        return PreformattedBonus(label=self._formatBonusLabel(token.count), userName=backport.text(R.strings.epic_battle.epicBattleItem.rewardPoints.header()), labelFormatter=self._getLabelFormatter(bonus), images=images, tooltip=makeTooltip(header=backport.text(R.strings.epic_battle.epicBattleItem.rewardPoints.header()), body=backport.text(R.strings.epic_battle.epicBattleItem.rewardPoints.description())), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))

    @classmethod
    def _getLabelAlign(cls, bonus):
        return LABEL_ALIGN.RIGHT


class EpicAbilityPtsFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(label=self._formatBonusLabel(bonus.getValue()), userName=backport.text(R.strings.epic_battle.epicBattleItem.rewardPoints.header()), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=makeTooltip(header=backport.text(R.strings.epic_battle.epicBattleItem.supplyPoints.header()), body=backport.text(R.strings.epic_battle.epicBattleItem.supplyPoints.description())), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))]

    def _formatBonusLabel(self, count):
        return formatCountLabel(count)

    @classmethod
    def _getImages(cls, bonus):
        images = {}
        for size in AWARDS_SIZES.ALL():
            res = R.images.gui.maps.icons.quests.bonuses.dyn(size).dyn('epicAbilityPoint')
            if res:
                images[size] = backport.image(res())

        return images

    @classmethod
    def _getLabelAlign(cls, bonus):
        return LABEL_ALIGN.RIGHT


class TmanTemplateBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for tokenID, token in bonus.getTokens().iteritems():
            if tokenID.startswith(RECRUIT_TMAN_TOKEN_PREFIX):
                formatted = self.__formatTmanTemplateToken(tokenID, token, bonus)
                if formatted is None:
                    _logger.error('Received wrong tman_template token from server: %s', tokenID)
                else:
                    result.append(formatted)

        return result

    def __formatTmanTemplateToken(self, tokenID, _, bonus):
        recruitInfo = getRecruitInfo(tokenID)
        if recruitInfo is None:
            return
        else:
            images = {}
            if recruitInfo.isFemale():
                bonusImageName = 'tankwoman'
            else:
                bonusImageName = 'tankman'
            for size in AWARDS_SIZES.ALL():
                images[size] = RES_ICONS.getBonusIcon(size, bonusImageName)

            nameStr = recruitInfo.getFullUserNameByNation(0)
            return PreformattedBonus(bonusName=bonus.getName(), userName=nameStr, label='', images=images, labelFormatter=self._getLabelFormatter(bonus), align=self._getLabelAlign(bonus), specialAlias=TOOLTIPS_CONSTANTS.TANKMAN_NOT_RECRUITED, specialArgs=[tokenID], isSpecial=True)


class LinkedSetTokenBonusFormatter(TokenBonusFormatter):

    def _formatBonusLabel(self, count):
        return 'x{}'.format(count)


class CustomizationUnlockFormatter(TokenBonusFormatter):
    c11n = dependency.descriptor(ICustomizationService)
    __TOKEN_POSTFIX = ':camouflage'
    __ICON_NAME = 'camouflage'

    def _format(self, bonus):
        tokens = bonus.getTokens()
        unlockTokenID = findFirst(lambda ID: ID.endswith(self.__TOKEN_POSTFIX), tokens.keys())
        if unlockTokenID is not None:
            camouflages = self.c11n.getCamouflages(criteria=REQ_CRITERIA.CUSTOMIZATION.UNLOCKED_BY(unlockTokenID))
            branch = bonus.getContext().get('branch')
            if branch == PM_BRANCH.REGULAR:
                tooltip = makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_BODY)
            elif branch == PM_BRANCH.PERSONAL_MISSION_2:
                tooltip = makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_ALLIANCE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_ALLIANCE_BODY)
            else:
                tooltip = None
            images = {size:RES_ICONS.getBonusIcon(size, self.__ICON_NAME) for size in AWARDS_SIZES.ALL()}
            result = [PreformattedBonus(bonusName=bonus.getName(), label=formatCountLabel(len(camouflages)), align=LABEL_ALIGN.RIGHT, images=images, isSpecial=False, tooltip=tooltip)]
        else:
            result = []
        return result


class VehiclesBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        result.extend(self._formatVehicle(bonus, bonus.getVehicles()))
        return result

    def _formatVehicle(self, bonus, vehicles):
        result = []
        for vehicle, vehInfo in vehicles:
            compensation = bonus.compensation(vehicle, bonus)
            if compensation:
                formatter = SimpleBonusFormatter()
                for bonusComp in compensation:
                    formattedComp = formatter.format(bonusComp)
                    result.extend(formattedComp)

            result.append(self._appendFormattedVehicle(bonus, vehicle, vehInfo))

        return result

    def _getUserName(self, vehicle):
        return vehicle.userName

    @classmethod
    def _getLabel(cls, vehicle):
        return vehicle.userName if cls.__hasUniqueIcon(vehicle) else ''

    @classmethod
    def _getVehicleLabel(cls, bonus, vehicle, vehInfo):
        return cls._getLabel(vehicle)

    @classmethod
    def _getImages(cls, vehicle, isRent=False):
        result = {}
        for size in AWARDS_SIZES.ALL():
            image = '../maps/icons/quests/bonuses/{}/{}'.format(size, getItemIconName(vehicle.name))
            if image in RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_ALL_ENUM:
                result[size] = image
            if isRent:
                image = RES_ICONS.getRentVehicleAwardIcon(size)
            else:
                image = RES_ICONS.getVehicleAwardIcon(size)
            result[size] = image

        return result

    @classmethod
    def __hasUniqueIcon(cls, vehicle):
        for size in AWARDS_SIZES.ALL():
            if cls._getImages(vehicle).get(size) != RES_ICONS.getVehicleAwardIcon(size):
                return True

        return False

    def _appendFormattedVehicle(self, bonus, vehicle, vehInfo):
        tmanRoleLevel = bonus.getTmanRoleLevel(vehInfo)
        rentDays = bonus.getRentDays(vehInfo)
        rentBattles = bonus.getRentBattles(vehInfo)
        rentWins = bonus.getRentWins(vehInfo)
        rentSeason = bonus.getRentSeason(vehInfo)
        if rentDays:
            rentExpiryTime = time_utils.getCurrentTimestamp()
            rentExpiryTime += rentDays * time_utils.ONE_DAY
        else:
            rentExpiryTime = 0
        isRent = rentDays or rentBattles or rentWins or rentSeason
        return PreformattedBonus(bonusName=bonus.getName(), label=self._getVehicleLabel(bonus, vehicle, vehInfo), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(vehicle), images=self._getImages(vehicle, isRent), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.AWARD_VEHICLE, specialArgs=[vehicle.intCD,
         tmanRoleLevel,
         rentExpiryTime,
         rentBattles,
         rentWins,
         rentSeason], isCompensation=self._isCompensation(bonus))


class RankedVehiclesBonusFormatter(VehiclesBonusFormatter):

    @classmethod
    def _getLabel(cls, vehicle):
        return vehicle.shortUserName

    @classmethod
    def _getVehicleLabel(cls, bonus, vehicle, vehInfo):
        return cls._getLabel(vehicle)

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.stats


class VehiclesCompensationFormatter(VehiclesBonusFormatter):

    def _formatVehicle(self, bonus, vehicles):
        result = []
        for vehicle, vehInfo in vehicles:
            compensation = bonus.checkIsCompensatedVehicle(vehicle)
            if compensation:
                result.append(self._appendFormattedVehicle(bonus, vehicle, vehInfo))

        return result

    @classmethod
    def _getLabel(cls, vehicle):
        return vehicle.shortUserName if cls.__hasUniqueIcon(vehicle) else ''

    @classmethod
    def __hasUniqueIcon(cls, vehicle):
        return True


class RentVehiclesBonusFormatter(VehiclesBonusFormatter):

    def _format(self, bonus):
        result = []
        rentVehicles = []
        restVehicles = []
        for vehicle, vehInfo in bonus.getVehicles():
            if bonus.isRentVehicle(vehInfo):
                rentVehicles.append((vehicle, vehInfo))
            if bonus.isNonZeroCompensation(vehInfo):
                restVehicles.append((vehicle, vehInfo))

        result.extend(self._formatRent(bonus, rentVehicles))
        result.extend(self._formatVehicle(bonus, restVehicles))
        return result

    def _formatRent(self, bonus, vehicles):
        result = []
        if not vehicles:
            return result
        if len(vehicles) == 1:
            result.extend(self._formatVehicle(bonus, vehicles))
        else:
            result.append(PreformattedBonus(bonusName=PACK_RENT_VEHICLES_BONUS, label=formatCountLabel(len(vehicles)), labelFormatter=text_styles.stats, images=self._getRentImages(), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.PACK_RENT_VEHICLES, specialArgs=self._getRentArgs(bonus, vehicles)))
        return result

    @classmethod
    def _getRentImages(cls):
        result = {}
        for size in AWARDS_SIZES.ALL():
            image = RES_ICONS.getRentVehicleAwardIcon(size)
            result[size] = image

        return result

    @classmethod
    def _getRentArgs(cls, bonus, vehicles):
        rentArgs = []
        for vehicle, vehInfo in vehicles:
            rentDays = bonus.getRentDays(vehInfo)
            rentBattles = bonus.getRentBattles(vehInfo)
            rentWins = bonus.getRentWins(vehInfo)
            shortData = {'vehicleName': vehicle.userName,
             'isPremium': vehicle.isPremium,
             'vehicleType': vehicle.type,
             'rentDays': rentDays,
             'rentBattles': rentBattles,
             'rentWins': rentWins}
            rentArgs.append(shortData)

        return rentArgs


class LinkedSetVehiclesBonusFormatter(VehiclesBonusFormatter):

    @classmethod
    def _getVehicleLabel(cls, bonus, vehicle, vehInfo):
        return formatTimeLabel(bonus.getRentDays(vehInfo) * time_utils.HOURS_IN_DAY)


class DossierBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for achievement in bonus.getAchievements():
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(achievement), images=self._getImages(achievement), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.BATTLE_STATS_ACHIEVS, specialArgs=[achievement.getBlock(), achievement.getName(), achievement.getValue()], isCompensation=self._isCompensation(bonus)))

        for badge in bonus.getBadges():
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(badge), images=self._getBadgeImages(badge), isSpecial=True, specialAlias=self._getBadgeTooltipAlias(), specialArgs=[badge.badgeID], isCompensation=self._isCompensation(bonus), postProcessTags=(PostProcessTags.getBadgeTag(badge),)))

        return result

    @classmethod
    def _getUserName(cls, achievement):
        return achievement.getUserName()

    @classmethod
    def _getImages(cls, bonus):
        return {AWARDS_SIZES.SMALL: bonus.getSmallIcon(),
         AWARDS_SIZES.BIG: bonus.getBigIcon()}

    @classmethod
    def _getBadgeImages(cls, bonus):
        return {AWARDS_SIZES.SMALL: bonus.getAwardBadgeIcon(ICONS_SIZES.X48),
         AWARDS_SIZES.BIG: bonus.getAwardBadgeIcon(ICONS_SIZES.X80)}

    @classmethod
    def _getBadgeTooltipAlias(cls):
        return TOOLTIPS_CONSTANTS.BADGE


class LoyalServiceBonusFormatter(DossierBonusFormatter):

    def _format(self, bonus):
        result = super(LoyalServiceBonusFormatter, self)._format(bonus)
        result.sort(key=lambda preFormattedBonus: int(not (PostProcessTags.IS_PREFIX_BADGE in preFormattedBonus.postProcessTags or PostProcessTags.IS_SUFFIX_BADGE in preFormattedBonus.postProcessTags)))
        return result

    @classmethod
    def _getBadgeTooltipAlias(cls):
        return TOOLTIPS_CONSTANTS.BADGE_LOYAL_SERVICE


class EventBoardsDossierBonusFormatter(DossierBonusFormatter):

    @classmethod
    def _getBadgeTooltipAlias(cls):
        return TOOLTIPS_CONSTANTS.EVENT_BOARDS_BADGE


class BadgesGroupBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        badges = bonus.getBadges()
        groupID = bonus.getValue()
        result.append(PreformattedBonus(images={AWARDS_SIZES.SMALL: RES_ICONS.getEventBoardBadgesGroup(groupID)}, isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.EVENT_BOARDS_BADGES_GROUP, specialArgs=self.__badgesTooltipData(badges), isCompensation=self._isCompensation(bonus)))
        return result

    @classmethod
    def __badgesTooltipData(cls, badges):
        result = []
        for badge in badges:
            result.append({'name': badge.getUserName(),
             'imgSource': badge.getSmallIcon(),
             'desc': badge.getUserDescription()})

        return result


class TankmenBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for group in bonus.getTankmenGroups().itervalues():
            if group['skills']:
                key = 'with_skills'
            else:
                key = 'no_skills'
            label = '#quests:bonuses/item/tankmen/%s' % key
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(key), images=self._getImages(bonus), tooltip=makeTooltip(TOOLTIPS.getAwardHeader(bonus.getName()), i18n.makeString(label, **group)), isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getUserName(cls, key):
        return i18n.makeString('#quests:bonusName/tankmen/%s' % key)

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, bonus.getName())

        return result


class TankwomanBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for tmanInfo in bonus.getTankmenData():
            if tmanInfo.isFemale:
                bonusID = 'tankwoman'
                username = i18n.makeString(QUESTS.BONUSES_ITEM_TANKWOMAN)
                result.append(PreformattedBonus(bonusName=bonus.getName(), userName=username, images=self._getImages(bonusID), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.PERSONAL_MISSIONS_TANKWOMAN, specialArgs=[]))
            bonusID = 'tankman'
            username = i18n.makeString(QUESTS.BONUSES_TANKMEN_DESCRIPTION, value=getRoleUserName(tmanInfo.role))
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=username, images=self._getImages(bonusID), tooltip=makeTooltip(i18n.makeString(QUESTS.BONUSES_TANKMEN_DESCRIPTION, value=getRoleUserName(tmanInfo.role)))))

        return result

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result


class CustomizationsBonusFormatter(SimpleBonusFormatter):
    c11n = dependency.descriptor(ICustomizationService)

    def _format(self, bonus):
        customizations = zip(bonus.getCustomizations(), bonus.getList())
        result = [ self._createCustomizationBonus(bonus, item, data) for item, data in customizations ]
        return result

    def _formatBonusLabel(self, count):
        return formatCountLabel(count)

    def _createCustomizationBonus(self, bonus, item, data):
        c11nItem = bonus.getC11nItem(item)
        return PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(c11nItem), userName=self._getUserName(c11nItem), label=self._formatBonusLabel(item.get('value')), labelFormatter=self._getLabelFormatter(bonus), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.TECH_CUSTOMIZATION_ITEM_AWARD, specialArgs=CustomizationTooltipContext(itemCD=data.get('intCD')), isCompensation=self._isCompensation(bonus), align=LABEL_ALIGN.RIGHT)

    @classmethod
    def _getImages(cls, c11nItem):
        result = {}
        for size in AWARDS_SIZES.ALL():
            iconName = c11nItem.itemTypeName
            if iconName == 'style' and c11nItem.modelsSet:
                iconName = 'style_3d'
            result[size] = RES_ICONS.getBonusIcon(size, iconName)

        return result

    @classmethod
    def _getUserName(cls, c11nItem):
        return i18n.makeString(QUESTS.getBonusName(c11nItem.itemTypeName))


class LinkedSetCustomizationsBonusFormatter(CustomizationsBonusFormatter):

    def _formatBonusLabel(self, count):
        return 'x{}'.format(count)


class OperationCustomizationsBonusFormatter(CustomizationsBonusFormatter):

    def _format(self, bonus):
        customizations = {}
        for item in bonus.getCustomizations():
            cType = item.get('custType')
            if cType in customizations:
                item, count = customizations[cType]
                customizations[cType] = (item, count + 1)
            customizations[cType] = (item, 1)

        branch = bonus.getContext().get('branch')
        if branch == PM_BRANCH.REGULAR:
            tooltip = makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_BODY)
        elif branch == PM_BRANCH.PERSONAL_MISSION_2:
            tooltip = makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_ALLIANCE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_ALLIANCE_BODY)
        else:
            tooltip = None
        result = []
        for item, count in customizations.itervalues():
            c11nItem = bonus.getC11nItem(item)
            result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(c11nItem), userName=self._getUserName(c11nItem), label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus), isSpecial=False, tooltip=tooltip))

        return result


class GoodiesBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for booster, count in bonus.getBoosters().iteritems():
            if booster is not None:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(booster), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(booster), specialAlias=TOOLTIPS_CONSTANTS.SHOP_BOOSTER, specialArgs=[booster.boosterID], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        for demountKit, count in bonus.getDemountKits().iteritems():
            if demountKit is not None:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getDemountKitImages(demountKit), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=demountKit.userName, specialAlias=TOOLTIPS_CONSTANTS.AWARD_DEMOUNT_KIT, specialArgs=[demountKit.intCD], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getImages(cls, booster):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, booster.boosterGuiType)

        return result

    @classmethod
    def _getDemountKitImages(cls, demountKit):
        return {AWARDS_SIZES.SMALL: demountKit.getIcon(ICONS_SIZES.X48),
         AWARDS_SIZES.BIG: demountKit.getIcon(ICONS_SIZES.X80)}

    @classmethod
    def _getUserName(cls, booster):
        return booster.fullUserName


class GoodiesEpicBonusFormatter(GoodiesBonusFormatter):

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.textEpic

    @classmethod
    def _getIcon(cls, guiTypeName):
        size = EPIC_AWARD_SIZE
        return {size: RES_ICONS.getBonusIcon(size, guiTypeName)}

    @classmethod
    def _getImages(cls, booster):
        return cls._getIcon(booster.boosterGuiType)

    @classmethod
    def _getDemountKitImages(cls, demountKit):
        return cls._getIcon(demountKit.demountKitGuiType)


class ItemsBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for item, count in sorted(bonus.getItems().items(), key=lambda i: i[0]):
            if item is not None and count:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), isSpecial=True, label=self._formatBonusLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(item), specialAlias=self.getTooltip(item), specialArgs=[item.intCD], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus), highlightType=self._getHighlightType(item), overlayType=self._getOverlayType(item), highlightIcon=self._getHighlightIcon(item), overlayIcon=self._getOverlayIcon(item)))

        return result

    def _formatBonusLabel(self, count):
        return formatCountLabel(count)

    @classmethod
    def _getUserName(cls, item):
        return item.userName

    @classmethod
    def _getImages(cls, item):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, item.getGUIEmblemID())

        return result

    @classmethod
    def getTooltip(cls, item):
        if item.itemTypeID == GUI_ITEM_TYPE.EQUIPMENT and 'avatar' in item.tags:
            return TOOLTIPS_CONSTANTS.BATTLE_CONSUMABLE
        if item.itemTypeID == GUI_ITEM_TYPE.SHELL:
            return TOOLTIPS_CONSTANTS.AWARD_SHELL
        return TOOLTIPS_CONSTANTS.AWARD_BATTLE_BOOSTER if item.itemTypeID == GUI_ITEM_TYPE.BATTLE_BOOSTER else TOOLTIPS_CONSTANTS.AWARD_MODULE

    @classmethod
    def _getHighlightType(cls, item):
        return {AWARDS_SIZES.BIG: item.getBigHighlightType(),
         AWARDS_SIZES.SMALL: item.getHighlightType()}

    @classmethod
    def _getOverlayType(cls, item):
        return {AWARDS_SIZES.BIG: item.getBigOverlayType(),
         AWARDS_SIZES.SMALL: item.getOverlayType()}

    @classmethod
    def _getHighlightIcon(cls, item):
        result = {}
        for size in AWARDS_SIZES.ALL():
            if item.itemTypeName == SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_NAME:
                result[size] = RES_ICONS.getBonusHighlight(size, SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER)
            result[size] = SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT

        return result

    @classmethod
    def _getOverlayIcon(cls, item):
        result = {}
        itemTypeName = item.itemTypeName
        for size in AWARDS_SIZES.ALL():
            if itemTypeName == SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_NAME:
                if item.isCrewBooster():
                    result[size] = RES_ICONS.getBonusOverlay(size, SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_CREW_REPLACE)
                else:
                    result[size] = RES_ICONS.getBonusOverlay(size, SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER)
            if item.getOverlayType():
                result[size] = RES_ICONS.getBonusOverlay(size, item.getOverlayType())

        return result


class ItemsEpicBonusFormatter(ItemsBonusFormatter):

    @classmethod
    def _getImages(cls, item):
        size = EPIC_AWARD_SIZE
        return {size: RES_ICONS.getBonusIcon(size, item.getGUIEmblemID())}


class LinkedSetItemsBonusFormatter(ItemsBonusFormatter):

    def _formatBonusLabel(self, count):
        return 'x{}'.format(count)


class EpicItemsBonusFormatter(ItemsBonusFormatter):

    @classmethod
    def _getImages(cls, item):
        result = {}
        for size in AWARDS_SIZES.ALL():
            if item.itemTypeID == GUI_ITEM_TYPE.BATTLE_BOOSTER and item.isCrewBooster():
                result[size] = RES_ICONS.getBonusIcon(size, item.name)
            result[size] = RES_ICONS.getBonusIcon(size, item.getGUIEmblemID())

        result['tooltip'] = item.getBonusIcon(AWARDS_SIZES.BIG)
        return result

    @classmethod
    def _getOverlayType(cls, item):
        result = super(EpicItemsBonusFormatter, cls)._getOverlayType(item)
        if item.itemTypeName == SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_NAME:
            if not item.isCrewBooster():
                result[AWARDS_SIZES.BIG] = SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_BIG
                result[AWARDS_SIZES.SMALL] = SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER
            else:
                result[AWARDS_SIZES.BIG] = result[AWARDS_SIZES.SMALL] = SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT
        return result

    @classmethod
    def _getOverlayIcon(cls, item):
        result = super(EpicItemsBonusFormatter, cls)._getOverlayIcon(item)
        itemTypeName = item.itemTypeName
        for size in AWARDS_SIZES.ALL():
            if itemTypeName == SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_NAME:
                if not item.isCrewBooster():
                    result[size] = RES_ICONS.getBonusOverlay(size, SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER)
                else:
                    result[size] = SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT

        return result


class RankedItemsBonusFormatter(ItemsBonusFormatter):

    @classmethod
    def _getHighlightType(cls, item):
        return {} if item.itemTypeID == GUI_ITEM_TYPE.OPTIONALDEVICE and item.isDeluxe else super(RankedItemsBonusFormatter, cls)._getHighlightType(item)


class EpicDossierBonusFormatter(DossierBonusFormatter):

    @classmethod
    def _getImages(cls, bonus):
        if isinstance(bonus, Badge):
            return {AWARDS_SIZES.SMALL: bonus.getSmallIcon(),
             AWARDS_SIZES.BIG: bonus.getBigIcon()}
        bonus, record = bonus.getRecordName()
        return {AWARDS_SIZES.SMALL: RES_ICONS.getEpicAchievementIcon(ICONS_SIZES.X48, record),
         AWARDS_SIZES.BIG: RES_ICONS.getEpicAchievementIcon(ICONS_SIZES.X80, record)}


class BlueprintBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonuses):
        isPackedBonuses = bonuses.canPacked()
        bonus = [PreformattedBonus(bonusName=bonuses.getBlueprintName(), label=formatCountLabel(bonuses.getCount()) if isPackedBonuses else bonuses.formatBlueprintValue(), userName=bonuses.getBlueprintTooltipName(), labelFormatter=self._getLabelFormatter(bonuses), images=self._getIcons(bonuses), tooltip=bonuses.getTooltip(), align=LABEL_ALIGN.CENTER, isCompensation=self._isCompensation(bonuses), specialArgs=[bonuses.getBlueprintSpecialArgs()], isSpecial=True, specialAlias=bonuses.getBlueprintSpecialAlias())]
        return bonus * bonuses.getCount() if not isPackedBonuses else bonus

    def _getIcons(self, bonus):
        res = {}
        for size in AWARDS_SIZES.ALL():
            res[size] = bonus.getImage(size if size != 'small' else 'medium')

        return res


class BlueprintGroupBonusFormatter(BlueprintBonusFormatter):

    def _format(self, bonuses):
        return [PreformattedBonus(bonusName=bonuses.getBlueprintName(), label=formatCountLabel(bonuses.getCount()), userName=bonuses.getBlueprintTooltipName(), labelFormatter=self._getLabelFormatter(bonuses), images=self._getIcons(bonuses), tooltip=bonuses.getTooltip(), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonuses), specialArgs=[bonuses.getBlueprintSpecialArgs()], isSpecial=True, specialAlias=bonuses.getBlueprintSpecialAlias(), postProcessTags='blueprints')]


class BlueprintGroupEpicBonusFormatter(BlueprintGroupBonusFormatter):

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.textEpic

    def _getIcons(self, bonuses):
        size = EPIC_AWARD_SIZE
        return {size: RES_ICONS.getBonusIcon(size, bonuses.getImageCategory())}


class CrewSkinsBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        compensationFormatter = SimpleBonusFormatter()
        for item, count, customCompensation, compensatedNumber in bonus.getItems():
            compensations = bonus.compensation(compensatedNumber, customCompensation, bonus)
            if compensations:
                for bonusComp in compensations:
                    formattedComp = compensationFormatter.format(bonusComp)
                    result.extend(formattedComp)

            if item is not None and count:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(item), align=self._getLabelAlign(count), isCompensation=self._isCompensation(bonus), specialAlias=TOOLTIPS_CONSTANTS.CREW_SKIN, specialArgs=[item.getID(), count], postProcessTags='crewSkin'))

        return result

    @classmethod
    def _getLabelAlign(cls, count):
        return LABEL_ALIGN.RIGHT if count > 1 else LABEL_ALIGN.CENTER

    @classmethod
    def _getUserName(cls, item):
        return localizedFullName(item)

    @classmethod
    def _getImages(cls, item):
        result = {}
        rarity = item.getRarity()
        for size in AWARDS_SIZES.ALL():
            sizePath = R.images.gui.maps.icons.quests.bonuses.dyn(size, None)
            if sizePath is not None:
                img = sizePath.dyn(item.itemTypeName + str(rarity))
                if img is not None and img.exists():
                    result[size] = backport.image(img())

        return result


class CrewBooksBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for item, count in bonus.getItems():
            if item is not None and count:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(item), align=self._getLabelAlign(count), isCompensation=self._isCompensation(bonus), specialAlias=TOOLTIPS_CONSTANTS.CREW_BOOK, specialArgs=[item.intCD, count]))

        return result

    @classmethod
    def _getLabelAlign(cls, count):
        return LABEL_ALIGN.RIGHT if count > 1 else LABEL_ALIGN.CENTER

    @classmethod
    def _getUserName(cls, item):
        return item.userName

    @classmethod
    def _getImages(cls, item):
        result = {}
        for size in AWARDS_SIZES.ALL():
            sizePath = R.images.gui.maps.icons.crewBooks.books.dyn(size, None)
            if sizePath is not None:
                img = sizePath.dyn(item.getBonusIconName())
                if img is not None and img.exists():
                    result[size] = backport.image(img())

        return result


class CrewBooksEpicBonusFormatter(CrewBooksBonusFormatter):

    @classmethod
    def _getImages(cls, item):
        result = {}
        size = EPIC_AWARD_SIZE
        sizePath = R.images.gui.maps.icons.quests.bonuses.dyn(size, None)
        if sizePath is not None:
            img = sizePath.dyn(item.getBonusIconName())
            if img is not None and img.exists():
                result[size] = backport.image(img())
        return result


class CrewSkinsCompensationFormatter(CrewSkinsBonusFormatter):

    def _format(self, bonus):
        result = []
        for item, count, _, compensatedNumber in bonus.getItems():
            if item is not None and compensatedNumber > 0:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), isSpecial=True, label=self._formatBonusLabel(item, count, compensatedNumber), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(item), align=self._getLabelAlign(compensatedNumber), isCompensation=self._isCompensation(bonus), specialAlias=TOOLTIPS_CONSTANTS.CREW_SKIN, specialArgs=[item.getID(), compensatedNumber]))

        return result

    def _formatBonusLabel(self, item, _, compensatedNumber):
        defaultStr = text_styles.stats(backport.text(R.strings.item_types.crewSkins.itemType.dyn(Rarity.STRINGS[item.getRarity()])()))
        formattedStr = formatCountLabel(count=compensatedNumber, defaultStr=defaultStr)
        return formattedStr


class EntitlementFormatter(SimpleBonusFormatter):

    @classmethod
    def _getImages(cls, bonus):
        images = {}
        for size in AWARDS_SIZES.ALL():
            images[size] = bonus.getIconBySize(size)

        return images

    def _format(self, bonus):
        result = []
        if bonus.isShowInGUI():
            result.append(self.__formatEntitlement(bonus))
        return result

    def __formatEntitlement(self, bonus):
        value = bonus.getValue()
        isFormattedAmount = bonus.isFormattedAmount(value.id)
        return PreformattedBonus(bonusName=bonus.getName(), userName=bonus.getUserName(value.id), label=formatCountLabel(value.amount) if isFormattedAmount else backport.getIntegralFormat(value.amount), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), align=LABEL_ALIGN.RIGHT if isFormattedAmount else LABEL_ALIGN.CENTER, isCompensation=self._isCompensation(bonus))
