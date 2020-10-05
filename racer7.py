import random, datetime, math
from operator import itemgetter

# Add Weather into races and its affects
# Build out an AI for pit stops
# Create some distance between people and make it more challenging to pass
def resetDriverScores(race):
    for driver in drivers:
        driver["Time"] = 0
        driver["TireWear"] = 100
        driver["TireType"] = "Soft"
        driver["StopCount"] = 0
        driver["RetiredYn"] = 0
        driver["LastSegmentTime"] = 0
        driver["TireChoices"] = ""
        driver["Results"][race["Name"]] = {}

def lightOrHeavyRain():
    chance = random.randrange(1,7)
    if(chance < 5):
        return "lightrain"
    else:
        return "heavyrain"

def checkSkyConditions(chanceOfRainToday):
    chance = random.randrange(1,7)
    chanceOfClouds = 1
    if(chanceOfRainToday == 1):
        chanceOfRainToday += 2

    if(chance < chanceOfRainToday):
        return "cloudy"
    else:
        return "clear"

def calculateWeather(race):
    weatherForecast = []
    rainPossible = 0
    rainChance = regionWeatherRules[race["Region"]]["RainChance"][race["Month"]-1]

    #Check if there will be rain today
    rainRoll = random.randrange(1,101)

    #We can have a possibility of rain
    if(rainChance < rainRoll):
        rainPossible = 1
    
    rainLastLap = 0
    rainingAtStartOfRace = random.randrange(1,7)

    priorLapWeather = ""
    for i in range(race['Laps']):
        forecast = ""
        allowChange = 0
        if(i == 0 and rainingAtStartOfRace < 3 and rainPossible == 1):
            forecast = lightOrHeavyRain()
        # If it is already raining we check to see if it keeps raining
        elif(priorLapWeather == "lightrain" or priorLapWeather == "heavyrain"):
            isItStillRaining = random.randrange(1,7)
            if(isItStillRaining <= 5):
                forecast = lightOrHeavyRain()
            else:
                forecast = "cloudy"
        # See if it is going to start raining again
        elif(rainPossible == 1):
            willTheRainOpenBackUp = random.randrange(1,7)
            if(willTheRainOpenBackUp <= 2):
                forecast = lightOrHeavyRain()
            else:
                forecast = checkSkyConditions(rainPossible)
        elif(rainPossible == 0):
            forecast = checkSkyConditions(rainPossible)
        
        #This function should really be recursive
        # Lets check to see if the weather actually changes, we do not want crazy differences from lap to lap since the time is low
        if(i != 0):
            weatherChangeCheck = random.randrange(1,7)
            if(weatherChangeCheck <= 5):
                forecast = priorLapWeather

        priorLapWeather = forecast
        weatherForecast.append(forecast)

    race["WeatherForecast"] = weatherForecast
    return weatherForecast

def checkYellowFlag(race):
    YellowFlagYn = race["YellowFlagYn"]
    if(YellowFlagYn == 1):
        yellowFlagRoll = random.randrange(1,7)
        if(yellowFlagRoll > 3):
            YellowFlagYn = 0
        else:
            race["LapUnderYellow"] += 1


def assignStartTireForRace(race, racers):
    i = 0
    for driver in racers:
        driver["TireType"] = chooseTire(race, driver, 0, i)
        i += 1

def doIHaveTheRightTire(driver, race, lapNumber):
    currentWeather = race["WeatherForecast"][lapNumber]
    if(lapNumber + 1 != race['Laps']):
        nextWeather    = race["WeatherForecast"][lapNumber + 1]
    else:
        nextWeather = currentWeather

    currentTire    = driver["TireType"]
    correctTire = 1
    if((nextWeather == "cloudy" or nextWeather == "clear") and (currentTire == "Wet" or currentTire == "Intermediate")):
        correctTire = 0
    elif((nextWeather == "lightrain" or nextWeather == "heavyrain") and (currentTire != "Wet" and currentTire != "Intermediate")):
        correctTire = 0

    #If our team is terrible at forecasting
    teamForecastCheck = random.randrange(1,7)
    if(teamForecastCheck > driver["Team"]["Forecasting"]):
        correctTire = 1

    return correctTire


