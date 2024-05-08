import pygame
from random import choices, randrange

from Display import Display
from Player import Player
from Projectile import Projectile
from Entity import Entity

# les différents bords de l'écran
sides = ["top", "bottom", "left", "the cooler 4th option (right)"]


class Enemy(Display, Entity):
    Instances = []

    def __init__(self, image, hp, atk, speed):
        Display.__init__(self, image, (0, 0), 50)

        # on choisit un bord d'où faire apparaitre l'ennemi
        width, height = pygame.display.get_surface().get_size()
        weights = [width, width, height, height]

        side = choices(sides, weights)[0]
        if side == 'top':
            y = 0
            x = randrange(width - 4)
        elif side == 'bottom':
            y = height - 4
            x = randrange(width - 4)
        elif side == 'left':
            x = 0
            y = randrange(height - 4)
        else:  # étant donné qu'on a ici un else, je peux mettre n'importe quel nom au dernier choix
            x = width - 4
            y = randrange(height - 4)
        self.coord = pygame.Vector2(x, y)

        Entity.__init__(self, [], maxhp=hp, armor=0, speed=speed, atk=atk)

        Enemy.Instances.append(self)

    def Update(self, dt):
        # si l'on ne touche pas le joueur, on avance
        if not self.Collide(Player.Instance):
            movement = Player.Instance.coord - self.coord
            movement.normalize_ip()
            self.coord += movement * dt * 50 * self.Get("speed")
        # sinon on l'attaque
        else:
            Player.Instance.Damage(self.Get("atk"))

        # check pour collisions avec projectiles
        collided = [proj for proj in Projectile.Instances
                    if self.Collide(proj) and self not in proj.collided and proj.pierce >= 1]
        collided.sort(key=lambda var: self.Distance(var))
        for proj in collided:
            # calcul des dégats
            damage = proj.power - self.Get("armor")
            if damage < 0:
                damage = 0
            self.Add("hurt", damage)
            # faire en sorte que l'ennemi ne se fasse pas toucher plusieurs fois par le même projectile
            proj.collided.append(self)
            proj.pierce -= 1
            # logique s'occupant de la mort de l'ennemi
            if self.Get("hp") <= 0:
                Player.Instance.Killed(proj, self)
                Enemy.Instances.remove(self)
                break

        super().Update(dt)
