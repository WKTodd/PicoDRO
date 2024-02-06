#PICO DRO W.K.Todd Dec2023
#credits:
#https://github.com/pololu/pololu-3pi-2040-robot/blob/master/micropython_demo/pololu_3pi_2040_robot
#/_lib/pio_quadrature_counter.py
#[modified by wkt] adding a zero counter routine
#
#https://github.com/rdagger/micropython-ssd1322
#[modified by wkt] font import can hang on non-utf-8 characters and optional init text
#
#min version : MicroPython v1.22.1
App_Name = "Pico DRO" 
version=3.01
# DRO uses signed integer for internal position values , each bit representing 100nm
#units per millimetre = 10000
UPmm = 10000
#globals
DEBUG = False
ENCODER_PINS = [(12, 13), (16, 17), (18, 19), (14, 15),] #must be contiguous pairs 4 max
#QO_PINS = [(10,11)] #quadrature output pins

#import ROM modules
from machine import Pin, SPI,  Timer,  # UART,PWM, 
from rp2 import PIO, StateMachine
import time, gc
#import python modules
from Inifile import Inifile
from ScreenControls import Screen
from ScreenController_SSD1322 import Screen_Manager
from pio_quadrature_counter import PIOQuadratureCounter
from ADCkeyboard import ADC_Keys
from QuadratureIO import Axis #, Quop
#import screens
from AboutScreen import About_Screen
from TwoAxesScreen import TwoAxes_Screen
from OneAxisScreen import OneAxis_Screen
from MenuScreen import Menu_Screen
#===============================class development area=======================

#------------------------------end of class area------------------------
# main application
#
class DRO():
    
    MQ = [] #message cue
    
    def __init__(self, IN_PINS, Qo_PINS=None,):
        self.led = Pin(25, Pin.OUT)
        self.Ini = Inifile(master=self)
        
        self.Xaxis = Axis("X", 0, IN_PINS, 5000)
        self.Yaxis = Axis("Y", 1, IN_PINS, 2000)
        #self.Zaxis = Axis("Z", 2, IN_PINS, 2000)
        #Waxis = Axis("W", 3, ENCODER_PINS)
        #Waxis.Units="Inch"
        #self.Qout = Quop(Qo_PINS[0],2000)  
        
        self.KB= ADC_Keys(2)
        self.ScnMan = Screen_Manager()
        self.AS = About_Screen(master=self, Version = version)
        self.TAS = TwoAxes_Screen(master=self,)
        self.TAS.Axes.append(self.Xaxis)
        self.TAS.Axes.append(self.Yaxis)
        self.OAS = OneAxis_Screen(master=self,)
        self.OAS.Axes.append(self.Xaxis)
        self.OAS.Axes.append(self.Yaxis)
        
        self.MNUS = Menu_Screen(master=self,)
        
        self.ScnMan.add_screen(self.AS)
        self.ScnMan.add_screen(self.TAS)
        self.ScnMan.add_screen(self.OAS)
        self.ScnMan.add_screen(self.MNUS)
        self.ScnMan.display.clear()
        self.set_res()
        
    def Save_settings(self, opt):
        self.Ini.save(opt) #opt = 0 save , opt=1 discard
        #update  resolutions settings etc.
        self.set_res()
        
    def set_res(self):        
        self.Xaxis.PPU = self.Ini.MS["xres"]
        self.Xaxis.Dir = self.Ini.MS["xdir"]
        self.Xaxis.Dia = self.Ini.MS["xdia"]
        self.Yaxis.PPU = self.Ini.MS["yres"]
        self.Yaxis.Dir = self.Ini.MS["ydir"]
        self.Yaxis.Dia = self.Ini.MS["ydia"]
        #self.Qout.PPU = self.Ini.MS["qres"]
        #self.Qout.function = self.Ini.MS["qout"]
             
    def Run(self,):

        self.ScnMan.show("About")
        time.sleep(3)
        self.ScnMan.show("XY")
        #self.ScnMan.show("woodworker")
        
        while True:
            #main loop
            self.led.toggle() #heart beat led
            #do message cue
            if len(self.MQ) >0:
                Fn = self.MQ.pop(0)
                if type(Fn) is tuple:
                    #Fn=(function,params)
                    Fn[0](Fn[1])
                else:
                    #Fn=function
                    Fn()
            
            key, V = self.KB.get_key()
            if key == 8:
                if self.ScnMan.Cur_scn !="Menu": #don't show twice
                    self.ScnMan.show("Menu")
                    
            if key == 7:
                if self.ScnMan.Cur_scn !="woodworker": 
                    self.ScnMan.show("woodworker")
                else:
                    self.ScnMan.show("XY")
                    
            if key:print(key,V)
            #Update screen
            self.ScnMan.update_screen(key)
            #Qout.set_intpos(Xaxis.get_intpos(), Yaxis.get_intpos())
            gc.collect()
            
            
   
#============================
# define and run the application
Dro = DRO(ENCODER_PINS,)
Dro.Run()

