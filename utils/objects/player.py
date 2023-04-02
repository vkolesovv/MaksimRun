import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, x, files, height):
        pygame.sprite.Sprite.__init__(self)
        self.files = files
        self.index = 0
        self.health = 100
        self.x = x
        self.height = height
        self.image = pygame.image.load(files[self.index]).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(x, height - 199))
        self.inPoop = False

    # Сменить фрейм
    def change(self):
        if self.index < len(self.files) - 1:
            self.index += 1
        else:
            self.index = 0
        self.image = pygame.image.load(self.files[self.index]).convert_alpha()
