from ScreenControls import Screen, Label, VScroll_box
from time import sleep
import gc

class Menu_Screen(Screen):
    '''Settings menu display'''

    
    def __init__(self, **kwargs):
        super(Menu_Screen, self).__init__(**kwargs)    
        self.name = "Menu"
        
        self.SBwidth = self.width //2 +50
        self.mode=0
        self.save_opt=0
        #setting
        self.SB = VScroll_box(master=self.ScnMan,
                             pos =[0,0],
                             font=-1,
                             height = self.height,
                             width = self.SBwidth,
                             text_align="left",   
                             )
        #current setting
        self.CS = Label(master=self.ScnMan,
                             pos =[self.SBwidth, self.SB.cursor],
                             font=-1,
                             height = 0,
                             width = self.width - self.SBwidth,
                             border =1
                        )
        self.CS.border_colour = self.SB.cursor_colour
        #options initially off screen
        self.OB = VScroll_box(master=self.ScnMan,
                             pos =[self.width,0],
                             font=-1,
                             height = self.height,
                             width = self.width - self.SBwidth,
                             text_align="left",    
                             )
        
        
        self.widgets.append(self.SB)
        self.widgets.append(self.CS)
        self.widgets.append(self.OB)


        # Menu_Options[0] = list of options
        # Menu_Options[x][0] = option description string - change for language
        # Menu_Options[x][1] = internal parameter -  do not change
        #Menu_Text.keys() = menu display string - change for different languages
        #Menu_Text[key][0] = index of Menu_Options
        #Menu_Text[key][1] = default option select
        #Menu_Text[key][2] = internal dict key -do not change

        
    def get_menustuff(self,):
        from MenuSettings import Menu_Options
        from MenuSettings import Menu_Text
        
        self.MO = Menu_Options
        self.MT = Menu_Text
                
        self.SB.add_item("Back and")
        self.update_options("Back")
        
        for I in Menu_Text: #add menu text
            self.SB.add_item(I)        
        self.SB.sort_items()
    
    def clr_menustuff(self,):
        self.SB.clr_items()
        self.OB.clr_items()
        del self.MO
        del self.MT
        gc.collect()
        
    def update_options(self, Dictkey):
        #load OB.items with options
        self.OB.clr_items()
        if "Back" in Dictkey:
            opt = ("Save","Discard")
            self.OB.add_item(opt[0])
            self.OB.add_item(opt[1])
            itm = opt[self.save_opt]
            
        else:
            opts = self.MT[Dictkey][0]
            Mkey = self.MT[Dictkey][2]
            cur_param = self.master.Ini.MS[Mkey]
            itm="" #default item

            for OS in self.MO[opts]:
                self.OB.add_item(OS[0])
                if OS[1] == cur_param:
                    itm = OS[0]
                    
            #fault here somewhere        
        self.CS.set_text(itm)            
        self.OB.show(itm)
        
    def set_option(self, Opt_no):
        #set selected option
        Dictkey  = self.SB.get_sel()
        #print(Opt_no)
        if "Back" in Dictkey:
            #self.master.back()
            self.save_opt = Opt_no
        else:
            Mkey = self.MT[Dictkey][2]
            opts = self.MT[Dictkey][0]
            self.master.Ini.MS[Mkey]= self.MO[opts][Opt_no][1]
            
        

    def set_mode(self,mode):
        #set option or setting mode
        if mode != self.mode:
            self.mode = mode
            self.update_options(self.SB.get_sel())
            if mode==1:
                #show and scroll Opt Box
                for I in range(self.width, self.SBwidth, -1):
                    self.OB.pos[0] = I
                    self.ScnMan.update(self.OB)
                self.CS.pos[0] = self.width #offscreen    
                                           
            else:
                self.CS.pos[0] = self.SBwidth
                for I in range(self.SBwidth, self.width, 2):
                    self.OB.pos[0] = I
                    self.CS.width = self.SBwidth - (self.width -I)
                    self.ScnMan.update(self.OB)
                    self.ScnMan.update(self.CS)   
 

    def do_mode(self, UD):
            if self.mode==1:
                self.OB.animate(Up=UD)              
            else:
                self.SB.animate(Up=UD)
                #self.SB.shuffle(Up=UD)
                self.update_options(self.SB.get_sel())
        
    def do_keys(self, key):
        if key==1:
            self.do_mode(True)
        elif key==2:
            self.set_mode(1)     
        elif key==3:
            if self.mode==1:
                self.set_option(self.OB.get_itemno())
                self.set_mode(0)
                if "Back" in self.SB.get_sel():
                    self.ScnMan.back()            
        elif key==4:
            self.do_mode(False)

            
#====================================================            
    def update(self, key):
        if key: self.do_keys(key)
        #update controls
        #self.master.update(self.SB)
        
    def on_open(self,):
        self.get_menustuff()
        self.SB.show(0)
        self.set_mode(0)
        self.update_options("Back")
    
    def on_close(self,):
        self.clr_menustuff()
        self.master.MQ.append((self.master.Save_settings,self.save_opt))
            
        