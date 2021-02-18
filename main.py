from pyroborobo import Pyroborobo, PyWorldModel
from controllersTest import ControllerTest
from objects import SwitchObject, GateObject, MyEnergyItem
from World_observer_Test import World_Observer_test

if __name__ == "__main__":
    rob = Pyroborobo.create("config/test.properties",
                            controller_class=ControllerTest,
                            world_model_class=PyWorldModel,
                            world_observer_class=World_Observer_test,
                            object_class_dict={'_default': MyEnergyItem,'gate': GateObject, 'switch': SwitchObject})
    rob.start()
    rob.update(3000)
    Pyroborobo.close()