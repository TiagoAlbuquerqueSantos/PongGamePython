
import sys
import random
import pygame

RESOLUCAO_TELA = LARGURA, ALTURA = 640, 480
FPS = 60

COR_FUNDO = (0, 0, 0)

# Propriedades da Bola
VEL_BOLA = 200
TAM_BOLA = 10
COR_BOLA = (255, 255, 255)
TAM_HITBOX = 20


class Bola():
    def __init__(self, main, pos_bola):
        self.main = main
        self.vel_bola = [self.gerar_velocidade(), self.gerar_velocidade()]
        self.pos_bola = list(pos_bola)

    def hitbox_bola(self):
        pos_hitbox_canto = (
            self.pos_bola[0] - TAM_BOLA, self.pos_bola[1] - TAM_BOLA)
        hitbox = pygame.Rect(
            pos_hitbox_canto[0], pos_hitbox_canto[1], TAM_HITBOX, TAM_HITBOX)
        return hitbox

    def gerar_velocidade(self):
        return random.randrange(-VEL_BOLA, VEL_BOLA)

    def direcionar(self):
        self.pos_bola[0] += self.vel_bola[0] * self.main.dt
        self.pos_bola[1] += self.vel_bola[1] * self.main.dt
        if self.pos_bola[1] < 0 or self.pos_bola[1] > ALTURA:
            self.vel_bola[1] *= -1

    def atualizar(self):
        self.direcionar()

    def desenhar(self):
        pygame.draw.circle(self.main.tela, COR_BOLA, self.pos_bola, TAM_BOLA)
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
        if self.pos_barra[1] > ALTURA - self.tam_barra[1]:
            self.pos_barra[1] = ALTURA - self.tam_barra[1]

    def atualizar(self):
        self.controle_movimento()
        self.hitbox_barra()

    def desenhar(self):
        pygame.draw.rect(self.main.tela, (255, 255, 255), self.rect_barra)


class PlayerDireita:
    def __init__(self, main):
        self.main = main
        self.tam_barra = [20, 150]
        self.pos_barra = [LARGURA - self.tam_barra[0], 0]
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
        if self.pos_barra[1] > ALTURA - self.tam_barra[1]:
            self.pos_barra[1] = ALTURA - self.tam_barra[1]

    def atualizar(self):
        self.controle_movimento()
        self.hitbox_barra()

    def desenhar(self):
        pygame.draw.rect(self.main.tela, (255, 255, 255), self.rect_barra)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pong Game')
        self.tela = pygame.display.set_mode(RESOLUCAO_TELA)
        self.font_style = pygame.font.SysFont(None, 30)
        self.relogio = pygame.time.Clock()
        self.dt = 0.1

        self.pontos = [0, 0]

        self.bolas = [Bola(self, (LARGURA // 2, ALTURA // 2))]

        self.jogador_1 = PlayerEsquerda(self)
        self.jogador_2 = PlayerDireita(self)

    def linha_divisao(self):
        pygame.draw.line(self.tela, (255, 255, 255),
                         (LARGURA // 2, 0), (LARGURA // 2, self.tela.get_height()), 1)

    def desenhar_pontuacao(self):
        texto = self.font_style.render(
            f'Pontuação: A {self.pontos[0]} | B {self.pontos[1]}', True, (255, 255, 0))
        rect_texto = texto.get_rect(
            center=(LARGURA // 2, 10))
        self.tela.blit(texto, rect_texto)

    def rodar(self):
        while True:
            self.tela.fill(COR_FUNDO)

            self.jogador_1.atualizar()
            self.jogador_2.atualizar()

            for bola in self.bolas:
                bola.atualizar()

                if bola.hitbox_bola().colliderect(self.jogador_1.hitbox_barra()):
                    bola.vel_bola[0] *= -1
                    self.pontos[0] += 1

                if bola.hitbox_bola().colliderect(self.jogador_2.hitbox_barra()):
                    bola.vel_bola[0] *= -1
                    self.pontos[1] += 1

                    num_aleatorio = random.randrange(3, 50)
                    print(num_aleatorio)
                    if self.pontos[0] == num_aleatorio and self.pontos[1] == num_aleatorio:
                        self.bolas.append(
                            Bola(self, (LARGURA // 2, ALTURA // 2)))

                if bola.pos_bola[0] < 0 or bola.pos_bola[0] > LARGURA:
                    pygame.quit()
                    sys.exit()

                bola.desenhar()
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
