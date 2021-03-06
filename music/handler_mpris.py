import songretriever
import DBusBase

class MprisBase(DBusBase.DBusBase):
    def __init__(self, session, iface_name, iface_path):
        DBusBase.DBusBase.__init__(self, session, iface_name, iface_path)
        self.check_song()

    def status_change(self, state):
        '''process player status changes'''
        self.check_song()

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        if DBusBase.DBusBase.reconnect(self):
            self.dbuspropiface = self.module.Interface(self.iface,
                                    dbus_interface='org.freedesktop.MediaPlayer')
            self.dbuspropiface.connect_to_signal('StatusChange', self.status_change)
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
            status = self.iface.get_dbus_method("GetStatus", 
                dbus_interface='org.freedesktop.MediaPlayer')()
            return status[0] == 0
        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            song = self.iface.get_dbus_method("GetMetadata",
                dbus_interface='org.freedesktop.MediaPlayer')()
            return songretriever.Song(song.get('artist', "?"),
                                      song.get('album', "?"),
                                      song.get('title', "?"))

class ClementineHandler(MprisBase):
    '''Handler for Clementine'''
    NAME = 'Clementine'
    DESCRIPTION = 'Music handler for Clementine'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name='org.mpris.clementine',
                 iface_path='/Player'):
        MprisBase.__init__(self, session, iface_name, iface_path)

class AudaciousHandler(MprisBase):
    '''Handler for Audacious'''
    NAME = 'Audacious'
    DESCRIPTION = 'Music handler for Audacious'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name='org.mpris.audacious',
                 iface_path='/Player'):
        MprisBase.__init__(self, session, iface_name, iface_path)

    def get_automatic_updates(self):
        '''When the handler can do automatic updates of player status
           and timeout are not needed.
        '''
        return False

class Amarok2Handler(MprisBase):
    '''Handler for Amarok2'''
    NAME = 'Amarok2'
    DESCRIPTION = 'Music handler for Amarok2'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name='org.mpris.amarok',
                 iface_path='/Player'):
        MprisBase.__init__(self, session, iface_name, iface_path)

class GuayadequeHandler(MprisBase):
    '''Handler for guayadeque'''
    NAME = 'Guayadeque'
    DESCRIPTION = 'Music handler for guayadeque'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session,
                 iface_name='org.mpris.guayadeque',
                 iface_path='/Player'):
        MprisBase.__init__(self, session, iface_name, iface_path)
