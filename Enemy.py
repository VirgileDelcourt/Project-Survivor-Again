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

    def __init__(self, image, hp, atk, speed, exp, player: Player, angle=0):
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
        self.angle = angle

        Entity.__init__(self, {}, maxhp=hp, armor=0, speed=speed, atk=atk, exp=exp)
        self._player_ref: Player = player
        Enemy.Instances.append(self)

    def Update(self, dt):
        # si l'on ne touche pas le joueur, on avance
        if not self.Collide(self._player_ref):
            movement = self._player_ref.coord - self.coord
            movement.normalize_ip()
            movement = movement.rotate(self.angle)
            self.coord += movement * dt * 50 * self.Get("speed")
        # sinon on l'attaque
        else:
            self._player_ref.Damage(self.Get("atk"))

        # check pour collisions avec projectiles
        collided = [proj for proj in Projectile.Instances
                    if self.Collide(proj) and self not in proj.collided and proj.Get("pierce") >= 1]
        collided.sort(key=lambda var: self.Distance(var))
        for proj in collided:
            # calcul des dégats
            damage = proj.Get("power") - self.Get("armor")
            if damage < 0:
                damage = 0
            self.Add("hurt", damage)
            # faire en sorte que l'ennemi ne se fasse pas toucher plusieurs fois par le même projectile
            proj.collided.append(self)
            proj.Add("pierce", -1)
            for keyword in proj.keywords_pierce:
                keyword.Pierce(proj)
            # logique s'occupant de la mort de l'ennemi
            if self.Get("hp") <= 0:
                self._player_ref.Killed(proj, self)
                Enemy.Instances.remove(self)
                break

        super().Update(dt)


class Newbie(Enemy):
    def __init__(self, player, curse):
        super().__init__("pap.png", int(5 * curse), int(10 * curse), player.Get("curse"), 10, player=player)


class Floatie(Enemy):
    def __init__(self, player, curse):
        super().__init__("bird.png", int(4 * curse), int(10 * curse), 2 * player.Get("curse"), 10,
                         player=player, angle=70)


class Shootie(Enemy):
    def __init__(self, player, curse):
        super().__init__("lit.png", int(2 * curse), int(curse), 0.5 * player.Get("curse"), 15,
                         player=player, angle=-85)
        self.timer = 2

    def Update(self, dt):
        super().Update(dt)
        if self.Get("hp") > 0:
            if self.timer > 0:
                self.timer -= dt
            else:
                EnemyProj(self._player_ref, self.Get("atk"), tuple(self.coord))
                self.timer += 2


class EnemyProj(Enemy):
    def __init__(self, player, curse, coord):
        super().__init__(None, 1, int(5 * curse), 0, 0, player=player)
        self.coord = pygame.Vector2(coord)
        self.color=pygame.Color("#d3201cff")
        self.radius = 30
        self.movement = player.coord - self.coord
        self.movement.normalize_ip()
        self.movement *= curse * 100

        self.Draw()

    def Update(self, dt):
        self.coord += self.movement * dt
        super().Update(dt)
    def Draw(self):
        border = 10
        width = 2 * self.radius
        pygame.draw.rect(self.surf, pygame.Color(0, 0, 0), rect=(0, 0, width, width))
        pygame.draw.rect(self.surf, self.color, rect=(border, border, width - 2 * border, width - 2 * border))
        pygame.draw.rect(self.surf, "white", rect=(width // 4, width // 4, width // 4, width // 4))
