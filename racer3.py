import random
from operator import itemgetter

# In this iteration we add in three segments with modifiers to the racers performance.  Also add in driver modifiers

def resetDriverScores():
    for driver in drivers:
        driver["Score"] = 0

def performRace(race, drivers):
    #Reset all of our scores to 0
    resetDriverScores()

    # Run our race
    for i in range(race["Laps"]):
        for segment in race["Segments"]:
            segmentBonus = segment["PassModifier"]
            segmentTest = segment["Test"]
            for driver in drivers:
                # All drivers will get a normalized speed here...
                score = random.randrange(1,6)
                driver["Score"] += score
                
                #Test our drivers skill for this section of the course
                # This is where individual skill versus the track comes in handy
                driverSkillCheck = driver["Driver"][segmentTest]
                testRoll = random.randrange(1,6)
                if(testRoll <= driverSkillCheck):
                    driver["Score"] -= segmentBonus

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
            {"Name":"Enzo Ferrari",     "Car":"Ferrari",    "Driver": {"Steering":3, "Cornering":1}, "Score":0, "Championship":0, "Results":{}},
            {"Name":"Albert Guyot",     "Car":"Bignan",     "Driver": {"Steering":2, "Cornering":2}, "Score":0, "Championship":0, "Results":{}}, 
            {"Name":"Lewis Hamlton",    "Car":"Mercades",   "Driver": {"Steering":6, "Cornering":3}, "Score":0, "Championship":0, "Results":{}},
            {"Name":"Samual Botas",     "Car":"Mercades",   "Driver": {"Steering":2, "Cornering":3}, "Score":0, "Championship":0, "Results":{}}
          ]
races = [   {"Name":"Monza",        "Laps":63, "Segments":[{"PassModifier":1, "Test":"Steering"},   {"PassModifier":1,  "Test":"Cornering"},        {"PassModifier":3, "Test":"Cornering"}]}, 
            {"Name":"Austrilia",    "Laps":55, "Segments":[{"PassModifier":2, "Test":"Cornering"},  {"PassModifier":1, "Test":"Steering"},          {"PassModifier":1, "Test":"Steering"}]}, 
            {"Name":"Montrel",      "Laps":35, "Segments":[{"PassModifier":2, "Test":"Steering"},   {"PassModifier":1,  "Test":"Cornering"},        {"PassModifier":0, "Test":"Steering"}]}
        ]
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
    