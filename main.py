from BOARD import Board
import pyxel

board = Board()

# The first is to create the game board, yu must check the API manual for
# more parameters
pyxel.init(board.width, board.height, title="1942")
# We load the pyxres file, it has a 16x16 cat in (0,0) in the bank 0.
# You must replace by a Mario image.
pyxel.load("assets/sprites.pyxres")
# We load a nave image of 16x16 in bank 1 at (17,0)
pyxel.image(1).load(17, 0, "assets/sprites.pyxres")
# To start the game, we call the run method with the functions update and draw
pyxel.run(board.update, board.draw)
