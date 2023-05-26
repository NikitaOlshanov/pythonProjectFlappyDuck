import pygame



class Button():
    def __init__(self, x, y, image): # Инициализация объекта класса Button
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = pygame.display.set_mode((800, 900))

    def draw(self): # Отрисовка кнопки и возврат действия кнопки
        action = False

        # Координаты мыши
        pos = pygame.mouse.get_pos()

        # Если мышь находится над кнопкой и нажата, действие происходит
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        self.screen.blit(self.image, (self.rect.x, self.rect.y)) # Отрисовка кнопки на поверхности
        return action # Возврат действия, чтобы код мог определить, нажата ли кнопка
