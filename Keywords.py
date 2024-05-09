import pygame

from Projectile import Projectile


class Mitosis:
    def __init__(self):
        self.Set("timer", 0)

    def Update(self, dt):
        self.Add("timer", -dt)
        if self.Get("timer") <= 0:
            keywords = self.keywords[:]
            keywords.remove(Mitosis)
            Projectile(self.coord, pygame.mouse.get_pos(), self.Get("power"), self.Get("size") / 2, self.Get("speed") * 2,
                       self.Get("basepierce"), self.Get("baseduration") / 2, keywords, color="grey")
            self.Add("timer", 1)
