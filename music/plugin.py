import extension

import os

from plugin_base import PluginBase

CATEGORY = 'listening to'

class Plugin(PluginBase):
    _authors = {'Mariano Guerra':'', 'Ariel Juodziukynas':'', 'Karasu':'',
                'Josh F':'', 'Adolfo Fitoria':''}
    _description = 'Show in your message what you are listening to'

    def __init__(self):
        PluginBase.__init__(self)

        self.session = None
        self.running = False

        self.player = None

    def stop(self):
        '''stop the plugin'''
        self.session = None
        self.running = False
        return True

    def start(self, session):
        '''start the plugin'''
        self.session = session

        self.category_register()
        self.extensions_register()

        self.running = True

        return True

    def config(self, session):
        '''config the plugin'''
        category = extension.get_category(CATEGORY)
        player = category.get_instance()

        if player != None:
            player.preferences()

        return True

    def configurable(self):
        '''this plugin is configurable'''
        return True

    def category_register(self):
        import songretriever
        extension.category_register(CATEGORY, songretriever.BaseMusicHandler, songretriever.BaseMusicHandler, True)

        return True

    def extensions_register(self):
        if os.name != "nt": #import unix players
            import handler_amarok2
            import handler_audacious2
            import handler_banshee
            import handler_clementine
            import handler_exaile
            import handler_gmusicbrowser
            import handler_guayadeque
            import handler_lastfm
            import handler_moc
            import handler_mpd
            import handler_mpris
            import handler_rhythmbox

            try:
                import handler_xmms2
                XMMSCLIENT = True
            except ImportError:
                XMMSCLIENT = False

            extension.register(CATEGORY, handler_amarok2.Amarok2Handler)
            extension.register(CATEGORY, handler_audacious2.Audacious2Handler)
            extension.register(CATEGORY, handler_banshee.BansheeHandler)
            extension.register(CATEGORY, handler_clementine.ClementineHandler)
            extension.register(CATEGORY, handler_exaile.ExaileHandler)
            extension.register(CATEGORY, handler_gmusicbrowser.GMusicBrowserHandler)
            extension.register(CATEGORY, handler_guayadeque.GuayadequeHandler)
            extension.register(CATEGORY, handler_lastfm.LastfmHandler)
            extension.register(CATEGORY, handler_moc.MocHandler)
            extension.register(CATEGORY, handler_mpd.MpdHandler)
            extension.register(CATEGORY, handler_mpris.MprisHandler)
            extension.register(CATEGORY, handler_rhythmbox.RhythmboxHandler)
            
            #Import OS X players
            import handler_itunes
            import handler_spotify
            extension.register(CATEGORY, handler_itunes.iTunesHandler)
            extension.register(CATEGORY, handler_spotify.SpotifyHandler)

            if XMMSCLIENT:
                extension.register(CATEGORY, handler_xmms2.Xmms2Handler)

            handler_id = self.session.config.d_extensions.get(CATEGORY, None)

            if handler_id is None:
                handler_id = extension._get_class_name(handler_rhythmbox.RhythmboxHandler)
                self.session.config.d_extensions.get(CATEGORY, handler_id)
        else: #import Windows players
            import handler_atunes
            import handler_foobar2000
            import handler_gomplayer
            import handler_mediamonkey
            import handler_mediaplayerclassic
            import handler_onebyone
            import handler_realplayer
            import handler_smplayer
            import handler_winamp
            import handler_xmplay
            
            extension.register(CATEGORY, handler_atunes.aTunesHandler)
            extension.register(CATEGORY, handler_foobar2000.Foobar2000Handler)
            extension.register(CATEGORY, handler_gomplayer.GOMPlayerHandler)
            extension.register(CATEGORY, handler_mediamonkey.MediaMonkeyHandler)
            extension.register(CATEGORY, handler_mediaplayerclassic.MediaPlayerClassicHandler)
            extension.register(CATEGORY, handler_onebyone.OneByOneHandler)
            extension.register(CATEGORY, handler_realplayer.RealPlayerHandler)
            extension.register(CATEGORY, handler_smplayer.SMPlayerHandler)
            extension.register(CATEGORY, handler_winamp.WinampHandler)
            extension.register(CATEGORY, handler_xmplay.XMPlayHandler)

            handler_id = self.session.config.d_extensions.get(CATEGORY, None)

            if handler_id is None:
                handler_id = extension._get_class_name(handler_winamp.WinampHandler)
                self.session.config.d_extensions.get(CATEGORY, handler_id)

        extension.set_default_by_id(CATEGORY, handler_id)
