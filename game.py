import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
RED = (255, 50, 50)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 255)
ORANGE = (255, 165, 0)

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Harrycane - The Poop Cannon Game!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a cooler Harry character with sunglasses and cape
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        
        # Draw cape (behind)
        pygame.draw.polygon(self.image, RED, [(10, 30), (5, 45), (15, 55), (20, 35)])
        pygame.draw.polygon(self.image, RED, [(40, 30), (45, 45), (35, 55), (30, 35)])
        
        # Draw body (cool outfit)
        pygame.draw.rect(self.image, BLACK, (15, 35, 20, 30))
        
        # Draw head
        pygame.draw.circle(self.image, (255, 220, 177), (25, 20), 15)
        
        # Draw cool sunglasses frames (black)
        pygame.draw.rect(self.image, BLACK, (14, 17, 9, 7), 2)
        pygame.draw.rect(self.image, BLACK, (26, 17, 9, 7), 2)
        # Bridge between lenses
        pygame.draw.line(self.image, BLACK, (23, 20), (26, 20), 2)
        # Temples (arms of glasses)
        pygame.draw.line(self.image, BLACK, (14, 20), (8, 18), 2)
        pygame.draw.line(self.image, BLACK, (35, 20), (40, 18), 2)
        
        # Clear lenses showing BROWN eyes underneath
        pygame.draw.circle(self.image, WHITE, (18, 20), 3)  # White of eye
        pygame.draw.circle(self.image, (101, 67, 33), (18, 20), 2)  # Brown iris
        pygame.draw.circle(self.image, BLACK, (18, 20), 1)  # Pupil
        
        pygame.draw.circle(self.image, WHITE, (30, 20), 3)  # White of eye
        pygame.draw.circle(self.image, (101, 67, 33), (30, 20), 2)  # Brown iris
        pygame.draw.circle(self.image, BLACK, (30, 20), 1)  # Pupil
        
        # Draw cool smile
        pygame.draw.arc(self.image, BLACK, (13, 23, 24, 12), 3.14, 0, 2)
        
        # Draw spiky cool hair
        points = [(18, 8), (20, 12), (22, 8), (24, 12), (26, 8), (28, 12), (30, 8), (32, 12)]
        for i in range(0, len(points)-1, 2):
            pygame.draw.polygon(self.image, BROWN, [points[i], points[i+1], (points[i][0]+2, points[i][1])])
        
        # Draw arms
        pygame.draw.rect(self.image, (255, 220, 177), (10, 40, 5, 15))
        pygame.draw.rect(self.image, (255, 220, 177), (35, 40, 5, 15))
        
        # Add "HARRY" nameplate above head
        font = pygame.font.Font(None, 16)
        text = font.render("HARRY", True, BLACK)
        # White background for nameplate
        text_rect = text.get_rect()
        pygame.draw.rect(self.image, WHITE, (8, 0, 34, 8))
        self.image.blit(text, (10, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = WINDOW_HEIGHT - 120
        self.speed = 5
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < WINDOW_HEIGHT - self.rect.height:
            self.rect.y += self.speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, is_super=False):
        super().__init__()
        self.is_super = is_super
        self.frame = 0
        
        if is_super:
            # Create SUPER POOP - MUCH BIGGER!
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.draw_super_poop()
            self.speed = 10
        else:
            # Create a more realistic poop projectile with swirl
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.draw_normal_poop()
            self.speed = 8
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_normal_poop(self):
        # Bottom layer - darker brown
        pygame.draw.ellipse(self.image, (101, 52, 13), (3, 15, 24, 12))
        
        # Middle layer
        pygame.draw.ellipse(self.image, BROWN, (5, 8, 20, 15))
        
        # Top swirl
        pygame.draw.ellipse(self.image, (160, 82, 45), (8, 3, 14, 12))
        pygame.draw.ellipse(self.image, (139, 69, 19), (10, 1, 10, 8))
        
        # Add some texture spots
        pygame.draw.circle(self.image, (101, 52, 13), (12, 12), 2)
        pygame.draw.circle(self.image, (101, 52, 13), (18, 15), 2)
        pygame.draw.circle(self.image, (80, 42, 10), (15, 18), 1)
        
        # Swirl tip
        pygame.draw.circle(self.image, (160, 82, 45), (15, 4), 3)
    
    def draw_super_poop(self):
        # Clear previous frame
        self.image.fill((0, 0, 0, 0))
        
        # Rotating rainbow aura
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for i, color in enumerate(colors):
            angle = (self.frame * 10 + i * 60) % 360
            radius = 28 + (i % 3) * 2
            x = 30 + int(radius * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).x)
            y = 30 + int(radius * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(self.image, color, (x, y), 4)
        
        # Electric sparks
        for i in range(8):
            angle = (self.frame * 20 + i * 45) % 360
            start_x = 30 + int(20 * pygame.math.Vector2(1, 0).rotate(angle).x)
            start_y = 30 + int(20 * pygame.math.Vector2(1, 0).rotate(angle).y)
            end_x = 30 + int(28 * pygame.math.Vector2(1, 0).rotate(angle).x)
            end_y = 30 + int(28 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.line(self.image, YELLOW, (start_x, start_y), (end_x, end_y), 2)
        
        # MASSIVE poop base - darker brown
        pygame.draw.ellipse(self.image, (101, 52, 13), (10, 30, 40, 22))
        
        # Middle layer - bigger
        pygame.draw.ellipse(self.image, BROWN, (12, 18, 36, 28))
        
        # Top swirl - bigger
        pygame.draw.ellipse(self.image, (160, 82, 45), (16, 8, 28, 24))
        pygame.draw.ellipse(self.image, (139, 69, 19), (20, 4, 20, 16))
        
        # Golden shine spots (super poop is special!)
        pygame.draw.circle(self.image, YELLOW, (25, 22), 3)
        pygame.draw.circle(self.image, YELLOW, (35, 28), 4)
        pygame.draw.circle(self.image, (255, 223, 0), (30, 32), 2)
        
        # Swirl tip with glow
        pygame.draw.circle(self.image, YELLOW, (30, 10), 6)
        pygame.draw.circle(self.image, (160, 82, 45), (30, 10), 4)
        
        # Add "SUPER!" text
        font = pygame.font.Font(None, 12)
        text = font.render("SUPER!", True, WHITE)
        text_rect = text.get_rect(center=(30, 50))
        self.image.blit(text, text_rect)
        
    def update(self):
        self.rect.x += self.speed
        
        # Animate super poop
        if self.is_super:
            self.frame += 1
            self.draw_super_poop()
        
        # Remove if off screen
        if self.rect.x > WINDOW_WIDTH:
            self.kill()

class BossMom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 100), pygame.SRCALPHA)
        self.original_image = None
        self.hit_timer = 0
        self.health = 30  # Boss has 30 health (3x more!)
        self.max_health = 30
        self.current_shout = ""
        self.shout_timer = 0
        
        self.draw_mom()
        
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH - 120
        self.rect.y = WINDOW_HEIGHT // 2 - 50
        self.speed_y = 3
        self.speed_x = 3
        self.direction_y = random.choice([-1, 1])
        self.direction_x = random.choice([-1, 1])
        self.attack_timer = 0
    
    def draw_mom(self, hit=False):
        """Draw the scary middle-aged mom boss"""
        self.image.fill((0, 0, 0, 0))
        
        color_mod = (255, 100, 100) if hit else (255, 220, 177)
        
        # Draw wild crazy hair (big and messy)
        for i in range(15):
            x = 25 + random.randint(-20, 20)
            y = 10 + random.randint(-5, 10)
            pygame.draw.line(self.image, (100, 50, 0), (40, 20), (x, y), 3)
        
        # Draw angry face (larger head)
        pygame.draw.circle(self.image, color_mod, (40, 30), 22)
        
        # Draw CRAZY angry eyes (wide open and scary)
        pygame.draw.circle(self.image, WHITE, (32, 27), 6)
        pygame.draw.circle(self.image, WHITE, (48, 27), 6)
        pygame.draw.circle(self.image, RED, (32, 27), 4)
        pygame.draw.circle(self.image, RED, (48, 27), 4)
        pygame.draw.circle(self.image, BLACK, (32, 27), 2)
        pygame.draw.circle(self.image, BLACK, (48, 27), 2)
        
        # Draw angry eyebrows (slanted down)
        pygame.draw.line(self.image, (80, 40, 0), (26, 20), (34, 24), 3)
        pygame.draw.line(self.image, (80, 40, 0), (46, 24), (54, 20), 3)
        
        # Draw scary wide open mouth with teeth
        pygame.draw.ellipse(self.image, BLACK, (30, 38, 20, 15))
        
        # Draw scary sharp teeth
        for i in range(5):
            x = 31 + i * 4
            pygame.draw.polygon(self.image, WHITE, [(x, 40), (x+2, 40), (x+1, 45)])
            pygame.draw.polygon(self.image, WHITE, [(x, 48), (x+2, 48), (x+1, 43)])
        
        # Draw body with apron
        pygame.draw.rect(self.image, (200, 50, 50), (22, 52, 36, 45))
        
        # Draw white apron
        pygame.draw.polygon(self.image, WHITE, [(30, 55), (50, 55), (52, 90), (28, 90)])
        
        # Draw apron strings
        pygame.draw.line(self.image, WHITE, (30, 55), (25, 60), 2)
        pygame.draw.line(self.image, WHITE, (50, 55), (55, 60), 2)
        
        # Draw rolling pin in hand (weapon!)
        pygame.draw.rect(self.image, (160, 120, 80), (8, 55, 15, 8))
        pygame.draw.circle(self.image, (100, 80, 60), (8, 59), 4)
        pygame.draw.circle(self.image, (100, 80, 60), (23, 59), 4)
        
        # Draw other arm
        pygame.draw.rect(self.image, color_mod, (57, 58, 10, 20))
        
        # Add "MAMMA" nameplate above head
        if not hit:
            font = pygame.font.Font(None, 18)
            text = font.render("MAMMA", True, BLACK)
            # White background for nameplate
            pygame.draw.rect(self.image, WHITE, (17, 0, 46, 11))
            self.image.blit(text, (19, 1))
        
        # Draw health bar above head
        bar_width = 60
        bar_height = 6
        health_width = int((self.health / self.max_health) * bar_width)
        
        # Background (red)
        pygame.draw.rect(self.image, RED, (10, 5, bar_width, bar_height))
        # Health (green)
        pygame.draw.rect(self.image, GREEN, (10, 5, health_width, bar_height))
        # Border
        pygame.draw.rect(self.image, BLACK, (10, 5, bar_width, bar_height), 1)
        
    def update(self):
        # Move up and down aggressively
        self.rect.y += self.speed_y * self.direction_y
        
        # Move left and right
        self.rect.x += self.speed_x * self.direction_x
        
        # Bounce off edges (boss can go anywhere on screen)
        if self.rect.y <= 0 or self.rect.y >= WINDOW_HEIGHT - self.rect.height - 50:
            self.direction_y *= -1
        
        if self.rect.x <= WINDOW_WIDTH // 3 or self.rect.x >= WINDOW_WIDTH - self.rect.width:
            self.direction_x *= -1
        
        # Boss changes direction more often (more erratic movement)
        if random.randint(0, 100) < 3:  # 3% chance each frame
            self.direction_x *= -1
        if random.randint(0, 100) < 3:
            self.direction_y *= -1
        
        # Handle hit flash effect
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.draw_mom(hit=False)
        
        # Update shout timer
        if self.shout_timer > 0:
            self.shout_timer -= 1
            if self.shout_timer == 0:
                self.current_shout = ""
        
        # Attack timer (for future attack patterns)
        self.attack_timer += 1
    
    def shout(self, text):
        """Make MAMMA shout something"""
        self.current_shout = text
        self.shout_timer = 120  # Show for 2 seconds at 60 FPS
    
    def hit(self):
        """Called when hit by projectile"""
        self.health -= 1
        self.hit_timer = 10
        self.draw_mom(hit=True)
        
        if self.health <= 0:
            return True  # Boss defeated
        return False

