import pygame
import sys
import random
import heapq
import os

HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0


def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Initialize Pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)  # Or any other font/size you like

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (30, 30, 30)  # Dark gray background
CELL_SIZE = 20
CELLS_X, CELLS_Y = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
is_ai = False  # Set to True to enable AI mode

class Food:
    def __init__(self, snake):
        self.x, self.y = 0, 0
        self.generate_food(snake)

    def generate_food(self, snake):
        while True:
            self.x = random.randint(0, CELLS_X - 1)
            self.y = random.randint(0, CELLS_Y - 1)

            if [self.x, self.y] != snake.head and [self.x, self.y] not in snake.body:
                break

    def draw(self, surface):
        color = (100, 0, 0)
        border_color = (255, 255, 255)
        center = (self.x * CELL_SIZE + CELL_SIZE // 2,
                  self.y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(surface, border_color, center,
                           CELL_SIZE // 2, width=0)
        pygame.draw.circle(surface, color, center, CELL_SIZE // 2 - 1, width=0)


class Snake:
    def __init__(self):
        self.head = [CELLS_X // 2, CELLS_Y // 2]
        self.body = [
            [self.head[0] - 1, self.head[1]],
            [self.head[0] - 2, self.head[1]]
        ]
        self.direction = (1, 0)  # default moving right
        self.moves = []
        self.score = 0

    def draw(self, screen):
        rect = pygame.Rect(
            self.head[0] * CELL_SIZE + 2,
            self.head[1] * CELL_SIZE + 2,
            CELL_SIZE - 2,
            CELL_SIZE - 2
        )
        border_rect = pygame.Rect(
            self.head[0] * CELL_SIZE,
            self.head[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        color = (255, 0, 0)
        border_color = (255, 255, 255)
        pygame.draw.rect(screen, border_color, border_rect, border_radius=2)
        pygame.draw.rect(screen, color, rect, border_radius=2)

        colors = [(0, 255, 0), (34, 139, 34), (0, 100, 0)]
        for i, part in enumerate(self.body):
            rect = pygame.Rect(
                part[0] * CELL_SIZE + 2,
                part[1] * CELL_SIZE + 2,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            )
            border_rect = pygame.Rect(
                part[0] * CELL_SIZE,
                part[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = colors[i % len(colors)]
            border_color = (255, 255, 255)

            pygame.draw.rect(screen, border_color,
                             border_rect, border_radius=2)
            pygame.draw.rect(screen, color, rect, border_radius=2)

    def update(self):
        if self.moves:  # Only pop if there's a new direction
            next_dir = self.moves.pop(0)  # Get the next direction

            # Prevent reversing
            if (next_dir[0] != -self.direction[0] or next_dir[1] != -self.direction[1]):
                self.direction = next_dir  # Only change direction if not reversing
        dx, dy = self.direction

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0], self.body[i][1] = self.body[i -
                                                         1][0], self.body[i - 1][1]

        self.body[0][0], self.body[0][1] = self.head[0], self.head[1]
        self.head[0] = (self.head[0] + dx) % CELLS_X
        self.head[1] = (self.head[1] + dy) % CELLS_Y

    def detect_collision(self, food):
        if self.head == [food.x, food.y]:
            self.score += 1
            self.body.append(self.body[-1][:])
            food.generate_food(self)
        elif self.head in self.body:
            return False

        return True

    def decide_move_simple(self, food):
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def is_safe(move):
            new_head = [
                (self.head[0] + move[0]) % CELLS_X,
                (self.head[1] + move[1]) % CELLS_Y
            ]
            return new_head not in self.body

        # Sort moves by Manhattan distance to food
        possible_moves.sort(key=lambda m: abs(
            (self.head[0] + m[0]) - food.x) + abs((self.head[1] + m[1]) - food.y))

        for move in possible_moves:
            if is_safe(move):
                return move

        # If all moves are bad, YOLO into death
        return self.direction

    def decide_move_smarter(self, food):
        def get_neighbors(pos):
            x, y = pos
            neighbors = [
                ((x - 1) % CELLS_X, y),
                ((x + 1) % CELLS_X, y),
                (x, (y - 1) % CELLS_Y),
                (x, (y + 1) % CELLS_Y),
            ]
            return [n for n in neighbors if list(n) not in self.body]

        def heuristic(a, b):
            # Manhattan distance with wrap-around considered
            dx = min(abs(a[0] - b[0]), CELLS_X - abs(a[0] - b[0]))
            dy = min(abs(a[1] - b[1]), CELLS_Y - abs(a[1] - b[1]))
            return dx + dy

        start = tuple(self.head)
        goal = (food.x, food.y)

        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
        came_from = {}
        g_score = {start: 0}
        visited = set()

        while open_set:
            _, cost, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                if path:
                    dx = path[0][0] - self.head[0]
                    dy = path[0][1] - self.head[1]

                    # handle wrap-around
                    if dx > 1:
                        dx = -1
                    elif dx < -1:
                        dx = 1
                    if dy > 1:
                        dy = -1
                    elif dy < -1:
                        dy = 1

                    return (dx, dy)

            visited.add(current)

            for neighbor in get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))

        # No path found — fallback to not crashing
        return self.direction


def start_menu(screen):
    global is_ai
    waiting = True
    while waiting:
        screen.fill(BG_COLOR)

        title_text = FONT.render(
            "Choose Mode: 1 - Human | 2 - AI", True, (255, 255, 255))
        shadow = FONT.render(
            "Choose Mode: 1 - Human | 2 - AI", True, (0, 0, 0))

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))

        screen.blit(shadow, shadow_rect)
        screen.blit(title_text, title_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    is_ai = False
                    waiting = False
                elif event.key == pygame.K_2:
                    is_ai = True
                    waiting = False


def main():
    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    start_menu(screen)
    print()

    # Clock to control frame rate
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake)

    high_score = load_high_score()

    move_delay = max(10, 150 - len(snake.body) * 2)
    last_move_time = pygame.time.get_ticks()

    # Main game loop
    running = True
    while running:
        clock.tick(FPS)  # Limit FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not is_ai:
                    if event.key == pygame.K_w:
                        snake.moves.append((0, -1))
                    elif event.key == pygame.K_s:
                        snake.moves.append((0, 1))
                    elif event.key == pygame.K_a:
                        snake.moves.append((-1, 0))
                    elif event.key == pygame.K_d:
                        snake.moves.append((1, 0))

        # Game logic goes here
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_delay:
            if is_ai and not snake.moves:
                next_move = snake.decide_move_smarter(food)
                snake.moves.append(next_move)
            snake.update()
            last_move_time = current_time

            if snake.detect_collision(food):
                move_delay = max(40, int(200 * (0.90 ** len(snake.body))))
            else:
                print("Snake died!")
                print("Final Score: ", snake.score)
                if snake.score > high_score:
                    print("🎉 NEW HIGH SCORE! 🎉")
                    high_score = snake.score
                    save_high_score(high_score)
                running = False

        # Drawing goes here
        screen.fill(BG_COLOR)
        food.draw(screen)
        snake.draw(screen)

        score_text = FONT.render(
            f"Score: {snake.score}", True, (255, 255, 255))
        shadow = FONT.render(f"Score: {snake.score}", True, (0, 0, 0))

        text_rect = score_text.get_rect(center=(WIDTH // 2, 20))
        shadow_rect = score_text.get_rect(
            center=(WIDTH // 2 + 1, 20 + 1))
        
        screen.blit(score_text, text_rect)
        screen.blit(shadow, shadow_rect)

        high_text = FONT.render(
            f"High Score: {high_score}", True, (255, 215, 0))  # Gold color
        high_shadow = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))

        high_rect = high_text.get_rect(center=(WIDTH // 2, 50))
        high_shadow_rect = high_text.get_rect(center=(WIDTH // 2 + 1, 50 + 1))

        screen.blit(high_text, high_rect)
        screen.blit(high_shadow, high_shadow_rect)


        # Write human or ai at top right corner of screen
        mode_text = FONT.render(
            "Mode: AI" if is_ai else "Mode: Human", True, (255, 255, 255))
        mode_shadow = FONT.render(
            "Mode: AI" if is_ai else "Mode: Human", True, (0, 0, 0))
        
        mode_rect = mode_text.get_rect(topright=(WIDTH - 20, 20))
        mode_shadow_rect = mode_shadow.get_rect(
            topright=(WIDTH - 20 + 1, 20 + 1))
        
        screen.blit(mode_text, mode_rect)
        screen.blit(mode_shadow, mode_shadow_rect)


        # Update display
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
