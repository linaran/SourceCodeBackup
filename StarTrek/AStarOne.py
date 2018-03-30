# Heuristics: Manhattan distance to goal
universe = []


def getTeleportList(jeanLuc):
    teleporter = universe[jeanLuc[0]][jeanLuc[1]]
    retValue = []
    for i in range(0, MAXHeight):
        for j in range(0, MAXWidth):
            if teleporter == universe[i][j] and (i != jeanLuc[0] or j != jeanLuc[1]):
                retValue.append((i - jeanLuc[0], j - jeanLuc[1]))
    return retValue


def getShuttleLand(jeanLuc):
    i = j = 0
    while i != MAXHeight:
        if universe[i][j] == 'SL':
            retValue = (i - jeanLuc[0], j - jeanLuc[1])
            break
        if j + 1 == MAXWidth:
            i += 1
            j = 0
        else:
            j += 1
    else:
        print "ShuttleLand not found!"
        exit(1)
    return retValue


def getCost(element):
    if element == "P" or element == "C" or element[0] == "T" or element == "SS" or element == "SL":
        return 0
    else:
        return int(element)


def nextNodeSpecial(jeanLuc, incZero, incOne):
    nextY = jeanLuc[0] + incZero
    nextX = jeanLuc[1] + incOne
    if universe[nextY][nextX][0] == "T":
        return(
            nextY,
            nextX,
            jeanLuc[2] + abs(incZero) + abs(incOne),
            abs(goal[0] - nextY) + abs(goal[1] - nextX),
            jeanLuc
        )
    elif universe[nextY][nextX] == "SL":
        return(
            nextY,
            nextX,
            jeanLuc[2] + 3*(abs(incZero) + abs(incOne)),
            abs(goal[0] - nextY) + abs(goal[1] - nextX),
            jeanLuc
        )


# getCost is important!
def nextNodeWalk(jeanLuc, incZero, incOne):
    nextY = jeanLuc[0] + incZero
    nextX = jeanLuc[1] + incOne
    return(
        nextY,
        nextX,
        jeanLuc[2] + abs(getCost(universe[nextY][nextX]) - getCost(universe[jeanLuc[0]][jeanLuc[1]])),
        abs(goal[0] - nextY) + abs(goal[1] - nextX),
        jeanLuc
    )


def expand(jeanLuc):
    retValue = []
    if jeanLuc[0] > 0:
        retValue.append(nextNodeWalk(jeanLuc, -1, 0)) # Up
    if jeanLuc[0] + 1 < MAXHeight:
        retValue.append(nextNodeWalk(jeanLuc, 1, 0)) # Down

    # Right and left walking is trickier
    if jeanLuc[1] >= MIDWidth:
        if jeanLuc[1] + 1 < MAXWidth:
            retValue.append(nextNodeWalk(jeanLuc, 0, 1)) # elAdrel right
        if jeanLuc[1] > MIDWidth:
            retValue.append(nextNodeWalk(jeanLuc, 0, -1)) # elAdrel left
    else:
        if jeanLuc[1] + 1 < MIDWidth:
            retValue.append(nextNodeWalk(jeanLuc, 0, 1)) # ship right
        if jeanLuc[1] > 0:
            retValue.append(nextNodeWalk(jeanLuc, 0, -1)) # ship Left

    # Special case expand
    if universe[jeanLuc[0]][jeanLuc[1]] == 'SS':
        shuttleLand = getShuttleLand(jeanLuc)
        retValue.append(nextNodeSpecial(jeanLuc, shuttleLand[0], shuttleLand[1]))
    if universe[jeanLuc[0]][jeanLuc[1]][0] == 'T':
        teleportList = getTeleportList(jeanLuc)
        for teleporter in teleportList:
            retValue.append(nextNodeSpecial(jeanLuc, teleporter[0], teleporter[1]))

    return retValue


def getSortedIndex(open, newJeanLuc):
    i = 0
    if not open:
        return 0
    for i in range(0, len(open)):
        if newJeanLuc[2] + newJeanLuc[3] < open[i][2] + open[i][3]:
            return i
    return i+1


def findClone(checkNode, open, closed):
    for node in open:
        if (node[0], node[1]) == (checkNode[0], checkNode[1]):
            return node
    for node in closed:
        if (node[0], node[1]) == (checkNode[0], checkNode[1]):
            return node


def killClone(target, open, closed):
    for i in range(len(open)-1, -1, -1):
        if (open[i][0], open[i][1]) == (target[0], target[1]):
            del open[i]
    for i in range(len(closed)-1, -1, -1):
        if (closed[i][0], closed[i][1]) == (target[0], target[1]):
            del closed[i]


def getPrintable(foundGoal):
    retValue = []
    while True:
        retValue.append((foundGoal[0]+1, foundGoal[1]+1))
        if foundGoal[4] == None:
            break
        foundGoal = foundGoal[4]
    return retValue


# Output coordinates must be incremented by one.
inp = open('input', 'r')

for line in inp:
    line = line.split()
    universe.append(line)

inp.close()

# Edges of space and time for the universe.
MAXHeight = len(universe)
MAXWidth = len(universe[0])

# Edge of space and time for starTrek and elAdrel.
# starTrek, elAdrel and universe share same height.
MIDWidth = MAXWidth /2

jeanLuc = (-1, -1, -1, -1, None)
goal = (-1, -1, -1, -1, None)
i = j = 0
for i in range(0, MAXHeight):
    for j in range(0, MAXWidth):
        if universe[i][j] == "P":
            jeanLuc = (i, j)
        if universe[i][j] == "C":
            goal = (i, j, 0, 0, None)
jeanLuc = (jeanLuc[0], jeanLuc[1], 0, goal[0] - jeanLuc[0] + goal[1] - jeanLuc[1], None)

if jeanLuc == (-1, -1, -1, -1, None) or goal == (-1, -1, -1, -1, None):
    print "Goal or jeanLuc not found, map is invalid programme will end."
    exit(1)

open = [jeanLuc]
closed = []
openNodes = 0
while open:
    # print open
    jeanLuc = open.pop(0)
    if (jeanLuc[0], jeanLuc[1]) == (goal[0], goal[1]):
        foundGoal = jeanLuc
        break
    closed.append(jeanLuc)
    newNodes = expand(jeanLuc)
    # print "open",open
    # print "closed",closed
    # print "newNodes",newNodes
    for node in newNodes:
        clone = findClone(node, open, closed)
        if clone:
            # print "CLONE FOUND", node
            if clone[2] <= node[2]:
                continue
            else:
                killClone(clone, open, closed)
        index = getSortedIndex(open, node)
        open.insert(index, node)
    # print "cleanup",open
    # print "cleanup",closed
    # print

print "Minimal cost:", foundGoal[2]
print "Open nodes:", len(closed)
print "Path:"
path = getPrintable(foundGoal)
for i in range(len(path)-1, -1, -1):
    if i != 0:
        print path[i], "->"
    else:
        print path[i]