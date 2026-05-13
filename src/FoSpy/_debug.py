from pprint import pprint

class Debug:
    def __init__(self):
        self.on = False

    def msg(self,msg):
        if self.on:
            print(msg)

    def pmsg(self,msg):
        if self.on:
            pprint(msg)