def pitStop(driver, race, lapCount, position):
    pitAdditionalTime = 0
    #Take the drivers tempurment into affect here, will they stay out?!
    temperTest = random.randrange(1,7)
    # No matter how pissed off you are you won't stay out on bad tires
    if(driver["TireWear"] < 3):
        temperTest = 1
    if(temperTest <= driver["Driver"]["Tempurment"]):
        # print("Pit Start " + str(pitAdditionalTime))
        # Pit - Add our variance
        pitAdditionalTime += race["Pit"]["BasePitTime"]
        # Add pit lap time variances
        pitAdditionalTime += random.randrange(0,3)
        # Add Base Pit Time
        pitAdditionalTime += 2
        # Check for Pit crew skill
        pitCrewSkillCheck = random.randrange(1,6)
        # See if they failed this test
        if(pitCrewSkillCheck > driver["Team"]["PitSkill"]):
            pitAdditionalTime += random.randrange(0,4)
        #Reset Tires
        driver["TireWear"] = 100
        
        #Figure out what tire to put on here.
        driver["TireType"] = chooseTire(race, driver, lapCount, position)
        
        driver["StopCount"] += 1

        #print("I pitted time " + str(pitAdditionalTime) + " New Tire " + driver["TireType"])

        #Update our drivers current time
        driver["CurrentLapTime"] += pitAdditionalTime
        driver["LastSegmentTime"] = pitAdditionalTime

def chooseTire(race, driver, lapCount, position):
    tireType = ""

    currentWeather = race["WeatherForecast"][lapCount]
    if(lapCount + 1 != race["Laps"]):
        nextWeather = race["WeatherForecast"][lapCount + 1]
    else:
        nextWeather = currentWeather
    idealTire = weather[nextWeather]["IdealTire"]
    # On the first lap we are going to put on whatever tire is ideal given the weather type
    if(lapCount == 0):
        tireType = idealTire
    else:
        # If the ideal tire would be soft then we can choose our options based on other factors
        if(idealTire == "Soft"):
            #Going to allow the AI to kind of guess at this one
            tireRoll = random.randrange(1,7)
            if(tireRoll > 3):
                tireType = "Medium"
            else:
                tireType = "Hard"
        #If it is not soft we will go with the ideal for now
        else:
            tireType = idealTire

    
    driver["TireChoices"] += " " + tires[tireType]["Abbreviation"] + "("+ str(lapCount) +")"
    
    return tireType

# Handles printing, also accumulating points for championship (should be another function)
def printRaceResults(race, drivers):

    drivers = sorted(drivers, key=itemgetter('Time'))

    polePosition = 1
    print( race["Name"] + " Results")
    print("Race Time Range ("+ str(datetime.timedelta(seconds=race["FastTotalTime"])) +" - "+ str(datetime.timedelta(seconds=race["SlowTotalTime"])) +")")
    print("Lap Time Range ("+ str(datetime.timedelta(seconds=race["FastestLap"])) +" - "+ str(datetime.timedelta(seconds=race["SlowestLap"])) +")")
    print("Laps Under Yellow:" + str(race["LapUnderYellow"]))
    print("-------------")
    for driver in drivers:
        if polePosition < len(points):
            driver["Championship"] += points[polePosition - 1]

        if(driver["RetiredYn"] == 1):
            displayPolePosition = "DNF"
            displayTime = ""
        else:
            displayPolePosition = str(polePosition)
            displayTime = str(datetime.timedelta(seconds=driver["Time"]))

        print(displayPolePosition + '\t' + driver["Name"] + ' ('+ driver["Make"] +') \t\t@' + displayTime + ' \t S('+ str(driver["StopCount"]) +') \t O('+ str(driver["OvertakeCount"]) +') \t Tires: '+ driver["TireChoices"] +' \tPoints:' + str(driver["Championship"]))
        polePosition +=1
    
    print("     ")

