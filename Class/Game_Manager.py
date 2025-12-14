# classes/game_manager.py
import pygame
from Class.Player import Player
from Class.Monster import Monster, Boss
from Class.Question import Question
import random

class GameManager:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = None
        self.monsters = []
        self.current_question = None
        self.current_monster = None
        self.game_state = "MENU"  # MENU, PLAYING, QUESTION, GAME_OVER, WIN
        self.current_level = 1
        self.monsters_defeated = 0
        self.spawn_timer = 0
        
        # Cooldown untuk mencegah collision berulang dengan monster yang sama
        self.collision_cooldown = {}  # {monster_id: frame_counter}
        self.cooldown_duration = 60  # 2 detik di 30 FPS (atau 1 detik di 60 FPS)
        
        # BARU: Timer untuk menjawab soal
        self.question_timer = 0
        self.question_time_limit = 30 * 60  # 30 detik * 60 FPS = 1800 frames
        self.question_start_time = 0

        self.max_level = 10  # Level maksimal
        self.final_boss_spawned = False  # Flag final boss
        self.is_final_boss_battle = False  # Flag battle state
    
    def start_game(self, player_name):
        """Inisialisasi game baru"""
        self.player = Player(player_name)
        self.monsters = []
        self.current_level = 1
        self.monsters_defeated = 0
        self.game_state = "PLAYING"
        self.collision_cooldown = {}
        self.final_boss_spawned = False
        self.is_final_boss_battle = False
        self.spawn_monster()

    def spawn_monster(self):
   
     x = random.randint(600, 750)
     y = random.randint(50, 550)
    
     player_level = self.player.get_level()
    
    # Final Boss di level 10
     if player_level >= self.max_level and not self.final_boss_spawned:
        monster = Boss(f"FINAL BOSS", self.max_level * 2, x, y)
        self.final_boss_spawned = True
        self.is_final_boss_battle = True
        print("=== FINAL BOSS APPEARED! ===")
    
    # Boss biasa setiap 5 monster
     elif self.monsters_defeated > 0 and self.monsters_defeated % 5 == 0:
        monster = Boss(f"Boss {player_level}", player_level, x, y)
    
    # Monster biasa
     else:
        difficulty = min(player_level, 3)
        monster = Monster(f"Monster {len(self.monsters)}", difficulty, x, y)
    
     self.monsters.append(monster)
    
    def check_collision(self):
        """
        Cek collision antara player dan monster
        REVISI: Tambah cooldown untuk mencegah collision berulang + Start timer
        """
        player_x, player_y = self.player.get_position()
        
        for monster in self.monsters:
            # Cek cooldown untuk monster ini
            monster_id = id(monster)
            if monster_id in self.collision_cooldown:
                if self.collision_cooldown[monster_id] > 0:
                    continue  # Skip monster ini karena masih cooldown
            
            monster_x, monster_y = monster.get_position()
            distance = ((player_x - monster_x)**2 + (player_y - monster_y)**2)**0.5
            
            if distance < 50:  # Collision threshold
                # Trigger question
                question_text, answer = monster.get_question()
                self.current_question = Question(question_text, answer)
                self.current_monster = monster
                self.game_state = "QUESTION"
                
                # Set cooldown untuk monster ini
                self.collision_cooldown[monster_id] = self.cooldown_duration
                
                # BARU: Start timer untuk menjawab
                self.question_timer = self.question_time_limit
                
                return True
        
        return False
    
    def answer_question(self, user_answer):
     is_correct = self.current_question.check_answer(user_answer)
    
     if is_correct:
        # Player benar, monster mati
        reward = self.current_monster.get_reward_points()
        self.player.gain_score(reward)
        is_final_boss = False
        if self.is_final_boss_battle:
            # Check if current monster is a Boss (has special ability)
            if hasattr(self.current_monster, '_Boss__special_ability'):
                is_final_boss = True
        
        # Hapus monster dari list dan cooldown
        monster_id = id(self.current_monster)
        if monster_id in self.collision_cooldown:
            del self.collision_cooldown[monster_id]
        
        # Remove monster dari list
        if self.current_monster in self.monsters:
            self.monsters.remove(self.current_monster)
        
        self.monsters_defeated += 1
        
        if is_final_boss:
            print("DEBUG: Setting state to WIN!")
            self.game_state = "WIN"  # WIN!
            self.current_question = None
            self.current_monster = None
            self.question_timer = 0
            print("=== YOU DEFEATED THE FINAL BOSS! ===")
            print(f"DEBUG: Game state is now: {self.game_state}")
            return
        
        
     else:
        # Player salah, player kena damage
        damage = self.current_monster.attack()
        self.player.take_damage(damage)
        
        # Monster tidak mati, set cooldown
        monster_id = id(self.current_monster)
        self.collision_cooldown[monster_id] = self.cooldown_duration
        
        # Cek apakah player mati
        if not self.player.is_alive():
            self.player.lose_life()
            if self.player.get_lives() <= 0:
                self.game_state = "GAME_OVER"
                self.current_question = None
                self.current_monster = None
                self.question_timer = 0
                return
    
    # Game lanjut
     self.current_question = None
     self.current_monster = None
     self.question_timer = 0
     self.game_state = "PLAYING"
    
    def timeout_question(self):
        if self.current_monster is None:
            return
        
        # Player kena damage karena timeout
        damage = self.current_monster.attack()
        self.player.take_damage(damage)
        
        # Monster tidak mati, set cooldown
        monster_id = id(self.current_monster)
        self.collision_cooldown[monster_id] = self.cooldown_duration
        
        # Cek apakah player mati
        if not self.player.is_alive():
            self.player.lose_life()
            if self.player.get_lives() <= 0:
                self.game_state = "GAME_OVER"
                self.current_question = None
                self.current_monster = None
                self.question_timer = 0
                return
        
        # Game lanjut
        self.current_question = None
        self.current_monster = None
        self.question_timer = 0
        self.game_state = "PLAYING"
    
    def update(self):
        if self.game_state == "PLAYING":
            # Update cooldown timers
            for monster_id in list(self.collision_cooldown.keys()):
                self.collision_cooldown[monster_id] -= 1
                if self.collision_cooldown[monster_id] <= 0:
                    del self.collision_cooldown[monster_id]
            
            # Update monster AI
            player_x, player_y = self.player.get_position()
            
            for monster in self.monsters:
                if monster.is_alive():
                    monster.move_towards_player(player_x, player_y)
            
            # Check collision
            self.check_collision()
            
            # Spawn monster baru
            self.spawn_timer += 1
            if self.spawn_timer > 180 and len(self.monsters) < 3:  # Setiap 3 detik
                self.spawn_monster()
                self.spawn_timer = 0
        
        elif self.game_state == "QUESTION":
            # BARU: Update question timer
            self.question_timer -= 1
            
            # Kalau waktu habis, dianggap salah jawab
            if self.question_timer <= 0:
                self.timeout_question()
    
    def get_game_stats(self):
        """Return statistik game untuk ditampilkan"""
        return {
            'score': self.player.get_score(),
            'level': self.player.get_level(),
            'lives': self.player.get_lives(),
            'health': self.player.get_health(),
            'monsters_defeated': self.monsters_defeated,
            'current_wave': self.current_level
        }
    
    def get_remaining_time(self):
        if self.game_state == "QUESTION":
            return max(0, self.question_timer // 60)  # Convert frames ke detik
        return 0