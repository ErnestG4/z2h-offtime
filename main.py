# copied these imports. reevaluate need.
import random
import time
import json
import colors
from colors import *
# import replit
# import sys
# import numpy


class GameTools:

  # return a yes or no answer string
  def get_yesno(self, prompt):
    while True:
      yesno = input(f"\n{prompt} ").strip()
      if len(yesno) != 0:
        if yesno[0].lower() == "y":
          return True
        elif yesno[0].lower() == "n":
          return False
        else:
          print("\n\t Enter Yes, No, or some other variant I recognize. I can do this all day, you know...\n")

  # return an integer between 0 and upper_bound, IE for health points, list choices
  def get_posint(self, prompt, upper_bound = 9999):
    while True:
      posint = input(f"\n{prompt} ")
      if not posint.isdigit():
        print("\n\tEnter a positive integer! \n")
      elif int(posint) == 0 or int(posint) > int(upper_bound):
        print("\n\tKeep it inside the lines, Jabroni.")
      else:
        return(int(posint))

class TextBox:
  
  def box_width(self,box_strings = ""):
    if box_strings == "":
      return(80)
    longest_text_length = 0
    for text in box_strings:
      if len(text.strip()) > longest_text_length:
        longest_text_length = len(text.strip())
    return(longest_text_length)
  
  def draw_box_top(self,width = 80):
    top_start_char = "\u256C"
    top_end_char = "\u256C"
    top_bridge_char = "\u2550"
    print(f'{top_start_char}{top_bridge_char * width}{top_end_char}')
  
  def draw_box_bottom(self,width = 80):
    bottom_start_char = "\u256C"
    bottom_end_char = "\u256C"
    bottom_bridge_char = "\u2550"
    print(f'{bottom_start_char}{bottom_bridge_char * width}{bottom_end_char}')

  def draw_text(self,box_strings,width = 80):
    side_char = "\u2551"
    space = " "
    for text in box_strings:
      space_mod_before = int((width - len(text.strip())) / 2)
      space_mod_after = int(width - space_mod_before - len(text.strip()))
      print(f"{side_char}{space * space_mod_before}{text.strip()}{space * space_mod_after}{side_char}")

  def load_text(self,string_file):
    print(f"{string_file}")
    text_file = open(string_file,'r')
    return text_file.readlines()
    



class GameState:
  # include """Docs for the class to be called by __doc__""" here

  # init vars
  def __init__(self):
    self.tools = GameTools()
    self.enemies = self.load_enemies()
    self.players = self.load_players()
    self.chosen_player = self.get_name()
    self.player_loot = []
    self.player_xp = 0

  # get player name -- change second posint argument to length of players list
  def get_name(self):
    print("\nBy what naem dost thou goethe? ")
    self.printnames(self.players)
    choice = self.tools.get_posint("Choice:",8)
    return(self.players[choice-1])

  # get initial HP
  # def init_hp(self):
  #   return self.tools.get_posint("What is your starting HP?",300)

  # ask if the user wants to play another round
  def play_again(self):
    return(self.tools.get_yesno("Would you like to play again? Yes or No?"))

  # calculate damage
  def damage(self):
    pass

  # Create enemy object from enemies.json
  def load_enemies(self):
    enemy_file = open('enemies.json','r')
    enemy_data = json.loads(enemy_file.read())
    enemies = []
    for enemy_stats in enemy_data:
      enemies.append(Enemy(enemy_stats))
    return(enemies)
  
  # Create player object from players.json
  def load_players(self):
    player_file = open('players.json','r')
    player_data = json.loads(player_file.read())
    players = []
    for player_stats in player_data:
      players.append(Player(player_stats))
    return(players)

  # display a numbered list of names
  def printnames(self, listcontents):
    listindex = 1
    for listitem in listcontents:
      print(f"\t{listindex}: {listitem.name}")
      listindex += 1


# Creature struct - parent to Player and Enemy
class Creature:
  def __init__(self,stats):
    self.name = stats["name"]
    self.hp = stats["hp"]
    self.ac = stats["ac"]
    self.attack_mod = stats["attack_mod"]
    self.dmg_die = stats["dmg_die"]
    self.dmg_mod = stats["dmg_mod"]
    
  def __str__(self):
    return f"{self.name} has {self.hp}HP."


# Player class - inherits from Creature
class Player(Creature):
  def __init__(self,stats):
    super().__init__(stats)
    self.race = stats["race"]
  def attack(self):
    player_roll = random.randint(1,20)
    return player_roll + self.attack_mod
    # return random.randint(1,20 + self.dmg_mod) 

  def damage(self):
    return random.randint(1,self.dmg_die) + self.dmg_mod

