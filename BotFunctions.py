# Functions that can be used by all my bots
# Note that all comments reference the line/lines directly below them.

# importing Random to be used in the code
import random


# A function that appends to a database
def databaseappend(database, message):
    with open(database, 'a+') as data:
        data.write(message + '\n')


# A function that wipes a database
def databasewipe(database):
    open(database, 'w+').close()


# A function that makes a list of all the lines in a database and returns them
def listoflines(database):
    with open(database, 'r') as data:
        datastr = data.read()
        datalist = datastr.split('\n')
        return datalist


# A function that finds the most used phrase in a list, and the amount of times it was used, and returns that
def mostused(datalist):
    seen = {}
    for x in datalist:
        seen[x] = 0
    for x in datalist:
        if x in seen:
            seen[x] += 1
    items = sorted(seen.items(), key=lambda item: item[1], reverse=True)
    return items[0]


# A function that picks a random item from a list
def randompick(datalist):
    return random.choice(datalist)


# A function that adds 1 to a number in specific databases
def uponesummon(database):
    with open(database, 'r') as data:
        currentsummons = data.read()
    with open(database, 'w+') as data:
        newsummons = int(currentsummons) + 1
        data.write(str(newsummons))
