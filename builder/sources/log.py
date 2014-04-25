class AseLog:
    def __init__(self, aliases=None, mute=False):
        self.mute = mute
        if isinstance(aliases, dict):
            self.aliases = aliases
        else:
            self.aliases = {}
        
    def put(self, message, args=None):
        if not self.mute:
            if self.aliases.has_key(message):
                message = self.aliases[message]
            if args is not None:
                message = message % args
            print message
            
    def log(self, message, args=None):
        self.put(message, args)
        
    def mute(self):
        self.mute = True
        
    def unmute(self):
        self.mute = False
