from pyroborobo import SquareObject, CircleObject,Pyroborobo
from controllersTest import ControllerTest

class Feuille(CircleObject):

    def __init__(self, id, data):
        super().__init__(id)
        self.set_color(255, 165, 0)
        self.transported = False
        self.data = data
        self.rob = Pyroborobo.get()

    def reset(self):
         pass

    def step(self):
         if self.transported == True:
                 self.hide()
        

    def is_walked(self, robid):
        r = self.rob.controllers
        c = r.get_robot_controller_at(robid)
        if(c.getCanCollect() == True):
            c.setObjCollected(True)
            print("Collecté")
            self.unregister()
        else:
            print("non collecté")
        
    def isTouched(self,robid) : 
        r = self.rob.controllers
        c = r.get_robot_controller_at(robid)
        print("touché")
        if(c.getCanCollect() == True):
            c.setObjCollected(True)
            print("Collected")
            self.transported = True
            # self.setRegion(0.0,0.2)
            self.hide()
            self.relocate()
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
                if self.cur_regrow <= 0:
                    self.show()
                    self.register()
                    self.triggered = False
    
        def is_walked(self, rob_id):
            print("I'm walked")
            self.triggered = True
            self.rob.objects[self.gate_id].open()
            self.cur_regrow = self.regrow_time
            self.hide()
            self.unregister()
    
        def inspect(self, prefix=""):
            return "I'm a switch!"


class GateObject(SquareObject):
        def __init__(self, id, data):
            SquareObject.__init__(self, id)
            self.triggered = False
            self.regrow_time = data['regrowTimeMax']
            self.cur_regrow = 0
    
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
    
        def open(self):
            self.triggered = True
            self.hide()
            self.unregister()
            self.cur_regrow = self.regrow_time
    
        def inspect(self, prefix=""):
            return "I'm a gate!"


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


            

        
        
