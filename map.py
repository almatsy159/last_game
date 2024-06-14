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
class Point:
    def __init__(self,x=0,y=0,z=0,color="black"):
        self.x =  x
        self.y = y
        self.z = z
        self.pos = (self.x,self.y,self.z)
        self.color = color 
    
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"
    
    def __add__(self,point):
        x = self.x + point.x
        y = self.y + point.y
        z = self.z + point.z
        return Point(x,y,z)
    
    def draw(self,screen):
        pg.draw.circle(screen,self.color,(self.x,self.y))
        
class Frame:
    def __init__(self,beg,end,color="white",grid=False):
        self.color = color
        #print(beg,end)
        self.beg = beg
        self.end = end
        self.w = self.end.x - self.beg.x
        self.h = self.end.y - self.beg.y
        print(self.w,self.h)
        self.rect = pg.Rect(self.beg.x,self.beg.y,self.w,self.h)
        self.surface = pg.Surface((self.w,self.h))
        self.elements = {}
        self.grid = grid
        
    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect)
        #if self.grid == True:
        #    self.make_grid(screen)
        for i,j in self.elements :
            j.draw(screen)
            
    def make_grid(self,screen,block=25,color="green"):
        x_init = self.beg.x
        y_init = self.beg.y
        x_end = self.end.x
        y_end = self.end.y
        #print(x_init,y_init)
        #print(x_end,y_end)
        
        for x in range(x_init,x_end,block):
            for y in range(y_init,y_end,block):
                rect = pg.Rect(x,y,block,block)
                pg.draw.rect(screen,color,rect,1)
    
    def clicked(self):
        print("clicked on frame")


        
class Tile:
    x = 50
    y = 50
    def __init__(self,name,cg,color="green"):
        self.name = name
        self.color = color
        self.dx = Tile.x
        self.dy = Tile.y
        self.img= pg.Surface((self.dx,self.dy))
        self.cg = cg
        self.rect = self.img.get_rect()
        self.rect.center = (self.cg.x,self.cg.y)
        self.id_item = 0
        self.contain = {}
    
    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect)
        
    def move(self,x=0,y=0,z=0):
        add = Point(x,y,z)
        self.cg = self.cg + add
        return True
        
    def add_item(self,item,id=None):
        if id ==None:
            id = self.id_item
        self.contain[id] = item
        return True
        
    def clicked(self):
        if self.color == "green":
            self.color = "red"
        else :
            self.color = "green"
        return self.name
        
class Game:
    def __init__(self,screen):
        self.screen = screen
        self.running = True
        self.clock = pg.time.Clock()
        self.elements = {}
        self.new = None
        self.w,self.h = self.screen.get_size()
        self.center = int(self.w/2),int(self.h/2)
        self.last_event = None

    def handling_event(self):
        event = None
        for event in pg.event.get():
            if event.type == pg.QUIT :
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.k_q:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event)
                for k,e in self.elements.items():
                    if e.rect.collidepoint(event.pos):
                        print("collided!")
                        e.clicked()
                    else:
                        print("nothing clicked on !")
                        
    def update(self):
        pass
    
    def add_element(self,name,element):
        self.elements[name] = element

    def display(self):
        pg.display.flip()
    
    def draw(self):
        for i,j in self.elements.items():
            #print(i,j)
            j.draw(self.screen)
        
    def first(self):
        center = Point(self.center[0],self.center[1],0)
        center_tile = Tile("center",center)
        self.elements["center_tile"] = center_tile
        #panel = Panel("hello_world")
        #self.elements["panel"] = panel
        test_beg = Point(50,50)
        test_end = Point(150,150)
        test_color = "red"
        test_frame = Frame(test_beg,test_end,test_color,grid=True)
        self.elements["test_frame"] = test_frame

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