import songretriever
import DBusBase

class MprisBase(DBusBase.DBusBase):
    def __init__(self, main_window, iface_name, iface_path):
        DBusBase.DBusBase.__init__(self, main_window, iface_name, iface_path)

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
            return songretriever.Song(song['artist'],
                                      song['album'],
                                      song['title'])

class ClementineHandler(MprisBase):
    '''Handler for Clementine'''
    NAME = 'Clementine'
    DESCRIPTION = 'Music handler for Clementine'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window=None,
                 iface_name='org.mpris.clementine',
                 iface_path='/Player'):
        MprisBase.__init__(self, main_window, iface_name, iface_path)

class Amarok2Handler(MprisBase):
    '''Handler for Amarok2'''
    NAME = 'Amarok2'
    DESCRIPTION = 'Music handler for Amarok2'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window=None,
                 iface_name='org.mpris.amarok',
                 iface_path='/Player'):
        MprisBase.__init__(self, main_window, iface_name, iface_path)

class GuayadequeHandler(MprisBase):
    '''Handler for guayadeque'''
    NAME = 'Guayadeque'
    DESCRIPTION = 'Music handler for guayadeque'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window = None,
                 iface_name='org.mpris.guayadeque',
                 iface_path='/Player'):
        MprisBase.__init__(self, main_window, iface_name, iface_path)

