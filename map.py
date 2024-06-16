import pygame as pg
import os
import time
# need to:
# add sprite asset to point
# replace url (not important in frame or tile) by name + dir + ext

# x = 0 , y = 0
# x = 0
# y = 0
# x = max
# y = max

def highlight(sprite,screen,color="red"):
    rect = sprite.rect
    pg.draw.rect(screen,color,rect,1)
    

def call_img(img,beg,w=50,h=50,pos=(0,0),scale=1,color="black",alpha=0):
    surface = pg.Surface((w,h))
    surface.blit(img,pos,(beg.x,beg.y,beg.x+w,beg.y+h))
    surface = pg.transform.scale(surface,(w*scale,h*scale))
    surface = surface.set_alpha(value=alpha)
    surface = surface.convert_alpha()
    return surface

class Point(pg.sprite.Sprite):
    points = pg.sprite.Group()
    def __init__(self,x=0,y=0,z=0,color="black",url=None,w=5,h=5,todraw = False):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.pos = (self.x,self.y,self.z)
        self.color = color
        if url != None:                
            self.image=pg.image.load(url)
            self.image = pg.transform.scale(self.image,(self.w,self.h)) 
        else:
            self.image = pg.Surface((w,h))
        self.todraw = todraw
        #if self.todraw == True:
        self.add(Point.points)
    
    def __str__(self):
        return f"{self.x},{self.y},{self.z}" 

