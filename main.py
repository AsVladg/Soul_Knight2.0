import pygame
import os
import sys
from pygame.locals import *
from pygame.sprite import Sprite, Group

pygame.init()
win_width, win_height = 1500, 750
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Soul Knight")

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 40)
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.original_image = None
        try:
            if player_image and os.path.exists(player_image):
                self.original_image = pygame.image.load(player_image).convert_alpha()
                self.image = pygame.transform.scale(self.original_image, (65, 65))
            else:
                raise FileNotFoundError
        except:
            self.image = pygame.Surface((65, 65))
            self.image.fill((255, 0, 0))
            font = pygame.font.SysFont(None, 20)
            text = font.render("No Image", True, (255, 255, 255))
            self.image.blit(text, (5, 25))
        
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.buff_active = False
        self.walls = Group()

    def collide_with_walls(self):
        return pygame.sprite.spritecollideany(self, self.walls)

    def update(self):
        keys = pygame.key.get_pressed()
        old_pos = self.rect.copy()
        
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
            
        self.rect.x = max(0, min(self.rect.x, win_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, win_height - self.rect.height))
        
        if self.collide_with_walls():
            self.rect = old_pos

def load_background(menu=False):
    try:
        if menu:
            bg_path = "soulknightглавфон.png"  
        else:
            bg_path = "Soulknight bg.png"  
            
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            return pygame.transform.scale(img, (win_width, win_height))
    except:
        pass
    
    bg = pygame.Surface((win_width, win_height))
    if menu:
        bg.fill((100, 100, 200))
    else:
        bg.fill((50, 50, 50))  
    return bg

def main_menu():
    menu_bg = load_background(menu=True)
    play_button = Button(win_width//2 - 150, win_height//2 - 50, 300, 80, "Играть", (100, 255, 100), (150, 255, 150))
    exit_button = Button(win_width//2 - 150, win_height//2 + 50, 300, 80, "Выход", (255, 100, 100), (255, 150, 150))
    
    title_font = pygame.font.SysFont('Arial', 80)
    title_text = title_font.render("Soul Knight", True, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if play_button.is_clicked(pygame.mouse.get_pos(), event):
                return True  
            if exit_button.is_clicked(pygame.mouse.get_pos(), event):
                pygame.quit()
                sys.exit()
        
        screen.blit(menu_bg, (0, 0))
        screen.blit(title_text, (win_width//2 - title_text.get_width()//2, 100))
        play_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.update()
        clock.tick(60)

def game_loop():
    background = load_background()
    player = Player("Темный рыцарь без фона.png", 5, 80, 3)
    all_sprites = Group()
    all_sprites.add(player)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  
                sys.exit()    
        
        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)
    
if __name__ == "__main__":
    while True:
        if main_menu(): 
            game_loop() 