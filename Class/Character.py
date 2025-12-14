# classes/character.py
from abc import ABC, abstractmethod

class Character(ABC):
    """
    Class abstrak untuk semua karakter dalam game
    Mendemonstrasikan Encapsulation dengan atribut protected
    """
    
    def __init__(self, name, health, x, y):
        self._name = name  # Protected attribute
        self.__health = health  # Private attribute (Encapsulation)
        self._x = x
        self._y = y
        self._is_alive = True
    
    # Getter dan Setter (Encapsulation)
    def get_health(self):
        return self.__health
    
    def set_health(self, value):
        self.__health = max(0, value)
        if self.__health == 0:
            self._is_alive = False
    
    def get_position(self):
        return (self._x, self._y)
    
    def move(self, dx, dy):
        """Method untuk menggerakkan karakter"""
        self._x += dx
        self._y += dy
    
    def take_damage(self, damage):
        """Method untuk menerima damage"""
        self.__health -= damage
        if self.__health <= 0:
            self.__health = 0
            self._is_alive = False
    
    def is_alive(self):
        return self._is_alive
    
    @abstractmethod
    def attack(self):
        """Abstract method yang harus diimplementasi oleh child class"""
        pass