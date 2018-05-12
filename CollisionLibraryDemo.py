import pygame
import random
import time
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from quadTree import QuadTree,Bound
from Constants import SCREEN_WIDTH,SCREEN_HEIGHT,TPF,FRAME_CAP, BLACK, WHITE, RED, GREEN
from GameObject import Polygon,getRandomCircle

## @package Demo
#  Used for demoing project
#
#  More details.
class Demo:

    ## The constructor.
    #  @param self The object pointer.
    def __init__(self):
        self.done = False
        self.polygonList = []
        self.bufferList = []
        self.circleList = []
        self.circleMod = False
        self.polygonMod = True
        self.quadTreeMode = False
        self.m = 0
        self.f = 0
        pygame.init()
        pygame.display.set_caption('Collision Demo')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.quadTree = QuadTree(0, Bound(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.stars = [(random.randint(1, SCREEN_WIDTH-1), random.randint(1, SCREEN_HEIGHT-1)) for _ in range(300)]

    ## method used to reset demo
    #  @param self The object pointer.
    def resetGameObjects(self):
        self.circleList.clear()
        self.polygonList.clear()
        self.bufferList.clear()

    def loadCircles(self):
        for _ in range(1000):
            circle = getRandomCircle(self.circleList)
            self.circleList.append(circle)

    ## method used to load polygon buffer
    #  @param self The object pointer.
    def loadPolygonBuffer(self):
        self.bufferList = self.bufferList + self.loadPreLoadedPolygons()
        p = self.readPolygonsFromFile()
        self.bufferList = self.bufferList + list(self.readPolygonsFromFile()) + list(self.readPolygonsFromFile())\
                          + list(self.readPolygonsFromFile()) + list(self.readPolygonsFromFile()) \
                          + list(self.readPolygonsFromFile()) + list(self.readPolygonsFromFile()) \
                          + list(self.readPolygonsFromFile()) + list(self.readPolygonsFromFile()) \
                          + list(self.readPolygonsFromFile())

    ## method used to load initial polygon
    #  @param self The object pointer.
    def loadPreLoadedPolygons(self):
        preLoaded = []
        for _ in range(20):
            preLoaded.append(Polygon([70, 150, 70], [70, 70, 150], random.uniform(0.5,2), random.randint(20,200)))
        return preLoaded

    ## method used to read polygon from a file having coordinates
    #  @param self The object pointer.
    def readPolygonsFromFile(self):
        p = []
        f = open('Assets\\pol.txt', 'r')
        try:
            x = []
            y = []
            for l in f:
                if len(l) <= 2:
                    v = random.uniform(0.5,2)
                    o = random.randint(0, 360)
                    t = Polygon(x, y, v, o)
                    p.append(t)
                    x = []
                    y = []
                else:
                    tx, ty = l.split(',')
                    ty = ty[:-1]
                    x.append(float(tx))
                    y.append(float(ty))
        finally:
            f.close()
        return p

    ## method used to run demo
    #  @param self The object pointer.
    def run(self):
        while not self.done:
            start_time = time.time()
            if self.m == 0:
                self.m = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and len(self.bufferList) > 0:
                        if self.polygonMod:
                            item = self.bufferList.pop()
                            self.polygonList.append(item)
                        elif self.circleMod:
                            new_circle = getRandomCircle(self.circleList)
                            self.circleList.append(new_circle)
                    elif event.key == pygame.K_d:
                        self.quadTreeMode = not self.quadTreeMode
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.done = True
                    elif event.key == pygame.K_r:
                        self.resetGameObjects()
                        self.loadPolygonBuffer()
                    elif event.key == pygame.K_1:
                        self.circleMod = False
                        self.polygonMod = True
                    elif event.key == pygame.K_2:
                        self.circleMod = True
                        self.polygonMod = False
            self.screen.fill(BLACK)
            for star in self.stars:
                pygame.draw.circle(self.screen, WHITE, star, 1)

            self.quadTree.clear()

            ## Update game object
            if self.polygonMod:
                for polygon in self.polygonList:
                    polygon.update()
                    self.quadTree.insertObject(polygon)
            elif self.circleMod:
                for circle in self.circleList:
                    circle.update()
                    self.quadTree.insertObject(circle)

            ## Check for collision
            if self.polygonMod:
                self.quadTree.handlePolygonCollision(self.polygonList)
            elif self.circleMod:
                self.quadTree.handleCircleCollision(self.circleList)

            ## Render the gameobjects
            if self.polygonMod:
                # Draw polygon and add to Quad tree
                for polygon in self.polygonList:
                    pygame.draw.polygon(self.screen, RED, polygon.getXYTuple())
            elif self.circleMod:
                for circle in self.circleList:
                    pygame.draw.circle(self.screen, RED, (int(round(circle.cX)), int(round(circle.cY))), circle.cR)

            if self.quadTreeMode:
                # Render quadtrees
                for node in self.quadTree.getAllNodes([]):
                    pygame.draw.rect(self.screen, GREEN,
                                     (node.getX(), node.getY(), node.getWidth(), node.getHeight()),
                                     2)

            pygame.display.update()
            cur_time = time.time()
            self.f += 1
            if self.f == FRAME_CAP:
                me = time.time()
                #print(self.f / (me - self.m))
                self.m = 0
                self.f = 0
            dif = cur_time - start_time
            delay_required = TPF - dif * 1000
            if delay_required > 0:
                time.sleep(delay_required / 1000)



demoProject = Demo()
demoProject.loadPolygonBuffer()
demoProject.loadCircles()
demoProject.run()




