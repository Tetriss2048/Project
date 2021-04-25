import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the game grid
import numpy as np # fundamental Python module for scientific computing
from tile import Tile # used for representing each tile on the tetromino
from point import Point

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create the tile matrix to store the tiles placed on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # game_over flag shows whether the game is over/completed or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200) 
      self.boundary_color = Color(0, 100, 200)
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

   def make_fall(self,x,y,string):
      #print("x: "+str(x)+",  y: " + str(y)+"   call from : "+string)
      for yVal in range(y-1,self.grid_height-1):
         if self.tile_matrix[yVal][x] != None:
            position = Point()
            position.y = yVal - 1
            position.x = x
            self.tile_matrix[yVal - 1][x] = Tile(position)
            self.tile_matrix[yVal - 1][x].set_number(self.tile_matrix[yVal][x].get_number())
            self.tile_matrix[yVal][x] = None


   def check_fall(self):
      didMoved = False

      for x in range(self.grid_width):
         y = 1

         while y < self.grid_height-1:
            if self.tile_matrix[y][x] != None and self.tile_matrix[y-1][x] == None:
               if x+1 < self.grid_width and  x > 0:
                  if self.tile_matrix[y][x+1] == None and  self.tile_matrix[y][x-1] == None:
                     self.make_fall(x,y,"checkFall, mid")
                     y -= 2
                     didMoved = True

               elif x+1 == self.grid_width:
                  if self.tile_matrix[y][x - 1] == None:
                     self.make_fall(x,y,"checkFall, right")
                     y -= 2
                     didMoved = True

               elif x == 0:
                  if self.tile_matrix[y][x + 1] == None:
                     self.make_fall(x,y,"checkFall , left")
                     y -= 2
                     didMoved = True

            y = y+1
      return didMoved

   def check_fall2(self):
      didMoved = False

      for y in range(1,self.grid_height-1):
         x = 0

         checkTiles = []

         while x < self.grid_width:
            if self.tile_matrix[y][x] != None:
               checkTiles.append(self.tile_matrix[y][x])
            else:
               if (len(checkTiles) > 0):
                  #print("checktiles num :  "+str( len(checkTiles)))
                  if self.AllDown(checkTiles,self.GetMinLowVal(checkTiles)):
                     didMoved = True
                  checkTiles.clear()

            x = x+1
         if(len(checkTiles) > 0):
            #print("checktiles num2 :  " +str( len(checkTiles)))
            if(self.AllDown(checkTiles,self.GetMinLowVal(checkTiles))):
               didMoved = True
            checkTiles.clear()
      return didMoved

   def GetMinLowVal(self,tiles):

      minVal = 100

      for i in range(len(tiles)):
         newMinVal = 0
         downIsNone = self.tile_matrix[tiles[i].get_position().y-1][tiles[i].get_position().x] == None

         while downIsNone:
            newMinVal = newMinVal + 1
            downIsNone = self.tile_matrix[tiles[i].get_position().y-1-newMinVal][tiles[i].get_position().x]==None

         if newMinVal<minVal:
            minVal = newMinVal

      #print("MinVal : "+str(minVal))
      return minVal

   def AllDown(self,tiles,downVal):
      if downVal == 0:
         return False

      for i in range(len(tiles)):
         for j in range(downVal):
            self.make_fall(tiles[i].get_position().x,tiles[i].get_position().y+1+j,"All Down")
      return downVal!=0


   def CheckNumbers(self):
      didMove = False
      for x in range(self.grid_width):
         y = 0
         makeZero = False
         while y < self.grid_height-1:
            if self.tile_matrix[y][x] != None and self.tile_matrix[y+1][x] != None:
               if self.tile_matrix[y][x].get_number() == self.tile_matrix[y+1][x].get_number():
                  self.tile_matrix[y][x].set_number(self.tile_matrix[y][x].get_number()*2)
                  self.tile_matrix[y+1][x] = None
                  makeZero = True
                  didMove = True

                  if self.tile_matrix[y+2][x] != None:

                     self.make_fall(x,y+2,"checkNumbers")

                     makeZero = True


            if makeZero:
               y = 0
               makeZero = False
            else:
               y = y+1

      self.display()
      return didMove


   def clear_rows(self):
      y=0
      while y < self.grid_height:
         row=0
         isFilled= True
         while row < self.grid_width:
            if self.tile_matrix[y][row] == None:
               isFilled=False
            row=row+1
         if isFilled:
            self.tile_matrix[y][row] = None
         y = y + 1
























