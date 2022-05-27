import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

screen_width  = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blocks World")


ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
ball_color = (200,200,200)
ball_speed_x = 5
ball_speed_y = 5

block = pygame.Rect(screen_width/2-15, screen_height/2-45, 30, 90)
block_color = (100,100,100)
block_move_y = 0


bg_color = pygame.Color('grey12')


click_pos = None
while True:
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                block_move_y = 10
            if event.key == pygame.K_UP:
                block_move_y = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                block_move_y = 0
            if event.key == pygame.K_UP:
                block_move_y = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
            
        

    if block.colliderect(ball):
        ball_speed_x = -ball_speed_x

    print(f"click {click_pos}")
    if click_pos and block.collidepoint(click_pos):
        block_move_y = 10
        print(f"click {click_pos}")
    else:
        block_move_y = 0

    block.y += block_move_y
    

    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x


    screen.fill(bg_color)   
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.rect(screen, block_color, block)

    
    pygame.display.flip()
    clock.tick(60)