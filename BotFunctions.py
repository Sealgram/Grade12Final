import random
# Functions that can be used by all my bots


def databaseappend(database, message):
    with open(database, 'a+') as data:
        data.write(message + '\n')


def databasewipe(database):
    open(database, 'w+').close()


def listoflines(database):
    with open(database, 'r') as data:
        datastr = data.read()
        datalist = datastr.split('\n')
        return datalist


def mostused(datalist):
    seen = {}
    for x in datalist:
        seen[x] = 0
    for x in datalist:
        if x in seen:
            seen[x] += 1
    items = sorted(seen.items(), key=lambda item: item[1], reverse=True)
    return items[0]


def randompick(datalist):
    return random.choice(datalist)
