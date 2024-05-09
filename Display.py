import pygame


class Display(pygame.sprite.Sprite):
    def __init__(self, image, coord, radius, color="white"):
        super().__init__()

        if image is not None:
            self.surf = pygame.image.load(image).convert_alpha()
        else:
            self.surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.surf, color, (radius, radius), radius)
        self.rect = self.surf.get_rect(center=coord)

        self.image = image
        self.color = color

        self.coord = pygame.Vector2(coord)
        self.radius = radius

    def Distance(self, display):
        return (self.coord - display.coord).magnitude()

    def Collide(self, display):
        if self.Distance(display) <= self.radius + display.radius:
            return True
        else:
            return False

    def Load_Image(self, image):
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(center=self.coord)

    def Update(self, dt):
        self.rect.center = self.coord

    def Change_Radius(self, newradius):
        if self.image is None:
            self.radius = newradius
            self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.surf, self.color, (self.radius, self.radius), self.radius)
            self.rect = self.surf.get_rect(center=self.coord)
        else:
            print("Tried to change size of a Display with an image (not implemented yet)")
