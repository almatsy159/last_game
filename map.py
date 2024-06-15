import pygame as pg
import os


def highlight(sprite,screen,color="red"):
    rect = sprite.rect
    pg.draw.rect(screen,color,)
    

def call_img(img,beg,w=50,h=50,pos=(0,0),scale=1,color="black"):
    #img =pg.image.load(url).convert_alpha()
    surface = pg.Surface((w,h)).convert_alpha()
    surface.blit(img,pos,(beg.x,beg.y,beg.x+w,beg.y+h))
    surface = pg.transform.scale(surface,(w*scale,h*scale))
    #surface.set_colorkey(color)
    return surface

#img0 = call_img("asset/ts/Factions/Knights/Buildings/House/House_Blue.png")

"""
g = pg.init()
screen = pg.display.set_mode((0,0))
clock = pg.time.Clock()

running = True
"""
"""
class Panel:
    def __init__(self,surface,text="",font=None,size=25,color="blue"):
        self.color = color
        self.font = font
        self.size = size
        self.font = pg.font.SysFont(self.font,self.size)
        self.surface = surface
        self.text = text
        self.img = self.font.render(self.text,True,self.color)
        self.rect = self.img.get_rect()
        
    def render(self):
        self.img = self.font.render(self.text,True,self.color)
    def edit_text(self,text=""):
        self.text = text
        
    def blit(self,screen,pos=(100,100)):
        screen.blit(self.img,pos)
    
    def edit_font(self,font=None,size=None):
        self.font = font
        self.size = size
        self.font = pg.font.SysFont(self.font,self.size)
        self.render()
    
    def draw(self,screen,pos=(150,150)):
        self.blit(screen,pos)
"""
class Point(pg.sprite.Sprite):
    points = pg.sprite.Group()
    def __init__(self,x=0,y=0,z=0,color="black"):
        super().__init__()
        self.x =  x
        self.y = y
        self.z = z
        self.pos = (self.x,self.y,self.z)
        self.color = color
        self.add(Point.points)
    
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"
    
    #def __add__(self,point):
    #    x = self.x + point.x
    #    y = self.y + point.y
    #    z = self.z + point.z
    #    return Point(x,y,z)
    
    #def draw(self,screen):
    #    pg.draw.circle(screen,self.color,(self.x,self.y))
        
