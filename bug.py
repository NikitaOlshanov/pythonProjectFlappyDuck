import pygame



class Bug(pygame.sprite.Sprite):
    def __init__(self, x, y, scroll_speed): # Инициализация объекта класса Bug
        pygame.sprite.Sprite.__init__(self)
        self.images = []  # Пустой список для изображений
        for num in range(1, 4): # Перебор изорбажений -> Создание анимированного спрайта
            img = pygame.image.load(f"img/bug{num}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scroll_speed = scroll_speed # Скорость прокрутки монеты (Движения)
        self.animation_cooldown = 10 # Кулдаун между кадрами анимции
        self.animation_timer = self.animation_cooldown

    def update(self): # Обновление позиции монеты. Если она вышла за пределы экрана - расстрелять его!
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()

        self.animation_timer -= 1 # Процесс анимации монеты. Когда таймер <= 0, значит пора сменить кадр анимации
        if self.animation_timer <= 0: # Увеличивается, чтобы переходить на след. кадр анимации
            self.animation_timer = self.animation_cooldown
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index] # Обновление кадра анимации согласно текущему индексу