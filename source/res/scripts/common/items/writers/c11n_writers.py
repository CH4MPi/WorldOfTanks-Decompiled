# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/items/writers/c11n_writers.py
from collections import namedtuple
from constants import IS_EDITOR
import Math
import ResMgr
import typing
import re
from string import lower, upper
import items.vehicles as iv
from items import _xml, parseIntCompactDescr
from soft_exception import SoftException
from items.components.c11n_constants import SeasonType, DecalType, CamouflageTilingType, CustomizationType, RENT_DEFAULT_BATTLES, EMPTY_ITEM_ID, ProjectionDecalType, CustomizationTypeNames, DEFAULT_SCALE_FACTOR_ID
from items.components.c11n_components import StyleItem, ApplyArea
from items.customizations import FieldTypes, FieldFlags, FieldType, SerializableComponent, SerializationException
from items.type_traits import equalComparator
from nations import NAMES
from items.utils import getDefaultGlossTexture
if IS_EDITOR:
    from reflection_framework.helpers.editor_shared_properties import isPropertyShared
else:
    isPropertyShared = lambda instance, path: False

def findOrCreate(section, subsectionName):
    if not section.has_key(subsectionName):
        return section.createSection(subsectionName)
    else:
        return section[subsectionName]


def resizeSection(section, newSize, newName):
    if len(section) == newSize:
        return False
    while len(section) > newSize:
        lastSection = section.child(len(section) - 1)
        section.deleteSection(lastSection)

    while len(section) < newSize:
        section.createSection(newName(len(section)))

    return True


def saveCustomizationItems(cache, folder):
    writeItemType(PaintXmlWriter(), cache, folder, 'paint')
    writeItemType(DecalXmlWriter(), cache, folder, 'decal')
    writeItemType(ProjectionDecalXmlWriter(), cache, folder, 'projection_decal')
    writeItemType(CamouflageXmlWriter(), cache, folder, 'camouflage')
    writeItemType(ModificationXmlWriter(), cache, folder, 'modification')
    writeItemType(StyleXmlWriter(), cache, folder, 'style')
    writeItemType(PersonalNumberXmlWriter(), cache, folder, 'personal_number')
    writeItemType(InsigniaXmlWriter(), cache, folder, 'insignia')
    writeItemType(SequenceXmlWriter(), cache, folder, 'sequence')
    writeItemType(AttachmentXmlWriter(), cache, folder, 'attachment')
    writeFontType(FontXmlWriter(), cache, folder, 'font')


class GroupSectionPicker(object):

    def __init__(self, group):
        self.ids = set(map(lambda itemRef: itemRef().id, group.editorData.itemRefs))
        self.name = group.name

    def __call__(self, gsections):
        bestSection = None
        bestMatch = 0
        for gsection in gsections:
            match = 0
            for iname, isection in gsection.items():
                if isection.has_key('id'):
                    id = isection['id'].asInt
                    if id in self.ids:
                        match += 1

            if match > bestMatch:
                bestMatch = match
                bestSection = gsection

        if bestSection is not None:
            return bestSection
        else:
            for gsection in gsections:
                if gsection.readString('name') == self.name:
                    return gsection

            return


def writeItemType(writer, cache, folder, itemName):
    refsections = {}
    changedRefs = set()
    fileListRewriters = {}
    groups = cache.editorData.groups[CUSTOMIZATION_ITEMS_NAME_TO_TYPE[itemName]]
    sourceFiles = cache.editorData.sourceFiles[CUSTOMIZATION_ITEMS_NAME_TO_TYPE[itemName]]
    for sourceXml in sourceFiles:
        rootSection = ResMgr.openSection(sourceXml)
        listRewriter = _xml.ListRewriter(rootSection, 'itemGroup')
        fileListRewriters[sourceXml] = listRewriter
        refsections[sourceXml] = rootSection

    for group in groups:
        if group.editorData.sourceXml is None:
            raise SoftException('Group {} has no sourceXml, data format has changed?'.format(group.name))
        sourceXml = group.editorData.sourceXml
        listRewriter = fileListRewriters.get(sourceXml, None)
        if listRewriter is None:
            raise SoftException('Group {} sourceXml not found in fileListRewriters'.format(group.name))
        groupSection = listRewriter.next(sectionPicker=GroupSectionPicker(group))
        changed = writeGroup(writer, group, groupSection, itemName)
        if changed:
            changedRefs.add(sourceXml)

    for ref in fileListRewriters:
        listRewriter = fileListRewriters[ref]
        changed = listRewriter.flush()
        if changed:
            changedRefs.add(ref)

    for ref, refsection in refsections.items():
        if ref in changedRefs:
            refsection.save()

    return


