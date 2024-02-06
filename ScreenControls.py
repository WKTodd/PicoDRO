#w.k.todd 2024
#screen controls for screen_manager
from time import sleep_ms
import gc

class Screen():

    def __init__(self, master=None, name="",):
        self.master= master
        self.ScnMan = self.master.ScnMan
        self.name =  name
        self.width = self.ScnMan.width
        self.height = self.ScnMan.height
        self.widgets=[]

class Label():

    def __init__(self, master=None, width=0, height=0 , pos=[0,0], text="",
                 font=-1, colour=15, align="left", border=0, value=None,
                 invert=False,):
        self.scnman = master #screen controller
        #print(self.scnman)
        self.font=font
        self.pos = pos
        self.text= text
        self.colour=colour
        self.align = align # 'right' or 'centre'
        self.width = width - (border*2)
        self.height =height - (border*2)
        self.border = border
        self.text_loc = [0,0]
        self.border_colour = 15
        self.invert = False
        self.value = value #general purpose variable
        self.invert = invert
        
        tw = self.scnman.text_width(self.font,self.text,)
        
        if self.width < tw:
            self.width= tw + (border*4)
            
        th = self.scnman.font_height(self.font)
        
        if self.height < th:
            self.height= th + (border*4)
        
        self.set_loc()
 
    def set_text(self, text):
        self.text=text
        self.set_loc()
        self.scnman.update(self)
        
    def set_loc(self):
        #align text
        tw = self.scnman.text_width(self.font, self.text)
        self.text_loc[1] = self.border + (self.height - self.scnman.font_height(self.font)) //2
        if "ce" in self.align:
            self.text_loc[0] = (self.border*2) +  (self.width - tw) //2
        elif "ri" in self.align:
            self.text_loc[0] = (self.border*2) +  self.width - tw
        else: #align left
            self.text_loc[0]= self.border
           
    def refresh(self):
        self.set_loc()
        self.scnman.refresh()
        
class Frame():
    
    def __init__(self,master=None, width=0, height=0 , pos=[0,0],):
        self.scnman = master #screen controller
        self.widgets=[]
        self.pos = pos
        self.width = width
        self.height = height
        
    def add_widget(self, w):
        #adjust width to contain widgets and set master
        w.scnman = self.scnman
        self.widgets.append(w)
    
    def refresh(self,):
        self.scnman.refresh()
    
    def update(self, widget):
        Xo, Yo = self.pos
        self.scnman.update(widget, Xo, Yo)
        

class VScroll_box(Frame):
    
    def __init__(self, **kwargs):
        self.font=kwargs.pop("font")
        if "fetch_fn" in kwargs.keys():
            self.fetch = kwargs.pop("fetch_fn")
        else:
            self.fetch = self.default_fetch
            
        self.text_align = kwargs.pop("text_align")
        
        super(VScroll_box, self).__init__(**kwargs)    
        self.labels=[]
        self.Items=[] #strings place holders for testing
        self.spacer =4
        
        if self.font is not None:
            #add labels
            self.step = self.spacer + self.scnman.font_height(self.font)
            self.nol = 2 + self.scnman.height //self.step
            if self.nol<5 : self.nol = 5 #quick bodge
            self.mid = self.nol//2
            
            self.cur_itm = 0 #scroll item
            self.cursor = (self.height-self.step-self.spacer)//2
            self.cursor_colour = 4
            self.labpos=[]
            
            offset =  -self.step * self.mid            
            #print(nol)
            for I in range(self.nol):
                lp =  offset + (I * self.step) + self.cursor
                self.labpos.append(lp)                
                NL = Label(master=self.scnman,
                             text="     ",
                             font = self.font,
                             pos = [2, lp],
                             height = self.step,
                             width = self.width,
                             colour = 15, #- (abs(I-self.mid)*4),
                             align = self.text_align,
                             )
                self.labels.append(NL)
                self.add_widget(NL)
            #print(self.nol,self.labpos,self.spacer,self.step)    
        else:            
            raise Exception("VScroll_box: no font defined")

    def add_item(self, item):
        self.Items.append(item)
    
    def sort_items(self,):
        self.Items.sort()
        
    def clr_items(self,):
        self.Items = []
        #self.clear()
        gc.collect
        
    def clear(self,):
        for L in self.labels:
            L.text=""
        self.update(self)
        
    def show(self, Itm, offset=0):
        if type(Itm) is str:
            Itm_no = self.Items.index(Itm)
        else:
            Itm_no = Itm
        
        ilo=  Itm_no - self.mid #item list offset from middle
        
        noi = len(self.Items)
        if noi ==0:noi=1e6 # #no roll over
        self.cur_itm = Itm_no % noi #can be changed in external fetch
        
        for I in range(self.nol):
            itmi = (I + ilo) #% noi
            self.labels[I].text = self.fetch(itmi, noi)
            self.labels[I].pos[1] = self.labpos[I] - offset
        
        self.update(self)
        
    def default_fetch(self, itmi,noi,):
        return self.Items[itmi%noi]

    def slide(self, offset):
        for I in range(self.nol):
            self.labels[I].pos[1] = self.labpos[I] - offset
        
    def shuffle(self, Up):
        Dv=(-1,1)
        self.cur_itm += Dv[Up]
        self.show(self.cur_itm)

    def animate(self, Up):       
        n = self.step//12
        Dv=(-1,1)
        for I in range(0,self.step,n):
            self.slide(Dv[Up]*I)
            self.update(self)
            sleep_ms(5)
        self.shuffle(Up)
        

    def get_sel(self):
        #return item text at cursor
        return self.labels[self.mid].text
    
    def get_itemno(self):
        return self.cur_itm #+ self.mid
        
    
    
#=============    
        
class Menu():
    settings_file="" #path
    Cur_Item =0
    Cur_Opt = 0
    Screen = None #sceen object or number
    master = None # screen_controller
    font = None
    settings={}
    
    def __init__(self, master, screen, set_file, show=False):
        self.scnman = master
        self.screen=screen
        self.show = show
        self.settings_file = set_file
        import json
        #load JSON
            
    