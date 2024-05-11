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


class Feed:
    def __init__(self):
        pass

    def Pierce(self):
        self.Add("size", 0.2)
        self.UpdateSize()


class SizeToPower:
    def __init__(self):
        self.Add("power", self.Get("size"))
        self.Set("size converted to damage", self.Get("size"))

    def Update(self, dt):
        if self.Get("size converted to damage") != self.Get("size"):
            if self.Get("size") > 0:
                self.Add("power", self.Get("size") - self.Get("size converted to damage"))
                self.Set("size converted to damage", self.Get("size"))
            else:
                self.Add("power", -self.Get("size converted to damage"))
                self.Set("size converted to damage", 0)