def writeGroup(itemWriter, group, groupSection, itemName):
    prototype = group.itemPrototype
    changed = itemWriter.write(prototype, groupSection)
    changed |= _xml.rewriteString(groupSection, 'name', group.name, defaultValue='')
    listRewriter = _xml.ListRewriter(groupSection, itemName)
    for itemRef in group.editorData.itemRefs:
        item = itemRef()
        if item.id == EMPTY_ITEM_ID:
            continue
        itemSection = listRewriter.next(lambda s, i=item: s['id'].asInt == i.id)
        changed |= itemWriter.write(item, itemSection)

    changed |= listRewriter.flush()
    return changed


def writeFontType(writer, cache, folder, itemName):

    def parseSourceSection(fontFilesPathes, fontItems, changedRefs):
        fontRefs = {}
        fontsSections = {}
        for fontFile in fontFilesPathes:
            refSection = ResMgr.openSection(fontFile)
            if refSection is None:
                _xml.raiseWrongXml(None, refSection, "can't find datasection")
            fontRefs[fontFile] = refSection
            for name, isection in refSection.items():
                if isection.has_key('id'):
                    id = isection['id'].asInt
                    if id in fontsSections.keys():
                        raise SoftException('Some font items have the same id {}.'.format(id))
                    if id in fontItems.keys():
                        fontsSections[id] = isection
                    else:
                        refSection.deleteSection(isection)
                        changedRefs.add(refSection)

            return (fontRefs, fontsSections)

        return

    sourceFiles = cache.editorData.sourceFiles[CUSTOMIZATION_ITEMS_NAME_TO_TYPE[itemName]]
    if len(sourceFiles) == 0:
        return
    else:
        if sourceFiles is None:
            raise SoftException('Item {} has no sourceXml, data format has changed?'.format(itemName + str(id)))
        items = cache.fonts
        changedRefs = set()
        refSections, fontsSections = parseSourceSection(sourceFiles, items, changedRefs)
        for id, item in items.items():
            sourceFile = item.editorData.sourceXml
            if sourceFile not in refSections.keys():
                raise SoftException("writeFontType: Couldn't find file {} ".format(sourceFile))
            sourceRef = refSections[sourceFile]
            if id not in fontsSections.keys():
                fontsSections[id] = sourceRef.createSection(itemName)
                _xml.rewriteInt(fontsSections[id], 'id', id)
            isection = fontsSections[id]
            changed = writer.write(item, isection)
            if changed:
                changedRefs.add(sourceRef)

        for refsection in changedRefs:
            refsection.save()

        return


def _natkey(s):

    def convert(t):
        try:
            return int(t)
        except ValueError:
            return t.lower()

    return map(convert, re.split('([0-9]+)', s))


def natsorted(seq):
    return sorted(seq, key=_natkey)


class VehicleFilterTagsConvertor(object):

    def convertToString(self, valuesList):
        result = ' '.join(natsorted(valuesList))
        return result


class VehicleFilterLevelConvertor(object):

    def convertToString(self, valuesList):
        result = ' '.join(map(str, sorted(valuesList)))
        return result


class VehicleFilterNationConvertor(object):

    def convertToString(self, valuesList):
        result = ' '.join(natsorted(map(lambda item: NAMES[item], valuesList)))
        return result


class VehicleFilterVehicleConvertor(object):

    def convertToString(self, valuesList):
        from items.vehicles import g_cache, g_list

        def getTankName(vehCompactDesc):
            itemTypeID, nationId, vehId = parseIntCompactDescr(vehCompactDesc)
            tank = g_cache.vehicle(nationId, vehId)
            return tank.name

        result = ' '.join(natsorted(map(lambda item: getTankName(item), valuesList)))
        return result


class StringFilterConvertor(object):

    def convertToString(self, valuesList):
        result = ' '.join(natsorted(valuesList))
        return result


class IntegerFilterConvertor(object):

    def convertToString(self, valuesList):
        result = ' '.join(map(str, sorted(valuesList)))
        return result


class BoolFilterConvertor(object):

    def convertToString(self, valuesList):
        return str(valuesList)


DECAL_TYPE_STRING = {DecalType.EMBLEM: 'EMBLEM',
 DecalType.INSCRIPTION: 'INSCRIPTION'}

class ItemsFilterDecalTypeConvertor(object):

    def convertToString(self, valuesList):

        def getDecalTypeMame(typeId):
            return DECAL_TYPE_STRING[typeId]

        result = ' '.join(natsorted(map(lambda item: getDecalTypeMame(item), valuesList)))
        return result


Description = namedtuple('FiltedFiels', ('section', 'attributeName', 'convertor'))
VEHICLE_FILTER_VALUE_DESCRIPTION = (Description('nations', 'nations', VehicleFilterNationConvertor()),
 Description('levels', 'levels', VehicleFilterLevelConvertor()),
 Description('tags', 'tags', VehicleFilterTagsConvertor()),
 Description('vehicles', 'vehicles', VehicleFilterVehicleConvertor()))
