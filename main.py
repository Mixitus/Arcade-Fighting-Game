import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# create a game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#draws over screen and transparency
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Brawler")

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# define colors
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 205)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player 1 and player 2 scores [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 100
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [43, 30]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 100
WIZARD_SCALE = 5
WIZARD_OFFSET = [38, 30]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/YoimiyaTheme.mp3")
pygame.mixer.music.set_volume(0.5)#cuts the volume in half
pygame.mixer.music.play(-1, 0.0, 5000)#music fades in slowly
samurai_fx = pygame.mixer.Sound("assets/audio/sword.wav")
samurai_fx.set_volume(0.5)
ninja_fx = pygame.mixer.Sound("assets/audio/sword.wav")
ninja_fx.set_volume(0.5)


# load background image
bg_image = pygame.image.load("assets/images/background/TokyoBackground.png").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/sprites/warrior-final.png").convert_alpha()

wizard_sheet = pygame.image.load("assets/images/wizard/sprites/wizard-final.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define the number of steps per animation

WARRIOR_ANIMATION_STEPS = [4, 8, 2, 2, 4, 4, 4, 4]
WIZARD_ANIMATION_STEPS = [4, 8, 2, 2, 4, 4, 4, 4]

#define font and size
count_font = pygame.font.Font("assets/fonts/FightingSpirit.ttf", 80)
score_font = pygame.font.Font("assets/fonts/FightingSpirit.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for drawing health bars
def draw_health_bars(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, samurai_fx)
fighter_2 = Fighter(2, 700, 280, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, ninja_fx)

# game loop (keeps the window on the screen until ready to exit game)
run = True
while run:
    clock.tick(FPS)
    # draw background
    draw_bg()
# show player stats
    draw_health_bars(fighter_1.health, 20, 20)
    draw_health_bars(fighter_2.health, 580, 20)
    draw_text("Samurai", score_font, RED, 20, 60)
    draw_text("Ninja", score_font, RED, 900, 60)
    draw_text("P1: " + str(score[0]), score_font, RED, 350, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)


    #update countdown
    if intro_count <= 0:
      # move fighters
      fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
      fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
      #display count timer, converting the integer to a string
      draw_text(str(intro_count), count_font, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update count timer
      if (pygame.time.get_ticks() - last_count_update) > 1000:
        intro_count -= 1
        last_count_update = pygame.time.get_ticks()




    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      #display victory image
      screen.blit(victory_img, (360, 150))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, samurai_fx)
        fighter_2 = Fighter(2, 700, 280, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, ninja_fx)

    # event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False






# update display
    pygame.display.update()

# exit pygame
pygame.quit()