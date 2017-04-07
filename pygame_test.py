#coding:utf-8
from __future__ import print_function

from game import BasicGUIGame
from map_ import BasicMap
from usv import OneStepUSV, SimpleUSV

if __name__ == '__main__':
    '''开始游戏'''
    test_map = BasicMap(20, 15)
    test_map.set_target(4, 4)
    # print(test_map)

    ship_xs, ship_ys = [5, 4, 5, 6, 5, 7, 7, 7], [5, 5, 4, 4, 6, 4, 5, 6]
    for uid, x, y in zip(range(8), ship_xs, ship_ys):
        test_friendly_ship = SimpleUSV(uid, x, y, env=test_map)
        test_friendly_ship.set_as_friendly()
        test_map.add_ship(test_friendly_ship)

    test_enemy_ship = SimpleUSV(uid=8, x=10, y=10, env=test_map)
    test_enemy_ship.set_as_enemy()
    test_map.add_ship(test_enemy_ship)
    # print(test_map)

    game = BasicGUIGame()
    game.set_map(test_map)
    game.start()
