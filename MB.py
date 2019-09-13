import math, pygame
import GY521
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)
YELLOW = (255,255,0)
 
# Size of break-out blocks
block_width = 50
block_height = 15
 
 
class Block(pygame.sprite.Sprite):
    """This class represents each block that will get knocked out by the ball
    It derives from the "Sprite" class in Pygame """
 
    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block,
            and its x and y position. """
        super(Block, self).__init__()
 
        self.image = pygame.Surface([block_width, block_height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
 
class Ball(pygame.sprite.Sprite):
    """ This class represents the ball
        It derives from the "Sprite" class in Pygame """
    speed = 12
    x = randint(0,360)
    y = 180
    direction = 200
 
    width = 12
    height = 12
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        super(Ball, self).__init__()

        self.image = pygame.Surface([self.width, self.height])
 
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
 
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        # Draw the ball
        pygame.draw.ellipse(self.image, WHITE, self.rect)
        
    def bounce(self, diff):
        """ This function will bounce the ball
            off a horizontal surface (not a vertical one) """
 
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
 
        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls. """
    
    speed = 0
 
    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        super(Player, self).__init__()
 
        self.width = 80
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((YELLOW))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
    def update(self):
        """ Update the player position. """
        #print GY521.getSerial()
        speed = ( GY521.getSerial() )/1000
        self.rect.x += speed
        # Hold paddle on screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
        if self.rect.x < 0:
            self.rect.x = 0

pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Motion Breakout bylong')
pygame.mouse.set_visible(0)
background = pygame.Surface(screen.get_size())
 
font = pygame.font.Font(None, 100)
 
# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
 
# Create the player paddle object
player = Player()
allsprites.add(player)
 
# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)
 
# The top of the block (y position)
top = 80
 
# Number of blocks to create
blockcount = 15
 
# --- Create blocks
 
# Five rows of blocks
for row in range(5):
    # 32 columns of blocks
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block = Block(BLUE, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # Move the top of the next row down
    top += block_height + 2

clock = pygame.time.Clock()

game_over = False

exit_program = False

lag = 1
 
# Main program loop
while not exit_program:
    clock.tick(30)
 
    screen.fill(BLACK)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
 
    if not game_over:
        # Update the player and ball positions
        player.update()
        game_over = ball.update()
 
    # If we are done, print game over
    if game_over:
        text = font.render("Game Over", True, WHITE)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
 
    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, balls, False):
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
 
        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
 
    # Check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    
    if len(deadblocks) > 0:
        ball.bounce(0)
 
        # Game ends if all the blocks are gone
        if len(blocks) == 0:
            game_over = True

    allsprites.draw(screen)
    pygame.display.flip()
    
    
    while lag > 0:
        lag -=1
        clock.tick(1)
        
pygame.quit()
