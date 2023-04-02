import pygame.sprite


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, filename, player_health, y):
        pygame.sprite.Sprite.__init__(self)

        self.filename = filename
        self.player_health = player_health
        self.image = pygame.image.load(f"{filename}{str(self.player_health)}.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(30, y))

    # Обновить параметры полоски
    def update_bar(self):
        self.image = pygame.image.load(f"{self.filename}{str(self.player_health)}.png").convert_alpha()
