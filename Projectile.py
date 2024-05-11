import pygame

from Display import Display
from Entity import Entity


class Projectile(Display, Entity):
    Instances = []

    def __init__(self, coord, target, atk, size, speed, pierce, duration, keywords, player, **kwargs):
        if "color" in kwargs:
            color = kwargs["color"]
        else:
            color = "gray"
        Display.__init__(self, None, coord, size * 25, color)
        self.Draw()
        self.movement = pygame.Vector2(target) - self.coord
        self.movement.normalize_ip()
        self.movement *= speed * 200
        self.collided = []

        Entity.__init__(self, [], power=atk, pierce=pierce, duration=duration,
                        speed=speed, size=size,
                        keywords=keywords, player=player, lifetime=0)

        for keyword in keywords:
            keyword.__init__(self)
        self.keywords_update = [C for C in keywords if hasattr(C, 'Update') and callable(C.Update)]
        self.keywords_expire = [C for C in keywords if hasattr(C, 'Expire') and callable(C.Expire)]
        self.keywords_pierce = [C for C in keywords if hasattr(C, 'Pierce') and callable(C.Pierce)]
        self.keywords_kill = [C for C in keywords if hasattr(C, 'Kill') and callable(C.Kill)]

        Projectile.Instances.append(self)

    def Update(self, dt):
        # mouvement
        self.coord += self.movement * dt
        self.Add("duration", -dt)
        self.Add("lifetime", dt)
        # on vérifie si le projectile ne devrait pas disparaitre
        if self.Get("duration") <= 0 or self.Get("pierce") <= 0:
            Projectile.Instances.remove(self)
            for keyword in self.keywords_expire:
                keyword.Expire(self)
        else:
            for keyword in self.keywords_update:
                keyword.Update(self, dt)
        super().Update(dt)

    def UpdateSize(self):
        self.Change_Radius(25 * self.Get("size"))

    def Draw(self):
        border = 10
        width = 2 * self.radius
        pygame.draw.rect(self.surf, pygame.Color(0, 0, 0), rect=(0, 0, width, width))
        pygame.draw.rect(self.surf, self.color, rect=(border, border, width - 2 * border, width - 2 * border))
        pygame.draw.rect(self.surf, "white", rect=(width // 4, width // 4, width // 4, width // 4))
        # pygame.draw.circle(self.surf, self.color, (self.radius, self.radius), self.radius)

    def Change_Radius(self, newradius):
        self.radius = newradius
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.Draw()
        self.rect = self.surf.get_rect(center=self.coord)
