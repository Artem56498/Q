import pygame
import random
import math
import sys

# ================== НАЛАШТУВАННЯ ==================
WIDTH, HEIGHT = 900, 600
FPS = 60
MAX_NIGHTS = 99

# Кольори
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("99 Ночей")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 60)

# ================== ГРАВЕЦЬ ==================
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 18
        self.speed = 4
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack_range = 60
        self.attack_cooldown = 300
        self.last_attack = 0

    def move(self, keys):
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def attack(self, enemies):
        now = pygame.time.get_ticks()
        if now - self.last_attack < self.attack_cooldown:
            return
        self.last_attack = now

        for e in enemies[:]:
            dist = math.hypot(self.x - e.x, self.y - e.y)
            if dist <= self.attack_range:
                enemies.remove(e)

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)

# ================== ВОРОГ ==================
class Enemy:
    def __init__(self, night):
        self.size = 20
        self.x = random.choice([0, WIDTH])
        self.y = random.randint(0, HEIGHT)
        self.speed = 1 + night * 0.03
        self.damage = 5

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

# ================== ФУНКЦІЇ ==================
def draw_hp(player):
    bar_width = 200
    hp_ratio = player.hp / player.max_hp
    pygame.draw.rect(screen, RED, (20, 20, bar_width, 20))
    pygame.draw.rect(screen, GREEN, (20, 20, bar_width * hp_ratio, 20))

def draw_text(text, x, y, fnt, color=WHITE):
    screen.blit(fnt.render(text, True, color), (x, y))

def wait(seconds):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < seconds * 1000:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

# ================== ГРА ==================
def game():
    player = Player()
    enemies = []
    night = 1
    state = "DAY"
    game_over = False
    win = False

    while True:
        clock.tick(FPS)
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and state == "NIGHT":
                player.attack(enemies)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or win):
                    return

        keys = pygame.key.get_pressed()

        # -------- DAY --------
        if state == "DAY":
            draw_text(f"Day {night}", WIDTH//2 - 60, HEIGHT//2, big_font)
            pygame.display.update()
            player.hp = player.max_hp
            wait(2)
            enemies.clear()

            enemy_count = 3 + night
            for _ in range(enemy_count):
                enemies.append(Enemy(night))

            state = "NIGHT"

        # -------- NIGHT --------
        elif state == "NIGHT":
            player.move(keys)

            for e in enemies:
                e.move(player)
                dist = math.hypot(player.x - e.x, player.y - e.y)
                if dist < player.radius + e.size / 2:
                    player.hp -= e.damage

            if player.hp <= 0:
                game_over = True

            if not enemies:
                night += 1
                if night > MAX_NIGHTS:
                    win = True
                else:
                    state = "DAY"

            player.draw()
            for e in enemies:
                e.draw()

            draw_hp(player)
            draw_text(f"Night {night} / {MAX_NIGHTS}", 20, 50, font)

        # -------- GAME OVER --------
        if game_over:
            draw_text("GAME OVER", WIDTH//2 - 140, HEIGHT//2 - 40, big_font, RED)
            draw_text("Press R to Restart", WIDTH//2 - 120, HEIGHT//2 + 20, font)
            pygame.display.update()
            continue

        # -------- WIN --------
        if win:
            draw_text("YOU WIN!", WIDTH//2 - 120, HEIGHT//2 - 40, big_font, GREEN)
            draw_text("Press R to Restart", WIDTH//2 - 120, HEIGHT//2 + 20, font)
            pygame.display.update()
            continue

        pygame.display.update()

# ================== ЗАПУСК ==================
while True:
    game()

