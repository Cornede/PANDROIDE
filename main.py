from pyroborobo import Pyroborobo
from controllersTest import ControllerTest
from objects import SwitchObject, UWallObject, Feuille
from World_observer_Test import World_Observer_test

if __name__ == "__main__":
    rob = Pyroborobo.create("config/test.properties",
                            controller_class=ControllerTest,
                            world_observer_class=World_Observer_test,
                            object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille})
    rob.start()
    rob.update(5000)
    rob.close() 