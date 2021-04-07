# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
#Program window name
pygame.display.set_caption("team_26_Qix")

# Define constants
UNIT_SIZE = 10
SCREEN_WIDTH = 500
HUD_WIDTH = 250
SCREEN_HEIGHT = 500
PLAYER_MOVE_SPEED = 10
QIX_MOVE_SPEED = 3

# State variables
previous_direction = 1   # for movement calculation
  #       1
  #   0       2
  #       3

# GAME SPACE ------------------------------------------------
class Vertex:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.index = None
    self.left = None
    self.up = None
    self.right = None
    self.down = None
  
  def setLeft(self, left):
    self.left = left
    
  def setUp(self, up):
    self.up = up
    
  def setRight(self, right):
    self.right = right
  
  def setDown(self, down):
    self.down = down
    
  def setIndex(index):
    self.index = index

class Line:
  def __init__(self, orientation, x, y, length, width):
    self.orientation = orientation # 0 for horizontal, 1 for vertical
    self.x = x
    self.y = y
    self.length = length
    self.width = width
    self.ends = None
    self.border = True
    
  def setEnds(self, dir1, vert1, dir2, vert2):
    self.ends = {
      dir1: vert1,
      dir2: vert2
      }

# init starting lines/vertices
def initLines(): 
  NW = Vertex(0, 0)
  NE = Vertex(SCREEN_WIDTH-UNIT_SIZE, 0)
  SE = Vertex(SCREEN_WIDTH-UNIT_SIZE, SCREEN_HEIGHT-UNIT_SIZE)
  SW = Vertex(0, SCREEN_HEIGHT-UNIT_SIZE)
  W = Line(1, 0, 0, SCREEN_HEIGHT, UNIT_SIZE)
  W.setEnds(1, NW, 3, SW)
  N = Line(0, 0, 0, UNIT_SIZE, SCREEN_WIDTH)
  N.setEnds(0, NW, 2, NE)
  E = Line(1, SCREEN_WIDTH-UNIT_SIZE, 0, SCREEN_HEIGHT, UNIT_SIZE)
  E.setEnds(1, NE, 3, SE)
  S = Line(0, 0, SCREEN_HEIGHT-UNIT_SIZE, UNIT_SIZE, SCREEN_WIDTH)
  S.setEnds(0, SW, 2, SE)
  NW.setDown(W)
  NW.setRight(N)
  NE.setLeft(N)
  NE.setDown(E)
  SE.setUp(E)
  SE.setLeft(S)
  SW.setRight(S)
  SW.setUp(W)
  lines.append(W)
  lines.append(N)
  lines.append(E)
  lines.append(S)

lines = []
tempLines = []

initLines()

