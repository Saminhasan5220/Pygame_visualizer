import sys
import math
import pygame
from serial import*
import numpy as np

#p[(i-U) % len(p)]
#p=[0, 1, 0, 0, 0]

color = (57,100,20,10)
class Arduino:
    def __init__(self,port="COM3",baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.msg = "Arduino ready"
        self.connected = False
        self.board = None
        
    def connect(self):
        try:
            msg =""
            self.board = Serial(self.port,self.baudrate)
            while msg.find(self.msg) == -1:
                while self.board.inWaiting() == 0:
                    pass
                msg = self.board.readline().decode('utf-8')
            
            self.connected =True
            self.board.flush()
            return self.connected 
        except Exception as e:
            print(e)
            return self.connected 
            
    def send(self,d):
        if type(d) != str:
            d =str(d)
        msg = d + '\n'
        msg = msg.encode('utf-8')
        self.board.write(msg)
        while(self.board.inWaiting()==0):
            pass
        data = self.board.readline().decode('utf-8').split(',')
        data[len(data) - 1] = data[len(data) - 1].rstrip()
        return data

    def disconnect(self):
        self.board.close()
        self.connected = False
  
  
        
class Compass:
    #fix color
    def __init__(self,screen,width=640,height=480):
        self.screen = screen
        self.width, self.height = width, height
        self.linewidth = 2
        self.fontsize = 20
        self.fov = 90
        self.increments = 5
        self.vlen = 18
        self.tickY = 0
        self.font = pygame.font.SysFont(None, self.fontsize)



    def transfrom(self,x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
        
        
    def nearest_multiple(self,a_number):
        return self.increments * round(a_number/self.increments)
        
    def constrain_angle(self,angle):
        if angle >= 180.0:
            angle-=360.0
        if angle <- 180.0:
            angle += 360.0
        return angle
    def rotate(self,x,y, angle):
        """Use numpy to build a rotation matrix and take the dot product."""
        #x, y = xy
        cx = self.width/2
        cy = self.height/2
        c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
        j = np.matrix([[c, s], [-s, c]])
        m = np.dot(j, [x-cx, y-cy])
        return float(m.T[0]) + cx, float(m.T[1]) + cy 
    
    def render(self,yaw  = 0,pitch = 0,roll = 0):
        start = self.nearest_multiple(yaw - (self.fov/2))
        ended = self.nearest_multiple(yaw + (self.fov/2))
        #pygame.draw.line(self.screen, (255,255,255), (self.width/2,self.tickY + self.vlen/2), (self.width/2,self.tickY + self.vlen), self.linewidth)
        for i in range(start,ended + 1,self.increments):
            tickX = self.transfrom(i,yaw - (self.fov/2),yaw + (self.fov/2),0,self.width)
            pygame.draw.line(self.screen, (127,127,127), (tickX,self.tickY), (tickX,self.vlen + self.tickY), self.linewidth)
            text = str(int(round(self.constrain_angle(i))))
            img = self.font.render(text , True, (127,127,127))
            textSize = self.font.size(text)
            self.screen.blit(img, (tickX - textSize[0]/2  , textSize[1]//2 + self.tickY + self.vlen))
        #pygame.draw.line(self.screen, (255,255,255), (0,self.height/2),(self.width,self.height/2), self.linewidth)
        self.line_segments(pitch,roll)
    
    def line_segments(self,pitch = 0,roll = 0):
        lim = 50

        start = self.nearest_multiple(pitch - (15))
        ended = self.nearest_multiple(pitch + (15))
        #pygame.draw.line(self.screen, (255,255,255), (self.width/2,self.tickY + self.vlen/2), (self.width/2,self.tickY + self.vlen), self.linewidth)
        for j in range(start,ended + 1,self.increments):
            text = str(int(round(-self.constrain_angle(j))))
            textSize = self.font.size(text)
            h = self.transfrom(j,pitch - (15),pitch + (15),lim,self.height-lim)
            half_width = self.width / 2
            quarter_width = self.width / 4
            half_quarter_width = quarter_width/8
            x0, y0 = quarter_width,h
            x1, y1 = x0 + half_quarter_width*4 ,h
            x2, y2 = x1, h - half_quarter_width * 0.5 * np.sign(j)#
            x3, y3 = half_width + half_quarter_width*4 ,h 
            x4, y4 = x3 + half_quarter_width*4  ,h
            x5, y5 = x3, h - half_quarter_width *0.5 * np.sign(j)#
            x6, y6  = x0 - textSize[0] -half_quarter_width ,h - textSize[1]//2 
            x7, y7 = x4 + textSize[0] + 0.5 *half_quarter_width ,h - textSize[1]//2 
            x0, y0 = self.rotate(x0,y0,roll)#,-half_width,h)
            x1, y1 = self.rotate(x1,y1,roll)#,-half_width,h)
            x2, y2 = self.rotate(x2,y2,roll)#,-half_width,h)
            x3, y3 = self.rotate(x3,y3,roll)#,-half_width,h)
            x4, y4 = self.rotate(x4,y4,roll)#,-half_width,h)
            x5, y5 = self.rotate(x5,y5,roll)#,-half_width,h)
            x6, y6 = self.rotate(x6,y6,roll)#,-half_width,h)
            x7, y7 = self.rotate(x7,y7,roll)#, - half_width,h)
            if (y1 and y2 and y3 and y4 and y5 and y6 and y7 > lim) and (y1 and y2 and y3 and y4 and y5 and y6 and y7 < self.height - lim):
                pygame.draw.line(self.screen, (255,255,255),(x0,y0),(x1,y1) , self.linewidth)
                pygame.draw.line(self.screen, (255,255,255),(x1,y1),(x2,y2) , self.linewidth)
                pygame.draw.line(self.screen, (255,255,255),(x3,y3),(x4,y4) , self.linewidth)
                pygame.draw.line(self.screen, (255,255,255),(x3,y3),(x5,y5) , self.linewidth)       
                img = self.font.render(text , True, (127,127,127))
                self.screen.blit(img, (x6,y6))                
                self.screen.blit(img, (x7,y7))                

class Visualizer:
    def __init__(self,width=640,height=480):
        self.Mega = Arduino()
        self.connection = self.Mega.connect()
        pygame.init()
        self.clock = clock = pygame.time.Clock()
        self.fps = 11
        self.width, self.height = width, height
        self.display = pygame.display
        self.screen = self.display.set_mode((self.width, self.height))
        self.display.set_caption('pants')
        self.icon = pygame.image.load('SPCX.ico')
        self.display.set_icon(self.icon)
        self.running = True
        self.background_colour = (0, 0, 0)
        self.debug = False
        self.compass = Compass(self.screen) 


        
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.Mega.disconnect()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.debug:
                    print(pygame.key.name(event.key),"DOWN")
                else:
                    pass
            if event.type == pygame.KEYUP:
                if self.debug:
                    print(pygame.key.name(event.key),"UP")
                else:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.debug:
                    print(event.pos,event.button)
                else:
                    pass
            if event.type == pygame.MOUSEBUTTONUP:
                if self.debug:
                    print(event.pos,event.button)
                else:
                    pass
            if event.type == pygame.MOUSEMOTION:    
                self.mouseX = event.pos[0]
                self.mouseY = event.pos[1]          
                if self.debug:
                    print(event.pos,event.rel,event.buttons)

                else:
                    pass

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(self.background_colour)
            #color = (255,255,255)
            center = self.mouseX,self.mouseY
            radius = 10 
            angle = self.Mega.send(0)
            self.compass.render(float(angle[2]),-float(angle[0]),float(angle[1]))
            #pygame.draw.circle(self.screen, color, center, radius) 
            self.display.flip()# UPDATE ENTIRE SCREEN
            self.clock.tick(self.fps)
            print(center,end='\r')
            #print("Attitude:",angle,"FPS:",int(round(self.clock.get_fps())),end="\r")
     

     
V = Visualizer()          
V.run()















































''' 
pygame.init()
clock = pygame.time.Clock()
(width, height) = (640, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GUI')
programIcon = pygame.image.load('SPCX.ico')
pygame.display.set_icon(programIcon)

running = True
while running:
    background_colour = (0,0,0)
    screen.fill(background_colour)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key),"DOWN")
        if event.type == pygame.KEYUP:
            print(pygame.key.name(event.key),"UP")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos,event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos,event.button)
        if event.type == pygame.MOUSEMOTION:
            print(event.pos,event.rel,event.buttons)
    clock.tick(60) 
pygame.quit()
sys.exit()
'''
