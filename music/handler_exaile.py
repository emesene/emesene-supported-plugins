import songretriever
import DBusBase

class ExaileHandler(DBusBase.DBusBase):
    '''Handler for exaile'''
    NAME = 'Exaile'
    DESCRIPTION = 'Music handler for exaile'
    AUTHOR = 'Karasu'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name = 'org.exaile.Exaile',
                 iface_path = '/org/exaile/Exaile'):
        DBusBase.DBusBase.__init__(self, session, iface_name, iface_path)
        self.check_song()

    def state_changed(self):
        '''process player status changes'''
        self.check_song()

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        if DBusBase.DBusBase.reconnect(self):
            self.dbuspropiface = self.module.Interface(self.iface,
                                    dbus_interface='org.exaile.Exaile')
            self.dbuspropiface.connect_to_signal('StateChanged', self.state_changed)
            self.dbuspropiface.connect_to_signal('TrackChanged', self.state_changed)
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
            status = self.iface.GetState()
            return status == "playing"
        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            artist = self.iface.GetTrackAttr('artist')
            if artist == None:
                artist = ""
            album = self.iface.GetTrackAttr('album')
            if album == None:
                album = ""
            title = self.iface.GetTrackAttr('title')
            if title == None:
                title = ""
            return songretriever.Song(artist, album, title)
