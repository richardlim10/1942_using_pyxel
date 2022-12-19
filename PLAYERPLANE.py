import Constants
from PLANE import Plane


class Playerplane(Plane):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite1 = Constants.PLAYER_SPRITE1
        # The game runs until lives are 0 or the plane wins
        self.lives = 3
        self.winner = False

    def move(self, direction: str, size: int):
        """ This method moves the plane when it receives the
        direction and the size of the plane"""
        # Checking the current horizontal size of Plane to stop it before
        # it reaches the right border
        plane_x_size = self.sprite1[3]
        plane_y_size = self.sprite1[4]
        if direction.lower() == 'right' and self.x < size - plane_x_size:
            self.x += 3
        if direction.lower() == 'left' and self.x > 0:
            self.x -= 3
        if direction.lower() == 'up' and self.y > 0:
            self.y -= 3
        if direction.lower() == "down" and self.y < size - plane_y_size:
            self.y += 3
