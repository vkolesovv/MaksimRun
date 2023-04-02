import random
import pygame
import utils


# Ну типо по приколу
def log(context="I", message="No message"):
    match context:
        case "I":
            print(f"[INFO]: {message}")
        case "W":
            print(f"[WARNING]: {message}")
        case "E":
            print(f"[ERROR]: {message}")


class MaksimRun:
    def __init__(self, size, fps, font):

        # Всякие параметры

        self.isPlayerJump = False
        self.score = 0
        self.size = size
        self.running = True
        self.fps = fps
        self.jump_strength = 5
        self.raw_speed = 8
        self.speed = self.raw_speed
        self.clock = pygame.time.Clock()

        self.width = self.size[0]
        self.height = self.size[1]

        # Инициализация всякой пайгеймерской вещи

        pygame.init()

        self.step_in_poop = pygame.mixer.Sound("assets/sounds/step_in_poop.mp3")

        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Максим ран")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.bmp"))

        self.font_name = font

        self.font = pygame.font.Font(font, 48)

        self.score_text = self.font.render(f"Ваш счет: {str(self.score)}", True, utils.GREEN)
        self.death_text = self.font.render("Ты весь в говне!"
                                           " Нажми на пробел, чтобы начать игру заново", True, utils.RED)

        # Создаю игрока, группу говна и полоску здоровья

        self.player = utils.Player(40, ["assets/images/man/man22.png",
                                        "assets/images/man/man32.png"], self.height)

        self.poops = pygame.sprite.Group()
        self.peas = pygame.sprite.Group()
        self.health_bar = utils.HealthBar("assets/images/health_bar/b", self.player.health, self.height - 50)

        if self.player.inPoop:
            self.speed = self.raw_speed // 2
            log("I", "Is in poop")

        pygame.time.set_timer(utils.CHANGE_MAN_EVENT, 2000 // self.speed)
        pygame.time.set_timer(utils.ADD_SCORE_EVENT, 500)

        # Главный цикл
        self.draw()

    def events(self, events, isDeath):
        for event in events:

            if isDeath:
                # Если хочет выйти, отключаю игру
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = False
                        MaksimRun(self.size, self.fps, self.font_name)

            else:
                # Если хочет выйти, отключаю игру
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    # Если нажал на пробел, игрок прыгает
                    if event.key == pygame.K_SPACE:
                        if not self.player.inPoop:
                            self.isPlayerJump = True
                        else:
                            log(message="Игрок попытался прыгнуть, но он в говне")
                            self.step_in_poop.play()

                # Пора менять картинку
                elif event.type == utils.CHANGE_MAN_EVENT:
                    self.player.change()

                # Пора начислять очко
                elif event.type == utils.ADD_SCORE_EVENT:
                    self.score += 1
                    self.score_text = self.font.render(f"Ваш счет: {str(self.score)}", True, utils.GREEN)

                    # Если кол-во очков кратно 50
                    if not self.score % 50:
                        log("I", f"Score - {self.score}")
                        self.raw_speed += 2

                        # Повышаю скорость смены картинки игрока
                        pygame.time.set_timer(utils.CHANGE_MAN_EVENT, 2000 // self.speed)

    def draw(self):
        jump_count = 13
        while self.running:
            if self.player.health > 0:
                self.speed = self.raw_speed

                # Если челик в говне
                if self.player.inPoop:
                    self.speed = 1

                    if random.randint(0, 100) < 5:
                        pygame.time.set_timer(utils.CHANGE_MAN_EVENT, 2000 // self.speed)

                        damage = random.randint(2, 5)
                        if self.player.health - damage > 0:
                            self.player.health -= damage
                        else:
                            self.player.health = 0

                        self.health_bar.player_health = self.player.health
                        self.health_bar.update_bar()
                # Если не в говне
                else:
                    self.speed = self.raw_speed

                    if random.randint(0, 100) < 5:
                        pygame.time.set_timer(utils.CHANGE_MAN_EVENT, 2000 // self.speed)

                self.events(pygame.event.get(), False)

                # Если челик прыгает
                if self.isPlayerJump:
                    if jump_count >= -13:
                        if jump_count < 0:
                            self.player.rect.y += (jump_count ** 2) / 3  # Вниз
                        else:
                            self.player.rect.y -= (jump_count ** 2) / 3  # Вверх
                        jump_count -= 1
                    else:
                        self.isPlayerJump = False
                        jump_count = 13

                # Хрень всякую отрисовываю
                self.screen.fill(utils.SKY)
                pygame.draw.rect(self.screen, utils.GRAY, (0, self.height - 200, 1000, 200))

                self.screen.blit(self.player.image, self.player.rect)

                self.screen.blit(self.score_text, (750, 10))
                self.screen.blit(self.health_bar.image, self.health_bar.rect)

                # С некоторым шансом вызываю говно
                if random.randrange(0, 100) < 0.2:
                    self.create_poop(self.poops)

                # С некоторым шансом вызываю горох
                if random.randrange(0, 100) < 0:
                    self.create_peas(self.peas)

                # Отрисовываю говно и горох
                self.poops.draw(self.screen)
                self.peas.draw(self.screen)

                # Двигаю говно и горох
                for i in self.poops:
                    i.rect.x -= self.speed

                for i in self.peas:
                    i.rect.x -= self.speed

                self.checkIfCollide()

                # Обновление

                pygame.display.update()
                self.clock.tick(self.fps)

                self.poops.update(self.height)

            # Если игрок мертв
            else:
                self.events(pygame.event.get(), True)
                self.screen.fill(utils.SKY)
                pygame.draw.rect(self.screen, utils.GRAY, (0, self.height - 200, 1000, 200))

                self.screen.blit(self.death_text, self.death_text.get_rect(center=(self.width // 2,
                                                                                   self.height // 2)))

                pygame.display.update()
                self.clock.tick(self.fps)

    def create_poop(self, group):

        # Прохожусь по всему говну
        for i in self.poops:
            # Если говно ещё почти ничего не прошло, не надо не перемещать, не создавать новый экземпляр
            if i.rect.x in range(850, 1500):
                return i

            # Если ушло влево за границы
            elif i.rect.x < 0:
                # Перемещаю на примерную исходную точку
                i.rect.x = random.randint(1010, 1500)
                return i

        # Эх, придётся спавнить новое
        poop = utils.Poop("assets/images/poop.png", self.height, group, self.speed)

        return poop

    def create_peas(self, group):
        for i in self.peas:
            if i.rect.x in range(850, 1500):
                return i
            elif i.rect.x < 0:
                i.rect.x = random.randint(1010, 1500)
                return i

        peas = utils.Peas("assets/images/peas.png", self.height, group)
        return peas

    def checkIfCollide(self):
        for poop in self.poops:
            if self.player.rect.collidepoint(poop.rect.center):

                if not self.player.inPoop:
                    self.step_in_poop.play()
                    self.player.inPoop = True
                return

        self.player.inPoop = False


if __name__ == "__main__":
    MaksimRun(size=(1000, 600), fps=30, font=None)
else:
    log("W", "__name__ не __main__. Зачем было так запускать?")
