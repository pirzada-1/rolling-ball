import pygame
import math
import sys

# Constants for simulation
WIDTH, HEIGHT = 800, 600
HEX_SIDE_LENGTH = 200
BALL_RADIUS = 20
GRAVITY = 0.5
AIR_RESISTANCE = 0.02
DAMPING = 0.8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rolling Ball in a Hexagon")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0

    def update(self, dt):
        # Apply gravity and air resistance
        self.vy += GRAVITY * dt
        self.vx *= (1 - AIR_RESISTANCE * dt)  # More accurate air resistance
        self.vy *= (1 - AIR_RESISTANCE * dt)  # More accurate air resistance

        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def create_hexagon(center_x, center_y, side_length):
    """Generate the vertices of a hexagon centered at (center_x, center_y)."""
    vertices = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center_x + side_length * math.cos(angle_rad)
        y = center_y + side_length * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices

def distance(point1, point2):
    """Calculate the distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def closest_point_on_line(A, B, P):
    """Find the closest point on the line segment AB to point P."""
    AP = (P[0] - A[0], P[1] - A[1])
    AB = (B[0] - A[0], B[1] - A[1])
    ab2 = AB[0]**2 + AB[1]**2
    ap_ab = AP[0] * AB[0] + AP[1] * AB[1]
    t = ap_ab / ab2
    t = max(0, min(1, t))
    return (A[0] + AB[0] * t, A[1] + AB[1] * t)

def check_collision(ball, hexagon_vertices):
    """Check for collisions between the ball and the hexagon's edges."""
    for i in range(len(hexagon_vertices)):
        A = hexagon_vertices[i]
        B = hexagon_vertices[(i + 1) % len(hexagon_vertices)]
        closest = closest_point_on_line(A, B, (ball.x, ball.y))
        if distance((ball.x, ball.y), closest) <= ball.radius:
            # Calculate the normal vector of the edge
            edge = (B[0] - A[0], B[1] - A[1])
            normal = (-edge[1], edge[0])
            norm_magnitude = math.sqrt(normal[0]**2 + normal[1]**2)
            normal = (normal[0] / norm_magnitude, normal[1] / norm_magnitude)

            # Reflect the velocity vector
            dot_product = ball.vx * normal[0] + ball.vy * normal[1]
            ball.vx -= 2 * dot_product * normal[0] * DAMPING
            ball.vy -= 2 * dot_product * normal[1] * DAMPING

            # Move the ball out of collision
            overlap = ball.radius - distance((ball.x, ball.y), closest)
            ball.x += overlap * normal[0]
            ball.y += overlap * normal[1]

def main():
    # Create the hexagon
    hexagon_vertices = create_hexagon(WIDTH // 2, HEIGHT // 2, HEX_SIDE_LENGTH)

    # Create the ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Main loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Convert to seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ball physics
        ball.update(dt)

        # Check for collisions
        check_collision(ball, hexagon_vertices)

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)
        ball.draw()

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()