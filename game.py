import pygame
import pygame.mixer
import random

from bird import Bird
from button import Button
from coin import Coin
from bug import Bug
from pipe import Pipe



class Game():
    def __init__(self): # Инициализация объекта класса Game
        pygame.init() # Инициализация всех модулей pygame
        pygame.display.set_caption('Flappy Duck') # Заголовок окна игры
        self.font = pygame.font.SysFont("Montseratt", 50) # Шрифт, размер
        self.white = (255, 255, 255) #Цвет
        # Созадние групп спрайтов для хранения экземпляров классов
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.bug_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock() # Управление фпсом в игре
        self.screen = pygame.display.set_mode((800, 900), pygame.HWSURFACE) # Поверхность с окном игры
        self.fps = 75
        self.screen_width = 800
        self.screen_height = 900

        self.flappy = Bird(100, 450) # Экземпляр класса птички, непосредственно представляет ее
        self.bird_group.add(self.flappy) # Добавление экземпляра self.flappy в группу с птицей

        self.scroll_speed = 4 # Скорость прокрутки игры
        self.ground_scroll = 0 # Смещение земли

        self.pipe_frequency = 2000 # Частота появления труб
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency # Сохраняет время последнего спавна трубы
        self.pass_pipe = False # Прошла ли птица трубу

        self.coin_frequency = 3000
        self.last_coin = pygame.time.get_ticks() - self.coin_frequency

        self.bug_frequency = 15000
        self.last_bug = pygame.time.get_ticks() - self.bug_frequency


        self.bg = pygame.image.load('img/bg.png')
        self.ground_img = pygame.image.load('img/ground.png')
        self.button_img = pygame.image.load('img/restart.png')

        pygame.mixer.music.load('sound/menu.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1) # Циклическое воспроизведение

        self.coin_sound = pygame.mixer.Sound('sound/coin.wav')
        self.coin_sound.set_volume(0.2)

        self.bug_sound = pygame.mixer.Sound('sound/bug.mp3')
        self.bug_sound.set_volume(0.02)

        self.game_over_sound = pygame.mixer.Sound('sound/game_over.mp3')
        self.game_over_sound.set_volume(0.2)

        self.is_boost_active = False # Активирован ли буст
        self.boost_timer = 0

        self.score = 0
        self.high_score = self.load_high_score()  # Загрузка максимального счета из файла



    def load_high_score(self): # Загрузка максимального счета из файла
        try:
            with open("high_score.txt", "r") as file: # Открытие файла, фромат чтения
                return int(file.read()) # Чтение файла и преобразование в целое число
        except FileNotFoundError:
            return 0 # Если файл не найдет, но макс счет = 0


    def save_high_score(self): # Сохранение максимального счета в файл
        with open("high_score.txt", "w") as file: # Открытие файла, формат записи
            file.write(str(self.high_score)) # Преобразование в строку, так как file.write() принимает только строки


    def draw_text(self, text, font, text_col, x, y): # Отрисовка текста на экране
        img = font.render(text, True, text_col) # Создание текста
        self.screen.blit(img, (x, y)) # Отображение на экране


    def reset_game(self): #Сбрасываем параметры при рестарте игры
        self.pipe_group.empty()
        self.flappy.rect.x = 100
        self.flappy.rect.y = int(450)
        self.flappy.falling = False
        self.score = 0
        self.coin_group.empty()
        self.bug_group.empty()
        self.fps = 75
        self.boost_timer = 0
        return self.score


    def run(self): # Основной цикл игры
        self.game_over = False
        self.button = Button(self.screen_width // 2 - 60, self.screen_height // 2 - 40, self.button_img) # Отображение кнопки
        while True: # Бесконечный цикл, выполняется до тех пор, пока игра активна
            self.clock.tick(self.fps) # Задание фпса в игре


            # Отрисовка объектов на экрае
            self.bird_group.update() # Состояние птицы, включая позицию и анимацию
            self.screen.blit(self.bg, (0, 0)) # Отрисовка фона
            self.pipe_group.draw(self.screen) # Отрисовка труб
            self.bird_group.draw(self.screen) # Отрисовка всех птиц
            self.coin_group.draw(self.screen) # Отрисовка монет
            self.bug_group.draw(self.screen) # Отрисовка жуков

            self.screen.blit(self.ground_img, (self.ground_scroll, 768)) # Отрисовка земли + ее перемещения
            self.draw_text(str(self.score), self.font, self.white, 40, 20) # Отрисовка счета

            fps_font = pygame.font.SysFont("Montseratt", 30) # Шрифт для фпс
            fps_text = fps_font.render(f"FPS: {int(self.clock.get_fps())}", True, self.white) # Создание фпс
            self.screen.blit(fps_text, (700, 20)) #Вывод фпс на экран



            if self.is_boost_active: # Логика буста (увеличиваем фпс, постепенно уменьшаем таймер. Когда таймер истекает, возвращаем фпс)
                self.fps = 120
                self.boost_timer -= 1
                if self.boost_timer <= 0:
                    self.fps = 75
                    self.is_boost_active = False


            if self.game_over: #Если игра проиграна
                if self.score > self.high_score:  # Проверка на новый рекорд
                    self.high_score = self.score
                    self.save_high_score()  # Сохранение нового рекорда в файл
                self.draw_text("Game Over", self.font, self.white, 320, 200)
                self.draw_text(f"Score: {self.score}", self.font, self.white, 350, 240)
                self.draw_text(f"High Score: {self.high_score}", self.font, self.white, 305, 280)


                if self.button.draw(): # Проверка на нажатие кнопки
                    self.game_over = False
                    self.score = self.reset_game() # Сброс игры
                    pygame.mixer.music.load('sound/menu.mp3')
                    pygame.mixer.music.play(-1)


            else:


                if self.flappy.flying and not self.game_over: #Если птица летит и игра не окончена
                    self.flappy.update_animation() # Обновление анимации
                    time_now = pygame.time.get_ticks() #Текущее время в милисекундах



                    if time_now - self.last_pipe > self.pipe_frequency: # Проверка, прошло ли достаточно времени с момента спавна последней трубы, чтобы заспавнить новую
                        pipe_height = random.randint(-100, 100) # Генерация высоты трубы в пределах указанного диапазона
                        btm_pipe = Pipe(self.screen_width, int(self.screen_height / 2) + pipe_height, -1) # Создание нижней трубы с учетом положения на экране и движения (-1)
                        top_pipe = Pipe(self.screen_width, int(self.screen_height / 2) + pipe_height, 1) # Создание верхенй трубы с учетом положения на экране и движения (1)
                        self.pipe_group.add(btm_pipe) # Добалвение нижней трубы в группу труб
                        self.pipe_group.add(top_pipe) # Добалвение верхней трубы в группу труб
                        self.last_pipe = time_now # Отслеживание времени последнего спавна трубы
                    self.pipe_group.update() # Обновление всех труб в группе (позиция, состояние)


                    if time_now - self.last_coin > self.coin_frequency: # Проверка, прошло ли достаточно времени с момента спавна последней монеты, чтобы заспавнить новую
                        coin_x = self.screen_width + 200 #Координата х при спавне монеты. Спавн за пределами экрана
                        coin_y = random.randint(200, self.screen_height - 200) #Координата у при спавне монеты
                        coin = Coin(coin_x, coin_y, self.scroll_speed) # Экземпляр монеты с заданными параметрами
                        self.coin_group.add(coin) # Добалвение монеты в группу монет
                        self.last_coin = time_now # Отслеживание времени последнего спавна монеты
                    self.coin_group.update() # Обновление всех монет в группе (позиция, состояние)


                    if time_now - self.last_bug > self.bug_frequency:
                        bug_x = self.screen_width + 200
                        bug_y = random.randint(200, self.screen_height - 200)
                        bug = Bug(bug_x, bug_y, self.scroll_speed)
                        self.bug_group.add(bug)
                        self.last_bug = time_now
                    self.bug_group.update()


                    # Проверка на столкновение птицы с монетой + действия при столкновении
                    if pygame.sprite.spritecollide(self.flappy, self.coin_group, True):
                        self.score += 1
                        self.coin_sound.play()


                    # Проверка на столкновение птицы с жуком + действия при столкновении
                    if pygame.sprite.spritecollide(self.flappy, self.bug_group, True):
                        self.score += 10
                        self.bug_sound.play()
                        self.is_boost_active = True
                        self.boost_timer = 10 * self.fps


                    # Проверка на столкновение птицы с трубами, землей и краем экрана. Остновка игры, полета, активация падения.
                    if pygame.sprite.spritecollide(self.flappy, self.pipe_group, False) or self.flappy.rect.top < 0 or self.flappy.rect.bottom >= 768:
                        self.game_over = True
                        self.flappy.flying = False
                        self.flappy.falling = True


                        if self.flappy.falling: # Если птичка падает, то скидываем ее на 10 пикселей по у вниз, проигрываем звук смэрти и останавливаем музычку
                            self.flappy.rect.y += 10
                        self.game_over_sound.play()
                        pygame.mixer.music.stop()


                    for pipe in self.pipe_group: # Итерация по всем объектам труб
                        if pipe.rect.right < self.flappy.rect.left and not pipe.passed: # Если левая гланица питцы прошла правую ганицу трубы, то труба пройдена и +1 очко
                            pipe.passed = True
                            self.score += 1


                    self.ground_scroll -= self.scroll_speed # Эффект прокрутки земли. Уменьшение значения ground_scroll на величину scroll_speed
                    if abs(self.ground_scroll) > 35: # Когда земля проходит больше чем 35 пикселей, она возвращается в исходное состояние, создание непрерывности.
                        self.ground_scroll = 0



            for event in pygame.event.get(): # Обработка списка всех событий, поулченных из pygame
                if event.type == pygame.QUIT: # Если тип события - выход, то...
                    self.save_high_score()  # Сохранение рекорда перед выходом
                    return # Прерывает функцию run и останавливает игру
                # Если событие - нажание мыши и птица не летит и игра не окончена, то запустить полет птицы
                if event.type == pygame.MOUSEBUTTONDOWN and not self.flappy.flying and not self.game_over:
                    self.flappy.flying = True


            pygame.display.flip() # Обновление ВСЕГО содержимого окна игры на экране