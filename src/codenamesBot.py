import sys 
import os
import math
import numpy as np
from typing import Dict, List, Tuple
from random import randrange

sys.path.append(os.path.join(sys.path[0],'..','lib'))
import pygame
pygame.init()

class VectorModel:
    
    def __init__(self, vector_dict: Dict[str, np.ndarray]):
        # YOUR CODE HERE
        self.vector_dict = vector_dict
        
    def embed(self, word: str) -> np.ndarray:
        # YOUR CODE HERE
        if word in self.vector_dict:
            return self.vector_dict[word]
        else:
            return None
    
    def vector_size(self) -> int:
        # YOUR CODE HERE
        for w,e in self.vector_dict.items():
            return len(e)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        # YOUR CODE HERE
        if len(vec1) != self.vector_size() or len(vec2) != self.vector_size():            
            return None
        vec1_len = 0
        vec2_len = 0
        dot_product = 0
        for i in range(self.vector_size()):
            vec1_len += math.pow(vec1[i],2)
            vec2_len += math.pow(vec2[i],2)
            dot_product += vec1[i]*vec2[i]
        vec1_len = math.sqrt(vec1_len)
        vec2_len = math.sqrt(vec2_len)
        
        if vec1_len == 0 or vec2_len == 0:
            return None
        
        cosine_similarity = dot_product / (vec1_len*vec2_len)
        return cosine_similarity

    def most_similar(self, word: str, top_n: int=5) -> List[Tuple[str, float]]:
        # YOUR CODE HERE
        if word not in self.vector_dict:
            return None
        
        word_vec = self.embed(word)
        most_similar_words = self.most_similar_vec(word_vec,top_n+1)
        if len(most_similar_words)>0:
            if most_similar_words[0][0] == word:
                return most_similar_words[1:top_n+1]
            else:
                return most_similar_words[0:top_n]
        
    def most_similar_vec(self, vec: np.ndarray, top_n: int=5) -> List[Tuple[str, float]]:
        # YOUR CODE HERE
        most_similar_words = [None for i in range(top_n)]
        for w,e in self.vector_dict.items():                
            score = self.cosine_similarity(vec,e)
            if score == None:
                continue
            bumped_word = None
            for i in range(top_n):
                if most_similar_words[i] == None:
                    most_similar_words[i] = (w,score)
                    continue
                elif bumped_word != None:
                    temp_word = most_similar_words[i]
                    most_similar_words[i] = bumped_word
                    bumped_word = temp_word                 
                elif most_similar_words[i][1] < score:
                    bumped_word = most_similar_words[i]
                    most_similar_words[i] = (w,score)
        return most_similar_words

class GameWord:
    def __init__(self,word:str,belonging:int):
        self.word = word 
        self.belonging = belonging
        self.revealed = False

    def store_most_similar_words(self,most_similar_words:List[str]):
        self.most_similar_words = most_similar_words

    def add_shared_similar_word(self, shared_similar_word: str, score: float, sharing_words: List[GameWord])

    def reveal_belonging(self)
        self.revealed = True
        return self.belonging


class ClueWord:
    def __init__(self, word:str, scores: List[Tuple[GameWord,float]]) -> None:
        self.word = word 
        self.scores = scores 
        self.clue_given = False 
        self.sort_by_score()       

    def sort_by_score(self):
        pass 

    def get_clue_score(self,team:int) -> Tuple[int,float]:
        pass 

    def set_clue_give(self):
        self.clue_given = True 


class GameGenerator: 
    def __init__(self,possible_words: List[str]) -> None:
        self.game_words = []
        self.game_manager = None
        self.game_ui_creator = None
        self.clue_giver_bot = None
        self.guesser_bot = None
        self.vector_model = VectorModel(vector_dict)

    def generate_words(self, words_n: int=25) -> List[GameWord]:
        for i in range(words_n):
            word_name = "Test"

            # TODO: get random word name from pool

            newWord = GameWord(word_name)
            self.game_words.append(newWord)
        return self.game_words


    def assign_belongings(self, words: List[GameWord], bomb_n: int = 1, teamA_n: int = 9, teamB_n: int = 8) -> List[GameWord]:
        neutral_words_n = len(words) - bomb_n - teamA_n - teamB_n
        for word in words:
            correct_belonging_found = False
            while not correct_belonging_found:
                belonging = randrange(4)
                if (belonging == 0 and bomb_n > 0):
                    bomb_n -= 1
                    correct_belonging_found = True
                    word.belonging = belonging
                if (belonging == 1 and teamA_n > 0):
                    teamA_n -= 1
                    correct_belonging_found = True
                    word.belonging = belonging
                if (belonging == 2 and teamB_n > 0):
                    teamB_n -= 1
                    correct_belonging_found = True
                    word.belonging = belonging
                if (belonging == 3 and neutral_words_n > 0):
                    neutral_words_n -= 1
                    correct_belonging_found = True
                    word.belonging = belonging

        return words



    def create_clue_giver_bot(self):
        self.clue_giver_bot = ClueGiverBot(self.vector_model, 1, self.game_words)

    def create_guesser_bot(self):
        self.guesser_bot = GuesserBot(self.vector_model, 1, self.game_words)

    def create_game_manager(self):
        self.game_manager = GameManager()

    def create_game_ui_creator(self):
        self.game_ui_creator = GameUiCreator()

    def pass_game_ui_creator_to_game_manager(self):
        self.game_manager.game_ui_creator = self.game_ui_creator 
    
    def start_game(self):
        pass

