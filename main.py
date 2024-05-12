import pygame
from pygame.locals import QUIT, K_1, K_2, K_3, K_KP1, K_KP2, K_KP3
from random import random, shuffle
from time import time

from Display import Display
from Player import Player
from Enemy import Enemy, Newbie, Floatie, Shootie
from Projectile import Projectile
import Upgrade as m_Upgrade
from Upgrade import Upgrade
import Keywords
from Wave import Wave

pygame.init()

# initialisation de la fenêtre et du joueur
dimx, dimy = 1080, 720
window = pygame.display.set_mode((dimx, dimy))
player = Player("pip.png", 100, 0, 1, 1, 2.5, 1, 2, 2, 2, 1, [])
waves = [Wave(0, (Newbie, 1)),
         Wave(60, (Newbie, 0.9), (Shootie, 0.1)),
         Wave(100, (Newbie, 1)),
         Wave(120, (Newbie, 0.7), (Floatie, 0.3)),
         Wave(140, (Floatie, 1)),
         Wave(180, (Newbie, 0.5), (Floatie, 0.5)),
         Wave(200, (Newbie, 1))]
currentwave = 0

# creation d'un masque pour l'écran de montee de niveau
tint = pygame.Surface((dimx, dimy))
tint.set_alpha(128)
tint.fill("grey")
font = pygame.font.Font(None, 40)
biggerfont = pygame.font.Font(None, 60)

# initialisation de chaque upgrade (pour remplir Upgrade.UpgradesLeft)
for nom in dir(m_Upgrade):
    if not nom.startswith('__') and nom != "Upgrade" and nom != "Keywords":
        classe = getattr(m_Upgrade, nom)
        classe()

# initialisation des listes necessaires a l'affichage de l'ecran de montee de niveau
upgrades_to_chose = []
upgrades_displays = [Display(None, (0, 0), 0), Display(None, (0, 0), 0), Display(None, (0, 0), 0)]

running = True
last = time()
timer = 0
while running:
    # calcul du temps depuis la derniere mise à jour
    dt = time() - last
    last = time()

    # on vérifie si le joueur veut quitter le jeu
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    # ici on s'occupe de la montee de niveau
    if player.Can_Lvl_Up():
        # on vérifie si on n'a pas encore choisi d'Upgrade
        if not upgrades_to_chose:
            # creation des choix d'Upgrade
            temp = Upgrade.UpgradesLeft[:]
            for _ in range(min(len(temp), 3)):
                shuffle(temp)
                upgrades_to_chose.append(temp.pop(0))
        # on vérifie si le joueur a choisi une Upgrade
        keys = pygame.key.get_pressed()
        if keys[K_1] or keys[K_KP1]:
            player.Level_Up(upgrades_to_chose[0])
            upgrades_to_chose = []
        elif keys[K_2] or keys[K_KP2]:
            player.Level_Up(upgrades_to_chose[1])
            upgrades_to_chose = []
        elif keys[K_3] or keys[K_KP3]:
            player.Level_Up(upgrades_to_chose[2])
            upgrades_to_chose = []

        # on stoppe le temps pendant la montée de niveau
        dt = 0

    timer += dt

    # spawn des ennemis (plus il y en a, moins on en spawn)
    curse = player.Get("curse") * ((timer / 300) + 1)
    if len(Enemy.Instances) == 0 \
            or random() < (1 / (len(Enemy.Instances) + 1)) * dt * 30 * curse:
        waves[currentwave].GetEnemy()(player, curse)
    if currentwave + 1 != len(waves) and timer >= waves[currentwave + 1].time:
        currentwave += 1

    # mise à jour de l'écran et de chaque entité
    window.fill("light green")
    player.Update(dt)
    # si le joueur bouge, on bouge toutes les autres entités
    if player.momentum != (0, 0):
        delta = player.momentum * dt * 150 * player.Get("speed")
        for display in Projectile.Instances + Enemy.Instances:
            display.coord += delta
    for enemy in Enemy.Instances:
        enemy.Update(dt)
        window.blit(enemy.surf, enemy.rect)
    for proj in Projectile.Instances:
        proj.Update(dt)
        window.blit(proj.surf, proj.rect)
    window.blit(player.surf, player.rect)

    # creation de la barre de vie
    if player.Get_State():
        pygame.draw.rect(window, "white",
                         [(dimx / 2) - (player.Get("maxhp") / 2), (dimy / 2) + 50,
                          player.Get("maxhp"), 20])
        pygame.draw.rect(window, "red",
                         [(dimx / 2) - (player.Get("maxhp") / 2), (dimy / 2) + 50, player.Get("hp"),
                          20])

    # creation de la barre d'exp
    exp_percent = player.experience / player.maxexp
    pygame.draw.rect(window, "white", [0, dimy - 30, dimx, 30])
    pygame.draw.rect(window, "blue", [0, dimy - 30, dimx * exp_percent, 30])

    # creation du timer
    t = ""
    if timer // 60 < 10:
        t += "0" + str(int(timer // 60))
    else:
        t += str(int(timer // 60))
    t += ":"
    if timer % 60 < 10:
        t += "0" + str(int(timer % 60))
    else:
        t += str(int(timer % 60))
    text = biggerfont.render(t, 1, "black")
    window.blit(text, (dimx / 2, 5))

    # creation de l'ecran de montee de niveau
    if upgrades_to_chose:
        window.blit(tint, (0, 0))
        for i in range(len(upgrades_to_chose)):
            upgrade = upgrades_to_chose[i]
            display = upgrades_displays[i]

            display.Load_Image(upgrade.icon)
            display.coord = pygame.Vector2(dimx * ((i + 1) / 4), 200)
            window.blit(display.surf, display.rect)

            text = font.render("[" + str(i + 1) + "] " + upgrade.name, 1, "black")
            window.blit(text, (dimx * ((i + 1) / 4) - 100, 350))

            text = font.render("Level " + str(upgrade.level + 1) + " / " + str(upgrade.maxlevel), 1, "black")
            window.blit(text, (dimx * ((i + 1) / 4) - 100, 450))

    # mise à jour de la fenetre
    pygame.display.flip()

    # si le joueur est mort, on quitte
    if not player.Get_State():
        running = False
    # s'il n'y a plus d'Upgrade restante, on quitte (pour eviter le crash)
    elif not Upgrade.UpgradesLeft:
        running = False
pygame.quit()
