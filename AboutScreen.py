from ScreenControls import Screen, Label

        
class About_Screen(Screen):
    '''About screen for DRO'''

    def __init__(self, **kwargs):
        self.version = kwargs.pop("Version")
        super(About_Screen, self).__init__(**kwargs)    
        self.name = "About"

        self.AL = Label(master = self.ScnMan,
                        width = self.width,
                        height = 0,
                        pos=[0,30],
                        text="(c) W.K.Todd 2024",
                        font=-1,
                        align="centre",
                        )
        
        self.VL = Label(master = self.ScnMan,
                        width = self.width,
                        height = 20,
                        pos=[0,0],
                        text = f"DRO version:{self.version}",
                        font=-1,
                        align="centre",
                        border = 1,
                        )
        
        self.widgets.append(self.AL)
        self.widgets.append(self.VL)
        
#=================================================        
    def update(self, key):
        pass

    def on_open(self,):
        pass
    
    def on_close(self,):
        pass