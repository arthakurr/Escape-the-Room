

# Do not modify the code below since it's needed to run the autograder accurately

quit_now = input("Enter 'quit' to quit or anything else to begin: ")

if quit_now.lower().strip() == "quit":
    exit(0)
    
# Start your code here

#ASNI colour codes
reset = "\033[0m"
yellow = "\033[33m"
green = "\033[32m"
red = "\033[31m"
cyan = "\033[36m"




from random import randint, choice
import string # This will make random codes

def reset_game():
    """This resets all of the game variables to start a new game."""
    global attempts_left, has_key, has_wire, has_note, safe_open, desk_searched, computer_on, computer_password, safe_code
    global has_blue_key, has_red_key, has_golden_key, basement_door_open, attic_door_open, secret_passage_open, bookshelf_moved
    global game_won
    #These are the game variables
    attempts_left = 5 #players have 5 attemps
    has_key = False #silver key
    has_wire = False # wire for the computer
    has_note = False #Note with the clue for the painting
    safe_open = False #Safe status
    desk_searched = False #if the desk is searched
    computer_on = False #computer status
    computer_password = randint(1,20)
    safe_code = str(randint(100,999)) # this creates a 3 digit code for the safe
    has_blue_key = False #key after the first door
    has_red_key = False #key behind the bookshelf
    has_golden_key = False #key from the basement
    basement_door_open = False #basement door status
    attic_door_open = False #attic door status
    secret_passage_open = False #Status for the secret passage
    bookshelf_moved = False #if the bookshelf has been moved or not
    game_won = False #game win status
    

def check_game_over():
    """This will check if the game is over due to running out of attempts"""
    global attempts_left, game_won #global will let us change the variables outside the function found on section 8.5 Function definitions.
   
    if game_won:
        print(green + "\nCONGRATULATIONS! YOU ESCAPED THE ROOM!" + reset)
        
        
        #Asks if the player wants to play again
        replay = input(cyan + "Do you want to play again? (y/n): " + reset)
        if replay.lower().strip() == "y":
            start_game() #restarts the game if they want to play again
        else:
            print(yellow + "Goodbye!" + reset)
            exit(0) #this exits the game
            
        return True #if the condition is met for game over
    
    if attempts_left <= 0:
        print(red + "\nYou ran out of attempts!" + reset)
        print(red + "GAME OVER" + reset)
        
        #Asks if the player wants to play again
        replay = input(cyan + "Do you want to play again? (y/n): " + reset)
        if replay.lower().strip() == "y":
            start_game() #restarts the game if they want to play again
        else:
            print(yellow + "Goodbye!" + reset)
            exit(0) #this exits the game
        
        return True # this will send the value back to where our function was called.
    return False #game is not over yet
    
def search_desk():
    """Lets the player search the desk for a wire"""
    global desk_searched, has_wire, attempts_left
    if desk_searched:
        print(cyan + "You have already searched the desk." + reset)
        return
    print(yellow + "\nYou search through the desk drawers..." + reset)
    print(green + "You find a piece of wire that looks useful!" + reset)
    has_wire = True #player has the wire now
    desk_searched = True #player has searched the desk now
    
def try_computer(): # docstrings 
    """Allows the player to use the computer"""
    global computer_on, attempts_left, safe_code
    
    if computer_on:
        print(green + "The computer shows: SAFE CODE", safe_code + reset)
        return
    
    if not has_wire:
        #the player needs the wire to turn the computer on
        print(red + "\nThe computer seems to be unplugged. Find something to connect the wire." + reset)
        return
    
    print(yellow + "\nYou use the wire to fix the computer's power." + reset)
    print(cyan + "The computer needs a password" + reset)
    
    print(yellow + "Hint: The password is a number between 1 and 20." + reset)
    #this is the loop to guess the password
    while True:
        guess = input(cyan + "Enter password number (or type 'quit' to exit): " + reset)
        if guess.lower() == "quit":
            return #this lets the player to exit the password gussing section
        try:
            guess = int(guess)
            if guess < 1 or guess > 20:
                print(red + "Number must be between 1 and 20!" + reset)
                continue #skips the rest of the loop
          
            if guess == computer_password:
                print(green + "Access granted! The screen shows: SAFE CODE", safe_code + reset)
                computer_on = True
                break #exits the guessing loop
            elif guess < computer_password:
                #hints that password is higher
                print(yellow + "Higher! Try again!" + reset)
                attempts_left -= 1
            else:
                print(yellow + "Lower! Try again!" + reset)
                #hints the password is lower
                attempts_left -= 1
            if check_game_over():
                return #checks if the player ran out of attempts
        
        except ValueError: #This helps if an user does not enter a number
            print(red + "Please enter a valid number" + reset)
            continue #skips rest of the loop
    
