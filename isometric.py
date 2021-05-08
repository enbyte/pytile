from pytile import *
import pygame

pygame.init()

imgld = ImageLoader()

isom_grass = imgld.LoadImage("images/isometric-grass.png")

running = True

air = NullTile()
grass = Tile(1, isom_grass, 1, 32, name="grass") 
tmap = IsometricTilemap("test", 'isometric-level', [air, grass], 32, C_MAT_PROVIDE_TYPE='file')

screen = pygame.display.set_mode((320, 22 * 10), flags=pygame.SCALED)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    tmap.draw(screen, yamount=11)       
    pygame.display.update()
            
pygame.quit()