# -*- coding: utf-8 -*-
# -*- coding: mbcs -*-

#summary:Guanglinzhong Bridge
#structure:Simple Support Beam
#load:Truck Load
#post:u, moment

#comment by lindinan in 20180707

from abaqus import *
from abaqusConstants import *
from caeModules import *

from interaction import *
from optimization import *
from sketch import *
from visualization import *
from connectorBehavior import *

import regionToolset

session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

nBeams=14    #number of beams
hDist=1.25   #horizontal distance
span=20

rouC50=2549
EC50=3.45E10
GC50=2.50E10
niuC50=0.2    #possion ratio

# Create a model.
modelName='GuanglinzhongBridge'

myModel = mdb.Model(name=modelName)

from part import *

# Create a sketch for the base feature.
mySketch = myModel.ConstrainedSketch(name='mySketch',sheetSize=10.0)

# Create the line.

#beam
for i in range(0,nBeams):    
    mySketch.Line(point1=(0.0, i*hDist), point2=(span, i*hDist))
#virtual beam
for i in range(0,span):
    mySketch.Line(point1=(i*1, 0), point2=(i*1, hDist*nBeams))

# Create a three-dimensional, deformable part.
myPart = myModel.Part(name='myPart', dimensionality=THREE_D, type=DEFORMABLE_BODY)

# Create the part's base feature
myPart.BaseWire(sketch=mySketch)

