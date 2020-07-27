import arcade
import random
from math import floor

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
radius = 10
eatRadius = 5
#delta_time = 1
x = 0

class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)
        self.delta_time = 1
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.x = 250
        self.y = 250

        self.counter = 0

        self.bodyX1 = 1000
        self.bodyY1 = 1000

        self.ateX1 = 0
        self.ateY1 = 0

        self.XPressed = 0
        self.YPressed = 0

        self.RightIsPressed = False
        self.LeftIsPressed = False
        self.UpIsPressed = False
        self.DownIsPressed = False
        self.SomethingIsPressed = False

        self.ArrayOfPresssedBottoms = ['0', '0']

        self.ate = False

        self.eatXPos = random.randint (1,499)
        self.eatYPos = random.randint (1,499)

        self.xCollision = True
        self.yCollision = False

        self.speeder = 2

        self.bodyList = []
        self.i = 0
        self.j = 0
        self.act = 0

        self.XbodyCoordinates = []
        self.YbodyCoordinates = []
        while self.j < 10:
            self.XbodyCoordinates.append(0)
            self.YbodyCoordinates.append(0)
            self.j += 1

        self.XTurn = [0]
        self.YTurn = [0]

    def setup(self):
        pass

    def on_draw(self):

        self.body_list = arcade.ShapeElementList()
        for self.i in range(0, 9):
            body = arcade.create_ellipse_filled(self.XbodyCoordinates[self.i], self.YbodyCoordinates[self.i], radius, radius, arcade.color.DARK_BLUE)
            self.body_list.append(body)


        arcade.start_render()
        self.body_list.draw()
        arcade.draw_circle_filled(self.x, self.y, radius, arcade.color.YELLOW)
        #arcade.draw_circle_filled(self.bodyX1, self.bodyY1, radius, arcade.color.YELLOW)
        #c = arcade.draw_circle_filled(self.x - radius, self.y - radius, radius, arcade.color.RED)
        arcade.draw_circle_filled(self.eatXPos, self.eatYPos, eatRadius, arcade.color.RED)
        # Здесь код рисунка

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

# Движение головы змеи
        if (self.up == True) and (self.yCollision == False):
            self.y = self.y + self.speeder
        if (self.down == True) and (self.yCollision == False):
            self.y = self.y - self.speeder
        if (self.right == True) and (self.xCollision == False):
            self.x = self.x + self.speeder
        if (self.left == True) and (self.xCollision == False):
            self.x = self.x - self.speeder
        if (self.xCollision == True) and (self.yCollision == True):
            self.y = self.y + 0
            self.x = self.x + 0

        if (self.DownIsPressed == False) and (self.UpIsPressed == False) and (self.RightIsPressed == False) and (self.LeftIsPressed == False):
            self.SomethingIsPressed = False
        else:
            self.SomethingIsPressed = True

# Увеличение длины змеи после поедания
        self.XbodyCoordinates[0] = self.x
        self.YbodyCoordinates[0] = self.y

