import pygame
import sys
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Futebol")

# Cores
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Carrega as imagens (substitua por imagens reais se tiver)
# Aqui usaremos formas geométricas como placeholders
def create_player_surface():
    surface = pygame.Surface((40, 80), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, BLUE, (0, 0, 40, 80))  # Corpo
    pygame.draw.circle(surface, WHITE, (20, 20), 15)     # Cabeça
    return surface

def create_ball_surface():
    surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(surface, WHITE, (15, 15), 15)
    pygame.draw.polygon(surface, BLACK, [(15, 0), (30, 15), (15, 30), (0, 15)])
    return surface

def create_goal_surface():
    surface = pygame.Surface((100, 200), pygame.SRCALPHA)
    pygame.draw.rect(surface, WHITE, (0, 0, 10, 200))  # Trave esquerda
    pygame.draw.rect(surface, WHITE, (0, 0, 100, 10))  # Trave superior
    pygame.draw.rect(surface, WHITE, (90, 0, 10, 200))  # Trave direita
    return surface

# Cria as superfícies
player_img = create_player_surface()
ball_img = create_ball_surface()
goal_img = create_goal_surface()

# Posições iniciais
player_pos = [100, HEIGHT // 2]
ball_pos = [200, HEIGHT // 2]
goal_pos = [WIDTH - 110, HEIGHT // 2 - 100]

# Velocidades
player_speed = 5
ball_speed = [0, 0]
ball_moving = False

# Pontuação
score = 0
font = pygame.font.Font(None, 36)

# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Função para desenhar o campo
def draw_field():
    screen.fill(GREEN)
    # Linhas do campo
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100), 2)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 2)
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 70, 2)

# Função para verificar colisão
def check_collision(player_rect, ball_rect):
    return player_rect.colliderect(ball_rect)

# Função para chutar a bola
def kick_ball():
    # Calcula a direção do chute em relação ao gol
    direction_x = goal_pos[0] + 50 - ball_pos[0]
    direction_y = goal_pos[1] + 100 - ball_pos[1]
    
    # Normaliza o vetor e multiplica pela força do chute
    length = (direction_x**2 + direction_y**2)**0.5
    if length > 0:
        direction_x = direction_x / length * 10
        direction_y = direction_y / length * 10
    
    return [direction_x, direction_y]

# Função para verificar gol
def check_goal(ball_rect):
    goal_rect = pygame.Rect(goal_pos[0], goal_pos[1], 100, 200)
    return goal_rect.colliderect(ball_rect)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_moving:
                ball_speed = kick_ball()
                ball_moving = True
    
    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos[1] > 50:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - 130:
        player_pos[1] += player_speed
    if keys[pygame.K_LEFT] and player_pos[0] > 50:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 90:
        player_pos[0] += player_speed
    
    # Movimento da bola
    if ball_moving:
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]
        
        # Verifica colisão com bordas
        if ball_pos[0] <= 50 or ball_pos[0] >= WIDTH - 80:
            ball_speed[0] = -ball_speed[0] * 0.8
        if ball_pos[1] <= 50 or ball_pos[1] >= HEIGHT - 80:
            ball_speed[1] = -ball_speed[1] * 0.8
        
        # Verifica se a bola parou
        if abs(ball_speed[0]) < 0.1 and abs(ball_speed[1]) < 0.1:
            ball_moving = False
            ball_speed = [0, 0]
        else:
            # Aplica atrito
            ball_speed[0] *= 0.98
            ball_speed[1] *= 0.98
        
        # Verifica gol
        ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], 30, 30)
        if check_goal(ball_rect):
            score += 1
            ball_moving = False
            ball_pos = [200, HEIGHT // 2]
            ball_speed = [0, 0]
    
    # Verifica colisão entre jogador e bola
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 40, 80)
    ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], 30, 30)
    if check_collision(player_rect, ball_rect) and not ball_moving:
        # Empurra a bola
        ball_pos[0] = player_pos[0] + 50
    
    # Desenha o campo
    draw_field()
    
    # Desenha o gol
    screen.blit(goal_img, goal_pos)
    
    # Desenha a bola
    screen.blit(ball_img, ball_pos)
    
    # Desenha o jogador
    screen.blit(player_img, player_pos)
    
    # Desenha a pontuação
    score_text = font.render(f"Gols: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Atualiza a tela
    pygame.display.flip()
    
    # Controla a taxa de quadros
    clock.tick(60)

pygame.quit()
sys.exit()