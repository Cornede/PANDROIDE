from pyroborobo import Controller, PyWorldModel, Pyroborobo, WorldObserver
from controllersTest import ControllerTest

#Variables globales
#Zone de jeu
zoneCollectMin = 50
depotMin = 400
depotMax = 450
rampeYMin=450
rampeYMax=700
nestYMin=950
nestYMax=1000




class World_Observer_test(WorldObserver):
    
    def __init__(self, world):
        super().__init__(world)
        self.rob = Pyroborobo.get()
        self.pointCount = 0
        
    def step_pre(self):
        super().step_pre()
        for c in self.rob.controllers:
            p = c.absolute_position
            x = p[0]
            y = p[1]
            if(c.getCanInstantDrop()==True):
                c.setObjCollected(False)
                ori = c.absolute_orientation
                if(y>nestYMin and y < nestYMax): # on est dans le nid
                        print("lacher dans le nid")
                        self.addPoint(50000)
                if(y>depotMin and y < rampeYMax):
                        self.addPoint(20000)
   
    def addPoint(self,p):
        self.pointCount=self.pointCount+p
                
            
        
        
        
      