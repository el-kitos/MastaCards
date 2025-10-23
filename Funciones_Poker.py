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
    # use cached fonts to avoid recreating them each frame
    global _FONT_REG, _FONT_BIG
    try:
        _FONT_REG
    except NameError:
        _FONT_REG = pygame.font.SysFont("arial", 28, bold=True)
        _FONT_BIG = pygame.font.SysFont("arial", 34, bold=True)
    fnt = _FONT_BIG if big else _FONT_REG
    img = fnt.render(str(text), True, color)
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


class Animation:
    """Animación no bloqueante simple para mover una superficie de un punto a otro."""
    def __init__(self, card_surf, start_pos, end_pos, duration=300):
        self.card_surf = card_surf
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.finished = False
        # optional metadata: card key (string) and current position
        self.card_key = None
        self.x = self.start_x
        self.y = self.start_y

    def update(self, screen):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        t = min(1.0, elapsed / self.duration)
        x = self.start_x + (self.end_x - self.start_x) * t
        y = self.start_y + (self.end_y - self.start_y) * t
        self.x = x
        self.y = y
        if t >= 1.0:
            self.finished = True
        return self.finished


def animate_card(card_surf, start_pos, end_pos, card_key=None, screen=None, clock=None, duration=300):
    anim = Animation(card_surf, start_pos, end_pos, duration)
    anim.card_key = card_key
    return anim
    
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