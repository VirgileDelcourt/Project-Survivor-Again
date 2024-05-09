import Keywords

class Upgrade:
    UpgradesLeft = []
    UpgradesGot = []

    def __init__(self, name, icon, maxlevel):
        self.name = name
        self.icon = icon
        self.level = 0
        self.maxlevel = maxlevel

        Upgrade.UpgradesLeft.append(self)

    def Apply(self, char):
        # /!\ fonction à appeler aprés l'utilisation de la fonction Apply de la sur-classe
        self.level += 1
        if self not in Upgrade.UpgradesGot:
            Upgrade.UpgradesGot.append(self)
        if self.level >= self.maxlevel:
            Upgrade.UpgradesLeft.remove(self)

    def __repr__(self):
        return self.name


class SizeUp(Upgrade):
    def __init__(self):
        super().__init__("Bigger Balls", "tip.png", 9)

    def Apply(self, char):
        if self.level + 1 == 9:
            char.keywords.append(Keywords.SizeToPower)
        else:
            char.Add("proj_size", 0.1)
        super().Apply(char)


class CooldownDown(Upgrade):
    def __init__(self):
        super().__init__("Faster Shoot", "lit.png", 99)

    def Apply(self, char):
        char.Add("maxtimer", -0.01)
        super().Apply(char)


class SpeedUp(Upgrade):
    def __init__(self):
        super().__init__("Quicker Bullet", "fet.png", 99)

    def Apply(self, char):
        char.Add("proj_speed", 0.1)
        super().Apply(char)


class GrowthUp(Upgrade):
    def __init__(self):
        super().__init__("Growth Juice", "pip.png", 10)

    def Apply(self, char):
        char.Add("growth", 0.1)
        super().Apply(char)


class CurseUp(Upgrade):
    def __init__(self):
        super().__init__("Cursed !", "pap.png", 10)

    def Apply(self, char):
        char.Add("curse", 0.1)
        super().Apply(char)


class PowerUp(Upgrade):
    def __init__(self):
        super().__init__("Stronger Balls", "tip.png", 5)

    def Apply(self, char):
        char.Add("power", 0.5 * (self.level + 1))
        super().Apply(char)


class PierceUp(Upgrade):
    def __init__(self):
        super().__init__("Piercing Bullets", "til.png", 10)

    def Apply(self, char):
        char.Add("pierce", 1)
        super().Apply(char)


class MovementUp(Upgrade):
    def __init__(self):
        super().__init__("Cooler Shoes", "fet.png", 10)

    def Apply(self, char):
        char.Add("speed", 0.05)
        super().Apply(char)


class Mitosis(Upgrade):
    def __init__(self):
        super().__init__("Slow and Steady", "til.png", 3)

    def Apply(self, char):
        if self.level + 1 == 3:
            char.keywords.append(Keywords.Mitosis)
        else:
            char.Add("proj_speed", -0.75)
            char.Add("duration", 2)
        super().Apply(char)


class Feed(Upgrade):
    def __init__(self):
        super().__init__("Feeding Bullets", "tip.png", 1)

    def Apply(self, char):
        char.keywords.append(Keywords.Feed)
        super().Apply(char)

# initialisation des variables de classe d'Upgrade
Upgrade.UpgradesGot = []
Upgrade.UpgradesLeft = []
