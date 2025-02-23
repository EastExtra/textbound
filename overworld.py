import pygame
import sys
import random
from test import battle, Character, Boss, generate_item
import test
from turtledemo.minimal_hanoi import play

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(".")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Player
player_size = 30
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Enemy (yellow circle)
enemy_radius = 20
enemy_x = random.randint(enemy_radius, WIDTH - enemy_radius)
enemy_y = random.randint(enemy_radius, HEIGHT - enemy_radius)

# Game state
enemy_visible = True
boss_battle = False
game_over = False

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Explore area function
def explore_area():
    if random.random() < 0.5:
        item = test.generate_item()
        print(f"You found an item!\n{item}\n")
        return item
    else:
        print("You found nothing of interest here.")
        return None

# Main game loop
while not game_over:
    dt = clock.tick(FPS) / 100.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True  # Exit game loop
        if event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_e:  # If 'E' is pressed
                explore_area()  # Call the explore function

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    if dx != 0 and dy != 0:
        dx *= 1.414
        dy *= 1.414
    player_x += dx * player_speed * dt
    player_y += dy * player_speed * dt

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

            #player_stats is defined locally within the battle encounter logic.
            class PlayerStats:
                def __init__(self, hp, enemies_defeated, turns_taken):
                    self.hp = hp
                    self.enemies_defeated = enemies_defeated
                    self.turns_taken = turns_taken
            player_stats = PlayerStats(hp=100, enemies_defeated=0, turns_taken=0)

            monster = test.create_enemy(player_stats)
            boss = Boss("MegaByte", hp=400, pp=150, attack=30, defense=20)

            battle_result = battle(team, monster)
            if battle_result:
                print("You defeated the monster!")
                boss_battle = True
            else:
                print("You lost the battle!")
                game_over = True

            if boss_battle:
                print("Prepare for the boss battle!")
                battle_result = battle(team, boss)
                if battle_result:
                    print("Congrats! You defeated the boss!")
                    game_over = True
                else:
                    print("You were defeated by the boss...")
                    game_over = True

            if not game_over:
                enemy_visible = True
                enemy_x = random.randint(enemy_radius, WIDTH - enemy_radius)
                enemy_y = random.randint(enemy_radius, HEIGHT - enemy_radius)
                pygame.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Overworld")

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (int(player_x), int(player_y), player_size, player_size))

    if enemy_visible:
        pygame.draw.circle(screen, YELLOW, (int(enemy_x), int(enemy_y)), enemy_radius)
    elif boss_battle:
        font = pygame.font(None, 36)
        text = font.render("Boss Battle in progress!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

if game_over:
    pygame.quit()
    sys.exit()
