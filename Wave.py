from random import choices


class Wave:
    def __init__(self, time, *args):
        self.time = time
        self.enemies = []
        self.probas = []
        for tup in args:
            self.enemies.append(tup[0])
            self.probas.append(tup[1])

    def GetEnemy(self):
        return choices(self.enemies, self.probas)[0]
