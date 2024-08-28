import random
import time

def welcome_message():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have to guess the correct number within a limited number of chances.\n")

def select_difficulty():
    print("Please select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")
    difficulty = input("Enter your choice (1/2/3): ")
    
    if difficulty == '1':
        return 10
    elif difficulty == '2':
        return 5
    elif difficulty == '3':
        return 3
    else:
        print("Invalid choice. Defaulting to Medium difficulty.")
        return 5

def play_game():
    welcome_message()
    
    # Select the difficulty level
    chances = select_difficulty()
    
    # Randomly select a number between 1 and 100
    number_to_guess = random.randint(1, 100)
    
    print(f"\nGreat! Let's start the game! You have {chances} chances to guess the number.\n")
    
    start_time = time.time()
    attempts = 0
    
    while chances > 0:
        guess = int(input("Enter your guess: "))
        attempts += 1
        
        if guess == number_to_guess:
            end_time = time.time()
            print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
            print(f"It took you {round(end_time - start_time, 2)} seconds.")
            return attempts  # Return the number of attempts as the score
        
        elif guess < number_to_guess:
            print("Incorrect! The number is greater than your guess.\n")
        else:
            print("Incorrect! The number is less than your guess.\n")
        
        chances -= 1
        print(f"You have {chances} chances left.\n")
    
    print(f"Sorry, you've run out of chances. The correct number was {number_to_guess}.")
    return None  # Return None to indicate the player didn't guess the number

def play_again():
    while True:
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again in ['yes', 'no']:
            return play_again == 'yes'
        print("Please enter 'yes' or 'no'.")

def main():
    high_score = None
    
    while True:
        score = play_game()
        
        if score and (high_score is None or score < high_score):
            high_score = score
            print(f"New high score! You guessed the number in {high_score} attempts.\n")
        
        if not play_again():
            print("Thank you for playing the Number Guessing Game!")
            if high_score:
                print(f"Your best score was {high_score} attempts. Well done!")
            break

if __name__ == "__main__":
    main()
