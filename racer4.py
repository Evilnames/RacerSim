import random, datetime
from operator import itemgetter

#This itteration changes our scoring system to use seconds instead of random numbers
def resetDriverScores():
    for driver in drivers:
        driver["Time"] = 0

def performRace(race, drivers):
    #Reset all of our scores to 0
    resetDriverScores()

    # Run our race
    for i in range(race["Laps"]):
        for segment in race["Segments"]:

            segmentBonus = segment["PassModifier"]
            segmentTest = segment["Test"]
            segmentFastTime = segment["LowTime"]
            segmentSlowTime = segment["HighTime"]

            for driver in drivers:
                # All drivers will get a normalized speed here...
                score = random.randrange(segmentFastTime, segmentSlowTime)
                driver["Time"] += score
                
                #Test our drivers skill for this section of the course
                # This is where individual skill versus the track comes in handy
                driverSkillCheck = driver["Driver"][segmentTest]
                testRoll = random.randrange(1,6)
                if(testRoll <= driverSkillCheck):
                    driver["Time"] -= segmentBonus

    # Update our Championship points
    drivers = sorted(drivers, key=itemgetter('Time'))
    
    #Accumulate championship points
    
    polePosition = 1
    print( race["Name"] + " Results")
    print("Race Time Range ("+ str(datetime.timedelta(seconds=race["FastTotalTime"])) +" - "+ str(datetime.timedelta(seconds=race["SlowTotalTime"])) +")")
    print("Lap Time Range ("+ str(datetime.timedelta(seconds=race["FastestLap"])) +" - "+ str(datetime.timedelta(seconds=race["SlowestLap"])) +")")
    print("-------------")
    for driver in drivers:
        if polePosition < len(points):
            driver["Championship"] += points[polePosition - 1]
        print(str(polePosition) + ' ' + driver["Name"] + ' ('+ driver["Car"] +') @' + str(datetime.timedelta(seconds=driver["Time"])) + ' Points:' + str(driver["Championship"]))
        polePosition +=1
    
    print("     ")

def accumulateRaceState(race):
    for segment in race["Segments"]:
        race["FastestLap"] += segment["LowTime"]
        race["SlowestLap"] += segment["HighTime"]
    race["FastTotalTime"] = race["FastestLap"] * race["Laps"]
    race["SlowTotalTime"] = race["SlowestLap"] * race["Laps"]

# Get our drivers setup
drivers = [ 
            {"Name":"Lewis Hamlton",        "Car":"Mercades",       "Driver": {"Steering":6, "Cornering":5}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Valtteri Bottas",      "Car":"Mercades",       "Driver": {"Steering":5, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Sebastian Vettel",     "Car":"Ferrari",        "Driver": {"Steering":5, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Charles Leclerc",      "Car":"Ferrari",        "Driver": {"Steering":5, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Alex Albon",           "Car":"Red Bull",       "Driver": {"Steering":3, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Max Verstappen",       "Car":"Red Bull",       "Driver": {"Steering":5, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Lando Norris",         "Car":"McLaren",        "Driver": {"Steering":3, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Carlos Sainz ",        "Car":"McLaren",        "Driver": {"Steering":3, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Daniel Ricciardo",     "Car":"Renault",        "Driver": {"Steering":3, "Cornering":4}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Esteban Ocon",         "Car":"Renault",        "Driver": {"Steering":3, "Cornering":3}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Pierre Gasly",         "Car":"AlphaTauri",     "Driver": {"Steering":3, "Cornering":3}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Daniil Kvyat",         "Car":"AlphaTauri",     "Driver": {"Steering":3, "Cornering":3}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Sergio Perez",         "Car":"Racing Point",   "Driver": {"Steering":3, "Cornering":3}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Lance Stroll",         "Car":"Racing Point",   "Driver": {"Steering":3, "Cornering":3}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Kimi Raikkonen",       "Car":"Alfa Romeo",     "Driver": {"Steering":2, "Cornering":2}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Antonio Giovinazzi",   "Car":"Alfa Romeo",     "Driver": {"Steering":2, "Cornering":2}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Romain Grosjean",      "Car":"Haas",           "Driver": {"Steering":2, "Cornering":2}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Kevin Magnussen",      "Car":"Haas",           "Driver": {"Steering":2, "Cornering":2}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"George Russell",       "Car":"Williams",       "Driver": {"Steering":2, "Cornering":1}, "Time":0, "Championship":0, "Results":{}},
            {"Name":"Nicholas Latifi",      "Car":"Williams",       "Driver": {"Steering":2, "Cornering":1}, "Time":0, "Championship":0, "Results":{}},
          ]
races = [   {"Name":"Austrian Grand Prix",          "Laps":71, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Segments":[{"PassModifier":5, "Test":"Steering",  "LowTime":32, "HighTime":45},   {"PassModifier":4,  "Test":"Cornering",  "LowTime":19, "HighTime":25},        {"PassModifier":6, "Test":"Cornering",  "LowTime":43, "HighTime":55}]}, 
            {"Name":"Hungarian Grand Prix",         "Laps":70, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Segments":[{"PassModifier":2, "Test":"Steering", "LowTime":50, "HighTime":56},   {"PassModifier":2, "Test":"Cornering",    "LowTime":43, "HighTime":49},        {"PassModifier":1, "Test":"Steering",   "LowTime":63, "HighTime":69}]}, 
            {"Name":"British Grand Prix",           "Laps":52, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Segments":[{"PassModifier":2, "Test":"Steering",  "LowTime":23, "HighTime":29},   {"PassModifier":3,  "Test":"Cornering",  "LowTime":43, "HighTime":56},        {"PassModifier":3, "Test":"Steering",   "LowTime":24, "HighTime":34}]}
        ]
points = [25,18,15,12,10,8,6,4,2,1]

# Run each race and report our results
for race in races:
    #Accumulate stats on the track
    accumulateRaceState(race)
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
    