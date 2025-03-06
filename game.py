import pygame
import random
from os import path

FPS = 60
WIDTH = 600
HEIGHT = 800

INDENT = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

IMAGE_PATH = path.join(path.dirname(__file__), 'images')
SOUND_PATH = path.join(path.dirname(__file__), 'sounds')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 40))
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
            shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(20, 60, 10)
        self.image = pygame.transform.scale(random.choice(enemy_images), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedx = random.randrange(-3, 4)
        self.speedy = random.randrange(1, 8)
        self.rotation_angle = 0
        self.rotation_image = self.image.copy()
        self.rotation_timer = pygame.time.get_ticks()
        self.rotation_speed = random.randrange(-8, 8)

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -30)
            self.speedx = random.randrange(-3, 4)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.rotation_timer > FPS:
            center = self.rect.center
            self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.rotation_image, self.rotation_angle)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.rotation_timer = now


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.bottom = player.rect.y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.explosion_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.explosion_timer > FPS:
            self.frame += 1
            if self.frame == len(explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            self.explosion_timer = now


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = powerup_image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
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
    image = pygame.transform.scale(player_image, (20, 20))
    for i in range(value):
        rect = image.get_rect()
        rect.x = WIDTH - 90 + 30 * i
        rect.y = 10
        screen.blit(image, rect)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

delay = 0
score = 0

font_name = pygame.font.match_font('arial', bold=True)
player_image = pygame.image.load(path.join(IMAGE_PATH, 'player.png'))
bullet_image = pygame.image.load(path.join(IMAGE_PATH, 'laser.png'))
powerup_image = pygame.image.load(path.join(IMAGE_PATH, 'shield.png'))
enemy_images = []
for i in range(1, 5):
    enemy_images.append(pygame.image.load(path.join(IMAGE_PATH, f'meteor_{i}.png')))
explosion_images = []
for i in range(1, 10):
    explosion_images.append(pygame.image.load(path.join(IMAGE_PATH, f'explosion_{i}.png')))

shoot_sound = pygame.mixer.Sound(path.join(SOUND_PATH,'shoot.wav'))
crash_sound = pygame.mixer.Sound(path.join(SOUND_PATH,'crash.wav'))
explosion_sound = pygame.mixer.Sound(path.join(SOUND_PATH,'explosion.wav'))

pygame.mixer.music.load(path.join(SOUND_PATH,'sound.mp3'))
pygame.mixer.music.set_volume(0.1)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


def create_enemy():
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)


for i in range(10):
    create_enemy()

running = True
pygame.mixer.music.play(-1)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        create_enemy()
        crash_sound.play()
        if player.get_lives(hit.size) == 0:
            delay = 3000
            running = False

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        explosion_sound.play()
        score += 70 - hit.size
        all_sprites.add(Explosion(hit.rect.center, hit.size))
        if random.random() < 0.1:
            powerup = Powerup(hit.rect.center)
            powerups.add(powerup)
            all_sprites.add(powerup)
        create_enemy()

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        player.health += 10
        if player.health > 100:
            player.health = 100

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
