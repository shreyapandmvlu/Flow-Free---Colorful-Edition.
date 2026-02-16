import pygame
import sys

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 580
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flow Free – Colorful Edition ✨")

# ---------------- COLORS ----------------
BG_TOP = (15, 15, 25)
BG_BOTTOM = (40, 40, 60)
GRID_COLOR = (80, 80, 110)

RED = (255, 80, 80)
BLUE = (80, 140, 255)
GREEN = (80, 220, 150)
YELLOW = (255, 230, 120)
ORANGE = (255, 160, 80)

COLORS = [RED, BLUE, GREEN, YELLOW, ORANGE]
WHITE = (240, 240, 240)

# ---------------- GRID ----------------
ROWS = COLS = 5
CELL = 80
OFFSET_Y = 60

font = pygame.font.SysFont("arial", 22)
bigfont = pygame.font.SysFont("arial", 40)

# ---------------- GAME STATES ----------------
start_screen = True
game_over = False

# ---------------- LEVEL ----------------
points = {
    RED: [(0, 0), (0, 4)],
    BLUE: [(1, 1), (3, 1)],
    GREEN: [(1, 4), (3, 3)],
    ORANGE: [(4, 0), (2, 3)],
    YELLOW: [(4, 4), (3, 4)]
}

paths = {}
current_color = None
current_path = []

def reset_game():
    global paths, current_color, current_path, game_over
    paths = {}
    current_color = None
    current_path = []
    game_over = False

# ---------------- BACKGROUND ----------------
def draw_gradient():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL, r * CELL + OFFSET_Y, CELL, CELL)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1, border_radius=8)

def draw_points():
    for color, pts in points.items():
        for r, c in pts:
            x = c * CELL + CELL // 2
            y = r * CELL + CELL // 2 + OFFSET_Y
            pygame.draw.circle(screen, color, (x, y), 20)
            pygame.draw.circle(screen, WHITE, (x, y), 8)

def draw_paths():
    for color, path in paths.items():
        if len(path) > 1:
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]

                x1 = c1 * CELL + CELL // 2
                y1 = r1 * CELL + CELL // 2 + OFFSET_Y
                x2 = c2 * CELL + CELL // 2
                y2 = r2 * CELL + CELL // 2 + OFFSET_Y

                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 14)

def check_win():
    return len(paths) == len(points)

# ---------------- MAIN LOOP ----------------
running = True
while running:

    # -------- START SCREEN --------
    if start_screen:
        draw_gradient()
        title = bigfont.render("FLOW FREE ✨", True, WHITE)
        msg = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title, (WIDTH//2 - 130, 220))
        screen.blit(msg, (WIDTH//2 - 120, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen = False
                    reset_game()
        continue

    draw_gradient()
    title = font.render("Flow Free Puzzle ✨", True, WHITE)
    screen.blit(title, (WIDTH // 2 - 90, 20))

    draw_grid()
    draw_paths()
    draw_points()

    if current_color:
        pygame.draw.rect(screen, current_color, (0, OFFSET_Y, WIDTH, HEIGHT - OFFSET_Y), 2)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            row = (my - OFFSET_Y) // CELL
            col = mx // CELL

            for color, pts in points.items():
                if (row, col) in pts:
                    current_color = color
                    current_path = [(row, col)]

        if event.type == pygame.MOUSEMOTION and current_color:
            mx, my = event.pos
            row = (my - OFFSET_Y) // CELL
            col = mx // CELL

            if 0 <= row < ROWS and 0 <= col < COLS:
                if (row, col) not in current_path:
                    lr, lc = current_path[-1]
                    if abs(lr - row) + abs(lc - col) == 1:
                        current_path.append((row, col))

        if event.type == pygame.MOUSEBUTTONUP:
            if current_color:
                if current_path[-1] in points[current_color]:
                    paths[current_color] = current_path
                current_color = None
                current_path = []

    # -------- CHECK WIN --------
    if check_win():
        game_over = True
        win_text = bigfont.render("YOU WIN! 🎉", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(win_text, (WIDTH//2 - 120, 250))
        screen.blit(restart_text, (WIDTH//2 - 120, 320))

    pygame.display.update()

pygame.quit()
sys.exit()
