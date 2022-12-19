import pyxel
from PLANE import Plane
import Constants


class SuperBombardier(Plane):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = Constants.SUPERBOMBARDIER_SPRITE
        self.lives = 10
        self.inboard = True

    def move(self, direction: str = "down"):
        """ This method receives a direction and moves the enemy """
        if direction == "down":
            self.y += 2

    def update(self):
        """ This method updates the information about the enemy. If the enemy goes out of the
        screen or loses all its lives, then it disappear """
        if self.y > Constants.HEIGHT:
            self.inboard = False
        if self.lives < 1:
            self.inboard = False

    def draw(self):
        """ The enemy can only be drawn if it is in the board """
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
