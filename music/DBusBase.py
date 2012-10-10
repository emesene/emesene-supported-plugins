import songretriever

ROOT_NAME = 'org.freedesktop.DBus'
ROOT_PATH = '/org/freedesktop/DBus'

class DBusBase(songretriever.MusicHandler):
    '''Handler for music players that use D-Bus'''

    def __init__(self, main_window, iface_name, iface_path):
        songretriever.MusicHandler.__init__(self, main_window)
        
        self.iface_name = iface_name
        self.iface_path = iface_path

        try:
            import dbus
            from dbus.mainloop.glib import DBusGMainLoop
            DBusGMainLoop(set_as_default = True)
            dbus.SessionBus()
        except dbus.DBusException, error:
            print 'Unable to use D-Bus: %s' % str(error)

        # dbus session, this is set in reconnect.
        self.bus = None
        # dbus interface set in reconnect.
        self.iface = None
        self.module = dbus
        self.root = dbus.SessionBus().get_object(ROOT_NAME, ROOT_PATH)
        self.autocheck_bus()

    def autocheck_bus(self):
        '''monitor bus for connect/disconnect events'''
        session = self.module.SessionBus()
        def cb(conected):
            if conected: # may be empty
                self.start()
            else:
                self.stop()

        self.watch = session.watch_name_owner(self.iface_name, cb)

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        ''' You don't need to override this'''
        self.bus = self.module.SessionBus()
        try:
            self.iface = self.bus.get_object(self.iface_name, self.iface_path)
            return True
        except self.module.DBusException, error:
            self.iface = None
            print 'D-Bus error: %s' % str(error)
            return False

    def is_running(self):
        '''Returns a True if the player is running'''
        ''' You don't need to override this'''
        if self.is_name_active(self.iface_name):
            if self.iface is None:
                self.reconnect()
            return True
        else:
            self.stop()
            return False

    def stop(self):
        songretriever.MusicHandler.stop(self)
        self.iface = None

    def is_playing(self):
        '''Returns True if a song is being played'''
        ''' This MUST be overriden'''
        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        ''' This MUST be overriden'''
        return False

    def is_name_active(self, name):
        '''return True if the name is active on dbus'''
        ''' You don't need to override this'''
        return bool(self.root.NameHasOwner(name))

