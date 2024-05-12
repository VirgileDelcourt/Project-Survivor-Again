import pygame

from Projectile import Projectile


class Mitosis:
    def __init__(self):
        self.Set("timer", 2)

    def Update(self, dt):
        self.Add("timer", -dt)
        if self.Get("timer") <= 0:
            keywords = self.Get("keywords")[:]
            keywords.remove(Mitosis)
            Projectile(self.coord, pygame.mouse.get_pos(), self.Get("power"), self.Get("size") / 2, self.Get("speed") * 2,
                       self.Get("basepierce"), self.Get("baseduration") / 2, keywords, self.Get("player"), color="grey")
            self.Add("timer", 2)


class Feed:
    def __init__(self):
        pass

    def Pierce(self):
        self.Add("size", 0.2)
        self.UpdateSize()


class SizeToPower:
    def __init__(self):
        self.Add("power", self.Get("size"))
        if self.Get("size") > 1:
            self.Set("size converted to damage", self.Get("size") - 1)
        else:
            self.Set("size converted to damage", 0)

    def Update(self, dt):
        print(self.Get("size"))
        if self.Get("size converted to damage") != self.Get("size") - 1:
            if self.Get("size") > 1:
                self.Add("power", self.Get("size") - 1 - self.Get("size converted to damage"))
                self.Set("size converted to damage", self.Get("size") - 1)
            else:
                self.Add("power", -self.Get("size converted to damage"))
                self.Set("size converted to damage", 0)
            print(self.Get("size converted to damage"))
        print()


class Boomerang:
    def __init__(self):
        pass

    def Expire(self):
        keywords = self.Get("keywords")[:]
        keywords.remove(Boomerang)
        Projectile(self.coord, self.Get("player").coord, self.Get("power"), self.Get("size"), self.Get("speed"),
                   10, self.Get("lifetime"), keywords, self.Get("player"))
