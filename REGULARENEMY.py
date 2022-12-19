import random

from PLANE import Plane
import Constants
import pyxel


class RegularEnemy(Plane):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = Constants.REGULAR_ENEMY_SPRITE
        self.inboard = True
        self.nextplane = False

    def move(self, direction: str):
        """ This method receives a direction and moves the enemy """
        if direction.lower() == "down":
            self.y = self.y + 3

    def update(self):
        """This method updates the information about the enemy. If the enemy goes out of the screen,
        then it can no longer shoot. When the enemy reaches a certain position, then its attribute nextplane changes
        to True which indicates that the next enemy can appear """
        if self.y == Constants.WIDTH/2:
            a = random.randint(1, 10)
            if a > 7:
                self.move("up")
            else:
                self.move("down")
        if self.y < 0 or self.y > Constants.WIDTH:
            self.inboard = False
        if self.y == 33:
            self.nextplane = True

    def draw(self):
        """ The object is only drawn when it is in the board """
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
