import pygame
import math
pygame.init()

WIDTH, HEIGHT=800,800

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('solar system simulation')

WHITE=(255,255,255)
YELLOW = (255,255,0)
BLUE=(100,149,237)
RED=(188,29,50)
DARK_GREY=(80,78,81)
BROWN=(139,69,19)

class Planet:
    AU=149.6e6*1000
    G=6.67428e-11
    SCALE=200/AU # 1AU = 100 pix
    TIMESTEP = 3600*24
    
    def __init__(self,x,y,radius,color,mass):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.mass=mass
        
        self.sun=False
        self.dist_to_sun=0
        self.orbit=[]
        
        self.x_vel=0
        self.y_vel=0
        
    def draw(self,win):
        x=self.x*self.SCALE+WIDTH/2
        y=self.y*self.SCALE+HEIGHT/2
        if len(self.orbit)>2:
            updated_points=[]
            for point in self.orbit:
                x,y=point
                x=x*self.SCALE+WIDTH/2
                y=y*self.SCALE+HEIGHT/2
                updated_points.append((x,y))
            #pygame.draw.lines(win,WHITE,False,updated_points, 1)
        pygame.draw.circle(win, self.color, (x,y), self.radius)

    def attraction(self,other):
        other_x,other_y=other.x,other.y
        distance_x=other_x-self.x
        distance_y=other_y-self.y
        distance = math.sqrt(distance_x**2+distance_y**2)
        
        if other.sun:
            self.dist_to_sun=distance
            
        force=self.G*self.mass*other.mass/distance**2
        theta = math.atan2(distance_y,distance_x)
        force_x=math.cos(theta)*force
        force_y=math.sin(theta)*force
        return force_x,force_y
    
    def update_pos(self,planets):
        total_fx=total_fy=0
        for planet in planets:
            if self==planet:
                continue
            fx,fy=self.attraction(planet)
            total_fx+=fx
            total_fy+=fy
            
        self.x_vel+=total_fx/self.mass*self.TIMESTEP
        self.y_vel+=total_fy/self.mass*self.TIMESTEP
        
        self.x+=self.x_vel*self.TIMESTEP
        self.y+=self.y_vel*self.TIMESTEP
        self.orbit.append((self.x,self.y))
    
def main():
    run =True
    clock=pygame.time.Clock()
    
    sun=Planet(0,0,30,YELLOW,1.98892*10**30)
    sun.sun=True
    
    earth=Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel=29.783*1000
    mars=Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel=24.077*1000
    mercury=Planet(0.387*Planet.AU, 0, 8,DARK_GREY, 3.30*10**23)
    mercury.y_vel=-47.4*1000
    venus=Planet(0.723*Planet.AU, 0, 14,WHITE,4.86*10**24)
    venus.y_vel=-35.02*1000
    planets=[sun,earth,mars,venus,mercury]
    
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                
        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)
            
        pygame.display.update()
                
    pygame.quit()
    
main()