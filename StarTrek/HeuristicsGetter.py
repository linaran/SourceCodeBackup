def getManDist(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def calculateShuttleCost(universe, jeanLuc, goal):
    global MAXHeight, MAXWidth, MIDWidth
    retValue = None
    shuttleLocation = None
    shuttleLanding = None
    for i in range(0, MAXHeight):
        for j in range(0, MIDWidth):
            if universe[i][j] == "SS":
                shuttleLocation = (i, j)
    for i in range(0, MAXHeight):
        for j in range(MIDWidth, MAXWidth):
            if universe[i][j] == "SL":
                shuttleLanding = (i, j)
    if shuttleLocation and shuttleLanding:
        retValue = getManDist(jeanLuc, shuttleLocation) + \
                   3*getManDist(shuttleLanding, shuttleLocation) + \
                   getManDist(shuttleLanding, goal)
    return retValue


def getClosestTeleport(universe, jeanLuc, goal):
    global MAXHeight, MAXWidth, MIDWidth
    minDistance = None
    retValue = None
    for i in range(0, MAXHeight):
        for j in range(0, MIDWidth):
            if not minDistance and universe[i][j][0] == "T":
                minDistance = getManDist(jeanLuc, (i, j))
                retValue = (i, j)
            elif universe[i][j][0] == "T":
                if abs(i - jeanLuc[0]) + abs(j - jeanLuc[1]) < minDistance:
                    minDistance = getManDist(jeanLuc, (i, j))
                    retValue = (i, j)
    return retValue


def calculateTeleportCost(universe, jeanLuc, goal, shipTeleport):
    global MAXHeight, MAXWidth, MIDWidth
    minCost = None
    if not shipTeleport:
        return None
    for i in range(0, MAXHeight):
        for j in range(MIDWidth, MAXWidth):
            if universe[i][j][0] == "T":
                if not minCost:
                    minCost = getManDist(shipTeleport, (i, j)) + getManDist((i, j), goal)
                elif getManDist(shipTeleport, (i, j)) + getManDist((i, j), goal) < minCost:
                    minCost = getManDist(shipTeleport, (i, j)) + getManDist((i, j), goal)
    return minCost + getManDist(jeanLuc, shipTeleport)


def getHeuristic(universe, jeanLuc, goal):
    global MAXHeight, MAXWidth, MIDWidth
    MAXHeight = len(universe)
    MAXWidth = len(universe[0])
    MIDWidth = MAXWidth /2
    if jeanLuc[1] < MIDWidth:
        shuttleCost = calculateShuttleCost(universe, jeanLuc, goal)
        shipTeleport = getClosestTeleport(universe, jeanLuc, goal)
        teleportCost = calculateTeleportCost(universe, jeanLuc, goal, shipTeleport)
        if not shuttleCost:
            return teleportCost
        elif not teleportCost:
            return shuttleCost
        else:
            return min(teleportCost, shuttleCost)
    else:
        return getManDist(jeanLuc, goal)