ITEMS_FILTER_VALUE_DESCRIPTION = (Description('tags', 'tags', StringFilterConvertor()),
 Description('id', 'ids', IntegerFilterConvertor()),
 Description('itemGroupName', 'itemGroupNames', StringFilterConvertor()),
 Description('type', 'types', ItemsFilterDecalTypeConvertor()),
 Description('historical', 'edCustomizationDisplayTypes', IntegerFilterConvertor()))
FILTER_ID_NAME = {CustomizationType.PROJECTION_DECAL: 'projection_decal',
 CustomizationType.PERSONAL_NUMBER: 'personal_number',
 CustomizationType.DECAL: 'decal'}
ALTERNATE_TO_NAME = {CustomizationType.DECAL: 'decal',
 CustomizationType.PROJECTION_DECAL: 'projection_decal',
 CustomizationType.PAINT: 'paint',
 CustomizationType.CAMOUFLAGE: 'camouflage',
 CustomizationType.MODIFICATION: 'modification',
 CustomizationType.PERSONAL_NUMBER: 'personal_number'}
CUSTOMIZATION_ITEMS_TYPE_TO_NAME = {CustomizationType.DECAL: 'decal',
 CustomizationType.PROJECTION_DECAL: 'projection_decal',
 CustomizationType.PAINT: 'paint',
 CustomizationType.CAMOUFLAGE: 'camouflage',
 CustomizationType.MODIFICATION: 'modification',
 CustomizationType.PERSONAL_NUMBER: 'personal_number',
 CustomizationType.STYLE: 'style',
 CustomizationType.INSIGNIA: 'insignia',
 CustomizationType.FONT: 'font',
 CustomizationType.ATTACHMENT: 'attachment',
 CustomizationType.SEQUENCE: 'sequence'}
CUSTOMIZATION_ITEMS_NAME_TO_TYPE = {v:k for k, v in CUSTOMIZATION_ITEMS_TYPE_TO_NAME.items()}

def saveItemFilter(filter, section, filterName, valueDescription):
    changed = False
    filterSection = findOrCreate(section, filterName)

    def countFilters(filterSection):
        includeCount = 0
        excludeCount = 0
        for iname, isection in filterSection.items():
            if iname == 'include':
                includeCount += 1
            if iname == 'exclude':
                excludeCount += 1

        return (includeCount, excludeCount)

    includeSectCnt, excludeSectCnt = countFilters(filterSection)
    if includeSectCnt != len(filter.include) or excludeSectCnt != len(filter.exclude):
        changed = True
        while len(filterSection) > 0:
            lastSection = filterSection.child(len(filterSection) - 1)
            filterSection.deleteSection(lastSection)

        def createSections(parentSection, sectionName, count):
            while count > 0:
                parentSection.createSection(sectionName)
                count -= 1

        createSections(filterSection, 'include', len(filter.include))
        createSections(filterSection, 'exclude', len(filter.exclude))

    def saveFilter(filterSection, filterName, filters, valueDescription):
        if len(filters) == 0:
            return False
        changed = False
        index = 0

        def saveFilterValue(subFilterSection, valueSectionName, valueHolder, atrributeListName, convertor):
            listOfValues = getattr(valueHolder, atrributeListName)
            if listOfValues is None:
                return False
            else:
                needWrite = True
                if isinstance(listOfValues, bool):
                    needWrite = listOfValues
                elif len(listOfValues) == 0:
                    needWrite = False
                if needWrite is False:
                    if subFilterSection.has_key(valueSectionName):
                        subFilterSection.deleteSection(valueSectionName)
                        return True
                else:
                    strValue = convertor.convertToString(listOfValues)
                    if strValue is None:
                        return False
                    return _xml.rewriteString(subFilterSection, valueSectionName, strValue)
                return False

        for iname, isection in filterSection.items():
            if iname == filterName:
                filterValue = filters[index]
                for valuedescr in valueDescription:
                    changed |= saveFilterValue(isection, valuedescr.section, filterValue, valuedescr.attributeName, valuedescr.convertor)

                index += 1

        return changed

    changed |= saveFilter(filterSection, 'include', filter.include, valueDescription)
    changed |= saveFilter(filterSection, 'exclude', filter.exclude, valueDescription)
    return changed


