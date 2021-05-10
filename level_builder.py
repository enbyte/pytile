import os
import pygame
from pytile import *
import time
import numpy


pygame.init()


LAVA_IMAGE = './images/lava.png'
DIRT_IMAGE = './images/dirt_0.png'
WATER_IMAGE = './images/water_0.png'
GRASS_IMAGE = './images/grass_0.png'

loader = ImageLoader()


p = time.time()

loaded_lava, loaded_dirt, loaded_water, loaded_grass = loader.LoadImages([LAVA_IMAGE, DIRT_IMAGE, WATER_IMAGE, GRASS_IMAGE])

lava = Tile(loaded_lava, name="Lava")
dirt = Tile(loaded_dirt, name="Dirt")
water = Tile(loaded_water, name="Water")
grass = Tile(loaded_grass, name="Grass")

air = NullTile()

width = int(input("Width? "))
height = 15

tmap = Tilemap('main', numpy.zeros([width, height]), [air, grass, dirt, water, lava], 32)

selected = 1
x = 0

running = True

screen = pygame.display.set_mode((480, 480), flags=pygame.SCALED)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_0]:
        selected = 0
    elif keys[pygame.K_1]:
        selected =  1
    elif keys[pygame.K_2]:
        selected = 2
        
    elif keys[pygame.K_3]:
        selected =  3
        
    if keys[pygame.K_LEFT]:
        tmap.x -= 3
        
    if keys[pygame.K_RIGHT]:
        tmap.x += 3
        
    if keys[pygame.K_q]:
        running = False
        
    if keys[pygame.K_c]:
        tmap.mat = numpy.zeros([width, height])
    
    if tmap.x > 0:
        tmap.x = 0
    mouse = pygame.mouse.get_pressed()[0]
    
    if mouse:
        
        tiles = tmap.getCollidingMouseTiles()
        if selected == 1 and tiles[0] < 14: #grass
            #fill out bottom
            for i in range(15 - tiles[0]):
                print(i)
                tmap.mat[i + tiles[0]][tiles[1]] = 2 #set to dirt
                
        tmap.mat[tiles[0]][tiles[1]] = selected
        
    screen.fill((255, 255, 255))
    tmap.draw(screen)
    
    pygame.display.update()


pygame.quit()