class Frame(pg.sprite.Sprite):
    frames = pg.sprite.Group()
    def __init__(self,beg,h,w,color="white",url=None,grid=False):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h
        self.beg = beg
        self.center = (self.beg.x+self.w//2,self.beg.y+self.h//2)

        print(self.w,self.h)
        self.url = url
        if self.url == None:
            self.image= pg.Surface((self.w,self.h))
        else:
            self.image=pg.image.load(url)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center=self.center
        self.elements = pg.sprite.Group()
        self.dico = {}
        self.grid = grid
        self.add(Frame.frames)
        
    #def draw(self,screen):
        #pg.draw.rect(screen,self.color,self.rect)
        #if self.grid == True:
        #    self.make_grid(screen)
        #for i,j in self.elements :
        #    j.draw(screen)
    def clicked(self,e,args=None):
        print(f"clicked on frame : {e}")
        
    def update(self,events):
        for e in events:
            #print("looking for event")
            if e.type == pg.MOUSEBUTTONDOWN:
                #print("in event")
                flag = 0
                ob = None
                for i,j in self.dico.items():
                    print(f"item : {i} ; {j}")
                    if self.rect.collidepoint(e.pos[0],e.pos[1]):
                        print(f"collided something {i},{j}")
                        if isinstance(j,Button):
                            print("clicked on button")
                            j.clicked()
                        if isinstance(j,Tile):
                            j.clicked(self)
                        flag = 1 
                        ob = j
                    else :
                        print("collided nothing")  
                if flag == 0:
                    self.clicked(e)
                else:
                    print(f"collided : {ob}")
                    
    
    def add_to_dic(self,id,element):
        self.dico[id] = element
        
    def clicked_on_child(self):
        print("clicked on child of frame")
        
class Tile(pg.sprite.Sprite):
    tiles = pg.sprite.Group()
    x = 100
    y = 100
    def __init__(self,name,cg,color="green",url=None,map_pos=(0,0)):
        super().__init__()
        self.map_pos = map_pos
        self.name = name
        self.color = color
        self.dx = Tile.x
        self.dy = Tile.y
        #self.image = pg.Surface((self.dx,self.dy))
        if url != None:
            #self.image = pg.image.load("/home/alma/Documents/prog/asset/grass.png")
            self.image = pg.image.load(url)
            self.image = pg.transform.scale(self.image,(self.dx,self.dy))
        else :
            self.image = pg.Surface((self.dx,self.dy))
        #self.image.fill(self.color)
        
        self.cg = cg
        #self.surface = pg.Surface((self.dx,self.dy))
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.cg.x,self.cg.y)
        self.id_item = 0
        self.elements = {}
        self.add(Tile.tiles)
    
    #def draw(self,screen):
    #    pg.draw.rect(screen,self.color,self.rect)
        
    def move(self,x=0,y=0,z=0):
        add = Point(x,y,z)
        self.cg = self.cg + add
        return True
        
    def add_item(self,item,id=None):
        if id ==None:
            id = self.id_item
        self.elements[id] = item
        return True
        
    def clicked(self,parent=None):
        print(f"clicked on tile {self.name}")
        if parent:
            print("parent in call")
            parent.clicked_on_child()
        else:
            print("no args in call")
        if self.color == "green":
            self.color = "red"
        else :
            self.color = "green"
        return self.name
    
    #def update(self,game):
    #    if self.cg.x > game.w:
            
class Player:
    def __init__(self,name=""):
        self.name = name
        self.money = 100
        self.life = 20
        self.magic = 100
        self.carac= [self.money,self.life,self.magic]
        
    def __str__(self):
        my_str = f"{self.name}"
        for c in self.carac :
            my_str += f"{c}"
        return my_str
    
    def loose_life(self,val=1):
        self.life -= val
        
    def get_healed(self,val=1):
        self.life += val
class Shop(Frame):
    def __init__(self,beg,h,w,color,url=None):
        super().__init__(beg,h,w,color,url)
        self.items = pg.sprite.Group()
    
    def clicked_on_child(self):
        print("clicked on child of shop")
        #self.frame = Frame
        
    #def add_item(self,id,ob):
    #    self.items[id] = ob
    
class ShopItem(Tile):
    shop_items = pg.sprite.Group()
    def __init__(self,url,frame,cg,w=100,h=100,color="red",name=None,cost=50):
        #cg = Point(cg.x,y)
        if name == None:
            self.name = f"{cg.x},{cg.y}"
        else:
            self.name = name
        super().__init__(name,cg,color,url)
        #self.image = pg.image.load(url)
        #self.rect = self.image.get_rect()
        #self.rect.center = (1700,500)
        self.cost = cost
        self.frame=frame
        self.add(ShopItem.shop_items)
        #self.y=y
        #self.x=x
        self.w=w
        self.h=h
        #self.btn = Button(self.x,self.y,self.w,self.h,'blue',frame,url)
    
    def clicked(self,args=None):
        print(f"clicked on shopitem :\nname : {self.name}\ncost : {self.cost}")

class Map:
    def __init__(self,dico,x,y,w,h):
        self.minimap = dico
        
        
