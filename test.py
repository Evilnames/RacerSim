import random
from operator import itemgetter

drivers = {}
drivers[0] = {"Name":"Albert Guyot", "Car":"Bignan", "Race":"D", "Winning":4, "Accident":2, "Retirement":2, "Pole":2, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[1] = {"Name":"Alfieri Maserati", "Car":"Fiat", "Race":"D", "Winning":4, "Accident":2, "Retirement":2, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[2] = {"Name":"Andre Lombard", "Car":"GN", "Race":"C", "Winning":0, "Accident":0, "Retirement":1, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[3] = {"Name":"Antonio Ascari", "Car":"Alfa Romeo", "Race":"N", "Winning":26, "Accident":2, "Retirement":4, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[4] = {"Name":"Archie Frazer Nash", "Car":"GN", "Race":"I", "Winning":14, "Accident":2, "Retirement":3, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[4] = {"Name":"Augusto Tarabusi", "Car":"SCAT", "Race":"C", "Winning":4, "Accident":1, "Retirement":3, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[5] = {"Name":"Enzo Ferrari", "Car":"Alfa Romeo", "Race":"D", "Winning":4, "Accident":2, "Retirement":2, "Pole":3, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}
drivers[6] = {"Name":"Domenico Gamboni", "Car":"Diatto", "Race":"D", "Winning":26, "Accident":3, "Retirement":3, "Pole":1, "Segment":{}, "Level":0, "Retired":0, "ChampionPoints":0}


resultTable = {}
resultTable["A"] = {"2":-5, "3":-4, "4":-3, "5":-3, "6":-2, "7":-2, "8":-1, "9":-1, "10":0, "11":0, "12":1}
resultTable["B"] = {"2":-4, "3":-3, "4":-3, "5":-2, "6":-2, "7":-1, "8":-1, "9":0, "10":0, "11":1, "12":1}
resultTable["C"] = {"2":-3, "3":-3, "4":-2, "5":-2, "6":-1, "7":-1, "8":0, "9":0, "10":1, "11":1, "12":2}
resultTable["D"] = {"2":-3, "3":-2, "4":-2, "5":-1, "6":-1, "7":0, "8":0, "9":1, "10":1, "11":2, "12":2}
resultTable["E"] = {"2":-2, "3":-2, "4":-1, "5":-1, "6":0, "7":0, "8":1, "9":1, "10":2, "11":2, "12":3}
resultTable["F"] = {"2":-2, "3":-1, "4":-1, "5":0, "6":0, "7":1, "8":1, "9":2, "10":2, "11":3, "12":3}
resultTable["G"] = {"2":-1, "3":-1, "4":0, "5":0, "6":1, "7":1, "8":2, "9":2, "10":3, "11":3, "12":4}
resultTable["H"] = {"2":-1, "3":0, "4":0, "5":1, "6":1, "7":2, "8":2, "9":3, "10":3, "11":4, "12":4}
resultTable["I"] = {"2":-0, "3":0, "4":1, "5":1, "6":2, "7":2, "8":3, "9":3, "10":4, "11":4, "12":5}
resultTable["J"] = {"2":-0, "3":1, "4":1, "5":2, "6":2, "7":3, "8":3, "9":4, "10":4, "11":5, "12":5}
resultTable["K"] = {"2":1, "3":1, "4":2, "5":2, "6":3, "7":3, "8":4, "9":4, "10":5, "11":5, "12":6}
resultTable["L"] = {"2":1, "3":2, "4":2, "5":3, "6":3, "7":4, "8":4, "9":5, "10":5, "11":6, "12":6}
resultTable["M"] = {"2":2, "3":2, "4":3, "5":3, "6":4, "7":4, "8":5, "9":5, "10":6, "11":6, "12":7}
resultTable["N"] = {"2":2, "3":3, "4":3, "5":4, "6":4, "7":5, "8":5, "9":6, "10":6, "11":7, "12":7}



# How to play
#



# First of all, for each racer you roll one 10 sided die and add the result to his/her Pole position
# propension value. The highest roll gets the Pole Position and the championship point for that, if
# available. Re-roll for ties until you obtain a starting grid.
def findPolePosition(racers):
    for driver in racers:
        # Roll 1d10
        diceRoll = random.randrange(10) + 1
        # Add Poll Position Propension Value
        poleSpot = diceRoll + racers[driver]['Pole']
        racers[driver]['PoleSpot'] = poleSpot

# Each race is divided in 8 segments and a final step. 
# So, if a driver obtains a -2 result on the Race Table on his first roll of the race,
# he reaches level -2 (gaining space), while if he obtains a +1 result he reaches level +1 (losing
# space); if the same driver on -2 level obtains a +1 on his second roll, he goes down one level,
# reaching -1, and so on for 8 segments.
def runRace(racers):
    Segments = 9

    # All drivers start on the grid start on Level 0 of the track. 
    for i in range(Segments):
        for driver in racers:
            if(racers[driver]["Retired"] == 0):
                # On each segment, you roll a die on the Race Table, according to the Race class of each driver and read the result. 
                roll1 = random.randrange(1,6)
                roll2 = random.randrange(1,6)
                roll = roll1 + roll2

                #During each segment of the race, if the driver's roll on the Race Table is a double (1-1, 2-2, and so
                #on), you have to make another roll on the Retirement Table. Note: you still have to apply the result
                #obtained on the Race Table before the roll on the Retirement Table.
                #Results on the Retirement Table could be no effect (false alarm), Accident check or Retirement
                #check. In case of a required check, you roll a 10 sided die against involved driver's required value
                #(Accident or Retirement ) and if the result is inside the given range, that driver is eliminated from the race.

                #Retirement Table (roll one 10-sided die, after a double on the Race Table)
                #0-3: No effect, 4-6: Accident Check (roll again against the Accident Value of the driver; if the result
                #is inside the given range, driver is eliminated from race (see also optional Accident rule); 7-9:
                #Retirement Check (roll again against the Retirement Value of the driver; if the result is inside the
                #given range, driver is eliminated from race)
                if(roll1 == roll2):
                    retirementRoll = random.randrange(1,10)
                    if(retirementRoll > 3 and retirementRoll < 7):
                        #Check Accidents
                        compareAccident = random.randrange(1,10)
                        if(compareAccident <= racers[driver]['Accident']):
                            racers[driver]['Retired'] = 1
                            racers[driver]["Level"] = 99 
                    elif(retirementRoll >=7):
                        compareRetirement = random.randrange(1,10)
                        # Then they are retired
                        if(compareRetirement <= racers[driver]['Retirement']):
                            racers[driver]['Retired'] = 1
                            racers[driver]["Level"] = 99

                # During the race, according to the results of their dice rolls, they gain or lose space from their starting point. 
                # Lookup our chart based on the Race Level
                score = resultTable[racers[driver]["Race"]][str(roll)]
                #Push this to our segement, and add to our level
                # Negative values are gains, while positive values are losses toward this 0 level. 
                racers[driver]["Level"] += score 
                racers[driver]["Segment"][i] = score

# Not Implemented yet
# When you have made all segment rolls for each driver (taking in account possible retirement for
# accidents or mechanical problems, that we'll discuss later), you pass to resolve the final step.
# Starting from the lower space on the grid (ie. the greater +number a driver has reached), you make a
# a final roll using the Winning instinct value for the driver, if more than one driver share the same
# space. You roll a 10 sided die and add the Winning Instinct value of the driver and the lower total
# value wins his space race. In case of the same final result, the lower starting Winning Instinct value
# prevails. In case of another tie, simply re-roll the dice for the drivers with the same starting values.
# In this way, you'll obtain the final classification for the race.



## Find pole position
findPolePosition(drivers)


##Run our Race?
runRace(drivers)

##Sort Drivers
drivers = sorted(drivers.values(), key=itemgetter('Level'))

## Output Race Results
print("Race Results")
print("-----------------------")
pole = 1
for driver in drivers:
    if(driver['Retired'] == 1):
        print("DNF : " + driver["Name"])
    else:
        print(str(pole) + ' : ' + driver["Name"] + ' ('+  driver["Car"]+') Time: ' + str(driver["Level"]))
    pole = pole + 1