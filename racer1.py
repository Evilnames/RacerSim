import random
from operator import itemgetter

# Get our drivers setup
drivers = [{"Name":"Enzo Ferrari", "Car":"Ferrari", "Score":0},{"Name":"Albert Guyot", "Car":"Bignan", "Score":0}, {"Name":"Lewis Hamlton", "Car":"Mercades", "Score":0}]
laps = 62

# Do our race
# This is a basic race that just adds the result of 1d6 each time, its the most basic of randomness
for i in range(laps):
    for driver in drivers:
        score = random.randrange(1,6)
        driver["Score"] += score

# Sort our drivers
drivers = sorted(drivers, key=itemgetter('Score'))

# Output our race results!
pole = 1
print("Race Results")
print("-----------")
for driver in drivers:
    print(str(pole) + ' - ' + driver["Name"] + ' ('+  driver["Car"] +')' + " @" + str(driver["Score"]) )
    pole += 1
    