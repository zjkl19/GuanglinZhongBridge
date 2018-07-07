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
nVirtualBeam=21    #number of the virtual beam

rouC50=2549
EC50=3.45E10
GC50=2.50E10
niuC50=0.2    #possion ratio

rouVirtualBeam=0
EVirtualBeam=3.45E10
GVirtualBeam=2.50E10
niuVirtualBeam=0.2    #possion ratio

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
for i in range(0,nVirtualBeam):
    mySketch.Line(point1=(i*1, 0), point2=(i*1, hDist*(nBeams-1)))

# Create a three-dimensional, deformable part.
myPart = myModel.Part(name='myPart', dimensionality=THREE_D, type=DEFORMABLE_BODY)

# Create the part's base feature
myPart.BaseWire(sketch=mySketch)

from section import *
# Create the beam section.

AMidBeam=6.112E-1
i11MidBeam=5.67572E-2
i12MidBeam=0.0
i22MidBeam=1.01174E-1
jj=1.09301E-1

ASideBeam=6.929E-1
i11SideBeam=6.46024E-2
i12SideBeam=0
i22SideBeam=1.34678E-1
jSideBeam=1.20873E-1

myModel.GeneralizedProfile(name='midBeamProfile', area=AMidBeam, i11=i11MidBeam, i12=i12MidBeam, i22=i22MidBeam, j=jj, gammaO=0.0, gammaW=0.0) 
myModel.BeamSection(name='midBeamSection', integration=BEFORE_ANALYSIS,density=rouC50,
	poissonRatio=0.20, beamShape=CONSTANT, profile='midBeamProfile', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((EC50, GC50), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

myModel.GeneralizedProfile(name='sideBeamProfile', area=ASideBeam, i11=i11SideBeam, i12=i12SideBeam, i22=i22SideBeam, j=jSideBeam, gammaO=0.0, gammaW=0.0) 
myModel.BeamSection(name='sideBeamSection', integration=BEFORE_ANALYSIS,density=rouC50,
	poissonRatio=0.20, beamShape=CONSTANT, profile='sideBeamProfile', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((EC50, GC50), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

myModel.IProfile(name='virtualBeamProfile', l=0.45,h=0.9,b1=1,b2=1,t1=0.12,t2=0.12,t3=0.001) 
myModel.BeamSection(name='virtualBeamSection', integration=BEFORE_ANALYSIS,density=0,
	poissonRatio=0.20, beamShape=CONSTANT, profile='virtualBeamProfile', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((EC50, GC50), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

###

#side beam
for j in range(0,nVirtualBeam-1):
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((0.5+j*1, 
        0, 0.0), ), )), sectionName='sideBeamSection', thicknessAssignment=
        FROM_SECTION)

for j in range(0,nVirtualBeam-1):
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((0.5+j*1, 
        (nBeams-1)*hDist, 0.0), ), )), sectionName='sideBeamSection', thicknessAssignment=
        FROM_SECTION)

#middle beam
for i in range(0,nBeams-2):
    for j in range(0,nVirtualBeam-1):
        myPart.SectionAssignment(offset=0.0, 
            offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
            edges=myPart.edges.findAt(((0.5+j*1, 
            (i+1)*hDist, 0.0), ), )), sectionName='midBeamSection', thicknessAssignment=
            FROM_SECTION)

#virtual beam
for i in range(0,nVirtualBeam):
    for j in range(0,nBeams-1):
        myPart.SectionAssignment(offset=0.0, 
            offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
            edges=myPart.edges.findAt(((i*1, 
            hDist/2+j*hDist, 0.0), ), )), sectionName='virtualBeamSection', thicknessAssignment=
            FROM_SECTION)

#beam
for i in range(0,nBeams):
    for j in range(0,nVirtualBeam-1):
        myPart.assignBeamSectionOrientation(method=
            N1_COSINES, n1=(0.0, -1.0, 0.0), region=Region(
            edges=myPart.edges.findAt(((0.5+j*1, i*hDist, 0.0), 
            ),)))

for i in range(0,nVirtualBeam):
    for j in range(0,nBeams-1):
        myPart.assignBeamSectionOrientation(method=
            N1_COSINES, n1=(-1.0, 0.0, 0.0), region=Region(
            edges=myPart.edges.findAt(((i*1, hDist/2+j*hDist, 0.0), 
            ),)))

myModel.rootAssembly.DatumCsysByDefault(CARTESIAN)
myModel.rootAssembly.Instance(dependent=ON, name=
    'myPart-1', part=myPart)

from step import *

myModel.StaticStep(name='Step-1', previous='Initial',
    nlgeom=OFF, description='Load of the beam.')


from load import *
myAssembly = myModel.rootAssembly

v=myAssembly.instances['myPart-1'].vertices
