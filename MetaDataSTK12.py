# Get reference to running STK instance using win32com
from win32com.client import GetActiveObject
uiApplication = GetActiveObject('STK12.Application')


# Get our IAgStkObjectRoot interface
root = uiApplication.Personality2 

print(root.CurrentScenario.InstanceName) 
print("Total number of objects: {0}".format(len(root.CurrentScenario.Children)))

for stkObject in root.CurrentScenario.Children:
    print(stkObject.ClassName + " " + stkObject.InstanceName)
    for stkObject in stkObject.Children:
        print(stkObject.ClassName + " " + stkObject.InstanceName)
        
        if stkObject.ClassName == "Sensor":
            patternType = stkObject.PatternType
            print ('0=ComplexConic, 1=SnCustom, 2=SnPHalfPower, 3=SnRectangular, 4=SnSAR, 5=SnSimpleConic, 6=SnEOIR')
            print patternType
            
        if stkObject.ClassName == "Antenna":
            antennaType = stkObject.Model.Name
            print antennaType
            
        if stkObject.ClassName == "Radar":
            radarType = stkObject.Model.Name
            print radarType
            
        if stkObject.ClassName == "Receiver":
            receiverType = stkObject.Model.Name
            print receiverType
            
        if stkObject.ClassName == "Transmitter":
            transmitterType = stkObject.Model.Name
            print transmitterType

    if stkObject.ClassName == "Facility":
        positionArray = stkObject.Position.QueryPlanetocentric()
        print('Position: {0:3.2f} {1:3.2f}'.format(positionArray[0], positionArray[1]))
        
    if stkObject.ClassName == "Satellite":
        possiblePropagator = stkObject.PropagatorSupportedTypes
        print possiblePropagator
        propagatorType = stkObject.PropagatorType
        print 'PropagatorType: ', propagatorType
        
    if stkObject.ClassName == "AreaTarget":
        centroidPosition = stkObject.Position.QueryPlanetocentricArray()
        print ('Position of Centroid: {0:3.2f} {1:3.2f}'.format(centroidPosition[0], centroidPosition[1]))
            
    if stkObject.ClassName == "CoverageDefinition":
        bounds = stkObject.PointDefinition.GridClass
        print 'Bounds:', bounds
        
    if stkObject.ClassName == "Missile":
        possibleTrajectory = stkObject.TrajectorySupportedTypes
        print possibleTrajectory
        usedTrajectory = stkObject.TrajectoryType
        print usedTrajectory
         
    if stkObject.ClassName == "Place":
        position = stkObject.Position.QueryPlanetocentricArray()
        print ('Position: {0:3.2f} {1:3.2f}'.format(position[0], position[1]))
        
    if stkObject.ClassName == "Target":
        positionArray = stkObject.Position.QueryPlanetocentric()
        print('Position: {0:3.2f} {1:3.2f}'.format(positionArray[0], positionArray[1]))
        
    if stkObject.ClassName == "Planet":
        centralBody = stkObject.PositionSourceData.CentralBody
        print centralBody
        
        
       