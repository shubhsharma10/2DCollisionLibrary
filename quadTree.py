import math

from Constants import MAX_OBJECTS
from SAT import checkForCollision

## @package Bound
#  Used to get rectangular bound of space objects
#
#  More details.
class Bound():
    ## The constructor.
    #  @param self The object pointer.
    #  @param x x-coordinate of top left point
    #  @param y y-coordinate of top left point
    #  @param width width of bound
    #  @param height height of bound
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    ## method used to get x coordinate of top left point.
    #  @param self The object pointer.
    def getX(self):
        return self.x

    ## method used to get y coordinate of top left point.
    #  @param self The object pointer.
    def getY(self):
        return self.y

    ## method used to get width of bound object
    #  @param self The object pointer.
    def getWidth(self):
        return self.width

    ## method used to get height of bound object
    #  @param self The object pointer.
    def getHeight(self):
        return self.height

## @package QuadTree
#  Used to create Quadtree to optimize collision
#  Each Node is type of Bound class
#  More details.
class QuadTree():

    ## The constructor.
    #  @param self The object pointer.
    #  @param level height(level) of Node in Quadtree
    #  @param rectBound node object
    def __init__(self,level,rectBound):
        self.level = level
        self.rectBound = rectBound
        self.objects = []
        self.nodes = [] ## 4 with each node

    ## method used to clear QuadTree
    #  @param self The object pointer.
    def clear(self):
        self.objects.clear()
        for node in self.nodes:
            node.clear()
        self.nodes.clear()

    ## method used to get object reciding on boundaries of QuadTree
    #  @param self The object pointer.
    def getGameObjects(self):
        return self.objects

    ## method used to get all nodes belonging to that QuadTree(a recursive function)
    #  @param self The object pointer.
    #  @param allNodes list of Nodes at current level
    def getAllNodes(self,allNodes):
        allNodes.append(self.rectBound)
        if len(self.nodes) > 0:
            for node in self.nodes:
                node.getAllNodes(allNodes)
        return allNodes

    ## method used to divide QuadTree into four quadrant
    #  @param self The object pointer.
    def splitNode(self):
        subWidth = int(self.rectBound.getWidth() / 2)
        subHeight = int(self.rectBound.getHeight()/2)
        x = self.rectBound.getX()
        y = self.rectBound.getY()

        self.nodes.append(QuadTree(self.level + 1, Bound(x, y, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x+subWidth, y, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x+subWidth, y+subHeight, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x, y+subHeight, subWidth, subHeight)))

    ## method used to get quadrant number based on where it resides in QuadTree
    #  @param self The object pointer.
    #  @param gameobject object of Bound class
    def getIndex(self,gameObject):
        if len(self.nodes) <= 0:
            return -1
        if gameObject.canFitInRect(self.nodes[0]):
            return 0
        elif gameObject.canFitInRect(self.nodes[1]):
            return 1
        elif gameObject.canFitInRect(self.nodes[2]):
            return 2
        elif gameObject.canFitInRect(self.nodes[3]):
            return 3
        else:
            return -1

    ## method used to insert object of Bound class to respective level in QuadTree(recursive function)
    #  @param self The object pointer.
    #  @param gameobject object of Bound class
    def insertObject(self,gameObject):
        # Check to insert in existing subnodes
        if len(self.nodes) > 0:
            subNodeIndex = self.getIndex(gameObject)
            if subNodeIndex > -1:
                self.nodes[subNodeIndex].insertObject(gameObject)
                return
        # Add to the parent
        self.objects.append(gameObject)

        # If exceeds limit then split and add
        if len(self.objects) > MAX_OBJECTS:
            if len(self.nodes) == 0:
                self.splitNode()
            # For keeping object in parent node
            newObjects = []
            for object in self.objects:
                subNodeIndex = self.getIndex(object)
                if subNodeIndex > -1:
                    self.nodes[subNodeIndex].insertObject(object)
                else:
                    newObjects.append(object)
            self.objects = newObjects

    ## method used to return list of all objects(Nodes) at current or lower level than gameobject in QuadTree
    #  @param self The object pointer.
    #  @param gameobject object of Bound class
    def retrieveObjs(self,gameObject):
        subNodeIndex = self.getIndex(gameObject)
        returnList = []
        if subNodeIndex > -1:
            returnList.extend(self.objects)
            returnList.extend(self.nodes[subNodeIndex].retrieveObjs(gameObject))
        else:
            returnList.extend(self.objects)
            if len(self.nodes) > 0:
                for node in self.nodes:
                    if gameObject.doesIntersect(node):
                        returnList.extend(node.retrieveObjs(gameObject))
        return returnList

    ## method used to update QuadTree
    #  @param self The object pointer.
    def updateGameObjects(self):
        for gameObject in self.objects:
            gameObject.update()

    ## method used to handle collision between current object and all objects in QuadTree
    #  @param self The object pointer.
    #  @param circleList list of all circles present in QuadTree
    def handleCircleCollision(self,circleList):
        collidedTuples = []
        for gameObject in circleList:
            possibleHits = self.retrieveObjs(gameObject)
            for possibleHit in possibleHits:
                centerDis = math.fabs(math.sqrt(
                    math.pow(possibleHit.cX - gameObject.cX, 2) + math.pow(possibleHit.cY - gameObject.cY, 2)))
                radiusSum = possibleHit.cR + gameObject.cR

                if centerDis <= radiusSum \
                        and (possibleHit.getGUID(),gameObject.getGUID()) not in collidedTuples \
                        and possibleHit.getGUID() != gameObject.getGUID():
                    collidedTuples.append((gameObject.getGUID(),possibleHit.getGUID()))
                    vx1 = (possibleHit.vx * (possibleHit.mass - gameObject.mass) +
                           (2 * gameObject.mass * gameObject.vx)) / (possibleHit.mass + gameObject.mass)
                    vy1 = (possibleHit.vy * (possibleHit.mass - gameObject.mass) +
                           (2 * gameObject.mass * gameObject.vy)) / (possibleHit.mass + gameObject.mass)
                    vx2 = (gameObject.vx * (gameObject.mass - possibleHit.mass) +
                           (2 * possibleHit.mass * possibleHit.vx)) / (possibleHit.mass + gameObject.mass)
                    vy2 = (gameObject.vy * (gameObject.mass - possibleHit.mass) +
                           (2 * possibleHit.mass * possibleHit.vy)) / (possibleHit.mass + gameObject.mass)
                    gameObject.updateVelocityAfterCollision((vx2,vy2))
                    possibleHit.updateVelocityAfterCollision((vx1,vy1))

    ## method used to handle collision between current object and all objects in QuadTree
    #  @param self The object pointer.
    #  @param polygonList list of all polygons present in QuadTree
    def handlePolygonCollision(self,polygonList):
        collidedTuples = []
        for gameObject in polygonList:
            possibleHits = set(self.retrieveObjs(gameObject))
            for possibleHit in possibleHits:
                centerDis = math.fabs(math.sqrt(
                    math.pow(possibleHit.cX - gameObject.cX, 2) + math.pow(possibleHit.cY - gameObject.cY, 2)))
                radiusSum = possibleHit.cR + gameObject.cR
                if centerDis <= radiusSum \
                        and (possibleHit.getGUID(), gameObject.getGUID()) not in collidedTuples \
                        and possibleHit.getGUID() != gameObject.getGUID():
                    collidedTuples.append((gameObject.getGUID(), possibleHit.getGUID()))
                    result = checkForCollision(gameObject,possibleHit)
                    if result[0]:
                        gameObject.pause()
                        possibleHit.pause()


