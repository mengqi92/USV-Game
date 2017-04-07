# coding=utf-8
from __future__ import print_function

from collections import namedtuple

PlaneAction = namedtuple("action", ['stay', 'clockwise', 'angular_speed', 'speed'])
BoardAction = namedtuple("action", ['stay', 'clockwise', 'angular_speed'])


def rotate(original_direction, rotation_degrees):
    return (original_direction + rotation_degrees) % 360


def euclidean_distance(position1, position2):
    '''计算两点的欧式距离'''
    x1, y1 = position1
    x2, y2 = position2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def manhattan_distance(position1, position2):
    '''计算两点之间的曼哈顿距离（棋盘距离）'''
    x1, y1 = position1
    x2, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)
