import pyxel

from BULLETS import Bullet
import Constants


class PlayerBullet(Bullet):
    bullet_list1 = []
    bullet_list2 = []

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Constants.BULLET_SPRITE
        self.inboard = True
        PlayerBullet.bullet_list1.append(self)
        PlayerBullet.bullet_list2.append(self)

    def move(self, direction: str = "up"):
        """ This method receives a direction and moves the bullet """
        if direction.lower() == "up":
            self.y -= 2

    def update(self):
        """ This method updates the information about the bullet. If the bullet goes out of the screen,
        then it cannot hit any enemies, and it is removed from the list"""
        if self.y <= 0:
            self.inboard = False
        if not self.inboard:
            self.bullet_list1.remove(self)
            self.bullet_list2.remove(self)

    def draw(self):
        """The object is only drawn if it is visible"""
        if self.inboard:
            pyxel.blt(self.x, self.y, *self.sprite)
