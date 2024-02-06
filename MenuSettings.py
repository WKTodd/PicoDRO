# MenuOptions[0] = list of options
# MenuOptions[x][0] = option description string - change for language
# MenuOptions[x][1] = internal setting do not change

'''NB.  The Q output function is evaluated by the Python eval() commmand so any valid function will work.
You will have to add 'import math' to the top of the DROVxxx.py module for advanced functions.
 A = is the output of the X axis , B is the Y axis.'''

Menu_Options = (
           [("right",1),("left",-1)],
           [("radius",0),("diameter",1)],
           [("0.1um",10000),("0.5um",2000),("1um",1000),("2um",500),("5um",200)],
           [("X","X"),("Y","Y"),("K","K"),("Q","Q")],
           [("Off",""),("X","A"),("Y","B"),("X+Y","A+B"),("X-Y","A-B"),("Y-X","B-A")],
           [("1",1),("2",2),("3",3),("4",4),("5",5)],
           [("1",1),("2",2),("3",3),("4",4)],
           [("blank",0),("text",1),("symbol",2)],
           [("1/64",64),("1/32",32),("1/16",16),],
           [("off",0), ("Frc only",1),("Frc+Main",2),],
          )



#key = menu display string - change for different languages
#key[0] = index of Menu_Options
#key[1] = default option select
#key[3] = internal dict key -do not change
Menu_Text = {
            "X Direction": [0,0,"xdir"],
            "X Resolution":[2,0,"xres"],
            "X Designation":[3,0,"xdes"],
            "X Radius/Diam":[1,0,"xdia"],
            "Y Direction": [0,0,"ydir"],
            "Y Resolution":[2,0,"yres"],
            "Y Designation":[3,1,"ydes"],
            "Y Radius/Diam":[1,0,"ydia"],
            "MM Decimals":[6,3,"mmdp"],
            "Inch Decimals":[5,4,"indp"],
            "Diam display":[7,0,"ddsp"],
            "Fraction Div's":[8,0,"fdiv"],
            "Fract Hi-light":[9,0,"fhil"],
            "Q output":[4,0,"qout"],
            "Q Resolution":[2,0,"qres"],
            }

#symbols for Diameter or Radius display  (check if characters are in selected font)
raddia_symbol = ("(<-","(<->)")



