import pyxel
from PLANE import Plane
import Constants


class Bombardier(Plane):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = Constants.BOMBARDIER_SPRITE
        self.lives = 6
        self.inboard = True

    def move(self, direction: str = "down"):
        """ This method receives a direction and moves the enemy """
        if direction == "down" and self.lives > 0:
            self.y += 2

    def update(self):
        """ This method updates the information about the enemy. If the enemy goes out of the
        screen or loses all its lives,then it disappears """
        if self.y > Constants.HEIGHT:
            self.inboard = False

    def draw(self):
        """ The enemy can only be drawn if it is in the board """
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