# PLAYER CODE -------------------------------------------------------
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((UNIT_SIZE, UNIT_SIZE)) # the size of the rectangle, 
        self.surf.fill((184, 245, 120)) # colour of the rectangle
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2 -5 , SCREEN_HEIGHT - 5)
        ) # the area on the screen that has the property of player, or simple the player
        self.onLine = lines[3]
        self.onVertex = None

    def draw(self, surface):
        screen.blit(self.surf, self.rect)    

    def update(self, pressed_keys):
      global previous_direction
      if bool(pressed_keys[K_SPACE]) and bool(self.onVertex):
        # UP
        if bool(pressed_keys[K_UP]):
          if bool(self.onVertex.up) or self.rect.top == 0:
            return
          newLine = Line(1, self.rect.x, self.rect.y - UNIT_SIZE, UNIT_SIZE*2, UNIT_SIZE)
          newLine.ends = {3: self.onVertex}
          self.onVertex.up = newLine
          tempLines.append(newLine) 
          previous_direction = 1  
          self.rect.move_ip(0, -PLAYER_MOVE_SPEED)
          self.onLine = None
          self.onVertex = None
        # DOWN
        elif bool(pressed_keys[K_DOWN]):
          if bool(self.onVertex.up) or self.rect.bottom == SCREEN_HEIGHT:
            return
          newLine = Line(1, self.rect.x, self.rect.y, UNIT_SIZE*2, UNIT_SIZE)
          newLine.ends = {1: self.onVertex}
          self.onVertex.down = newLine
          tempLines.append(newLine) 
          previous_direction = 3  
          self.rect.move_ip(0, PLAYER_MOVE_SPEED)
          self.onLine = None
          self.onVertex = None
        # LEFT
        elif bool(pressed_keys[K_LEFT]):
          if bool(self.onVertex.up) or self.rect.left == 0:
            return
          newLine = Line(0, self.rect.x - UNIT_SIZE, self.rect.y, UNIT_SIZE, UNIT_SIZE*2)
          newLine.ends = {2: self.onVertex}
          self.onVertex.left = newLine
          tempLines.append(newLine) 
          previous_direction = 0  
          self.rect.move_ip(-PLAYER_MOVE_SPEED, 0)   
          self.onLine = None
          self.onVertex = None
        # RIGHT
        elif bool(pressed_keys[K_RIGHT]):
          if bool(self.onVertex.up) or self.rect.right == SCREEN_WIDTH:
            return
          newLine = Line(0, self.rect.x, self.rect.y, UNIT_SIZE, UNIT_SIZE*2)     
          newLine.ends = {0: self.onVertex}  
          self.onVertex.right = newLine
          tempLines.append(newLine) 
          previous_direction = 2  
          self.rect.move_ip(PLAYER_MOVE_SPEED, 0)
          self.onLine = None
          self.onVertex = None
          
      elif bool(pressed_keys[K_SPACE]) and not bool(self.onVertex):
        # UP
        if bool(pressed_keys[K_UP]):
          if bool(self.onLine):
            if self.onLine.orientation == 1:
              return
            else: 
              startNewLineVertical(self, 1)
              self.rect.move_ip(0, -PLAYER_MOVE_SPEED)
              previous_direction = 1
          elif previous_direction != 3:
            continueLine(self, 1)
            self.rect.move_ip(0, -PLAYER_MOVE_SPEED)
            previous_direction = 1
        # DOWN
        elif bool(pressed_keys[K_DOWN]):
          if bool(self.onLine):
            if self.onLine.orientation == 1:
              return
            else:
              startNewLineVertical(self, 3)
              self.rect.move_ip(0, PLAYER_MOVE_SPEED)
              previous_direction = 3
          elif previous_direction != 1:
            continueLine(self, 3) 
            self.rect.move_ip(0, PLAYER_MOVE_SPEED)
            previous_direction = 3
        # LEFT
        elif bool(pressed_keys[K_LEFT]):
          if bool(self.onLine): 
            if self.onLine.orientation == 0:
              return
            else:
              startNewLineHorizontal(self, 0)
              self.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
              previous_direction = 0
          elif previous_direction != 2:
            continueLine(self, 0) 
            self.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
            previous_direction = 0
        # RIGHT
        elif bool(pressed_keys[K_RIGHT]):
          if bool(self.onLine):
            if self.onLine.orientation == 0:
              return
            else:
              startNewLineHorizontal(self, 2)
              self.rect.move_ip(PLAYER_MOVE_SPEED, 0)
              previous_direction = 2
          elif previous_direction != 0:
            continueLine(self, 2)
            self.rect.move_ip(PLAYER_MOVE_SPEED, 0)
            previous_direction = 2
      
      elif bool(self.onLine) and bool(self.onVertex) | bool(checkVertices(self)):
        currentVertex = checkVertices(self)
        self.onVertex = currentVertex
        if bool(pressed_keys[K_UP]) and bool(currentVertex.up):
          self.rect.move_ip(0, -PLAYER_MOVE_SPEED)
          previous_direction = 1
          self.onLine = currentVertex.up
          self.onVertex = False
        elif bool(pressed_keys[K_DOWN]) and bool(currentVertex.down):
          self.rect.move_ip(0, PLAYER_MOVE_SPEED)
          previous_direction = 3
          self.onLine = currentVertex.down
          self.onVertex = False
        elif bool(pressed_keys[K_LEFT]) and bool(currentVertex.left):
          self.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
          previous_direction = 0
          self.onLine = currentVertex.left
          self.onVertex = False
        elif bool(pressed_keys[K_RIGHT]) and bool(currentVertex.right):
          self.rect.move_ip(PLAYER_MOVE_SPEED, 0)
          previous_direction = 2
          self.onLine = currentVertex.right
          self.onVertex = False
        
      elif bool(pressed_keys[K_UP]) and bool(self.onLine) and (self.onLine.orientation == 1):
        self.rect.move_ip(0, -PLAYER_MOVE_SPEED)
        previous_direction = 1
      elif bool(pressed_keys[K_DOWN]) and bool(self.onLine) and (self.onLine.orientation == 1):
        self.rect.move_ip(0, PLAYER_MOVE_SPEED)
        previous_direction = 3
      elif bool(pressed_keys[K_LEFT]) and bool(self.onLine) and (self.onLine.orientation == 0):
        self.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
        previous_direction = 0
      elif bool(pressed_keys[K_RIGHT]) and bool(self.onLine) and (self.onLine.orientation == 0):
        self.rect.move_ip(PLAYER_MOVE_SPEED, 0)
        previous_direction = 2

      # Keep player on the screen
      if self.rect.left < 0:
        self.rect.left = 0
      elif self.rect.right > SCREEN_WIDTH:
        self.rect.right = SCREEN_WIDTH
      elif self.rect.top <= 0:
        self.rect.top = 0
      elif self.rect.bottom >= SCREEN_HEIGHT:
        self.rect.bottom = SCREEN_HEIGHT
  
    # Is the player on the line it's drawing
    def checkLineCollision(self):
      index = 0
      while index < len(tempLines) - 3:
        if self.rect.x >= tempLines[index].x and self.rect.x < tempLines[index].x + tempLines[index].width and self.rect.y >= tempLines[index].y and self.rect.y < tempLines[index].y + tempLines[index].length:
          return True
        index += 1
        
    def checkLineIntersection(self):
      global lines, tempLines
      for line in lines:
        if self.rect.x >= line.x and self.rect.x < line.x + line.width and self.rect.y >= line.y and self.rect.y < line.y + line.length:
          needNewVert = True
          # newVert = None
          for vertex in line.ends:
            if self.rect.x == line.ends[vertex].x and self.rect.y == line.ends[vertex].y:
              needNewVert = False
              newVert = line.ends[vertex]
          
          if not needNewVert:
            if previous_direction == 0:
              newVert.right = tempLines[len(tempLines) - 1]
              tempLines[len(tempLines) - 1].ends.update({0: newVert})
              split1 = newVert.up
            elif previous_direction == 1:
              newVert.down = tempLines[len(tempLines) - 1]
              tempLines[len(tempLines) - 1].ends.update({1: newVert})
              split1 = newVert.left
            elif previous_direction == 2:
              newVert.left = tempLines[len(tempLines) - 1]
              tempLines[len(tempLines) - 1].ends.update({2: newVert})
              split1 = newVert.up
            else:
              newVert.up = tempLines[len(tempLines) - 1]
              tempLines[len(tempLines) - 1].ends.update({3: newVert})
              split1 = newVert.left
          else:
            newVert = Vertex(self.rect.x, self.rect.y)
            if previous_direction % 2 == 0:
              split1 = Line(1, line.x, line.y, self.rect.y + UNIT_SIZE - line.y, UNIT_SIZE)
              split1.ends = {1: line.ends[1], 3: newVert} 
              line.ends[1].down = split1
              split2 = Line(1, self.rect.x, self.rect.y, line.length + line.y - self.rect.y, UNIT_SIZE)
              split2.ends = {1: newVert, 3: line.ends[3]}
              line.ends[3].up = split2
              newVert.up = split1
              newVert.down = split2
              if previous_direction == 0:
                newVert.right = tempLines[len(tempLines) - 1]
                tempLines[len(tempLines) - 1].ends.update({0: newVert})
              else:
                newVert.left = tempLines[len(tempLines) - 1]
                tempLines[len(tempLines) - 1].ends.update({2: newVert})
            else:
              newVert = Vertex(self.rect.x, self.rect.y)
              split1 = Line(0, line.x, line.y, UNIT_SIZE, self.rect.x + UNIT_SIZE - line.x)
              split1.ends = {0: line.ends[0], 2: newVert}
              line.ends[0].right = split1
              split2 = Line(0, self.rect.x, self.rect.y, UNIT_SIZE, line.width + line.x - self.rect.x)
              split2.ends = {0: newVert, 2: line.ends[2]}
              line.ends[2].left = split2
              newVert.left = split1
              newVert.right = split2
              if previous_direction == 1:
                newVert.down = tempLines[len(tempLines) - 1]
                tempLines[len(tempLines) - 1].ends.update({1: newVert})
              else:
                newVert.up = tempLines[len(tempLines) - 1]
                tempLines[len(tempLines) - 1].ends.update({3: newVert})
            
            lines.append(split1)
            lines.append(split2)
            lines.remove(line)
            
          lines = lines + tempLines
          self.onLine = split1
          self.onVertex = newVert
          tempLines = []
          break
        
    def reset(self):
      self.rect = self.surf.get_rect(
        center=(SCREEN_WIDTH/2 - 5 , SCREEN_HEIGHT - 5))
      self.onLine = lines[3]
      self.onVertex = None
      
