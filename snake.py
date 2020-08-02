import arcade
import random
import time
from math import floor

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
TITLE = 'Snake'
radius = 10
eatRadius = 5
IsCollized = False
#delta_time = 1
x = 0

class MyGame(arcade.View):
    """ Главный класс приложения. """

    def __init__(self, width, height, title):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        #В какую сторону движется
        self.up = False
        self.down = False
        self.right = False
        self.left = False

        self.x = 250
        self.y = 250

        self.counter = 0

        #Координаты еды
        self.ateX1 = 0
        self.ateY1 = 0

        #Коодинаты предыдущего поедания, чтобы увеличить змею и не рисковать выйти за пределы массива
        self.ateXPrev = 0
        self.ateYPrev = 0

        self.ate = False
        self.ate1 = False

        self.eatXPos = random.randint (5,SCREEN_WIDTH - 5)
        self.eatYPos = random.randint (5,SCREEN_HEIGHT - 5)

        self.xCollision = True
        self.yCollision = False

        self.speeder = 4

        self.bodyList = []
        self.i = 0
        self.j = 3

        self.zU = 0
        self.zD = 0
        self.zL = 0
        self.zR = 0

        self.slower = 0
        #score + 4
        self.act = 4
        self.fastEatProtector = 0

        self.score = 0
        # Регулируем сложность
        self.diffic = 0

        # Координы сегментов змеи в самом начале игры
        self.XbodyCoordinates = [10,30,50,70]
        self.YbodyCoordinates = [100,100,100,100]

        self.IsGone = False

    def setup(self):
        pass

    def on_draw(self):
        # Добавляем координты места, где змея поела. В этом месте создаем новый сегмент тела
        self.body_list = arcade.ShapeElementList()
        if self.ate == True:
            self.ate = False
            body = arcade.create_ellipse_filled(self.ateXPrev, self.ateYPrev, radius, radius, arcade.color.WHITE)
            self.body_list.append(body)

        # Рисуем тело в самом начале игры
        for self.i in range(0, self.act):
            body = arcade.create_ellipse_filled(self.XbodyCoordinates[self.i], self.YbodyCoordinates[self.i], radius, radius, arcade.color.WHITE)
            self.body_list.append(body)


        arcade.start_render()
        arcade.draw_text("Счёт: " + str(self.score), 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 10)
        self.body_list.draw()
        arcade.draw_circle_filled(self.eatXPos, self.eatYPos, eatRadius, arcade.color.RED)

    def on_update(self, delta_time):
# Контроль столконовения змеи с краями карты
        if (self.x >= SCREEN_WIDTH - radius) and (self.left == False):
            self.xCollision = True
        elif (self.x <= 0 + radius) and (self.right == False):
            self.xCollision = True
        else:
            self.xCollision = False

        if (self.y >= SCREEN_HEIGHT - radius) and (self.down == False):
            self.yCollision = True
        elif (self.y <= 0 + radius) and (self.up == False):
            self.yCollision = True
        else:
            self.yCollision = False

# Увеличение скорости со времением
        if self.score <= 10:
            self.diffic = 1/30
        if 10 < self.score <= 15:
            self.diffic = 1/45
        if 15 < self.score <= 20:
            self.diffic = 1/60
        if 20 < self.score <= 25:
            self.diffic = 1/75
        if 25 < self.score:
            self.diffic = 1/90

# Описание движения всех сегментов змеи, кроме головы
        if self.slower % self.diffic == 0:
         # балансируем скорость игры

            if self.up == True:
                if self.zU < self.act + 1:
                    time.sleep(self.diffic)
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2] + radius * 2
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2]
                    self.zU += 1
                else:
                    self.zU = 0

            if self.down == True:
                if self.zU < self.act+1:
                    time.sleep(self.diffic)
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2] - radius * 2
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2]
                    self.zU += 1
                else:
                    self.zU = 0

            if self.left == True:
                if self.zU < self.act+1:
                    time.sleep(self.diffic)
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2]
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2] - radius * 2
                    self.zU += 1
                else:
                    self.zU = 0

            if self.right == True:
                if self.zU < self.act:
                    time.sleep(self.diffic)
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2]
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2] + radius * 2
                    self.zU += 1
                else:
                    self.zU = 0
            self.IsGone = True

        # Проверяем, чтобы координаты пищи не находились на змее, если это так, то генерируем новые координаты еды
        for self.z in range (0, self.act - 1):
            if (self.YbodyCoordinates[self.z] < self.eatYPos + radius + eatRadius + 5) and (self.YbodyCoordinates[self.z] > self.eatYPos - radius - eatRadius - 5) and (self.XbodyCoordinates[self.z] < self.eatXPos + radius + eatRadius + 5) and (self.XbodyCoordinates[self.z] > self.eatXPos - radius - eatRadius - 5):
                while (self.YbodyCoordinates[self.z] < self.eatYPos + radius + eatRadius + 5) and (self.YbodyCoordinates[self.z] > self.eatYPos - radius - eatRadius - 5) and (self.XbodyCoordinates[self.z] < self.eatXPos + radius + eatRadius + 5) and (self.XbodyCoordinates[self.z] > self.eatXPos - radius - eatRadius - 5):
                    self.eatXPos = random.randint (50,SCREEN_WIDTH - 50)
                    self.eatYPos = random.randint (50,SCREEN_HEIGHT - 50)
                self.ate = True
                self.act += 1
                self.score += 1
                self.XbodyCoordinates.append(0)
                self.YbodyCoordinates.append(0)

        # Проверяем змею на самоукус
        for self.z in range (0, self.act - 1):
            for self.i in range (0, self.act - 1):
                print (self.XbodyCoordinates[self.i],' ', self.XbodyCoordinates[self.z], ' ',self.YbodyCoordinates[self.i], ' ', self.YbodyCoordinates[self.z] )
                if (self.z != self.i) and (self.XbodyCoordinates[self.i] == self.XbodyCoordinates[self.z]) and (self.YbodyCoordinates[self.i] == self.YbodyCoordinates[self.z]):
                    game_over = GameOverView(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
                    self.window.show_view(game_over)

        if self.XbodyCoordinates[0] > SCREEN_WIDTH or self.YbodyCoordinates[0] > SCREEN_HEIGHT or self.XbodyCoordinates[0] < 0 or self.YbodyCoordinates[0] < 0:
            IsCollized = True
            game_over = GameOverView(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
            self.window.show_view(game_over)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            pass

        if symbol == arcade.key.DOWN:
            pass

        if symbol == arcade.key.RIGHT:
            pass

        if symbol == arcade.key.LEFT:
            pass

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.UP and self.IsGone == True:
            if self.down == False:
                self.up = True
                self.down = False
                self.right = False
                self.left = False
                self.IsGone == False

        if symbol == arcade.key.DOWN and self.IsGone == True:
            if self.up == False:
                self.up = False
                self.down = True
                self.right = False
                self.left = False
                self.IsGone == False

        if symbol == arcade.key.RIGHT and self.IsGone == True:
            if self.left == False:
                self.left = False
                self.up = False
                self.down = False
                self.right = True
                self.left = False
                self.IsGone == False

        if symbol == arcade.key.LEFT and self.IsGone == True:
            if self.right == False:
                self.up = False
                self.down = False
                self.right = False
                self.left = True
                self.IsGone == False

class GameIntroView(arcade.View):
    def __init__(self, width, height, title):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Нажмите пробел, чтобы начать игру", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
            self.window.show_view(game)

class GameOverView(arcade.View):
    def __init__(self, width, height, title):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Игра окончена", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
            self.window.show_view(game)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    menu_view = GameIntroView(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
