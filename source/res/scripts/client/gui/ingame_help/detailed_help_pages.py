# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/ingame_help/detailed_help_pages.py
import logging
import CommandMapping
from gui.impl import backport
from gui.impl.gen import R
from gui.shared.utils.functions import replaceHyphenToUnderscore
from gui.shared.utils.key_mapping import getReadableKey
from soft_exception import SoftException
_logger = logging.getLogger(__name__)

def buildPagesData(ctx):
    datailedList = []
    if ctx.get('isWheeled') and ctx.get('hasSiegeMode'):
        datailedList.extend(buildSiegeModePages())
    if ctx.get('hasBurnout'):
        datailedList.extend(buildBurnoutPages())
    if ctx.get('isWheeled'):
        datailedList.extend(buildWheeledPages())
    if ctx.get('isDualGun'):
        datailedList.extend(buildDualGunPages())
    if ctx.get('battleRoyale') and ctx.get('mapGeometryName'):
        datailedList.extend(_buildBattleRoyalePages(ctx['mapGeometryName']))
    return datailedList


def buildTitle(ctx):
    title = backport.text(R.strings.ingame_help.detailsHelp.default.title())
    vehName = ctx.get('vehName')
    if vehName is not None:
        title = vehName
    return title


def buildSiegeModePages():
    pages = []
    siegeKeyName = getReadableKey(CommandMapping.CMD_CM_VEHICLE_SWITCH_AUTOROTATION)
    keyName = siegeKeyName if siegeKeyName else backport.text(R.strings.ingame_help.detailsHelp.noKey())
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.twoModes.title()), backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.twoModes(), key1=keyName), [siegeKeyName], backport.image(R.images.gui.maps.icons.battleHelp.wheeledHelp.wheel_two_mode()))
    return pages


def buildBurnoutPages():
    pages = []
    breakeKeyName = getReadableKey(CommandMapping.CMD_BLOCK_TRACKS)
    forwardKeyName = getReadableKey(CommandMapping.CMD_MOVE_FORWARD)
    keyName1 = breakeKeyName if breakeKeyName else backport.text(R.strings.ingame_help.detailsHelp.noKey())
    keyName2 = forwardKeyName if forwardKeyName else backport.text(R.strings.ingame_help.detailsHelp.noKey())
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.burnout.title()), backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.burnout(), key1=keyName1, key2=keyName2), [forwardKeyName, breakeKeyName], backport.image(R.images.gui.maps.icons.battleHelp.wheeledHelp.wheel_burnout()))
    return pages


def buildWheeledPages():
    pages = []
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.stableChassis.title()), backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.stableChassis()), [], backport.image(R.images.gui.maps.icons.battleHelp.wheeledHelp.wheel_chassis()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.aboutTechnique.title()), backport.text(R.strings.ingame_help.detailsHelp.wheeledVeh.aboutTechnique()), [], backport.image(R.images.gui.maps.icons.battleHelp.wheeledHelp.wheel_details()))
    return pages


def buildDualGunPages():
    pages = []
    shootKey = getReadableKey(CommandMapping.CMD_CM_SHOOT)
    chargeKey = getReadableKey(CommandMapping.CMD_CM_CHARGE_SHOT)
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.dualGun.volley_fire.title()), backport.text(R.strings.ingame_help.detailsHelp.dualGun.volley_fire()), [chargeKey], backport.image(R.images.gui.maps.icons.battleHelp.dualGunHelp.volley_fire()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.dualGun.quick_fire.title()), backport.text(R.strings.ingame_help.detailsHelp.dualGun.quick_fire()), [shootKey], backport.image(R.images.gui.maps.icons.battleHelp.dualGunHelp.quick_fire()))
    return pages


def _buildBattleRoyalePages(mapGeometryName):
    pages = []
    mapResourceName = 'c_' + replaceHyphenToUnderscore(mapGeometryName)
    imagePath = R.images.gui.maps.icons.battleHelp.battleRoyale.dyn(mapResourceName)
    if not imagePath.isValid():
        raise SoftException('No icons found for map {}'.format(mapGeometryName))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.radar.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.radar.description()), [], backport.image(imagePath.br_radar()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.zone.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.zone.description()), [], backport.image(imagePath.br_zone()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.sectorVision.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.sectorVision.description()), [], backport.image(imagePath.br_sector()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.airDrop.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.airDrop.description()), [], backport.image(imagePath.br_airdrop()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.upgrade.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.upgrade.description()), [], backport.image(imagePath.br_tree()))
    _addPage(pages, backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.uniqueAbilities.title()), backport.text(R.strings.ingame_help.detailsHelp.battleRoyale.uniqueAbilities.description()), [], backport.image(imagePath.br_unique_abilities()))
    return pages


def _addPage(datailedList, title, descr, buttons, image):
    data = {'title': title,
     'descr': descr,
     'buttons': buttons,
     'image': image}
    datailedList.append(data)