# Player helper functions     
def checkVertices(self):
  for direction in self.onLine.ends:
    if (self.rect.x == self.onLine.ends[direction].x) and (self.rect.y == self.onLine.ends[direction].y):
      return self.onLine.ends[direction]

def startNewLineVertical(self, direction):
  newLine = Line(1, self.rect.x, self.rect.y - UNIT_SIZE if direction == 1 else self.rect.y, UNIT_SIZE*2, UNIT_SIZE)
  baseVert = Vertex(self.rect.x, self.rect.y)
  newLine.ends = {1 if direction == 3 else 3: baseVert}
  split1 = Line(0, self.onLine.x, self.onLine.y, UNIT_SIZE, self.rect.x + UNIT_SIZE - self.onLine.x)
  split1.ends = {0: self.onLine.ends[0], 2: baseVert}
  self.onLine.ends[0].right = split1
  split2 = Line(0, self.rect.x, self.rect.y, UNIT_SIZE, self.onLine.width + self.onLine.x - self.rect.x)
  split2.ends = {0: baseVert, 2: self.onLine.ends[2]}
  self.onLine.ends[2].left = split2
  baseVert.left = split1
  baseVert.right = split2
  lines.append(split1)
  lines.append(split2)
  tempLines.append(newLine)
  lines.remove(self.onLine)
  if direction == 1:
    baseVert.up = newLine
  else:
    baseVert.down = newLine
  self.onLine = None
  
