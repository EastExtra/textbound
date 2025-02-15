import pygame 
import sys 
import random 
from test import battle, Character, Boss 

pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(".")

#colors 
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)

#player 
player_size = 50 
player_x = WIDTH // 2 
player_y = HEIGHT // 2 
player_speed = 5 

#enemy(yellow circle)
enemy_radius = 20
enemy_x = random.randint(enemy_radius, WIDTH - enemy_radius)
enemy_y = random.randint(enemy_radius, HEIGHT - enemy_radius)

#game state
enemy_visible = True 

#frame rate
clock = pygame.time.Clock()
FPS = 60

#boss
boss_battle = False 

#main game loop 
running = True 
while running:
    dt = clock.tick(FPS) / 100.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        dx += player_speed * dt  
    if keys[pygame.K_UP]:
        dy -= player_speed * dt 
    if keys[pygame.K_DOWN]:
        dy += player_speed * dt 

    if dx != 0 and dy != 0:
        dx *= 0.707
        dy *= 0.707

    player_x += dx
    player_y += dy

    player_x = max(0, min(player_x, WIDTH - player_size))
    player_y = max(0, min(player_y, HEIGHT - player_size))
    
    if enemy_visible:
        distance = ((player_x + player_size/2 - enemy_x)**2 + (player_y + player_size/2 - enemy_y)**2)**0.5
        if distance < (player_size/2 + enemy_radius):
            enemy_visible = False 

            # Main battle 
            pythonie = Character("Pythonie", hp=100, pp=50, attack=15, defense=5)
            javacript = Character("Javacript", hp=90, pp=60, attack=12, defense=4)
            rustacean = Character("Rustacean", hp=120, pp=30, attack=18, defense=8)
            golanger = Character("Golanger", hp=110, pp=40, attack=14, defense=6)
            team = [pythonie, javacript, rustacean, golanger]
            monster = Character("Monster", hp=50, pp=20, attack=10, defense=3)
            boss = Boss("MegaByte", hp=300, pp=100, attack=25, defense=15)

            battle_result = battle(team, monster)
            if battle_result:
                print("You defeated the monster!")
                boss_battle = True 
            else:
                print("You lost the battle!")
                running = False 

            if boss_battle:
                print("Prepare for the boss battle!")
                battle_result = battle(team, boss)
                if battle_result:
                    print("Congrats! You defeated the boss!")
                else:
                    print("You were defeated by the boss...")
                running = False # end game after boss battle 

            if running:
                pygame.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Overworld")

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (int(player_x), int(player_y), player_size, player_size))

    if enemy_visible:
        pygame.draw.circle(screen, YELLOW, (int(enemy_x), int(enemy_y)), enemy_radius)
    elif boss_battle:
        font = pygame.font.Font(None, 36)
        text = font.render("Boss Battle in progress!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()

