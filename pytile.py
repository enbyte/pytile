import numpy
import pytile_tools as tools
from pprint import pprint as pprint
import pygame
import sys
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import mask_col
import time
import copy


Tk().withdraw() #So there is no tkinter GUI other than the filedialog, only the pygame one


__verbose__ = False
Flase = False #mhm I'm lazy
global inited
inited = False
path = './images/'
pygame.init()

if '--verbose' in sys.argv or '-v' in sys.argv:
    __verbose__ = True

if '--no-player' in sys.argv:
    __player__ = False
else:
    __player__ = True
SETTINGS = {
      "col_mat":"draw"
    }
    
class SpecialNotContainedByTilemapError(Exception): pass
class SpecialDoesNotIntersectTilemapError(Exception): pass
class PointDoesNotIntersectTilemapError(Exception): pass


def getOnGround():
    bot = player.getCollidingTilesForSide(t, 4)
    top = player.getCollidingTilesForSide(t, 1)
    return (((1 in bot) or (2 in bot)) and (0 in bot)) and (0 in top)

def getInWall():
    sides = union(player.getCollidingTilesForSide(t, 2), player.getCollidingTilesForSide(t, 3))
    for item in sides:
        if not item == 0:
            return True
    return False
    

def text(font, message, color):
    return font.render(text, True, color)

def message():
    print("PyTile 1.2.2 (5fd3a:29fa)")

def union(lst1, lst2):
    f = set(lst1) | set(lst2)
    return f

def getOffsetFromRef(pixels_off, ref, BLOCK_SIZE):
    return abs(pixels_off - ref) % BLOCK_SIZE

def xblit(pos, display, image): #just minor efficiency checks, not sure if pygame.blit() has this
    image_size = image.get_rect()
    if pos[0] + image_size[0] < 0 and pos[1] + image_size[1] < 0:
        pass
    else:
        display.blit(image, pos)
    
def display(width, height):
    return pygame.display.set_mode((width, height))

def init():
    global creg, inited
    creg = CollisionsRegistry()
    inited = True
    

class ImageLoader():
    def __init__(self,name="ImageLoader"):
        self.name = name
    def LoadImages(self, list_):
        p = list_[:] #immutable copy
        r = []
        for x in p:
            try:
                r.append(pygame.image.load(x))
            except Exception: #e.g, FileNotFoundError, etc...
                r.append(False)
        return r
    def LoadImage(self, image): #odd, it isn't even using "self" but still needs it as an argument... oh well
        return pygame.image.load(image)
    


#ImageLoader works (as of 7 June 2020)!
'''
ImgLoader todo:
1) Load spritesheet

'''


class CollisionsRegistry():
    def __init__(self):
        self.triggers = []
        self.tilemaps = []
        self.specialtiles = []
        self.tiles = []
        self.inited = True
    def register(self, obj):
        if type(obj) == Tile:
            self.tiles.append(obj)
            if __verbose__:
                print('Tile %s registered' % obj.name)
        elif type(obj) == SpecialTile:
            self.specialtiles.append(obj)
            if __verbose__:
                print('SpecialTile %s registered' % obj.name)
        elif type(obj) == Tilemap:
            self.tilemaps.append(obj)
            if __verbose__:
                print("Tilemap %s registered" % obj.name)
    def addUnsidedSpecialCollision(self, sp1, sp2, func):
        self.triggers.append(['sp_sp', None,  sp1, sp2, func])
    def addSidedSpecialTilemapCollision(self, sp, tmap, sides, tile, func):
        self.triggers.append(['sp_lv', sides, sp, tmap, tile, func])
    def checkCollisions(self): #finished: unsided sp_sp, todo: sided sp_sp, unsided sp_tmap, sided sp_tmap
        for trig in self.triggers: #here begins the if loops
            if trig[0] == 'sp_sp': #special-special
                if trig[1] == None: #unsided collision
                    if trig[2].getCollideWithSpecial(trig[3]):
                        trig[4]()
            elif trig[0] == 'sp_lv':
                if not trig[0] == None: #sided collision
                    sides = trig[1]
                    sp = trig[2]
                    tmap = trig[3]
                    tiles = trig[4]
                    func = trig[5]
                    for side in sides:
                        col = sp.getCollidingTilesForSide(tmap, side)
                        for tilex in col:
                            if tmap.tiles[tilex] in tiles:
                                func()
                elif trig[0] == None:
                    if sp.isTmapCollide(tmap):
                        func()
        