def raceSegment(race, lapNumber, segment, drivers, currentWeather):
    weatherSpeedReduction = currentWeather["SpeedReduction"]
    driverIterator = 0

    #Get Segment Details
    segmentBonus = segment["PassModifier"]
    segmentTest = segment["Test"]
    segmentFastTime = segment["LowTime"]
    segmentSlowTime = segment["HighTime"]
    segmentCarTest = segment["CarTest"]
    segmentDRS   = segment["DRSInSegment"]

    #Modify times for the weather
    segmentFastTime += math.floor(segmentFastTime * weatherSpeedReduction / 100)
    segmentSlowTime += math.floor(segmentSlowTime * weatherSpeedReduction / 100)

    for driver in drivers:
        if(driver["RetiredYn"] == 0):
            currentSegmentTime = 0

            # This is some details about our tires
            NormalTireWear =        tires[driver["TireType"]]["NormalWear"]
            NormalPitRangeStart =   tires[driver["TireType"]]["NormalPitRangeStart"]
            CriticalErrorTireWear = tires[driver["TireType"]]["CriticalErrorTireWear"]
            ReductionThreshold  =   tires[driver["TireType"]]["ReductionThreshold"]
            
            # If this is a yellow flag then everyone slows down
            if(race["YellowFlagYn"] == 1):
                currentSegmentTime = segmentSlowTime
            else:
                # Look at the driver in front of me, is he within the fastest time? 
                # f so I use my overtake skill to try to get a better time then him
                if(driverIterator != 0):
                    driverAheadSegmentTime = drivers[driverIterator - 1]["LastSegmentTime"]
                    driverAheadTime = drivers[driverIterator -1]["Time"]
                    myCurrentTime = driver["Time"]

                    timeDifference = myCurrentTime - driverAheadTime

                    if(timeDifference <= segmentFastTime):
                        #Do a test against the drivers overtakes
                        currentDriverOvertake = driver["Driver"]["Overtake"]
                        #Modify our currentdriverovertake score if DRS is enabled and in this segment
                        if(segmentDRS == 1 and race["DRSEnabled"] == 1):
                            currentDriverOvertake += 2

                        previousDriverOvertake = drivers[driverIterator -1]["Driver"]["Overtake"]
                        testOvertake = random.randrange(1,7)
                        if(currentDriverOvertake < testOvertake and previousDriverOvertake > testOvertake):
                            segmentFastTime = driverAheadSegmentTime - 5
                            driver["OvertakeCount"] += 1

                if(segmentFastTime >= segmentSlowTime):
                    segmentSlowTime = segmentFastTime + 1

                # All drivers will get a normalized speed here...
                score = random.randrange(segmentFastTime, segmentSlowTime)
                currentSegmentTime += score
                
                #Test our drivers skill for this section of the course
                # This is where individual skill versus the track comes in handy
                driverSkillCheck = driver["Driver"][segmentTest]
                carSkillCheck = driver["Car"][segmentCarTest]

                testDriverRoll = random.randrange(1,7)
                testCarRoll    = random.randrange(1,7)

                # If the tire wear is below the reduction threshold we check to see if we get bonus
                if(driver["TireWear"] < ReductionThreshold):
                    allowDriverToIncreaseSpeed = 0
                    carSkillCheckReduction = 2
                else:
                    allowDriverToIncreaseSpeed = 1
                    carSkillCheckReduction = 0

                if(allowDriverToIncreaseSpeed == 1):
                    if(testDriverRoll <= driverSkillCheck):
                        currentSegmentTime -= segmentBonus
                    # If this is a 6 and the driver does not have a 6 skill check our tires got a little more messed up
                    elif(testDriverRoll == 6 and driverSkillCheck != 6):
                        currentSegmentTime += segmentBonus

                # Do a car check against the course
                if(testCarRoll + carSkillCheckReduction <= carSkillCheck):
                    currentSegmentTime -= segmentBonus
                elif(testCarRoll == 6 and carSkillCheck != 6):
                    currentSegmentTime += segmentBonus
                    driver["TireWear"] -= CriticalErrorTireWear

                    # Do a reliability roll here to see if the car just takes a shit and is DNF
                    testEngineHiccup = random.randrange(1,7)
                    # If we fail our engine hiccup
                    if(testEngineHiccup > 5):
                        # Test to see if the engine messed up
                        engineReliabilityRoll = random.randrange(1,101)
                        # if it is higher then we have an issue
                        if(engineReliabilityRoll > driver["Car"]["EngineReliability"]):
                            testDNF = random.randrange(1,7)
                            # There is a slight chance that this means that we are disqualified
                            if(testDNF == 6):
                                driver["RetiredYn"] = 1
                                # There is another chance that we smash so hard into a wall that it forces a yellow flag
                                testYellowFlagGo = random.randrange(1,7)
                                if(testYellowFlagGo >= 5):
                                    race["YellowFlagYn"] = 1
                else:
                    currentSegmentTime += segmentBonus

            #Accumulate driver details
            driver["CurrentLapTime"] += currentSegmentTime
            driver["LastSegmentTime"] = currentSegmentTime
        else:
            driver["CurrentLapTime"] = 9999
            driver["LastSegmentTime"] = 9999
        driverIterator += 1