def check_safe():
    """Lets the player open the safe using a code"""
    global safe_open, has_note, attempts_left
    
    if safe_open:
        print(cyan + "The safe is already open." + reset)
        return
    
    if not computer_on:
        print(yellow + "\nThe safe needs a 3-digit code. Maybe you should find the code first?" + reset)
    else:
        print(yellow + "\nThe safe needs a 3-digit code. You remember seeing it on the computer." + reset)
    
    guess = input(cyan + "Enter code: " + reset)
    
    if not guess.isdigit() or len(guess) != 3: #checks if the guess is a 3 digit number
        print(red + "Please enter a valid 3-digit code!" + reset)
        attempts_left -= 1
        if check_game_over():
            return #checks if player ran out of attempts
        return
    
    if guess == safe_code:
        print(green + "The safe opens! Inside you find a note..." + reset)
        print(yellow + "The note says: 'The key is behind the painting, but watch out for traps!'" + reset)
        safe_open = True
        has_note = True #player has the note about the painting clue
    else:
        print(red + "Wrong code!" + reset)
        attempts_left -= 1
        if check_game_over():
            return
        
def check_painting():
    """Lets player check behind the painting for a key"""
    global has_key, attempts_left
    
    if has_key:
        print(cyan + "You already got the key from the painting." + reset)
        return
    if not has_note:
        #the player needs the sliver key to open the door
        print(red +"Maybe you should find a clue about the painting first..." + reset)
        # attempts_left -= 1 #dont need to minus an atttempt for that
        if check_game_over():
            return
        return
    print(yellow + "\nYou carefully check behind the painting..." + reset)
    print(green +"Success! You found a small silver key!" + reset)
    has_key = True
    
def try_door():
    """Lets the player try to escape from the door"""
    global attempts_left, has_blue_key
    
    if not has_key:
        print(red +"The door is locked. You need to find a key!" + reset)
        attempts_left -= 1
        if check_game_over():
            return
        return
    
    if has_blue_key:
        #player has already opened this door
        print(yellow + "\nYou already unlocked this door and found the blue key" + reset)
        return
    
    print(green + "\nYou put the key in the lock..." + reset)
    print(green + "The door opens to reveal another room" + reset)
    print(green + "You've found a blue key on the floor!" + reset)
    has_blue_key = True #player has the blue key now
    return
    
def check_bookshelf():
    """Lets the player check the bookshelf for secret passage"""
    global bookshelf_moved, has_red_key, attempts_left
    
    if bookshelf_moved:
        #bookshelf is already moved
        print(cyan + "You've already moved the bookshelf." + reset)
        return
    
    if not has_blue_key:
        #player needs to use the bookshelf
        print(red + "You notice something odd about the bookshelf, but can't figure out how to interact with it." + reset)
        return
    
    print(yellow + "\nYou notice a blue keyhole behind one of the books..." + reset)
    print(yellow + "You insert the blue key and turn it." + reset)
    print(green + "The bookshelf slides to reveal a secret passage!" + reset)
    print(green + "You find a red key inside!" + reset)
    bookshelf_moved = True #bookshelf got moved
    has_red_key = True #player has red key now
    return
    
def try_basement_door():
    """Lets the player try to open the basement door"""
    global basement_door_open, attempts_left
    
    if basement_door_open:
        #basement door is already open
        print(cyan + "The basement door is already open." + reset)
        return
    
    if not has_red_key:
        #player needs red key for the basement door
        print(red + "The basement door is locked with a red lock. You need to find the right key." + reset)
        attempts_left -= 1
        if check_game_over():
            return
        return
    
    print(yellow + "\nYou insert the red key into the basement door..." + reset)
    print(green + "The door unlocks! You can now access the basement." + reset)
    basement_door_open = True #basement door is open now
    return
    
def explore_basement():
    """This lets the player explore the basement"""
    global has_golden_key, attempts_left
    
    if not basement_door_open:
        #player has already explored the basement
        print(red + "You need to unlock the basement door first." + reset)
        return
    
    if has_golden_key:
        print(cyan + "You've already explored the basement and found the golden key." + reset)
        return
    
    print(yellow + "\nYou carefully descend into the dark basement..." + reset) 
    print(yellow + "After searching through cobwebs and old furniture..." + reset)
    print(green + "You discover a golden key hidden inside an old chest!" + reset) 
    has_golden_key = True #player has golden key
    return
    
