# main.py - Version dengan Support Gambar (Fixed Path)
import pygame
import sys
import os

# Check if classes exist
try:
    from Class.Game_Manager import GameManager
except ImportError:
    print("ERROR: Classes not found!")
    print("Please create the following files first:")
    print("  - classes/__init__.py")
    print("  - classes/character.py")
    print("  - classes/player.py")
    print("  - classes/monster.py")
    print("  - classes/question.py")
    print("  - classes/game_manager.py")
    print("\nRefer to the tutorial for complete class implementations.")
    input("Press Enter to exit...")
    sys.exit(1)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Adventure")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game Manager
game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)

# ============= LOAD IMAGES =============
def safe_print(text):
    """Print dengan encoding yang aman untuk Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Ganti karakter Unicode dengan ASCII
        text = text.replace('✓', '[OK]').replace('✗', '[X]')
        print(text)

def load_image(filename, size=None):
    """
    Function untuk load gambar dengan error handling
    FIXED: Menggunakan path Asset/Image/ sesuai struktur folder Anda
    """
    try:
        path = os.path.join('Asset', 'Image', filename)
        
        if not os.path.exists(path):
            safe_print(f"[!] Image not found: {path}")
            return None
            
        image = pygame.image.load(path).convert_alpha()
        
        if size:
            image = pygame.transform.scale(image, size)
        
        safe_print(f"[OK] Loaded: {filename}")
        return image
    except pygame.error as e:
        safe_print(f"[X] Could not load image: {filename}")
        safe_print(f"    Error: {e}")
        return None

# Load all images
safe_print("\n=== Loading Assets ===")
player_img = load_image('Player.png', (40, 40))      
monster_img = load_image('Monster.png', (50, 50)) 
boss_img = load_image('Boss.png', (70, 70))          
background_img = load_image('Background.png', (SCREEN_WIDTH, SCREEN_HEIGHT))  
safe_print("======================\n")

def draw_background():
    """Gambar background, fallback ke gradient yang lebih keren jika tidak ada gambar"""
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        for y in range(400):
            # Gradient dari biru langit ke biru muda
            blue_val = int(135 + (y / 400) * 60)
            sky_color = (100, blue_val, 255)
            pygame.draw.line(screen, sky_color, (0, y), (SCREEN_WIDTH, y))
        
        # Grass (bawah)
        for y in range(400, SCREEN_HEIGHT):
            # Gradient hijau
            green_val = int(180 - ((y - 400) / 200) * 50)
            grass_color = (50, green_val, 50)
            pygame.draw.line(screen, grass_color, (0, y), (SCREEN_WIDTH, y))
        
        # Tambah clouds (awan sederhana)
        cloud_color = (255, 255, 255, 100)
        cloud_surface = pygame.Surface((100, 40))
        cloud_surface.set_alpha(100)
        cloud_surface.fill((255, 255, 255))
        
        # Gambar beberapa awan
        screen.blit(cloud_surface, (100, 80))
        screen.blit(cloud_surface, (300, 50))
        screen.blit(cloud_surface, (500, 100))
        screen.blit(cloud_surface, (650, 70))

def draw_entity(image, fallback_color, x, y, size):
    if image:
        # Gambar image dengan center di (x, y)
        rect = image.get_rect(center=(int(x), int(y)))
        screen.blit(image, rect)
    else:
        # Fallback: gambar lingkaran
        pygame.draw.circle(screen, fallback_color, (int(x), int(y)), size)

def draw_menu():
    """Menggambar menu utama"""
    draw_background()
    
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Title
    title = font.render("MATH ADVENTURE", True, WHITE)
    title_shadow = font.render("MATH ADVENTURE", True, BLACK)
    
    # Center title
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
    title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, 202))
    
    screen.blit(title_shadow, title_shadow_rect)
    screen.blit(title, title_rect)
    
    # Instructions - CENTERED
    subtitle = small_font.render("Tekan SPACE Untuk Mulai", True, WHITE)
    instructions = small_font.render("Gunakan Tombol Panah Untuk Bergerak", True, WHITE)
    credits = small_font.render("Jawab Pertanyaan Matematika Untuk Mengalahkan Monster!", True, (200, 200, 200))
    
    # Get rect for centering
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 300))
    instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, 350))
    credits_rect = credits.get_rect(center=(SCREEN_WIDTH//2, 400))
    
    # Blit centered text
    screen.blit(subtitle, subtitle_rect)
    screen.blit(instructions, instructions_rect)
    screen.blit(credits, credits_rect)

def draw_game():
    """Menggambar game state"""
    draw_background()
    
    # Draw Player
    player_x, player_y = game_manager.player.get_position()
    draw_entity(player_img, BLUE, player_x, player_y, 20)
    
    # Draw player name tag
    name_text = small_font.render("YOU", True, WHITE)
    name_bg = pygame.Surface((40, 20))
    name_bg.fill(BLACK)
    name_bg.set_alpha(150)
    screen.blit(name_bg, (player_x - 20, player_y - 40))
    screen.blit(name_text, (player_x - 15, player_y - 38))
    
    # Draw Monsters
    for monster in game_manager.monsters:
        monster_x, monster_y = monster.get_position()
        
        # Check if it's a Boss
        is_boss = hasattr(monster, '_Boss__special_ability')
        
        if is_boss:
            draw_entity(boss_img, (150, 0, 0), monster_x, monster_y, 35)
            label = small_font.render("BOSS", True, RED)
        else:
            draw_entity(monster_img, RED, monster_x, monster_y, 25)
            label = small_font.render(f"Lv.{monster.get_difficulty()}", True, WHITE)
        
        # Monster label background
        label_bg = pygame.Surface((50, 20))
        label_bg.fill(BLACK)
        label_bg.set_alpha(150)
        screen.blit(label_bg, (monster_x - 25, monster_y - 50))
        screen.blit(label, (monster_x - 20, monster_y - 48))
    
    # Draw HUD Panel (Stats)
    panel_height = 180
    panel = pygame.Surface((250, panel_height))
    panel.fill((0, 0, 0))
    panel.set_alpha(180)
    screen.blit(panel, (10, 10))
    progress_y = 145

    # Progress label
    progress_label = small_font.render("TO FINAL:", True, (255, 255, 0))
    screen.blit(progress_label, (20, progress_y))

    # Progress bar
    bar_width = 210
    bar_height = 15
    bar_x = 20
    bar_y = progress_y + 25
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

    # Fill based on level
    current_level = game_manager.player.get_level()
    max_level = game_manager.max_level
    fill_percentage = min(current_level / max_level, 1.0)
    fill_width = int(bar_width * fill_percentage)
    
    # Color gradient
    if fill_percentage < 0.5:
        bar_color = (0, 255, 0)  # Green
    elif fill_percentage < 0.8:
        bar_color = (255, 255, 0)  # Yellow
    else:
        bar_color = (255, 215, 0)  # Gold
    
    if fill_width > 0:
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
    
    # Border
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    # Text
    progress_text = small_font.render(f"Lv {current_level}/{max_level}", True, WHITE)
    screen.blit(progress_text, (bar_x + 70, bar_y - 2))

    
    # Draw Stats with better formatting
    stats = game_manager.get_game_stats()
    
    y_offset = 20
    stats_data = [
        ("SCORE", stats['score'], GREEN),
        ("LEVEL", stats['level'], BLUE),
        ("HEALTH", f"{stats['health']}", RED if stats['health'] < 30 else WHITE),
        ("LIVES", "♥" * stats['lives'], RED),
        ("DEFEATED", stats['monsters_defeated'], (255, 255, 0))
    ]
    
    for label, value, color in stats_data:
        label_text = small_font.render(f"{label}:", True, WHITE)
        value_text = small_font.render(str(value), True, color)
        screen.blit(label_text, (20, y_offset))
        screen.blit(value_text, (150, y_offset))
        y_offset += 25

def draw_question():
    """Menggambar layar pertanyaan dengan TIMER"""
    draw_background()
    
    # Darken background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Question box
    box_width = 600
    box_height = 450  # Lebih tinggi untuk timer
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = (SCREEN_HEIGHT - box_height) // 2
    
    # Draw box with border
    pygame.draw.rect(screen, (30, 30, 100), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 3)
    
    # Question title
    title = font.render("SOLVE THIS!", True, (255, 255, 0))
    screen.blit(title, (box_x + 200, box_y + 30))
    
    # TIMER DISPLAY
    remaining_time = game_manager.get_remaining_time()
    
    # Timer bar background
    timer_bar_width = 500
    timer_bar_x = box_x + 50
    timer_bar_y = box_y + 80
    pygame.draw.rect(screen, (50, 50, 50), (timer_bar_x, timer_bar_y, timer_bar_width, 30))
    
    # Timer bar fill (warna berubah sesuai waktu)
    time_percentage = remaining_time / 30.0
    fill_width = int(timer_bar_width * time_percentage)
    
    if time_percentage > 0.5:
        timer_color = GREEN
    elif time_percentage > 0.25:
        timer_color = (255, 255, 0)  # Yellow
    else:
        timer_color = RED
    
    if fill_width > 0:
        pygame.draw.rect(screen, timer_color, (timer_bar_x, timer_bar_y, fill_width, 30))
    
    # Timer border
    pygame.draw.rect(screen, WHITE, (timer_bar_x, timer_bar_y, timer_bar_width, 30), 2)
    
    # Timer text
    timer_text = small_font.render(f"Time: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (box_x + 260, timer_bar_y + 5))
    
    # Question text
    question_text = font.render(game_manager.current_question.get_question_text(), True, WHITE)
    screen.blit(question_text, (box_x + 180, box_y + 130))
    
    # Options with better styling
    options = game_manager.current_question.get_options()
    option_labels = ['1', '2', '3', '4']
    
    for i, (label, option) in enumerate(zip(option_labels, options)):
        option_y = box_y + 200 + i * 50
        
        # Option button background
        button_rect = pygame.Rect(box_x + 100, option_y, 400, 40)
        pygame.draw.rect(screen, (50, 50, 150), button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 2)
        
        # Option text
        option_text = small_font.render(f"[{label}]  {option}", True, WHITE)
        screen.blit(option_text, (box_x + 120, option_y + 10))
    
    # Instructions
    instruction = small_font.render("Tekan 1, 2, 3, Atau 4 Untuk Jawab", True, (200, 200, 200))
    instruction_rect = instruction.get_rect(center=(box_x + box_width//2, box_y + 410))
    screen.blit(instruction, instruction_rect)

def draw_game_over():
    """Menggambar layar game over"""
    draw_background()
    
    # Darken background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    stats = game_manager.get_game_stats()
    
    # Title with shadow effect
    title_shadow = font.render("GAME OVER", True, BLACK)
    title = font.render("GAME OVER", True, RED)
    screen.blit(title_shadow, (SCREEN_WIDTH//2 - 98, 152))
    screen.blit(title, (SCREEN_WIDTH//2 - 100, 150))
    
    # Stats box
    box_width = 400
    box_height = 200
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = 250
    
    pygame.draw.rect(screen, (50, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, RED, (box_x, box_y, box_width, box_height), 3)
    
    # Final stats
    score = small_font.render(f"Final Score: {stats['score']}", True, WHITE)
    level = small_font.render(f"Reached Level: {stats['level']}", True, WHITE)
    defeated = small_font.render(f"Monsters Defeated: {stats['monsters_defeated']}", True, WHITE)
    
    screen.blit(score, (box_x + 100, box_y + 40))
    screen.blit(level, (box_x + 100, box_y + 80))
    screen.blit(defeated, (box_x + 100, box_y + 120))
    
    # Restart instruction
    restart = small_font.render("Tekan R Untuk Restart Atau Q Untuk Keluar", True, (255, 255, 0))
    restart_rect = restart.get_rect(center=(SCREEN_WIDTH//2, 500))
    screen.blit(restart, restart_rect)

def draw_win_screen():
    """Menggambar layar kemenangan"""
    draw_background()
    
    # Darken background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    stats = game_manager.get_game_stats()
    
    # Title with gold color
    title_font = pygame.font.Font(None, 72)
    title = title_font.render("YOU WIN!", True, (255, 215, 0))
    title_shadow = title_font.render("YOU WIN!", True, BLACK)
    screen.blit(title_shadow, (SCREEN_WIDTH//2 - 148, 102))
    screen.blit(title, (SCREEN_WIDTH//2 - 150, 100))
    
    # Congratulations message
    congrats = font.render("CONGRATULATIONS!", True, (255, 255, 0))
    screen.blit(congrats, (SCREEN_WIDTH//2 - 150, 180))
    
    # Stats box
    box_width = 400
    box_height = 250
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = 240
    
    pygame.draw.rect(screen, (0, 100, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (255, 215, 0), (box_x, box_y, box_width, box_height), 3)
    
    # Final stats
    y_offset = box_y + 30
    
    stats_text = [
        f"Final Score: {stats['score']}",
        f"Final Level: {stats['level']}",
        f"Monsters Defeated: {stats['monsters_defeated']}",
        f"Remaining Health: {stats['health']}",
        f"Remaining Lives: {stats['lives']}"
    ]
    
    for text in stats_text:
        stat_render = small_font.render(text, True, WHITE)
        screen.blit(stat_render, (box_x + 80, y_offset))
        y_offset += 35
    
    # Victory message
    victory = small_font.render("You are a Math Master!", True, (255, 255, 0))
    screen.blit(victory, (SCREEN_WIDTH//2 - 130, 510))
    
    # Options
    restart = small_font.render("Tekan R Untuk Main Lagi Atau Q Untuk Keluar", True, (200, 200, 200))
    restart_rect = restart.get_rect(center=(SCREEN_WIDTH//2, 550))
    screen.blit(restart, restart_rect)

# ============= MAIN GAME LOOP =============
safe_print("\nStarting game...")
safe_print("If you see 'Image not found' messages above, the game will use colored shapes instead.")
safe_print("\n")

running = True
while running:
    clock.tick(FPS)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Menu State
            if game_manager.game_state == "MENU":
                if event.key == pygame.K_SPACE:
                    game_manager.start_game("Player")
            
            # Question State
            elif game_manager.game_state == "QUESTION":
                options = game_manager.current_question.get_options()
                if event.key == pygame.K_1 and len(options) > 0:
                    game_manager.answer_question(options[0])
                elif event.key == pygame.K_2 and len(options) > 1:
                    game_manager.answer_question(options[1])
                elif event.key == pygame.K_3 and len(options) > 2:
                    game_manager.answer_question(options[2])
                elif event.key == pygame.K_4 and len(options) > 3:
                    game_manager.answer_question(options[3])
            
            elif game_manager.game_state == "WIN":
                if event.key == pygame.K_r:
                    game_manager.start_game("Player")
                elif event.key == pygame.K_q:
                    running = False
            
            # Game Over State
            elif game_manager.game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    game_manager.start_game("Player")
                elif event.key == pygame.K_q:
                    running = False
    
    # Player Movement (Playing State)
    if game_manager.game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        movement = [
            keys[pygame.K_UP],
            keys[pygame.K_DOWN],
            keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT]
        ]
        game_manager.player.move_with_keys(movement)
        
        # Keep player in bounds
        x, y = game_manager.player.get_position()
        x = max(20, min(SCREEN_WIDTH - 20, x))
        y = max(20, min(SCREEN_HEIGHT - 20, y))
        game_manager.player._x = x
        game_manager.player._y = y
    
    # Update Game
    game_manager.update()
    
    # Drawing
    if game_manager.game_state == "MENU":
        draw_menu()
    elif game_manager.game_state == "PLAYING":
        draw_game()
    elif game_manager.game_state == "QUESTION":
        draw_question()
    elif game_manager.game_state == "WIN":
        draw_win_screen()
    elif game_manager.game_state == "GAME_OVER":
        draw_game_over()
    
    pygame.display.flip()

pygame.quit()
sys.exit()