class BaseCustomizationItemXmlWriter(object):

    def write(self, item, section):
        changed = False
        changed |= rewriteInt(section, 'id', item, 'id')
        changed |= rewriteInt(section, 'historical', item, 'customizationDisplayType')
        changed |= rewriteString(section, 'priceGroup', item, 'priceGroup', '')
        changed |= rewriteString(section, 'requiredToken', item, 'requiredToken', '')
        changed |= rewriteString(section, 'texture', item, 'texture', '')
        changed |= rewriteInt(section, 'maxNumber', item, 'maxNumber', 0)
        changed |= rewriteTags(section, item)
        if _needWrite(item, 'season'):
            enumValue = encodeEnum(SeasonType, item.season)
            if enumValue is None:
                enumValue = encodeFlagEnum(SeasonType, item.season)
            changed |= _xml.rewriteString(section, 'season', enumValue, 'undefined')
        else:
            section.deleteSection('season')
        changed |= rewriteString(section, 'userString', item, 'i18n.userKey', '')
        changed |= rewriteString(section, 'description', item, 'i18n.descriptionKey', '')
        if not _needWrite(item, 'filter'):
            changed |= section.deleteSection('filter')
        else:
            changed |= saveItemFilter(item.filter, section, 'vehicleFilter', VEHICLE_FILTER_VALUE_DESCRIPTION)
        return changed


class PaintXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(PaintXmlWriter, self).write(item, section)
        changed |= rewriteFloat(section, 'gloss', item, 'gloss', 0.0)
        changed |= rewriteFloat(section, 'metallic', item, 'metallic', 0.0)
        color = item.color
        c_a, c_r, c_g, c_b = (0, 0, 0, 0)
        if color > 0:
            c_a = color >> 24 & 255
            c_r = color >> 16 & 255
            c_g = color >> 8 & 255
            c_b = color & 255
        color = Math.Vector4(c_b, c_g, c_r, c_a)
        if _needWrite(item, 'color'):
            changed |= _xml.rewriteVector4(section, 'color', color)
        else:
            changed |= section.deleteSection('color')
        return changed


class DecalXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(DecalXmlWriter, self).write(item, section)
        changed |= rewriteBool(section, 'mirror', item, 'canBeMirrored')
        if _needWrite(item, 'type'):
            changed |= _xml.rewriteString(section, 'type', encodeEnum(DecalType, item.type))
        else:
            changed |= section.deleteSection('type')
        return changed


class ProjectionDecalXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(ProjectionDecalXmlWriter, self).write(item, section)
        changed |= rewriteBool(section, 'mirror', item, 'canBeMirroredHorizontally')
        changed |= rewriteString(section, 'glossTexture', item, 'glossTexture', getDefaultGlossTexture())
        changed |= rewriteInt(section, 'scaleFactorId', item, 'scaleFactorId', DEFAULT_SCALE_FACTOR_ID)
        return changed


class CamouflageXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(CamouflageXmlWriter, self).write(item, section)
        changed |= rewriteFloat(section, 'invisibilityFactor', item, 'invisibilityFactor', 1.0)
        changed |= rewritePalettes(section, item)
        changed |= rewriteCamouflageRotation(section, item)
        changed |= rewriteCamouflageScales(section, item)
        changed |= rewriteCamouflageTiling(section, item)
        changed |= rewriteCamouflageTilingSettings(section, item)
        changed |= rewriteCamouflageGlossMetallicSettings(section, item)
        return changed


def rewriteEffects(item, section):
    if not _needWrite(item, 'effects'):
        return section.deleteSection('effects')
    else:
        changed = False
        effectsSection = findOrCreate(section, 'effects')
        changed |= resizeSection(effectsSection, 2, lambda id: 'effect')
        index = 0

        def writeEffectValue(effectSection, type, value):
            result = _xml.rewriteString(effectSection, 'type', type)
            result |= _xml.rewriteFloat(effectSection, 'value', value)
            return result

        while index < 2:
            effectSection = effectsSection.child(index)
            typeSection = findOrCreate(effectSection, 'type')
            effectType = typeSection.asString
            if effectType is None or effectType == '':
                if index == 0:
                    effectType = 'paint_age'
                if index == 1:
                    effectType = 'paint_fading'
            effectValue = 0
            if effectType == 'paint_age':
                effectValue = item.strength
            elif effectType == 'paint_fading':
                effectValue = item.fading
            changed |= writeEffectValue(effectSection, effectType, effectValue)
            index += 1

        return changed


class ModificationXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(ModificationXmlWriter, self).write(item, section)
        changed |= rewriteEffects(item, section)
        return changed


