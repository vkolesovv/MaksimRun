import pygame.sprite


class Poop(pygame.sprite.Sprite):
    def __init__(self, file_name, height, group, speed):
        pygame.sprite.Sprite.__init__(self)

        self.height = height
        self.x = 1010

        self.speed = speed

        self.image = pygame.image.load(file_name).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(self.x, self.height - 198))
        self.add(group)