# Описание движения всех сегментов змеи, кроме головы
        if self.ate == True and (self.up == True or self.down == True):
                    #self.bodyX1 = self.x
                    #self.bodyY1 = self.y - radius*2
                    #for self.i in range (1, self.act):
            self.XbodyCoordinates[self.act] = self.XbodyCoordinates[self.act -1]
            self.YbodyCoordinates[self.act] = self.YbodyCoordinates[self.act - 1] - radius * 2
            self.ate = False
            #self.ate = False
        elif self.ate == True and (self.right == True or self.left == True):
                    #self.bodyX1 = self.x - radius*2
                    #self.bodyY1 = self.y
                    #for self.i in range (1, self.act):
            self.XbodyCoordinates[self.act] = self.XbodyCoordinates[self.act - 1] - radius * 2
            self.YbodyCoordinates[self.act] = self.YbodyCoordinates[self.act - 1]
            self.ate = False

        for self.i in range (1, self.act+1):
            if self.up == True and self.ArrayOfPresssedBottoms[self.counter] == 'R' and self.XTurn[self.counter] > self.XbodyCoordinates[self.i] and self.ate == False:
                #self.bodyX1 = self.bodyX1 + delta_time * self.speeder
                #for self.i in range (1, self.act):floor(self.XbodyCoordinates[self.i])
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] + self.speeder
            """elif self.up == True and self.ArrayOfPresssedBottoms[self.counter] == 'R' and self.XbodyCoordinates[self.i - 1] < self.XbodyCoordinates[self.i] and self.ate == False:
                    self.bodyX1 = self.bodyX1 - self.speeder
                    #for self.i in range (1, self.act):
                    self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] - self.speeder"""
            if self.up == True and self.XbodyCoordinates[self.i]  == self.XbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyX1 = self.x
                self.bodyY1 = self.y - radius*2
                #for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i - 1] - radius * 2
                self.XbodyCoordinates[self.i] = self.XbodyCoordinates[self.i - 1]

            if self.up == True and self.ArrayOfPresssedBottoms[self.counter] == 'L' and self.XTurn[self.counter] < self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 - self.speeder
                #for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] - self.speeder
            """elif self.up == True and self.ArrayOfPresssedBottoms[self.counter] == 'L' and self.XbodyCoordinates[self.i - 1] > self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 + self.speeder
                #for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] + self.speeder"""
            if self.up == True and self.XbodyCoordinates[self.i]  == self.XbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyX1 = self.x
                self.bodyY1 = self.y - radius*2
            #    for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i - 1] - radius * 2
                self.XbodyCoordinates[self.i] = self.XbodyCoordinates[self.i - 1]


            if self.down == True and self.ArrayOfPresssedBottoms[self.counter] == 'R' and self.XTurn[self.counter] > self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 - self.speeder
    #            for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] + self.speeder
            """elif self.down == True and self.ArrayOfPresssedBottoms[self.counter] == 'R' and self.XbodyCoordinates[self.i - 1] < self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 + self.speeder
#                for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] -  self.speeder"""
            if self.down == True and self.XbodyCoordinates[self.i]  == self.XbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyX1 = self.x
                self.bodyY1 = self.y + radius*2
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i - 1] + radius * 2
                self.XbodyCoordinates[self.i] = self.XbodyCoordinates[self.i - 1]


            """if self.down == True and self.ArrayOfPresssedBottoms[self.counter] == 'L' and self.XbodyCoordinates[self.i - 1] > self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 + self.speeder
        #        for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] + self.speeder"""
            if self.down == True and self.ArrayOfPresssedBottoms[self.counter] == 'L' and self.XTurn[self.counter] < self.XbodyCoordinates[self.i] and self.ate == False:
                self.bodyX1 = self.bodyX1 - self.speeder
    #            for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i] - self.speeder
            if self.down == True and self.XbodyCoordinates[self.i]  == self.XbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyX1 = self.x
                self.bodyY1 = self.y + radius*2
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i - 1] + radius * 2
                self.XbodyCoordinates[self.i] = self.XbodyCoordinates[self.i - 1]

            if self.right == True and self.ArrayOfPresssedBottoms[self.counter] == 'U' and self.YTurn[self.counter] > self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 + self.speeder
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] + self.speeder
            """elif self.right == True and self.ArrayOfPresssedBottoms[self.counter] == 'U' and self.YbodyCoordinates[self.i - 1] < self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 - self.speeder
            #    for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] - self.speeder"""
            if self.right == True and self.YbodyCoordinates[self.i]  == self.YbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyY1 = self.y
                self.bodyX1 = self.x + radius*2
        #        for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i - 1] + radius * 2
                self.YbodyCoordinates[self.i] = self.YbodyCoordinates[self.i - 1]

            if self.left == True and self.ArrayOfPresssedBottoms[self.counter] == 'U' and self.YTurn[self.counter] > self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 + self.speeder
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] + self.speeder
            """elif self.left == True and self.ArrayOfPresssedBottoms[self.counter] == 'U' and self.YbodyCoordinates[self.i - 1] < self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 - self.speeder
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] - self.speeder"""
            if self.right == True and self.YbodyCoordinates[self.i]  == self.YbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyY1 = self.y
                self.bodyX1 = self.x - radius*2
        #        for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i - 1] - radius * 2
                self.YbodyCoordinates[self.i] = self.YbodyCoordinates[self.i - 1]


            """if self.right == True and self.ArrayOfPresssedBottoms[self.counter] == 'D' and self.YbodyCoordinates[self.i - 1] > self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 + self.speeder
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] + self.speeder"""
            if self.right == True and self.ArrayOfPresssedBottoms[self.counter] == 'D' and self.YTurn[self.counter] < self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 - self.speeder
    #            for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] - self.speeder
            if self.right == True and self.YbodyCoordinates[self.i]  == self.YbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyY1 = self.y
                self.bodyX1 = self.x - radius*2
