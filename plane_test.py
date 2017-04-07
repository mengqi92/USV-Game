#coding:utf-8
from __future__ import print_function

from game import BasicGUIGame
from map_ import BasicMap
from usv import BasicPlaneUSV
from util import PlaneAction


class MyUSV(BasicPlaneUSV):
  '''一个策略简单的USV,派生自OneStepUSV'''
  def __init__(self, uid, x, y, env):
    super(MyUSV, self).__init__(uid, x, y, env)

  def decision_algorithm(self):
    return PlaneAction(stay=False, clockwise=False, angular_speed=2.0, speed=1)

if __name__ == '__main__':
    '''开始游戏'''
    test_map = BasicMap(100, 100)
    test_map.set_target(50, 50)
    # print(test_map)

    test_friendly_ship = MyUSV(uid=0,x=50, y=80, env=test_map)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)

    game = BasicGUIGame()
    game.set_map(test_map)
    game.start()
