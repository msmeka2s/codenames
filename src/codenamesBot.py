import sys 
import os
import math
import random
import numpy as np
import pickle 
from typing import Dict, List, Tuple
from random import randint, randrange

from pygame import key
from pygame.draw import rect
from pygame.version import PygameVersion

sys.path.append(os.path.join(sys.path[0],'..','lib'))
import pygame
pygame.init()
pygame.font.init()

codenames_font = pygame.font.SysFont('Calibri',35)
header_font = pygame.font.SysFont('Calibri',80)
# --- GLOBAL VARIABLES
# window
window_size = (1200,960)
window_bg_color = (221,207,180)
# standard values
element_height = 110
standard_btn_color = (150,150,150)
standard_font_color = (0,0,0)
# word button
word_button_size = (200,element_height)
word_button_color_hover = (200,200,200)
word_button_color_neutral = (250,250,150)
word_button_color_teamA = (232,93,100)
word_button_color_teamB = (104,168,232)
word_button_color_bomb = (0,0,0)
font_color_bomb = (200,200,200)
# clue input
clue_word_size = (500,element_height)
clue_amount_size = (150,element_height)
clue_send_btn_size = (250,element_height)
clue_color = (200,240,200)
clue_frame_color = (130,220,80)
clue_font_color = (150,150,150)
clue_send_btn_font_color = (255,255,255)
# game text 
game_text_size = (window_size[0],element_height)
# menu button colors
clue_giver_color = (220,140,110)
guesser_color = (170,110,230)
disabled_color = (200,200,180)
disabled_font_color = (190,190,170)

# variables
player_typing = False 

class ButtonElement:
    def __init__(self,callback_object,rect:pygame.rect,text:str,interactable:bool,font=codenames_font,font_color=standard_font_color,bg_color=standard_btn_color,hover_color=None,active_color=None,active_font_color=None) -> None:
        self.rect = rect
        self.text = text
        self.interactable = interactable
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        self.draw_color = bg_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.active_font_color = active_font_color
        self.callback_object = callback_object
        self.active = False

    def check_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            # hover 
            if self.hover_color is not None and not self.active:
                self.draw_color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.callback_object.button_callback(self)                
        else:
            if not self.active:
                self.draw_color = self.bg_color

    def set_active(self,active):
        self.active = active
        if active:
            if self.active_color is not None:
                self.draw_color = self.active_color
            if self.active_font_color is not None:
                self.font_color = self.active_font_color
        else:
            self.draw_color = self.bg_color

    def draw(self,win):
        if self.interactable:            
            self.check_mouse()
        
        pygame.draw.rect(win,self.draw_color,self.rect,border_radius=10)
        text_surface = self.font.render(self.text,True,self.font_color)
        text_rect = text_surface.get_rect(center=(self.rect[0]+self.rect[2]/2,self.rect[1]+self.rect[3]/2))
        win.blit(text_surface,(text_rect))


