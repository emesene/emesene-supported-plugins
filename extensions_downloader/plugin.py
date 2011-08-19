import extension
from plugin_base import PluginBase

import ExtensionsDownloader

class Plugin(PluginBase):
    _authors = {'Andrea Stagi':''}
    _description = 'A plugin to download themes'

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.session = session
        self.extensions_register()
        self.instance = ExtensionsDownloader.ExtensionsDownloader(self.session)
        self.instance.add_list_item()

    def stop(self):
        self.instance.remove_list_item()

    def extensions_register(self):
        extension.register('extension downloader', ExtensionsDownloader.ExtensionsDownloader)
