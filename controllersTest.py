from pyroborobo import Controller, PyWorldModel, Pyroborobo


class ControllerTest(Controller):
    world_model: PyWorldModel  # Predeclare that world_model is a PyWorldModel for better code completion

    def __init__(self, world_model):
        # It is *mandatory* to call the super constructor before any other operation to link the python object to its C++ counterpart
        Controller.__init__(self, world_model)
        self.rob = Pyroborobo.get()
        self.setObjCollected(False);
        self.setCanInstantDrop(False);
        self.setIsObserved(False)
        self.rotspeed = 0.5
        self.nb_sensors == 8
       

    def reset(self):
        print("I'm initialised")

    def step(self):  
        self.set_translation(1)
        self.set_rotation(0)
        camera_dist = self.world_model.camera_pixel_distance
        camera_max_range = self.world_model.maxdistcamera
        camera_ids = self.world_model.camera_objects_ids
        must_flee = False  # have we encountered a wall and must prioritise avoiding obstacle
        if camera_dist[1] < camera_max_range:  # if we see something on our right
            if self.get_object_at(1) == 4:  # And it is food
                self.set_rotation(-self.rotspeed)  # GO TOWARD IT
            else:
                self.set_rotation(self.rotspeed)  # flee it
                must_flee = True
        elif camera_dist[2] < camera_max_range:  # if we see something in front of us
            if self.get_object_at(2) == 4 and not must_flee:  # If we are not avoiding obstacle and it's food
                self.set_rotation(0)
            else:
                self.set_rotation(self.rotspeed)  # turn left
                must_flee = True
        elif camera_dist[3] < camera_max_range:  # Otherwise, if we see something on our right
            if self.get_object_at(3) == 4 and not must_flee:
                self.set_rotation(self.rotspeed)  # turn left
            else:
                self.set_rotation(-self.rotspeed)
                must_flee = True

        
        maxRampSpeed = 0.3
        p = self.absolute_position
        orientation = self.absolute_orientation
        x = p[0]
        y = p[1]
        if (x > 250 and x < 670 and y > 450 and y < 700 and orientation < 0.0):
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

    def getIsObserved(self,c):
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
            self.etCanDropSlope(True)
            self.setCanDropNest(True)
            self.setCanInstantDrop(True)
        if (c == False):
            print("Can recollect")
            self.setCanCollect(True)
            self.setCanDropSlope(False)
            self.setCanDropNest(False)
            self.setCanInstantDrop(False)
    
            

    
    
  