def performRace(race, drivers):
    #Get the weather forecast for the race
    weatherForceast = calculateWeather(race)
    #Reset all of our scores to 0
    resetDriverScores(race)

    #Assign the correct tire based on the race
    assignStartTireForRace(race,drivers)

    # Run our race
    for i in range(race["Laps"]):
        # Check to see if yellow has a chance of going away
        checkYellowFlag(race)

        #Get our weather details
        currentWeather = weather[weatherForceast[i]]
        
        for segment in race["Segments"]:
            raceSegment(race, i, segment, drivers, currentWeather)

        # Accumulate driver details and reset other details
        driverIterator = 0 
        for driver in drivers:
            if(driver["RetiredYn"] == 0):
                #At end of lap we test if we took a pit stop
                allowPitStop = 0
                if(driver["TireWear"] < tires[driver["TireType"]]["NormalPitRangeStart"]):
                    allowPitStop = 1
                elif(doIHaveTheRightTire(driver, race, i) == 0):
                    allowPitStop = 1
                
                if(allowPitStop == 1):
                    pitStop(driver, race, i, driverIterator)

            # Update our tire wear with our normal tire wear at the end of the lap
            driver["TireWear"]                      -= tires[driver["TireType"]]["NormalWear"]
            driver["Time"]                          += driver["CurrentLapTime"]
           # print(driver["Name"] + '#'+ str(i) +' Lap time : ' + str(datetime.timedelta(seconds=driver["CurrentLapTime"])) +  ' Total time : ' + str(datetime.timedelta(seconds=driver["Time"])) +  ' Tire Wear:' + str(driver["TireWear"]) + "("+ driver["TireType"] +")")

            driver["CurrentLapTime"]                = 0
            driver["Results"][race["Name"]][i]      = {}
            driver["Results"][race["Name"]][i]["LapTime"] = driver["CurrentLapTime"]
            driver["Results"][race["Name"]][i]["TireWear"] = driver["TireWear"]
            driver["Results"][race["Name"]][i]["CurrentTire"] = driver["TireType"]
            if(driver["RetiredYn"] == 1):
                driver["Time"] = 99999999999

            driverIterator += 1

        # Sort our drivers for the next lap, this allows us to know who is in 1,2,3 etc
        drivers = sorted(drivers, key=itemgetter('Time'))
        if(race["AllowDRSOnLap"] >= i):
            race["DRSEnabled"] = 1

    #Accumulate championship points
    printRaceResults(race, drivers)


def accumulateRaceState(race):
    for segment in race["Segments"]:
        race["FastestLap"] += segment["LowTime"]
        race["SlowestLap"] += segment["HighTime"]
    race["FastTotalTime"] = race["FastestLap"] * race["Laps"]
    race["SlowTotalTime"] = race["SlowestLap"] * race["Laps"]

