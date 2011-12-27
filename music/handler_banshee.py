import songretriever
import DBusBase

class BansheeHandler(DBusBase.DBusBase):
    '''Handler for banshee'''
    NAME = 'Banshee'
    DESCRIPTION = 'Music handler for banshee'
    AUTHOR = 'Adolfo Fitoria'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name = 'org.bansheeproject.Banshee',
                 iface_path = '/org/bansheeproject/Banshee/PlayerEngine'):
        DBusBase.DBusBase.__init__(self, session, iface_name, iface_path)
        self.check_song()

    def state_changed(self, state):
        '''process player status changes'''
        if state in ["idle", "loading", "loaded"]:
            #skip intermediate status
            return
        self.check_song()

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        if DBusBase.DBusBase.reconnect(self):
            self.dbuspropiface = self.module.Interface(self.iface,
                                    dbus_interface='org.bansheeproject.Banshee.PlayerEngine')
            self.dbuspropiface.connect_to_signal('StateChanged', self.state_changed)
            return True

        return False

    def get_automatic_updates(self):
        '''When the handler can do automatic updates of player status
           and timeout are not needed.
        '''
        return True

    def is_playing(self):
        '''Returns True if a song is being played'''
        if self.is_running():
            if self.iface.GetCurrentState() == "playing":
                return True
        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            info = self.iface.GetCurrentTrack()
            return songretriever.Song(info.get('artist', '?'),
                info.get('album', '?'),
                info.get('name', '?'))

        return None
