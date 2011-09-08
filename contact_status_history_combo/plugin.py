import extension
from plugin_base import PluginBase

import HistoryStatusCombo

class Plugin(PluginBase):
    _authors = {'Jose Rostagno':''}
    _description = 'Show a list with the history of online/offline events of' \
                   'every contact with a timestamp'

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.extensions_register()
        return True

    def stop(self):
        return False

    def config(self, session):
        '''method to config the plugin'''
        pass

    def extensions_register(self):
        extension.register('below userlist', HistoryStatusCombo.HistoryStatusCombo)
