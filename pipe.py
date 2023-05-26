import pygame



class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position): # Определение/Инициализация класса Pipe
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        self.scroll_speed = 4 #Скорость прокрутки трубы
        self.passed = False
        self.pipe_gap = 200
        # Число позиции указывает на то, какая труба должна идти
        # 1 - Верхняя труба, -1 - нижняя труба
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(self.pipe_gap / 2)]

    def update(self): # Обновление труб и удаление, если она за пределами экрана
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()