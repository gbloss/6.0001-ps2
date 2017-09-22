import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def sanitized_input(prompt, input_type=None, input_min=None, input_max=None):
    """
        Args:
            prompt (str): The text to display for user input.
            input_type (str, float, int): The type of input the user
                must enter. Defaults to None.
            input_min (float, int, optional): The optional minimum 
                value for the user input.  Defaults to None.
            input_max (float, int, optional): The optional maximum 
                value for the user input.  Defaults to None.
                
        Return:
            The value of the user input
    """

    if input_min is not None and input_max is not None and input_max < input_min:
        raise ValueError("Minimum must be less than or equal to the maximum.")
    while True:
        user_input = input(prompt)
        if input_type is not None:
            try:
                user_input = input_type(user_input) 
            except ValueError:
                print("Input type must be {0}.".format(input_type.__name__))
                continue
        if input_max is not None and user_input >= input_max:
            print("Input must be less than {0}.".format(input_max))
        elif input_min is not None and user_input <= input_min:
            print("Input must be greater than {0}.".format(input_min))
        else:
            return user_input


def is_word_guessed (word, guess):
    """
        args:
            word (str): The word to search through.
            guess (str): The letters guessed.
        
        return:
            True if the word is guessed.  False if it is not.
    """
# Set Constant Values
# Set Variables
    found = True
    i = 0
    word_to_check = str(word)
    guess_to_check = str(guess)
    
# Check each letter in word

    while i < len(word_to_check) and found == True:
        letter_to_check = str(word_to_check[i])
# See if current letter is in guess
        if guess_to_check.find(letter_to_check) > -1:
            found = True
        else:
            found = False
        i +=1
    
    return found
            
def get_guessed_word (word, guess):
    """
        args:
            word (str): The word to search through.
            guess (str): The letters guessed.
        
        return:
            String that reveals the placement of correct guesses
    """
    masked_word = ""
    word_to_check = str(word)
    guess_to_check = str(guess)
    
# Check each letter in word

    for i in range(len(word_to_check)):
        letter_to_check = str(word_to_check[i])
# See if current letter is in guess
        if guess_to_check.find(letter_to_check) > -1:
            masked_word = masked_word + letter_to_check
        else:
            masked_word = masked_word + "_ "
    
    return masked_word

def get_available_letters (guess):
    """
        args:
            guess (str): The letters guessed.
        
        return:
            String that shows remaining lowercase letters to guess from.
    """
    return_choices = ""
    alphabet = string.ascii_lowercase
    guess_to_check = str(guess)
    
# Check each letter in word
    for i in range(len(alphabet)):
        if guess_to_check.find(alphabet[i]) > -1:
            return_choices = return_choices
        else:
            return_choices = return_choices + alphabet[i]

    return return_choices

def match_with_gaps (my_word, other_word):
    """
        args:
            my_word (str): String with wildcard characters '_'
            other_word (str): String to compare my_word against
        return:
            Boolean.  True if the words are a potential match, false if not.
    """
    i = 0

    words_match = True
    my_word = my_word.replace(" ","")
    if len(my_word) != len(other_word):
        words_match = False
    else:
        while i < (len(my_word)) and words_match == True:
            if my_word[i] == "_":
                words_match = True
            elif my_word[i] == other_word[i]:
                words_match = True
            else:
                words_match = False
            i += 1
            
    return words_match
            
def show_possible_matches (my_word):
    """
        args:
            my_word (str): String with wildcard characters '_'
            other_word (str): String to compare my_word against
        return:
            Boolean.  True if the words are a potential match, false if not.
    """
    possible_matches = ""
    for i in range(len(wordlist)):
        if match_with_gaps(my_word,wordlist[i]) == True:
            possible_matches += " " + wordlist[i]
    if possible_matches == "":
        print("No matches found")
    else:
        print("Possible matches are:")
        print(possible_matches)
    
    return True

def hangman (secret_word):
    """
        args:
            secret word (str): A word that is to be the basis of the hangman
                game
        
        return:
            True if the game is won. False if the game was lost.
    """
    user_guesses = ""
    allowed_guesses = 6
    number_guesses = 0
    game_over = False
    number_warnings = 3
    two_guess_letters = "aeiou"
    wildcard = "*"

    print ("Welcome to the game Hangman!")
    print ("I am thinking of a word that is", len(secret_word),"letters long.")
    print (get_guessed_word(secret_word,user_guesses))
    
    while number_guesses < allowed_guesses and game_over == False:
        print ("You have",allowed_guesses - number_guesses,"guesses left.")
        print ("Available letters to guess: ",get_available_letters(user_guesses))        
        guessed_letter = str.lower(sanitized_input("Please guess a letter: ",str))

        if guessed_letter == wildcard:
            show_possible_matches(get_guessed_word(secret_word,user_guesses))
        elif user_guesses.find(guessed_letter) > -1 or str.isalpha(guessed_letter) != True:
            if number_warnings == 0:
                print("I told you!  You now lose a guess! ",get_guessed_word(secret_word,user_guesses))
                number_guesses += 1
            else:
                number_warnings = number_warnings-1
                print("Oops! Your guess must be a letter (no numbers or characters) that you haven't guessed.")
                print("You have",number_warnings,"warnings left:",get_guessed_word(secret_word,user_guesses))
        else:
            user_guesses += guessed_letter
            if secret_word.find(guessed_letter) > -1:
                print("Good guess:",get_guessed_word(secret_word,user_guesses))
            elif str.isalpha(guessed_letter) != True:
                if number_warnings == 0:
                    print("I told you!  You now lose a guess! ",get_guessed_word(secret_word,user_guesses))
                    number_guesses += 1
                else:
                    number_warnings = number_warnings-1
                    print("Oops! That is not a valid letter. You have",number_warnings,"warnings left:",get_guessed_word(secret_word,user_guesses))
            else:
                print("Oops! That letter is not in my word:",get_guessed_word(secret_word,user_guesses))
                if two_guess_letters.find(guessed_letter) > -1:
                    number_guesses +=1
                number_guesses += 1
        print ("------------")
        if is_word_guessed (secret_word,user_guesses):
            game_over = True

    if game_over:
        print("Congratulations you won!")
        print("Your total score for this game is:",(allowed_guesses - number_guesses)*len(secret_word))
    else:
        print("Sorry, you ran out of guesses.  The word was", secret_word)

    return False


# Set Constant Values
# Set Variables



secret_word = choose_word(wordlist)
hangman(secret_word)
