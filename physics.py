import pygame

GRAVITY = 600



pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

    

p_pos = pygame.Vector2((screen.get_width() / 2), screen.get_height() / 2)
player = pygame.Rect(0, 0, 100, 25)
player.center = p_pos
p_rad = 20
p_vel = pygame.Vector2(0,0)

    

f_width, f_height = 400, 75
floor = pygame.Rect((screen.get_width()/2) - (f_width/2), screen.get_height()-(f_height*2), f_width, f_height)
dt = 0
while running:
    
    # Close Window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    
    
    # Gravity
    p_vel.y += GRAVITY * dt
    
    if floor.colliderect(player):
        p_pos.y = floor.top - player.height/2
        p_vel.y = 0
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        p_vel.y = -200
    
    if keys[pygame.K_r]:
        p_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    if keys[pygame.K_LEFT]:
        p_vel.x = -200
    elif keys[pygame.K_RIGHT]:
        p_vel.x = 200
    else:
        p_vel.x = 0
    
    
    
        
    p_pos.x += p_vel.x * dt
    p_pos.y += p_vel.y * dt
    player.center = p_pos
    
    
    # Draw to the screen
    screen.fill("white")
    pygame.draw.rect(screen, "red", player)
    pygame.draw.rect(screen, "black", floor)
    pygame.display.flip() #render
    
    
    
    
    
   
    
    
    
    

    dt = clock.tick(30) / 1000
    
    
pygame.quit()