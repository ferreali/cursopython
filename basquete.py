import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meu Time de Basquete")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)

# Relógio para controle de FPS
clock = pygame.time.Clock()
FPS = 60

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, number, team, is_controlled=False):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.color = BLUE if team == "home" else RED
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        
        # Número do jogador
        font = pygame.font.SysFont(None, 15)
        text = font.render(str(number), True, WHITE)
        text_rect = text.get_rect(center=(10, 10))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.has_ball = False
        self.team = team
        self.number = number
        self.is_controlled = is_controlled
        self.target = None
    
    def update(self, ball):
        keys = pygame.key.get_pressed()
        
        if self.is_controlled:
            # Movimentação com teclado
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            
            # Limitar movimento dentro da tela
            self.rect.x = max(0, min(WIDTH - 20, self.rect.x))
            self.rect.y = max(0, min(HEIGHT - 20, self.rect.y))
            
            # Passar a bola
            if keys[pygame.K_SPACE] and self.has_ball:
                self.has_ball = False
                # Encontrar jogador mais próximo na mesma equipe
                teammates = [p for p in players if p.team == self.team and p != self]
                if teammates:
                    closest = min(teammates, key=lambda p: math.dist((self.rect.x, self.rect.y), 
                                                                    (p.rect.x, p.rect.y)))
                    ball.pass_to(closest)
            
            # Arremessar
            if keys[pygame.K_a] and self.has_ball:
                self.has_ball = False
                ball.shoot()
        
        elif self.target:
            # Movimentação automática para o alvo
            dx = self.target[0] - self.rect.x
            dy = self.target[1] - self.rect.y
            distance = max(1, math.sqrt(dx*dx + dy*dy))
            
            if distance > 5:
                self.rect.x += dx / distance * self.speed
                self.rect.y += dy / distance * self.speed
            else:
                self.target = None
        
        # Se está perto da bola e não tem posse, tentar pegar
        if not self.has_ball and math.dist((self.rect.x, self.rect.y), 
                                          (ball.rect.x, ball.rect.y)) < 30:
            if ball.possessor is None or ball.possessor.team != self.team:
                self.has_ball = True
                ball.possessor = self
                ball.attached_to = self

# Classe da Bola
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (5, 5), 5)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.possessor = None
        self.attached_to = None
        self.speed = [0, 0]
        self.in_air = False
    
    def update(self):
        if self.attached_to:
            # A bola está com um jogador
            self.rect.center = self.attached_to.rect.center
        elif self.in_air:
            # A bola está em movimento
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            
            # Adicionar gravidade
            self.speed[1] += 0.2
            
            # Verificar se atingiu o chão
            if self.rect.y >= HEIGHT - 50:
                self.in_air = False
                self.speed = [0, 0]
                self.rect.y = HEIGHT - 55
    
    def pass_to(self, target):
        self.attached_to = None
        self.in_air = True
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        distance = max(1, math.sqrt(dx*dx + dy*dy))
        self.speed = [dx/distance * 5, dy/distance * 5]
        
        # Definir alvo para o receptor
        target.target = (self.rect.x + dx, self.rect.y + dy)
    
    def shoot(self):
        self.attached_to = None
        self.in_air = True
        # Arremessar em direção à cesta
        basket_x = random.choice([100, WIDTH-100])
        power = random.uniform(8, 12)
        
        dx = basket_x - self.rect.x
        dy = (HEIGHT - 150) - self.rect.y  # Altura da cesta
        distance = max(1, math.sqrt(dx*dx + dy*dy))
        self.speed = [dx/distance * power, dy/distance * power - 3]  # -3 para dar curva

# Classe da Quadra
def draw_court():
    # Fundo (madeira da quadra)
    pygame.draw.rect(screen, BROWN, (0, 0, WIDTH, HEIGHT))
    
    # Linhas da quadra
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 50, 2)
    
    # Cestas
    pygame.draw.rect(screen, RED, (90, HEIGHT-150, 20, 2))
    pygame.draw.rect(screen, BLUE, (WIDTH-110, HEIGHT-150, 20, 2))

# Criação dos objetos
players = pygame.sprite.Group()
ball = Ball()
all_sprites = pygame.sprite.Group(ball)

# Criar time da casa (azul)
for i, pos in enumerate([(200, 200), (300, 300), (400, 200), (200, 400), (300, 500)]):
    player = Player(pos[0], pos[1], i+1, "home", i==0)  # Jogador 1 é controlado
    players.add(player)
    all_sprites.add(player)

# Criar time visitante (vermelho)
for i, pos in enumerate([(600, 200), (500, 300), (400, 200), (600, 400), (500, 500)]):
    player = Player(pos[0], pos[1], i+1, "away")
    players.add(player)
    all_sprites.add(player)

# Dar a bola para o jogador controlado
for player in players:
    if player.is_controlled:
        player.has_ball = True
        ball.possessor = player
        ball.attached_to = player
        break

# Loop principal do jogo
running = True
while running:
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Trocar jogador controlado
                current_controlled = next(p for p in players if p.is_controlled)
                teammates = [p for p in players if p.team == current_controlled.team and p != current_controlled]
                if teammates:
                    current_controlled.is_controlled = False
                    new_controlled = random.choice(teammates)
                    new_controlled.is_controlled = True
                    
                    # Transferir a bola se o jogador atual a possuía
                    if current_controlled.has_ball:
                        current_controlled.has_ball = False
                        new_controlled.has_ball = True
                        ball.possessor = new_controlled
                        ball.attached_to = new_controlled
    
    # Atualizar sprites
    players.update(ball)
    ball.update()
    
    # Verificar se a bola entrou na cesta
    if not ball.in_air and ball.rect.y <= HEIGHT - 150 and ball.rect.y >= HEIGHT - 160:
        if 90 <= ball.rect.x <= 110:
            print("Ponto para o time visitante!")
            ball.rect.center = (WIDTH//2, HEIGHT//2)
        elif WIDTH-110 <= ball.rect.x <= WIDTH-90:
            print("Ponto para o time da casa!")
            ball.rect.center = (WIDTH//2, HEIGHT//2)
    
    # Desenhar tudo
    draw_court()
    all_sprites.draw(screen)
    
    # Mostrar instruções
    font = pygame.font.SysFont(None, 24)
    instructions = [
        "Setas: Mover",
        "Espaço: Passar",
        "A: Arremessar",
        "Tab: Trocar jogador"
    ]
    
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 25))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()