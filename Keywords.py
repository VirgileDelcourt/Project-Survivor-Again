import pygame

from Projectile import Projectile


class Mitosis:
    def __init__(self):
        print("initied")
        self.Set("timer", 0)

    def Update(self, dt):
        self.Add("timer", -dt)
        print(self.Get("timer"))
        if self.Get("timer") <= 0:
            keywords = self.keywords[:]
            keywords.remove(Mitosis)
            Projectile(self.coord, pygame.mouse.get_pos(), self.Get("power"), self.Get("size"), self.Get("speed"),
                       self.Get("basepierce"), self.Get("baseduration"), keywords)
            self.Add("timer", 1)
