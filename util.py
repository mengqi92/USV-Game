# coding=utf-8
from __future__ import print_function

from collections import namedtuple
PlaneAction = namedtuple("action", ['stay', 'clockwise', 'angular_speed', 'speed'])
BoardAction = namedtuple("action", ['stay', 'clockwise', 'angular_speed'])
