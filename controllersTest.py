from pyroborobo import Pyroborobo, Controller
import numpy as np


class ControllerTest(Controller):

    def __init__(self, wm):
        # It is *mandatory* to call the super constructor before any other operation to link the python object to its C++ counterpart
        super().__init__(wm)
        self.arena_size = Pyroborobo.get().arena_size
        self.rob = Pyroborobo.get()
        self.setObjCollected(False);
        self.setCanInstantDrop(False);
        self.setIsObserved(False)
        self.rotspeed = 0.5

    def reset(self):
        pass

    def step(self):  
        self.set_translation(1)
        self.set_rotation(0)
        camera_dist = self.get_all_distances()
        
        # si le robot n'a pas d'objet il va en chercher
        if (self.getCanCollect() == True):
            if camera_dist[1] < 1:  # if we see something on our right
                if self.get_object_at(1) == 9:  # Si c'est une feuille
                      self.set_rotation(-0.5)  # turn right
                else:
                      self.set_rotation(0.5) # on évite si ce n'est pas une feuille
                      
            elif camera_dist[2] < 1:  # if we see something in front of us
                if self.get_object_at(2) == 9: # Si c'est une feuille
                    self.set_rotation(0)
                else :
                    self.set_rotation(0.5)  # On évite si ce n'est pas une feuille
                    
            elif camera_dist[3] < 1:  # Otherwise, if we see something on our left
                if self.get_object_at(3) == 9: # Si c'est une feuille
                    self.set_rotation(0.5)  # turn left
                else:
                    self.set_rotation(-0.5)  # on évite si ce n'est pas une feuille
                    
        # Si le robot a un objet il doit se rediriger vers le nid     
        elif (self.getCanCollect() == False):
            orient = self.get_closest_landmark_orientation()
            self.set_rotation(np.clip(orient, -1, 1))
            self.set_translation(1)
            pos = self.absolute_position
            if (pos[0]>445 and pos[0]<455 and pos[1]>845 and pos[1]<855):
                    self.setObjCollected(False)
                    #self.setCanCollect(True)
                    """
                    if (self.get_distance_at(1) < 1  # if we see something on our left
                        or self.get_distance_at(2) < 1):  # or in front of us
                        self.set_rotation(0.5)  # turn right
                    elif self.get_distance_at(3) < 1:  # Otherwise, if we see something on our right
                            self.set_rotation(-0.5)  # turn left
                    """
                    
        # Quand le robot est sur la pente 
        maxRampSpeed = 0.3
        p = self.absolute_position
        orientation = self.absolute_orientation
        x = p[0]
        y = p[1]
        if (x > 250 and x < 670 and y > 450 and y < 700 and orientation < 0.0):
            self.set_translation(maxRampSpeed)
        if (x > 250 and x < 670 and y > 450 and y < 700 and orientation > 0.0):
            self.set_translation(maxRampSpeed)
            
# Fonctions de ramassage et dépôt d'objets
    def getCanCollect(self):
        return self.canCollect
    
    def getCanDropSlope(self):
            return self.canDropSlope
        
    def getCanDropNest(self):
          return self.canDropNest
      
    def getCanInstantDrop(self):
        return self.instantDrop
    
    def getObjCollected(self):
        return self.objCollected

    def getIsObserved(self):
        return self.objObserved

# Fonction set
    
    def setCanCollect(self,c):
        self.canCollect = c
    
    def setCanDropSlope(self,c):
        self.canDropSlope = c
        
    def setCanDropNest(self,c):
         self.canDropNest = c
      
    def setCanInstantDrop(self,c):
        self.instantDrop = c
        
    def setIsObserved(self,c):
        self.objObserved = c
    
    def setObjCollected(self,c):
        self.objCollected = c
        if(c == True):
            print("Can not collect anymore")
            self.setCanCollect(False)
            self.setIsObserved(False)
            self.setCanDropSlope(True)
            self.setCanDropNest(True)
            self.setCanInstantDrop(True)
        if (c == False):
            print("Can recollect")
            self.setCanCollect(True)
            self.setCanDropSlope(False)
            self.setCanDropNest(False)
            self.setCanInstantDrop(False)
    
            

    
    
  
