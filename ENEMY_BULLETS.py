import Constants
from BULLETS import Bullet
import pyxel


class EnemyBullet(Bullet):
    EnemyBullet_list = []

    def __init__(self, x, y):
        super().__init__(x, y)
        self.inboard = True
        self.sprite = Constants.ENEMY_BULLET_SPRITE
        EnemyBullet.EnemyBullet_list.append(self)

    def move(self, direction: str = "down"):
        """ This method receives a direction and moves the bullet """
        if direction.lower() == "down":
            self.y += 4

    def update(self):
        """ This method updates the information about the bullet. If the bullet goes out of the
        screen, then it is removed from the list of bullets """
        if self.y > Constants.HEIGHT:
            self.inboard = False
        if not self.inboard:
            self.EnemyBullet_list.remove(self)

    def draw(self):
        """ The object is only drawn if it is visible """
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
