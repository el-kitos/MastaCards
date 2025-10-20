import pygame
import random

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']





# Colores
GREEN_TABLE = (39, 119, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 30, 30)
GRAY = (180, 180, 180)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

# Botones y texto
def draw_button(rect, text, font, screen,active=True):
    color = GOLD if active else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_text(text, x, y, screen, color=WHITE, center=False, big=False):
    fnt = pygame.font.SysFont("arial", 34 if big else 28, bold=True)
    img = fnt.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def render_card(card_text, font):
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


def animate_card(card_surf, start_pos, end_pos, screen, clock, duration=300):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        t = (pygame.time.get_ticks() - start_time) / duration
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        screen.fill(GREEN_TABLE)
        screen.blit(card_surf, (x, y))
        pygame.display.flip()
        clock.tick(60)
    return {"image": card_surf, "x": start_pos[0], "y": start_pos[1],
        "end_x": end_pos[0], "end_y": end_pos[1] }
    
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

def draw_hand(cards, y_pos, card_back, card_images, screen, hide_first=False):
    for i, card in enumerate(cards):
        if hide_first and i == 1:
            screen.blit(card_back, (100 + i * 70, y_pos))
        else:
            screen.blit(card_images[card], (100 + i * 70, y_pos))