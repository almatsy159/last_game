import pygame as pg

"""
g = pg.init()
screen = pg.display.set_mode((0,0))
clock = pg.time.Clock()

running = True
"""

class Point:
    def __init__(self,x=0,y=0,z=0,color="black"):
        self.x =  x
        self.y = y
        self.z = z
        self.pos = (self.x,self.y,self.z)
        self.color = color 
    
    def __add__(self,point):
        x = self.x + point.x
        y = self.y + point.y
        z = self.z + point.z
        return Point(x,y,z)
    
    def draw(self,screen):
        pg.draw.circle(screen,self.color,(self.x,self.y))
        

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