import pygame
import random
import sys

# Inicialización
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack - Mesa de apuestas")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)

# Colores
GREEN_TABLE = (39, 119, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 30, 30)
GRAY = (180, 180, 180)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

# Sonidos
try:
    sound_card = pygame.mixer.Sound("sounds/card.wav")
    sound_win = pygame.mixer.Sound("sounds/win.wav")
    sound_lose = pygame.mixer.Sound("sounds/lose.wav")
    sound_draw = pygame.mixer.Sound("sounds/draw.wav")
except:
    sound_card = sound_win = sound_lose = sound_draw = None

# Botones y texto
def draw_button(rect, text, active=True):
    color = GOLD if active else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_text(text, x, y, color=WHITE, center=False, big=False):
    fnt = pygame.font.SysFont("arial", 34 if big else 28, bold=True)
    img = fnt.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

# Cartas
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def render_card(card_text):
    card = pygame.Surface((60, 90))
    card.fill(WHITE)
    pygame.draw.rect(card, BLACK, (0, 0, 60, 90), 2)

    # Color según el palo
    suit = card_text[-1]
    color = RED if suit in ['♥', '♦'] else BLACK

    label = font.render(card_text, True, color)
    label_rect = label.get_rect(center=(30, 45))
    card.blit(label, label_rect)
    return card

def render_back_card():
    card = pygame.Surface((60, 90))
    card.fill(GRAY)
    pygame.draw.rect(card, BLACK, (0, 0, 60, 90 ), 2)
    pygame.draw.circle(card, BLUE, (30, 45), 20, 5)
    return card

card_images = {f"{rank}{suit}": render_card(f"{rank}{suit}") for suit in suits for rank in ranks}
card_back = render_back_card()

# Animación
def animate_card(card_surf, start_pos, end_pos, duration=300):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        t = (pygame.time.get_ticks() - start_time) / duration
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        screen.fill(GREEN_TABLE)
        screen.blit(card_surf, (x, y))
        pygame.display.flip()
        clock.tick(60)

# Lógica del mazo
def create_deck():
    deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def card_value(card):
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[:-1] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_hand(cards, y_pos, hide_first=False):
    for i, card in enumerate(cards):
        if hide_first and i == 1:
            screen.blit(card_back, (100 + i * 70, y_pos))
        else:
            screen.blit(card_images[card], (100 + i * 70, y_pos))

# Juego principal
def mainBlackjack():
    players = [
        {"name": "Jugador 1", "money": 1000, "bet": 100},
        {"name": "Jugador 2", "money": 1000, "bet": 100}
    ]
    stats = {"ganadas": 0, "perdidas": 0, "empatadas": 0}
    current_player = 0

    while any(player["money"] > 0 for player in players):
        player = players[current_player]
        if player["money"] <= 0:
            current_player = (current_player + 1) % 2
            continue

        deck = create_deck()
        player_hand, dealer_hand = [], []

        for _ in range(2):
            card = deck.pop()
            player_hand.append(card)
            if sound_card: sound_card.play()
            animate_card(card_images[card], (WIDTH // 2, HEIGHT // 2), (100 + len(player_hand) * 70, 380))

            card_d = deck.pop()
            dealer_hand.append(card_d)
            if sound_card: sound_card.play()
            animate_card(card_images[card_d], (WIDTH // 2, HEIGHT // 2), (100 + len(dealer_hand) * 70, 100))

        stand = False
        game_over = False
        result = ""
        ronda_terminada = False

        pedir_btn = pygame.Rect(50, 600, 180, 50)
        plantarse_btn = pygame.Rect(250, 600, 180, 50)
        apuesta_mas_btn = pygame.Rect(470, 600, 100, 50)
        apuesta_menos_btn = pygame.Rect(580, 600, 100, 50)
        salir_btn = pygame.Rect(700, 600, 180, 50)
        otra_ronda_btn = pygame.Rect(400, 400, 200, 50)

        while not ronda_terminada:
            screen.fill(GREEN_TABLE)
            pygame.draw.rect(screen, (20, 90, 20), (0, 550, WIDTH, 150))

            draw_text(f"{player['name']} - Dinero: ${player['money']}", 20, 20)
            draw_text(f"Apuesta: ${player['bet']}", 20, 60)

            draw_hand(player_hand, 380)
            if stand or game_over:
                draw_hand(dealer_hand, 100)
            else:
                draw_hand(dealer_hand, 100, hide_first=True)

            draw_text(f"{player['name']}: {hand_value(player_hand)}", 100, 340)
            if stand or game_over:
                draw_text(f"Croupier: {hand_value(dealer_hand)}", 100, 200)

            if game_over:
                color = GREEN if "Ganaste" in result else RED if "Pierdes" in result else BLUE
                pygame.draw.rect(screen, BLACK, (280, 260, 440, 120), border_radius=15)
                pygame.draw.rect(screen, WHITE, (280, 260, 440, 120), 4, border_radius=15)
                draw_text(result, WIDTH // 2, 320, color, center=True, big=True)
                draw_button(otra_ronda_btn, "Otra ronda")

            # Botones
            draw_button(pedir_btn, "Pedir Carta", not game_over)
            draw_button(plantarse_btn, "Plantarse", not game_over)
            draw_button(apuesta_mas_btn, "+50", not game_over and player["bet"] + 50 <= player["money"])
            draw_button(apuesta_menos_btn, "-50", not game_over and player["bet"] - 50 >= 50)
            draw_button(salir_btn, "Salir", True)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if salir_btn.collidepoint(event.pos):
                        pygame.quit(); sys.exit()

                    if not game_over:
                        if apuesta_mas_btn.collidepoint(event.pos) and player["bet"] + 50 <= player["money"]:
                            player["bet"] += 50
                        elif apuesta_menos_btn.collidepoint(event.pos) and player["bet"] - 50 >= 50:
                            player["bet"] -= 50
                        elif pedir_btn.collidepoint(event.pos):
                            card = deck.pop()
                            player_hand.append(card)
                            if sound_card: sound_card.play()
                            animate_card(card_images[card], (WIDTH // 2, HEIGHT // 2), (100 + len(player_hand) * 70, 380))
                            if hand_value(player_hand) > 21:
                                result = "¡Te pasaste! Pierdes."
                                player["money"] -= player["bet"]
                                stats["perdidas"] += 1
                                if sound_lose: sound_lose.play()
                                game_over = True
                        elif plantarse_btn.collidepoint(event.pos):
                            stand = True
                            while hand_value(dealer_hand) < 17:
                                card = deck.pop()
                                dealer_hand.append(card)
                                if sound_card: sound_card.play()
                                animate_card(card_images[card], (WIDTH // 2, HEIGHT // 2), (100 + len(dealer_hand) * 70, 100))

                            p_val = hand_value(player_hand)
                            d_val = hand_value(dealer_hand)

                            if d_val > 21 or p_val > d_val:
                                result = "¡Ganaste!"
                                player["money"] += player["bet"]
                                stats["ganadas"] += 1
                                if sound_win: sound_win.play()
                            elif p_val < d_val:
                                result = "Pierdes."
                                player["money"] -= player["bet"]
                                stats["perdidas"] += 1
                                if sound_lose: sound_lose.play()
                            else:
                                result = "Empate."
                                stats["empatadas"] += 1
                                if sound_draw: sound_draw.play()
                            game_over = True

                    elif game_over and otra_ronda_btn.collidepoint(event.pos):
                        ronda_terminada = True

            clock.tick(30)

        current_player = (current_player + 1) % 2 


    pygame.quit()   
    print("Fin del juego.")

if __name__ == "__main__":
    mainBlackjack()