#                for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i - 1] - radius * 2
                self.YbodyCoordinates[self.i] = self.YbodyCoordinates[self.i - 1]


            """if self.left == True and self.ArrayOfPresssedBottoms[self.counter] == 'D' and self.YbodyCoordinates[self.i - 1] > self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 + self.speeder
            #    for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] + self.speeder"""
            if self.left == True and self.ArrayOfPresssedBottoms[self.counter] == 'D' and self.YTurn[self.counter] < self.YbodyCoordinates[self.i] and self.ate == False:
                self.bodyY1 = self.bodyY1 - self.speeder
        #        for self.i in range (1, self.act):
                self.YbodyCoordinates[self.i]  = self.YbodyCoordinates[self.i] - self.speeder
            if self.left == True and self.YbodyCoordinates[self.i]  == self.YbodyCoordinates[self.i-1] and self.ate == False:
                self.bodyY1 = self.y
                self.bodyX1 = self.x + radius*2
    #            for self.i in range (1, self.act):
                self.XbodyCoordinates[self.i]  = self.XbodyCoordinates[self.i - 1] + radius * 2
                self.YbodyCoordinates[self.i] = self.YbodyCoordinates[self.i - 1]

# Момент поедания
        if (self.y <= self.eatYPos + radius + eatRadius) and (self.y >= self.eatYPos - radius - eatRadius ) and (self.x <= self.eatXPos + radius + eatRadius) and (self.x >= self.eatXPos - radius - eatRadius):
            self.eatXPos = random.randint (1,SCREEN_WIDTH)
            self.eatYPos = random.randint (1,SCREEN_HEIGHT)
            self.ate = True
            self.ateX1 = self.x
            self.ateY1 = self.y
            self.act += 1
# Для контроля переменных
        if (self.left == True) or (self.right == True) or (self.up == True) or (self.down == True):
            print (self.eatXPos, ' ', self.eatYPos, ' ',self.x , ' ', self.y, ' ',  self.ArrayOfPresssedBottoms[self.counter], ' ', self.bodyX1, ' ', self.bodyY1, ' ', self.XbodyCoordinates[self.act], ' ', self.YbodyCoordinates[self.act], ' ',self.XTurn[self.counter] , ' ',self.YTurn[self.counter] )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.UpIsPreesed = True
            #self.counter = self.counter + 1
            #if self.counter >= 1:
            #    self.ArrayOfPresssedBottoms.append('U')

        if symbol == arcade.key.DOWN:
            self.DownIsPressed = True
            #self.counter = self.counter + 1
            #if self.counter >= 1:
            #    self.ArrayOfPresssedBottoms.append('D')


        if symbol == arcade.key.RIGHT:
            self.RightIsPressed = True
            #self.counter = self.counter + 1
            #if self.counter >= 1:
            #    self.ArrayOfPresssedBottoms.append('R')

        if symbol == arcade.key.LEFT:
            self.LeftIsPressed = True
            #self.counter = self.counter + 1
            #if self.counter >= 1:
            #    self.ArrayOfPresssedBottoms.append('L')

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            if self.down == False:
                self.up = True
                self.down = False
                self.right = False
                self.left = False
                self.XTurn.append(self.x)
                self.YTurn.append(self.y)
                self.counter += 1
                if self.counter >= 1:
                #self.XTurn.append(self.x)
                #self.YTurn.append(self.y)
                    self.ArrayOfPresssedBottoms.append('U')

        if symbol == arcade.key.DOWN:
            if self.up == False:
                self.up = False
                self.down = True
                self.right = False
                self.left = False
                self.XTurn.append(self.x)
                self.YTurn.append(self.y)
                self.counter += 1
                if self.counter >= 1:
                #self.XTurn.append(self.x)
                #self.YTurn.append(self.y)
                    self.ArrayOfPresssedBottoms.append('D')

        if symbol == arcade.key.RIGHT:
            if self.left == False:
                self.left = False
                self.up = False
                self.down = False
                self.right = True
                self.left = False
                self.XTurn.append(self.x)
                self.YTurn.append(self.y)
                self.counter += 1
                if self.counter >= 1:
                #self.XTurn.append(self.x)
                #self.YTurn.append(self.y)
                    self.ArrayOfPresssedBottoms.append('R')

        if symbol == arcade.key.LEFT:
            if self.right == False:
                self.up = False
                self.down = False
                self.right = False
                self.left = True
                self.XTurn.append(self.x)
                self.YTurn.append(self.y)
                self.counter += 1
                if self.counter >= 1:
                #self.XTurn.append(self.x)
                #self.YTurn.append(self.y)
                    self.ArrayOfPresssedBottoms.append('L')

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
