import random
import pyxel
from PLAYERPLANE import Playerplane
from PLAYERBULLET import PlayerBullet
from REGULARENEMY import RegularEnemy
from REDENEMY import RedEnemy
from BOMBARDIER import Bombardier
from SUPERBOMBARDIER import SuperBombardier
from ENEMY_BULLETS import EnemyBullet
import Constants


class Board:
    """ This class contains all the information needed to represent the
    board"""
    def __init__(self):
        """ The parameters are the width and height of the board"""
        # Initializing the object
        self.width = Constants.WIDTH
        self.height = Constants.HEIGHT
        self.score = 0
        self.high_score = 0
        self.finish = False

        # This block initializes pyxel
        # The first thing to do is to create the screen, see API for more parameters
        pyxel.init(self.width, self.height, title="1942")
        # Loading the pyxres file
        pyxel.load("assets/sprites.pyxres")

        # We create our objects and assign them a position in the board
        self.plane = Playerplane(int(self.width / 2), 200)

        # creating the lists of bullets for the player and enemies
        self.bullet_list1 = PlayerBullet.bullet_list1
        self.bullet_list2 = PlayerBullet.bullet_list2
        self.enemybullet_list = EnemyBullet.EnemyBullet_list

        # The following loops are for loops used to create and add enemies to each respective list. This will allow
        # the "draw" method to generate the enemies on the board
        self.regular_enemies = []
        for i in range(21):
            a = random.randint(30, 210)
            self.regular_enemies.append(RegularEnemy(a, 0))

        self.red_enemies = []
        self.red_enemies2 = []
        for j in range(5):
            self.red_enemies.append(RedEnemy(Constants.RED_ENEMY_INITIAL[j], 0))
            self.red_enemies2.append(RedEnemy(Constants.RED_ENEMY_INITIAL[j], 0))

        self.bombardier_list = []
        for i in range(2):
            self.bombardier_list.append(Bombardier(random.randint(50, 200), 0))
        self.super_bombardier = SuperBombardier(Constants.SUPERBOMBARDIER_INITIAL[0],
                                                Constants.SUPERBOMBARDIER_INITIAL[1])

        # Running the game
        pyxel.run(self.update, self.draw)

    def update(self):
        """ This is executed each frame, here invocations to the update
        methods of all objects must be included """
        if not self.finish:
            # While the plane is alive but has not won, we execute these methods
            if self.plane.lives > 0 and not self.plane.winner:
                self.player_bullets()
                self.player_update()
                self.enemies_shots()
                self.stage1()
                self.stage2()
                self.stage3()
                self.stage4()
                self.red_enemies_points()
                self.red_enemies2_points()
                self.reg_enemies_points()
                self.bombardiers_points()
                self.superbombardier_points()
            else:
                # If the player has either we update the high score, so then it can be showed.
                # We also give the option of playing another time by clicking the space bar.
                if self.score > self.high_score:
                    self.high_score = self.score
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.create_lists()
                    self.revive_enemies()
                    self.score = 0
                    self.plane.lives = 3
                    self.plane.winner = False

    def player_update(self):
        """ Here are stored the player movements when pressing certain keys """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.plane.move('right', self.width)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.plane.move('left', self.width)
        if pyxel.btn(pyxel.KEY_UP):
            self.plane.move('up', self.height)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.plane.move('down', self.height)

        # Shooting when pressing space key
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.pbullet1 = PlayerBullet(self.plane.x, self.plane.y)
            self.pbullet2 = PlayerBullet(self.plane.x+12, self.plane.y)

        # If the plane is higher than the position 3 on the y-axis, the player wins. It isn't 0 as
        # in the class design, we didn't allow the plane to move outside the board.
        if self.plane.y < 3:
            self.plane.winner = True

    def player_bullets(self):
        """ Here we have the movement of the player bullets, of both lists, as our plane shoots two
         bullets at a time """
        for element in self.bullet_list1:
            element.move("up")
            element.update()
        for element in self.bullet_list2:
            element.move("up")
            element.update()

    # Scoring system
    def red_enemies_points(self):
        """ This function is for the count of points. If an element either player bullet list,
         reaches the position of a plane of the first red enemies' list, then the enemy disappears
         from the board. It only works if the enemy and the bullets are shown on the screen """
        for element in self.red_enemies:
            if element.inboard:
                for a in self.bullet_list1:
                    if a.inboard:
                        if element.x <= a.x <= element.x + Constants.RED_ENEMY_WIDTH and \
                                element.y - Constants.RED_ENEMY_HEIGHT <= a.y <= element.y:
                            self.score += 200
                            element.inboard = False
                    for b in self.bullet_list2:
                        if b.inboard:
                            if element.x <= b.x <= element.x + Constants.RED_ENEMY_WIDTH \
                                    and element.y >= b.y >= element.y - Constants.RED_ENEMY_HEIGHT / 2:
                                self.score += 200
                                element.inboard = False

    def red_enemies2_points(self):
        """ The score increases if any element of either player bullet list has the same position as
        a red enemy of the second list. If this happens the red enemy disapears """
        for element in self.red_enemies2:
            if element.inboard:
                for a in self.bullet_list1:
                    if a.inboard:
                        if element.x <= a.x <= element.x + Constants.RED_ENEMY_WIDTH and \
                                element.y - Constants.RED_ENEMY_HEIGHT <= a.y <= element.y:
                            self.score += 200
                            element.inboard = False
                    for b in self.bullet_list2:
                        if b.inboard:
                            if element.x <= b.x <= element.x + Constants.RED_ENEMY_WIDTH \
                                    and element.y >= b.y >= element.y - Constants.RED_ENEMY_HEIGHT / 2:
                                self.score += 200
                                element.inboard = False

    def reg_enemies_points(self):
        """ This method modifies the score when shooting a red enemy. If a player bullet reaches a regular
         enemy position, the enemy disappears and the score increases """
        for element in self.regular_enemies:
            if element.inboard:
                for a in self.bullet_list1:
                    if a.inboard and (element.x < a.x < element.x + Constants.REGULAR_ENEMY_WIDTH
                                      and element.y > a.y > Constants.REGULAR_ENEMY_HEIGHT / 2):
                        self.score += 100
                        element.inboard = False

                for b in self.bullet_list2:
                    if b.inboard and (element.x < b.x < element.x + Constants.REGULAR_ENEMY_WIDTH
                                      and element.y > b.y > element.y - Constants.REGULAR_ENEMY_HEIGHT / 2):
                        self.score += 100
                        element.inboard = False

    def bombardiers_points(self):
        """ This method is responsible for making the bombardiers vanish when shot. Bombardiers
        give more points than regular and red enemies, as they have more lives """
        for element in self.bombardier_list:
            if element.inboard:
                for a in self.bullet_list1:
                    if a.inboard:
                        if element.x < a.x < element.x + Constants.BOMBARDIER_WIDTH \
                                and element.y > a.y > element.y - Constants.BOMBARDIER_HEIGHT / 2:
                            element.lives -= 1
                            if element.lives < 1:
                                self.score += 350
                                pyxel.blt(element.x, element.y, 0, 137, 38, 3, 3)
                                element.inboard = False

                for b in self.bullet_list2:
                    if b.inboard:
                        if element.x > b.x < element.x + Constants.BOMBARDIER_HEIGHT \
                                and element.y > b.y > element.y - Constants.BOMBARDIER_HEIGHT / 2:
                            element.lives -= 1
                            if element.lives < 1:
                                self.score += 350
                                pyxel.blt(element.x, element.y, 0, 137, 38, 3, 3)
                                element.inboard = False

    # Super bombardier
    def superbombardier_points(self):
        """ When a superbombardier is eliminated, the score increases the most as it is the enemy with the
         most lives """
        if self.super_bombardier.inboard:
            for a in self.bullet_list1:
                if a.inboard and (
                        self.super_bombardier.x <= a.x <= self.super_bombardier.x + Constants.SUPERBOMBARDIER_WIDTH
                        and self.super_bombardier.y <= a.y <= self.super_bombardier.y - Constants.SUPERBOMBARDIER_HEIGHT / 2):
                    self.super_bombardier.lives -= 1
                    if self.super_bombardier.lives < 1:
                        self.score += 450
                        pyxel.blt(a.x, a.y, 0, 137, 38, 3, 3)
                        self.super_bombardier.alive = False

                for b in self.bullet_list2:
                    if b.inboard and (
                            self.super_bombardier.x <= b.x <= self.super_bombardier.x + Constants.SUPERBOMBARDIER_WIDTH
                            and self.super_bombardier.y >= b.y >= self.super_bombardier.y - Constants.SUPERBOMBARDIER_HEIGHT / 2):
                        self.super_bombardier.lives -= 1
                        if self.super_bombardier.lives < 1:
                            self.score += 450
                            pyxel.blt(b.x, b.y, 0, 137, 38, 3, 3)
                            self.super_bombardier.alive = False

    def create_lists(self):
        """ This method creates the lists of objects.It is useful in order to play several times. As
         each game, the enemies either are shot or go out of the screen, this method creates the
          objects in their original position. """
        self.plane = Playerplane(int(self.width / 2), 200)
        self.pbullet1 = PlayerBullet(self.plane.x, self.plane.y)
        self.pbullet2 = PlayerBullet(self.plane.x + 12, self.plane.y)
        self.bullet_list1 = PlayerBullet.bullet_list1
        self.bullet_list2 = PlayerBullet.bullet_list2
        self.enemybullet_list = EnemyBullet.EnemyBullet_list

        self.regular_enemies = []
        for i in range(21):
            a = random.randint(30, 210)
            self.regular_enemies.append(RegularEnemy(a, 0))

        self.red_enemies = []
        self.red_enemies2 = []
        for j in range(5):
            self.red_enemies.append(RedEnemy(Constants.RED_ENEMY_INITIAL[j], 0))
            self.red_enemies2.append(RedEnemy(Constants.RED_ENEMY_INITIAL[j], 0))

        self.bombardier_list = []
        for i in range(2):
            self.bombardier_list.append(Bombardier(random.randint(50, 200), 0))
        self.super_bombardier = SuperBombardier(Constants.SUPERBOMBARDIER_INITIAL[0], Constants.SUPERBOMBARDIER_INITIAL[1])

    def revive_enemies(self):
        """ This method revives the enemies for the next game, as during a game they move and
         disappear of the board or are shot, and an enemy can only be shot again if it is in the
          board, as it is only visible that way """
        for element in self.regular_enemies:
            element.inboard = True
        for element in self.red_enemies:
            element.inboard = True
        for element in self.red_enemies2:
            element.inboard = True
        for element in self.bombardier_list:
            element.inboard = True
        self.super_bombardier.lives = 3

    def stage1(self):
        """ During the first stage only a group of regular and red enemies appear. A plane only
        appears if the previous one has reached a certain position, which is indicated by the attribute
        nextplane """
        self.regular_enemies[0].move("down")
        self.regular_enemies[0].update()
        for i in range(1, 5):
            if self.regular_enemies[i-1].nextplane:
                self.regular_enemies[i].move("down")
                self.regular_enemies[i].update()
        if not self.regular_enemies[4].inboard:
            self.red_enemies[0].move("down")
            self.red_enemies[0].update()
            for i in range(1, 3):
                if self.red_enemies[i-1].nextplane:
                    self.red_enemies[i+2].move("down")
                    self.red_enemies[i+2].update()
                    self.red_enemies[i].move("down")
                    self.red_enemies[i].update()

    def stage2(self):
        """ In this stage another group of regular enemies and the second group of red enemies appear
        The first plane only appears when the last one of the previous stage is no longer visible.
        Red enemies appear in a v formation """
        if not self.red_enemies[4].inboard:
            self.regular_enemies[5].move("down")
            self.regular_enemies[5].update()
            for i in range(6, 11):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].move("down")
                    self.regular_enemies[i].update()
            if not self.regular_enemies[10].inboard:
                self.red_enemies2[0].move("down")
                self.red_enemies2[0].update()
                # They appear in a determined position and the
                # tuple that contains their position goes from left to right
                # The second and third plane only appear when the first plane has reached a certain y.
                # The same happens with the fourth and fifth plane
                for i in range(1, 3):
                    if self.red_enemies2[i - 1].nextplane:
                        self.red_enemies2[i + 2].move("down")
                        self.red_enemies2[i + 2].update()
                        self.red_enemies2[i].move("down")
                        self.red_enemies2[i].update()

    def stage3(self):
        """ In the stage3 regular enemies and bombardiers appear """
        if self.red_enemies2[4].y > self.height:
            self.regular_enemies[11].move("down")
            self.regular_enemies[11].update()
            for i in range(12, 16):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].move("down")
                    self.regular_enemies[i].update()
        if self.regular_enemies[15].y > self.height:
            self.bombardier_list[0].move("down")
            self.bombardier_list[0].update()
        if not self.bombardier_list[0].inboard:
            self.bombardier_list[1].move("down")
            self.bombardier_list[1].update()

    def stage4(self):
        """ In the last stage of the game the player plane must face the superbombardier """
        if not self.bombardier_list[1].inboard:
            self.regular_enemies[16].move("down")
            self.regular_enemies[16].update()
            for i in range(17, 21):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].move("down")
                    self.regular_enemies[i].update()
        if self.regular_enemies[20].y > self.height:
            self.super_bombardier.move("down")
            self.super_bombardier.update()

    def enemies_shots(self):
        """ This method is in charge of the way of shooting of the enemies. Each enemy can only shoot
        if it is on the screen. Regular enemies only shoot once, red enemies don't usually shoot and
        the bombardiers and superbombardiers shoot more than one bullet at a time """
        for element in self.regular_enemies:
            if element.inboard:
                if element.y == 33:
                    self.enemybullet = EnemyBullet(element.x, element.y)
        for element in self.red_enemies:
            if element.inboard:
                a = random.randint(1, 5)
                if element.y == 33 and a == 3:
                    self.enemybullet = EnemyBullet(element.x, element.y)

        for element in self.bombardier_list:
            if element.inboard:
                a = random.randint(2, 3)
                if element.y == 24 or element.y == 80:
                    for i in range(a):
                        self.enemybullet = EnemyBullet(element.x+8*i, element.y)

        if self.super_bombardier.inboard:
            a = random.randint(4, 5)
            if self.super_bombardier.y == 66:
                for i in range(a):
                    self.enemybullet = EnemyBullet(self.super_bombardier.x + 9 * i, self.super_bombardier.y)

        for element in self.enemybullet_list:
            element.move("down")
            element.update()
            if self.plane.y+Constants.PLAYER_HEIGHT/2 > element.y > self.plane.y\
                    and self.plane.x+Constants.PLAYER_WIDTH > element.x > self.plane.x:
                self.plane.lives -= 1

    def draw(self):
        """ This is executed also each frame, it is responsible for painting everything on the
        screen"""

        pyxel.cls(0)
        pyxel.blt(self.plane.x, self.plane.y, *self.plane.sprite1)
        # The elements of the bullet list are drawn

        pyxel.text(180, 18, f"SCORE{self.score:5}", 7)
        pyxel.text(10, 18, f"LIVES{self.plane.lives:5}", 7)
        self.stage1draw()
        self.stage2draw()
        self.stage3draw()
        self.stage4draw()
        self.bullets_draw()
        self.gameover_screen()
        self.background_draw()

    def background_draw(self):
        """ This function makes stars appear in our background """
        for i in range(70):
            pyxel.blt(random.randint(3, 240), random.randint(3, 240), *Constants.STAR_SPRITE)

    def gameover_screen(self):
        """ This is what we see when the game finishes, the score and the high score are shown.
        If we have won, the screen will say WINNER, and if we lost the screen will read GAME OVER """
        if self.plane.lives < 1 or self.plane.winner:
            pyxel.cls(0)
            pyxel.text(95, 190, f"PRESS SPACE BAR", 7)
            pyxel.text(100, 100, f"HIGH SCORE{self.high_score:5}", 7)
            pyxel.text(100, 130, f"SCORE{self.score:5}", 7)
            if self.plane.lives < 1:
                pyxel.text(100, 70, f"GAME OVER", 8)
            else:
                pyxel.text(100, 70, f"WINNER!", 8)

    def stage1draw(self):
        """ This method draws all the enemies of the first stage """
        self.regular_enemies[0].draw()
        for i in range(1, 5):
            if self.regular_enemies[i - 1].nextplane:
                self.regular_enemies[i].draw()
        if not self.regular_enemies[4].inboard:
            self.red_enemies[0].draw()
            for i in range(1, 3):
                if self.red_enemies[i - 1].nextplane:
                    self.red_enemies[i + 2].draw()
                    self.red_enemies[i].draw()

    def stage2draw(self):
        """Thanks to this method we can see all the enemies that appear in the second stage"""
        if not self.red_enemies[4].inboard:
            self.regular_enemies[5].draw()
            for i in range(6, 11):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].draw()
            if not self.regular_enemies[10].inboard:
                self.red_enemies2[0].draw()
                for i in range(1, 3):
                    if self.red_enemies2[i - 1].nextplane:
                        self.red_enemies2[i + 2].draw()
                        self.red_enemies2[i].draw()

    def stage3draw(self):
        """ This method draws the enemies of the third stage while they are in the board """
        if self.red_enemies2[4].y > self.height:
            self.regular_enemies[11].draw()
            for i in range(12, 16):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].draw()
        if self.regular_enemies[15].y > self.height:
            self.bombardier_list[0].draw()
        if not self.bombardier_list[0].inboard:
            self.bombardier_list[1].draw()

    def stage4draw(self):
        """ This method draws the enemies of stage 4 """
        if not self.bombardier_list[1].inboard:
            self.regular_enemies[16].draw()
            for i in range(17, 21):
                if self.regular_enemies[i - 1].nextplane:
                    self.regular_enemies[i].draw()
        if self.regular_enemies[20].y > self.height:
            self.super_bombardier.draw()

    def bullets_draw(self):
        """ This method draws the bullets """
        for element in self.bullet_list1:
            element.draw()
        for element in self.bullet_list2:
            element.draw()
        for element in self.enemybullet_list:
            element.draw()