class MainMenu:
    def __init__(self) -> None:
        self.bg = None
        # Choose Team 
        self.header_rect = pygame.Rect(0,0,window_size[0],2*element_height)
        self.team_text_rect = pygame.Rect(0,self.header_rect[3],window_size[0],element_height)
        self.team_a_rect = pygame.Rect(window_size[0]/2 - 3/2 * word_button_size[0],self.team_text_rect[1]+self.team_text_rect[3],word_button_size[0],word_button_size[1])
        self.team_a_btn = ButtonElement(self,self.team_a_rect,"Team Red",True,hover_color=word_button_color_hover,active_color=word_button_color_teamA)
        self.team_b_rect = pygame.Rect(window_size[0]/2 + 1/2 * word_button_size[0],self.team_text_rect[1]+self.team_text_rect[3],word_button_size[0],word_button_size[1])
        self.team_b_btn = ButtonElement(self,self.team_b_rect,"Team Blue",True,hover_color=word_button_color_hover,active_color=word_button_color_teamB)
        # Choose Role
        self.role_text_rect = pygame.Rect(0,self.team_a_rect[1]+self.team_a_rect[3],window_size[0],element_height)
        self.clue_giver_rect = pygame.Rect(window_size[0]/2 - 3/2 * word_button_size[0],self.role_text_rect[1]+self.role_text_rect[3],word_button_size[0],word_button_size[1])
        self.clue_giver_btn = ButtonElement(self,self.clue_giver_rect,"Clue Giver",True,hover_color=word_button_color_hover,active_color=clue_giver_color)
        self.guesser_rect = pygame.Rect(window_size[0]/2 + 1/2 * word_button_size[0],self.role_text_rect[1]+self.role_text_rect[3],word_button_size[0],word_button_size[1])
        self.guesser_btn = ButtonElement(self,self.guesser_rect,"Guesser",True,hover_color=word_button_color_hover,active_color=guesser_color)
        # Start Game
        self.start_game_rect = pygame.Rect(window_size[0]/2 - word_button_size[0]/2,self.clue_giver_rect[1]+self.clue_giver_rect[3]+element_height,word_button_size[0],word_button_size[1])
        self.start_game_btn = ButtonElement(self,self.start_game_rect,"Start Game",False,bg_color=disabled_color,font_color=disabled_font_color,active_color=clue_frame_color)
        self.chosen_team = None
        self.chosen_role = None
        self.start_game = False 
       
    def create_main_menu(self):
        pass

    def put_text(self,text:str,rect,font = codenames_font,text_color = standard_font_color):
        text_surface = font.render(text,True,text_color)
        text_rect = text_surface.get_rect(center=(rect[0]+rect[2]/2,rect[1]+rect[3]/2))
        win.blit(text_surface,(text_rect))

    def button_callback(self,button):
        if button == self.team_a_btn:
            self.chosen_team = "team_a"
            self.team_a_btn.set_active(True)
            self.team_b_btn.set_active(False)
        elif button == self.team_b_btn:
            self.chosen_team = "team_b"
            self.team_a_btn.set_active(False)
            self.team_b_btn.set_active(True)
        elif button == self.clue_giver_btn:
            self.chosen_role = "clue_giver"
            self.clue_giver_btn.set_active(True)
            self.guesser_btn.set_active(False)
        elif button == self.guesser_btn:
            self.chosen_role = "guesser"
            self.clue_giver_btn.set_active(False)
            self.guesser_btn.set_active(True)
        elif button == self.start_game_btn:
            self.start_game = True 
        if self.chosen_team is not None and self.chosen_role is not None:
            self.start_game_btn.interactable = True
            self.start_game_btn.set_active(True)
            self.start_game_btn.font_color = (255,255,255)


    def draw(self,win):
        self.put_text("Main Menu",self.header_rect,font = header_font)
        self.put_text("Choose Your Team", self.team_text_rect)
        self.team_a_btn.draw(win)
        self.team_b_btn.draw(win)
        self.put_text("Choose Your Role", self.role_text_rect)
        self.clue_giver_btn.draw(win)
        self.guesser_btn.draw(win)
        self.start_game_btn.draw(win)

    def redraw_game_window(self):        
        if self.bg != None:
            win.blit(self.bg,(0,0))
        else:
            win.fill(window_bg_color)
        self.draw(win)
        pygame.display.update()   

class VectorModel: # Max    
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

class GameWord: # Florian
    def __init__(self,word:str,belonging:int):
        self.word = word 
        self.belonging = belonging
        self.revealed = False

    def store_most_similar_words(self,most_similar_words:List[str]):
        self.most_similar_words = most_similar_words


    def add_shared_similar_word(self, shared_similar_word: str, score: float, sharing_words):
        pass

    def reveal_belonging(self)->int:
        self.revealed = True
        return self.belonging

    @staticmethod 
    def  lookup_belonging(name:str)->int:
        if name == "bomb":
            return 0
        elif name == "team_a":
            return 1

        elif name == "team_b":
            return 2

        elif name == "neutral":
            return 3


class ClueWord: # Florian
    def __init__(self, word:str, scores: List[Tuple[GameWord,float]]) -> None:
        self.word = word 
        self.scores = scores 
        self.clue_given = False 
        self.clue_score = 0
        self.sort_by_score()       

    def sort_by_score(self):
        pass 

    def get_clue_score(self,team:int) -> Tuple[int,float]:
        pass 

    def set_clue_given(self):
        self.clue_given = True 


