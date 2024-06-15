import pygame as pg



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
    def __init__(self,beg,h,w,color="white",grid=False):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h
        self.beg = beg
        self.center = (self.beg.x+self.w//2,self.beg.y+self.h//2)

        print(self.w,self.h)
        
        self.image= pg.Surface((self.w,self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center=self.center
        self.elements = pg.sprite.Group()
        self.grid = grid
        self.add(Frame.frames)
        
    #def draw(self,screen):
        #pg.draw.rect(screen,self.color,self.rect)
        #if self.grid == True:
        #    self.make_grid(screen)
        #for i,j in self.elements :
        #    j.draw(screen)
    def clicked(self):
        print("clicked on frame")
        
        
class Tile(pg.sprite.Sprite):
    tiles = pg.sprite.Group()
    x = 50
    y = 50
    def __init__(self,name,cg,color="green"):
        super().__init__()
        self.name = name
        self.color = color
        self.dx = Tile.x
        self.dy = Tile.y
        self.image = pg.Surface((self.dx,self.dy))
        self.image.fill(self.color)
        self.cg = cg
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
        
    def clicked(self):
        if self.color == "green":
            self.color = "red"
        else :
            self.color = "green"
        return self.name
    
    #def update(self,game):
    #    if self.cg.x > game.w:
            
        
class Game:
    def __init__(self,screen,ytile=10,xtile=10,font="Arial",font_size=30):
        self.ytile = ytile
        self.xtile = xtile
        self.font = pg.font.SysFont(font,font_size)
        self.bg = pg.image.load("/home/alma/Documents/prog/asset/bg0.jpg")
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
        self.w,self.h = self.screen.get_size()
        print(self.w,self.h)
        self.center = int(self.w/2),int(self.h/2)
        self.last_event = None
    
    def draw_text(self,text="",color="grey",x=0,y=0):
        img = self.font.render(text,True,color)
        self.screen.blit(img,(x,y))
    
    def mouse_click(self,event):
        self.draw_text(f"{event.pos}","white",event.pos[0]+100,event.pos[1]+100)
            

    def handling_event(self):
        event = None
        for event in pg.event.get():
            if event.type == pg.QUIT :
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event)
                if self.status == "creation":
                    click = Point(event.pos[0],event.pos[1])
                    #tile = Tile("noname",click,"blue")
                    self.mouse_click(event)
                
                #for k,e in self.elements.items():
                #    pass
                    #if e.rect.collidepoint(event.pos):
                    #    print("collided!")
                    #    e.clicked()
                    #else:
                    #    print("nothing clicked on !")
                        
    def update(self):
        Frame.frames.update()
        Tile.tiles.update()
    
    def add_element(self,name,element):
        self.elements[name] = element

    def display(self):
        pg.display.flip()
    
    def draw(self,opt=None):
        #for i,j in self.elements.items():
        #    #print(i,j)
        #    j.draw(self.screen)
        Tile.tiles.draw(self.screen)
        Frame.frames.draw(self.screen)
        #self.draw_text("A","black",150,150)
        #Point.points.draw()
        #for t in Tile.tiles:
            #print(t.cg.x)
    
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
        
        #dialog_beg = Point(1700,200)
        #dialog_w = 100
        #dialog_h = 150
        #dialog = Frame(dialog_beg,dialog_w,dialog_h,"purple")
        
        #print(Tile.tiles)
        #test_frame.add(Frame.frames)
        #self.elements["test_frame"] = test_frame
        
        #t1 = self.draw_text("hello world",color="white",x=500,y=200)
        x_init = 100
        y_init = 100
        bloc = 50
        delta = 1
        cpt=0
        
        for x in range(self.xtile): 
            for y in range(self.ytile):
                if cpt%2 ==0:
                    color = "white"
                    ncolor = "grey"
                else:
                    color = "grey"
                    ncolor="black"
                    
                if x%2 ==1:
                    tmp = color
                    color = ncolor
                    ncolor = tmp
                name = f"{x},{y}"
                xt = x_init + (x * bloc)
                yt = y_init + (y * bloc)
                cg = Point(xt,yt,0)
                print(x,y)
                tile = Tile(name,cg,color)
                cpt += 1
        print(cpt)
    def run(self):
        self.first()
        while self.running == True:
            self.handling_event()
            self.update()
            self.draw()
            self.display()
            self.clock.tick(60)

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((0,0))
    global g1
    g1 = Game(screen)
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