class Tile():
    def __init__(self, image, name="Undefined Tile",):
        self.name = name
        self.image = image
        creg.register(self)
    def __get__(self): #testing...
        print("Tile call to %s (ID number %s) in __get__" % self.name, self.idnum)
        return self.image
    def __repr__(self): #testing... 
        return ("Tile call to %s (ID number %s) in __repr__" % (self.name, self.idnum))
    def draw(self,surface,x,y, row=None, col=None):
        xblit((x,y), surface, self.image)
    

class SpecialTile(Tile):
    def __init__(self, solid, image, idnum, x, y, blocksize, name="Undefined Special Tile"):
            self.solid = solid
            self.image = image
            self.idnum = idnum
            self.x = x
            self.y = y
            self.size = blocksize
    def getCollideWithSpecial(self, spec):
            if self.x + self.size < spec.x or self.x > spec.x + spec.size: return False
            if self.y + self.size < spec.y or self.y > spec.y + spec.size: return False
            return True
    def isTmapCollide(self, tmap):
        l = tmap
        if self.x + self.size < l.x or self.x > l.x + (l.BLOCK_SIZE * len(l.mat[0])):
            return False
        if self.y + self.size < l.y or self.y > l.y + (l.BLOCK_SIZE * len(l.mat)):
            return False
        return True
    def draw(self, surface):
        xblit((self.x, self.y), surface, self.image)
    def getCollidingTilesForSide(self, tmap, side):
        assert side > 0 and side <= 5
        assert type(tmap) == Tilemap
        if not self.isTmapCollide(tmap):
            return []
        
        '''
            _1
         2 |_| 3 inside = 5
            4
        '''
        
        
        if side == 1 or side == 4:
            if side == 1:
                s_x = self.x
                s_y = self.y
            elif side == 4:
                s_x = self.x
                s_y = self.y + self.size
                
            lpoint = tmap.getTilePoint(s_x, s_y)
            rpoint = tmap.getTilePoint(s_x + self.size, s_y)
            firstrow = lpoint[1]
            lastrow = rpoint[1]
            firstcol = lpoint[0]
            lastcol = rpoint[0]
            try:
                slc1 = tools.subsection(tmap.mat, firstrow, lastrow, firstcol, lastcol)[0]
            except IndexError:
                slc1 = []
        
        if side == 2 or side == 3:
            if side == 2:
                s_x = self.x
                s_y = self.y
            elif side == 3:
                s_x = self.x + self.size
                s_y = self.y
                
            top_point = tmap.getTilePoint(s_x, s_y)
            bot_point = tmap.getTilePoint(s_x, s_y + self.size)
            firstrow = top_point[1]
            lastrow = bot_point[1]
            firstcol = top_point[0]
            lastcol = bot_point[0]
            slc = tools.subsection(tmap.mat, firstrow, lastrow, firstcol, lastcol)
            slc1 = tools.matToList(slc)
        tiles = []
        for tile in slc1:
            if not tile in tiles:
                tiles.append(tile)
                
        return slc1
imgld = ImageLoader(name="imgloader0")
class NullTile(Tile):
    def draw(self, a, b, c):
        pass
    def __init__(self):
        self.image = pygame.Surface((0,0))
#print(coin)
#print(myMatrix)

class TileData:
    def __init__(self, tmap, row, col):
        self.tmap = tmap
        self.row = row
        self.col = col
        self.tilenumber = tmap.mat[row][col]
        self.tile = tmap.associated_tiles[self.tilenumber]


