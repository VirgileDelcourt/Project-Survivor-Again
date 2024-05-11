_stats = {"maxhp": 0,
          "armor": 0,
          "speed": 1}


class Entity:
    def __init__(self, base_stats, **stats):
        self.stats = {}
        for stat in _stats:
            if stat not in stats:
                stats[stat] = _stats[stat]
        for key in stats:
            self.stats[key] = stats[key]
            self.stats["base" + key] = self.stats[key]
        for key in base_stats:
            if key not in self.stats:
                self.stats[key] = base_stats[key]
                self.stats["base" + key] = self.stats[key]

        self.Set("hurt", 0)

    def Get(self, stat):
        if stat == "hp":
            return self.Get("maxhp") - self.Get("hurt")
        return self.stats[stat]

    def Set(self, stat, n):
        self.stats[stat] = n

    def Add(self, stat, n):
        self.stats[stat] += n

    def Get_State(self):
        if self.Get("hp") <= 0:
            return False
        else:
            return self.Get("hp")

    def Damage(self, pow):
        pow -= self.Get("armor")
        if pow < 0:
            pow = 0
        self.Add("hurt", pow)
