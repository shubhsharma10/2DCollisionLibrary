import math
import random
import uuid
from smallestCircle import make_circle
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

## @package GameObject
#  Used as main parent class for all objects residing in space
#
#  More details.
class GameObject:

    ## The constructor.
    #  @param self The object pointer.
    #  @param x x-coordinate of center
    #  @param y y-coordinate of center
    #  @param r radius
    #  @param v velocity of object
    #  @param o orientation of object
    def __init__(self,x,y,r,v=0,o=0):
        self.guid = uuid.uuid4()
        self.cX = x
        self.cY = y
        self.cR = r
        self.v = v
        self.o = math.radians(o)
        self.vy = math.cos(self.o) * self.v
        self.vx = math.sin(self.o) * self.v
        self.isPaused = False

    ## method used to get unique id of object
    #  @param self The object pointer.
    def getGUID(self):
        return self.guid

    ## method used to check if GameObject can fit in Rectangle
    #  @param self The object pointer.
    #  @param quadNode rectangle to check with
    def canFitInRect(self, quadNode):
        pass

    ## method used to check if GameObject is colliding with horizontal wall
    #  @param self The object pointer.
    def checkForHorizontalWallCollision(self):
        pass

    ## method used to get circle bounding gameobject
    #  @param self The object pointer.
    def getCircle(self):
        return (self.cX, self.cY, self.cR)

    ## method used to check if GameObject is colliding eith vertical wall
    #  @param self The object pointer.
    def checkForVerticalWallCollision(self):
        pass

    ## method used to update state of gameobject
    #  @param self The object pointer.
    def update(self):
        pass

    ## method used to check if GameObject intersects with Rectangle
    #  @param self The object pointer.
    #  @param rect rectangle with which intersection is checked
    def doesIntersect(self,rect):
        pass

    ## method used to stop movement of gameobject
    #  @param self The object pointer.
    def pause(self):
        self.isPaused = True

    ## method used to offsets polygon's position and flips velocity
    #  @param self The object pointer.
    #  @param offsetVector change offset of gameobject by offsetVector
    def offset(self, offsetVector):
        pass

    ## method used to update velocity of gameobject
    #  @param self The object pointer.
    #  @param newVelocity new velocity of gameobject
    def updateVelocity(self, newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]

    ## method used to update velocity of gameobject after collision
    #  @param self The object pointer.
    #  @param newVelocity new velocity of gameobject
    def updateVelocityAfterCollision(self,newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]

