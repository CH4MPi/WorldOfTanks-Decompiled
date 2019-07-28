# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/prb_control/entities/event/squad/actions_handler.py
from gui.prb_control.entities.base.squad.actions_handler import SquadActionsHandler
from gui.prb_control.events_dispatcher import g_eventDispatcher

class EventBattleSquadActionsHandler(SquadActionsHandler):

    def _loadPage(self):
        g_eventDispatcher.loadEventHangar()

    def _showBattleQueueGUI(self):
        g_eventDispatcher.loadEventBattleQueue()