# Get our drivers setup
drivers = [ 
            {"Name":"Lewis Hamlton",        "Make":"Mercades",       "Driver": {"Steering":5, "Cornering":5, "Tempurment":4, "Overtake":4}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":6, "EngineReliability":98}, "Team":{"PitSkill":6, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Valtteri Bottas",      "Make":"Mercades",       "Driver": {"Steering":5, "Cornering":4, "Tempurment":6, "Overtake":4}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":6, "EngineReliability":98}, "Team":{"PitSkill":6, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Sebastian Vettel",     "Make":"Ferrari",        "Driver": {"Steering":5, "Cornering":5, "Tempurment":3, "Overtake":4}, "Car": {"Acceleration":6, "Cornering":6, "Suspension":5, "EngineReliability":98}, "Team":{"PitSkill":6, "Forecasting":4}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Charles Leclerc",      "Make":"Ferrari",        "Driver": {"Steering":5, "Cornering":4, "Tempurment":5, "Overtake":4}, "Car": {"Acceleration":6, "Cornering":6, "Suspension":5, "EngineReliability":96}, "Team":{"PitSkill":6, "Forecasting":4}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Alex Albon",           "Make":"Red Bull",       "Driver": {"Steering":5, "Cornering":4, "Tempurment":6, "Overtake":6}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":5, "EngineReliability":95}, "Team":{"PitSkill":6, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Max Verstappen",       "Make":"Red Bull",       "Driver": {"Steering":5, "Cornering":5, "Tempurment":4, "Overtake":5}, "Car": {"Acceleration":6, "Cornering":5, "Suspension":5, "EngineReliability":95}, "Team":{"PitSkill":6, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Lando Norris",         "Make":"McLaren",        "Driver": {"Steering":6, "Cornering":4, "Tempurment":5, "Overtake":4}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":4, "EngineReliability":95}, "Team":{"PitSkill":5, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Carlos Sainz",         "Make":"McLaren",        "Driver": {"Steering":5, "Cornering":4, "Tempurment":5, "Overtake":3}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":4, "EngineReliability":95}, "Team":{"PitSkill":5, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Daniel Ricciardo",     "Make":"Renault",        "Driver": {"Steering":3, "Cornering":4, "Tempurment":3, "Overtake":4}, "Car": {"Acceleration":5, "Cornering":4, "Suspension":4, "EngineReliability":95}, "Team":{"PitSkill":5, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Esteban Ocon",         "Make":"Renault",        "Driver": {"Steering":4, "Cornering":3, "Tempurment":5, "Overtake":5}, "Car": {"Acceleration":5, "Cornering":4, "Suspension":4, "EngineReliability":95}, "Team":{"PitSkill":4, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Pierre Gasly",         "Make":"AlphaTauri",     "Driver": {"Steering":3, "Cornering":4, "Tempurment":5, "Overtake":4}, "Car": {"Acceleration":5, "Cornering":3, "Suspension":5, "EngineReliability":94}, "Team":{"PitSkill":4, "Forecasting":6}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Daniil Kvyat",         "Make":"AlphaTauri",     "Driver": {"Steering":4, "Cornering":3, "Tempurment":5, "Overtake":3}, "Car": {"Acceleration":5, "Cornering":3, "Suspension":4, "EngineReliability":93}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Sergio Perez",         "Make":"Racing Point",   "Driver": {"Steering":3, "Cornering":3, "Tempurment":4, "Overtake":6}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":4, "EngineReliability":92}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Lance Stroll",         "Make":"Racing Point",   "Driver": {"Steering":4, "Cornering":5, "Tempurment":5, "Overtake":6}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":5, "EngineReliability":91}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Kimi Raikkonen",       "Make":"Alfa Romeo",     "Driver": {"Steering":2, "Cornering":2, "Tempurment":2, "Overtake":4}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":3, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":4}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Antonio Giovinazzi",   "Make":"Alfa Romeo",     "Driver": {"Steering":5, "Cornering":2, "Tempurment":5, "Overtake":3}, "Car": {"Acceleration":5, "Cornering":5, "Suspension":4, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":4}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Romain Grosjean",      "Make":"Haas",           "Driver": {"Steering":2, "Cornering":6, "Tempurment":3, "Overtake":4}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":5, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Kevin Magnussen",      "Make":"Haas",           "Driver": {"Steering":4, "Cornering":2, "Tempurment":4, "Overtake":3}, "Car": {"Acceleration":4, "Cornering":4, "Suspension":3, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"George Russell",       "Make":"Williams",       "Driver": {"Steering":2, "Cornering":4, "Tempurment":5, "Overtake":3}, "Car": {"Acceleration":3, "Cornering":3, "Suspension":3, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
            {"Name":"Nicholas Latifi",      "Make":"Williams",       "Driver": {"Steering":3, "Cornering":2, "Tempurment":5, "Overtake":4}, "Car": {"Acceleration":3, "Cornering":3, "Suspension":3, "EngineReliability":90}, "Team":{"PitSkill":4, "Forecasting":5}, "TireType":"Soft",  "TireWear": 100, "Time":0, "CurrentLapTime": 0,"LastSegmentTime":0,"RetiredYn": 0, "OvertakeCount":0,"StopCount":0, "Championship":0, "TireChoices":"", "Results":{}},
          ]
races = [   {"Name":"Austrian Grand Prix",                  "Laps":71, "FastestLap":0.00,"DRSEnabled":0, "AllowDRSOnLap":3, "YellowFlagYn" : 0,"LapUnderYellow":0, "Month":7, "Region":"Central Europe","SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Pit":{"BasePitTime":25}, "Segments":[{"DRSInSegment":1, "PassModifier":5, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":32, "HighTime":39},   {"DRSInSegment":0,"PassModifier":4,  "Test":"Cornering", "CarTest":"Cornering",  "LowTime":19, "HighTime":25},        {"DRSInSegment":0, "PassModifier":6, "CarTest":"Suspension", "Test":"Cornering",  "LowTime":43, "HighTime":52}]},
            {"Name":"Steirermark Grand Prix",               "Laps":71, "FastestLap":0.00,"DRSEnabled":0, "AllowDRSOnLap":3, "YellowFlagYn" : 0,"LapUnderYellow":0, "Month":7, "Region":"Central Europe","SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00, "Pit":{"BasePitTime":25}, "Segments":[{"DRSInSegment":1, "PassModifier":5, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":32, "HighTime":39},   {"DRSInSegment":0,"PassModifier":4,  "Test":"Cornering", "CarTest":"Cornering",  "LowTime":19, "HighTime":25},        {"DRSInSegment":0, "PassModifier":6, "CarTest":"Suspension", "Test":"Cornering",  "LowTime":43, "HighTime":52}]}, 
            {"Name":"Hungarian Grand Prix",                 "Laps":70, "FastestLap":0.00,"DRSEnabled":0, "AllowDRSOnLap":3, "YellowFlagYn" : 0,"LapUnderYellow":0, "Month":7, "Region":"Central Europe","SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00,"Pit":{"BasePitTime":35}, "Segments":[{"DRSInSegment":0, "PassModifier":2, "Test":"Steering", "CarTest":"Cornering", "LowTime":50, "HighTime":56},   {"DRSInSegment":1,"PassModifier":2, "Test":"Cornering",   "CarTest":"Acceleration",  "LowTime":43, "HighTime":49},        {"DRSInSegment":0, "PassModifier":1, "CarTest":"Suspension", "Test":"Steering",   "LowTime":63, "HighTime":69}]}, 
            {"Name":"British Grand Prix",                   "Laps":52, "FastestLap":0.00,"DRSEnabled":0, "AllowDRSOnLap":3, "YellowFlagYn" : 0,"LapUnderYellow":0, "Month":8, "Region":"British Isles","SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00,"Pit":{"BasePitTime":20}, "Segments":[{"DRSInSegment":0, "PassModifier":2, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":23, "HighTime":29},   {"DRSInSegment":1,"PassModifier":3,  "Test":"Cornering", "CarTest":"Suspension",  "LowTime":43, "HighTime":53},        {"DRSInSegment":0, "PassModifier":3, "CarTest":"Cornering", "Test":"Steering",   "LowTime":24, "HighTime":32}]},
            {"Name":"70th Anniversary Grand Prix",          "Laps":52, "FastestLap":0.00,"DRSEnabled":0, "AllowDRSOnLap":3, "YellowFlagYn" : 0,"LapUnderYellow":0, "Month":8, "Region":"British Isles","SlowestLap":0.00, "FastTotalTime":0.00, "SlowTotalTime":0.00,"Pit":{"BasePitTime":20}, "Segments":[{"DRSInSegment":0, "PassModifier":2, "Test":"Steering", "CarTest":"Acceleration",  "LowTime":23, "HighTime":29},   {"DRSInSegment":1,"PassModifier":3,  "Test":"Cornering", "CarTest":"Suspension",  "LowTime":43, "HighTime":53},        {"DRSInSegment":0, "PassModifier":3, "CarTest":"Cornering", "Test":"Steering",   "LowTime":24, "HighTime":32}]},
        ]
points = [25,18,15,12,10,8,6,4,2,1]
tires  = {  
            # NormalWear - For each lap how much are we reducing this?
            # SuccessBonus - When we succeed on a sector what is the maximum we can gain from that section
            # Reduction Threshold - This is the point where tires start to reduce the possibility of getting a bonus
            # NormalPitRangeStart - When does the game start thinking about a pit stop?
            "Soft"          :  {"NormalWear":2,   "SuccessBonus":4, "ReductionThreshold":50,     "NormalPitRangeStart":50, "CriticalErrorTireWear" : 3, "Abbreviation":"S"},
            "Medium"        :  {"NormalWear":1.5, "SuccessBonus":3, "ReductionThreshold":35,     "NormalPitRangeStart":25, "CriticalErrorTireWear" : 2, "Abbreviation":"M"},
            "Hard"          :  {"NormalWear":1,   "SuccessBonus":2, "ReductionThreshold":25,     "NormalPitRangeStart":10, "CriticalErrorTireWear" : 1, "Abbreviation":"H"},
            "Wet"           :  {"NormalWear":.25, "SuccessBonus":1, "ReductionThreshold":15,     "NormalPitRangeStart":15, "CriticalErrorTireWear" : 1, "Abbreviation":"W"},
            "Intermediate"  :  {"NormalWear":.50, "SuccessBonus":1, "ReductionThreshold":25,     "NormalPitRangeStart":25, "CriticalErrorTireWear" : 1, "Abbreviation":"I"},
        }
# Ideal tire will tell the racers what they should most likely start on
# Speed reduction is what % we are going to reduce the lowest/highest item by
weather = {
    "lightrain"     : {"Name":"Light Rain", "IdealTire":"Intermediate", "SpeedReduction":60},
    "heavyrain"     : {"Name":"Heavy Rain", "IdealTire":"Wet",          "SpeedReduction":85},
    "cloudy"        : {"Name":"Cloudy",     "IdealTire":"Soft",         "SpeedReduction":10},
    "clear"         : {"Name":"Clear",      "IdealTire":"Soft",         "SpeedReduction":0}
}
regionWeatherRules = {
    # Rain chance tells us that during this month we expect an X percentage chance that there will be rain on this day.
    # High Tempature is in F
    "Central Europe" : {"RainChance":[15,15,15,15,25,20,15,15,10,10,20,20], "HighTempature":[38,43,53,63,73,78,82,82,73,62,49,40]},
    "British Isles"  : {"RainChance":[40,30,30,30,27,27,25,25,27,33,33,33], "HighTempature":[48,49,53,59,65,70,74,73,67,60,53,48]}
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
    