class GameGenerator: # Max
    def __init__(self,possible_words: List[str],player_team:int,player_is_guesser:bool) -> None:
        self.possible_words = possible_words
        self.game_words = []
        self.player_team = player_team
        self.player_is_guesser = player_is_guesser
        self.game_manager = None
        self.game_ui_creator = None
        self.clue_giver_bot = None
        self.guesser_bot = None        
        self.vector_model = None
        self.setup_game()

    def setup_game(self):
        self.generate_words()
        self.assign_belongings(self.game_words)
        if self.player_is_guesser:
            self.create_clue_giver_bot()
        else:
            self.create_guesser_bot()
        self.create_game_manager()
        self.create_game_ui_creator()
        self.start_game()

    def generate_words(self, words_n: int=25) -> List[GameWord]:
        possible_words = self.possible_words.copy()
        self.game_words.clear()
        for i in range(words_n):
            index = random.randrange(len(possible_words))            
            game_word = GameWord(possible_words[index],-1)
            self.game_words.append(game_word)         
            possible_words.pop(index)           
            
        return self.game_words

    def assign_belongings(self, words: List[GameWord], bomb_n: int = 1, teamA_n: int = 9, teamB_n: int = 8) -> List[GameWord]:
        neutral_words_n = len(words) - bomb_n - teamA_n - teamB_n
        game_words_copy = self.game_words.copy()

        def assign_belonging(amount,belonging,remaining_words):
            for i in range(amount):
                index = random.randrange(len(remaining_words))
                remaining_words[index].belonging = belonging
                remaining_words.pop(index)
            return remaining_words            

        game_words_copy = assign_belonging(bomb_n,0,game_words_copy)
        game_words_copy = assign_belonging(teamA_n,1,game_words_copy)
        game_words_copy = assign_belonging(teamB_n,2,game_words_copy)
        game_words_copy = assign_belonging(neutral_words_n,3,game_words_copy)

        return self.game_words


    def create_clue_giver_bot(self):
        self.clue_giver_bot = ClueGiverBot(self.vector_model, self.player_team, self.game_words)

    def create_guesser_bot(self):
        self.guesser_bot = GuesserBot(self.vector_model, self.player_team, self.game_words)

    def create_game_manager(self):
        if self.player_is_guesser:
            self.game_manager = GameManager_PlayerIsGuesser(self.game_words,self.clue_giver_bot)
        else:
            self.game_manager = GameManager_PlayerIsClueGiver(self.game_words,self.guesser_bot)

    def create_game_ui_creator(self):
        self.game_ui_creator = GameUiCreator(self.game_words,self.player_is_guesser,self.player_team,self.game_manager)
    
    def start_game(self):
        pass

class ClueGiverBot: # Florian
    def __init__(self, vector_model, team: int, game_words: List[GameWord], similar_word_cutoff: int=200) -> None:
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
        for i in range(self.game_words):
            word = self.game_words[i]
            for similar_word in word.most_similar_words:
                clue_word = None
                for j in range(i+1,len(self.game_words)):
                    compare_word = self.game_words[j]
                    for possible_clue in compare_word.most_similar_words:
                        if similar_word == possible_clue:
                            if clue_word is None:
                                clue_scores = []
                                clue_scores.append((word,self.vector_model.cosine_similarity(self.vector_model.embed(word.word),self.vector_model.embed(similar_word))))
                                clue_scores.append((compare_word,self.vector_model.cosine_similarity(self.vector_model.embed(compare_word.word),self.vector_model.embed(possible_clue))))
                                clue_word = ClueWord(possible_clue,clue_scores)    
                                self.possible_clues.append(clue_word)                            
                            else:
                                clue_word.scores.append((compare_word,self.vector_model.cosine_similarity(self.vector_model.embed(compare_word.word),self.vector_model.embed(possible_clue))))
    
    def get_best_clue(self)->ClueWord: 
        if len(self.possible_clues>0):
            self.possible_clues[0].get_clue_score()
            best_clue = self.possible_clues[0]
        for clue_word in self.possible_clues:
            if clue_word.get_clue_score() > best_clue.clue_score:
                best_clue = clue_word
        return best_clue
    
    def give_clue(self,clue:ClueWord):
        pass 