class Frame(pg.sprite.Sprite):
    frames = pg.sprite.Group()
    def __init__(self,beg,h,w,color="white",url=None):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h
        self.beg = beg
        self.center = (self.beg.x+self.w//2,self.beg.y+self.h//2)

        self.url = url
        if self.url != None:
            #print("load image for {self.name}")         
            self.image=pg.image.load(url)
            self.image = pg.transform.scale(self.image,(self.w,self.h)).convert_alpha()
            #p=Point(50,1000)
            #self.image = call_img(self.image,p,w,h)      
        else:
            self.image= pg.Surface((self.w,self.h))
            
        #self.image.fill(self.color)
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
    def __init__(self,name,cg,color="green",url=None,map_pos=(0,0),x=50,y=50):
        super().__init__()
        self.map_pos = map_pos
        self.name = name
        self.color = color
        self.dx = x
        self.dy = y
        
        if url != None:
            self.image = pg.image.load(url)
            self.image = pg.transform.scale(self.image,(self.dx,self.dy))
        else :
            self.image = pg.Surface((self.dx,self.dy))
        
        self.cg = cg
        self.rect = self.image.get_rect()
        self.rect.center = (self.cg.x,self.cg.y)
        self.id_item = 0
        self.elements = {}
        self.add(Tile.tiles)

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
        #print(f"clicked on tile {self.name}")
        if parent:
            print("parent in call")
            parent.clicked_on_child()
        else:
            print("no args in call")
        if self.color == "green":
            self.color = "red"
        else :
            self.color = "green"
        g1.to_print = self.name
        return self.name
    
    def get_group(self):
        return Tile.tiles

class MapTile(Tile):
    def __init__(self, map,name, cg, color="green", url=None, map_pos=(0, 0), x=50, y=50):
        super().__init__(name, cg, color, url, map_pos, x, y)
        self.map = map
class Decoration(Frame):
    def __init__(self,beg,h,w,url,color="white"):
        super().__init__(beg,h,w,color,url)
    
class Tools(Frame):
    def __init__(self,lst ,beg, h, w, color="white", url=None):
        super().__init__(beg, h, w, color, url)
        self.lst = lst
    
class Banner(Frame):
    def __init__(self,beg,w,h,url,color="black"):
        super().__init__(beg,h,w,color,url)
        
class Player(Frame):
    def __init__(self,name,beg,h,w,color,url,pos=(0,0)):
        super().__init__(beg,h,w,color,url)
        self.name = name
        self.pos = pos
        b0 = Point(beg.x+50,beg.y+250)
        self.life = Carac(20,"life")
        b1 = Point(beg.x+50,beg.y+300)
        self.money = Carac(100,"money")
        #self.life = 20
        b2 = Point(beg.x+50,beg.y+350)
        self.stone = Carac(0,"food")
        self.magic = 100
        self.carac= [self.money,self.life,self.magic]
        self.home = self.pos
        self.tiles = {}
        self.access = {}
    """
    def tile_access(self,x,y):
        for i,j in self.tiles.items() :
            if not self.access[i]:
                x1,y1 = i[0],i[1]
                self.access[x1,y1] = True
                self.access[x1-1,y1] = True
                self.access[x1+1,y1] = True
                self.access[x1,y1-1] = True 
                self.access[x1,y1+1] = True
    """    
        
        #self.owned = {}
    def change_pos(self,x=0,y=0):
        self.pos = self.pos[0] + x, self.pos[1] + y
        
    def __str__(self):
        my_str = f"{self.name}"
        for c in self.carac :
            my_str += f"{c}"
        return my_str
    def loose_money(self,val=1):
        print("losing :",val)
        self.money -= val
    def loose_life(self,val=1):
        self.life -= val
        
    def get_healed(self,val=1):
        self.life += val
        
    def tolist(self):
        lst = [f"{self.name}"]
        for c in self.carac:
            lst.append(f"{c}")
            
    def update(self,events=None):
        self.carac= [self.pos,self.money,self.life,self.magic]
        
class Shop(Frame):
    def __init__(self,beg,h,w,color,url=None):
        super().__init__(beg,h,w,color,url)
        self.items = pg.sprite.Group()
    
    def clicked_on_child(self):
        print("clicked on child of shop")

class ShopItem(Tile):
    shop_items = pg.sprite.Group()
    def __init__(self,url,frame,cg,w=100,h=100,color="red",name=None,cost=50,x=100,y=100,number=1):
        #cg = Point(cg.x,y)
        if name == None:
            self.name = f"{cg.x},{cg.y}"
        else:
            self.name = name
        super().__init__(name,cg,color,url,x=x,y=y)
        self.cost = cost
        self.number = number
        self.frame=frame
        self.add(ShopItem.shop_items)
        self.w=w
        self.h=h
        self.selling= False
        
    def clicked(self,args=None):
        print(f"clicked on shopitem :\nname : {self.name}\ncost : {self.cost}")
    
    def get_item(self):
        res = None
        if self.number > 0:
            res = self
            self.number -=1
            self.selling = False
        return res
class Map(pg.sprite.Sprite):
    maps = pg.sprite.Group()
    def __init__(self,game,x,y,w,h,xi=0,yi=0):
        # x and y are blocksize
        super().__init__()
        self.xi = xi
        self.yi = yi
        self.image = pg.Surface((w,h))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.tiles = pg.sprite.Group()
        #self.map_tiles = {}
        
        self.game = game
        self.minimap = {}
        for i in range(w):
            for j in range(h):
                if i == 1:
                    name = "Water"
                elif i==0:
                    name = "grass"
                elif i == w-1:
                    name = "Water"
                else :
                    name = "mud"
                p=(x*i,y*j)
                #print(p)
                tile = game.make_maptile(self,name,self.xi+ (50*i),self.yi + (50*j),"grey",map_pos=(j,i))
                self.minimap[i,j] = tile 
                self.tiles.add(tile)
                #self.map_tiles[tile] = {} 
                #self.dico[x,y] = tile
                #print(p)
        #print(self.minimap)
        Map.maps.add(self)

class Carac:

    def __init__(self,val, name):
        self.name = name
        self.val = val

    
    def __plus__(self,val=0):
        self.val += val
        return self.val
        
    def __minus__(self,val=0):
        self.val -= val
        return self.val
        
    def __lt__(self,val=0):
        return self.val < val
    
    def __le__(self,val=0):
        return self.val <= val
    
    def __gt__(self,val=0):
        return self.val < val
    
    def __ge__(self,val=0):
        return self.val <= val
    
    def __eq__(self,val=0):
        return self.val == val
class Panel(Frame):
    panels = pg.sprite.Group()
    def __init__(self,text, beg, h, w,color="white",bg="black",font="Arial", url=None):
        super().__init__(beg, h, w, color, url)
        self.text = text
        self.font = font
        self.bg = bg
        self.add_text()
        self.add(Panel.panels)
        self.lines = []
        
    def add_text(self,font=None,size=25,color=None,bg=None):
        if color ==None:
            color = self.color
        if font == None:
            font = self.font
        if bg == None:
            bg = self.bg
        font = pg.font.SysFont(font,size)
        surface = font.render(self.text,True,color,bg)
        self.image.blit(surface,(0,0))
        self.image.convert()
        
    def edit_text(self,text=""):
        self.image.fill(self.bg)
        self.text = text
        self.add_text()
        
    def update(self,args=None):
        self.edit_text(self.text)
class Description(Frame):
    def __init__(self,beg,h, w, color="white", url=None):
        super().__init__(beg, h, w, color, url)
        
class ComposedColSprite(pg.sprite.Sprite):
    def __init__(self,center,top=None,bot=None):
        super().__init__()
        #self.w = left.w + center.w + right.w
        self.w = center.w
        self.h = bot.h + center.h + top.h
        self.image = pg.Surface(self.w,self.h)
        self.rect = self.image.get_rect()
        current_height = 0
        if top:
            current_height += top.h
            self.image.blit(top.image,(0,0,center.w,current_height)) 
        current_height += center.h   
        self.image.blit(center.image,(0,top.h,center.w,top.h+center.h)) 
        if bot:
            self.image.blit(bot.image,(0,current_height,0,current_height+bot.h))
        

class Game:
    def __init__(self,screen,ytile=11,xtile=21,font="Arial",font_size=30,img_dir="asset",color="red"):
        
        self.text = {}
        self.changed = False
        self.first_time = True
        self.color = color
        self.objects = {"frames":Frame,"tiles":Tile,"maps":Map,"panels":Panel}
        self.flag = False
        self.init_pos = (5,11)
        #self.to_exe= ""
        self.current_path = os.getcwd()
        self.img_dir = img_dir
        print(self.current_path)
        
        self.ytile = ytile
        self.xtile = xtile
        self.font = pg.font.SysFont(font,font_size)
        self.bg = pg.image.load(f"{self.current_path}/asset/bg0.jpg")
        
        self.bg.set_alpha(200)
        self.bg = self.bg.convert()
        
        self.status = "creation"
        self.screen = screen
        self.screen.blit(self.bg,(0,0))
        self.running = True
        self.clock = pg.time.Clock()
        self.elements = {"frames":Frame,"tiles":Tile}
        self.new = None
        self.selected = None
        self.selected_state = None
        self.to_print = "No Text"
        
        self.w,self.h = self.screen.get_size()
        print(self.w,self.h)
        self.center = int(self.w/2),int(self.h/2)
        self.last_event = None
    
    def draw_text(self,text="",color="grey",x=0,y=0):
        img = self.font.render(text,True,color)
        self.screen.blit(img,(x,y))
        return img
    
    def mouse_click(self,event):
        #self.draw_text(f"{event.pos}","white",event.pos[0]+100,event.pos[1]+100)
        res = self.check_obj(event)
        if isinstance(res,MapTile) and isinstance(self.selected,ShopItem) and res:
            if self.player.money >= self.selected.cost:
                if self.selected.selling == True:
                    item = self.selected.get_item()
                    print(f"plaver money : {self.player.money}\n{self.player.tiles}\n{self.selected.selling}")
                    self.player.money -= self.selected.cost
                    self.player.tiles[res] = self.selected
                    #self.selected.selling = False
                    print(f"plaver money : {self.player.money}\n{self.player.tiles}\n{self.selected.selling}")
                else :
                    if self.selected.number > 0:
                        self.selected.selling = True
                    else :
                        print("out of order !")
            else :
                print("not enough money !")
            self.selected = None
        elif isinstance(res,(ShopItem,Shop)) and isinstance(self.selected,ShopItem):
            print("shouldn't buy item")
        elif isinstance(res,MapTile):
            if res == self.selected:
                print("clicked twice on tile !")
        if res :
            highlight(res,self.screen,self.color)
            print(f"selected : {res}")
            self.selected = res
            self.to_print = f"{res}"
        else:
            print("no result =x")
            self.to_print = "no result"
        
    def check_obj(self,event):
        #print(event)
        res = None
        for k,s in self.objects.items():
            #print(k,s)
            y = eval(f"s.{k}")
            #print(y.sprites)
            for i in y.sprites():
                """
                print(i)
                print(event)
                if isinstance(i,Decoration):
                    print("is decoration")
                elif isinstance(i,Tools):
                    print("is tool")
                elif isinstance(i,Tile):
                    print("is tile")
                elif isinstance(i,Frame):
                    print("is frame")
                """
                if i.rect.collidepoint(event.pos):
                    #print(f"{i} collided !")
                    res = i
                
        return res
            
            
    def make_shopitem(self,name,dir,x,y,parent,ext="png"):
            path = self.get_img(name,dir,ext)
            beg = Point(x,y)
            shop_item = ShopItem(path,parent,beg,name=name)
            parent.add_to_dic((beg.x,beg.y),name)
            return shop_item
        
    def make_shop(self,x,y,w,h,name,dir,ext="png",color="red"):
            beg = Point(x,y)
            path = self.get_img(name,dir,ext)
            #call_img()
            shop = Shop(beg,h,w,color,path)
            return shop
        
    def get_img(self,name,dir=None,ext="png"):
        if dir == None:
            dir = self.img_dir
        path = f"{self.current_path}/{dir}/{name}.{ext}"
        return path

    def make_tile(self,name,x,y,color,dir="asset",ext="png",map_pos=(0,0)):
        cg = Point(x,y)
        path = self.get_img(name,dir,ext)
        tile = Tile(name,cg,color,path,map_pos)
        return tile
    def make_maptile(self,map,name,x,y,color,dir="asset",ext="png",map_pos=(0,0)):
        cg = Point(x,y)
        path = self.get_img(name,dir,ext)
        tile = MapTile(map,name,cg,color,path,map_pos)
        return tile             
    def handling_event(self,events):
        #if self.selected != None:
        #    print(self.selected)
            
            #if isinstance(self.selected,ShopItem):
            #    if self.perso.money >= self.selected.cost :
            #        self.selected_state = "buyable"
            #    else :
            #        self.selected_state = "not_buyable"
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
                    #if self.selected != None and self.selected:
                    self.mouse_click(event)
                    #print("hey in event")
                    #print(event)
                    #if self.status == "creation":
                    #click = Point(event.pos[0],event.pos[1])
                    #url = self.get_img("grass")
                    #self.mouse_click(event)
                    self.flag = True
                self.last_event = event
                        
    def update(self,events=None):
        Frame.frames.update(events)
        Tile.tiles.update()
        Map.maps.update()
        #self.panel.edit_text(self.to_print)
        #self.panel_desc.edit_text(f"{self.player}")
        #print(self.main_map.map_tiles)
        for t in Tile.tiles :
            #print(t.map_pos,self.player.pos)
            if t.map_pos == self.player.pos:
                #print("éequal !")
                #highlight(t,self.screen,"green")
                t.image.fill(t.color)
        #Panel.panels.update()
    
    def add_element(self,name,element):
        self.elements[name] = element

    def display(self):
        if self.changed == True or self.first_time ==True:
            pg.display.flip()
            if self.first_time == True:
                self.first_time = False
    
    def draw(self,events=None):
        
        for i,j in self.objects.items():
            exec(f"j.{i}.draw(self.screen)")
        dialog_text = self.draw_text(f"{self.to_print}","red",1600,150)
        if self.flag == True:
            for e in events:
                #print(e)
                if e.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_click(e)
                    print("false flag in self. draw")
                    self.flag = False
        
    def first(self):
        bt = Point(650,700)

        # b for beg ; p for player ; h for head ;e for end; d for description;b banner
        bp2 = Point(25,125)
        bsh = Point(1300,0)
        shop_head = Decoration(bsh,400,800,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Up.png")
        esh = Point(1300,600)
        shop_tail = Decoration(esh,400,800,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Down.png")
        shop = self.make_shop(1500,100,400,750,"Carved_9Slides","asset/ts/UI/Banners")
        dialog_text = self.draw_text(self.to_print,"red",1720,150)
        
        bbh = Point(300,-75)
        ban_head = Decoration(bbh,300,200,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Left.png")
        
        bbt = Point(1350,-75)
        ban_tail = Decoration(bbt,300,200,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Right.png")
        
        bth = Point(300,624)
        tool_head = Decoration(bth,500,350,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Left.png")
        
        btt = Point(1350,624)
        tool_tail = Decoration(btt,500,350,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Right.png")
        

        bt = Point(450,749)
        tool = Tools([],bt,250,1150,"grey","/home/alma/Documents/prog/asset/ts/UI/Banners/Carved_9Slides.png")

        bb = Point(400,0)
        banner = Banner(bb,1150,150,"/home/alma/Documents/prog/asset/ts/UI/Banners/Carved_9Slides.png")
        
        
        #bttt = Point(300,300)
        #test = ShopItem("/home/alma/Documents/prog/asset/items1.png",shop,bttt,100,100)
        
        #btp = Point(450,25)
        #self.panel = Panel(self.to_print,btp,100,400)
        
        #bdp = Point(10,500)
        #self.panel_desc = Panel(f"{self.player}",bdp,100,200)
        bp = Point(0,100)
        
        bdh = Point(-200,0)
        desc_head = Decoration(bdh,400,800,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Up.png")
        edh = Point(-200,600)
        desc_tail = Decoration(edh,400,800,"/home/alma/Documents/prog/asset/ts/UI/Banners/Banner_Connection_Down.png")
        description = Description(bp,750,400,"red","/home/alma/Documents/prog/asset/ts/UI/Banners/Carved_9Slides.png")
        
        self.player = Player("alma",bp2,200,200,"red","/home/alma/Documents/prog/asset/gob.png",self.init_pos)
        #perso = Player("alma",bp,800,400,"red","/home/alma/Documents/prog/asset/ts/UI/Banners/Carved_9Slides.png")
        
        x= 100
        y = 100
        bloc = 100
        #tile_map = {}
        self.main_map = Map(self,x,y,self.xtile,self.ytile,450,205)
        """
        for x in range(self.xtile): 
            for y in range(self.ytile):
                
                
                #color = "grey"
                #name = "mud"
                #path = self.get_img(name)
                xt = x_init + (x * bloc)
                yt = y_init + (y * bloc)
                #cg = Point(xt,yt,0)
                #tile = Tile(name,cg,color,path,map_pos=(x,y))
                tile = self.make_tile("mud",xt,yt,"grey")
                #tile_map[x,y] = tile
        """    
        self.make_shopitem("House_Blue","asset/ts/Factions/Knights/Buildings/House",1600,500,shop)
        self.make_shopitem("Castle_Blue","asset/ts/Factions/Knights/Buildings/Castle",1600,600,shop)
        
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