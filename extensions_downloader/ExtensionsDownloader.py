'''module to define the ExtensionsDownloader class, used by plugin.py'''
import gtk
import gobject

import e3
import gui
import extension
from gui.gtkui import utils

from DownloadExtension import DownloadExtension

class ExtensionsDownloader():
    """a plugin to download themes and plugins"""
    NAME = 'Extensions Downloader'
    DESCRIPTION = 'A plugin to download themes and plugins'
    AUTHOR = 'Andrea Stagi'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session):
        """constructor"""
        self.session = session
        self.instance = extension.get_and_instantiate('preferences', self.session)

        if self.session is not self.instance.session:
            extension.delete_instance('preferences')
            self.instance = extension.get_and_instantiate('preferences', self.session)

        self.page = DownloadExtension(self.session)

    def add_list_item(self):
        self.instance.add_to_list(gtk.STOCK_NETWORK, _('Download extensions'), self.page)


    def remove_list_item(self):
        self.instance.remove_from_list(gtk.STOCK_NETWORK, _('Download extensions'), self.page)
        

    def on_status_changed(self , *args):
        """called when a status is selected"""
        stat = self.model.get(self.get_active_iter(), 1)[0]

        if self.status != stat:
            self.status = stat
            self.main_window.session.set_status(stat)

    def on_status_change_succeed(self, stat):
        """called when the status was changed on another place"""
        if stat in e3.status.ORDERED:
            self.status = stat
            index = e3.status.ORDERED.index(stat)
            self.set_active(index)

    def on_scroll_event(self, button, event):
        """called when a scroll is made over the combo"""
        self.popup()
        return True