def startNewLineHorizontal(self, direction):
  newLine = Line(0, self.rect.x - UNIT_SIZE if direction == 0 else self.rect.x, self.rect.y, UNIT_SIZE, UNIT_SIZE*2)
  baseVert = Vertex(self.rect.x, self.rect.y)
  newLine.ends = {0 if direction == 2 else 2: baseVert}
  split1 = Line(1, self.onLine.x, self.onLine.y, self.rect.y + UNIT_SIZE - self.onLine.y, UNIT_SIZE)
  split1.ends = {1: self.onLine.ends[1], 3: baseVert}
  self.onLine.ends[1].down = split1
  split2 = Line(1, self.rect.x, self.rect.y, self.onLine.length + self.onLine.y - self.rect.y, UNIT_SIZE)
  split2.ends = {1: baseVert, 3: self.onLine.ends[3]}
  self.onLine.ends[3].up = split2
  baseVert.up = split1
  baseVert.down = split2
  lines.append(split1)
  lines.append(split2)
  tempLines.append(newLine)
  lines.remove(self.onLine)
  if direction == 0:
    baseVert.left = newLine
  else:
    baseVert.right = newLine
  self.onLine = None
  
def continueLine(self, direction):
  global previous_direction
  if direction == 0 and previous_direction == 0:
    tempLines[len(tempLines) - 1].x -= UNIT_SIZE
    tempLines[len(tempLines) - 1].width += UNIT_SIZE
  elif direction == 1 and previous_direction == 1:
    tempLines[len(tempLines) - 1].y -= UNIT_SIZE
    tempLines[len(tempLines) - 1].length += UNIT_SIZE
  elif direction == 2 and previous_direction == 2:
    tempLines[len(tempLines) - 1].width += UNIT_SIZE
  elif direction == 3 and previous_direction == 3:
    tempLines[len(tempLines) - 1].length += UNIT_SIZE
  else:
    newVert = Vertex(self.rect.x, self.rect.y)
    if previous_direction == 0:
      newVert.right = tempLines[len(tempLines) - 1]
      tempLines[len(tempLines) - 1].ends.update({0: newVert})
    elif previous_direction == 1:
      newVert.down = tempLines[len(tempLines) - 1]
      tempLines[len(tempLines) - 1].ends.update({1: newVert})
    elif previous_direction == 2:
      newVert.left = tempLines[len(tempLines) - 1]
      tempLines[len(tempLines) - 1].ends.update({2: newVert})
    else:
      newVert.up = tempLines[len(tempLines) - 1]
      tempLines[len(tempLines) - 1].ends.update({3: newVert})
    
    newLine = Line(0 if direction % 2 == 0 else 1, 
                  self.rect.x if direction != 0 else self.rect.x - UNIT_SIZE,
                  self.rect.y if direction != 1 else self.rect.y - UNIT_SIZE,
                  UNIT_SIZE if direction % 2 == 0 else UNIT_SIZE*2,
                  UNIT_SIZE*2 if direction % 2 == 0 else UNIT_SIZE)
    if direction == 0:
      newVert.left = newLine
      newLine.ends = {2: newVert}
    elif direction == 1:
      newVert.up = newLine
      newLine.ends = {3: newVert}
    elif direction == 2:
      newVert.right = newLine
      newLine.ends = {0: newVert}
    else:
      newVert.down = newLine
      newLine.ends = {1: newVert}
    
    tempLines.append(newLine)
    
 
