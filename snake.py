from random import *
import pygame
pygame.init()
pygame.mixer.init()

# serpent
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_tete = {
            "H" : pygame.image.load("assets/images/head_up.png").convert_alpha(),
            "B": pygame.image.load("assets/images/head_down.png").convert_alpha(),
            "G": pygame.image.load("assets/images/head_left.png").convert_alpha(),
            "D": pygame.image.load("assets/images/head_right.png").convert_alpha()
        }
        self.orientation = "D"
        self.image = self.img_tete[self.orientation]
        self.rect = self.image.get_rect()
        self.rect.x = (nb_tuile // 3) * taille_tuile + larg_murs
        self.rect.y = (nb_tuile // 2) * taille_tuile + score_hauteur
        self.taille = 2
        total.add(self)

    def update(self):
        global fin
        global score

        self.image = self.img_tete[self.orientation]
        x = self.rect.x
        y = self.rect.y

        if len(serpent) < self.taille :
            self.ajouter_corps()

        if self.orientation == "H":
            self.rect.y -= taille_tuile
        elif self.orientation == "B":
            self.rect.y += taille_tuile
        elif self.orientation == "D":
            self.rect.x += taille_tuile
        elif self.orientation == "G":
            self.rect.x -= taille_tuile

        if self.rect.x < larg_murs :
            fin = True
        elif self.rect.x > largeur - 2 * larg_murs :
            fin = True
        if self.rect.y < score_hauteur :
            fin = True
        elif self.rect.y > hauteur - 2 * larg_murs :
            fin = True

        prec_x = self.rect.x
        prec_y = self.rect.y
        count = 1
        for elt in serpent :
            elt_x = elt.get_x()
            elt_y = elt.get_y()
            elt.set_xy(x, y)
            if count == self.taille :
                elt.image = self.img_queue((prec_x, prec_y), (x, y))
            else :
                elt.image = self.img_corps((prec_x, prec_y), (elt_x, elt_y), (x, y))
            prec_x = x
            prec_y = y
            x = elt_x
            y = elt_y
            count += 1

        liste_collision = pygame.sprite.spritecollide(self, total, False)
        for cld in liste_collision :
            if type(cld) == Body :
                fin = True
            elif type(cld) == Apple :
                score += 1
                self.taille += 1
                cld.kill()
                new_food = Apple()
                nourriture.play()

    def ajouter_corps(self):
        corps = Body(self.rect.x, self.rect.y)
        serpent.add(corps)
        total.add(corps)

    def img_queue(self, prec, mnt):
        if mnt[0] < prec[0] : # vers la gauche
            image = pygame.image.load("assets/images/tail_left.png").convert_alpha()
        elif mnt[0] > prec[0] : # vers la droite
            image = pygame.image.load("assets/images/tail_right.png").convert_alpha()
        elif mnt[1] < prec[1] : # vers le bas
            image = pygame.image.load("assets/images/tail_up.png").convert_alpha()
        else : # vers le haut
            image = pygame.image.load("assets/images/tail_down.png").convert_alpha()
        return image

    def img_corps(self, prec, suiv, mnt):
        image = pygame.image.load("assets/images/body_horizontal.png").convert_alpha()
        if mnt[0] < prec[0] : # depuis la droite
            if mnt[1] < suiv[1] : # vers le bas
                image = pygame.image.load("assets/images/body_bottomright.png").convert_alpha()
            elif mnt[1] > suiv[1] : # vers le haut
                image = pygame.image.load("assets/images/body_topright.png").convert_alpha()
            else : # tout droit
                image = pygame.image.load("assets/images/body_horizontal.png").convert_alpha()
        elif mnt[0] > prec[0] : # depuis la gauche
            if mnt[1] < suiv[1] : # vers le bas
                image = pygame.image.load("assets/images/body_bottomleft.png").convert_alpha()
            elif mnt[1] > suiv[1] : # vers le haut
                image = pygame.image.load("assets/images/body_topleft.png").convert_alpha()
            else : # tout droit
                image = pygame.image.load("assets/images/body_horizontal.png").convert_alpha()
        elif mnt[1] < prec[1] : # depuis le bas
            if mnt[0] < suiv[0] : # vers la droite
                image = pygame.image.load("assets/images/body_bottomright.png").convert_alpha()
            elif mnt[0] > suiv[0] : # vers la gauche
                image = pygame.image.load("assets/images/body_bottomleft.png").convert_alpha()
            else : # tout droit
                image = pygame.image.load("assets/images/body_vertical.png").convert_alpha()
        elif mnt[1] > prec[1] : # depuis le haut
            if mnt[0] < suiv[0] : # vers la droite
                image = pygame.image.load("assets/images/body_topright.png").convert_alpha()
            elif mnt[0] > suiv[0] : # vers la gauche
                image = pygame.image.load("assets/images/body_topleft.png").convert_alpha()
            else : # tout droit
                image = pygame.image.load("assets/images/body_vertical.png").convert_alpha()
        return image


class Body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/body_vertical.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_x(self): return self.rect.x

    def get_y(self): return self.rect.y

    def set_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/apple.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.boucle = True
        while self.boucle :
            self.rect.x = randint(1, nb_tuile - 1) * taille_tuile + larg_murs
            self.rect.y = randint(1, nb_tuile - 1) * taille_tuile + score_hauteur
            liste_collision = pygame.sprite.spritecollide(self, total, False)
            if len(liste_collision) == 0 :
                self.boucle = False
        total.add(self)

def afficher_score():
    global score
    background = pygame.Surface((largeur, score_hauteur))
    background.fill(color["score"])
    background.convert()
    image = pygame.image.load("assets/images/apple.png").convert_alpha()
    pygame.transform.scale(image, (60, 60))
    image_pos = image.get_rect(right = largeur  / 2 + 5, centery = score_hauteur / 2)
    background.blit(image, image_pos)
    font = pygame.font.Font("assets/font/Poppins-Regular.ttf", 24)
    texte = font.render(f"{score}", 1, color["blanc"])
    txt_pos = texte.get_rect(left = largeur / 2 + 5, centery = score_hauteur / 2)
    background.blit(texte, txt_pos)
    screen.blit(background, (0, 0))

def dessiner_arriere_plan():
    screen.fill(color["score"])
    herbe = pygame.Surface((taille_tuile * nb_tuile, taille_tuile * nb_tuile))
    herbe.fill(color["herbe"])
    herbe_foncee = pygame.Surface((taille_tuile, taille_tuile))
    herbe_foncee.fill(color["herbe_foncée"])
    count = 0
    for t in range(nb_tuile) :
        for i in range(nb_tuile):
            if count % 2 == 1 :
                herbe.blit(herbe_foncee, (taille_tuile * i, taille_tuile * t))
            count += 1
    screen.blit(herbe, (larg_murs, score_hauteur))

#fenetre
taille_tuile = 40
nb_tuile = 15
score_hauteur = 60
larg_murs = 30
largeur = taille_tuile * nb_tuile + 2 * larg_murs
hauteur = taille_tuile * nb_tuile + score_hauteur + larg_murs
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake")

#couleurs
color = {
    "blanc" : pygame.Color(255, 255, 255),
    "noir" : pygame.Color(0, 0, 0),
    "vert" : pygame.Color(0, 255, 0),
    "herbe" : pygame.Color(125, 255, 0),
    "herbe_foncée" : pygame.Color(115, 240, 0),
    "score" : pygame.Color(5, 150, 0)
}

# Musique
pygame.mixer.music.load("assets/music/music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# Sons
perdu = pygame.mixer.Sound("assets/music/gameover.mp3")
perdu.set_volume(1)
nourriture = pygame.mixer.Sound("assets/music/food.mp3")
nourriture.set_volume(1)
mouvement = pygame.mixer.Sound("assets/music/move.mp3")
mouvement.set_volume(0.7)

#groupes de gestion
serpent = pygame.sprite.Group()
total = pygame.sprite.Group()

#sprites
snake = Snake()
apple = Apple()

running = True
fin = False
score = 0
clock = pygame.time.Clock()

apple.rect.x = 12 * taille_tuile + larg_murs
apple.rect.y = snake.rect.y
while running:
    dessiner_arriere_plan()
    snake.update()
    total.draw(screen)
    afficher_score()
    if fin :
        pygame.mixer.music.stop()
        perdu.play()
        running = False
        pygame.time.wait(1500)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_o and snake.orientation != "B" :
                snake.orientation = "H"
                mouvement.play()
                break
            elif event.key == pygame.K_l and snake.orientation != "H" :
                snake.orientation = "B"
                mouvement.play()
                break
            elif event.key == pygame.K_m and snake.orientation != "G" :
                snake.orientation = "D"
                mouvement.play()
                break
            elif event.key == pygame.K_k and snake.orientation != "D" :
                snake.orientation = "G"
                mouvement.play()
                break
    clock.tick(9)
    pygame.display.flip()
pygame.quit()