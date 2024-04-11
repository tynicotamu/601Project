import sqlite3, csv
import pandas as pd

# Query for Total Podiums
value = 'Verstappen, Sergio'
conn = sqlite3.connect("data/f1stats.db")
cursor = conn.cursor()
cursor.execute("""
SELECT COUNT(position) 
FROM results 
INNER JOIN drivers ON results.driverId = drivers.driverId 
WHERE drivers.surname = ? AND position IN (1,2,3)
GROUP BY drivers.surname""", (value.split(',')[0],))
polePositions = cursor.fetchone()

# Query for Total Wins
value = 'Hamilton, Sergio'
cursor.execute("""
SELECT COUNT(position) 
FROM results 
INNER JOIN drivers ON results.driverId = drivers.driverId 
WHERE drivers.surname = ? AND position = 1
GROUP BY drivers.surname""", (value.split(',')[0],))
totalWins = cursor.fetchone()

print(totalWins)

# Query for Last Win
value = 'Hamilton, Sergio'
cursor.execute("""
SELECT circuits.name, races.year
FROM circuits 
INNER JOIN races 
ON circuits.circuitID = races.circuitId 
INNER JOIN results
ON races.raceId = results.raceId
INNER JOIN drivers
ON results.driverID = drivers.driverId     
WHERE drivers.surname = ? AND position = 1
ORDER BY races.date DESC
""", (value.split(',')[0],))
lastWin = cursor.fetchone()

print(lastWin[0],'-', lastWin[1])

# Most won Circuit
value = 'Hamilton, Sergio'
cursor.execute("""
SELECT COUNT(circuits.name), circuits.name
FROM circuits 
INNER JOIN races 
ON circuits.circuitID = races.circuitId 
INNER JOIN results
ON races.raceId = results.raceId
INNER JOIN drivers
ON results.driverID = drivers.driverId     
WHERE drivers.surname = ? AND position = 1
GROUP BY circuits.name
ORDER BY COUNT(circuits.name) DESC
""", (value.split(',')[0],))
mostWonCircuit = cursor.fetchone()
print(mostWonCircuit)

