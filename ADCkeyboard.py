# ADC button input
# four buttons          3v3
#                        ^
#                       4k7
#   _1k___1k___1k___1k___|__ ADC
#  |    |    |    |
#  1k   1k   1k   1k
#  |    |    |    |
# sw4  sw3  sw2  sw1
#  |____|____|____|__________GND
#


from machine import ADC
from time import sleep
from ScreenController import Screen, Label, VScroll_box #etc.

class ADC_Keys():
    defaults = [11300,19000,24200,28200,8000,9000,9500,16600,17200,22700]
    
    def __init__(self, adc_pin, ):
        
        self.Adc = ADC(adc_pin)
        self.prev_key = None
        
    def keyscan(self, V, klist):
        key=None
        for I in klist:
            if V < I+250 and V>I-250:
                key = 1 + klist.index(I)
        return key
        
    def get_key(self):
        V=0
        key = None
        for I in range(10):
            V = (V + self.Adc.read_u16())//2           
        if V>40000:
            self.prev_key=None          
        elif self.prev_key == None:
            key = self.keyscan(V,self.defaults)
            self.prev_key = key
        return key, V

        
class ADCKeyCal_Screen(Screen):
    '''ADC keyboard calibration screen
    Press two or more keys at start-up to calibrate
    '''
    
    CalSeq = [
                "Release all keys",
                "Press key ",
                "Press key {A} and {B} at the same time",
                "Press keys to test",
                "Press keys in all combinations",
                "Reboot or cycle power to continue",
              ]
    
    def __init__(self, **kwargs):
        #self.my_param = kwargs.pop("my_param")
        super(ADCKeyCal_Screen, self).__init__(**kwargs)    
        self.name = "AKCal"
# these are part of screen object        
#         self.ScnMan = self.master.ScnMan #screen manager
#         self.name =  name
#         self.width = self.ScnMan.width
#         self.height = self.ScnMan.height
#         self.widgets=[] # any screen_object in here will be rendered to screen
    
        self.sequence =0
        
        self.Title  = Label( master= self.ScnMan,
                        width = self.width,
                        height = 0,
                        pos=[0,30],
                        text="Keyboard Calibration",
                        font=-1,
                        align="centre",
                        ) 
    
        self.IL = Label(master = self.ScnMan,
                        width = self.width,
                        height = 20,
                        pos=[0,0],
                        text = CalSeq[0],
                        font=-1,
                        align="centre",
                        border = 1,
                        )
    
        self.widgets.append(self.Title)
        self.widgets.append(self.IL)
        
        #self.master.KB
        
    
        
    def do_keys(self, key):
        '''process key presses'''
        if key==1:
            pass
        elif key==2:
            pass     
        elif key==3:
            pass
        elif key==4:
            pass
            

            
#====================================================            
    def update(self, key):
        if key: self.do_keys(key)
        #update controls
        
    def on_open(self,):
        #called before render
        pass
    
    def on_close(self,):
        #called prior to close
        pass



#for testing    
# if __name__ == "__main__":
#     KB= ADC_Keys(2)
# 
#     while True:
#         sleep(0.2)
#         K, V = KB.get_key()
#         if K: print(K, V)
# 