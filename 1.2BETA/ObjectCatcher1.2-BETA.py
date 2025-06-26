import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

BACKGROUND_COLOR = (20, 20, 30)
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 36)

# Traduzioni
translations = {
    "it": {"game_over": "Game Over", "score": "Punteggio", "retry": "Premi SPAZIO per rigiocare", "quit": "Premi ESC per uscire", "lives": "Vite"},
    "en": {"game_over": "Game Over", "score": "Score", "retry": "Press SPACE to retry", "quit": "Press ESC to quit", "lives": "Lives"},
    "uk": {"game_over": "Гру завершено", "score": "Рахунок", "retry": "Натисни ПРОБІЛ, щоб спробувати знову", "quit": "Натисни ESC, щоб вийти", "lives": "Життя"},
    "es": {"game_over": "Juego terminado", "score": "Puntuación", "retry": "Presiona ESPACIO para volver a jugar", "quit": "Presiona ESC para salir", "lives": "Vidas"},
    "de": {"game_over": "Spiel vorbei", "score": "Punktzahl", "retry": "Drücke LEERTASTE zum Neustart", "quit": "Drücke ESC zum Beenden", "lives": "Leben"},
}

# Limiti velocità caduta
falling_speed_limit = 11
falling_speed_limit_min = 5
falling_speed_limit_max = 20

# Disegna testo centrato
def draw_text_centered(text, y, color=(255, 255, 255)):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def draw_hearts(lives):
    heart = "❤"
    for i in range(lives):
        heart_text = font.render(heart, True, (255, 0, 0))
        screen.blit(heart_text, (WIDTH - 40 * (i + 1), 10))

def select_language():
    languages = [("Italiano", "it"), ("English", "en"), ("Українська", "uk"), ("Español", "es"), ("Deutsch", "de")]
    selected = 1
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered("Select Language", 80, (200, 200, 0))
        for i, (name, _) in enumerate(languages):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            draw_text_centered(name, 160 + i * 50, color)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(languages)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(languages)
                elif event.key == pygame.K_RETURN:
                    return languages[selected][1]

def select_lives(texts):
    options = [("Hard (1)", 1), ("Normal (3)", 3), ("Easy (5)", 5)]
    selected = 1
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered("Select Difficulty", 80, (200, 200, 0))
        for i, (label, _) in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            draw_text_centered(label, 160 + i * 50, color)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected][1]

def pause_menu():
    options = ["Resume", "Change Language", "Change Difficulty"]
    selected = 0
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered("Paused", 80, (255, 255, 0))
        for i, text in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            draw_text_centered(text, 160 + i * 50, color)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower().replace(" ", "_")

def game_loop(texts, initial_lives):
    global falling_speed_limit

    player_w, player_h = 40, 40
    player_x = WIDTH // 2 - player_w // 2
    player_y = HEIGHT - 2 * player_h
    player_speed = 5

    falling_w, falling_h = 40, 40
    falling_x, falling_y = 0, 0
    falling_speed = 4
    block_type = "normal"

    score = 0
    lives = initial_lives

    def spawn_block():
        nonlocal falling_x, falling_y, block_type
        falling_x = random.randint(0, WIDTH - falling_w)
        falling_y = -falling_h
        rand = random.random()
        if rand < 0.9:
            block_type = "normal"
        elif rand < 0.95:
            block_type = "slowdown"
        else:
            block_type = "speedup"

    spawn_block()
    paused = False

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = pause_menu()
                    if choice == "resume":
                        continue
                    elif choice == "change_language":
                        return "language"
                    elif choice == "change_difficulty":
                        return "difficulty"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_x -= player_speed
        if keys[pygame.K_RIGHT]: player_x += player_speed
        player_x = max(0, min(WIDTH - player_w, player_x))

        falling_y += falling_speed

        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        falling_rect = pygame.Rect(falling_x, falling_y, falling_w, falling_h)

        if player_rect.colliderect(falling_rect):
            if block_type == "normal":
                score += 1
                if score % 5 == 0 and falling_speed < falling_speed_limit:
                    falling_speed += 1
                    if score % 10 == 0:
                        player_speed += 1
            elif block_type == "slowdown":
                falling_speed_limit = max(falling_speed_limit_min, falling_speed_limit - 1)
            elif block_type == "speedup":
                falling_speed_limit = min(falling_speed_limit_max, falling_speed_limit + 1)
            spawn_block()

        elif falling_y > HEIGHT:
            if block_type == "normal":
                lives -= 1
                if lives <= 0:
                    return show_game_over(score, texts)
            spawn_block()

        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_w, player_h))
        color = (255, 0, 0) if block_type == "normal" else (128, 0, 255) if block_type == "slowdown" else (255, 165, 0)
        pygame.draw.rect(screen, color, (falling_x, falling_y, falling_w, falling_h))

        score_text = font.render(f"{texts['score']}: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        draw_hearts(lives)

        pygame.display.flip()
        clock.tick(FPS)

def show_game_over(score, texts):
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered(texts["game_over"], HEIGHT // 2 - 60, (255, 0, 0))
        draw_text_centered(f"{texts['score']}: {score}", HEIGHT // 2 - 10)
        draw_text_centered(texts["retry"], HEIGHT // 2 + 40)
        draw_text_centered(texts["quit"], HEIGHT // 2 + 80)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():
    lang = select_language()
    texts = translations[lang]
    lives = select_lives(texts)
    while True:
        result = game_loop(texts, lives)
        if result == "language":
            lang = select_language()
            texts = translations[lang]
        elif result == "difficulty":
            lives = select_lives(texts)
        else:
            break

main()
