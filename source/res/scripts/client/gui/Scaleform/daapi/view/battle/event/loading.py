# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/event/loading.py
from helpers import dependency
from gui.battle_control.arena_info.interfaces import IArenaLoadController
from skeletons.gui.battle_session import IBattleSessionProvider
from gui.Scaleform.daapi.view.bootcamp.bc_intro_page import BCIntroPage

class EventLoading(BCIntroPage, IArenaLoadController):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def _populate(self):
        super(EventLoading, self)._populate()
        self.sessionProvider.addArenaCtrl(self)

    def _dispose(self):
        self.sessionProvider.removeArenaCtrl(self)
        super(EventLoading, self)._dispose()

    def updateSpaceLoadProgress(self, progress):
        self.as_updateProgressS(progress)

    def videoFinished(self):
        pass
