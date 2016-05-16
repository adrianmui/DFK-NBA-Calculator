#  DF_Player.py
#  FantasyCalculator
#
#  Created by adrian mui on 4/4/16.
#

class DF_Player:

    def  __init__(self, name, id, position, salary, fantasy_points, instances_exceeded):
        self.name = name
        self.id = id
        self.position = position
        self.salary = salary
        self.fantasy_points = fantasy_points
        self.instances_exceeded = instances_exceeded

    def description(self):
        return self.name + "," + self.id + "," + self.position + "," + self.salary + "," + self.fantasy_points + "," + self.instances_exceeded