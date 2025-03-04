import pygame
import random

FPS = 60
WIDTH = 600
HEIGHT = 800

INDENT = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - INDENT
        self.shoot_delay = 300
        self.shoot_timer = pygame.time.get_ticks() - self.shoot_delay
        self.lives = 3
        self.lives_timer = pygame.time.get_ticks()
        self.hidden = False
        self.health = 100
        self.speedx = 0

    def update(self):
        self.speedx = 0
        if player.hidden:
            now = pygame.time.get_ticks()
            if now - self.lives_timer > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - INDENT
        else:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            if self.rect.left < INDENT:
                self.rect.left = INDENT
            if self.rect.right > WIDTH - INDENT:
                self.rect.right = WIDTH - INDENT

    def get_lives(self, value):
        player.health -= value
        if player.health <= 0:
            player.lives -= 1
            player.hidden = True
            player.rect.top = HEIGHT + 50
            player.lives_timer = pygame.time.get_ticks()
            if player.lives > 0:
                player.health = 100
        return player.lives

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - player.shoot_timer > self.shoot_delay:
            bullet = Bullet()
            bullets.add(bullet)
            all_sprites.add(bullet)
            player.shoot_timer = now


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(20, 60, 10)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedx = random.randrange(-3, 4)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -30)
            self.speedx = random.randrange(-3, 4)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.bottom = player.rect.y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    screen.blit(surface, rect)


def draw_health(value):
    border_rect = pygame.Rect(10, 10, 102, 12)
    health_rect = pygame.Rect(11, 11, value, 10)
    pygame.draw.rect(screen, WHITE, border_rect)
    pygame.draw.rect(screen, GREEN, health_rect)


def draw_lives(value):
    for i in range(value):
        draw_text("X", 20, RED, WIDTH - 20 * (i + 1), 10)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

delay = 0
score = 0
font_name = pygame.font.match_font('arial', bold=True)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


def create_enemy():
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)


for i in range(10):
    create_enemy()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        create_enemy()
        if player.get_lives(hit.size) == 0:
            delay = 3000
            running = False

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 70 - hit.size
        create_enemy()

    screen.fill(BLACK)
    draw_health(player.health)
    draw_text(f"Очки: {score}", 20, WHITE, WIDTH / 2, 10)
    draw_lives(player.lives)
    if delay == 0:
        all_sprites.draw(screen)
    else:
        draw_text("Игра завершена", 50, RED, WIDTH / 2, HEIGHT / 2 - 50)
    pygame.display.flip()
pygame.time.delay(delay)
pygame.quit()
