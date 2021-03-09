from pyroborobo import Pyroborobo, Controller, CircleObject, SquareObject
import copy
from controllersTest import ControllerTest

class Feuille(CircleObject):

    def __init__(self, id, data):
        super().__init__(id)
        self.set_color(255, 165, 0)
        self.transported = False
        self.data = data
        self.default_x = copy.copy(data["x"])
        self.default_y = copy.copy(data["y"])
        self.rob = Pyroborobo.get() # Get pyroborobo singleton

    def reset(self):
        self.show()
        self.register()
        self.transported= False


    def step(self):
         x, y = self.position
         if self.transported == True: # si l'objet est transporté
              if x < 20:
                 new_x= 5 # mettre une coordonnées aléatoire en bas de la pente
                 new_y= 6 # mettre une coordonnées aléatoire en bas de la pente
                 self.unregister()
                 success = self.relocate(new_x, new_y)
                 if not success:
                     self.relocate(self.default_x, self.default_y)
                     self.transported= False
                 self.register()
                 
                 
    def is_walked(self, robid):
        for c in self.rob.controllers:
            if(c.get_id() == robid):
                if(c.getCanCollect() == True):
                    print("Collecté")
                    c.setObjCollected(True)
                    c.setCanInstantDrop(True)
                    self.transported = True
                    self.hide()
                    self.unregister()
                else:
                    print("non collecté")
        
    def isTouched(self,robid) : 
        for c in self.rob.controllers:
            if(c.get_id() == robid):
                if(c.getCanCollect() == True):
                    print("Collected")
                    c.setObjCollected(True)
                    c.setCanInstantDrop(True)
                    self.transported = True
                    self.hide()
                    self.unregister()
                else : 
                    print("non collecté")
            
class SwitchObject(CircleObject):
    def __init__(self, id, data):
        CircleObject.__init__(self, id)  # Do not forget to call super constructor
        self.regrow_time = data['regrowTimeMax']
        self.cur_regrow = 0
        self.triggered = False
        self.gate_id = data['sendMessageTo']
        self.rob = Pyroborobo.get()  # Get pyroborobo singleton

    def reset(self):
        self.show()
        self.register()
        self.triggered = False
        self.cur_regrow = 0

    def step(self):
        if self.triggered:
            self.cur_regrow -= 1
            if self.cur_regrow <= 0 and self.can_register():
                self.show()
                self.register()
                self.triggered = False

    def is_walked(self, rob_id):
        self.triggered = True
        self.rob.objects[self.gate_id].open()
        self.cur_regrow = self.regrow_time
        self.hide()
        self.unregister()

    def inspect(self, prefix=""):
        return "I'm a switch!"

class UWallObject(SquareObject):
    def __init__(self, id, data):
        super().__init__(id)
        self.data = data
        self.unregister()
        if data["side"] == "left":
            self.solid_height = 100
            self.solid_width = 10
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(200, 300)
        elif data["side"] == "right":
            self.solid_height = 100
            self.solid_width = 10
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(300, 300)
        elif data["side"] == "bottom":
            self.solid_height = 10
            self.solid_width = 90
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(250, 345)
        self.register()

    def step(self):
        pass

    def inspect(self, prefix=""):
        return str(self.position)


class ResourceObject(CircleObject):
    def __init__(self, id_, data):
        CircleObject.__init__(self, id_)  # Do not forget to call super constructor
        self.regrow_time = 100
        self.cur_regrow = 0
        self.triggered = False
        self.rob = Pyroborobo.get()  # Get pyroborobo singleton

    def reset(self):
        self.show()
        self.register()
        self.triggered = False
        self.cur_regrow = 0

    def step(self):
        if self.triggered:
            self.cur_regrow -= 1
            if self.cur_regrow <= 0:
                self.show()
                self.register()
                self.triggered = False

    def is_walked(self, rob_id):
        self.triggered = True
        self.cur_regrow = self.regrow_time
        self.hide()
        self.unregister()


            

        
        
