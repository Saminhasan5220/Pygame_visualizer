import sys
import math
import pygame
class Visualizer:
    def __init__(self,width=640,height=480):
        self.mouseX,self.mouseY = 0,0
        pygame.init()
        pygame.joystick.init()
        self.clock = clock = pygame.time.Clock()
        self.fps = 61
        self.width, self.height = width, height
        self.display = pygame.display
        self.screen = self.display.set_mode((self.width, self.height))
        self.display.set_caption('Visualizer_pygame')
        self.icon = pygame.image.load('SPCX.ico')
        self.display.set_icon(self.icon)
        self.running = True
        self.background_colour = (127,127,127)
        self.debug = True
        self.joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick_init = [self.joystick[x].init() for x in range(pygame.joystick.get_count())]
        self.joystick_name = [self.joystick[x].get_name() for x in range(pygame.joystick.get_count())]
        #self.joystick = pygame.joystick.Joystick(1)
        #self.joystick_name = self.joystick.get_name()
        self.joystick_ids = [self.joystick[x].get_id() for x in range(pygame.joystick.get_count())]
        self.axes = [self.joystick[x].get_numaxes() for x in range(pygame.joystick.get_count())]
        self.buttons = [self.joystick[x].get_numbuttons() for x in range(pygame.joystick.get_count())]
        self.hats = [self.joystick[x].get_numhats() for x in range(pygame.joystick.get_count())]
        self.numballs = [self.joystick[x].get_numballs() for x in range(pygame.joystick.get_count())]


        if self.debug:
            print(self.joystick)
            print(self.joystick_name)


        
        
    def handle_events(self):
        #JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.joystick.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.debug:
                    print(pygame.key.name(event.key),"DOWN")
            elif event.type == pygame.KEYUP:
                if self.debug:
                    print(pygame.key.name(event.key),"UP")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.debug:
                    print(event.pos,event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.debug:
                    print(event.pos,event.button)

            elif event.type == pygame.MOUSEMOTION:  
                self.mouseX = event.pos[0]
                self.mouseY = event.pos[1]          
                if self.debug:
                    print(event.pos,event.rel,event.buttons)

            elif event.type == pygame.JOYAXISMOTION:
                if self.debug:
                    print(event.joy, "---", event.axis, "---", event.value)
            #elif event.type == pygame.JOYBALLMOTION:
            #    if self.debug:
            #        print(event.joy, event.ball, event.rel)
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.debug:
                    print(event.joy, "---", event.button)
                    print(pygame.key.name(event.button),"DOWN")

            elif event.type == pygame.JOYBUTTONUP:
                if self.debug:
                    print(event.joy,"---",event.button)
                    print(pygame.key.name(event.button),"UP")

            elif event.type == pygame.JOYHATMOTION:
                if self.debug:
                    print(event.joy, "---", event.hat, "---", event.value)



    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(self.background_colour)

            #self.display.update()#UPDATE WHOLE SCREEN,IF NO ARGUMENTS GIVEN SAME AS FLIP
            self.display.flip()# UPDATE ENTIRE SCREEN
            self.clock.tick(self.fps)
            print("FPS:",int(round(self.clock.get_fps())),end="\r")
            
            
V = Visualizer()
V.run()