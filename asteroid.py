from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        self.x
        self.y
        self.radius
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt