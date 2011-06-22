import songretriever
import commands

class SpotifyHandler(songretriever.MusicHandler):
    '''Handler for Spotify'''
    NAME = 'Spotify'
    DESCRIPTION = 'Music handler for Spotify OS X'
    AUTHOR = 'Josh F'
    WEBSITE = 'www.sidhosting.co.uk'
    
    def __init__(self, main_window = None):
        songretriever.MusicHandler.__init__(self, main_window)
                
    def is_playing(self):
        command = "/Applications/emesene.app/Contents/Resources/emesene/plugins/music/isplaying Spotify 2>/dev/null"
        status = commands.getoutput(command) 
        return status == 'playing' 

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            getartist = """osascript -e 'tell application "Spotify" to artist of current track' 2>/dev/null"""
            artist = commands.getoutput(getartist)
            getalbum = """osascript -e 'tell application "Spotify" to album of current track' 2>/dev/null"""
            album = commands.getoutput(getalbum)
            gettitle = """osascript -e 'tell application "Spotify" to name of current track' 2>/dev/null"""
            title = commands.getoutput(gettitle)
            return songretriever.Song(artist, album, title)