class Tilemap():
    def __init__(self, name, matrix, associated_tiles, BLOCK_SIZE, C_MAT_PROVIDE_TYPE='mat', C_TILE_FUNC_DICT={}):
        self.name = name
        self.tiles = associated_tiles
        self.x = 0
        self.y = 0
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.BLOCK_SIZE = BLOCK_SIZE
        self.B_S = BLOCK_SIZE
        if C_MAT_PROVIDE_TYPE == 'mat':
            self.mat = matrix
            self.drawmat = matrix
        else:
            self.mat = tools.load_tmap_mat(matrix, self)
            self.drawmat = self.mat
        self._tdict = C_TILE_FUNC_DICT
    def getIfPointContained(x, y):
        if x < self.x or x > (self.width * self.B_S): return False
        if y < self.y or y > (self.height * self.B_S): return False
        return True
    def draw(self, surface):
        mat = self.mat
        hreps = 0
        lreps = 0
        dk = self._tdict.keys()
        for row in mat:
            for item in row:
                #print(d[hreps])
                #print(d[lreps])
                tile_num = mat[hreps][lreps]
                
                #print(v)
                if tile_num or tile_num == 0:
                    tile_num = int(tile_num)   
                    tile = self.tiles[tile_num]
                    if tile_num in dk:
                        tile = self._tdict[tile_num](tile, lreps, hreps)
                    tile_img_height = tile.image.get_rect().height
                    attempt_x = (self.BLOCK_SIZE * lreps) + self.x
                    attempt_y = (self.BLOCK_SIZE * hreps) + self.y
                    true_x = attempt_x
                    true_y = attempt_y - (tile_img_height - self.BLOCK_SIZE)
                    tile.draw(surface, true_x, true_y)
                lreps += 1
            hreps += 1
            lreps = 0
    def getTilePoint(self, x, y):
        if x < self.x or x > self.x + (self.BLOCK_SIZE * len(self.mat[0])):
            raise PointDoesNotIntersectTilemapError
        elif y < self.y or y > self.y + (self.BLOCK_SIZE * len(self.mat)):
            raise PointDoesNotIntersectTilemapError
        mX = x
        mY = y
        #print('MX: %s MY: %s' % (mX, mY))
        xdist = abs(self.x - mX)
        ydist = abs(self.y - mY)
        #print('Xdist: %s Ydist: %s' % (xdist, ydist))
        xind = math.trunc(xdist / self.BLOCK_SIZE)
        yind = math.trunc(ydist / self.BLOCK_SIZE)
        #print('Xind: %s Yind: %s' % (xind, yind))
        return [yind, xind]
    def getCollidingMouseTiles(self):
        m_pos = pygame.mouse.get_pos()
        return self.getTilePoint(m_pos[0], m_pos[1])
    #t = mat.subsection(mat.Matrix("cheese", 5, 5), 1, 4, 2,4)
    #print(t)
    #print(CoinImage)
    
    def genTileData(self):
        pass


class IsometricTilemap(Tilemap):
    def draw(self, surface, yamount=10, xamount=0):
        d = self.mat
        hreps = 0
        lreps = 0
        for x in d:
            for y in x:
                #print(d[hreps])
                #print(d[lreps])
                v = d[hreps][lreps]
                #print(v)
                if v or v==0:
                    r = int(v)   
                    n = self.tiles[r]
                    n.draw(surface, ((self.BLOCK_SIZE*lreps) + self.x) - (xamount * lreps), (self.BLOCK_SIZE*hreps) + self.y - (yamount * hreps))
                lreps+=1
            hreps+=1
            lreps = 0
global allowJumping
allowJumping = False

def collide():
    print('collided!')
    sys.stdout.flush()
    
def goto(x, y):
    player.x = x
    player.y = y
    
def cancelXvel():
    didCancelXvel = True
    temp = t.xvel
    t.xvel = 0
    t.x += temp 
    #player.y += player.yvel
    #print('i\'m in a wall') 
    player.wall = True
    player.y += player._temp_yvel -1

def cancelYvel():
    player.allowjumping = True
    temp = player.yvel
    player.y += temp
    player._temp_yvel = temp
    player.yvel = 0
    
def trueCancelYvel():
    #player.canceledYvelThisFrame = True
    on_ground = getOnGround()
    if on_ground:
        if abs(player.yvel) > abs(t.xvel): cancelYvel()
    
    else:
        cancelYvel()
        
    
    
    
    

def e_p_m(t): #enable player move
    if t == 'l':
        player.canmovel = True
    elif t == 'r':
        player.canmover = True
def calc_to_move(player, level, point=100):
    if player.x < point and level.x == 0:
        return player
    else:
        return level
    
def get_present(x, y):
    player.presents += 1
    t.mat[y][x] = 0
init()
    
