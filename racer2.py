import random
from operator import itemgetter

# This itteration allows for multiple races to be run

def resetDriverScores():
    for driver in drivers:
        driver["Score"] = 0

def performRace(race, drivers):
    #Reset all of our scores to 0
    resetDriverScores()

    # Run our race
    for i in range(race["Laps"]):
        for driver in drivers:
            score = random.randrange(1,6)
            driver["Score"] += score

    # Update our Championship points
    drivers = sorted(drivers, key=itemgetter('Score'))
    
    #Accumulate championship points
    polePosition = 1
    print( race["Name"] + " Results ")
    print("-------------")
    for driver in drivers:
        if polePosition < len(points):
            driver["Championship"] += points[polePosition - 1]
        print(str(polePosition) + ' ' + driver["Name"] + ' ('+ driver["Car"] +') @' + str(driver["Score"]) + ' Points:' + str(driver["Championship"]))
        polePosition +=1
    
    print("     ")

# Get our drivers setup
drivers = [ 
            {"Name":"Enzo Ferrari", "Car":"Ferrari", "Score":0, "Championship":0, "Results":{}},
            {"Name":"Albert Guyot", "Car":"Bignan", "Score":0, "Championship":0, "Results":{}}, 
            {"Name":"Lewis Hamlton", "Car":"Mercades", "Score":0, "Championship":0, "Results":{}},
            {"Name":"Samual Botas", "Car":"Mercades", "Score":0, "Championship":0, "Results":{}}
          ]
races = [{"Name":"Monza", "Laps":63}, {"Name":"Austrilia", "Laps":55}, {"Name":"Montrel", "Laps":35}]
points = [25,18,15,12,10,8,6,4,2,1]

# Run each race and report our results
for race in races:
    performRace(race, drivers)

# Sort our drivers
champions = sorted(drivers, key=itemgetter('Championship'), reverse=True)

# Output our race results!
pole = 1
print("Championship Results")
print("-----------")
for champion in champions:
    print(str(pole) + ' - ' + champion["Name"] + ' ('+  champion["Car"] +')' + " @" + str(champion["Championship"]) )
    pole += 1
    