class BossProjectile(pygame.sprite.Sprite):
    """Projectiles thrown by MAMMA boss"""
    def __init__(self, x, y, projectile_type):
        super().__init__()
        self.projectile_type = projectile_type
        
        if projectile_type == "dish":
            # Draw dirty dishes with food stains - STACK OF PLATES
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Bottom plate (largest)
            pygame.draw.ellipse(self.image, WHITE, (2, 20, 36, 15))
            pygame.draw.ellipse(self.image, (240, 240, 240), (5, 22, 30, 11))
            # Middle plate
            pygame.draw.ellipse(self.image, WHITE, (6, 13, 28, 13))
            pygame.draw.ellipse(self.image, (235, 235, 235), (8, 15, 24, 9))
            # Top plate
            pygame.draw.ellipse(self.image, WHITE, (10, 6, 20, 11))
            pygame.draw.ellipse(self.image, (230, 230, 230), (12, 8, 16, 7))
            # Dirty food stains (brown/green/red)
            pygame.draw.circle(self.image, (139, 90, 43), (15, 25), 4)  # Brown food
            pygame.draw.circle(self.image, (100, 140, 80), (25, 23), 3)  # Green food
            pygame.draw.circle(self.image, (180, 60, 50), (18, 16), 3)  # Ketchup
            pygame.draw.circle(self.image, (200, 150, 0), (22, 18), 2)  # Mustard
            # Fork sticking out prominently
            pygame.draw.rect(self.image, (192, 192, 192), (32, 10, 3, 18), 0)
            # Fork prongs
            for i in range(4):
                pygame.draw.rect(self.image, (192, 192, 192), (30 + i*2, 10, 1, 6), 0)
            
        elif projectile_type == "vacuum":
            # Draw a vacuum cleaner with hose
            self.image = pygame.Surface((65, 55), pygame.SRCALPHA)
            
            # Main body (upright vacuum - tall and narrow, GREY)
            pygame.draw.rect(self.image, (140, 140, 140), (35, 10, 22, 35), 0)  # Grey body
            pygame.draw.rect(self.image, (100, 100, 100), (37, 12, 18, 31), 0)  # Darker center
            
            # Vacuum brand label
            pygame.draw.rect(self.image, (220, 220, 220), (38, 20, 16, 8), 0)
            
            # Handle at top
            pygame.draw.arc(self.image, (100, 100, 100), (32, 5, 28, 15), 3.14, 0, 4)
            
            # Vacuum head/nozzle at bottom (the part that sucks)
            pygame.draw.rect(self.image, (50, 50, 50), (30, 42, 32, 8), 0)
            pygame.draw.rect(self.image, BLACK, (32, 44, 28, 4), 0)  # Suction slot
            
            # Small wheels
            pygame.draw.circle(self.image, BLACK, (36, 50), 4, 0)
            pygame.draw.circle(self.image, BLACK, (56, 50), 4, 0)
            pygame.draw.circle(self.image, (80, 80, 80), (36, 50), 2, 0)
            pygame.draw.circle(self.image, (80, 80, 80), (56, 50), 2, 0)
            
            # Flexible hose coming from side (thick black tube)
            hose_points = [(35, 25), (30, 26), (25, 28), (20, 30), (15, 33), (10, 36), (5, 40)]
            for i in range(len(hose_points) - 1):
                pygame.draw.line(self.image, (60, 60, 60), hose_points[i], hose_points[i+1], 6)
            
            # Hose attachment/nozzle at end
            pygame.draw.circle(self.image, (80, 80, 80), (5, 40), 5, 0)
            pygame.draw.circle(self.image, (40, 40, 40), (5, 40), 3, 0)
            
            # Power cord wrapped around (brown/black cord)
            pygame.draw.line(self.image, (40, 40, 40), (40, 15), (38, 40), 2)
            
            # Power button (small green light)
            pygame.draw.circle(self.image, (0, 200, 0), (46, 18), 3, 0)
            
        else:  # mop
            # Draw a mop with bucket
            self.image = pygame.Surface((55, 60), pygame.SRCALPHA)
            
            # Bucket (gray metal with blue water)
            pygame.draw.polygon(self.image, (130, 130, 130), [(12, 35), (40, 35), (43, 52), (9, 52)], 0)
            # Bucket rim (shiny)
            pygame.draw.rect(self.image, (180, 180, 180), (9, 33, 34, 4), 0)
            
            # BRIGHT BLUE water inside (very visible)
            pygame.draw.polygon(self.image, (30, 120, 200), [(14, 37), (38, 37), (40, 50), (12, 50)], 0)
            
            # Bubbles/foam (white)
            pygame.draw.circle(self.image, WHITE, (20, 41), 4, 0)
            pygame.draw.circle(self.image, WHITE, (30, 43), 3, 0)
            pygame.draw.circle(self.image, WHITE, (25, 47), 3, 0)
            pygame.draw.circle(self.image, (200, 220, 255), (20, 41), 2, 0)
            pygame.draw.circle(self.image, (200, 220, 255), (30, 43), 1, 0)
            
            # Bucket handle (dark wire)
            pygame.draw.arc(self.image, (60, 60, 60), (16, 23, 22, 18), 3.14, 0, 5)
            
            # Mop handle (BROWN wooden pole - thick and visible)
            pygame.draw.rect(self.image, (120, 80, 40), (26, 0, 8, 40), 0)
            pygame.draw.ellipse(self.image, (100, 60, 20), (25, 0, 10, 12), 0)
            
            # Wood grain (darker lines)
            pygame.draw.line(self.image, (80, 50, 20), (28, 5), (28, 38), 2)
            pygame.draw.line(self.image, (80, 50, 20), (32, 8), (32, 35), 2)
            
            # Mop head (WHITE strings hanging on side - very visible)
            pygame.draw.ellipse(self.image, WHITE, (15, 33, 24, 14), 0)
            pygame.draw.ellipse(self.image, (230, 230, 230), (17, 35, 20, 10), 0)
            
            # Mop strings (thick wet strands)
            for i in range(10):
                string_x = 17 + i * 2.2
                length = 10 if i % 2 == 0 else 8
                pygame.draw.line(self.image, (220, 220, 220), (string_x, 42), (string_x - 1, 42 + length), 3)
                # Water drips (blue)
                if i % 2 == 0:
                    pygame.draw.circle(self.image, (50, 150, 220), (int(string_x - 1), 42 + length), 2, 0)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -6  # Move left towards Harry
        self.spin = 0
        
    def update(self):
        self.rect.x += self.speed
        
        # Spin effect
        self.spin += 10
        if self.spin >= 360:
            self.spin = 0
        
        # Remove if off screen
        if self.rect.x < -50:
            self.kill()

