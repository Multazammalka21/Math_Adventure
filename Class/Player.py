# classes/player.py
from Class.Character import Character


class Player(Character):
    def __init__(self, name, x=100, y=400):
        super().__init__(name, health=100, x=x, y=y)
        self.__score = 0  # Private attribute
        self.__level = 1
        self.__lives = 3
        self.__speed = 5
    
    # Getters (Encapsulation)
    def get_score(self):
        return self.__score
    
    def get_level(self):
        return self.__level
    
    def get_lives(self):
        return self.__lives
    
    def get_speed(self):
        return self.__speed
    
    # Methods
    def answer_question(self, is_correct):
        """Method untuk memproses jawaban"""
        if is_correct:
            self.gain_score(10 * self.__level)
            return True
        else:
            self.take_damage(20)
            return False
    
    def gain_score(self, points):
        """Method untuk menambah score"""
        self.__score += points
        # Level up setiap 100 points
        if self.__score >= self.__level * 100:
            self.level_up()
    
    def level_up(self):
   
     if self.__level >= 10:
        return  # Stop di level 10
    
     self.__level += 1
     bonus_health = 20
     new_health = self.get_health() + bonus_health
     self.set_health(new_health)
     print(f"Level Up! Now level {self.__level}")
    
    def lose_life(self):
        """Method untuk kehilangan nyawa"""
        self.__lives -= 1
        if self.__lives > 0:
            self.set_health(100)  # Reset health
    
    def attack(self):
        """Override abstract method dari Character (Polymorphism)"""
        return 15 * self.__level
    
    def move_with_keys(self, keys):
        """Method khusus player untuk movement dengan keyboard"""
        if keys[0]:  # UP
            self.move(0, -self.__speed)
        if keys[1]:  # DOWN
            self.move(0, self.__speed)
        if keys[2]:  # LEFT
            self.move(-self.__speed, 0)
        if keys[3]:  # RIGHT
            self.move(self.__speed, 0)