class ComponentXmlSerializer(object):

    def __init__(self):
        super(ComponentXmlSerializer, self).__init__()

    def encode(self, section, target):
        return self.__encodeCustomType(section, None, target)

    def __encodeCustomType(self, section, key, obj):
        changed = False
        if key is None:
            objSection = section
        else:
            objSection = section[key]
            if objSection is None:
                objSection = section.createSection(key)
                changed = True
        for fieldName, fieldType in obj.fields.iteritems():
            if fieldType.flags & FieldFlags.DEPRECATED:
                continue
            if fieldType.flags & FieldFlags.NON_XML:
                continue
            value = getattr(obj, fieldName)
            if value is not None:
                changed |= self.__encodeValue(objSection, fieldName, value, fieldType)
            changed |= objSection.deleteSection(fieldName)

        return changed

    def __encodeArray(self, section, key, value, fieldType):
        changed = False
        if key is None:
            array = section
        else:
            array = section[key]
            if array is None:
                array = section.createSection(key)
                changed = True
        for name, child in array.items():
            if name != 'item':
                array.deleteSection(child)
                changed = True

        with _xml.ListRewriter(array, 'item') as children:
            for item in value:
                preferred = None
                try:
                    if 'id' in item:
                        preferred = lambda s: s.readInt('id') == item.id
                except TypeError:
                    pass

                child = children.next(preferred)
                changed |= self.__encodeValue(child, None, item, fieldType)

        return changed

    def __encodeValue(self, section, key, value, fieldType):
        if fieldType.type == FieldTypes.VARINT:
            return _xml.rewriteInt(section, key, value)
        if fieldType.type == FieldTypes.FLOAT:
            return _xml.rewriteFloat(section, key, value)
        if fieldType.type == FieldTypes.APPLY_AREA_ENUM:
            if fieldType.flags & FieldFlags.SAVE_AS_STRING:
                return _xml.rewriteString(section, key, encodeFlagEnum(ApplyArea, value).upper())
            return _xml.rewriteInt(section, key, value)
        if fieldType.type == FieldTypes.TAGS:
            return _xml.rewriteString(section, key, ' '.join(value))
        if fieldType.type == FieldTypes.STRING:
            return _xml.rewriteString(section, key, value)
        if fieldType.type == FieldTypes.OPTIONS_ENUM:
            return _xml.rewriteInt(section, key, value)
        if fieldType.type & FieldTypes.TYPED_ARRAY:
            ft = fieldType._asdict()
            ft['type'] ^= FieldTypes.TYPED_ARRAY
            return self.__encodeArray(section, key, value, FieldType(**ft))
        if fieldType.type >= FieldTypes.CUSTOM_TYPE_OFFSET:
            return self.__encodeCustomType(section, key, value)
        raise SerializationException('Unsupported field type %d' % (fieldType.type,))