class FlyingCat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.flap_frame = 0
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        self.draw_cat()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.randint(-4, -2)
        self.speed_y = random.choice([-2, -1, 0, 1, 2])
        
    def draw_cat(self):
        """Draw a black cat with white spots"""
        self.image.fill((0, 0, 0, 0))
        
        # Draw cat body (black)
        pygame.draw.ellipse(self.image, BLACK, (15, 18, 22, 16))
        
        # Draw cat head (black)
        pygame.draw.circle(self.image, BLACK, (25, 15), 11)
        
        # Draw ears (pointy black)
        pygame.draw.polygon(self.image, BLACK, [(17, 7), (19, 15), (22, 10)])
        pygame.draw.polygon(self.image, BLACK, [(28, 10), (31, 15), (33, 7)])
        
        # Draw pink inner ears
        pygame.draw.polygon(self.image, (255, 192, 203), [(19, 10), (20, 14), (21, 11)])
        pygame.draw.polygon(self.image, (255, 192, 203), [(29, 11), (30, 14), (31, 10)])
        
        # Draw white spots on body
        pygame.draw.circle(self.image, WHITE, (20, 22), 3)
        pygame.draw.ellipse(self.image, WHITE, (28, 24, 6, 5))
        pygame.draw.circle(self.image, WHITE, (18, 28), 2)
        
        # Draw white spot on face
        pygame.draw.circle(self.image, WHITE, (23, 18), 2)
        
        # Draw eyes (green cat eyes)
        pygame.draw.circle(self.image, GREEN, (22, 14), 3)
        pygame.draw.circle(self.image, GREEN, (28, 14), 3)
        pygame.draw.ellipse(self.image, BLACK, (21, 13, 2, 4))
        pygame.draw.ellipse(self.image, BLACK, (27, 13, 2, 4))
        
        # Draw white whiskers
        pygame.draw.line(self.image, WHITE, (15, 16), (8, 14), 1)
        pygame.draw.line(self.image, WHITE, (15, 18), (8, 18), 1)
        pygame.draw.line(self.image, WHITE, (15, 20), (8, 22), 1)
        pygame.draw.line(self.image, WHITE, (35, 16), (42, 14), 1)
        pygame.draw.line(self.image, WHITE, (35, 18), (42, 18), 1)
        pygame.draw.line(self.image, WHITE, (35, 20), (42, 22), 1)
        
        # Draw black tail (curved)
        tail_points = [(30, 28), (33, 32), (35, 35), (34, 38)]
        for i in range(len(tail_points) - 1):
            pygame.draw.line(self.image, BLACK, tail_points[i], tail_points[i+1], 3)
        
        # White tip on tail
        pygame.draw.circle(self.image, WHITE, (34, 38), 2)
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom
        if self.rect.y <= 0 or self.rect.y >= WINDOW_HEIGHT - 100:
            self.speed_y *= -1
        
        # Remove if off screen (left side)
        if self.rect.x < -50:
            self.kill()

