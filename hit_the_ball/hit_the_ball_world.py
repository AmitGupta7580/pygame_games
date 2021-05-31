import random
import math
import time
import threading
import pygame
from pygame.draw import rect, circle, line


# ===  Global Parameters  ===
ARENA_HEIGHT = 410
ARENA_WIDTH = 410
LOGGER_HEIGHT = 70
LOGGER_WIDTH = 410
FALSE_AREA_HEIGTH = 50
# ===========================

class HitTheBallLogger:
  def __init__(self, screen) :
    self.LOOGING_BACKGROUND = (255, 255, 255)

    # pygame surface
    self.screen = screen

    # Updating screen for score and steps
    self.update_screen(0)

  def update_screen(self, score):

    # clearing logging area
    rect(self.screen, self.LOOGING_BACKGROUND, pygame.Rect(0, 410, LOGGER_WIDTH, LOGGER_HEIGHT))

    # Adding score and steps
    font = pygame.font.SysFont("Times new Roman", 25)
    self.screen.blit(font.render("Score : {}".format(score), True, (0, 0, 0)), (150, 430))  # Score

class HitTheBallWorld:
  def __init__(self, chances) :
    pygame.init()
    self.BACKGROUND_COLOR = (0, 0, 0)
    self.WALL_COLOR = (203,65,84)
    self.BALL_COLOR = (255, 0, 0)
    self.BAR_COLOR = (50, 255, 50)
    self.WALL_WIDTH = 5
    self.BALL_RADIUS = 7
    self.BALL_VELOCITY = 6 # pixel per second
    self.BAR_LENGTH = 50
    self.BAR_WIDTH = 4
    self.BAR_Y = ARENA_WIDTH - self.WALL_WIDTH - FALSE_AREA_HEIGTH + (self.BAR_WIDTH//2)

    # pygame surface
    self.screen = pygame.display.set_mode((ARENA_WIDTH, ARENA_HEIGHT + LOGGER_HEIGHT))
    pygame.display.set_caption('Hit The Ball Game')

    # Drawing Walls
    min_X = (self.WALL_WIDTH/2)
    max_X = ARENA_HEIGHT - (self.WALL_WIDTH/2)
    corner = [(min_X, min_X), (min_X, max_X), (max_X, min_X), (max_X, max_X)]
    line(self.screen, self.WALL_COLOR, corner[0], corner[1], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[0], corner[2], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[1], corner[3], width=self.WALL_WIDTH)
    line(self.screen, self.WALL_COLOR, corner[2], corner[3], width=self.WALL_WIDTH)

    # Drawing the line of False Area
    line(self.screen, (255, 255, 255), (5, 360), (ARENA_WIDTH-5, 360), width=2)

    # Creating Logger
    self.logger = HitTheBallLogger(self.screen)

    # elements of game
    self.bar = None
    self.ball_pos = None
    self.ball_vel_x = None
    self.ball_vel_y = None

    self.thread = None
    self.shutdown = False
    self.chance = chances
    # self.restart()

  def restart(self):
    print("Chance Count : {}".format(self.chance))

    # closing previous thread
    if self.thread is not None:
      self.thread.join()

    # Erase previous snake and food
    if self.ball_pos is not None:
      # erase ball
      x, y = self.ball_pos
      circle(self.screen, self.BACKGROUND_COLOR, (x, y), self.BALL_RADIUS)
      self.ball_pos = None
    if self.bar is not None:
      # erase bar
      line(self.screen, self.BACKGROUND_COLOR, (self.bar - (self.BAR_LENGTH//2), self.BAR_Y), (self.bar + (self.BAR_LENGTH//2), self.BAR_Y), width=self.BAR_WIDTH)
      self.bar = None

    # spawing bar
    self.bar = 200
    self.render_bar(200)

    # spawning ball
    self.ball_pos = (200, self.BAR_Y - self.BALL_RADIUS - (self.BAR_WIDTH//2))
    self.ball_vel_x = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    self.ball_vel_y = -math.sqrt(self.BALL_VELOCITY ** 2 - self.ball_vel_x ** 2)
    self.render_ball((200, self.BAR_Y - self.BALL_RADIUS - (self.BAR_WIDTH//2)))

    # Keep track of score and steps
    self.score = 0

    # update screen of logger
    self.logger.update_screen(self.score)

    # running thread for ball
    self.shutdown = False
    self.thread = threading.Thread(target=self.move_ball)
    self.thread.start()

  def render_ball(self, center):
    x_prev, y_prev = self.ball_pos
    x, y = center

    # Collision with left and right wall
    if x < 5 + self.BALL_RADIUS:
      x = 5 + self.BALL_RADIUS
      self.ball_vel_x = -self.ball_vel_x
    elif x > 405 - self.BALL_RADIUS:
      x = 405 - self.BALL_RADIUS
      self.ball_vel_x = -self.ball_vel_x

    # collision with top wall
    if y < 5 + self.BALL_RADIUS:
      y = 5 + self.BALL_RADIUS
      self.ball_vel_y = -self.ball_vel_y
    
    # collison with bottom line
    if y > self.BAR_Y - self.BALL_RADIUS - (self.BAR_WIDTH//2):
      if x <= self.bar + (self.BAR_LENGTH//2) + 2 and x >= self.bar - (self.BAR_LENGTH//2) - 2:
        y = self.BAR_Y - self.BALL_RADIUS - (self.BAR_WIDTH//2)
        self.ball_vel_y = -self.ball_vel_y
        # score a point
        self.score += 1
      else: # crossing False line
        self.chance -= 1
        self.shutdown = True
        # raise exception

    # erase previous position of ball
    circle(self.screen, self.BACKGROUND_COLOR, (x_prev, y_prev), self.BALL_RADIUS)

    # draw ball
    circle(self.screen, self.BALL_COLOR, (x, y), self.BALL_RADIUS)
    self.ball_pos = (x, y)

  def move_ball(self):
    while not self.shutdown:
      x_init, y_init = self.ball_pos
      x = int(self.ball_vel_x + x_init)
      y = int(self.ball_vel_y + y_init)
      self.render_ball((x, y))
      time.sleep(0.02)

  def render_bar(self, X):
    bar_half_length = (self.BAR_LENGTH//2)

    # Border Cases
    if X - bar_half_length < 5:
      X = bar_half_length + 5
    if X + bar_half_length > 405:
      X = 405 - bar_half_length

    # erase bar from prev_position
    line(self.screen, self.BACKGROUND_COLOR, (self.bar - bar_half_length, self.BAR_Y), (self.bar + bar_half_length, self.BAR_Y), width=self.BAR_WIDTH)

    # draw bar
    line(self.screen, self.BAR_COLOR, (X - bar_half_length, self.BAR_Y), (X + bar_half_length, self.BAR_Y), width=self.BAR_WIDTH)
    self.bar = X

  def move_bar(self, direction):
    x = self.bar
    if direction == 'left':
      x -= 12
    elif direction == 'right':
      x += 12
    
    self.render_bar(x)

  def run(self) :

    while self.chance > 0:
      self.restart()

      direction = None
      while not self.shutdown:
        # fetching pressed key
        for event in pygame.event.get():  
          if event.type == pygame.QUIT:  
            break
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
              direction = 'left'
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
              direction = 'right'
      
        # Move bar
        if direction is not None:
          self.move_bar(direction)

        # update looging screen
        self.logger.update_screen(self.score)

        pygame.display.flip()
        direction = None


if __name__ == '__main__':
  print("Inside Main Function")
  chances = 5
  world = HitTheBallWorld(chances)
  world.run()