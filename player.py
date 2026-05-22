import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_SHOOT_SPEED
import math

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        #if keys[pygame.K_a]:
            #self.rotate(-dt)
        #if keys[pygame.K_d]:
            #self.rotate(dt)

        #experimental mouse turning logic below
        # 1. Get mouse position
        m_x, m_y = pygame.mouse.get_pos()

        # 2(oldmethod). Find difference from center
        #center_x = SCREEN_WIDTH / 2
        #center_y = SCREEN_HEIGHT / 2
        #dx = m_x - center_x
        #dy = m_y - center_y

        # 2 using current player position to calculate the difference
        current_x = self.position.x
        current_y = self.position.y
        dx = m_x - current_x
        dy = m_y - current_y

        # 3. Calculate the angle in degrees
        # We use -dy because Pygame's Y axis is inverted
        target_angle = math.degrees(math.atan2(-dy, dx))


        # 4. Set rotation: "-" is added to make the ship move the same angle as the mouse. -90 aligns the ship with the mouse
        self.rotation = -target_angle - 90

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()


    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector


    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        
