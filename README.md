\mainpage

# 2D Collision Demo

## Team

Team Name: Intelligance

Team members
- Shubham Sharma
- Chandan Shankarappa
- Prem Shah


## Description
The core idea of the project was to build a physics engine to simulate object in space, based on collision detection and collision resolution patterns. But due to inadequte resources on collision resolution for objects other than a circle, for now, we have implemented two demos -
1) A polygon collision detection system
2) A circle collision detection and resolution system
The algorithms we have used for this project can be found in this document - https://bit.ly/2HAetR9

## Instructions
- Run the demo.py file using a Python compiler
- To access the two different modes, use number keys 1 and 2
- To add polygons/circles press 'A'
- To display the quad tree division, press 'D'
- To reset the simulation, press 'R'
Note : Make sure Pygame is installed

## Minimum Viable Product

A Minimum Viable Product (MVP) is the smallest subset of features that you consider a project to be a success. Make a list below of the features you consider to be in your MVP. Then make a list of features that are 'stretch goals' that you think you can achieve.

MVP
- Multiples objects rendering.
- At least 100 objects collision detection without drastic framedrops.
- Good collision resolution.

Strecth Goals
- Display quad tree
- Debug mode
- etc

### Website
- http://collision-demo.herokuapp.com/

### Build (binary file)
- https://bit.ly/2vpUY9b

### Post mortem
- If we had more time, we could have better implemented the underlying architecture using Pybind and SDL in C++ for rendering instead of using Pygame.
- We could have also figured out an approximation function for polygon collision resolution as currently we found no useful resource for it.
- We used regional quad tree for paritioning the region and for retreiving possible objects for collision detection. We could have implemented PolygonMap Quad Tree or researched more on it to see if there was any other better option for us to implement.
- We optimized our polygon collision detection best we could in given time, however there are some algorithms which are better equipped to handle it. However 
implementing them is a complex job, if we had more time we could try some of them and see which one would have worked best for us. We implemented algorithm which was more widely used for this problem. It didn't necessarily satisfy the standards we were hoping to achieve.