class BigBird(pygame.sprite.Sprite):
    """A big bird that flies across the top of the screen"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        self.wing_up = True
        self.draw_bird()
        
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + 50  # Start off-screen right
        self.rect.y = random.randint(50, 150)  # Fly at top of screen
        self.speed = -3  # Move left
        self.has_dropped = False
        
    def draw_bird(self):
        """Draw a big bird"""
        self.image.fill((0, 0, 0, 0))
        
        # Bird body (plump brown body)
        pygame.draw.ellipse(self.image, (139, 90, 43), (20, 20, 35, 25))
        
        # Bird head
        pygame.draw.circle(self.image, (139, 90, 43), (25, 23), 12)
        
        # Beak (yellow/orange)
        pygame.draw.polygon(self.image, (255, 165, 0), [(15, 23), (8, 21), (8, 25)])
        
        # Eyes (beady black eyes)
        pygame.draw.circle(self.image, BLACK, (20, 20), 3)
        pygame.draw.circle(self.image, WHITE, (19, 19), 1)  # Eye shine
        
        # Wings (flapping)
        if self.wing_up:
            # Wings up position
            pygame.draw.ellipse(self.image, (120, 80, 40), (15, 15, 20, 12))
            pygame.draw.ellipse(self.image, (120, 80, 40), (40, 15, 20, 12))
        else:
            # Wings down position
            pygame.draw.ellipse(self.image, (120, 80, 40), (15, 28, 20, 12))
            pygame.draw.ellipse(self.image, (120, 80, 40), (40, 28, 20, 12))
        
        # Tail feathers
        pygame.draw.polygon(self.image, (100, 70, 30), [(50, 30), (60, 28), (65, 32), (60, 36), (50, 35)])
        
        # Feet (small orange legs)
        pygame.draw.line(self.image, (255, 140, 0), (30, 43), (28, 48), 2)
        pygame.draw.line(self.image, (255, 140, 0), (40, 43), (42, 48), 2)
        
    def update(self):
        self.rect.x += self.speed
        
        # Flap wings animation
        if random.randint(0, 5) == 0:
            self.wing_up = not self.wing_up
            self.draw_bird()
        
        # Remove if off screen (left side)
        if self.rect.x < -100:
            self.kill()
    
    def should_drop_turd(self):
        """Check if bird should drop a turd (when in middle of screen)"""
        if not self.has_dropped and WINDOW_WIDTH // 3 < self.rect.x < 2 * WINDOW_WIDTH // 3:
            self.has_dropped = True
            return True
        return False

class BirdTurd(pygame.sprite.Sprite):
    """A large bird turd that falls slowly"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        self.draw_turd()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 2  # Falls slowly
        
    def draw_turd(self):
        """Draw a large bird turd (white with grey spots)"""
        # Main turd shape (white/grey splat)
        pygame.draw.ellipse(self.image, WHITE, (5, 5, 20, 30))
        pygame.draw.ellipse(self.image, (220, 220, 220), (8, 8, 14, 24))
        
        # Splat drops
        pygame.draw.circle(self.image, WHITE, (10, 35), 5)
        pygame.draw.circle(self.image, WHITE, (20, 35), 4)
        
        # Grey spots/texture
        pygame.draw.circle(self.image, (180, 180, 180), (12, 15), 3)
        pygame.draw.circle(self.image, (180, 180, 180), (18, 22), 2)
        pygame.draw.circle(self.image, (180, 180, 180), (14, 28), 2)
        
    def update(self):
        self.rect.y += self.speed_y
        
        # Remove if off screen (bottom)
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()

