from random import choices


class Wave:
    def __init__(self, time, *args):
        self.time = time  # temps à partir de quoi la vague doit arriver
        self.enemies = []  # liste de tous les ennemis qui peuvent spawner durant cette vague
        self.probas = []  # liste des probabilités pour chaque ennemi de spawner
        # les indices de enemies et probas correspondent (probas[0] est la probabilité de enemies[0] de spawn)
        for tup in args:
            self.enemies.append(tup[0])
            self.probas.append(tup[1])

    def GetEnemy(self):
        return choices(self.enemies, self.probas)[0]
