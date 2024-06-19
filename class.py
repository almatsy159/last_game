import pygame as pg
import os


def call_img(img,beg,w=50,h=50,pos=(0,0),scale=1,color="black",alpha=0):
    surface = pg.Surface((w,h))
    surface.blit(img,pos,(beg.x,beg.y,beg.x+w,beg.y+h))
    surface = pg.transform.scale(surface,(w*scale,h*scale))
    surface = surface.set_alpha(value=alpha)
    surface = surface.convert_alpha()
    return surface

def get_url(name,dir="asset",ext="png"):
    current_path = os.getcwd()
    path = f"{current_path}/{dir}/{name}.{ext}"
    return path


class ComposedSprite:
    def __init__(self,sprites,pos,orientation="tl"):
        """_summary_

        Args:
            sprites (_type_): _description_
            pos (_type_): _description_
            orientation (str, optional): _description_. Defaults to "tl".
        """
        if isinstance(sprites,list):
            print("sprites is  a list(expect a list of sprites,or url)")
            l = len(sprites)
            for i in sprites:
                if isinstance(i,pg.sprite.Sprite):
                    print("is a a sprite")
                elif isinstance(i,str):
                    #try url
                    self.try_url(i)
            
        elif isinstance(sprites,str):
            print("sprite is an str (probably! url)")
            #try url
            self.try_url(sprites)
            
        else :
            print("not initialised")
            raise TypeError
    def try_url(self,url):
        if os.path.exists(url):
            ext= os.path.splitext
            if ext == "json":
                self.get_json(url)
            if ext == "png":
                self.load_image(url)
    
    def get_json(self):
        pass
    
    # maybe external of this class !
    def load_image(self,url):
        image = pg.image.load(url)
        return image
            
        self.image = pg.image.load(url)
        
class Player:
    def __init__(self,name="player"):
        self.name = name
        self.map = {}

    def add_tile(self,x,y,tile):
        self.map[x,y] = tile
        
class Frame(pg.sprite.Sprite):
    frames = pg.sprite.Group()
    def __init__(self,beg,h,w,url):
        super().__init__()
        self.w = w
        self.h = h
        self.beg = beg
        self.center = (self.beg.x+self.w//2,self.beg.y+self.h//2)
        self.url = url        
        self.image=pg.image.load(url)
        self.image = pg.transform.scale(self.image,(self.w,self.h)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center=self.center
        
        
        self.elements = pg.sprite.Group()
        self.dico = {}
        self.add(Frame.frames)
        
    def clicked(self,e,args=None):
        #print(f"clicked on frame : {e}")
        pass
    def update(self,events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                flag = 0
                ob = None
                for i,j in self.dico.items():
                    if self.rect.collidepoint(e.pos[0],e.pos[1]):
                        if isinstance(j,Tile):
                            j.clicked(self)
                        flag = 1 
                        ob = j
                    else :
                        #print("collided nothing in self.dico")
                        pass
                if flag == 0:
                    #print("making frame process")
                    self.clicked(e)
                else:
                    print(f"collided : {ob}")
                    
    
    def add_to_dic(self,id,element):
        self.dico[id] = element
        
    def clicked_on_child(self):
        print("clicked on child of frame")
        
    def get_group(self):
        return Frame.frames

class Tile(pg.sprite.Sprite):
    tiles = pg.sprite.Group()
    #x = 50
    #y = 50
    def __init__(self,name,x,y,directory,ext="png",map_pos=(0,0)):
        super().__init__()
        self.map_pos = map_pos
        self.name = name
        self.dir = directory
        self.ext = ext
        self.x = x
        self.y = y
        self.url = get_url(self.name,self.dir,self.ext)
        
        self.image = pg.image.load(self.url)
        self.image = pg.transform.scale(self.image,(self.x,self.y))
        
        
        self.x=x
        self.y=y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.id_item = 0
        self.elements = {}
        self.add(Tile.tiles)

    def clicked_on_child(self):
        print(f"clicked on {self}")
class Game:
    def __init__(self,screen,font="Arial",font_size=30,img_dir="asset",color="red"):
        
        self.text = {}
        self.changed = False
        self.first_time = True
        self.color = color
        self.objects = {"frames":Frame,"tiles":Tile}
    
        self.img_dir = img_dir
        
    
        self.font = pg.font.SysFont(font,font_size)
        self.bg = pg.image.load(f"asset/bg0.jpg")
        
        #self.bg.set_alpha(200)
        self.bg = self.bg.convert()
        
        #self.status = "creation"
        self.screen = screen
        self.screen.blit(self.bg,(0,0))
        self.running = True
        self.clock = pg.time.Clock()
        self.elements = {"frames":Frame,"tiles":Tile}
    
        self.w,self.h = self.screen.get_size()
        print(self.w,self.h)
        self.center = int(self.w/2),int(self.h/2)
        self.last_event = None
    
    def draw_text(self,text="",color="grey",x=0,y=0):
        img = self.font.render(text,True,color)
        self.screen.blit(img,(x,y))
        return img
    
    def mouse_click(self,event):
        print(f"clicked : {event}")
        
    def check_obj(self,event):
        #print(event)
        res = None
        for k,s in self.objects.items():
            #print(k,s)
            y = eval(f"s.{k}")
            #print(y.sprites)
            for i in y.sprites():
                if i.rect.collidepoint(event.pos):
                    #print(f"{i} collided !")
                    res = i
                
        return res
            
            
    def get_img(self,name,dir=None,ext="png"):
        if dir == None:
            dir = self.img_dir
        path = f"{self.current_path}/{dir}/{name}.{ext}"
        return path

    def handling_event(self,events):
        for event in events:
            if event :
                self.changed = True
            if event != self.last_event:
                if event.type == pg.QUIT :
                    self.running = False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_click(event)
                self.last_event = event
                        
    def update(self,events=None):
        Frame.frames.update(events)
        Tile.tiles.update()

    def display(self):
        if self.changed == True or self.first_time ==True:
            pg.display.flip()
            if self.first_time == True:
                self.first_time = False
    
    def draw(self,events=None):
        
        for i,j in self.objects.items():
            exec(f"j.{i}.draw(self.screen)")

    def first(self):
        Tile("grass",100,100,"asset")
    def run(self):
        self.first()
        while self.running == True:
            event = pg.event.get()
            self.handling_event(event)
            self.update(event)
            self.draw(event)
            self.display()
            self.clock.tick(60)

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((0,0))
    global g1
    g1 = Game(screen)
    
    g1.run()
    pg.quit()
