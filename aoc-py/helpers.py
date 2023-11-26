import os

def readday(day, year):
    home = os.environ["HOME"]
    with open(f"{home}/git/aoc/input/{year}/{day}", "r") as f:
        return f.read()

def openday(day, year): 
    home = os.environ["HOME"]
    return open(f"{home}/git/aoc/input/{year}/{day}", "r")

def readdaylines(day, year):
    return readday(day, year).splitlines()