def try_attic_door():
    """lets the player try and open the attic door"""
    global attic_door_open, attempts_left, secret_passage_open
    
    if attic_door_open:
        # attic door is already open
        print(cyan + "The attic door is already open." + reset)
        return
    
    if not has_golden_key:
        # player needs golden key for the attic
        print(red + "The attic door has a golden lock. You need to find the right key." + reset)
        attempts_left -= 1
        if check_game_over():
            return
        return
    
    print(yellow + "\nYou insert the golden key into the attic door..." + reset)
    print(green + "The door unlocks! You can now access the attic." + reset)
    attic_door_open = True # attic door is open
    return
    
def explore_attic():
    """Lets the player explore the attic and find the exit"""
    global secret_passage_open, game_won
    
    if not attic_door_open:
        #player needs to open the attic door first
        print(red + "You need to unlock the attic door first." + reset)
        return
    
    if secret_passage_open:
        #plater has already found the passage but did not escape
        print(green + "\nYou've already found the secret passage out!" + reset)
        print(green + "You climb through the passage and escape to freedom!" + reset)
        game_won = True # this means that the player won the game
        check_game_over() #checks game over
        return
        
    
    print(yellow + "\nYou search the dusty attic carefully..." + reset)
    print(green + "You discover a hidden trapdoor in the ceiling!" + reset)
    print(green + "The trapdoor leads outside to freedom!" + reset)
    secret_passage_open = True # secret passage is open
    game_won = True # this will end the game and player won
    check_game_over() 
    
#Now this will start the game loop
def start_game():
    reset_game() # resets all of the game's variables
    
    print(cyan + "Welcome to Aryan's Escape Room!" + reset)
    print(yellow + "You are locked inside Aryan's escape room. Find clues and escape before you run out of attempts!" + reset)
    print(yellow + "You have 5 total attempts to escape before you get locked inside forever" + reset)
    
    #This starts the main game loop, it continus until the player wins or runs out of attempts
    while attempts_left > 0 and not game_won:
        print(cyan + "\n------------------" + reset)
        print(yellow + f"Attempts remaining: {attempts_left}" + reset)
        print(cyan + "What would you like to do?" + reset)
        #these are the actions the player could pick-without peer feedback
        print("1. Search desk")
        print("2. Check computer")
        print("3. Examine safe")
        print("4. Look behind the painting")
        print("5. Try the door")
        
        #added because of peer feedback, conditionally shows options based on the players progress
        if has_blue_key:
            print("6. Examine bookshelf")
        else:
            print("6. [Find blue key first]")
        if bookshelf_moved:
            print("7. Try basement door")
        else:
            print("7. [Find secret passage first]")
        if basement_door_open:
            print("8. Explore basement")  
        else:
            print("8. [Open basement door first]")
        if has_golden_key:
            print("9. Try attic door")
        else:
            print("9. [Find golden key first]")
        if attic_door_open:
            print("10. Explore attic")
        else:
            print("10. [Open attic door first]")
            
        print("Q. Quit game")
        
        
        
        #allows the player to pick a value
        choice = input(cyan + "\nEnter choice (1-10 or Q): " + reset).lower() # makes letters lowercase
        

        #runs whatever value the player selects
        if choice == "1":
            search_desk()
        elif choice == "2":
            try_computer()
        elif choice == "3":
            check_safe()
        elif choice == "4":
            check_painting()
        elif choice == "5":
            try_door()
        elif choice == "6":
            if has_blue_key:
                check_bookshelf()
            else:
                #this blocks the action if requirement not met
                print(red + "You need to find the blue key first." + reset)
        elif choice == "7":
            if bookshelf_moved:
                try_basement_door()    
            else:
                 #this blocks the action if requirement not met
                print(red + "You need to find the secret passage first." + reset)
        elif choice == "8":
            if basement_door_open:
                explore_basement()
            else:
                 #this blocks the action if requirement not met
                print(red + "You need to open the basement door first." + reset)
        elif choice == "9":
            if has_golden_key:
                try_attic_door()
            else:
                 #this blocks the action if requirement not met
                print(red + "You need to find the golden key first." + reset)
        elif choice == "10":
            if attic_door_open:
                explore_attic()
            else:
                 #this blocks the action if requirement not met
                print(red + "You need to open the attic door first." + reset)
        elif choice == "q":
            #lets the player exit if wishes to quit
            print(red + "You have quit the game." + reset)
            return
        
        else:
            #handles if the player inputs an invalid choice
            print(red + "Invalid choice! Please enter a valid option." + reset)
        
        #this handles if the game ends because of the player running out of attempts
    if not game_won and attempts_left <= 0:
        check_game_over()

        # these are the final messages and the option to replay
    print(cyan + "\nThanks for playing" + reset)
    replay = input(cyan + "Do you want to play again? (y/n): " + reset)
    if replay.lower().strip() == "y":
       start_game() # restarts the game if player wishes
    else:
       print(yellow + "Goodbye!" + reset)
       exit(0) # this exits the program

#start the game
start_game()