import arcade
import random
from math import floor

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
radius = 10
eatRadius = 5
#delta_time = 1
x = 0

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)
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

        self.score = 0
        # Регулируем сложность
        self.diffic = 0

        # Координы сегментов змеи в самом начале игры
        self.XbodyCoordinates = [10,30,50,70]
        self.YbodyCoordinates = [100,100,100,100]

    def setup(self):
        pass

    def on_draw(self):
        # Добавляем координты места, где змея поела. В этом месте создаем новый сегмент тела
        self.body_list = arcade.ShapeElementList()
        if self.ate == True:
            self.XbodyCoordinates.append(self.ateXPrev)
            self.YbodyCoordinates.append(self.ateYPrev)
            self.ate = False
            body = arcade.create_ellipse_filled(self.ateXPrev, self.ateYPrev, radius, radius, arcade.color.DARK_BLUE)
            self.body_list.append(body)

        # Рисуем тело в самом начале игры
        for self.i in range(0, self.act):
            body = arcade.create_ellipse_filled(self.XbodyCoordinates[self.i], self.YbodyCoordinates[self.i], radius, radius, arcade.color.DARK_BLUE)
            self.body_list.append(body)


        arcade.start_render()
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
            self.diffic = 8
        if 10 < self.score <= 15:
            self.diffic = 6
        if 15 < self.score <= 20:
            self.diffic = 5
        if 20 < self.score <= 25:
            self.diffic = 4
        if 25 < self.score:
            self.diffic = 3
# Описание движения всех сегментов змеи, кроме головы
        if self.slower % self.diffic == 0: # балансируем скорость игры

            if self.up == True:
                if self.zU < self.act + 1:
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2] + radius * 2
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2]
                    self.zU += 1
                else:
                    self.zU = 0

            if self.down == True:
                if self.zU < self.act+1:
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2] - radius * 2
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2]
                    self.zU += 1
                else:
                    self.zU = 0

            if self.left == True:
                if self.zU < self.act+1:
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2]
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2] - radius * 2
                    self.zU += 1
                else:
                    self.zU = 0

            if self.right == True:
                if self.zU < self.act:
                    self.YbodyCoordinates[self.zU - 1] = self.YbodyCoordinates[self.zU - 2]
                    self.XbodyCoordinates[self.zU - 1] = self.XbodyCoordinates[self.zU - 2] + radius * 2
                    self.zU += 1
                else:
                    self.zU = 0
            self.slower += 1
        else:
            self.slower += 1

# Момент поедания
        for self.j in range (0, self.act):
            if (self.YbodyCoordinates[self.j] <= self.eatYPos + radius + eatRadius + 5) and (self.YbodyCoordinates[self.j] >= self.eatYPos - radius - eatRadius - 5) and (self.XbodyCoordinates[self.j] <= self.eatXPos + radius + eatRadius + 5) and (self.XbodyCoordinates[self.j] >= self.eatXPos - radius - eatRadius - 5):
                self.ateXPrev = self.XbodyCoordinates[0]
                self.ateYPrev = self.YbodyCoordinates[0]
                self.ate = True
                self.act += 1
                self.score += 1
                # Проверяем, чтобы координаты пищи не находились на змее, если это так, то генерируем новые координаты еды
                for self.z in range (0, self.act - 1):
                    print (self.z,' ', len(self.XbodyCoordinates),' ', len(self.YbodyCoordinates))
                    if (self.YbodyCoordinates[self.z] <= self.eatYPos + radius + eatRadius + 5) and (self.YbodyCoordinates[self.z] >= self.eatYPos - radius - eatRadius - 5) and (self.XbodyCoordinates[self.z] <= self.eatXPos + radius + eatRadius + 5) and (self.XbodyCoordinates[self.z] >= self.eatXPos - radius - eatRadius - 5):
                        self.eatXPos = random.randint (1,SCREEN_WIDTH) // 10 * 10
                        self.eatYPos = random.randint (1,SCREEN_HEIGHT) // 10 * 10

# Для контроля переменных
        """if (self.left == True) or (self.right == True) or (self.up == True) or (self.down == True):
            print (self.score, ' ', self.act, ' ',self.zU)"""

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
        if symbol == arcade.key.UP:
            if self.down == False:
                self.up = True
                self.down = False
                self.right = False
                self.left = False

        if symbol == arcade.key.DOWN:
            if self.up == False:
                self.up = False
                self.down = True
                self.right = False
                self.left = False

        if symbol == arcade.key.RIGHT:
            if self.left == False:
                self.left = False
                self.up = False
                self.down = False
                self.right = True
                self.left = False

        if symbol == arcade.key.LEFT:
            if self.right == False:
                self.up = False
                self.down = False
                self.right = False
                self.left = True

class GameOverView(arcade.View):
    """ Class to manage the game over view """
    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        arcade.start_render()
        arcade.draw_text("Game Over - press ESCAPE to advance", WIDTH/2, HEIGHT/2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    menu_view = MenuView()
    window.show_view(menu_view)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