class GuesserBot: # Max
    def __init__(self, vector_model, team: int, game_words: List[GameWord]) -> None:
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
                        if ms_word == game_word.word:
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

class WordButton: # Florian
    def __init__(self,game_word:GameWord,pos_x:int,pos_y:int,game_manager,bg_img = None) -> None:
        self.game_word = game_word        
        self.game_manager = game_manager        
        self.rect = pygame.Rect(pos_x,pos_y,word_button_size[0],word_button_size[1])
        self.active_color = None
        self.active_font_color = None
        self.font_color = standard_font_color
        self.get_active_color()
        self.button = ButtonElement(self,self.rect,self.game_word.word,False,font_color=self.font_color,hover_color=word_button_color_hover,active_color=self.active_color,active_font_color=self.active_font_color)

    def draw(self,win):        
        self.button.draw(win)

    def set_active(self):
        self.button.set_active(True)
        
    def button_callback(self,button):
        self.get_active_color() 

    def get_active_color(self):
        if self.game_word.belonging == 0:
            self.active_color = word_button_color_bomb
            self.active_font_color = font_color_bomb
        elif self.game_word.belonging == 1:
            self.active_color = word_button_color_teamA
        elif self.game_word.belonging == 2:
            self.active_color = word_button_color_teamB
        elif self.game_word.belonging == 3:
            self.active_color = word_button_color_neutral

