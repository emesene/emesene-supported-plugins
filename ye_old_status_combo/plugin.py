import extension
from plugin_base import PluginBase

import StatusCombo

class Plugin(PluginBase):
    _author = {'Mariano Guerra':''}
    _description = 'A combo to select the status like emesene 1.0'
    
    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        if hasattr(extension, 'unregister'):
            extension.register('below userlist', StatusCombo.StatusCombo, force_default=True)
        else:
            extension.register('below userlist', StatusCombo.StatusCombo)
        return True

    def stop(self):
        if hasattr(extension, 'unregister'):
            extension.unregister('below userlist', StatusCombo.StatusCombo)
        return False

    def config(self, session):
        '''method to config the plugin'''
        pass