class StyleXmlWriter(BaseCustomizationItemXmlWriter):
    __outfitSerializer = ComponentXmlSerializer()

    def write(self, item, section):
        changed = super(StyleXmlWriter, self).write(item, section)
        changed |= rewriteBool(section, 'isRent', item, 'isRent')
        if item.isRent:
            changed |= rewriteInt(section, 'rentCount', item, 'rentCount', RENT_DEFAULT_BATTLES)
        else:
            changed |= section.deleteSection('rentCount')
        changed |= rewriteString(section, 'modelsSet', item, 'modelsSet', 'default')
        changed |= self.__writeOutfits(item.outfits, section)
        changed |= self.__writeFiltersItems(item.itemsFilters, section)
        changed |= self.__writeAlternateItems(item.alternateItems, section)
        changed |= self.__writeDependencies(item.dependencies, section)
        changed |= self.__write3dProgression(item.styleProgressions, section)
        return changed

    def __writeOutfits(self, outfits, section):
        singleOutfit = None
        seasonsMask = 0
        for season, outfit in outfits.iteritems():
            seasonsMask |= season
            if singleOutfit is None:
                singleOutfit = outfit
                continue
            if outfit != singleOutfit:
                singleOutfit = None
                break

        if seasonsMask != SeasonType.ALL:
            singleOutfit = None
        changed = False
        with _xml.ListRewriter(section, 'outfits/outfit') as oSections:
            if singleOutfit is None:
                for season, outfit in outfits.iteritems():
                    changed |= self.__writeOutfit(oSections, season, outfit)

            else:
                changed |= self.__writeOutfit(oSections, seasonsMask, singleOutfit)
            changed |= oSections.changed
        return changed

    def __writeOutfit(self, oSections, season, outfit):
        changed = False
        seasonName = encodeEnum(SeasonType, season)
        oSection = oSections.next(lambda s: s.readString('season').lower() == seasonName)
        changed |= _xml.rewriteString(oSection, 'season', seasonName)
        for projectionDecal in outfit.projection_decals:
            if projectionDecal.editorData.decalType == ProjectionDecalType.POSITION:
                projectionDecal.tags = None
                projectionDecal.scaleFactorId = None
                projectionDecal.options = None
            projectionDecal.position = None
            projectionDecal.rotation = None
            projectionDecal.scale = None
            projectionDecal.doubleSided = None
            projectionDecal.showOn = None

        changed |= self.__outfitSerializer.encode(oSection, outfit)
        return changed

    def __writeAlternateItems(self, alterItems, isection):
        changed = False
        if len(alterItems) == 0:
            if isection.has_key('alternateItems'):
                isection.deleteSection('alternateItems')
                changed |= True
        else:
            alternateItemsSection = isection['alternateItems']
            if alternateItemsSection is None:
                alternateItemsSection = isection.createSection('alternateItems')
                changed |= True
            childCount = len(alternateItemsSection)
            childIndex = childCount - 1
            currentItemsNames = ' '.join(natsorted(map(lambda item: ALTERNATE_TO_NAME[item], alterItems.keys())))
            while childIndex >= 0:
                childSection = alternateItemsSection.child(childIndex)
                sectionName = childSection.name
                if sectionName not in currentItemsNames:
                    alternateItemsSection.deleteSection(sectionName)
                    changed |= True
                childIndex -= 1

        for itemType, itemValues in alterItems.iteritems():
            alternateItemSectionName = ALTERNATE_TO_NAME[itemType]
            oSection = alternateItemsSection[alternateItemSectionName]
            if oSection is None:
                oSection = alternateItemsSection.createSection(alternateItemSectionName)
                changed |= True
            itemsValue = ' '.join(map(str, sorted(itemValues)))
            changed |= _xml.rewriteString(oSection, 'id', itemsValue)

        return changed

    def __writeDependencies(self, dependencies, isection):
        changed = False
        collection = dependencies
        camouflagesCount = len(collection)
        if camouflagesCount == 0:
            if isection.has_key('dependencies'):
                isection.deleteSection('dependencies')
                changed |= True
        else:
            dependenciesSection = findOrCreate(isection, 'dependencies')
            changed |= resizeSection(dependenciesSection, camouflagesCount, lambda id: 'camouflage')
            sectionIndex = 0
            for camoId, items in collection.iteritems():
                camoSection = dependenciesSection.child(sectionIndex)
                changed |= _xml.rewriteInt(camoSection, 'id', camoId)
                for childKey, idsList in items.iteritems():
                    childName = '{}'.format(lower(CustomizationTypeNames[childKey]))
                    idsStr = ' '.join(map(str, idsList))
                    changed |= _xml.rewriteString(camoSection, childName, idsStr)

                sectionIndex += 1

        return changed

    def __writeFiltersItems(self, filters, isection):
        changed = False
        if len(filters) == 0:
            if isection.has_key('itemFilters'):
                isection.deleteSection('itemFilters')
                changed |= True
        else:
            itemFiltersSection = isection['itemFilters']
            if itemFiltersSection is None:
                itemFiltersSection = isection.createSection('itemFilters')
                changed |= True
            for filterId, filterValue in filters.iteritems():
                filterName = FILTER_ID_NAME[filterId]
                changed |= saveItemFilter(filterValue, itemFiltersSection, filterName, ITEMS_FILTER_VALUE_DESCRIPTION)

        return changed

    def __write3dProgression(self, progression, isection):
        sectionName = 'styleProgressions'
        if progression is None or len(progression) == 0:
            if isection.has_key(sectionName):
                isection.deleteSection(sectionName)
                return True
            return False
        else:
            changed = False
            stagesCount = len(progression)
            if stagesCount == 0:
                if isection.has_key(sectionName):
                    isection.deleteSection(sectionName)
                    changed |= True
            else:
                progression3dSection = isection[sectionName]
                if progression3dSection is None:
                    progression3dSection = isection.createSection(sectionName)
                    changed |= True
                if stagesCount != len(progression3dSection):
                    changed |= resizeSection(progression3dSection, stagesCount, lambda id: 'stage')
                stageIndex = 0
                for stageName, progressionValue in progression.iteritems():
                    stageSection = progression3dSection.child(stageIndex)
                    if 'materials' in progressionValue.keys():
                        materialsList = progressionValue['materials']
                        materialsStr = ' '.join(materialsList)
                        changed |= _xml.rewriteString(stageSection, 'materials', materialsStr)
                    if 'additionalOutfit' in progressionValue.keys():
                        outfit = progressionValue['additionalOutfit']
                        changed |= self.__writeOutfits(outfit, stageSection)
                    stageIndex += 1

            return changed


class PersonalNumberXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(PersonalNumberXmlWriter, self).write(item, section)
        changed |= rewriteInt(section, 'digitsCount', item, 'digitsCount')
        changed |= rewriteString(section, 'preview_texture', item, 'previewTexture')
        return changed


class InsigniaXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(InsigniaXmlWriter, self).write(item, section)
        changed |= rewriteString(section, 'atlas', item, 'atlas', '')
        changed |= rewriteString(section, 'alphabet', item, 'alphabet', '')
        changed |= rewriteBool(section, 'canBeMirrored', item, 'canBeMirrored', False)
        return changed


class AttachmentXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(AttachmentXmlWriter, self).write(item, section)
        changed |= rewriteString(section, 'name', item, 'name', '')
        changed |= rewriteInt(section, 'sequenceId', item, 'sequenceId', -1)
        changed |= rewriteString(section, 'modelName', item, 'modelName', '')
        changed |= rewriteString(section, 'attachmentLogic', item, 'attachmentLogic', '')
        changed |= rewriteBool(section, 'initialVisibility', item, 'initialVisibility', False)
        return changed


class SequenceXmlWriter(BaseCustomizationItemXmlWriter):

    def write(self, item, section):
        changed = super(SequenceXmlWriter, self).write(item, section)
        changed |= rewriteString(section, 'name', item, 'name', '')
        changed |= rewriteString(section, 'sequenceName', item, 'sequenceName', '')
        return changed


def writeFontAlphabet(item):
    xmlPath = item.editorData.alphabet
    if xmlPath is None or len(xmlPath) == 0:
        return
    else:
        section = ResMgr.openSection(xmlPath)
        if section is None:
            return
        changed = False
        if len(section.items()) != len(item.editorData.alphabetList):
            changed |= resizeSection(section, len(item.editorData.alphabetList), lambda id: 'glyph')
        itemIndex = 0
        for name, isection in section.items():
            glyphItem = item.editorData.alphabetList[itemIndex]
            changed |= _xml.rewriteString(isection, 'name', glyphItem.name)
            vBegin = Math.Vector2(glyphItem.position[0], glyphItem.position[1])
            changed |= _xml.rewriteVector2(isection, 'begin', vBegin)
            vEnd = Math.Vector2(glyphItem.position[2], glyphItem.position[3])
            changed |= _xml.rewriteVector2(isection, 'end', vEnd)
            itemIndex += 1

        if changed:
            section.save()
        return


class FontXmlWriter(object):

    def write(self, item, section):
        changed = _xml.rewriteString(section, 'texture', item.texture)
        changed |= _xml.rewriteString(section, 'alphabet', item.alphabet)
        changed |= _xml.rewriteString(section, 'name', 'font_' + str(item.id))
        writeFontAlphabet(item)
        return changed


def _needWrite(item, propertyPath):
    return item.edIsPrototype or not isPropertyShared(item, propertyPath.split('.'))


def _rewriteFn(tp):
    eq = equalComparator(tp)
    readTp = 'read' + tp
    writeTp = 'write' + tp

    def read(section, name, defaultValue=None):
        r = getattr(section, readTp)
        return r(name) if defaultValue is None else r(name, defaultValue)

    def rewrite(section, subsectionName, item, propertyPath, defaultValue=None):
        if not _needWrite(item, propertyPath):
            return section.deleteSection(subsectionName)
        else:
            path = propertyPath.split('.')
            value = item
            for propertyName in path:
                value = getattr(value, propertyName)

            if value is None:
                return False
            if eq(read(section, subsectionName, defaultValue), value):
                return False
            w = getattr(section, writeTp)
            w(subsectionName, value)
            return True

    return rewrite


rewriteInt = _rewriteFn('Int')
rewriteBool = _rewriteFn('Bool')
rewriteString = _rewriteFn('String')
rewriteFloat = _rewriteFn('Float')
rewriteVector2 = _rewriteFn('Vector2')
rewriteVector3 = _rewriteFn('Vector3')
rewriteVector4 = _rewriteFn('Vector4')

def rewriteTags(section, item):
    if not _needWrite(item, 'tags'):
        return section.deleteSection('tags')
    tags = item.tags
    rewrite = len(tags) > 0
    if section.has_key('tags'):
        if not rewrite:
            section.deleteSection('tags')
            return True
        oldTags = iv._readTags(None, section, 'tags', 'customizationItem')
        rewrite = oldTags != tags
    if rewrite:
        tagsStr = ' '.join(tags)
        return _xml.rewriteString(section, 'tags', tagsStr)
    else:
        return False


def rewritePalettes(section, item):
    if not _needWrite(item, 'palettes'):
        return section.deleteSection('palettes')
    changed = False
    palettes = item.palettes
    if not palettes or len(palettes) == 0:
        return section.deleteSection('palettes')
    palettesSection = findOrCreate(section, 'palettes')
    changed |= resizeSection(palettesSection, len(palettes), lambda id: 'palette')
    for index, palette in enumerate(palettes):

        def sectName(id):
            return 'c' + str(id)

        paletteSection = palettesSection.child(index)
        changed |= resizeSection(paletteSection, len(palette), sectName)
        for i, iPalette in enumerate(palette):
            r = iPalette & 255
            g = iPalette >> 8 & 255
            b = iPalette >> 16 & 255
            a = iPalette >> 24 & 255
            colorStr = ' '.join([str(r),
             str(g),
             str(b),
             str(a)])
            changed |= _xml.rewriteString(paletteSection, sectName(i), colorStr)

    return changed


