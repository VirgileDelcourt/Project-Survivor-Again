import pygame
from Display import Display


class Projectile(Display):
    Instances = []

    def __init__(self, coord, target, atk, size, speed, pierce, duration):
        super().__init__(None, coord, size * 25)
        self.movement = pygame.Vector2(target) - self.coord
        self.movement.normalize_ip()
        self.movement *= speed * 200
        self.collided = []

        self.power = atk
        self.pierce = pierce
        self.duration = duration

        Projectile.Instances.append(self)

    def Update(self, dt):
        # mouvement
        self.coord += self.movement * dt
        self.duration -= dt
        # on vérifie si le projectile ne devrait pas disparaitre
        if self.duration <= 0:
            Projectile.Instances.remove(self)
        elif self.pierce <= 0:
            Projectile.Instances.remove(self)
        super().Update(dt)
