from rp2 import PIO, StateMachine
import time
from pio_quadrature_counter import PIOQuadratureCounter
from machine import Pin, Timer

class Axis():
    '''Name: X Y Z etc.
SM= state machine number 0,1,2,3
ENCODER_PINS =  list of contiguous pairs of pins (tuples) '''

    def __init__(self, name, SM, ENCODER_PINS, PPU):
        self.name = name        
        self.Ch =PIOQuadratureCounter(SM,ENCODER_PINS[SM][0],ENCODER_PINS[SM][1])
        self.Ch.SetZero()
        self.PPU = PPU
        self.ZeroPos =0
        self.Units="mm"
        self.Dir = 1
        self.Dia = 0 #display as diameter

        
    def get_intpos(self):
        '''return internal position (x100nm) - integer'''
        return UPmm // self.PPU * self.Ch.read() 
        
    def Get_Pos(self, Inch = False):
        '''return value in units (mm/inch) - float'''
        P = (1+self.Dia) * self.Dir * (self.Ch.read() - self.ZeroPos) / self.PPU
        if Inch or self.Units=="Inch":
            return P/25.4
        else:
            return P
    
    def Zero(self):
        self.ZeroPos=self.Ch.read()
        
    
class Quop():
    '''Quadrature output class
Pins = tuple (A,B) outputs '''
    Seq = ((0,0),(1,0),(1,1),(0,1))

    
    def __init__(self, Pins, PPU=10000, Qfreq=5000):
        self.Aop = Pin(Pins[0], Pin.OUT)
        self.Bop = Pin(Pins[1], Pin.OUT)
        self.PPU = PPU
        self.SlotTimer = Timer(mode=Timer.PERIODIC , freq=Qfreq, callback=self.update)
        self._SC = 0 #modulo 4
        self._count=0
        self.PPU =1
        self.position=0
        self._intpos=0
        self.function = "A+B"
        
    def set_intpos(self, A, B=0, C=0, D=0):
        if self.function:
            self._intpos= eval(self.function)
            self.position = (intpos* self.PPU) // UPmm
        
    def set_count(self, Count):
        self._count = Count
    
    def Inc_count(self):
        self._SC = (self._SC+1)%4
        self._count +=1
        
    def Dec_count(self):
        self._SC = (self._SC-1)%4
        self._count -=1
        
    def Output(self,):        
        self.Aop.value(self.Seq[self._SC][0])
        self.Bop.value(self.Seq[self._SC][1])
        
    def update(self,t):
        if self._count < self.position:
            self.Inc_count()
            self.Output()
        elif self._count > self.position:
            self.Dec_count()
            self.Output()