if __name__ == "__main__":
    now0 = time.time()
    
    init()
    collidedWithLevel = False
    player_move_x = 100
        #player.presents = 0
    
    air = NullTile()
    global setThisFrame
    #global player
    imgld = ImageLoader(name="imgloader0")
    now = time.time()
    
    print(now - now0)
    
    DirtImage = imgld.LoadImage(path + 'dirt_1.png')
    bg = imgld.LoadImage(path + 'pixel_bg.png')
    GrassImage = imgld.LoadImage(path + 'grass_3.png')
    WaterImage = imgld.LoadImage(path + 'water_0.png')
    PlayerImage = imgld.LoadImage(path +'player_0.png')
    PresentImage = imgld.LoadImage(path + 'present_0.png')
    CruddyGrassImage = imgld.LoadImage(path + 'cruddy_grass.png')
    now2 = time.time()
    
    print(now2 - now)
    dirt =  Tile(DirtImage, name="Dirt")
    grass = Tile(GrassImage, name="Grass")
    water = Tile(WaterImage, name="Water")
    present = Tile(PresentImage, name="Present")
    crud = Tile(CruddyGrassImage, name="Cruddy Grass")
    dirt = crud
    player = SpecialTile(1, PlayerImage, 2, 100, 0, 31, name='Player')
    player.canceledYvelThisFrame = False
    #test_sp = SpecialTile(1, GrassImage,2,  0, 0, 32, name="Test")
    #test_sp2 = SpecialTile(1, DirtImage, 2, 0, 0, 32, name="Test2")
    #creg.addUnsidedSpecialCollision(test_sp, test_sp2, collide)
    print("Images Loaded Succesfully")
    '''
    milky_ways = pygame.mixer.Sound("sounds/milky_ways.ogg")
    print("Sounds Loaded Successfully")
    milky_ways.play()
    '''
    global t
    global didCancelXvel
    
    t = Tilemap("Mini_Test", 'level', [air, grass, dirt, water, present], 32, C_MAT_PROVIDE_TYPE='file')
    BLACK = (0,0,0)
    flags = pygame.SCALED
    screen = pygame.display.set_mode((480,480), flags)
    pygame.display.set_caption("PyTile test run")
    running = True
    t.x = 0
    t.y = 0
    player.presents = 0
    player.allowjumping = False
    player.wall = False
    draw_it = 1
    player.yvel = 0
    t.xvel = 0
    t.falsexvel = 0
    
    creg.addSidedSpecialTilemapCollision(player, t, (4,1), (grass, dirt), trueCancelYvel)
    creg.addSidedSpecialTilemapCollision(player, t, (3,2), (grass, dirt), cancelXvel)
    
    
    creg.addSidedSpecialTilemapCollision(player, t, (1,2,3,4), (present,), lambda: get_present(t.getTilePoint(player.x, player.y)[1], t.getTilePoint(player.x, player.y)[0]))
    
    
    print(mask_col.genColMask(t.mat, edge_col_tiles=[0], ignore_tiles=[0]))
    while running:
        player.canceledYvelThisFrame = False
        setThisFrame = False
        didCancelXvel = False
        wall = False
        #Order: 
        #creg.checkCollisions()
        # Velocity, Collisions, Bounds, Draw, Update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if __player__:
                
                    t.xvel -= 3
                
            else:
                t.x -= 3
        if keys[pygame.K_RIGHT]:
            if __player__:
                
                    t.xvel += 3
                
            else:
                t.x += 3
        if keys[pygame.K_q]:
            running = False
        if keys[pygame.K_c]:
            for row_index in range(len(t.mat)):
                for item_index in range(len(t.mat[row_index])):
                    t.mat[row_index][item_index] = 0
        if keys[pygame.K_s]:
            tools.save(t.mat, asksaveasfilename(), clearfile=True)
        if keys[pygame.K_l]:
            tools.load_tmap_mat(askopenfilename(), t)
        if pygame.mouse.get_pressed()[0]:
            #print('mouse!')
            hover = t.getCollidingMouseTiles()
            if type(hover[0]) == int:
                #t.mat[hover[0]][hover[1]] = draw_it
                #print(hover[0], hover[1])
                t.mat[hover[0]][hover[1]] = draw_it
        if keys[pygame.K_0]:
            draw_it = 0
        if keys[pygame.K_1]:
            draw_it = 1
        if keys[pygame.K_2]:
            draw_it = 2
        if keys[pygame.K_3]:
            draw_it = 3
        if keys[pygame.K_4]:
            draw_it = 4
            
        if keys[pygame.K_UP]:
            if player.allowjumping:
                player.yvel += 10
                player.allowjumping = False
                '''
        if keys[pygame.K_DOWN]:
            player.y += 3
'''
        if __player__:
            #c = calc_to_move(player, t)
            player.y -= player.yvel
            
            t.x -= t.xvel
            
            creg.checkCollisions()
        
            player.yvel -= 0.5
        
        if player.x < 0:
            player.x = 0
        if player.x > 480 - 32:
            player.x = 480 -32
        if player.y > (480 - 32):
            player.y = 480 - 32
        
        if t.xvel > 0:
            t.xvel -= 1
        elif t.xvel < 0:
            t.xvel += 1
        if t.xvel > 5:
            t.xvel = 5
        if t.xvel < -5:
            t.xvel = -5
        
        if t.x > 0:
            t.x = 0
        #pygame.display.flip()
        mouse_pos = pygame.mouse.get_pos()
        #test_sp.x = mouse_pos[0]
        #test_sp.y = mouse_pos[1]
        '''
        collidedWithLevel = test_sp.isTmapCollide(t)
        if collidedWithLevel:
            test_sp.image = DirtImage
        else:
            test_sp.image = GrassImage
        '''
        screen.fill(BLACK)
        screen.blit(bg, (0, 0))
        #keys = pygame.key.get_pressed()
        
        #creg.checkCollisions()
        t.draw(screen)
        if __player__:
            player.draw(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    print("successful run!")
elif __name__ == "pytile":
    message()
pygame.quit()



