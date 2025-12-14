# classes/question.py
import random

class Question:
    """
    Class untuk mengelola soal matematika
    Mendemonstrasikan Encapsulation
    """
    
    def __init__(self, question_text, correct_answer):
        self.__question_text = question_text  # Private
        self.__correct_answer = correct_answer  # Private
        self.__options = self.__generate_options()
    
    def __generate_options(self):
        """Private method untuk generate pilihan jawaban"""
        options = [self.__correct_answer]
        
        # Generate 3 jawaban salah
        while len(options) < 4:
            wrong = self.__correct_answer + random.randint(-10, 10)
            if wrong not in options and wrong > 0:
                options.append(wrong)
        
        random.shuffle(options)
        return options
    
    def get_question_text(self):
        return self.__question_text
    
    def get_options(self):
        return self.__options
    
    def check_answer(self, user_answer):
        """Method untuk mengecek jawaban"""
        return user_answer == self.__correct_answer
    
    def get_correct_answer(self):
        return self.__correct_answer