import random
import time
import sqlite3
import sys

# Establish database connection
conn = sqlite3.connect('game_scores.db')

def create_scores_tables():
    """Create score tables for each game."""
    cursor = conn.cursor()
    
    # Create a table for each game
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rps_scores (
            id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_scores (
            id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countdown_scores (
            id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coinflip_scores (
            id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS typing_scores (
            id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    """)
    
    conn.commit()


def add_score(game, username, score):
    """Add score to the specified game table."""
    cursor = conn.cursor()
    table_name = f"{game}_scores"
    sql = f"INSERT INTO {table_name} (username, score) VALUES (?, ?)"
    cursor.execute(sql, [username, score])
    conn.commit()


def get_scores(game):
    """Retrieve top scores for the specified game."""
    cursor = conn.cursor()
    table_name = f"{game}_scores"
    sql = f"SELECT username, score FROM {table_name} ORDER BY score"
    return cursor.execute(sql).fetchmany(10)


# --- Game Implementations ---

# ASCII art for Rock, Paper, Scissors
game_titles = {
    "rps": '''\033[32m
    █▀█ █▀█ █▀▀ █▄▀  
    █▀▄ █▄█ █▄▄ █░█  

    █▀█ ▄▀█ █▀█ █▀▀ █▀█  
    █▀▀ █▀█ █▀▀ ██▄ █▀▄  

    █▀ █▀▀ █ █▀ █▀ █▀█ █▀█ █▀
    ▄█ █▄▄ █ ▄█ ▄█ █▄█ █▀▄ ▄█
    \033[0m''',
    "rock": '''
  \033[31m  _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
    \033[0m''',
    "paper": '''
  \033[36m_______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
\033[0m ''',

    "scissors": '''
  \033[33m _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
    \033[0m'''
}

# ASCII art for Coin Flip
heads = """ 
  \033[92m╔════════╗  
 ╔╝ ░░░▒▒▓ ╚╗ 
╔╝ ░░░░▒▒▓▓ ╚╗
║ ░░░HEAD▒▓▓ ║
╚╗ ░░░▒▒▒▓▓ ╔╝
 ╚╗ ░░░▒▒▓ ╔╝ 
  ╚════════╝\033[0m  
"""

tails = """
  \033[91m╔════════╗  
 ╔╝ ░░░▒▒▓ ╚╗ 
╔╝ ░░░░▒▒▓▓ ╚╗
║ ░░░TAIL▒▓▓ ║
╚╗ ░░░▒▒▒▓▓ ╔╝
 ╚╗ ░░░▒▒▓ ╔╝ 
  ╚════════╝\033[0m  
"""

def display_game_title():
    """Display the ASCII art title of Rock, Paper, Scissors."""
    print(game_titles["rps"])

def rock_paper_scissors():
    display_game_title()  # Show the game title with ASCII art
    choices = ['rock', 'paper', 'scissors']
    username = input('Enter your name: ')
    user_score = 0

    while True:
        user_choice = input("Choose rock, paper, or scissors (or 'quit' to exit): ").lower()
        if user_choice == 'quit':
            break
        
        if user_choice == 'rock':
            print(game_titles["rock"])
        elif user_choice == 'paper':
            print(game_titles["paper"])
        elif user_choice == 'scissors':
            print(game_titles["scissors"])
        else:
            print("Invalid choice. Please choose rock, paper, or scissors.")
            continue
        
        computer_choice = random.choice(choices)
        print(f"Computer chose {computer_choice}:")
        
        if computer_choice == 'rock':
            print(game_titles["rock"])
        elif computer_choice == 'paper':
            print(game_titles["paper"])
        elif computer_choice == 'scissors':
            print(game_titles["scissors"])

        if user_choice == computer_choice:
            print("\033[43m\033[97mIt's a tie!\033[0m")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            print("\033[42m\033[30mYou win!\033[0m")
            user_score += 1
        else:
            print("\033[41m\033[97mYou lose!\033[0m")

    print(f"Your final score: {user_score}")
    add_score('rps', username, user_score)

def coin_flip_simulator():
    username = input('Enter your name: ')
    user_score = 0
    
    while True:
        user_guess = input("\033[97mGuess heads or tails (or 'quit' to exit):\033[0m ").lower()
        if user_guess == 'quit':
            break
        if user_guess not in ['heads', 'tails']:
            print("\033[31mInvalid guess. Please choose heads or tails.\033[0m")
            continue
        
        flip_result = random.choice(['heads', 'tails'])
        print(f"Coin flip result: {flip_result}")
        
        if flip_result == 'heads':
            print(heads)
        else:
            print(tails)
        
        if user_guess == flip_result:
            print("\033[92mYou guessed correctly!\033[0m")
            user_score += 1
        else:
            print("\033[91mIncorrect guess! \033[0m")

    print(f"Your final score: {user_score}")
    add_score('coinflip', username, user_score)

def memory_card_matching():
    cards = ['\033[95mA\033[0m', '\033[96mK\033[0m', '\033[91mQ\033[0m', '\033[94mJ\033[0m', '\033[95mA\033[0m', '\033[96mK\033[0m', '\033[91mQ\033[0m', '\033[94mJ\033[0m']
    random.shuffle(cards)
    print("Memory Card Matching - Try to match pairs!")
    
    username = input('Enter your name: ')
    user_score = 0
    revealed_cards = ['*' for _ in cards]
    
    while '*' in revealed_cards:
        print("Cards:", " ".join(revealed_cards))
        card1 = int(input("Choose the first card to flip (1-8): ")) - 1
        card2 = int(input("Choose the second card to flip (1-8): ")) - 1
        
        if cards[card1] == cards[card2]:
            print(f"Match! {cards[card1]} - {cards[card2]}")
            revealed_cards[card1] = cards[card1]
            revealed_cards[card2] = cards[card2]
            user_score += 1
        else:
            print(f"Not a match. {cards[card1]} - {cards[card2]}")

    print(f"Your final score: {user_score}")
    add_score('memory', username, user_score)

def countdown_timer_quiz():
    questions = [
        ("What is 2+2?", "4"),
        ("What is 3*5?", "15"),
        ("What is 10-4?", "6")
    ]
    
    username = input('Enter your name: ')
    user_score = 0
    
    for question, answer in questions:
        print(question)
        start_time = time.time()
        user_answer = input("Your answer: ")
        end_time = time.time()
        
        time_taken = end_time - start_time
        if user_answer == answer and time_taken < 10:
            print("Correct!")
            user_score += 1
        else:
            print("Incorrect or too slow!")
    
    print(f"Your final score: {user_score}")
    add_score('countdown', username, user_score)

def typing_speed_test():
    sentence = "The quick brown fox jumps over the lazy dog."
    username = input('Enter your name: ')
    
    print("\033[95m Typing Speed Test - Type the following sentence as quickly as you can:\033[0m")
    print(sentence)
    
    start_time = time.time()
    user_input = input("Type the sentence: ")
    end_time = time.time()
    
    time_taken = end_time - start_time
    if user_input == sentence:
        print(f"Correct! Time taken: {time_taken:.2f} seconds.")
        score = 100 / time_taken
    else:
        print("Incorrect typing!")
        score = 0
    
    print(f"Your score: {score}")
    add_score('typing', username, score)

# --- Main Menu ---

def choose_game():
    """Allow the user to choose a game."""
    while True:
        print("\n\033[97mChoose your game:\033[0m")
        print("\033[92m1. Rock, Paper, Scissors\033[0m")
        print("\033[93m2. Memory Card Matching\033[0m")
        print("\033[94m3. Countdown Timer Quiz\033[0m")
        print("\033[96m4. Coin Flip Simulator\033[0m")
        print("\033[95m5. Typing Speed Test\033[0m")
        print("\033[91m6. Quit\033[0m")
        
        game_choice = input("Enter the number of your choice: ")

        if game_choice == '1':
            game_menu('rps')
        elif game_choice == '2':
            game_menu('memory')
        elif game_choice == '3':
            game_menu('countdown')
        elif game_choice == '4':
            game_menu('coinflip')
        elif game_choice == '5':
            game_menu('typing')
        elif game_choice == '6':
            print("Goodbye!")
            exit()

def game_menu(game):
    """Display game options."""
    while True:
        print("\nChoose an option:")
        print("1. Play")
        print("2. Scores")
        print("3. Back")
        
        option = input("Enter your choice: ")

        if option == '1':
            if game == 'rps':
                rock_paper_scissors()
            elif game == 'memory':
                memory_card_matching()
            elif game == 'countdown':
                countdown_timer_quiz()
            elif game == 'coinflip':
                coin_flip_simulator()
            elif game == 'typing':
                typing_speed_test()
        elif option == '2':
            scores = get_scores(game)
            print('-' * 20)
            for score in scores:
                print(f"{score[0]}: {score[1]}")
            print('-' * 20)
        elif option == '3':  # When the user chooses to go back
            return  # This will exit the current loop and return to the previous menu

if __name__ == "__main__":
    create_scores_tables()
    choose_game()
