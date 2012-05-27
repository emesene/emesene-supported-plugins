import extension
import os
import re

from plugin_base import PluginBase
from gui.base import Handler
import MusicButton

CATEGORY = 'listening to'

import songretriever

#import handlers
if os.name != "nt": #import unix players
    import handler_banshee
    import handler_exaile
    import handler_lastfm
    import handler_moc
    import handler_mpd
    import handler_mpris
    import handler_mpris2
    import handler_rhythmbox

    try:
        import handler_xmms2
        XMMSCLIENT = True
    except ImportError:
        XMMSCLIENT = False

    #Import OS X players
    import handler_itunes
    import handler_spotify
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

class Plugin(PluginBase):
    _authors = {'Mariano Guerra':'', 'Ariel Juodziukynas':'', 'Karasu':'',
                'Josh F':'', 'Adolfo Fitoria':''}
    _description = 'Show in your message what you are listening to'

    def __init__(self):
        PluginBase.__init__(self)

        self.session = None
        self.player = None

    def stop(self):
        '''stop the plugin'''
        self.session = None
        extension.delete_instance(CATEGORY)
        if hasattr(extension, 'unregister'):
            extension.unregister('userpanel button', MusicButton.MusicButton)
            self.extensions_unregister()

        return True

    def start(self, session):
        '''start the plugin'''
        self.session = session

        extension.category_register(CATEGORY, songretriever.BaseMusicHandler, songretriever.BaseMusicHandler, True)
        self.extensions_register()

        extension.get_and_instantiate(CATEGORY, session)

        if hasattr(extension, 'unregister'):
            extension.register('userpanel button', MusicButton.MusicButton, force_default=True)
        else:
            extension.register('userpanel button', MusicButton.MusicButton)

        return True

    def config(self, session):
        '''config the plugin'''
        player = extension.get_instance(CATEGORY)

        if player is not None:
            player.preferences()

        return True

    def configurable(self):
        '''this plugin is configurable'''
        return True

    def extensions_register(self):
        if os.name != "nt": #import unix players
            extension.register(CATEGORY, handler_mpris.Amarok2Handler)
            extension.register(CATEGORY, handler_mpris.AudaciousHandler)
            extension.register(CATEGORY, handler_banshee.BansheeHandler)
            extension.register(CATEGORY, handler_mpris.ClementineHandler)
            extension.register(CATEGORY, handler_exaile.ExaileHandler)
            extension.register(CATEGORY, handler_mpris2.GMusicBrowserHandler)
            extension.register(CATEGORY, handler_mpris.GuayadequeHandler)
            extension.register(CATEGORY, handler_lastfm.LastfmHandler)
            extension.register(CATEGORY, handler_moc.MocHandler)
            extension.register(CATEGORY, handler_mpd.MpdHandler)
            extension.register(CATEGORY, handler_mpris2.PraghaHandler)
            extension.register(CATEGORY, handler_mpris2.RhythmboxHandler)
            extension.register(CATEGORY, handler_mpris2.AudaciousHandler)
            extension.register(CATEGORY, handler_rhythmbox.RhythmboxHandler)

            #OS X players
            extension.register(CATEGORY, handler_itunes.iTunesHandler)
            extension.register(CATEGORY, handler_spotify.SpotifyHandler)

            if XMMSCLIENT:
                extension.register(CATEGORY, handler_xmms2.Xmms2Handler)

            handler_id = self.session.config.d_extensions.get(CATEGORY, None)

            if handler_id is None:
                handler_id = extension._get_class_name(handler_rhythmbox.RhythmboxHandler)
                self.session.config.d_extensions.get(CATEGORY, handler_id)
        else: #import Windows players
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

    def extensions_unregister(self):
        if os.name != "nt": #import unix players
            extension.unregister(CATEGORY, handler_mpris.Amarok2Handler)
            extension.unregister(CATEGORY, handler_mpris.AudaciousHandler)
            extension.unregister(CATEGORY, handler_banshee.BansheeHandler)
            extension.unregister(CATEGORY, handler_mpris.ClementineHandler)
            extension.unregister(CATEGORY, handler_exaile.ExaileHandler)
            extension.unregister(CATEGORY, handler_mpris2.GMusicBrowserHandler)
            extension.unregister(CATEGORY, handler_mpris.GuayadequeHandler)
            extension.unregister(CATEGORY, handler_lastfm.LastfmHandler)
            extension.unregister(CATEGORY, handler_moc.MocHandler)
            extension.unregister(CATEGORY, handler_mpd.MpdHandler)
            extension.unregister(CATEGORY, handler_mpris2.PraghaHandler)
            extension.unregister(CATEGORY, handler_mpris2.RhythmboxHandler)
            extension.unregister(CATEGORY, handler_mpris2.AudaciousHandler)
            extension.unregister(CATEGORY, handler_rhythmbox.RhythmboxHandler)

            #OS X players
            extension.unregister(CATEGORY, handler_itunes.iTunesHandler)
            extension.unregister(CATEGORY, handler_spotify.SpotifyHandler)

            if XMMSCLIENT:
                extension.unregister(CATEGORY, handler_xmms2.Xmms2Handler)
        else: #import Windows players
            extension.unregister(CATEGORY, handler_atunes.aTunesHandler)
            extension.unregister(CATEGORY, handler_foobar2000.Foobar2000Handler)
            extension.unregister(CATEGORY, handler_gomplayer.GOMPlayerHandler)
            extension.unregister(CATEGORY, handler_mediamonkey.MediaMonkeyHandler)
            extension.unregister(CATEGORY, handler_mediaplayerclassic.MediaPlayerClassicHandler)
            extension.unregister(CATEGORY, handler_onebyone.OneByOneHandler)
            extension.unregister(CATEGORY, handler_realplayer.RealPlayerHandler)
            extension.unregister(CATEGORY, handler_smplayer.SMPlayerHandler)
            extension.unregister(CATEGORY, handler_winamp.WinampHandler)
            extension.unregister(CATEGORY, handler_xmplay.XMPlayHandler)
