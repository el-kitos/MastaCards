import importlib
import pygame
import sys
import os

# ---------------- CONFIG ---------------- #
ANCHO, ALTO = 1152, 700
FPS = 60
AMARILLO = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MASTA - Menú")
clock = pygame.time.Clock()

POS_MENU_PRINCIPAL_NORM = [0.399, 0.526]
OPCIONES_PRINCIPAL = ["PLAY", "EXIT"]

WBTN = int(ANCHO * 0.38)
HBTN = int(ALTO * 0.085)

# ---------------- UTILIDADES ---------------- #
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "IMG")

def cargar_imagen(nombre, fallback_color=(10, 10, 10)):
    ruta = os.path.join(IMG_DIR, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert()
        if img.get_size() != (ANCHO, ALTO):
            img = pygame.transform.smoothscale(img, (ANCHO, ALTO)).convert()
        return img
    surf = pygame.Surface((ANCHO, ALTO))
    surf.fill(fallback_color)
    return surf

def get_btn_rect(center):
    rect = pygame.Rect(0, 0, WBTN, HBTN)
    rect.center = center
    return rect

def dibujar_resaltado(rect, grosor=3, color=AMARILLO):
    pygame.draw.rect(screen, color, rect, grosor)

def esperar_frame():
    pygame.display.flip()
    clock.tick(FPS)


# ---------------- ESCENAS ---------------- #
def menu_principal():
    fondo = cargar_imagen("MastaCards.png")
    seleccion = 0
    cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    cursor_arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
        centros = [(ANCHO // 2, int(ALTO * p)) for p in POS_MENU_PRINCIPAL_NORM]
        rects = [get_btn_rect(c) for c in centros]

        screen.blit(fondo, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hovered = None
        for i, r in enumerate(rects):
            if r.collidepoint(mouse_pos):
                hovered = i
                break
        if hovered is not None:
            seleccion = hovered
            pygame.mouse.set_cursor(cursor_hand)
        else:
            pygame.mouse.set_cursor(cursor_arrow)

        dibujar_resaltado(rects[seleccion])
        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    seleccion = (seleccion - 1) % len(OPCIONES_PRINCIPAL)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    seleccion = (seleccion + 1) % len(OPCIONES_PRINCIPAL)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    eleccion = OPCIONES_PRINCIPAL[seleccion]
                    if eleccion == "EXIT": return "exit"
                    if eleccion == "PLAY": return "play"
                    

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rects[seleccion].collidepoint(event.pos):
                    eleccion = OPCIONES_PRINCIPAL[seleccion]
                    if eleccion == "EXIT": return "exit"
                    if eleccion == "PLAY": return "play"
                    


def menu_play():
    opciones = ["BLACKJACK", "BACCARAT", "TRUCO", "MINAS", "BACK"]
    seleccion = 0
    fondo = cargar_imagen("mastafamilyfriendly.png")
    fuente = pygame.font.Font(None, 72)

    posiciones = [
        (ANCHO // 2, int(ALTO * 0.45)),
        (ANCHO // 2, int(ALTO * 0.55)),
        (ANCHO // 2, int(ALTO * 0.65)),
        (ANCHO // 2, int(ALTO * 0.75)),
        (ANCHO // 2, int(ALTO * 0.85))
    ]

    cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    cursor_arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
        screen.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        rects = []
        mouse_pos = pygame.mouse.get_pos()
        hovered = None

        for i, (txt, pos) in enumerate(zip(opciones, posiciones)):
            col = (255, 255, 255) if i != seleccion else AMARILLO
            rend = fuente.render(txt, True, col)
            r = rend.get_rect(center=pos)
            rects.append(r.inflate(30, 20))
            screen.blit(rend, r)
            if rects[i].collidepoint(mouse_pos):
                hovered = i

        if hovered is not None:
            seleccion = hovered
            pygame.mouse.set_cursor(cursor_hand)
        else:
            pygame.mouse.set_cursor(cursor_arrow)

        dibujar_resaltado(rects[seleccion])
        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return opciones[seleccion]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rects[seleccion].collidepoint(event.pos):
                    return opciones[seleccion]


def pantalla_tutorial():
    fondo_tutorial = cargar_imagen("TUTORIAL.png", fallback_color=(20, 10, 30))
    fuente = pygame.font.Font(None, 48)

    while True:
        screen.blit(fondo_tutorial, (0, 0))
        texto = "Press ESC to return"
        help_txt = fuente.render(texto, True, (230, 230, 230))
        screen.blit(help_txt, help_txt.get_rect(center=(ANCHO//2, ALTO-60)))

        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return


def pantalla_proximamente():
    fuente = pygame.font.Font(None, 100)
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((0, 0, 0))
    texto = fuente.render("PRÓXIMAMENTE...", True, (255, 255, 0))
    rect = texto.get_rect(center=(ANCHO//2, ALTO//2))

    while True:
        screen.blit(fondo, (0, 0))
        screen.blit(texto, rect)
        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


# ---------------- BUCLE PRINCIPAL ---------------- #
def main():
    while True:
        destino = menu_principal()
        if destino == "exit":
            pygame.quit(); sys.exit()
        elif destino == "play":
            eleccion = menu_play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_principal()
            if eleccion == "BLACKJACK":
                mod = importlib.import_module("blackjack")
                mod.mainBlackjack()
                for event in pygame.event.get():    
                    if event.type == pygame.QUIT:
                        menu_principal()
            elif eleccion == "TRUCO":
                mod = importlib.import_module("truco.mainT")
                mod.mainTruco()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu_principal()
            elif eleccion == "BACCARAT":
                mod = importlib.import_module("baccarat")
                mod.mainBaccarat()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu_principal()
            elif eleccion == "MINAS":
                global screen
                res_original = (ANCHO,ALTO)
                screen = pygame.display.set_mode((600, 700))
                pygame.display.set_caption("Minas")
                mod = importlib.import_module("minas")
                mod.mainMinas()
                screen = pygame.display.set_mode(res_original)
                pygame.display.set_caption("MASTA - Menú")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu_principal()
            elif eleccion == "BACK":
                continue


if __name__ == "__main__":
    main()