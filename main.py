import pygame
import random
import os
import math
import time
import datetime
from lunardate import LunarDate
WIDTH = 1370
HEIGHT = 767
FPS = 250
img_path = os.path.join(os.path.dirname(__file__), "img")
audio_path = os.path.join(os.path.dirname(__file__), "audio")
def randv():    
    v = random.random() * 22
    while (v < 15):
        v = random.random() * 22
    return v

def rand_color():   
    color_list = [(244, 214, 215), (55, 20, 88), (151, 68, 114), (230, 190, 146), (244, 252, 255), (230, 197, 246), (181, 180, 222), (191, 85, 177), (255, 199, 209), (200, 50, 66), (223, 219, 216), (158, 167, 164), (173, 254, 255), (185, 219, 149), (72, 141, 235), (252, 117, 249), (232, 169, 180), (155, 157, 170), (182, 98, 130), (248, 215, 20), (136, 214, 253), (221, 0, 27), (255, 105, 180)]
    return color_list[random.randint(0, len(color_list) - 1)]


def add_fireworks(list):  
    if (random.random() < 3 / 10):
        list.append(Fireworks())

class Item(pygame.sprite.Sprite):  
    def __init__(self, vy, x, color, shape, speed_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.shape = shape
        if color == (-1, -1, -1): 
            color = rand_color()
        self.color = color
        self.radius = randv() / 8  
        pygame.draw.circle(self.image, self.color, (8, 8), self.radius) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, HEIGHT - 10) 
        self.vx = 0
        self.vy = vy*speed_factor
        self.is_explode = False 
        self.count = 0

    def update(self, radius):
        self.move()
        if self.rect.y > HEIGHT - 20 and self.is_explode:
            self.kill()
        if self.vy < 1 and not self.is_explode:
            self.explode(radius)
        if self.is_explode: 
            self.count += 1
            if self.count > 55:
                self.kill()

    def move(self): 
        t = 1 / 60
        g = 9.8
        self.rect.x += self.vx * t * 25
        self.rect.y -= (2 * self.vy - g * t) * t / 2 * 25
        self.vy = self.vy - g * t

    def explode(self, radius):  
        self.is_explode = True
        angle = random.randint(0, 359) * math.pi / 180
        if self.shape == 'circle':
            self.vx += math.cos(angle) * radius
            self.vy -= math.sin(angle) * radius
        elif self.shape == 'star':
            star_factor = math.sin(5 * angle)
            self.vx += star_factor * math.cos(angle) * radius
            self.vy -= star_factor * math.sin(angle) * radius


class Fireworks():  
    def __init__(self):
        self.list = pygame.sprite.Group()
        self.vy = randv()
        self.x = WIDTH * random.random()
        self.num = random.randint(30, 40) 
        color = rand_color()
        if random.randint(1, 2) == 1:   
            color = (-1, -1, -1)
        shape = random.choice(['circle']) 
        self.list.add(Item(self.vy, self.x, color, shape, speed_factor) for i in range(self.num))
        self.start_time = time.time()  

    def draw(self, screen):
        self.list.draw(screen)

    def update(self):   
        radius = random.random() * 10
        while (radius < 8):
            radius = random.random() * 10
        self.list.update(radius)
        if (time.time() - self.start_time > 5):
            return True
        else:
            return False
def get_new_year_countdown():
    now = datetime.datetime.now()
    lunar_now = LunarDate.fromSolarDate(now.year, now.month, now.day)
    lunar_new_year = LunarDate(lunar_now.year + 1, 1, 1)
    new_year_date = lunar_new_year.toSolarDate()
    new_year = datetime.datetime(new_year_date.year, new_year_date.month, new_year_date.day)  
    countdown = new_year - now
    return countdown


def main():
    pygame.init()
    pygame.mixer.init()
    global speed_factor
    speed_factor = 1.17
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  
    pygame.display.set_caption("NEW YEAR")
    pygame.display.set_icon(pygame.image.load(os.path.join((img_path), "vi.png")).convert()) 
    bgm = pygame.mixer.music.load(os.path.join(audio_path, "TetOnRoi.mp3"))  
    pygame.mixer.music.play(-1) 
    clock = pygame.time.Clock()

    fireworks_list = [Fireworks() for i in range(5)]    
    running = True  
    count = 2
    while running:  
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if count == 2:
            screen.blit(pygame.image.load(os.path.join(img_path, "background.png")), (0, 0)) 
            count = 0
        count += 1
        add_fireworks(fireworks_list)
        dels = []   
        for index, item in enumerate(fireworks_list):
            if item.update():
                dels.append(index)
            item.draw(screen)
        #countdown = get_new_year_countdown()
        #countdown_text = f"Countdown: {countdown.days}d {countdown.seconds // 3600}h {(countdown.seconds // 60) % 60}m {countdown.seconds % 60}s"
        #font = pygame.font.Font('Erase Old Year.ttf', 44)
        #text = font.render(countdown_text, 1, (255, 0,0))
        #screen.blit(text, (380,615))

        pygame.display.flip()
        for i in dels:  
            del fireworks_list[i]

    pygame.QUIT
    exit()
if __name__ == "__main__":
    main()