class PappaKiss(pygame.sprite.Sprite):
    """A kiss thrown by PAPPA that gives Harry extra lives"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.draw_kiss()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = -4  # Move left towards Harry
        self.float_offset = 0
        
    def draw_kiss(self):
        """Draw a pink heart kiss"""
        # Draw a heart shape (pink/red)
        heart_color = (255, 105, 180)  # Hot pink
        
        # Left half of heart
        pygame.draw.circle(self.image, heart_color, (10, 12), 8)
        # Right half of heart
        pygame.draw.circle(self.image, heart_color, (20, 12), 8)
        # Bottom point of heart
        pygame.draw.polygon(self.image, heart_color, [(5, 12), (25, 12), (15, 25)])
        
        # Add shine/highlight
        pygame.draw.circle(self.image, (255, 182, 193), (8, 9), 3)
        pygame.draw.circle(self.image, (255, 182, 193), (18, 9), 3)
        
        # Add small sparkles around it
        sparkle_color = (255, 255, 255)
        pygame.draw.line(self.image, sparkle_color, (2, 5), (4, 7), 1)
        pygame.draw.line(self.image, sparkle_color, (26, 5), (28, 7), 1)
        pygame.draw.line(self.image, sparkle_color, (15, 2), (15, 4), 1)
        
    def update(self):
        self.rect.x += self.speed_x
        
        # Float up and down gently
        self.float_offset += 0.1
        self.rect.y += int(2 * pygame.math.Vector2(0, 1).rotate(self.float_offset * 180 / 3.14).y)
        
        # Remove if off screen (left side)
        if self.rect.x < -50:
            self.kill()

class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a middle-aged dad character with beer belly
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        self.original_image = None
        self.hit_timer = 0
        self.kiss_timer = 0
        
        self.draw_dad()
        
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH - 100
        self.rect.y = WINDOW_HEIGHT // 2  # Start in middle height
        self.speed_y = 2
        self.speed_x = 2
        self.direction_y = random.choice([-1, 1])
        self.direction_x = random.choice([-1, 1])
    
    def draw_dad(self, hit=False):
        """Draw the middle-aged dad character"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        
        color_mod = (255, 100, 100) if hit else (255, 220, 177)
        
        # Draw receding hairline
        pygame.draw.ellipse(self.image, (100, 80, 60), (15, 8, 30, 15))
        
        # Draw bald spot on top
        pygame.draw.circle(self.image, (255, 220, 177), (30, 12), 8)
        
        # Draw bigger head (middle-aged)
        pygame.draw.circle(self.image, color_mod, (30, 25), 18)
        
        # Draw tired eyes with bags
        pygame.draw.circle(self.image, WHITE, (24, 23), 4)
        pygame.draw.circle(self.image, WHITE, (36, 23), 4)
        pygame.draw.circle(self.image, BLACK, (25, 24), 2)
        pygame.draw.circle(self.image, BLACK, (37, 24), 2)
        # Eye bags
        pygame.draw.arc(self.image, (150, 120, 100), (20, 26, 10, 6), 3.14, 0, 1)
        pygame.draw.arc(self.image, (150, 120, 100), (32, 26, 10, 6), 3.14, 0, 1)
        
        # Draw tired frown
        pygame.draw.arc(self.image, BLACK, (20, 32, 20, 10), 0, 3.14, 2)
        
        # Draw polo shirt
        pygame.draw.rect(self.image, (100, 150, 200), (15, 43, 30, 35))
        
        # Draw beer belly (round)
        pygame.draw.ellipse(self.image, (100, 150, 200), (12, 55, 36, 25))
        
        # Draw collar
        pygame.draw.polygon(self.image, (80, 120, 160), [(25, 43), (30, 50), (35, 43)])
        
        # Draw pocket with pen
        pygame.draw.rect(self.image, (80, 120, 160), (20, 50, 8, 10))
        pygame.draw.line(self.image, BLACK, (24, 50), (24, 56), 1)
        
        # Draw arms
        pygame.draw.rect(self.image, color_mod, (8, 48, 7, 20))
        pygame.draw.rect(self.image, color_mod, (45, 48, 7, 20))
        
        # Add "PAPPA" nameplate above head
        if not hit:
            font = pygame.font.Font(None, 16)
            text = font.render("PAPPA", True, BLACK)
            # White background for nameplate
            pygame.draw.rect(self.image, WHITE, (10, 0, 40, 10))
            self.image.blit(text, (12, 1))
        
    def update(self):
        # Move up and down
        self.rect.y += self.speed_y * self.direction_y
        
        # Move left and right
        self.rect.x += self.speed_x * self.direction_x
        
        # Bounce off edges
        if self.rect.y <= 0 or self.rect.y >= WINDOW_HEIGHT - self.rect.height - 50:
            self.direction_y *= -1
        
        if self.rect.x <= WINDOW_WIDTH // 2 or self.rect.x >= WINDOW_WIDTH - self.rect.width:
            self.direction_x *= -1
        
        # Randomly change direction occasionally
        if random.randint(0, 100) < 2:  # 2% chance each frame
            self.direction_x *= -1
        if random.randint(0, 100) < 2:
            self.direction_y *= -1
        
        # Handle hit flash effect
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.draw_dad(hit=False)
        
        # Increment kiss timer
        self.kiss_timer += 1
    
    def hit(self):
        """Called when hit by projectile"""
        self.hit_timer = 10  # Flash for 10 frames
        self.draw_dad(hit=True)
    
    def should_throw_kiss(self):
        """Check if PAPPA should throw a kiss (every 10 seconds)"""
        if self.kiss_timer >= 600:  # 10 seconds at 60 FPS
            self.kiss_timer = 0
            return True
        return False

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.boss_projectiles = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.bird_turds = pygame.sprite.Group()
        self.pappa_kisses = pygame.sprite.Group()
        
        self.player = Player()
        self.target = Target()
        self.boss = None
        
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.target)
        self.targets.add(self.target)
        
        self.score = 0
        self.hits = 0
        self.super_ready = False
        self.lives = 3
        self.cat_spawn_timer = 0
        self.boss_spawn_timer = 0
        self.boss_defeated_timer = 0
        self.boss_active = False
        self.boss_attack_timer = 0
        self.bird_spawn_timer = random.randint(900, 1800)  # 15-30 seconds at 60fps
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
    def shoot(self):
        # Check if super poop is ready
        if self.super_ready:
            projectile = Projectile(self.player.rect.right, self.player.rect.centery, is_super=True)
            self.super_ready = False
            self.hits = 0
            print("🌟💩 SUPER POOP ACTIVATED! 💩🌟")
        else:
            projectile = Projectile(self.player.rect.right, self.player.rect.centery, is_super=False)
        
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)
        
    def spawn_cat(self):
        """Spawn a flying cat from the right side"""
        y = random.randint(50, WINDOW_HEIGHT - 150)
        cat = FlyingCat(WINDOW_WIDTH, y)
        self.all_sprites.add(cat)
        self.cats.add(cat)
    
    def spawn_bird(self):
        """Spawn a big bird from the right side"""
        bird = BigBird()
        self.all_sprites.add(bird)
        self.birds.add(bird)
        print("🦅 BIG BIRD INCOMING! Watch out for falling turds! 🦅")
    
    def spawn_bird_turd(self, x, y):
        """Spawn a bird turd falling from the bird"""
        turd = BirdTurd(x, y)
        self.all_sprites.add(turd)
        self.bird_turds.add(turd)
        print("💩 BIRD TURD INCOMING! DODGE IT! 💩")
    
    def spawn_pappa_kiss(self):
        """Spawn a kiss from PAPPA that gives extra life"""
        kiss = PappaKiss(self.target.rect.x, self.target.rect.centery)
        self.all_sprites.add(kiss)
        self.pappa_kisses.add(kiss)
        print("💕 PAPPA sends a KISS! Catch it for an extra life! 💕")
    
    def spawn_boss(self):
        """Spawn the scary mom boss"""
        if not self.boss_active:
            self.boss = BossMom()
            self.all_sprites.add(self.boss)
            self.boss_group.add(self.boss)
            self.boss_active = True
            self.boss_attack_timer = 0
            # Hide regular dad during boss fight
            self.target.rect.x = -200
            print("👹 BOSS FIGHT! SCARY MAMMA HAS APPEARED! 👹")
    
    def boss_throw_projectile(self):
        """MAMMA throws dishes, vacuum, or mop"""
        if self.boss and self.boss_active:
            projectile_types = ["dish", "vacuum", "mop"]
            proj_type = random.choice(projectile_types)
            projectile = BossProjectile(self.boss.rect.x, self.boss.rect.centery, proj_type)
            self.all_sprites.add(projectile)
            self.boss_projectiles.add(projectile)
            
            # MAMMA shouts Swedish mom phrases!
            mom_phrases = [
                "Nu ska du gå och lägga dig!",
                "Har du slut skärmtid,\nså har du slut skärmtid!",
                "Nej, det är inte godisdag!"
            ]
            phrase = random.choice(mom_phrases)
            
            # Make MAMMA shout on screen
            self.boss.shout(phrase)
            
            # Print message with her shout
            if proj_type == "dish":
                print(f"🍽️ MAMMA throws DISHES and shouts: '{phrase}'")
            elif proj_type == "vacuum":
                print(f"🧹 MAMMA throws VACUUM CLEANER and shouts: '{phrase}'")
            else:
                print(f"🧽 MAMMA throws MOP and shouts: '{phrase}'")
    
    def check_collisions(self):
        # Check if projectiles hit boss
        if self.boss_active:
            boss_hits = pygame.sprite.groupcollide(self.projectiles, self.boss_group, True, False)
            if boss_hits:
                for projectile in boss_hits.keys():
                    if self.boss.hit():
                        # Boss defeated!
                        self.score += 100
                        self.boss_active = False
                        self.boss_defeated_timer = 0
                        self.target.rect.x = WINDOW_WIDTH - 100  # Bring back dad
                        print("🎉 BOSS DEFEATED! MAMMA IS GONE! +100 points! 🎉")
                        self.boss.kill()
                    else:
                        self.score += 10
                        print(f"💥 HIT MAMMA! Health: {self.boss.health}/{self.boss.max_health}")
        
        # Check if projectiles hit target (regular dad)
        if not self.boss_active:
            hits = pygame.sprite.groupcollide(self.projectiles, self.targets, True, False)
            if hits:
                # Check if it was a super poop hit
                for projectile in hits.keys():
                    if projectile.is_super:
                        self.score += 50  # Super poop worth more!
                        print("💥 SUPER POOP HIT! +50 points! 💥")
                    else:
                        self.score += 10
                        self.hits += 1
                        
                        # Check if super poop is ready
                        if self.hits >= 5:
                            self.super_ready = True
                            print("⚡ SUPER POOP READY! Next shot will be EPIC! ⚡")
                
                self.target.hit()  # Trigger hit effect
        
        # Check if player hits a cat (lose life!)
        cat_hits = pygame.sprite.spritecollide(self.player, self.cats, True)
        if cat_hits:
            self.lives -= 1
            print(f"😿 HIT BY CAT! Lives remaining: {self.lives}")
            if self.lives <= 0:
                self.game_over = True
                print("💀 GAME OVER! 💀")
        
        # Check if projectiles hit cats (destroy the cats!)
        cat_projectile_hits = pygame.sprite.groupcollide(self.projectiles, self.cats, True, True)
        if cat_projectile_hits:
            self.score += 5
            print("🎯 Cat destroyed! +5 points")
        
        # Check if boss projectiles hit player
        if self.boss_active:
            boss_proj_hits = pygame.sprite.spritecollide(self.player, self.boss_projectiles, True)
            if boss_proj_hits:
                self.lives -= 1
                print(f"💥 HIT BY MAMMA'S ATTACK! Lives remaining: {self.lives}")
                if self.lives <= 0:
                    self.game_over = True
                    print("💀 GAME OVER! 💀")
        
        # Check if bird turds hit player (lose life!)
        turd_hits = pygame.sprite.spritecollide(self.player, self.bird_turds, True)
        if turd_hits:
            self.lives -= 1
            print(f"💩 HIT BY BIRD TURD! Lives remaining: {self.lives}")
            if self.lives <= 0:
                self.game_over = True
                print("💀 GAME OVER! 💀")
        
        # Check if player catches PAPPA's kiss (gain life!)
        kiss_hits = pygame.sprite.spritecollide(self.player, self.pappa_kisses, True)
        if kiss_hits:
            self.lives += 1
            print(f"💕 CAUGHT PAPPA'S KISS! +1 life! Lives: {self.lives}")
            
    def draw(self):
        # Change background color during boss fight
        if self.boss_active:
            # Dark red/purple scary background
            screen.fill((100, 50, 80))
        else:
            # Normal sky blue background
            screen.fill((135, 206, 235))
        
        # Draw ground
        pygame.draw.rect(screen, (34, 139, 34), (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        
        # Draw all sprites
        self.all_sprites.draw(screen)
        
        # Draw MAMMA's speech bubble if she's shouting
        if self.boss_active and self.boss and self.boss.current_shout:
            # Draw speech bubble
            bubble_font = pygame.font.Font(None, 20)
            lines = self.boss.current_shout.split('\n')
            max_width = max([bubble_font.size(line)[0] for line in lines])
            line_height = bubble_font.get_height()
            bubble_width = max_width + 20
            bubble_height = (line_height * len(lines)) + 20
            
            # Position above MAMMA
            bubble_x = self.boss.rect.x + self.boss.rect.width // 2 - bubble_width // 2
            bubble_y = self.boss.rect.y - bubble_height - 20
            
            # Make sure bubble stays on screen
            if bubble_x < 10:
                bubble_x = 10
            if bubble_x + bubble_width > WINDOW_WIDTH - 10:
                bubble_x = WINDOW_WIDTH - bubble_width - 10
            if bubble_y < 10:
                bubble_y = 10
            
            # Draw white bubble with black border
            pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), 0, 10)
            pygame.draw.rect(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 3, 10)
            
            # Draw speech bubble tail (triangle pointing to MAMMA)
            tail_points = [
                (bubble_x + bubble_width // 2 - 10, bubble_y + bubble_height),
                (bubble_x + bubble_width // 2 + 10, bubble_y + bubble_height),
                (self.boss.rect.x + self.boss.rect.width // 2, self.boss.rect.y)
            ]
            pygame.draw.polygon(screen, WHITE, tail_points, 0)
            pygame.draw.polygon(screen, BLACK, tail_points, 3)
            
            # Draw text inside bubble
            y_offset = bubble_y + 10
            for line in lines:
                text_surface = bubble_font.render(line, True, BLACK)
                text_x = bubble_x + (bubble_width - text_surface.get_width()) // 2
                screen.blit(text_surface, (text_x, y_offset))
                y_offset += line_height
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_font = pygame.font.Font(None, 32)
        lives_color = RED if self.lives == 1 else BLACK
        lives_text = lives_font.render(f"Lives: {'❤️' * self.lives}", True, lives_color)
        screen.blit(lives_text, (WINDOW_WIDTH - 150, 10))
        
        # Draw boss warning or hit counter
        hit_font = pygame.font.Font(None, 28)
        if self.boss_active:
            # Boss fight warning
            boss_font = pygame.font.Font(None, 36)
            flash_colors = [RED, (255, 100, 0), YELLOW]
            color = flash_colors[(pygame.time.get_ticks() // 200) % len(flash_colors)]
            boss_text = boss_font.render("⚠️ BOSS FIGHT! ⚠️", True, color)
            screen.blit(boss_text, (WINDOW_WIDTH // 2 - 120, 50))
        elif self.super_ready:
            # Flash the super ready message
            flash_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
            color = flash_colors[(pygame.time.get_ticks() // 100) % len(flash_colors)]
            super_text = hit_font.render("⚡ SUPER POOP READY! ⚡", True, color)
            screen.blit(super_text, (10, 50))
        else:
            hits_text = hit_font.render(f"Hits: {self.hits}/5", True, BLACK)
            screen.blit(hits_text, (10, 50))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            screen.blit(game_over_text, game_over_rect)
            
            final_score_font = pygame.font.Font(None, 48)
            final_score_text = final_score_font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(final_score_text, final_score_rect)
            
            restart_font = pygame.font.Font(None, 32)
            restart_text = restart_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)
        else:
            # Draw instructions
            inst_font = pygame.font.Font(None, 24)
            inst_text = inst_font.render("Arrow Keys: Move | SPACE: Shoot | ESC: Quit", True, BLACK)
            screen.blit(inst_text, (WINDOW_WIDTH // 2 - 200, 10))
        
        pygame.display.flip()
        
    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.check_collisions()
            
            # Spawn cats periodically (not during boss fight)
            if not self.boss_active:
                self.cat_spawn_timer += 1
                if self.cat_spawn_timer >= 90:  # Spawn every 1.5 seconds (at 60 FPS)
                    self.spawn_cat()
                    self.cat_spawn_timer = 0
            
            # Spawn big bird periodically
            self.bird_spawn_timer += 1
            if self.bird_spawn_timer >= random.randint(900, 1800):  # 15-30 seconds
                self.spawn_bird()
                self.bird_spawn_timer = 0
            
            # Check if any bird should drop a turd
            for bird in self.birds:
                if bird.should_drop_turd():
                    self.spawn_bird_turd(bird.rect.centerx, bird.rect.bottom)
            
            # Check if PAPPA should throw a kiss (not during boss fight)
            if not self.boss_active and self.target.should_throw_kiss():
                self.spawn_pappa_kiss()
            
            # Boss spawn logic
            if not self.boss_active:
                self.boss_spawn_timer += 1
                # Spawn boss every 20 seconds (1200 frames at 60 FPS)
                if self.boss_spawn_timer >= 1200:
                    self.spawn_boss()
                    self.boss_spawn_timer = 0
            else:
                # Boss attacks during boss fight
                self.boss_attack_timer += 1
                if self.boss_attack_timer >= 80:  # Attack every ~1.3 seconds
                    self.boss_throw_projectile()
                    self.boss_attack_timer = 0
                
                # After boss is defeated, wait before allowing next boss
                if self.boss_defeated_timer >= 0:
                    self.boss_defeated_timer += 1
                    if self.boss_defeated_timer >= 600:  # 10 seconds cooldown
                        self.boss_defeated_timer = -1
    
    def restart(self):
        """Restart the game"""
        self.__init__()

def main():
    game = Game()
    running = True
    
    print("🎮 Harrycane Game Started!")
    print("Controls: Arrow Keys to move, SPACE to shoot, ESC to quit")
    print("⚠️ AVOID THE FLYING CATS! ⚠️")
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not game.game_over:
                    game.shoot()
                elif event.key == pygame.K_r and game.game_over:
                    game.restart()
                    print("🔄 Game Restarted!")
        
        game.update()
        game.draw()
    
    print(f"🎯 Final Score: {game.score}")
    print("Thanks for playing Harrycane!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
