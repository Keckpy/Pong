import sys
import asyncio
import pygame

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Codespaces Pong")
clock = pygame.time.Clock()

# Game Objects
paddle_w, paddle_h = 15, 90
p1_y = HEIGHT // 2 - paddle_h // 2
p2_y = HEIGHT // 2 - paddle_h // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5
ball_size = 20

score1, score2 = 0, 0
font = pygame.font.SysFont("Courier", 40, bold=True)

# Async loop is required to keep web versions responsive
async def main():
    global p1_y, p2_y, ball_x, ball_y, ball_dx, ball_dy, score1, score2
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Event tracking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input tracking
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and p1_y > 0: p1_y -= 5
        if keys[pygame.K_s] and p1_y < HEIGHT - paddle_h: p1_y += 5
        if keys[pygame.K_UP] and p2_y > 0: p2_y -= 5
        if keys[pygame.K_DOWN] and p2_y < HEIGHT - paddle_h: p2_y += 5

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Wall bounces
        if ball_y <= 0 or ball_y >= HEIGHT - ball_size:
            ball_dy *= -1

        # Paddle rects for collision
        p1_rect = pygame.Rect(50, p1_y, paddle_w, paddle_h)
        p2_rect = pygame.Rect(WIDTH - 50 - paddle_w, p2_y, paddle_w, paddle_h)
        ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

        if ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect):
            ball_dx *= -1.05

        # Score zones
        if ball_x < 0:
            score2 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = 5
        elif ball_x > WIDTH:
            score1 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = -5

        # Draw visuals
        pygame.draw.rect(screen, (255, 255, 255), p1_rect)
        pygame.draw.rect(screen, (255, 255, 255), p2_rect)
        pygame.draw.ellipse(screen, (255, 255, 255), ball_rect)
        
        score_surface = font.render(f"{score1}   {score2}", True, (255, 255, 255))
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # Yield control to the browser runner

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
