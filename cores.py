import pygame
import sys
import random
from pygame.locals import *

# Inicializar o pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo de Cores para Crianças')

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
ROSA = (255, 192, 203)
CIANO = (0, 255, 255)
MARROM = (165, 42, 42)

# Lista de cores disponíveis no jogo
CORES_DISPONIVEIS = [
    ("Vermelho", VERMELHO),
    ("Verde", VERDE),
    ("Azul", AZUL),
    ("Amarelo", AMARELO),
    ("Roxo", ROXO),
    ("Laranja", LARANJA),
    ("Rosa", ROSA),
    ("Ciano", CIANO),
    ("Marrom", MARROM)
]

# Fontes
FONTE_GRANDE = pygame.font.Font(None, 72)
FONTE_PEQUENA = pygame.font.Font(None, 36)

# Variáveis do jogo
cor_alvo = None
cor_alvo_nome = ""
pontuacao = 0
tempo_restante = 60
ultimo_tempo = pygame.time.get_ticks()
acertos_consecutivos = 0

def escolher_cor_alvo():
    """Escolhe uma cor aleatória para ser o alvo"""
    global cor_alvo, cor_alvo_nome
    cor_alvo_nome, cor_alvo = random.choice(CORES_DISPONIVEIS)
    # Garantir que a próxima cor não seja a mesma
    while cor_alvo_nome == CORES_DISPONIVEIS[0][0] and len(CORES_DISPONIVEIS) > 1:
        cor_alvo_nome, cor_alvo = random.choice(CORES_DISPONIVEIS)

def desenhar_botoes():
    """Desenha os botões coloridos na tela"""
    botoes = []
    # Pegar 3 cores aleatórias, incluindo a cor alvo
    cores_btn = random.sample([c for c in CORES_DISPONIVEIS if c[0] != cor_alvo_nome], 2)
    cores_btn.append((cor_alvo_nome, cor_alvo))
    random.shuffle(cores_btn)
    
    for i, (nome, cor) in enumerate(cores_btn):
        btn_rect = pygame.Rect(150 + i * 200, 300, 150, 150)
        pygame.draw.rect(TELA, cor, btn_rect)
        pygame.draw.rect(TELA, PRETO, btn_rect, 3)  # Borda
        botoes.append((btn_rect, nome, cor))
    
    return botoes

def mostrar_pontuacao():
    """Mostra a pontuação e o tempo na tela"""
    texto_pontos = FONTE_PEQUENA.render(f"Pontos: {pontuacao}", True, PRETO)
    texto_tempo = FONTE_PEQUENA.render(f"Tempo: {tempo_restante}", True, PRETO)
    TELA.blit(texto_pontos, (20, 20))
    TELA.blit(texto_tempo, (LARGURA - 150, 20))

def tela_inicial():
    """Mostra a tela inicial do jogo"""
    TELA.fill(BRANCO)
    titulo = FONTE_GRANDE.render("Jogo de Cores", True, PRETO)
    subtitulo = FONTE_PEQUENA.render("Clique na cor que corresponde ao nome", True, PRETO)
    instrucao = FONTE_PEQUENA.render("Pressione qualquer tecla para começar", True, PRETO)
    
    TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))
    TELA.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 250))
    TELA.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, 350))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN or evento.type == MOUSEBUTTONDOWN:
                esperando = False

def tela_final():
    """Mostra a tela final com a pontuação"""
    TELA.fill(BRANCO)
    titulo = FONTE_GRANDE.render("Fim do Jogo!", True, PRETO)
    pontos = FONTE_PEQUENA.render(f"Sua pontuação: {pontuacao}", True, PRETO)
    instrucao = FONTE_PEQUENA.render("Pressione qualquer tecla para sair", True, PRETO)
    
    TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))
    TELA.blit(pontos, (LARGURA//2 - pontos.get_width()//2, 250))
    TELA.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, 350))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT or evento.type == KEYDOWN or evento.type == MOUSEBUTTONDOWN:
                esperando = False

def jogo_principal():
    """Loop principal do jogo"""
    global pontuacao, tempo_restante, ultimo_tempo, acertos_consecutivos
    
    escolher_cor_alvo()
    relogio = pygame.time.Clock()
    rodando = True
    
    while rodando:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo >= 1000:  # 1 segundo
            tempo_restante -= 1
            ultimo_tempo = tempo_atual
        
        if tempo_restante <= 0:
            rodando = False
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn_rect, nome, cor in botoes:
                    if btn_rect.collidepoint(pos):
                        if nome == cor_alvo_nome:
                            pontuacao += 1 + acertos_consecutivos // 3  # Bônus por acertos consecutivos
                            acertos_consecutivos += 1
                            escolher_cor_alvo()
                        else:
                            acertos_consecutivos = 0
                        break
        
        TELA.fill(BRANCO)
        
        # Mostrar o nome da cor alvo
        texto_cor = FONTE_GRANDE.render(cor_alvo_nome, True, PRETO)
        TELA.blit(texto_cor, (LARGURA//2 - texto_cor.get_width()//2, 150))
        
        # Desenhar os botões e atualizar a lista de botões
        botoes = desenhar_botoes()
        
        # Mostrar pontuação e tempo
        mostrar_pontuacao()
        
        # Feedback visual para acertos consecutivos
        if acertos_consecutivos > 0:
            bonus_text = FONTE_PEQUENA.render(f"Sequência: {acertos_consecutivos}", True, VERDE)
            TELA.blit(bonus_text, (LARGURA//2 - bonus_text.get_width()//2, 220))
        
        pygame.display.update()
        relogio.tick(30)

# Executar o jogo
tela_inicial()
jogo_principal()
tela_final()
pygame.quit()
sys.exit()