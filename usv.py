# coding=utf-8
from __future__ import print_function

from math import sin, cos, pi
from util import BoardAction, rotate, euclidean_distance, manhattan_distance
# from util import PlaneAction, BoardAction


class StaticUSV(object):
    """一个静态的USV类,move方法将会留空,这表示此类USV不可行动"""

    def __init__(self, uid, x, y, env):
        '''每艘USV的独立id,可以用来区分各舰'''
        self.id = uid
        '''env是指当前USV所在的环境,它指向当前游戏中这艘USV所在的Map类实例'''
        self.env = env
        self.x, self.y = x, y
        self.speed = 0.0
        self.angular_speed = 0.0
        self.direction = 0.0
        self.is_enemy = False

    def decision_algorithm(self):
        '''decision_algroithm是指导USV运动的方法,返回一个自定义的action字典'''
        pass

    def move(self):
        '''USV运动的主方法,根据action来调用其它辅助函数完成下一时刻USV位置的计算'''
        pass

    def is_decision_legal(self, decisionX, decisionY):
        '''判断USV决定要去的位置是否合法;在这个基本的函数里,所有舰艇不得走出地图范围,不得走到
        其它舰艇已经占用的位置;友军舰艇不得走到被保护的目标点.'''
        width, height = self.env.width, self.env.height
        if(decisionX < 0 or decisionY < 0 or decisionX > width - 1 or decisionY > height - 1):
            return False

        occupied = False
        for ship in self.env.ships:
            if(ship.id == self.id):
                continue
            shipX, shipY = ship.coordinate()
            if(shipX == decisionX and shipY == decisionY):
                occupied = True

        if(not self.is_enemy):
            tX, tY = self.env.target_coordinate()
            if(tX == decisionX and tY == decisionY):
                occupied = True

        if(occupied):
            return False

        return True

    def turn(self, clockwise):
        '''这一函数描绘本艘USV在一单位时间内如何改变自身方向,因此其作用是在顺时针或逆时针方向上
        增加当前USV角速度的绝对值(角度变化=角速度*1时间单位=角速度的绝对值)'''
        if(clockwise):
            self.direction = (self.direction + self.angular_speed) % 360
        else:
            self.direction = (self.direction - self.angular_speed) % 360

    def coordinate(self):
        '''返回本USV的位置'''
        return self.x, self.y

    def set_as_enemy(self):
        '''将本USV定义为敌方(进攻方)'''
        self.is_enemy = True

    def set_as_friendly(self):
        '''将本USV定义为友军(防守方)'''
        self.is_enemy = False


class BasicPlaneUSV(StaticUSV):
    """基本平面USV, 这个USV可以在瞬间改变自己的角速度和速度, 转动后在对应方向上走动一帧时间*速度的距离"""

    def __init__(self, uid, x, y, env):
        super(BasicPlaneUSV, self).__init__(uid, x, y, env)

    def decision_algorithm(self):
        '''这种USV的action对象有四个属性:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;3.angular_speed角速度;4.speed速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed*t(一帧时间)度,然后前进当前的速度*t的距离'''
        # traveling = PlaneAction(stay=False, clockwise=False, angular_speed=20.0, speed=10.0)
        # anchoring = PlaneAction(stay=True, clockwise=False, angular_speed=0.0, speed=0.0)
        raise NotImplementedError("请覆盖decision_algorithm方法!")

    def move(self):
        action = self.decision_algorithm()
        if(not action.stay):
            self.update_direction(action)
            self.update_speed(action)
            self.update_coordinate()

    def update_direction(self, action):
        self.angular_speed = action.angular_speed
        self.turn(action.clockwise)

    def update_speed(self, action):
        self.speed = action.speed

    def update_coordinate(self):
        self.x -= cos(pi * self.direction / 180) * self.speed
        self.y += sin(pi * self.direction / 180) * self.speed