class Button(pg.sprite.Sprite):
    buttons = pg.sprite.Group()
    def __init__(self,x=0,y=0,w=10,h=10,color="red",frame=None,url=None):
        super().__init__()
        self.url = url
        self.frame = frame
        self.color=color
        self.w=w
        self.h=h
        if self.url == None :
            self.image = pg.Surface((25,25))
        else :
            self.image = pg.image.load(self.url)
            beg = Point(0,0)
            self.image = call_img(self.image,beg)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center=(self.x,self.y)
        
    def clicked(self,e=None):
        print(f"in button , event clicked: {self} :\n\t{e}")

    def update(self,events):
        for e in events:
            #print("looking for event")
            if e.type == pg.MOUSEBUTTONDOWN:
                #print("in event")    
                self.clicked(e)
    
    def add_frame(self,frame):
        if isinstance(frame,Frame):
            self.frame = frame  
            frame.add_to_dic((self.x,self.y),self)
    
    #def draw(self,screen,color="blue"):
    #    pg.draw.rect(screen,color,self.rect)    
    
class Game:
    def __init__(self,screen,perso,ytile=3,xtile=2,font="Arial",font_size=30,img_dir="asset"):
        
        #### temporary #####
        self.objects = {"frames":Frame,"tiles":Tile}
        self.buttons = {}
        self.text = {}
        
        ##### end ######
        self.perso = perso
        
        self.current_path = os.getcwd()
        self.img_dir = img_dir
        print(self.current_path)
        self.ytile = ytile
        self.xtile = xtile
        self.font = pg.font.SysFont(font,font_size)
        self.bg = pg.image.load(f"{self.current_path}/asset/bg0.jpg")
        
        self.bg = self.bg.convert()
        self.bg.set_alpha(200)
        self.status = "creation"
        self.screen = screen
        self.screen.blit(self.bg,(0,0))
        self.running = True
        self.clock = pg.time.Clock()
        self.elements = {"frames":Frame,"tiles":Tile}
        self.new = None
        self.selected = None
        self.to_print = "No Text"
        self.w,self.h = self.screen.get_size()
        print(self.w,self.h)
        self.center = int(self.w/2),int(self.h/2)
        self.last_event = None
    
    def draw_text(self,text="",color="grey",x=0,y=0):
        img = self.font.render(text,True,color)
        self.screen.blit(img,(x,y))
    
    def mouse_click(self,event):
        self.draw_text(f"{event.pos}","white",event.pos[0]+100,event.pos[1]+100)
            
    def make_shopitem(self,name,dir,x,y,parent,ext="png"):
            path = self.get_img(name,dir,ext)
            beg = Point(x,y)
            shop_item = ShopItem(path,parent,beg,name=name)
            parent.add_to_dic((beg.x,beg.y),name)
            return shop_item
        
    def get_img(self,name,dir=None,ext="png"):
        if dir == None:
            dir = self.img_dir
        path = f"{self.current_path}/{dir}/{name}.{ext}"
        return path
        
    def handling_event(self,events):
        #event = None
        #for event in pg.event.get():
        for event in events:
            if event.type == pg.QUIT :
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event)
                if self.status == "creation":
                    click = Point(event.pos[0],event.pos[1])
                    url = self.get_img("grass")
                    print(url)
                    #tile = Tile("noname",click,"blue",url)
                    self.mouse_click(event)
                
                #for k,e in self.elements.items():
                #    pass
                    #if e.rect.collidepoint(event.pos):
                    #    print("collided!")
                    #    e.clicked()
                    #else:
                    #    print("nothing clicked on !")
                        
    def update(self,events=None):
        Frame.frames.update(events)
        Tile.tiles.update()
    
    def add_element(self,name,element):
        self.elements[name] = element

    def display(self):
        pg.display.flip()
    
    def draw(self,opt=None):
        #for i,j in self.elements.items():
        #    #print(i,j)
        #    j.draw(self.screen)
        #self.screen.fill("white")
        
        for i,j in self.objects.items():
            exec(f"j.{i}.draw(self.screen)")
        #Frame.frames.draw(self.screen)
        #Tile.tiles.draw(self.screen)
        dialog_text = self.draw_text(f"{self.to_print}","red",1720,150)
        #self.draw_text("A","black",150,150)
        #Point.points.draw()
        #for t in Tile.tiles:
            #print(t.cg.x)
        ### tmp ###
        #for k,b in self.buttons.items():
        #    b.draw(self.screen)
        #Button.buttons.draw(self.screen)
        ### end ###
        #self.draw_text(f"{t.cg.x},{t.cg.y}","grey",t.cg.x,t.cg.y)
        
    def first(self):
        #center = Point(self.center[0],self.center[1],0)
        #center_tile = Tile("center",center)
        #self.tiles = Tile.tiles
        #center_tile.add(Tile.tiles)
        #self.elements["center_tile"] = center_tile
        #panel = Panel("hello_world")
        #self.elements["panel"] = panel
        #test_beg = Point(50,50)
        #test_w
        #test_h
        #test_color = "red"
        #test_frame = Frame(test_beg,test_end,test_color,grid=True)
        
        dialog_beg = Point(1700,100)
        dialog_w = 200
        dialog_h = 700
        shop = Shop(dialog_beg,dialog_h,dialog_w,"purple")
        dialog_text = self.draw_text("hello","red",1720,150)
        
        #btn_quit_dialog = Button(1770,120)
        #tmp
        #self.buttons[1770,120] = btn_quit_dialog
        #dialog.add_to_dic((1770,120),btn_quit_dialog)
        #btn_quit_dialog.add_frame(dialog)
        
        #print(Tile.tiles)
        #test_frame.add(Frame.frames)
        #self.elements["test_frame"] = test_frame
        
        #t1 = self.draw_text("hello world",color="white",x=500,y=200)
        x_init = 100
        y_init = 100
        bloc = 100
        #delta = 1
        cpt=0
        tile_map = {}
        
        for x in range(self.xtile): 
            for y in range(self.ytile):
                #if cpt%2 ==0:
                #    color = "white"
                #else:
                color = "grey"
                name = "mud"
                path = self.get_img(name)
                xt = x_init + (x * bloc)
                yt = y_init + (y * bloc)
                cg = Point(xt,yt,0)
                #print(x,y)
                tile = Tile(name,cg,color,path,map_pos=(x,y))
                cpt += 1
                tile_map[x,y] = tile
        #self.tile_map = Map(tile_map)
        #print(cpt)
        
        
        
        self.make_shopitem("House_Blue","asset/ts/Factions/Knights/Buildings/House",1750,500,shop)
        #house_path = self.get_img("House_Blue","asset/ts/Factions/Knights/Buildings/House")
        #house_beg = Point(1750,500)
        #house = Tile("house",house_beg,url=house_path)
        #house = ShopItem(house_path,shop,house_beg,name="house")
        #shop.add_to_dic((1750,500),house)
        
        
        self.make_shopitem("Castle_Blue","asset/ts/Factions/Knights/Buildings/Castle",1750,600,shop)
        #castle_path = self.get_img("Castle_Blue","asset/ts/Factions/Knights/Buildings/Castle")
        #castle_beg = Point(1750,600)
        #castle = Tile("castle",castle_beg,url=castle_path)
        #castle = ShopItem(castle_path,shop,castle_beg,name="castle")
        #shop.add_to_dic((1750,600),castle)
        
        
        #castle = Button(1700,500,100,100,house_path)
        #self.buttons[1700,500]=castle
        #castle.add_frame(dialog)
        #house_img = call_img(house_path,def_beg,100,100)
        
        
        
    def run(self):
        self.first()
        while self.running == True:
            event = pg.event.get()
            self.handling_event(event)
            self.update(event)
            self.draw()
            self.display()
            self.clock.tick(60)

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((0,0))
    global g1
    perso = Player("alma")
    g1 = Game(screen,perso)
    
    g1.run()
    pg.quit()

"""
while running:
    
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    screen.fill("black")
    pg.display.flip()
    clock.tick(60)
    
pg.quit()
"""