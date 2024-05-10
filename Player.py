import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

from Display import Display
from Projectile import Projectile
from Entity import Entity

stats = {"maxhp": 100,
         "hurt": 0,  # dégâts subits
         "armor": 0,  # réduit les dégâts
         "speed": 1,  # vitesse de déplacement

         "maxtimer": 1,  # délai entre chaque attaque
         "power": 1,  # puissance de chaque projectile
         "proj_size": 1,  # taille de chaque projectile (pourcentage)
         "proj_speed": 1,  # vitesse de chaque projectile (pourcentage)
         "pierce": 1,  # nombre d'ennemis que la balle traverse avant d'expirer
         "duration": 1,  # durée (en seconde) de la balle

         "growth": 1,  # modifie l'exp gagnée (pourcentage)
         "curse": 1}  # modifie le nombre d'ennemis qui apparaissent (pourcentage)


class Player(Display, Entity):
    def __init__(self, image, hp, armor, speed, cooldown, atk, proj_size, proj_speed, pierce, duration, keywords):
        x, y = pygame.display.get_window_size()
        Display.__init__(self, image, (x / 2, y / 2), 50)
        Entity.__init__(self, stats,
                        maxhp=hp,
                        armor=armor,
                        speed=speed,
                        maxtimer=cooldown,
                        power=atk,
                        proj_size=proj_size,
                        proj_speed=proj_speed,
                        pierce=pierce,
                        duration=duration)

        self.timer = cooldown  # temps restant avant la prochaine attaque
        self.keywords = keywords  # modificateurs appliqués sur les projectiles tirés
        self.invincibility = 0  # temps d'invincibilité restant (en seconde)
        self.momentum = pygame.Vector2(0, 0)  # distance à bouger pour cette frame

        self.experience = 0  # experience actuelle
        self.maxexp = 100  # experience requise pour monter de niveau
        self.level = 0  # niveau actuel

    def Damage(self, pow):
        # perd des pv et obtient 1 seconde d'invincibilité
        if self.invincibility <= 0:
            Entity.Damage(self, pow)
            self.invincibility = 1

    def Fire(self):
        # tire un projectile
        pos = pygame.mouse.get_pos()
        Projectile(self.coord, pos, self.Get("power"), self.Get("proj_size"), self.Get("proj_speed"),
                   self.Get("pierce"), self.Get("duration"), self.keywords[:])

    def Update(self, dt):
        # réduit le temps d'invincibilité restant
        if self.invincibility > 0:
            self.invincibility -= dt

        # réduit le temps avant la prochaine attaque
        if self.timer > 0:
            self.timer -= dt
        # tire si l'attaque est prête
        if self.timer <= 0:
            self.Fire()
            self.timer += self.Get("maxtimer")

        # changement du momentum
        keys = pygame.key.get_pressed()
        x, y = 0, 0
        if keys[K_LEFT]:
            x += 1
        if keys[K_RIGHT]:
            x -= 1
        if keys[K_UP]:
            y += 1
        if keys[K_DOWN]:
            y -= 1
        vec = pygame.Vector2(x, y)
        # on ramène le vecteur à une magnitude de 1 (pour que le joueur bouge toujours de 1)
        if (x, y) != (0, 0):
            vec.normalize_ip()
        self.momentum = pygame.Vector2(x, y) * self.Get("speed")

        Display.Update(self, dt)

    def Killed(self, proj, ennemy):
        self.experience += 10 * self.Get("growth")

    def Can_Lvl_Up(self):
        return self.experience >= self.maxexp

    def Level_Up(self, upgrade):
        # /!\ ne check pas si le joueur peut augmenter de niveau
        # gagne l'amélioration donnée
        upgrade.Apply(self)
        # mise à jour de l'exp requise pour monter de niveau
        self.experience -= self.maxexp
        self.maxexp *= 1.05
