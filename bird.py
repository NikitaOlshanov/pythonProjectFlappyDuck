import pygame



class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y): # Инициализация объекта класса Bird
        pygame.sprite.Sprite.__init__(self)
        self.flying = False
        self.game_over = False
        self.images = [] #Пустой список
        self.falling = False
        self.FALL_SPEED = 7
        self.index = 0
        self.counter = 0

        for num in range(1, 5): # Загрузка изображений и добавление их в список. Перебор изображений -> создание анимированного спрайта
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # Прямоугольник, соответствующий спрайту птицы
        self.rect.center = [x, y] # Центр прямоугольника
        self.vel = 0 # Скорость птицы
        self.clicked = False # Была ли птица нажата мышью

    def update_animation(self): #Обновление анимации птицы
        flap_cooldown = 5 #Задержка между спрайтами
        self.counter += 1

        if self.counter > flap_cooldown: # При каждом вызове метода update_animation, self.counter увеличивается на 1, и# если достигнута заданная задержка (flap_cooldown), то индекс текущего изображения увеличивается. Если достигнут конец списка self.images, индекс сбрасывается в 0.
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

        # Поворот птицы при полете
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

    def update(self): # Обновление позиции птицы

        if self.flying == True:
            # apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        elif self.falling:  # Обновление позиции при падении
            if self.rect.bottom < 768:
                self.rect.y += self.FALL_SPEED

        if self.game_over == False:
            # Прыжок
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # else:
            # Разворот птицы клювом вниз
            # self.image = pygame.transform.rotate(self.images[self.index], -90)