class ClueInput:
    def __init__(self,pos_x_clue:int,pos_y_clue:int,pos_x_amount:int,pos_y_amount:int, pos_x_send:int, pos_y_send:int) -> None:    
        self.rect_clue = pygame.Rect(pos_x_clue,pos_y_clue,clue_word_size[0],clue_word_size[1])
        self.rect_amount = pygame.Rect(pos_x_amount,pos_y_amount,clue_amount_size[0],clue_amount_size[1])
        self.rect_send_btn = pygame.Rect(pos_x_send,pos_y_send,clue_send_btn_size[0],clue_send_btn_size[1])
        self.input_enabled = True
        self.clue_text = "Enter a Clue."
        self.amount_text = "1"
        self.clue_input_active = False 
        self.amount_input_active = False
        self.clue_input_init = False
        self.amount_input_init = False
        self.clue_entered = False 
        self.amount_entered = False 
        self.send_btn_active = False         
        self.flash_counter = 0
        self.flash_interval = 20
        self.draw(win)

    def clue_clicked(self):
        global player_typing
        if self.input_enabled:
            if not self.clue_input_init:
                self.clue_text = ''
            player_typing = True
            self.clue_input_active = True
            self.amount_input_active = False             
    
    def amount_clicked(self):
        global player_typing
        if self.input_enabled:
            if not self.amount_input_init:
                self.amount_text = ''
            player_typing = True 
            self.clue_input_active = False
            self.amount_input_active = True 

    def put_text(self,text:str,rect,text_color = clue_font_color):
        text_surface = codenames_font.render(text,True,text_color)
        text_rect = text_surface.get_rect(center=(rect[0]+rect[2]/2,rect[1]+rect[3]/2))
        win.blit(text_surface,(text_rect))

    def type(self,event):
        global player_typing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                player_typing = False
                if self.clue_input_active and self.clue_input_init:
                    self.clue_entered = True
                elif self.amount_input_active and self.amount_input_init:
                    self.amount_entered = True
                self.amount_input_active = False
                self.clue_input_active = False
            elif self.clue_input_active: 
                    # player giving clue
                    if event.key == pygame.K_BACKSPACE:
                        self.clue_text = self.clue_text[:-1]
                        if self.clue_text == '':
                            self.clue_input_init = False 
                    elif event.key == pygame.K_TAB:
                        if self.clue_input_init:
                            self.clue_entered = True 
                        self.amount_clicked()
                    elif event.unicode.isalpha():
                        if not self.clue_input_init:
                            self.clue_text = ''
                            self.clue_input_init = True
                        self.clue_text += event.unicode                        
            elif self.amount_input_active:  
                    # player giving amount
                    if event.key == pygame.K_BACKSPACE:
                        self.amount_text = self.amount_text[:-1]
                        if self.amount_text == '':
                            self.amount_input_init = False 
                    elif event.key == pygame.K_TAB:
                        if self.amount_input_init:
                            self.amount_entered = True                         
                    elif event.unicode.isdigit():
                        if not self.amount_input_init:
                            self.amount_text = ''
                            self.amount_input_init = True
                        self.amount_text += event.unicode    

    def flash_input_signal(self):
        self.flash_counter += 1
        if self.flash_counter>=self.flash_interval:
            if self.clue_input_active:
                if self.clue_text == "":
                    self.clue_text = "I"
                elif self.clue_text == "I":
                    self.clue_text = ""
            if self.amount_input_active:
                if self.amount_text == "":
                    self.amount_text = "I"
                elif self.amount_text == "I":
                    self.amount_text = ""
            self.flash_counter = 0

    def check_mouse(self):
        global player_typing
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            if self.rect_clue.collidepoint(pos):
                self.clue_clicked()
            elif self.rect_amount.collidepoint(pos):                
                self.amount_clicked()
            elif self.rect_send_btn.collidepoint(pos) and self.send_btn_active:
                self.send_clue()
            else:            
                if self.clue_input_active:
                    if not self.clue_input_init:
                        self.clue_text = ''      
                    else:
                        self.clue_entered = True      
                if self.amount_input_active:
                    if not self.amount_input_init:
                        self.amount_text = ''
                    else:
                        self.amount_entered = True 
                self.clue_input_active = False 
                self.amount_input_active = False 
                player_typing = False
                self.flash_counter = 0

    def send_clue(self):
        pass 

    def draw(self,win):    
        global player_typing    
        # clue input
        pygame.draw.rect(win,clue_color,self.rect_clue,border_radius=10)
        pygame.draw.rect(win,clue_frame_color,self.rect_clue,4,border_radius=10)
        if not self.clue_input_init and self.clue_input_active:
            self.flash_input_signal()
        self.put_text(self.clue_text,self.rect_clue)
        # amount input
        pygame.draw.rect(win,clue_color,self.rect_amount,border_radius=10)
        pygame.draw.rect(win,clue_frame_color,self.rect_amount,4,border_radius=10)
        if not self.amount_input_init and self.amount_input_active:
            self.flash_input_signal()
        self.put_text(self.amount_text,self.rect_amount)
        # send button
        if self.clue_entered and self.amount_entered:
            self.send_btn_active = True 
        else:
            self.send_btn_active = False 
        if self.send_btn_active:
            pygame.draw.rect(win,clue_frame_color,self.rect_send_btn,border_radius=10)
            self.put_text("Send Clue",self.rect_send_btn,clue_send_btn_font_color)
        # check mouse action
        self.check_mouse()

class GameText:
    def __init__(self,pos_x:int,pos_y:int,default_text:str = '',text_color = standard_font_color) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = default_text
        self.font_color = text_color
        self.rect = pygame.Rect(pos_x,pos_y,game_text_size[0],game_text_size[1])
        self.show_text = False 
        self.draw(win)
        
    def draw(self,win):        
        text_surface = codenames_font.render(self.text,True,self.font_color)
        text_rect = text_surface.get_rect(center=(self.rect[0]+game_text_size[0]/2,self.rect[1]+game_text_size[1]/2))
        win.blit(text_surface,(text_rect))

class GameManager: # Florian
    def __init__(self) -> None:
        self.game_ui_creator = None

    def set_game_ui_creator(self,game_ui_creator):
        self.game_ui_creator = game_ui_creator

