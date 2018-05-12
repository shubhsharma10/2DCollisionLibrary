import math

## Documentation for getting a list of axes
#  @param points list of points
#
#  More details.
def getAxes(points):
    axes = []
    for i in range(len(points)):
        a = points[i]
        b = points[(i+1)%len(points)]
        edge = (a[0]-b[0],a[1]-b[1])
        axis = (edge[1],-edge[0])
        axes.append(axis)
    return axes

## Documentation for normalizing axis
#  @param axis axis to normalize
#
#  More details.
def normalize(axis):
    magnitude = math.sqrt(math.pow(axis[0],2)+math.pow(axis[1],2))
    ax = axis[0] / magnitude
    ay = axis[1] / magnitude
    return (ax,ay)

## Documentation for getting projection of points on axis
#  @param points list of points
#  @param axis axis to project on
#
#  More details.
def getProjection(points,axis):
    projections = [point[0]*axis[0] + point[1]*axis[1] for point in points]
    return (min(projections),max(projections))

## Documentation for getting interval distance
#  @param minA minimum value of pointA
#  @param maxA maximum value of pointA
#  @param minB minimum value of pointB
#  @param maxB maximum value of pointB
#
#  More details.
def getIntervalDistance(minA,maxA,minB,maxB):
    if (minA < minB):
        return minB - maxA
    else:
        return minA - maxB

## Documentation for getting dot products of two vectors
#  @param vectorA first vector
#  @param vectorB second vector
#
#  More details.
def dotProduct(vectorA,vectorB):
    return vectorA[0]*vectorB[0] + vectorA[1]*vectorB[1]

## Documentation for checking collision between two polygons
#  @param polygonA first polygon
#  @param polygonB second polygon
#
#  More details.
def checkForCollision(polygonA,polygonB):
    areIntersecting = True
    pointsA = polygonA.getXYTuple()
    pointsB = polygonB.getXYTuple()
    axesA = getAxes(pointsA)
    axesB = getAxes(pointsB)
    axes = axesA + axesB
    minIntervalDis = math.inf
    translationAxis = ()

    for axis in axes:
        minA, maxA = getProjection(pointsA,axis)
        minB, maxB = getProjection(pointsB,axis)
        intervalDis = getIntervalDistance(minA,maxA,minB,maxB)
        if intervalDis > 0 :
            areIntersecting = False

        intervalDis = math.fabs(intervalDis)
        if intervalDis < minIntervalDis :
            minIntervalDis = intervalDis
            translationAxis = normalize(axis)

            centerDis = (polygonA.getCircle()[0] - polygonB.getCircle()[0],
                         polygonA.getCircle()[1] - polygonB.getCircle()[1])
            if dotProduct(centerDis,translationAxis) < 0 :
                translationAxis = (-translationAxis[0],-translationAxis[1])

    ax = 0
    ay = 0
    if(areIntersecting):
        ax = minIntervalDis*translationAxis[0]
        ay = minIntervalDis*translationAxis[1]

    result = (areIntersecting,ax,ay)
    return result


