from PLANE import Plane
import Constants
import pyxel


class RedEnemy(Plane):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = Constants.RED_ENEMY_SPRITE
        self.nextplane = False
        self.inboard = True

    def move(self, direction: str):
        """ This method receives a direction and moves the enemy """
        if direction.lower() == "down":
            self.y += 3

    def update(self):
        """ This method updates the information about the enemy. If the enemy goes out of the screen,
        then it can't shoot. When the enemy reaches a certain position, then the attribute nextplane changes
        to True which indicates that the next enemy can appear"""
        if self.y > 40:
            self.nextplane = True
        if self.y > Constants.HEIGHT:
            self.inboard = False

    def draw(self):
        """ The object is only drawn when it is in the board """
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
