#we need to import the extension module to handle extensions
import extension
from plugin_base import PluginBase

#we also need to import the widget we are going to display
import Widget

class Plugin(PluginBase):
    #description and author/s to show on preferences
    _description = "Plugin that prints 'Hello world'"
    _authors = {"arielj": "arieljuod@gmail.com"}

    #this will be called the first time the plugin is started
    def __init__(self):
        #first of all, call PluginBase's init
        PluginBase.__init__(self)

    #you MUST implement this, check /plugin_base.py on the root directory
    def start(self, session):
        '''do whatever your plugin will do at start
          -subscribe session signals
          -call some session's method
          -etc...
        '''
        self._started = True #used for PluginBase.is_active method
        self.extensions_register() #we register the extension at start

    #you MUST implement this, check /plugin_base.py on the root directory
    def stop(self):
        '''do whatever your plugin will do at stop:
          -unsubscribe session signals subscribed at start (always unsubscribe all subscribed signals!!)
          -disconnect signals connected at start
          -destroy or delete objects if needed (remember, Python uses a Garbage collector)
          -etc...
        
          you can use the sentence "pass" if you want a blank method:
              def stop(self):
                  pass
        '''
        self._started = False #used for PluginBase.is_active method

    #if you have some config for your plugin, you must implement this method
    def config(self, session):
        pass

    def extensions_register(self):
        #register the custom widget to the desired category
        extension.register('below panel', Widget.HelloWorldWidget)