# Enemy class - inherits from Creature
class Enemy(Creature):
  def __init__(self,stats):
    super().__init__(stats)
    self.CR = stats["CR"]
  
  def attack(self):
    return random.randint(1,20) + self.dmg_mod

  def damage(self):
    return random.randint(1,self.dmg_die) + self.dmg_mod

  def __str__(self):
    return f"{self.name} has {self.hp}HP and will be a {self.CR} challenge!"

# combat sequence between player and enemy
def combat(state, player, enemy):
  enemy_temp_hp = enemy.hp
  attack_round = 1
  
  # Attack loop
  while True:
    player_attack_roll = player.attack()
    player_damage_roll = player.damage()
    enemy_attack_roll = enemy.attack()
    enemy_damage_roll = enemy.damage()
    print(f"\n\t ROUND {attack_round}:")
    # Enemy attack sequence
    if enemy_attack_roll > player.ac:
      player.hp -= enemy_damage_roll
      print(f"\tThe {enemy.name} {color('HITS', fg='red')} {player.name} for {enemy_damage_roll} damage.")
    else:
      print(f"\tThe {enemy.name} {color('MISSES', fg='cyan')} {player.name}.")
    print(f"\n\t{player.name} has {player.hp} hp remaining.\n")
    # Check for defeated player
    if player.hp <= 0:
      print(f"\n\tYou have been bested by a(n) {enemy.name}.")
      return()
    # Player attack sequence
    print(f"\t{player.name} rolls a {player_attack_roll} attack roll.")
    if player.race == "halfling" and (player_attack_roll - player.attack_mod) == 1:
      player_attack_roll = player.attack()
      print(f"\n\tAh ye little lucky bastage. Re-rolling your 1 gives you a {player_attack_roll}")
    if (player_attack_roll - player.attack_mod) == 1:
      print(f"\n\tYou critically fail and hit your own foot, injuring yourself for {player_damage_roll/2} damage.")
      player.hp -= int(player_damage_roll/2)
    if (player_attack_roll - player.attack_mod) == 20:
      print("\n\tYou crit for double damage!")
      player_damage_roll = player_damage_roll * 2
    if player_attack_roll > enemy.ac:
      enemy_temp_hp -= player_damage_roll
      print(f"\n\t{player.name} {color('HITS', fg='red')} the {enemy.name} for {player_damage_roll} damage.")
    else:
      print(f"\n\t{player.name} {color('MISSES', fg='cyan')} the {enemy.name}")
    print(f"\n\tThe {enemy.name} {consider_damage(enemy_temp_hp,enemy.hp)}")
    # Check for defeated enemy
    if enemy_temp_hp <= 0:
      print(f"\n\tYou have successfully dispatched the {enemy.name}.")
      time.sleep(1)
      return()
    # Ask if the player wants to run away
    if state.tools.get_yesno("Would you like to run away?"):
      print("\n\tYou clutch your wounds and flee into the wilderness, wailing like a baby.")
      return()
    attack_round += 1
    
    

# return a string describing how damaged something is
def consider_damage(health,maxhealth):      
  if health <= 0:
    return(f"is {color('DEAD.',fg='red')}")
  elif health/maxhealth <= .2:
    return("is missing some limbs, but still clinging to life.")
  elif health/maxhealth <= .4:
    return("is badly injured and bleeding all over the place.")
  elif health/maxhealth <= .6:
    return("has some gnarly cuts and gashes.")  
  elif health/maxhealth < .8:
    return("has a few bruises and scratches")
  elif health/maxhealth < 1:
    return("is really pissed off now.")
  else:
    return("is completely fine.")

# introduce the game.. ew that's a nasty solution FIX IT... sometime later, that is.
def display_intro():
  draw_box = TextBox()
  intro = "intro.txt"
  intro_strings = load_text(intro)
  box_width = draw_box.box_width(intro_strings)
  draw_box.draw_box_top(box_width)
  draw_box.draw_text(intro_strings,box_width)
  draw_box.draw_box_bottom(box_width)

def load_text(string_file):
  text_file = open(string_file,'r')
  return text_file.readlines()

def main():
  print("TESTING")
  # print(color('my string', fg='blue'))
  # print(color('some text', fg='red', bg='yellow', style='underline'))
  display_intro()
  state = GameState()
  print(f"\n{state.chosen_player.name} has {state.chosen_player.hp} starting hp.")
  while True:
    temp_check = random.randint(1,5)
    temp_count = 1
    for enemy in state.enemies:
      if temp_count == temp_check:
        combat(state,state.chosen_player,enemy)
      temp_count += 1  
    #   print(enemy)
    #   print(f"{enemy.name} attacks with a {enemy.attack()} for {enemy.damage()} damage.")
    if state.chosen_player.hp <= 0:
      print(f"\n\tYou crawl, beaten and bloody, back to pluffton. Be sure to subtract {state.chosen_player.hp * -1} from tomorrow's starting hp.")
      break
    if not state.play_again():
      print("\n\tYou head back to Pluffton with your haul of spoils.")
      break

if __name__ == "__main__":
  main()