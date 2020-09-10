import random, datetime
from operator import itemgetter

# Adds car checks, tire wear and pit stops
def resetDriverScores(race):
    for driver in drivers:
        driver["Time"] = 0
        driver["TireWear"] = 100
        driver["TireType"] = "Soft"
        driver["StopCount"] = 0
        driver["Results"][race["Name"]] = {}

def performRace(race, drivers):
    #Reset all of our scores to 0
    resetDriverScores(race)
    # Run our race
    for i in range(race["Laps"]):
        for driver in drivers:
            currentLapTime = 0
            NormalTireWear = tires[driver["TireType"]]["NormalWear"]
            NormalPitRangeStart = tires[driver["TireType"]]["NormalPitRangeStart"]
            CriticalErrorTireWear = tires[driver["TireType"]]["CriticalErrorTireWear"]

            driver["TireWear"] -= NormalTireWear
            for segment in race["Segments"]:
                #Get Segment Details
                segmentBonus = segment["PassModifier"]
                segmentTest = segment["Test"]
                segmentFastTime = segment["LowTime"]
                segmentSlowTime = segment["HighTime"]
                segmentCarTest = segment["CarTest"]

                # All drivers will get a normalized speed here...
                score = random.randrange(segmentFastTime, segmentSlowTime)
                currentLapTime += score
                
                #Test our drivers skill for this section of the course
                # This is where individual skill versus the track comes in handy
                driverSkillCheck = driver["Driver"][segmentTest]
                carSkillCheck = driver["Car"][segmentCarTest]

                testDriverRoll = random.randrange(1,7)
                testCarRoll    = random.randrange(1,7)

                if(testDriverRoll <= driverSkillCheck):
                    currentLapTime -= segmentBonus
                # If this is a 6 and the driver does not have a 6 skill check our tires got a little more messed up
                elif(testDriverRoll == 6 and driverSkillCheck != 6):
                    currentLapTime += segmentBonus

                # Do a car check against the course
                if(testCarRoll <= carSkillCheck):
                    currentLapTime -= segmentBonus
                elif(testCarRoll == 6 and carSkillCheck != 6):
                    currentLapTime += segmentBonus
                    driver["TireWear"] -= CriticalErrorTireWear
                else:
                    currentLapTime += segmentBonus

            # Should I pit this lap logic?
            if(driver["TireWear"] < NormalPitRangeStart):
                #Take the drivers tempurment into affect here, will they stay out?!
                temperTest = random.randrange(1,7)
                # No matter how pissed off you are you won't stay out on bad tires
                if(driver["TireWear"] < 3):
                    temperTest = 1
                if(temperTest <= driver["Driver"]["Tempurment"]):
                    # print("Pit Start " + str(currentLapTime))
                    # Pit - Add our variance
                    currentLapTime += race["Pit"]["BasePitTime"]
                    # Add pit lap time variances
                    currentLapTime += random.randrange(0,3)
                    # Add Base Pit Time
                    currentLapTime += 2
                    # Check for Pit crew skill
                    pitCrewSkillCheck = random.randrange(1,6)
                    # See if they failed this test
                    if(pitCrewSkillCheck > driver["Team"]["PitSkill"]):
                        currentLapTime += random.randrange(0,4)
                    #Reset Tires
                    driver["TireWear"] = 100
                    #Set our tires to Medium (For now)
                    driver["TireType"] = "Medium"
                    driver["StopCount"] += 1
                    # print("Pit End " + str(currentLapTime))

            driver["Time"] += currentLapTime
            driver["Results"][race["Name"]][i] = {}
            driver["Results"][race["Name"]][i]["LapTime"] = currentLapTime
            driver["Results"][race["Name"]][i]["TireWear"] = driver["TireWear"]
            driver["Results"][race["Name"]][i]["CurrentTire"] = driver["TireType"]

            #print(driver["Name"] + '#'+ str(i) +' Lap time : ' + str(datetime.timedelta(seconds=currentLapTime)) + ' Tire Wear:' + str(driver["TireWear"]) + "("+ driver["TireType"] +")")

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
        print(str(polePosition) + ' ' + driver["Name"] + ' ('+ driver["Make"] +') @' + str(datetime.timedelta(seconds=driver["Time"])) + ' ('+ str(driver["StopCount"]) +') Points:' + str(driver["Championship"]))
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
            {"Name":"Lewis Hamlton",        "Make":"Mercades",       "Driver": {"Steering":6, "Cornering":5, "Tempurment":4}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":6}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Valtteri Bottas",      "Make":"Mercades",       "Driver": {"Steering":5, "Cornering":4, "Tempurment":6}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":6}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Sebastian Vettel",     "Make":"Ferrari",        "Driver": {"Steering":5, "Cornering":4, "Tempurment":3}, "Car": {"Acceleration":6, "Cornering":6, "Suspension":5}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Charles Leclerc",      "Make":"Ferrari",        "Driver": {"Steering":5, "Cornering":4, "Tempurment":5}, "Car": {"Acceleration":6, "Cornering":6, "Suspension":5}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Alex Albon",           "Make":"Red Bull",       "Driver": {"Steering":3, "Cornering":4, "Tempurment":6}, "Car": {"Acceleration":6, "Cornering":4, "Suspension":4}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Max Verstappen",       "Make":"Red Bull",       "Driver": {"Steering":5, "Cornering":4, "Tempurment":4}, "Car": {"Acceleration":6, "Cornering":4, "Suspension":4}, "Team":{"PitSkill":6}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Lando Norris",         "Make":"McLaren",        "Driver": {"Steering":3, "Cornering":4, "Tempurment":5}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":4}, "Team":{"PitSkill":5}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Carlos Sainz",         "Make":"McLaren",        "Driver": {"Steering":3, "Cornering":4, "Tempurment":5}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":4}, "Team":{"PitSkill":5}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Daniel Ricciardo",     "Make":"Renault",        "Driver": {"Steering":3, "Cornering":4, "Tempurment":3}, "Car": {"Acceleration":5, "Cornering":4, "Suspension":4}, "Team":{"PitSkill":5}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Esteban Ocon",         "Make":"Renault",        "Driver": {"Steering":3, "Cornering":3, "Tempurment":5}, "Car": {"Acceleration":5, "Cornering":4, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Pierre Gasly",         "Make":"AlphaTauri",     "Driver": {"Steering":3, "Cornering":3, "Tempurment":5}, "Car": {"Acceleration":5, "Cornering":3, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Daniil Kvyat",         "Make":"AlphaTauri",     "Driver": {"Steering":3, "Cornering":3, "Tempurment":5}, "Car": {"Acceleration":5, "Cornering":3, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Sergio Perez",         "Make":"Racing Point",   "Driver": {"Steering":3, "Cornering":3, "Tempurment":4}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Lance Stroll",         "Make":"Racing Point",   "Driver": {"Steering":3, "Cornering":3, "Tempurment":5}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":3}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Kimi Raikkonen",       "Make":"Alfa Romeo",     "Driver": {"Steering":2, "Cornering":2, "Tempurment":2}, "Car": {"Acceleration":4, "Cornering":5, "Suspension":3}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Antonio Giovinazzi",   "Make":"Alfa Romeo",     "Driver": {"Steering":2, "Cornering":2, "Tempurment":5}, "Car": {"Acceleration":4, "Cornering":5, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Romain Grosjean",      "Make":"Haas",           "Driver": {"Steering":2, "Cornering":2, "Tempurment":3}, "Car": {"Acceleration":4, "Cornering":2, "Suspension":4}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Kevin Magnussen",      "Make":"Haas",           "Driver": {"Steering":2, "Cornering":2, "Tempurment":4}, "Car": {"Acceleration":4, "Cornering":2, "Suspension":3}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"George Russell",       "Make":"Williams",       "Driver": {"Steering":2, "Cornering":1, "Tempurment":5}, "Car": {"Acceleration":3, "Cornering":2, "Suspension":2}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
            {"Name":"Nicholas Latifi",      "Make":"Williams",       "Driver": {"Steering":2, "Cornering":1, "Tempurment":5}, "Car": {"Acceleration":3, "Cornering":2, "Suspension":2}, "Team":{"PitSkill":4}, "TireType":"Soft",  "TireWear": 100, "Time":0,"StopCount":0, "Championship":0, "Results":{}},
          ]
races = [   {"Name":"Austrian Grand Prix",          "Laps":71, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Pit":{"BasePitTime":25}, "Segments":[{"PassModifier":5, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":32, "HighTime":45},   {"PassModifier":4,  "Test":"Cornering", "CarTest":"Cornering",  "LowTime":19, "HighTime":25},        {"PassModifier":6, "CarTest":"Suspension", "Test":"Cornering",  "LowTime":43, "HighTime":55}]}, 
           {"Name":"Hungarian Grand Prix",         "Laps":70, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00,"Pit":{"BasePitTime":35}, "Segments":[{"PassModifier":2, "Test":"Steering", "CarTest":"Cornering", "LowTime":50, "HighTime":56},   {"PassModifier":2, "Test":"Cornering",   "CarTest":"Acceleration",  "LowTime":43, "HighTime":49},        {"PassModifier":1, "CarTest":"Suspension", "Test":"Steering",   "LowTime":63, "HighTime":69}]}, 
           {"Name":"British Grand Prix",           "Laps":52, "FastestLap":0.00, "SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00,"Pit":{"BasePitTime":20}, "Segments":[{"PassModifier":2, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":23, "HighTime":29},   {"PassModifier":3,  "Test":"Cornering", "CarTest":"Suspension",  "LowTime":43, "HighTime":56},        {"PassModifier":3, "CarTest":"Cornering", "Test":"Steering",   "LowTime":24, "HighTime":34}]}
        ]
points = [25,18,15,12,10,8,6,4,2,1]
tires  = {  
            # NormalWear - For each lap how much are we reducing this?
            # SuccessBonus - When we succeed on a sector what is the maximum we can gain from that section
            # Reduction Threshold - ???
            # NormalPitRangeStart - When does the game start thinking about a pit stop?
            "Soft" :    {"NormalWear":2, "SuccessBonus":4, "ReductionThreshold":45,     "NormalPitRangeStart":50, "CriticalErrorTireWear": 3},
            "Medium" :  {"NormalWear":1.5, "SuccessBonus":3, "ReductionThreshold":25,    "NormalPitRangeStart":25, "CriticalErrorTireWear" : 2},
            "Hard" :    {"NormalWear":1, "SuccessBonus":2, "ReductionThreshold":15,    "NormalPitRangeStart":10, "CriticalErrorTireWear" : 1},
        }

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
    print(str(pole) + ' - ' + champion["Name"] + ' ('+  champion["Make"] +')' + " @" + str(champion["Championship"]) )
    pole += 1
    