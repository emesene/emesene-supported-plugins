#!/usr/bin/env python

import extension
from plugin_base import PluginBase

import SnarlNotification 

class Plugin(PluginBase):
    _description = "Plugin for Snarl notifications"
    _authors = {"Shawn McTear": "syst3mfailur3@gmail.com"}

    def __init__(self):
        """Initialize plugin"""
        PluginBase.__init__(self)
        self.sn = SnarlNotification.sn

    def start(self, session):
        """Start plugin"""
        self.session = session
        self.sn.register('application/x-emesene2', 'emesene2')
        
    def stop(self):
        """Stop plugin"""
        self.sn.unregister('application/x-emesene2')

    def config(self, session):
        """Configurations for plugin"""
        pass

    def extension_register(self):
        """Register extention"""
        extension.register('notificationGUI', SnarlNotification.SnarlNotification)