def rewriteCamouflageRotation(section, camouflageItem):
    if not _needWrite(camouflageItem, 'rotation'):
        return section.deleteSection('rotation')
    changed = False
    hullRotation = camouflageItem.rotation['hull']
    gunRotation = camouflageItem.rotation['gun']
    turretRotation = camouflageItem.rotation['turret']

    def rewritePartRotation(section, partName, value):
        return _xml.rewriteFloat(section, partName, value)

    rotationSection = findOrCreate(section, 'rotation')
    changed |= rewritePartRotation(rotationSection, 'HULL', hullRotation)
    changed |= rewritePartRotation(rotationSection, 'TURRET', turretRotation)
    changed |= rewritePartRotation(rotationSection, 'GUN', gunRotation)
    return changed


def rewriteCamouflageScales(section, camouflageItem):
    if not _needWrite(camouflageItem, 'scales'):
        return section.deleteSection('scales')
    scalesResult = Math.Vector3(camouflageItem.scales[0], camouflageItem.scales[1], camouflageItem.scales[2])
    return _xml.rewriteVector3(section, 'scales', scalesResult)


def correctTankNameByCurrentSectionName(section, tankName):
    if section.has_key(tankName):
        return tankName
    index = tankName.find(':')
    if index > 0:
        tmpTankName = tankName[index + 1:len(tankName)]
        if section.has_key(tmpTankName):
            return tmpTankName
    return tankName


def rewriteCamouflageTiling(section, camouflageItem):
    if not _needWrite(camouflageItem, 'tiling') or not camouflageItem.tiling:
        return section.deleteSection('tiling')
    else:
        changed = False
        tilingSection = findOrCreate(section, 'tiling')
        for key, value in camouflageItem.tiling.items():
            if value is None:
                continue
            tankName = camouflageItem.editorData.tilingName[key]
            correctedTankName = correctTankNameByCurrentSectionName(tilingSection, tankName)
            tilingRes = Math.Vector4(value[0], value[1], value[2], value[3])
            changed |= _xml.rewriteVector4(tilingSection, correctedTankName, tilingRes)

        for iname, isection in tilingSection.items():
            if iname not in camouflageItem.editorData.tilingName.values():
                tilingSection.deleteSection(iname)
                changed = True

        return changed


def rewriteCamouflageTilingSettings(section, camouflageItem):
    if not _needWrite(camouflageItem, 'tilingSettings') or camouflageItem.tilingSettings is None:
        return section.deleteSection('tilingSettings')
    else:
        changed = False
        tilingSettings = camouflageItem.tilingSettings
        tilingType = tilingSettings[0]
        if section.has_key('tilingSettings'):
            tilingSettingsSection = section['tilingSettings']
        elif tilingType != CamouflageTilingType.LEGACY:
            tilingSettingsSection = section.createSection('tilingSettings')
        else:
            return changed
        tilingTypeStr = encodeEnum(CamouflageTilingType, tilingType)
        changed |= _xml.rewriteString(tilingSettingsSection, 'type', tilingTypeStr, 'legacy')
        if tilingSettings[1] is not None:
            factor = Math.Vector2(tilingSettings[1][0], tilingSettings[1][1])
            changed |= _xml.rewriteVector2(tilingSettingsSection, 'factor', factor)
        if tilingSettings[2] is not None:
            offset = Math.Vector2(tilingSettings[2][0], tilingSettings[2][1])
            changed |= _xml.rewriteVector2(tilingSettingsSection, 'offset', offset)
        return changed


def rewriteCamouflageGlossMetallicSettings(section, camouflageItem):
    changed = False
    if camouflageItem.editorData.glossMetallicSettingsType == 0:
        changed |= section.deleteSection('glossMetallicMap')
        changed |= _xml.rewriteVector4(section, 'gloss', camouflageItem.glossMetallicSettings['gloss'])
        changed |= _xml.rewriteVector4(section, 'metallic', camouflageItem.glossMetallicSettings['metallic'])
    elif camouflageItem.editorData.glossMetallicSettingsType == 1:
        changed |= section.deleteSection('gloss')
        changed |= section.deleteSection('metallic')
        changed |= _xml.rewriteString(section, 'glossMetallicMap', camouflageItem.glossMetallicSettings['glossMetallicMap'])
    return changed


def encodeFlagEnum(enumClass, intValue):
    items = []
    degree = 0
    while intValue > 0:
        if intValue % 2 == 1:
            items.append(encodeEnum(enumClass, 1 << degree))
        intValue = intValue >> 1
        degree += 1

    return ' '.join(items)


def encodeEnum(enumClass, intValue):
    for enum, value in enumClass.__dict__.iteritems():
        if enum.startswith('_'):
            continue
        if intValue == value:
            return enum.lower()

    return None
