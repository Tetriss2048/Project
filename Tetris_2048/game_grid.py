import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid
import numpy as np  # fundamental Python module for scientific computing
from tile import Tile  # used for representing each tile on the tetromino
from point import Point

# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.point = 0
        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(198, 217, 191)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(152, 186, 140)
        self.boundary_color = Color(152, 186, 140)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 8 * self.line_thickness

    # Method used for displaying the game grid
    def display(self):
        # clear the background canvas to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current (active) tetromino
        if self.current_tetromino != None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()

        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(30)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(self.grid_width+2, self.grid_height-2, "Score: " + str(self.point))

        stddraw.setPenColor(stddraw.DARK_BLUE)
        stddraw.filledRectangle(13, 2, 3, 2)

        stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
        stddraw.filledRectangle(13.15, 2.1, 2.8, 1.8)

        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(22)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(13.15+2.8/2, 2.1+1.8/2, "Pause")



        stddraw.setPenColor(Color(150,150,150))
        stddraw.filledRectangle(13, 5, 3, 2)

        stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
        stddraw.filledRectangle(13.15, 5.1, 2.8, 1.8)


        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(22)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(13.15 + 2.8 / 2, 5.1 + 1.8 / 2, "Restart")




        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(17-.1, 20.4-.1, 1.4, 1.4)

        stddraw.setPenColor(Color(255, 0, 0))
        stddraw.filledRectangle(17, 20.4, 1, 1)


        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(38)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(17 + 1 / 2, 20.4 + 1 / 2, "X")


        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(300)

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # draw each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] != None:
                    self.tile_matrix[row][col].draw()
                    # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # return False if the cell is out of the grid
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] != None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method for updating the game grid by placing the given tiles of a stopped
    # tetromino and checking if the game is over due to having tiles above the
    # topmost game grid row. The method returns True when the game is over and
    # False otherwise.
    def update_grid(self, tiles_to_place):

        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])

        for col in range(n_cols):
            for row in range(n_rows):
                # place each occupied tile onto the game grid
                if tiles_to_place[row][col] != None:
                    pos = tiles_to_place[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]

                    # the game is over if any placed tile is out of the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

    def make_fall(self, x, y, string):
        # print("x: "+str(x)+",  y: " + str(y)+"   call from : "+string)
        for yVal in range(y - 1, self.grid_height - 1):
            if self.tile_matrix[yVal][x] != None:
                position = Point()
                position.y = yVal - 1
                position.x = x
                self.tile_matrix[yVal - 1][x] = Tile(position)
                self.tile_matrix[yVal - 1][x].set_number(self.tile_matrix[yVal][x].get_number())
                self.tile_matrix[yVal][x] = None

# to find tiles that need to fall and stick together, creates a list and appends tiles next to each other until see a gap
# calls  AllDown and GetMinLowVal to make the tiles fall as needed
    def check_fall2(self):
        didMoved = False

        for y in range(1, self.grid_height - 1):
            x = 0

            checkTiles = []

            while x < self.grid_width:
                if self.tile_matrix[y][x] != None:
                    checkTiles.append(self.tile_matrix[y][x])
                else:
                    if (len(checkTiles) > 0):
                        # print("checktiles num :  "+str( len(checkTiles)))
                        if self.AllDown(checkTiles, self.GetMinLowVal(checkTiles)):
                            didMoved = True
                        checkTiles.clear()

                x = x + 1
            if (len(checkTiles) > 0):
                # print("checktiles num2 :  " +str( len(checkTiles)))
                if (self.AllDown(checkTiles, self.GetMinLowVal(checkTiles))):
                    didMoved = True
                checkTiles.clear()
        return didMoved
# For tiles holding each other in the air; to get the distance of the tile closest to the tile at the bottom
    def GetMinLowVal(self, tiles):

        minVal = 100

        for i in range(len(tiles)):
            newMinVal = 0
            downIsNone = self.tile_matrix[tiles[i].get_position().y - 1][tiles[i].get_position().x] == None

            while downIsNone:
                newMinVal = newMinVal + 1
                downIsNone = self.tile_matrix[tiles[i].get_position().y - 1 - newMinVal][
                                 tiles[i].get_position().x] == None

            if newMinVal < minVal:
                minVal = newMinVal

        # print("MinVal : "+str(minVal))
        return minVal

    def AllDown(self, tiles, downVal):
        if downVal == 0:
            return False

        for i in range(len(tiles)):
            for j in range(downVal):
                self.make_fall(tiles[i].get_position().x, tiles[i].get_position().y + 1 + j, "All Down")
        return downVal != 0

    def SetColors(self):
       for x in range(self.grid_width):
          for y in range(self.grid_height):
             if self.tile_matrix[y][x]!=None:

                tile_number = self.tile_matrix[y][x].get_number()
                self.tile_matrix[y][x].tile_color(tile_number)


#Checks if tile and tile above it are the same,
# if it has the same number, multiply it by two and write to the bottom tile.
    def CheckNumbers(self):
        didMove = False
        for x in range(self.grid_width):
            y = 0
            makeZero = False
            while y < self.grid_height - 1:
                if self.tile_matrix[y][x] != None and self.tile_matrix[y + 1][x] != None:
                    if self.tile_matrix[y][x].get_number() == self.tile_matrix[y + 1][x].get_number():

                        # set tile colors to green before merging
                        self.tile_matrix[y][x].set_color()
                        self.tile_matrix[y + 1][x].set_color()

                        self.tile_matrix[y][x].set_number(self.tile_matrix[y][x].get_number() * 2)
                        self.tile_matrix[y + 1][x] = None
                        self.point += self.tile_matrix[y][x].get_number() #adds what is collected to the score

                        # getting tile's new computed number

                        makeZero = True
                        didMove = True

                        if self.tile_matrix[y + 2][x] != None:
                            self.make_fall(x, y + 2, "checkNumbers")

                            makeZero = True

                if makeZero:
                    y = 0
                    makeZero = False
                else:
                    y = y + 1

        self.display()
        return didMove

#Checks if the line is full, calls clear_row if it is full.
    def check_rows(self):
        y = 0
        moved = False
        while y < self.grid_height:
            row = 0
            isFilled = True
            while row < self.grid_width:
                if self.tile_matrix[y][row] == None:
                    isFilled = False
                row = row + 1
            if isFilled:
                moved = True
                self.clear_row(y)
            y = y + 1
        return moved

#Equals the whole line to None and adds each deleted tile to the score
    def clear_row(self,y):
        x = 0
        sum = 0

        while x < self.grid_width:
           sum += self.tile_matrix[y][x].get_number()
           self.tile_matrix[y][x] = None
           self.make_fall(x,y+1,"")
           x += 1
        self.point += sum