## @package Polygon
#  Polygon class which inherits GameObject class
#
#  More details.
class Polygon(GameObject):
    ## The constructor.
    #  @param self The object pointer.
    #  @param x x-coordinate of center
    #  @param y y-coordinate of center
    #  @param v velocity of object
    #  @param o orientation of object
    def __init__(self, x, y, v=0, o=0):
        self.x = x
        self.y = y
        cX,cY,cR = make_circle(self.getXYTuple())
        super().__init__(int(cX),int(cY),int(cR),v,o)

    ## method used to check if Polygon is colliding with horizontal wall
    #  @param self The object pointer.
    def checkForHorizontalWallCollision(self):
        if any(i <= 0 for i in self.y) or any(i >= SCREEN_HEIGHT for i in self.y):
            self.vy = -(self.vy)

    ## method used to check if Polygon is colliding with vertical wall
    #  @param self The object pointer.
    def checkForVerticalWallCollision(self):
        if any(i <= 0 for i in self.x) or any(i >= SCREEN_WIDTH for i in self.x):
            self.vx = -(self.vx)

    ## method used to check update polygon
    #  @param self The object pointer.
    def update(self):
        if not self.isPaused:
            self.checkForVerticalWallCollision()
            self.checkForHorizontalWallCollision()

            for i in range(len(self.x)):
                self.x[i] += self.vx
                self.y[i] += self.vy
            self.cX, self.cY, self.cR = make_circle(self.getXYTuple())
            self.cX = int(self.cX)
            self.cY = int(self.cY)
            self.cR = int(self.cR)

    ## method used to check if GameObject intersects with Rectangle
    #  @param self The object pointer.
    #  @param quadNode rectangle with which intersection is checked
    def doesIntersect(self,quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()
        for corner in zip(self.x,self.y):
            if x1 < corner[0] < x2 and y1 < corner[1] < y2:
                return True
        return False

    ## method used to check if Polygon can fit in Rectangle
    #  @param self The object pointer.
    #  @param quadNode rectangle to check on
    def canFitInRect(self, quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()

        for corner in self.getXYTuple():
            if not (x1 <= corner[0] <= x2 and y1 <= corner[1] <= y2):
                return False
        return True

    ## method used to offsets polygon's position and flips velocity
    #  @param self The object pointer.
    #  @param offsetVector change offset of Polygon by offsetVector
    def offset(self, offsetVector):
        for i in range(len(self.x)):
            self.x[i] += offsetVector[0]
            self.y[i] += offsetVector[1]
        self.vx = - self.vx
        self.vy = - self.vy
        self.cX, self.cY, self.cR = make_circle(self.getXYTuple())
        self.cX = int(self.cX)
        self.cY = int(self.cY)
        self.cR = int(self.cR)

    ## method used to get center of polygon as tuple
    #  @param self The object pointer.
    def getXYTuple(self):
        return list(zip(self.x, self.y))

    ## method used to get circle tuple of polygon
    #  @param self The object pointer.
    def getCircleTuple(self):
        return [self.cX, self.cY, self.vx, self.vy, self.cR, 3 * math.pow(self.cR, 2)]

## @package Circle
#  Circle class which inherits GameObject class
#
#  More details.
class Circle(GameObject):
    ## The constructor.
    #  @param self The object pointer.
    #  @param x x-coordinate of center
    #  @param y y-coordinate of center
    #  @param v velocity of object
    #  @param o orientation of object
    def __init__(self, x, y, r,v=0,o=0):
        super().__init__(x,y,r,v,o)
        self.mass = 3 * math.pow(self.cR,2)

    ## method used to check if Circle is colliding with horizontal wall
    #  @param self The object pointer.
    def checkForHorizontalWallCollision(self):
        if self.cY - self.cR <= 0 or self.cY + self.cR >= SCREEN_HEIGHT:
            self.vy = -(self.vy)

    ## method used to check if Circle is colliding with vertical wall
    #  @param self The object pointer.
    def checkForVerticalWallCollision(self):
        if self.cX - self.cR <= 0 or self.cX + self.cR >= SCREEN_WIDTH:
            self.vx = -(self.vx)

    ## method used to check if Circle can fit in Rectangle
    #  @param self The object pointer.
    #  @param quadNode rectangle to check on
    def canFitInRect(self, quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()

        cx1 = self.cX - self.cR
        cx2 = self.cX + self.cR
        cy1 = self.cY - self.cR
        cy2 = self.cY + self.cR

        if (x1 <= cx1 <= x2) and (x1 <= cx2 <= x2) and (y1 <= cy1 <= y2) and (y1 <= cy2 <= y2):
            return True
        return False

    # method used to check if Circle intersects with Rectangle
    # @param self The object pointer.
    # @param quadNode rectangle to check on
    def doesIntersect(self,quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()
        deltaX = self.cX - max(x1, min(self.cX, x2))
        deltaY = self.cY - max(y1, min(self.cY, y2))
        return (deltaX * deltaX + deltaY * deltaY) < (self.cR * self.cR)

    # method used to update circle
    # @param self The object pointer.
    def update(self):
        if not self.isPaused:
            self.checkForVerticalWallCollision()
            self.checkForHorizontalWallCollision()

            self.cX += self.vx
            self.cY += self.vy

    ## method used to update velocity of circle after collision
    #  @param self The object pointer.
    #  @param newVelocity new velocity of circle
    def updateVelocityAfterCollision(self,newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]
        self.cX += self.vx
        self.cY += self.vy

## Documentation for getting a random circle.
#  @param circleList list of existing circles
#
#  More details.
def getRandomCircle(circleList):
    newCircleFound = False
    x,y,r = 0,0,0
    while not newCircleFound:
        x = random.randint(10, SCREEN_WIDTH)
        y = random.randint(10, SCREEN_HEIGHT)
        r = 4
        if len(circleList)==0:
            return Circle(x,y,r,random.uniform(0.5, 2),random.randint(10, 180))
        cnt = 0
        for existingCircle in circleList:
            distFromPrevCircle = int(math.hypot(existingCircle.cX - x, existingCircle.cY - y))
            if not distFromPrevCircle <= int(existingCircle.cX + r):
                cnt = cnt + 1
                break
        if cnt==1:
            newCircleFound = True
    return Circle(x,y,r,random.uniform(0.5, 2),random.randint(10, 180))