
import json
GRADES_FILE = 'data/grades.json'

def getGrades ():
    with open(GRADES_FILE, "r") as f:
        grades =  json.load(f)
    if "Vincent" in grades and grades["Vincent"] >= 90:
        success = True
    else:
        success = False

    return grades, success