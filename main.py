import random
from sys import exit

import pygame


class Main:
    def __init__(self):
        # Timebar inicjalizacja
        self.timebar_surface = pygame.image.load('Assets/imgs/Other/TimeBar.png')
        self.timebar_surface = pygame.transform.scale(self.timebar_surface, (260, 80))
        self.timebar_rect = self.timebar_surface.get_rect(center=(screen.get_width() // 2, 150))

        self.rectangle_bg = pygame.Rect(195, 115, 250, 70)
        self.width = 119  # max: 234, min: 2, half: 119
        self.height = 65
        self.main_rectangle = pygame.Rect(203, 115, self.width, self.height)

    def draw(self):
        self.width -= 0.5
        self.main_rectangle = pygame.Rect(203, 115, int(self.width), self.height)
        pygame.draw.rect(screen, '#3c2d00', self.rectangle_bg, )
        pygame.draw.rect(screen, '#bd2800', self.main_rectangle)
        screen.blit(self.timebar_surface, self.timebar_rect)


class Timberman:
    def __init__(self):
        # Wczytanie obrazów postaci
        self.timberman1 = pygame.image.load('Assets/imgs/Player/Player0.png')
        self.timberman1 = pygame.transform.scale2x(self.timberman1)

        self.timberman2 = pygame.image.load('Assets/imgs/Player/Player1.png')
        self.timberman2 = pygame.transform.scale2x(self.timberman2)

        self.timberman3 = pygame.image.load('Assets/imgs/Player/Player2.png')
        self.timberman3 = pygame.transform.scale2x(self.timberman3)

        self.timberman3_flip = pygame.transform.flip(self.timberman3, True, False)
        self.rip = pygame.image.load('Assets/imgs/Player/Tombstone.png')
        self.rip = pygame.transform.scale2x(self.rip)

        # Skalowanie obrazu postaci
        self.timberman_surface = self.timberman1

        # Uzyskanie prostokąta określającego pozycję postaci
        self.timberman_rect = self.timberman_surface.get_rect(topleft=(20, 550))

        # Flaga określająca, czy postać jest zwrócona w prawo
        self.facing_right = False

        # Aktualny obraz postaci
        self.timber_now = self.timberman1

        # Ustawienie początkowego wyniku
        self.score = 0

        # Inicjalizacja czcionki do wyświetlania wyniku
        self.font = pygame.font.Font('Assets/font/font.ttf', 50)
        self.text = self.font.render(str(self.score), True, (255, 255, 255))
        self.better_timber = 0

        # załadowanie poprzedzniego najlepszego wyniku.
        try:
            with open('score.txt', 'r') as file:
                self.best_score = int(file.read().strip())
        except ValueError:
            self.best_score = 0

    def draw(self):
        if self.timberman_surface == self.timberman3 or self.timberman_surface == self.timberman3_flip:

            '''Szybciej zmienia się z timberman3 na domyslny'''

            if self.better_timber >= 2:
                if not self.facing_right:
                    self.timberman_surface = self.timber_now
                else:
                    self.timberman_surface = pygame.transform.flip(self.timber_now, True, False)
                    self.facing_right = True
                self.better_timber = 0
            else:
                self.better_timber += 1

        # Rysowanie postaci na ekranie
        screen.blit(self.timberman_surface, self.timberman_rect)

        # Wyświetlanie wyniku na środku ekranu
        screen.blit(self.text, self.text.get_rect(center=((screen.get_width() // 2), 300)))

    def K_LEFT(self):
        if game and not start_menu:
            self.better_timber = 0
            Chop.play()  # dzwiek
            # Zwiększenie wyniku i aktualizacja wyświetlanego tekstu
            self.score += 1
            self.text = self.font.render(str(self.score), True, (255, 255, 255))

            # Zmiana powierzchni postaci przy ruchu w lewo
            self.timberman_surface = self.timberman3
            self.facing_right = False

            # Obracanie postaci w lewo jeśli była zwrócona w prawo
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
                self.facing_right = False

            # Ustawienie pozycji postaci na lewą stronę
            self.timberman_rect.topleft = (20, 550)

    def K_RIGHT(self):
        if game and not start_menu:
            Chop.play()  # dzwiek
            self.better_timber = 0
            # Zwiększenie wyniku i aktualizacja wyświetlanego tekstu
            self.score += 1
            self.text = self.font.render(str(self.score), True, (255, 255, 255))

            # Zmiana powierzchni postaci przy ruchu w prawo
            self.timberman_surface = self.timberman3_flip
            self.facing_right = True

            # Obracanie postaci w prawo jeśli była zwrócona w lewo
            if not self.facing_right:
                self.timberman_surface = self.timberman3_flip
                self.facing_right = True

            # Ustawienie pozycji postaci na prawą stronę
            self.timberman_rect.topleft = (340, 540)

    def update_surface(self):
        # Aktualizacja powierzchni postaci do animacji
        if self.timber_now == self.timberman1:
            # Zmiana obrazu na timberman2
            self.timberman_surface = self.timberman2
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.timber_now = self.timberman2
        elif self.timber_now == self.timberman2:
            # Zmiana obrazu na timberman1
            self.timberman_surface = self.timberman1
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.timber_now = self.timberman1

    def check_collision(self, treeinstance, maininstance):
        if game:
            # Sprawdzenie kolizji z pierwszą gałęzią
            if treeinstance.branch_rects[0] is not None:
                if self.timberman_rect.colliderect(treeinstance.branch_rects[0]):
                    # Ustawienie gry na false, gdy dojdzie do kolizji
                    self.timberman_surface = self.rip

                    if self.facing_right:
                        self.timberman_rect = self.timberman_surface.get_rect(topleft=(400, 540))
                    else:
                        self.timberman_rect = self.timberman_surface.get_rect(topleft=(15, 540))

                    self.score_update()
                    GameOver.play()
                    return False

            elif maininstance.width <= 2:
                self.timberman_surface = self.rip

                self.score_update()
                GameOver.play()
                return False
        return True

    def score_update(self):
        # TODO: napraw
        if self.score - 1 > self.best_score:
            HighScore.play()
            self.best_score = self.score
            with open('score.txt', 'w') as file:
                file.write(str(self.best_score))


class Tree:
    def __init__(self):
        # Wczytanie i skalowanie obrazów pni
        self.log_surface = pygame.image.load('Assets/imgs/Tree/Log0.png')
        self.log_surface = pygame.transform.scale2x(self.log_surface)

        # Ustawienie prostokąta dla pnia
        self.log_rect = self.log_surface.get_rect(center=(320, 619))

        # Lista pni
        self.log_list = [self.log_surface, self.log_surface, self.log_surface, self.log_surface, self.log_surface]

        # Wczytanie obrazów gałęzi i ich pozycjonowanie
        self.branch_left_surface = pygame.image.load('Assets/imgs/Tree/Branch.png')
        self.branch_left_rect = self.branch_left_surface.get_rect(center=(110, 550))
        self.branch_right_surface = pygame.image.load('Assets/imgs/Tree/Branch.png')
        self.branch_right_surface = pygame.transform.flip(self.branch_right_surface, True, False)

        # Losowe rozmieszczenie gałęzi
        self.branch_list = [None, None, None,
                            random.choice([None, self.branch_left_surface, self.branch_right_surface]),
                            None,
                            random.choice([None, self.branch_left_surface, self.branch_right_surface])]

        # Lista prostokątów dla gałęzi
        self.branch_rects = []

    def draw(self):
        # Czyszczenie listy prostokątów gałęzi
        self.branch_rects.clear()

        # Rysowanie pni drzewa na ekranie
        height = 761
        for log in self.log_list:
            rect = log.get_rect(center=(320, (height - 142)))
            screen.blit(log, rect)
            height -= 142

        # Rysowanie gałęzi na ekranie
        height = 834
        for branch in self.branch_list:
            if branch is not None:
                if branch == self.branch_left_surface:
                    rect = branch.get_rect(center=(110, (height - 142)))
                    if rect:
                        self.branch_rects.append(rect)
                    screen.blit(branch, rect)
                else:
                    rect = branch.get_rect(center=(530, (height - 142)))
                    if rect:
                        self.branch_rects.append(rect)
                    screen.blit(branch, rect)
                height -= 142
            else:
                height -= 142
                self.branch_rects.append(None)

    def click(self):
        if game and not start_menu:
            # Usunięcie pierwszego elementu (gałęzi) z listy
            self.branch_list.pop(0)

            # Dodanie nowej gałęzi na końcu listy w zależności od ostatniej gałęzi
            if self.branch_list[-1] == self.branch_right_surface:
                self.branch_list.append(
                    random.choice([None, None, self.branch_right_surface]))  # Zwiększenie szansy na None
            elif self.branch_list[-1] == self.branch_left_surface:
                self.branch_list.append(random.choice([None, None, self.branch_left_surface]))
                # Zwiększenie szansy na None
            else:
                self.branch_list.append(random.choice([None, self.branch_left_surface, self.branch_right_surface]))


# Inicjalizacja Pygame
pygame.init()
pygame.mixer.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((640, 960))
pygame.display.set_caption("Hello World!")

# Wczytanie tła
sky_surface = pygame.image.load('Assets/imgs/Background/sky.png')
ground_surface = pygame.image.load('Assets/imgs/Background/Forest.png')

# Zegar do kontroli czasu
clock = pygame.time.Clock()

# Ustawienie timera do animacji postaci
timber_animation1 = pygame.USEREVENT + 1
pygame.time.set_timer(timber_animation1, 200)

game = False
start_menu = True

# Utworzenie obiektu Timberman
timberman = Timberman()

# Utworzenie obiektu Tree
tree = Tree()

main = Main()

# menu po śmierci
menu = pygame.image.load('Assets/imgs/Background/menu.png')
menu_rect = menu.get_rect(center=(320, 270))
font = pygame.font.Font('Assets/font/DisposableDroidBB.ttf', 60)

play = pygame.image.load('Assets/imgs/Buttons/PlayButton.png')
play_rect = play.get_rect(center=(320, 670))

# start menu
caption = pygame.image.load('Assets/imgs/Other/caption.png')
caption = pygame.transform.scale(caption, (caption.get_width() // 2, caption.get_height() // 2))
caption_rect = caption.get_rect(center=(320, 180))

chop1 = pygame.image.load('Assets/imgs/Other/chop1.png')
chop1_rect = chop1.get_rect(center=(90, 870))
chop2 = pygame.image.load('Assets/imgs/Other/chop2.png')
chop2_rect = chop2.get_rect(center=(550, 870))

chop1_right = True
chop2_right = True


def chop_LEFT():
    #TODO: popraw
    global chop1_rect, chop1_right
    if chop1_right:
        chop1_rect.x += 10
        if chop1_rect.x > 320 - 180:  # Check for half window width
            chop1_right = False
    else:
        chop1_rect.x -= 10
        if chop1_rect.x < 0:  # Adjust to stay within left edge
            chop1_right = True


def chop_RIGHT():
    # TODO: popraw
    global chop2_rect, chop2_right
    if chop2_right:
        chop2_rect.x += 10
        if chop2_rect.x > 640 - 180:  # Adjust to stay within right edge
            chop2_right = False
    else:
        chop2_rect.x -= 10
        if chop2_rect.x < 640 / 2:  # Check for half window width
            chop2_right = True


# Dzwięki
soundtrack = pygame.mixer.Sound('Assets/Music/Soundtrack.wav')
soundtrack.play(-1)
Button = pygame.mixer.Sound('Assets/Sounds/Button.wav')
Chop = pygame.mixer.Sound('Assets/Sounds/Chop.wav')
GameOver = pygame.mixer.Sound('Assets/Sounds/GameOver.wav')
HighScore = pygame.mixer.Sound('Assets/Sounds/HighScore.wav')

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game:
            if event.type == timber_animation1:
                # Aktualizacja powierzchni postaci co 200 ms
                timberman.update_surface()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    timberman.K_LEFT()
                    # Sprawdzenie kolizji postaci z gałęziami
                    game = timberman.check_collision(tree, main)
                    tree.click()
                    if main.width < 234:
                        main.width += 5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    timberman.K_RIGHT()
                    # Sprawdzenie kolizji postaci z gałęziami
                    game = timberman.check_collision(tree, main)
                    tree.click()
                    if main.width < 240:
                        main.width += 5

        if not game and not start_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lewy przycisk
                    if play_rect.collidepoint(event.pos):
                        Button.play()  # dzwięk po kliknieciu
                        # restart gry
                        timberman = Timberman()
                        tree = Tree()
                        main = Main()
                        game = True

        elif start_menu and not game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lewy przycisk
                    if play_rect.collidepoint(event.pos):
                        Button.play()  # dzwięk po kliknieciu
                        game = True
                        start_menu = False

    # Rysowanie tła
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 0))

    # Rysowanie drzewa
    tree.draw()

    # Rysowanie postaci
    timberman.draw()

    if start_menu:
        chop_RIGHT()
        chop_LEFT()

        screen.blit(caption, caption_rect)
        screen.blit(play, play_rect)
        screen.blit(chop1, chop1_rect)
        screen.blit(chop2, chop2_rect)

    elif game:
        game = timberman.check_collision(tree, main)
        main.draw()

    elif not game:
        timberman.score_update()
        # Rysowanie menu po śmierci
        screen.blit(menu, menu_rect)
        new_score = font.render(str(timberman.score - 1), True, (255, 255, 255))
        new_score_rect = new_score.get_rect(center=(320, 430))
        best_score = font.render(str(timberman.best_score - 1), True, (255, 255, 255))
        best_score_rect = best_score.get_rect(center=(320, 310))
        screen.blit(new_score, new_score_rect)
        screen.blit(best_score, best_score_rect)
        screen.blit(play, play_rect)
    # Sprawdzenie kolizji postaci z gałęziami

    # Aktualizacja ekranu
    pygame.display.update()

    # Ustawienie liczby klatek na sekundę
    clock.tick(120)
