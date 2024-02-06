from ScreenControls import Screen, Label
from MenuSettings import raddia_symbol
        
class TwoAxes_Screen(Screen):
    '''XY display'''

    def __init__(self, **kwargs):
        super(TwoAxes_Screen, self).__init__(**kwargs)    
        self.name = "XY"
        self.mmdp = "+3.4f"
        self.indp = "+2.5f"
        self.df = "+3.4f"
        self.Xd = Label(master = self.ScnMan,
                        width = 0,
                        height = 0,
                        pos=[0,0],
                        text="X:",
                        font=0,
                        )
        self.Yd = Label(master = self.ScnMan,
                        width = 0,
                        height = 0,
                        pos=[0,32],
                        text="Y:",
                        font=0,
                        )        
        
        self.Xmm = Label(master = self.ScnMan,
                        width = 0,
                        height = 0,
                        pos=[32,0],
                        text="-000.0000",
                        font=0,
                        align="right",
                        )
        self.Ymm = Label(master = self.ScnMan,
                        width = 0,
                        height = 0,
                        pos=[32,32],
                        text="+000.0000",
                        font=0,
                        align="right",
                        )
        
        self.Xrd = Label(master = self.ScnMan,
                        width = 0,
                        height = self.Xmm.height,
                        pos=[150,0],
                        text="",
                        font=-1,
                        align="centre",
                        )
        self.Yrd = Label(master = self.ScnMan,
                        width = 0,
                        height = self.Ymm.height,
                        pos=[150,32],
                        text="",
                        font=-1,
                        align="centre",
                        )
                
        
        self.Units = Label(master = self.ScnMan,
                        width = 30,
                        height = 20,
                        pos=[220,0],
                        text = "mm",
                        font=-1,
                        align="centre",
                        border = 0,
                        )
        
        self.widgets.append(self.Xd)
        self.widgets.append(self.Yd)
        self.widgets.append(self.Xrd)
        self.widgets.append(self.Yrd)  
        self.widgets.append(self.Xmm)
        self.widgets.append(self.Ymm)
        self.widgets.append(self.Units)
        self.Unit_Inch = False
        self.Axes=[] #axes are added by DRO
        
        self.set_params()
        self.set_InchMM()
        
        
    def set_InchMM(self, Inch=None):
        if Inch is not None: self.Unit_Inch = Inch
        U = ("mm","Inch")
        self.Units.set_text(U[self.Unit_Inch])
        dp =(self.mmdp,self.indp)
        self.df = f"{dp[self.Unit_Inch]}"
                
    def do_keys(self, key):
            if key==1:
                self.Axes[0].Zero()
            elif key==4:
                self.Axes[1].Zero()                
            elif key==2:
                self.Unit_Inch = not self.Unit_Inch
                self.set_InchMM()
                
            elif key==3:
                pass

    def set_params(self,):
        self.Xd.text = self.master.Ini.MS["xdes"]
        self.Yd.text = self.master.Ini.MS["ydes"]
        ddo = self.master.Ini.MS["ddsp"]
        self.Xrd.text =""
        self.Yrd.text =""
        if ddo == 1:
            self.Xrd.text = self.master.Ini.get_menutext("xdia")
            self.Yrd.text = self.master.Ini.get_menutext("ydia")
        elif ddo==2:
            #raddia_symbol = ("(<-","(<->)")
            self.Xrd.text = raddia_symbol[self.master.Ini.MS["xdia"]]
            self.Yrd.text = raddia_symbol[self.master.Ini.MS["ydia"]]
        
        self.mmdp = f"+3.{self.master.Ini.MS['mmdp']}f"
        self.indp = f"+2.{self.master.Ini.MS['indp']}f"
        
#====================================================            
    def update(self, key):
        if key: self.do_keys(key)
        fn=(self.Xmm,self.Ymm)
        #update display
        for Ax in self.Axes:
            t = f"{Ax.Get_Pos(self.Unit_Inch):{self.df}}"
            fn[Ax.name=="Y"].set_text(t)
            
    def on_open(self,):
        self.set_params()
        self.set_InchMM()
        
    def on_close(self,):
        pass