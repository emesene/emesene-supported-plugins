import songretriever
import commands

class SpotifyHandler(songretriever.MusicHandler):
    '''Handler for Spotify'''
    NAME = 'Spotify'
    DESCRIPTION = 'Music handler for Spotify on OS X'
    AUTHOR = 'Josh F'
    WEBSITE = 'www.sidhosting.co.uk'
    
    def __init__(self, session):
        songretriever.MusicHandler.__init__(self, session)
        
    def is_running(self):
        '''Check whether Spotify is running'''
        isrunning = """osascript -e 'tell application "System Events" to (name of processes) contains "Spotify"' 2>/dev/null"""
        running = commands.getoutput(isrunning) 
        return running == 'true' 

    def is_playing(self):
        '''Check whether Spotify is playing'''
        if self.is_running():
            isplaying = """osascript -e 'tell application "Spotify" to player state as string' 2>/dev/null"""
            playerstate = commands.getoutput(isplaying) 
            return playerstate == 'playing'  

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
