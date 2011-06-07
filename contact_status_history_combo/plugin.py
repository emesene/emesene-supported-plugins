import extension
from plugin_base import PluginBase

import HistoryStatusCombo

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.extensions_register()
        return True

    def stop(self):
        #disconect signals
        self.on_stop()
        return False

    def config(self, session):
        '''method to config the plugin'''
        pass

    def extensions_register(self):
        extension.register('below userlist', HistoryStatusCombo.HistoryStatusCombo)