class ClueGiverBot:
    def __init__(self, vector_model: VectorModel, team: int, game_words: List[GameWord], similar_word_cutoff: int=200) -> None:
        self.vector_model = vector_model
        self.team = team 
        self.game_words = game_words
        self.similar_word_cutoff = similar_word_cutoff
        self.possible_clues = []
        pass

    def get_most_similar_words(self):
        for game_word in self.game_words:
            game_word.store_most_similar_words(self.vector_model.most_similar(game_word.word,self.similar_word_cutoff))
    
    def get_shared_similar_words(self):
        pass 

    def get_best_clue(self)->ClueWord: 
        pass 
    
    def give_clue(self,clue:ClueWord):
        pass 

class GuesserBot:
    def __init__(self, vector_model: VectorModel, team: int, game_words: List[GameWord]) -> None:
        self.vector_model = vector_model
        self.team = team 
        self.game_words = game_words
        pass

    def take_guess(self,given_clue:Tuple[str,int]):
        most_similar = self.vector_model.most_similar(given_clue[0], 200)
        guesses = []
        for i in range(given_clue[1]):
            found_guess = False
            for ms in most_similar:
                if not found_guess:
                    ms_word = ms[0]
                    for game_word in self.game_words:
                        if ms_word === game_word.word:
                            found_guess = True
                            guesses.append(game_word)
                            break
        return guesses

    def handle_reveal(self,guess_was_right:bool):
        pass 

    def store_wrong_guess(self,given_clue:Tuple[str,int]):
        pass 

    def take_extra_guess(self):
        pass 

class WordButton:
    def __init__(self,game_word:GameWord,row:int,col:int,player_is_guesser:bool,game_manager,bg_img = None) -> None:
        self.game_word = game_word
        self.player_is_guesser = player_is_guesser
        self.game_manager = game_manager
        pass

    def draw(self):
        pass 

    def clicked(self):
        pass 

    def reveal_belonging(self):
        pass 

class GameManager:
    def __init__(self) -> None:
        self.game_ui_creator = None

    def set_game_ui_creator(self,game_ui_creator):
        self.game_ui_creator = game_ui_creator

class GameUiCreator:
    def __init__(self,game_words:List[GameWord],player_is_guesser:bool,game_manager:GameManager) -> None:
        self.game_words = game_words
        self.player_is_guesser = player_is_guesser
        self.word_buttons = []
        self.clue_input = None 
        self.clue_amount_input = None
        self.clue_display = None 
        self.clue_amount_display = None 
        self.create_game_ui()

    def create_game_ui(self):
        pass 

    def show_clue_from_bot(self,clue:Tuple[str,int]):
        pass 

    def reveal_player_guess(self,pressed_button:WordButton):
        pass 

    def reveal_bot_guess(self,bot_guess:GameWord):
        pass 
        
    

class GameManager_PlayerIsGuesser(GameManager):
    def __init__(self,game_words:List[GameWord],clue_giver_bot:ClueGiverBot) -> None:
        self.game_words = game_words
        self.clue_giver_bot = clue_giver_bot

    def start_game(self):
        pass 

    def get_clue_from_bot(self):
        pass 

    def handle_player_guess(self,pressed_button:WordButton):
        pass 

    def check_for_game_end(self) -> bool:
        pass 

    def enable_next_guess(self):
        pass 

    def end_turn(self):
        pass 

    def end_game(self):
        pass 

class GameManager_PlayerGivesClues(GameManager):
    def __init__(self,game_words: List[GameWord],guesser_bot:GuesserBot) -> None:
        self.game_words = game_words
        self.guesser_bot = guesser_bot

    def start_game(self):
        pass 

    def ask_for_player_clue(self):
        pass 

    def handle_player_clue(self,player_clue:Tuple(str,int)):
        pass 

    def get_guess_from_bot(self):
        pass

    def check_for_game_end(self) -> bool:
        pass 

    def end_turn(self):
        pass 

    def end_game(self):
        pass 
        