# ENEMY CODE ----------------------------------------------------------------------
class Qix(pygame.sprite.Sprite):
    def __init__(self):
        super(Qix, self).__init__()
        self.surf = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
        self.surf.fill((255, 50, 50))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2 -5 , SCREEN_HEIGHT/2-5)
        )

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        up    = (0,-QIX_MOVE_SPEED)
        down  = (0, QIX_MOVE_SPEED)
        left  = (-QIX_MOVE_SPEED,0)
        right = (QIX_MOVE_SPEED, 0)
        move = [up,down,left,right]
        
        self.rect.move_ip(random.choice(move))

        #makes sure the Qix doesn't move onto the borders where the player is safe
        if self.rect.left < UNIT_SIZE:
            self.rect.left = UNIT_SIZE
        if self.rect.right > SCREEN_WIDTH-UNIT_SIZE:
            self.rect.right = SCREEN_WIDTH-UNIT_SIZE
        if self.rect.top <= UNIT_SIZE:
            self.rect.top = UNIT_SIZE
        if self.rect.bottom >= SCREEN_HEIGHT-UNIT_SIZE:
            self.rect.bottom = SCREEN_HEIGHT-UNIT_SIZE

    def draw(self, surface): #this draws the object on the screen every update
        screen.blit(self.surf, self.rect)    


# RESET BUTTON -------------------------------------
class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('impact', 20)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


# HUD CODE -----------------------------------
def getCoverage():
  return "0%" # placehold

rectangle = pygame.Rect(SCREEN_WIDTH, 0, HUD_WIDTH, SCREEN_HEIGHT)
resetButton = Button((255,0,0), SCREEN_WIDTH + (HUD_WIDTH / 3), 350, HUD_WIDTH / 3, 75, "RESET")
def hudUpdate():
  # draw background
  pygame.draw.rect(screen, (15, 123, 123), rectangle)
  
  # draw title
  title_font = pygame.font.SysFont('impact', 60)
  title_surface = title_font.render('QIX', False, (255, 255, 255))
  title_rect = title_surface.get_rect()
  title_rect.center = ((HUD_WIDTH / 2) + SCREEN_WIDTH, 100)
  screen.blit(title_surface, title_rect)
  
  # draw percentage filled
  percent_font = pygame.font.SysFont('impact', 40)
  percent_surface = percent_font.render(getCoverage(), False, (255, 255, 255))
  percent_rect = percent_surface.get_rect()
  percent_rect.center = ((HUD_WIDTH / 2) + SCREEN_WIDTH, 220)
  screen.blit(percent_surface, percent_rect)
  
  # draw reset button
  resetButton.draw(screen)


# Assign FPS a value
FPS = 15 # FPS = mode
FramePerSec = pygame.time.Clock()

# Initialize pygame-----------------------------------------
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH + HUD_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()
qix = Qix()

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if resetButton.isOver(pygame.mouse.get_pos()):
            tempLines = []
            lines = []
            initLines()
            player.reset()
            
        # Check for KEYDOWN event
        elif event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

        # Check for QUIT event. If user clicks the X button then exit
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    #updates the player/enemy coordinates
    player.update(pressed_keys)
    qix.update()

    # Fill the screen with black, without this it leaves a movement trail, just comment this out to see
    # This woudl be good for showing the player what areas he'll obtain upon successful incursion
    screen.fill((0, 0, 0))
    
    # Update the lines
    if player.checkLineCollision():
      tempLines = []
      lines = []
      initLines()
      player.reset()
      
    if not bool(player.onLine):
      player.checkLineIntersection()

    # Draw the lines
    print(len(lines))
    for line in lines:
      pygame.draw.rect(screen, (122, 122, 122), (line.x, line.y, line.width, line.length))
    for line in tempLines:
      pygame.draw.rect(screen, (210, 210, 210), (line.x, line.y, line.width, line.length))
    
    # Draw the player on the screen
    player.draw(screen)
    qix.draw(screen)  
    #FPS, higher fps = faster player movement when holding the arrow keys 
    FramePerSec.tick(FPS)

    # Update the display
    hudUpdate()
    pygame.display.update()
    pygame.display.flip()
    
    # if player.onVertex:
    #   print(player.onVertex.x)
    #   print(player.onVertex.y)
    #   print(player.onLine.length)
    #   print(player.onLine.width)

# Exit program
pygame.quit()


