import pygame
import sys
import random

# Inizializza Pygame
pygame.init()

# Dimensioni della finestra
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

# Colore di sfondo
BACKGROUND_COLOR = (20, 20, 30)

# Imposta il tempo di frame
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 36)

# Traduzioni
translations = {
    "it": {
        "game_over": "Game Over",
        "score": "Punteggio",
        "retry": "Premi SPAZIO per rigiocare",
        "quit": "Premi ESC per uscire"
    },
    "en": {
        "game_over": "Game Over",
        "score": "Score",
        "retry": "Press SPACE to retry",
        "quit": "Press ESC to quit"
    },
    "uk": {
        "game_over": "Гру завершено",
        "score": "Рахунок",
        "retry": "Натисни ПРОБІЛ, щоб спробувати знову",
        "quit": "Натисни ESC, щоб вийти"
    },
    "es": {
        "game_over": "Juego terminado",
        "score": "Puntuación",
        "retry": "Presiona ESPACIO para volver a jugar",
        "quit": "Presiona ESC para salir"
    },
    "de": {
        "game_over": "Spiel vorbei",
        "score": "Punktzahl",
        "retry": "Drücke LEERTASTE zum Neustart",
        "quit": "Drücke ESC zum Beenden"
    },
}

# Disegna testo centrato
def draw_text_centered(text, y, color=(255, 255, 255)):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

# Menu per selezionare la lingua
def select_language():
    languages = [("Italiano", "it"), ("English", "en"), ("Українська", "uk"), ("Español", "es"), ("Deutsch", "de")]
    selected = 1  # English default

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered("Select Language", 80, (200, 200, 0))

        for i, (name, code) in enumerate(languages):
            color = (255, 255, 255)
            if i == selected:
                color = (0, 255, 0)
            draw_text_centered(name, 160 + i * 50, color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(languages)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(languages)
                elif event.key == pygame.K_RETURN:
                    return languages[selected][1]  # Codice lingua

# Loop principale del gioco
def game_loop(texts):
    player_width, player_height = 40, 40
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 2 * player_height
    player_speed = 5

    falling_width, falling_height = 40, 40
    falling_x = random.randint(0, WIDTH - falling_width)
    falling_y = -falling_height
    falling_speed = 4

    score = 0

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        player_x = max(0, min(WIDTH - player_width, player_x))

        falling_y += falling_speed

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        falling_rect = pygame.Rect(falling_x, falling_y, falling_width, falling_height)

        if player_rect.colliderect(falling_rect):
            score += 1
            falling_y = -falling_height
            falling_x = random.randint(0, WIDTH - falling_width)
            if score % 5 == 0 and falling_speed < 9:
                falling_speed += 1

        if falling_y > HEIGHT:
            return show_game_over(score, texts)

        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, (255, 0, 0), (falling_x, falling_y, falling_width, falling_height))
        score_text = font.render(f"{texts['score']}: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Schermata Game Over
def show_game_over(score, texts):
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text_centered(texts['game_over'], HEIGHT // 2 - 60, (255, 0, 0))
        draw_text_centered(f"{texts['score']}: {score}", HEIGHT // 2 - 10)
        draw_text_centered(texts['retry'], HEIGHT // 2 + 40)
        draw_text_centered(texts['quit'], HEIGHT // 2 + 80)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Avvio principale
def main():
    selected_lang = select_language()
    texts = translations[selected_lang]
    while True:
        rigioca = game_loop(texts)
        if not rigioca:
            break

main()
