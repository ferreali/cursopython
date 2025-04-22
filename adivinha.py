#agora você esta atuando como desenvolvedor de jogos.Crie um jogo de adivinhação de palavras
# onde você irá sortear uma 
#palavra aleatória e o jogador terá 3 chances de acertar.Antes de cada tentativa do jogador você irá
# mostrar uma dica sobre a palavra.Se
#ele acertar ou não acertar em 3 tentativas,pergunte se ele quer outra palavra ou terminar o jogo.
# Desenvolva em python utilizando pyGame.
#altere o código para incluir um placar somando 1 para cada palavra certa e -0.33 para cada palavra errada.

import pygame
import random
import sys
from pygame.locals import *

# Inicializa o pygame
pygame.init()

# Configurações da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo de Adivinhação de Palavras')

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)

# Fontes
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Banco de palavras e dicas (palavra: [dicas])
word_bank = {
    "python": ["É uma linguagem de programação", "O nome vem de um animal", "É interpretada"],
    "jogo": ["É uma forma de entretenimento", "Pode ser eletrônico ou físico", "Tem regras"],
    "computador": ["Máquina eletrônica", "Processa dados", "Pode ter Windows ou Linux"],
    "programacao": ["Criação de software", "Envolve algoritmos", "Usa linguagens específicas"],
    "algoritmo": ["Sequência de passos", "Resolve um problema", "Base da programação"],
    "dados": ["Informação digital", "Pode ser estruturado ou não", "Matéria-prima da informação"],
    "inteligencia": ["Capacidade cognitiva", "Pode ser artificial", "Relacionada a aprendizado"],
    "internet": ["Rede mundial", "Conecta computadores", "Usa protocolos TCP/IP"]
}

def get_random_word():
    word = random.choice(list(word_bank.keys()))
    hints = word_bank[word]
    return word, hints

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    current_word, current_hints = get_random_word()
    attempts = 0
    max_attempts = 3
    input_text = ''
    game_active = True
    feedback = ''
    feedback_color = BLACK
    
    # Loop principal
    running = True
    while running:
        window.fill(WHITE)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if game_active:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if input_text.lower() == current_word.lower():
                            feedback = "Parabéns! Você acertou!"
                            feedback_color = GREEN
                            game_active = False
                        else:
                            attempts += 1
                            if attempts >= max_attempts:
                                feedback = f"Game over! A palavra era: {current_word}"
                                feedback_color = RED
                                game_active = False
                            else:
                                feedback = f"Incorreto! Tente novamente. Tentativas restantes: {max_attempts - attempts}"
                                feedback_color = RED
                        input_text = ''
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            else:
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # Reinicia o jogo com nova palavra
                        current_word, current_hints = get_random_word()
                        attempts = 0
                        input_text = ''
                        feedback = ''
                        game_active = True
                    elif event.key == K_n:
                        running = False
        
        # Desenha a interface
        draw_text("Jogo de Adivinhação de Palavras", font_large, BLUE, window, 100, 50)
        
        if game_active:
            # Mostra dica atual
            hint_index = min(attempts, len(current_hints) - 1)
            draw_text(f"Dica: {current_hints[hint_index]}", font_medium, BLACK, window, 100, 150)
            
            # Mostra tentativas restantes
            draw_text(f"Tentativas restantes: {max_attempts - attempts}", font_small, BLACK, window, 100, 200)
            
            # Caixa de entrada
            draw_text("Digite sua resposta:", font_medium, BLACK, window, 100, 250)
            pygame.draw.rect(window, GRAY, (100, 300, 600, 50))
            draw_text(input_text, font_medium, BLACK, window, 110, 310)
        else:
            # Feedback final
            draw_text(feedback, font_medium, feedback_color, window, 100, 200)
            draw_text("Deseja jogar novamente? (Y/N)", font_medium, BLACK, window, 100, 300)
        
        pygame.display.update()

if __name__ == "__main__":
    main()