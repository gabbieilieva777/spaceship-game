import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #създава прозореца
pygame.display.set_caption("Spaceships")

#цветове в rgb
BLUE = (10, 100, 145)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

FPS = 60 
VEL = 5
BULLET_VEl = 7
MAX_BULLETS = 3


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) #създава правоъгълник, който разделя прозореца на две полета


BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/bulletfire.wav')
SPACESHIP_HIT_SOUND = pygame.mixer.Sound('assets/spaceship_hit.wav')
RESTART_SOUND = pygame.mixer.Sound('assets/win_sound.wav')
VICTORY_SOUND = pygame.mixer.Sound('assets/victory.wav')

HEALTH_FONT = pygame.font.SysFont('roboto', 40)
WINNER_FONT = pygame.font.SysFont('roboto', 100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_red.png'))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2



YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
#променя размерите на корабите и ги обръща, така че да сочат един към друг

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.jpg')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #в тази функция се рисува всичко на екрана
    #WIN.fill(BLUE) -> така се запълва с цвят, ако не се използва изображение за фон
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))



    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet) #рисуват се куршумите

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_movement(keys_pressed, yellow): #функция за движението и границите на движение на единия кораб
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # down
        yellow.y += VEL


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down
        red.y += VEL

def bullets(yellow_bullets, red_bullets, yellow, red): #функция за движението на куршумите, като за куршумите на всеки кораб има отделен цикъл
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEl
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VEl
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text): #функция специално за текста накрая на играта, който обявява победителя

   draw_text = WINNER_FONT.render(text, 1, WHITE)
   WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_width()/2))
   pygame.display.update()
   VICTORY_SOUND.play()
   pygame.time.delay(5000)


def main(): #главната функция, в която се случва всичко
    yellow = pygame.Rect(200, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #задава fps на програмата
        for event in pygame.event.get():  #цикъл, в който сe намират всички events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                #този if прави така, че като натиснем x, за да затворим прозореца програмата реално се затваря

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1
                SPACESHIP_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                SPACESHIP_HIT_SOUND.play()



        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            draw_winner(winner_text)
            RESTART_SOUND.play()
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()


main()
#накрая викаме главната фунцкия, с което викаме и всички функции в нея