class GameUiCreator: # Florian
    def __init__(self,game_words:List[GameWord],player_is_guesser:bool,player_team:int,game_manager:GameManager) -> None:
        self.game_words = game_words
        self.player_is_guesser = player_is_guesser
        self.player_team = player_team
        self.game_manager = game_manager
        self.word_buttons = []
        self.clue_input = None 
        self.clue_amount_input = None
        self.game_text = None
        self.words_per_row = 5
        self.words_per_col = len(game_words) / self.words_per_row
        self.bg = None 
        self.create_game_ui()

    def create_game_ui(self):
        current_row = 0
        current_col = 0
        space_x = (window_size[0] - (self.words_per_row*word_button_size[0])) / (self.words_per_row + 1)
        space_y = (window_size[1] - element_height*(2+self.words_per_col)) / (3+self.words_per_col)
        for game_word in self.game_words:
            pos_x = (current_col+1)*space_x + current_col*word_button_size[0]
            pos_y = (current_row+1)*space_y + current_row*word_button_size[1]
            word_button = WordButton(game_word,pos_x,pos_y,self.game_manager)
            if not self.player_is_guesser:
                word_button.set_active()
            self.word_buttons.append(word_button)
            if current_col >= self.words_per_row-1:
                current_row += 1
                current_col = 0
            else: 
                current_col += 1        
        game_text_y = pos_y + word_button_size[1] + space_y
        self.game_text = GameText(space_x,game_text_y,'Please provide a clue.')
        clue_input_x = 2*space_x + clue_word_size[0]
        clue_send_btn_x = space_x + clue_input_x + clue_amount_size[0]
        clue_input_y = game_text_y + clue_word_size[1] + space_y
        self.clue_input = ClueInput(space_x,clue_input_y,clue_input_x,clue_input_y,clue_send_btn_x,clue_input_y)
             
    def redraw_game_window(self):
        if self.bg != None:
            win.blit(self.bg,(0,0))
        else:
            win.fill(window_bg_color)
        
        for word_button in self.word_buttons:
            word_button.draw(win)

        self.clue_input.draw(win)
        self.game_text.draw(win)
        pygame.display.update()   
    

    def show_clue_from_bot(self,clue:Tuple[str,int]):
        pass 

    def reveal_player_guess(self,pressed_button:WordButton):
        pass 

    def reveal_bot_guess(self,bot_guess:GameWord):
        pass 
        
    

class GameManager_PlayerIsGuesser(GameManager): # Florian
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

class GameManager_PlayerIsClueGiver(GameManager): # Max 
    def __init__(self,game_words: List[GameWord],guesser_bot:GuesserBot) -> None:
        self.game_words = game_words
        self.guesser_bot = guesser_bot

    def start_game(self):
        pass 

    def ask_for_player_clue(self):
        pass 

    def handle_player_clue(self,player_clue:Tuple[str,int]):
        pass 

    def get_guess_from_bot(self):
        pass

    def check_for_game_end(self) -> bool:
        pass 

    def end_turn(self):
        pass 

    def end_game(self):
        pass 
        

if __name__ == "__main__":    
    win = pygame.display.set_mode(window_size)       
    pygame.display.set_caption("Codenames Bot") 
    clock = pygame.time.Clock()
    
    main_menu = MainMenu()
    # main loop
    main_menu_running = True 
    while main_menu_running:
        # TEST CONDITION: PLAYER IS TEAM A AND CLUE GIVER
        main_menu.chosen_role = 'guesser'
        main_menu.chosen_team = 'team_a'
        main_menu.start_game = True 
        # TEST CONDITION END 
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_running = False                        
        main_menu.redraw_game_window()
        if main_menu.start_game:
            possible_words = []
            for word in ['Tomato','Bench','Hair','Sand','Apple','Uniform','Jacket','Present','Box','Baseball','Orange','Majority','Window','Gun','Kite','Bowl','Castle','Mars','Material','Keyboard','Pocket','Phone','Discussion','Song','Pasta','Chimney','Stone','Treehouse','Coffee']:
                possible_words.append(word)
            
            player_is_guesser = True if main_menu.chosen_role == 'guesser' else False 
            player_team = GameWord.lookup_belonging(main_menu.chosen_team)
            game_generator = GameGenerator(possible_words,player_team,player_is_guesser)
            main_menu_running = False
            run = True 
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if player_typing:
                if event.type == pygame.KEYDOWN:
                    game_generator.game_ui_creator.clue_input.type(event)            
        game_generator.game_ui_creator.redraw_game_window()

