import pygame.sprite


class Peas(pygame.sprite.Sprite):
    def __init__(self, filename, height, group):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(1020, height - 300))

        self.add(group)
