import random
import sys
import pygame

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60
ROAD_LEFT = 50
ROAD_RIGHT = 350
CAR_WIDTH = 40
CAR_HEIGHT = 80
PLAYER_START_X = 180
PLAYER_START_Y = 500
PLAYER_SPEED = 10
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_TIME = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD_COLOR = (65, 65, 65)
ROAD_EDGE_COLOR = (230, 230, 230)
YELLOW = (255, 220, 0)
BLUE = (40, 120, 230)
RED = (220, 45, 45)
GREEN = (40, 150, 70)

class Car:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, CAR_WIDTH, CAR_HEIGHT)
        self.color = color

    def draw(self, screen):

        pygame.draw.rect(
            screen, self.color, self.rect, border_radius=7
        )

        # Front and rear windows
        front_window = pygame.Rect(
            self.rect.x + 7, self.rect.y + 12, 26, 20
        )
        rear_window = pygame.Rect(
            self.rect.x + 7, self.rect.y + 48, 26, 15
        )

        pygame.draw.rect(
            screen, (180, 220, 240), front_window, border_radius=4
        )
        pygame.draw.rect(
            screen, (180, 220, 240), rear_window, border_radius=4
        )

        # Wheels
        for wheel_y in (self.rect.y + 13, self.rect.y + 50):
            pygame.draw.rect(
                screen, BLACK,
                (self.rect.x - 2, wheel_y, 5, 18),
                border_radius=2
            )
            pygame.draw.rect(
                screen, BLACK,
                (self.rect.right - 3, wheel_y, 5, 18),
                border_radius=2
            )

class Obstacle:

    def __init__(self, x, y=0):
        self.car = Car(x, y, RED)
        self.speed = OBSTACLE_SPEED
        self.passed = False



    @property
    def rect(self):
        return self.car.rect

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        self.car.draw(screen)

class CarRacingGame:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Racing Game - PS No. 42")

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("arial", 30, bold=True)
        self.info_font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)

        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, OBSTACLE_SPAWN_TIME)

        self.reset()

    def reset(self):
        self.player = (
            PLAYER_START_X, PLAYER_START_Y, BLUE
        )
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.road_line_offset = 0

    def spawn_obstacle(self):
    
        obstacle_x = random.randint(
            ROAD_LEFT, ROAD_RIGHT - CAR_WIDTH
        )
        self.obstacles.append(Obstacle(obstacle_x))

    def handle_key(self, key):

        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return

        if key == pygame.K_LEFT:
            self.player.rect.x = max(
                ROAD_LEFT,
                self.player.rect.x - PLAYER_SPEED
            )

        elif key == pygame.K_RIGHT:
            self.player.rect.x = min(
                ROAD_RIGHT - CAR_WIDTH,
                self.player.rect.x + PLAYER_SPEED
            )

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self.handle_key(event.key)

            if (
                event.type == self.spawn_event
                and not self.game_over
            ):
                self.spawn_obstacle()

        return True

    def update(self):
    
        if self.game_over:
            return

        for obstacle in self.obstacles:
            obstacle.update()

            # Add one point when an obstacle completely passes the screen.
            if (
                not obstacle.passed
                and obstacle.rect.top > WINDOW_HEIGHT
            ):
                obstacle.passed = True
                self.score += 1

            # Check collision between player and obstacle.
            if self.player.rect.colliderect(obstacle.rect):
                self.game_over = True
                break

        # Remove obstacles that have passed the screen.
        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if obstacle.rect.top <= WINDOW_HEIGHT
        ]

        self.road_line_offset = (
            self.road_line_offset + OBSTACLE_SPEED
        ) % 60

    def draw_road(self):
    
        self.screen.fill(GREEN)

        pygame.draw.rect(
            self.screen,
            ROAD_COLOR,
            (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, WINDOW_HEIGHT)
        )

        pygame.draw.line(
            self.screen, ROAD_EDGE_COLOR,
            (ROAD_LEFT, 0), (ROAD_LEFT, WINDOW_HEIGHT), 4
        )
        pygame.draw.line(
            self.screen, ROAD_EDGE_COLOR,
            (ROAD_RIGHT, 0), (ROAD_RIGHT, WINDOW_HEIGHT), 4
        )

        dash_y = -60 + self.road_line_offset

        while dash_y < WINDOW_HEIGHT:
            pygame.draw.rect(
                self.screen,
                YELLOW,
                (198, dash_y, 4, 30)
            )
            dash_y += 60

    def draw_score(self):
    
        score_text = self.info_font.render(
            f"Score: {self.score}", True, WHITE
        )
        self.screen.blit(score_text, (10, 10))

        control_text = self.small_font.render(
            "Use LEFT / RIGHT arrows to move", True, WHITE
        )
        self.screen.blit(control_text, (10, 38))

    def draw_game_over(self):
    
        overlay = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render(
            "GAME OVER", True, WHITE
        )
        final_score_text = self.info_font.render(
            f"Final Score: {self.score}", True, WHITE
        )
        restart_text = self.small_font.render(
            "Press R to restart", True, WHITE
        )

        self.screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(WINDOW_WIDTH // 2, 245)
            )
        )
        self.screen.blit(
            final_score_text,
            final_score_text.get_rect(
                center=(WINDOW_WIDTH // 2, 295)
            )
        )
        self.screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, 335)
            )
        )

    def draw(self):

        self.draw_road()

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.player.draw(self.screen)
        self.draw_score()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
    
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    game = CarRacingGame()
    game.run()


if __name__ == "__main__":
    main()