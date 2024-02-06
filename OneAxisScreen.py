
from ScreenControls import Screen, Label, VScroll_box
from MenuSettings import raddia_symbol
        
class OneAxis_Screen(Screen):
    '''single axis display with fraction scroll'''

    def __init__(self, **kwargs):
        super(OneAxis_Screen, self).__init__(**kwargs)    
        self.name = "woodworker"
        self.Axis =0 #default axis 0=x 1=y
        self.set_vars()
        
        self.Ad = Label(master = self.ScnMan,
                        width = 12,
                        height = self.height,
                        pos=[0,0],
                        text="X:",
                        font=0,
                        border=1,
                        align="centre",
                        )        
        self.Ain = Label(master = self.ScnMan,
                        width = 0,
                        height = 0,
                        pos=[44,0],
                        text="-00.00000",
                        font=0,
                        align="right",
                        )
        self.Amm = Label(master = self.ScnMan,
                        width = self.Ain.width,
                        height = 0,
                        pos=[44,32],
                        text="+000.0000",
                        font=-1,
                        align="right",
                        )
        
        self.Ard = Label(master = self.ScnMan,
                        width = self.Ain.width,
                        height = self.Amm.height,
                        pos=[44,46],
                        text="diameter",
                        font=-1,
                        align="right",
                        )

        self.FSB = VScroll_box(master=self.ScnMan,
                         pos =[self.width -53,0],
                         font=-1,
                         height = self.height,
                         width = 52,
                         text_align = "left",
                         fetch_fn = self.frac_fetch,
                         )
        
        self.ISB = VScroll_box(master=self.ScnMan,
                         pos =[self.width-100,0],
                         font=-1,
                         height = self.height,
                         width = 37,
                         text_align = "right",
                         fetch_fn = self.inch_fetch,                                  
                         )

        self.Fid = Label(master = self.ScnMan,
                        width = 10,
                        height = 12,
                        pos=[self.width-64,24],
                        text="-",
                        font=-1,
                        align="centre",
                        border=0,
                        )

        self.widgets.append(self.Ad)
        self.widgets.append(self.Ard)
        self.widgets.append(self.Amm)
        self.widgets.append(self.Ain)
        self.widgets.append(self.FSB)
        self.widgets.append(self.ISB)
        self.widgets.append(self.Fid)        
        self.Axes=[] #axes are added by DRO

        
    def inch_fetch(self,itmi, noi):
        t = f'{itmi:+3}-'
        return t
    
    def frac_fetch(self,itmi, noi):
        div = self.Divisor
        itm =itmi%div 
        if itmi==0 or itm==0:
            t="-0"
        else:
            In = self.Axes[self.Axis].Get_Pos(1)
            if In >0.5: 
                itm = abs(itmi)%div                         
            if itmi>0:
                 t = self.Proper_fraction(itm,div )              
            else:
                 t = self.Proper_fraction(div-itm,div )
        return t

    def Proper_fraction(self, Num, Div):
        while Num%2 == 0:
            Num = Num//2
            Div = Div//2        
        return f"-{Num}/{Div}"
        
        
    def do_keys(self, key):
            if key==1:
                self.Axes[self.Axis].Zero()
            elif key==4:
                self.Axis = (1+self.Axis) % len(self.Axes)
                self.set_params()
            elif key==2:
                pass                
            elif key==3:
                pass

    def set_params(self,):
        XY = self.Axes[self.Axis].name.lower()
        self.Ad.set_text(self.master.Ini.MS[f"{XY}des"])
            
        ddo = self.master.Ini.MS["ddsp"]
        self.Ard.text =""
        if ddo == 1:
            self.Ard.text = self.master.Ini.get_menutext(f"{XY}dia")
        elif ddo==2:
            #raddia_symbol = ("(<-","(<->)")
            self.Ard.text = raddia_symbol[self.master.Ini.MS[f"{XY}dia"]]
        self.set_vars()
            
    def set_vars(self,):
        
        self.mmdp = f"+3.{self.master.Ini.MS['mmdp']}f"
        self.indp = f"+2.{self.master.Ini.MS['indp']}f"
        self.Divisor = self.master.Ini.MS["fdiv"]
        self.FHilight = self.master.Ini.MS["fhil"]
        
#====================================================            
    def update(self, key):
        if key: self.do_keys(key)
        #update display
        Ax = self.Axes[self.Axis]
        t = f"{Ax.Get_Pos(0):{self.mmdp}}mm"
        self.Amm.set_text(t)
        In = Ax.Get_Pos(1)
        t = f'{In:{self.indp}}'
        self.Ain.set_text(t+'"')
        #do inch scroll
        iIn = int(In)
        fIn = In-iIn
        dIn = int(fIn * self.ISB.step)
        self.ISB.show(iIn,dIn)
        #do fraction scroll
        #self.Divisor
        sIn = int(fIn*self.Divisor)
        cIn = fIn-(sIn/self.Divisor)
        self.FSB.show(sIn, int(cIn * self.FSB.step *self.Divisor))
        
        if f"{iIn + sIn/self.Divisor:{self.indp}}" == t and self.FHilight:
            self.Fid.set_text(">")
            if self.FHilight ==2 :self.Ain.invert=True
        else:
            self.Fid.set_text("-")
            self.Ain.invert=False
        
    def on_open(self,):
        self.set_params()
        
    def on_close(self,):
        pass