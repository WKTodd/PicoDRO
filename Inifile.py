#inifile class to handle menu settings etc.

#import os
import json

class Inifile():
    '''Initialisation object - loads settings file etc.'''
    def __init__(self, master=None, filename="Settings"):
        self.master=master
        self.iniExt = "JSON"
        self.inifilename = filename
        self.load_set()
        
    def load_set(self):        
        
        try:
            with open(f"{self.inifilename}.{self.iniExt}") as json_file:
                self.MS = json.load(json_file)
                        
        except :
            #if no settings.json file
            from MenuSettings import Menu_Options as tempMO
            from MenuSettings import Menu_Text as tempMT
            #save as json file
            self.MS = self.extract_set(tempMT, tempMO)
            self.saveasjson(self.MS, filepath = f"{self.inifilename}.{self.iniExt}")
            
    def get_menutext(self, mkey):
        #return correct menu option text
        text=""
        from MenuSettings import Menu_Options as tempMO
        from MenuSettings import Menu_Text as tempMT
        for mnu in tempMT:
            if tempMT[mnu][2] == mkey:
                dopt = tempMT[mnu][0]
        
        for opt in tempMO[dopt]:
            if opt[1] == self.MS[mkey]:
                text = opt[0]
                
        return text
                

    def extract_set(self, DS, MO):
        #create master settings dict from options list and settings dict
        # MenuOptions[0] = list of options
        # MenuOptions[x][0] = option description string - change for language
        # MenuOptions[x][1] = internal parameter -  do not change
        #key = menu display string - change for different languages
        #key[0] = index of Menu_Options
        #key[1] = default option select
        #key[2] = internal dict key -do not change
        MS={}
        #MS = {"internal key":internal parameter,....}
        
        for K in DS:
            opt_set = DS[K][0]
            opt = DS[K][1]
            MS[DS[K][2]] = MO[opt_set][opt][1]
        
        return MS

    def saveasjson(self, ItObj , filepath=""):
        
        try:
            with open(filepath, mode = "w",) as outfile:  
                 json.dump(ItObj, outfile)                 
        except OSError as e:
            return e
        
        
    def save(self, reload):
        if reload:
            self.load_set()
        else:
            self.saveasjson(self.MS, filepath = f"{self.inifilename}.{self.iniExt}")
            
