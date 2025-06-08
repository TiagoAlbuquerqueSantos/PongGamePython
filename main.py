
import sys
import random
import pygame

TAM_TELA = (640, 480)
FPS = 60

VEL_BOLA = 300


class Bola():
    def __init__(self, main, pos_bola):
        self.main = main
        self.tam_bola = 10
        self.vel_bola = [self.gerar_velocidade(), self.gerar_velocidade()]
        self.pos_bola = list(pos_bola)

    def hitbox_bola(self):
        tam_hitbox = 20
        pos_hitbox_canto = (
            self.pos_bola[0] - self.tam_bola, self.pos_bola[1] - self.tam_bola)
        hitbox = pygame.Rect(
            pos_hitbox_canto[0], pos_hitbox_canto[1], tam_hitbox, tam_hitbox)
        return hitbox

    def gerar_velocidade(self):
        return random.randrange(-VEL_BOLA, VEL_BOLA)

    def direcionar(self):
        self.pos_bola[0] += self.vel_bola[0] * self.main.dt
        self.pos_bola[1] += self.vel_bola[1] * self.main.dt
        if self.pos_bola[1] < 0 or self.pos_bola[1] > TAM_TELA[1]:
            self.vel_bola[1] *= -1

    def atualizar(self):
        self.direcionar()

    def desenhar(self):
        pygame.draw.circle(self.main.tela, (255, 255, 255),
                           self.pos_bola, self.tam_bola)
       # pygame.draw.rect(self.main.tela, (255, 255, 0), self.hitbox_bola())


class PlayerEsquerda:
    def __init__(self, main):
        self.main = main
        self.tam_barra = [20, 150]
        self.pos_barra = [0, 0]
        self.vel_barra = 200

    def hitbox_barra(self):
        self.rect_barra = pygame.Rect(
            self.pos_barra[0], self.pos_barra[1], self.tam_barra[0], self.tam_barra[1])
        return self.rect_barra

    def controle_movimento(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.pos_barra[1] -= self.vel_barra * self.main.dt
        if teclas[pygame.K_s]:
            self.pos_barra[1] += self.vel_barra * self.main.dt

        if self.pos_barra[1] < 0:
            self.pos_barra[1] = 0
        if self.pos_barra[1] > TAM_TELA[1] - self.tam_barra[1]:
            self.pos_barra[1] = TAM_TELA[1] - self.tam_barra[1]

    def atualizar(self):
        self.controle_movimento()
        self.hitbox_barra()

    def desenhar(self):
        pygame.draw.rect(self.main.tela, (255, 255, 255), self.rect_barra)


class PlayerDireita:
    def __init__(self, main):
        self.main = main
        self.tam_barra = [20, 150]
        self.pos_barra = [TAM_TELA[0] - self.tam_barra[0], 0]
        self.vel_barra = 200

    def hitbox_barra(self):
        self.rect_barra = pygame.Rect(
            self.pos_barra[0], self.pos_barra[1], self.tam_barra[0], self.tam_barra[1])
        return self.rect_barra

    def controle_movimento(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.pos_barra[1] -= self.vel_barra * self.main.dt
        if teclas[pygame.K_DOWN]:
            self.pos_barra[1] += self.vel_barra * self.main.dt

        if self.pos_barra[1] < 0:
            self.pos_barra[1] = 0
        if self.pos_barra[1] > TAM_TELA[1] - self.tam_barra[1]:
            self.pos_barra[1] = TAM_TELA[1] - self.tam_barra[1]

    def atualizar(self):
        self.controle_movimento()
        self.hitbox_barra()

    def desenhar(self):
        pygame.draw.rect(self.main.tela, (255, 255, 255), self.rect_barra)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pong Game')
        self.tela = pygame.display.set_mode(TAM_TELA)
        self.relogio = pygame.time.Clock()
        self.dt = 0.1

        self.pontos = [0, 0]

        self.font_style = pygame.font.SysFont(None, 30)

        self.bola = Bola(self, (self.tela.get_width() //
                         2, self.tela.get_height() // 2))

        self.jogador_1 = PlayerEsquerda(self)
        self.jogador_2 = PlayerDireita(self)

    def linha_divisao(self):
        pygame.draw.line(self.tela, (255, 255, 255),
                         (TAM_TELA[0] // 2, 0), (TAM_TELA[0] // 2, self.tela.get_height()), 1)

    def desenhar_pontuacao(self):
        texto = self.font_style.render(
            f'Pontuação: A {self.pontos[0]} | B {self.pontos[1]}', None, (255, 255, 0))
        rect_texto = texto.get_rect(
            center=(TAM_TELA[0] // 2, 10))
        self.tela.blit(texto, rect_texto)

    def rodar(self):
        while True:
            self.tela.fill((0, 0, 0))

            self.bola.atualizar()
            self.jogador_1.atualizar()
            self.jogador_2.atualizar()

            if self.bola.hitbox_bola().colliderect(self.jogador_1.hitbox_barra()):
                self.bola.vel_bola[0] *= -1
                self.pontos[0] += 1

            if self.bola.hitbox_bola().colliderect(self.jogador_2.hitbox_barra()):
                self.bola.vel_bola[0] *= -1
                self.pontos[1] += 1

            if self.bola.pos_bola[0] < 0 or self.bola.pos_bola[0] > TAM_TELA[0]:
                pygame.quit()
                sys.exit()

            self.bola.desenhar()
            self.jogador_1.desenhar()
            self.jogador_2.desenhar()

            self.linha_divisao()
            self.desenhar_pontuacao()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.dt = self.relogio.tick(FPS) / 1000
            self.dt = max(0.001, min(0.1, self.dt))


Game().rodar()
