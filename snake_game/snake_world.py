import random
import pygame
from pygame.draw import rect, circle, line


# ===  Global Parameters  ===
ARENA_HEIGHT = 410
ARENA_WIDTH = 410
LOGGER_HEIGHT = 100
LOGGER_WIDTH = 410
# ===========================

class SnakeWorldLogger:
  def __init__(self, screen) :
    self.LOOGING_BACKGROUND = (255, 255, 255)

    # pygame surface
    self.screen = screen

    # clearing logging area
    rect(self.screen, self.LOOGING_BACKGROUND, pygame.Rect(0, 410, LOGGER_WIDTH, LOGGER_HEIGHT))

    # line seprating score and controlller guide
    line(self.screen, (203,65,84), (LOGGER_WIDTH//2, 410), (LOGGER_WIDTH//2, 410 + LOGGER_HEIGHT), width=5)

    # Adding Controller Guide
    font = pygame.font.SysFont("Times new Roman", 13)
    screen.blit(font.render("W (UP)", True, (0, 0, 0)), (80, 425))     # Up
    screen.blit(font.render("S (DOWN)", True, (0, 0, 0)), (70, 475))   # Down
    screen.blit(font.render("A (LEFT)", True, (0, 0, 0)), (10, 450))   # Left
    screen.blit(font.render("D (RIGHT)", True, (0, 0, 0)), (140, 450))  # Right

    # Updating screen for score and steps
    self.update_screen(0, 0)

  def update_screen(self, score, steps):

    # clearing right-logging area
    rect(self.screen, self.LOOGING_BACKGROUND, pygame.Rect(207.5, 410, 202.5, LOGGER_HEIGHT))

    # Adding score and steps
    font = pygame.font.SysFont("Times new Roman", 25)
    self.screen.blit(font.render("Steps : {}".format(steps), True, (0, 0, 0)), (255, 425))  # Steps
    self.screen.blit(font.render("Score : {}".format(score), True, (0, 0, 0)), (255, 470))  # Score

class SnakeWorld:
  def __init__(self) :
    pygame.init()
    self.BACKGROUND_COLOR = (0, 0, 0)
    self.BLOCK_SIZE = 20
    self.WALL_COLOR = (203,65,84)
    self.FOOD_COLOR = (255, 0, 0)
    self.SNAKE_COLOR = (50, 255, 50)
    self.WALL_WIDTH = 5
    self.FOOD_RADIUS = 7

    # pygame surface
    self.screen = pygame.display.set_mode((ARENA_WIDTH, ARENA_HEIGHT + LOGGER_HEIGHT))
    pygame.display.set_caption('Snake Game')

    # Drawing Walls
    min_X = (self.WALL_WIDTH/2)
    max_X = ARENA_HEIGHT - (self.WALL_WIDTH/2)
    corner = [(min_X, min_X), (min_X, max_X), (max_X, min_X), (max_X, max_X)]
    line(self.screen, self.WALL_COLOR, corner[0], corner[1], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[0], corner[2], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[1], corner[3], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[2], corner[3], width=self.WALL_WIDTH)

    # Creating Logger
    self.logger = SnakeWorldLogger(self.screen)

    # elements of game
    self.food = None
    self.snake_pos = []
    self.snake = None
    self.restart()

  def restart(self):

    # Erase previous snake and food
    if self.food is not None:
      extra = (self.BLOCK_SIZE/2)
      x, y = self.pos_to_cords(self.food)
      circle(self.screen, self.BACKGROUND_COLOR, (x + extra, y + extra), self.FOOD_RADIUS)
      self.food = None
    if len(self.snake_pos) > 0:
      for body in self.snake_pos:
        x, y = body
        X, Y = self.pos_to_cords((x, y))
        rect(self.screen, self.BACKGROUND_COLOR, pygame.Rect(X, Y, self.BLOCK_SIZE, self.BLOCK_SIZE))

    # spawing snake
    self.snake_pos = [(0, 0)]
    self.snake = (0, 0)
    x, y = self.pos_to_cords(self.snake)
    rect(self.screen, self.SNAKE_COLOR, pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))

    # Spawing food
    self.spawn_food()

    # Keep track of score and steps
    self.score = 0
    self.steps = 0

    # update screen of logger
    self.logger.update_screen(self.score, self.steps)

  def spawn_food(self):
    # erasing previous position
    extra = (self.BLOCK_SIZE/2)
    if self.food is not None:
      x, y = self.pos_to_cords(self.food)
      circle(self.screen, self.BACKGROUND_COLOR, (x + extra, y + extra), self.FOOD_RADIUS)

    # selecting new position
    positions = self.empty_cells()
    self.food = positions[random.randint(0, len(positions)-1)] # randomly selects pos of food
    x, y = self.pos_to_cords(self.food)
    circle(self.screen, self.FOOD_COLOR, (x + extra, y + extra), self.FOOD_RADIUS)

  def move_snake(self, direction):
    x, y = self.snake
    if direction == 'left':
      x -= 1
    elif direction == 'right':
      x += 1
    elif direction == 'front':
      y -= 1
    elif direction == 'back':
      y += 1

    # Border Cases
    if x < 0 or x > 19 or y < 0 or y > 19:
      # raise exception going outside of arena
      raise Exception

    # next cell its own tail
    for body in self.snake_pos:
      if body == (x, y):
        # raise exception of cutting its own tail
        raise Exception

    # increment in no. of steps
    self.steps += 1

    # next cell is food
    if self.food == (x, y):
      self.score += 1
      self.spawn_food()
    else :
      # move tail of snake
      x_tail, y_tail = self.snake_pos.pop(0)
      X, Y = self.pos_to_cords((x_tail, y_tail))
      rect(self.screen, self.BACKGROUND_COLOR, pygame.Rect(X, Y, self.BLOCK_SIZE, self.BLOCK_SIZE))

    # got new state x, y
    X, Y = self.pos_to_cords((x, y))
    rect(self.screen, self.SNAKE_COLOR, pygame.Rect(X, Y, self.BLOCK_SIZE, self.BLOCK_SIZE))
    self.snake = (x, y)
    self.snake_pos.append((x, y))
    self.logger.update_screen(self.score, self.steps)

  def run(self) :
    direction = None
    while True:
      # fetching pressed key
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
          break
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP or event.key == pygame.K_w:
            direction = 'front'
          if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            direction = 'back'
          if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            direction = 'left'
          if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            direction = 'right'

      # snake is moved
      if direction is not None:
        self.move_snake(direction)
      
      pygame.display.flip()

      # setting direction to default value
      direction = None

  def pos_to_cords(self, pos):
    # convert local index to pygame surface pixels
    x = pos[0] * self.BLOCK_SIZE + 5
    y = pos[1] * self.BLOCK_SIZE + 5
    return (x, y)

  def empty_cells(self):
    # fetching empty cells
    positions = []
    for row in range(ARENA_HEIGHT//self.BLOCK_SIZE):
      for col in range(ARENA_WIDTH//self.BLOCK_SIZE):
        cell = (row, col)
        found = False

        # searching in all the possible cells occupied by snake
        for pos in self.snake_pos:
          if pos == cell:
            found = True
            break
        if not found:
          positions.append(cell)

    return positions


if __name__ == '__main__':
  print("Inside Main Function")
  world = SnakeWorld()
  chances = 5
  while chances > 0:
    try:
      world.run()
    except Exception:
      world.restart()
      chances -= 1
      print(f"Chances Left : {chances}")
    