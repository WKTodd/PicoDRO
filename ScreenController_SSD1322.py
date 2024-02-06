#Screen Controller for SDD1322 and 256x64 oled  - WKT2024

from xglcd_font import XglcdFont
from machine import Pin, SPI, Timer
from ssd1322 import Display
from time import sleep_ms
from ScreenControls import Screen, Label, Frame, VScroll_box 

class Screen_Manager():
    Screens = {}
    ScnStak =[]
    Cur_scn =""
    Display = None
    fonts=[]
    
    def __init__(self,):
        spi = SPI(0, baudrate=25000000, sck=Pin(6), mosi=Pin(7))
        self.display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(3), text="Loading...")
        self.load_fonts()
        self.width = self.display.width
        self.height = self.display.height

    def add_screen(self, SCRN):
        self.Screens[SCRN.name]=SCRN
                
    def show(self, scrn_name):
        if self.Cur_scn:
            self.Screens[self.Cur_scn].on_close()
            self.ScnStak.append(self.Cur_scn)
        self.Screens[scrn_name].on_open()
        self.Cur_scn = scrn_name
        self.display.clear()
        self.refresh()
        
    def back(self):
        self.show(self.ScnStak.pop(-1))
        
    def update_screen(self, key):
            self.Screens[self.Cur_scn].update(key)
            
    def font_height(self, font):
        if font >=0:
            return self.fonts[font].height
        else:
            #defalult 8x8 font
            return 8
        
    def text_width(self, font, text):
        if font <0:
        #defalult 8x8 font
            return len(text)*8
        else:
            return self.fonts[font].measure_text(text)


    def update(self, scr_obj, Xo=0, Yo=0):
        #redraw object - modify to suit display driver
        if type(scr_obj) is Label:
            self.clear_obj(scr_obj, Xo, Yo,)
            self.refresh_Label(scr_obj, Xo, Yo,)
            
        elif type(scr_obj) is Frame :
            self.refresh_widgets(scr_obj, Xo, Yo,)
            
        elif type(scr_obj) is VScroll_box:
            #print("vscroll_box",scr_obj)            
            self.clear_obj(scr_obj)
            Xo, Yo = scr_obj.pos
            #print(scr_obj,Xo,Yo)
            for l in scr_obj.widgets:
                self.refresh_Label(l,Xo,Yo)
                
            self.display.draw_hline(scr_obj.pos[0] +Xo,
                                    scr_obj.cursor,
                                    scr_obj.width,
                                    gs=scr_obj.cursor_colour)
            self.display.draw_hline(scr_obj.pos[0] +Xo,
                                    scr_obj.cursor + scr_obj.step,scr_obj.width,
                                    gs=scr_obj.cursor_colour,)
        
        self.display.present()
        
    def clear_obj(self, scr_obj, Xo=0, Yo=0):
        self.display.fill_rectangle(
             x = scr_obj.pos[0] + Xo,
             y = scr_obj.pos[1] + Yo,
             w = scr_obj.width,
             h = scr_obj.height,
             gs=0                        
             ) 
        
    def refresh(self):
        '''refresh all'''
        #self.display.clear()
        scrn = self.Screens[self.Cur_scn]
        self.refresh_widgets(scrn)
        
    def refresh_widgets(self, container, Xoffset=0, Yoffset=0):
        #print(container)
        for w in container.widgets:
            #print(w)
            if type(w) is Label:
                self.clear_obj(w, Xoffset, Yoffset,)  
                self.refresh_Label(w, Xoffset, Yoffset,)
                
            elif type(w) is Frame:
                Xo, Yo = w.pos
                self.refresh_widgets(w, Xo, Yo,)
            
            elif type(w) is VScroll_box:
                #print(container,w)
                Xo, Yo = w.pos
                self.refresh_widgets(w, Xo, Yo,)
                self.display.draw_hline(w.pos[0],w.cursor,w.width,
                                        gs=w.cursor_colour,)
                self.display.draw_hline(w.pos[0],w.cursor+ w.step,w.width,
                                        gs=w.cursor_colour,)
                
        self.display.present()            
            
    def refresh_Label(self,w, Xo, Yo): 
        if w.border:
            self.display.draw_rectangle(
                         x = w.pos[0] + Xo,
                         y = w.pos[1] + Yo,
                         w=w.width,
                         h=w.height,
                         gs=w.border_colour                         
                         )
        if w.font==-1:
            self.display.draw_text8x8(
                                 x = w.pos[0] + w.text_loc[0] + Xo,
                                 y = w.pos[1] + w.text_loc[1] + Yo,
                                 text=w.text,
                                 gs=w.colour,
                                 )
        else:
            self.display.draw_text(
                              x=w.pos[0] + w.text_loc[0] + Xo,
                              y=w.pos[1] + w.text_loc[1] + Yo,
                              text=w.text,
                              gs=w.colour,
                              font=self.fonts[w.font],
                              invert = w.invert
                              )

        

            
    def load_fonts(self):
        #default font (-1) is 8x8 framebuffer font        
        #font = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)
        #font = XglcdFont('lib/fonts/ArcadePix9x11.c', 9, 11)
        #font = XglcdFont('lib/fonts/Roboto_18x22.c', 18, 22)
        #font = XglcdFont('lib/fonts/IBMPlexMono12x24.c', 12, 24)
        font = XglcdFont('lib/fonts/UMTruncated12x24.c', 12, 24)
        #font = XglcdFont('lib/fonts/PerfectPixel_18x25.c', 18, 25)
        #font = XglcdFont('lib/fonts/PerfectPixel_23x32.c', 23, 32)
        #font = XglcdFont('lib/fonts/Broadway17x15.c', 17, 15)
        #font = XglcdFont('lib/fonts/EspressoDolce18x24.c', 18, 24)
        #font = XglcdFont('lib/fonts/Robotron13x21.c', 13, 21)
        #font = XglcdFont('lib/fonts/Robotron7x11.c', 7, 11)
        #font2 = XglcdFont('lib/fonts/Bally5x8.c', 5, 8)
        #font2 = XglcdFont('lib/fonts/Bally7x9.c', 7, 9)
        #font2 = XglcdFont('lib/fonts/NeatoReduced5x7.c', 5, 7)
        #font2 = XglcdFont('lib/fonts/FixedFont5x8.c', 5, 8)
        self.fonts.append(font)
        
