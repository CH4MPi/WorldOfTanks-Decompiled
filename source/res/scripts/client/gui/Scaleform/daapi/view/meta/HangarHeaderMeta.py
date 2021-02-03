# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/HangarHeaderMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class HangarHeaderMeta(BaseDAAPIComponent):

    def onQuestBtnClick(self, questType, questID):
        self._printOverrideError('onQuestBtnClick')

    def as_setDataS(self, data):
        return self.flashObject.as_setData(data) if self._isDAAPIInited() else None

    def as_createBattlePassS(self):
        return self.flashObject.as_createBattlePass() if self._isDAAPIInited() else None

    def as_removeBattlePassS(self):
        return self.flashObject.as_removeBattlePass() if self._isDAAPIInited() else None

    def as_createRankedBattlesS(self):
        return self.flashObject.as_createRankedBattles() if self._isDAAPIInited() else None

    def as_removeRankedBattlesS(self):
        return self.flashObject.as_removeRankedBattles() if self._isDAAPIInited() else None

    def as_createBobS(self):
        return self.flashObject.as_createBob() if self._isDAAPIInited() else None

    def as_removeBobS(self):
        return self.flashObject.as_removeBob() if self._isDAAPIInited() else None