class OneStepUSV(BasicPlaneUSV):
    """一个简单的USV类,在网格上它一次只能走动一步.每一时间单位,这种USV能够瞬时的改变自己的角速度,然后转动,最后向
    转动后的方向上移动一格."""

    def __init__(self, uid, x, y, env):
        super(OneStepUSV, self).__init__(uid, x, y, env)
        self.speed = 1

    def decision_algorithm(self):
        '''这种USV的action字典有三个参数:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;3.angular_speed角速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed度,然后前进一步.注意由于
        此模型下angular_speed只能为90的倍数'''
        # traveling = BoardAction(stay=False, clockwise=False, angular_speed=20.0)
        # anchoring = BoardAction(stay=True, clockwise=False, angular_speed=0.0)
        raise NotImplementedError("请覆盖decision_algorithm方法!")

    def move(self):
        action = self.decision_algorithm()
        if(not action.stay):
            self.update_direction(action)
            self.update_coordinate()

    def update_coordinate(self):
        if(self.direction == 0.0):
            self.x -= self.speed
        elif(self.direction == 90.0):
            self.y += self.speed
        elif(self.direction == 180.0):
            self.x += self.speed
        elif(self.direction == 270.0):
            self.y -= self.speed
        else:
            raise ValueError(
                "OneStepUSV的direction属性应该是正交角度,然而,得到了 %f 度" % self.direction)
        # print("我是%d号船,我现在走到了(%f,%f)"%(self.id,self.x,self.y))


class SimpleUSV(OneStepUSV):
    '''一个策略简单的USV,派生自OneStepUSV'''
    def __init__(self, uid, x, y, env):
        super(SimpleUSV, self).__init__(uid, x, y, env)

    def decision_algorithm(self):
        if(self.is_enemy):
            return self.attack_decision_algorithm()
        else:
            return self.protection_decision_algorithm()

    def make_decision_by_nearest_position(self, cur_x, cur_y, cur_direction, target):
        '''
        在当前舰艇四个方向邻域中寻找与目标最接近的坐标，作为下一步行动目的地，返回下一步行动

        param:
            cur_x, cur_y: 舰艇当前横纵坐标
            cur_direction: 舰艇当前朝向
            target: 目标舰艇坐标
        return:
            下一步行动 BoardAction 对象
        '''
        # 当前舰艇的四方向邻域坐标
        neighbors = {90: (cur_x, cur_y + 1), 180: (cur_x + 1, cur_y), 270: (cur_x, cur_y - 1), 0: (cur_x - 1, cur_y)}
        # 可供选择的行动策略
        strategy_options = [{'distance': manhattan_distance(target, neighbor), 'next_move': neighbor, 'angular_to_be': angular}
                            for angular, neighbor in neighbors.items()]
        # 寻找与目标最接近的坐标
        nearest_strategies = sorted(strategy_options, key=lambda d: d['distance'])

        for strategy in nearest_strategies:
            if(self.is_decision_legal(*strategy['next_move'])):
                return BoardAction(stay=False,
                                   clockwise=(strategy['angular_to_be'] - cur_direction) > 0,
                                   angular_speed=abs(strategy['angular_to_be'] - cur_direction))

    def attack_decision_algorithm(self):
        '''进攻方策略:在上下左右四个格子中,选择离目标最近的那个格子,如果出现相等就随机选一个;
        如果发现目标格子被其它舰艇占用,选择次近的格子;如果全部被占用,保持不动
        (这不见得是什么高明的策略,即是是防守方保持静止,也很有可能使进攻方进入死循环)'''
        target = self.env.target_coordinate()
        return self.make_decision_by_nearest_position(self.x, self.y, self.direction, target)

    def protection_decision_algorithm(self):
        '''试图出现在进攻方想要出现的那一个格子上,更具体的说,以进攻方的目标格子为"目标",实行进攻方的策略.
        这个测试游戏里面敌舰只有一艘,所以敌人想要去的位置是确定的,如果敌人选择不动,以敌人的位置为目标位置'''

        '''得到敌人的目标位置'''
        enemy = self.env.enemy_ships[0]
        enemy_action = enemy.attack_decision_algorithm()
        if(enemy_action.stay):
            target = enemy.coordinate()
        else:
            enemy_direction = rotate(enemy.direction,
                                     enemy_action.angular_speed if enemy_action.clockwise else -enemy_action.angular_speed)

            enemy_x, enemy_y = enemy.coordinate()
            if(enemy_direction == 0.0):
                target = enemy_x - 1, enemy_y
            elif(enemy_direction == 90.0):
                target = enemy_x, enemy_y + 1
            elif(enemy_direction == 180.0):
                target = enemy_x + 1, enemy_y
            elif(enemy_direction == 270):
                target = enemy_x, enemy_y - 1

        return self.make_decision_by_nearest_position(enemy_x, enemy_y, enemy_direction, target)
