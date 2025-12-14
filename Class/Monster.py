# classes/monster.py
from Class.Character import Character
import random

class Monster(Character):
    """
    Class Monster mewarisi Character (Inheritance)
    """
    
    def __init__(self, name, difficulty, x, y):
        health = 30 + (difficulty * 20)
        super().__init__(name, health, x, y)
        self.__difficulty = difficulty  # Private (Encapsulation)
        self.__reward_points = 10 * difficulty
        self.__speed = 2 + difficulty
    
    def get_difficulty(self):
        return self.__difficulty
    
    def get_reward_points(self):
        return self.__reward_points
    
    def attack(self):
        """Override method attack (Polymorphism)"""
        return 10 + (self.__difficulty * 5)
    
    def move_towards_player(self, player_x, player_y):
        """AI sederhana untuk mengejar player"""
        if self._x < player_x:
            self._x += self.__speed
        elif self._x > player_x:
            self._x -= self.__speed
            
        if self._y < player_y:
            self._y += self.__speed
        elif self._y > player_y:
            self._y -= self.__speed
    
    def get_question(self):
        """Generate soal berdasarkan difficulty"""
        if self.__difficulty == 1:
            # Penjumlahan sederhana
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            question = f"{a} + {b} = ?"
            answer = a + b
        elif self.__difficulty == 2:
            # Pengurangan dan perkalian
            a = random.randint(1, 12)
            b = random.randint(1, 12)
            question = f"{a} × {b} = ?"
            answer = a * b
        else:
            # Pembagian
            b = random.randint(2, 10)
            answer = random.randint(2, 15)
            a = answer * b
            question = f"{a} ÷ {b} = ?"
        
        return question, answer


class Boss(Monster):
    """
    Class Boss mewarisi Monster (Multi-level Inheritance)
    Mendemonstrasikan Polymorphism dengan special ability
    """
    
    def __init__(self, name, difficulty, x, y):
        super().__init__(name, difficulty + 2, x, y)
        self.__special_ability = "Multi-Question"
        self.__special_cooldown = 0
    
    def attack(self):
        """Override attack dengan damage lebih besar (Polymorphism)"""
        base_damage = super().attack()
        return base_damage * 2
    
    def special_attack(self):
        """Method khusus Boss"""
        if self.__special_cooldown == 0:
            self.__special_cooldown = 5
            return True  # Trigger multiple questions
        return False
    
    def update_cooldown(self):
        if self.__special_cooldown > 0:
            self.__special_cooldown -= 1
    
    def get_question(self):
        """Override untuk soal lebih sulit (Polymorphism)"""
        # Soal kombinasi operasi
        a = random.randint(5, 20)
        b = random.randint(2, 10)
        c = random.randint(1, 10)
        
        operations = [
            (f"({a} + {b}) × {c} = ?", (a + b) * c),
            (f"{a} × {b} - {c} = ?", a * b - c),
            (f"({a} - {b}) × {c} = ?", (a - b) * c)
        ]
        
        question, answer = random.choice(operations)
        return question, answer