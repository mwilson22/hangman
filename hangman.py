from importlib.util import spec_from_loader
import os
import time
import random
from hangman_pics import hangman_pic
from cursor_ctrl import *

MAX_GUESSES = 11


def get_attempts_str(attempts):
    return f"Lives left: {MAX_GUESSES - attempts}"


def get_dashes_and_letters_str(word, guesses):
    """Detect if the guess is in the word.
       Return:
       1 the dashes string for displaying which letters have been found
       2 whether it was an incorrect guess"""
    length = len(word)
    incorrect = True
    dashes_letters = '_' * length

    if len(guesses) != 0:
        for i in range(length):
            # Check all guesses for all letters
            if word[i] in guesses:
                dashes_letters = dashes_letters[:i] + \
                    word[i] + dashes_letters[i+1:]

            # Only a correct guess if the last guess matches a letter
            if word[i] == guesses[-1]:
                incorrect = False

    return dashes_letters, incorrect


def display_hangman(fail_count, dashes_letters, guesses):
    """Show the incorrect guess total and the partial word with dashes
       next to the hangman picture"""
    os.system('clear')
    print("\n            HANGMAN")
    print(hangman_pic[fail_count])
    print('\033[5;12H', get_attempts_str(fail_count))

    spread_dashes = ''
    for i in range(len(dashes_letters)):
        spread_dashes += dashes_letters[i] + ' '

    print('\033[7;12H', spread_dashes, f'  ({len(dashes_letters)} letters)')
    print('\033[9;12H Guesses: ', guesses)
    move_cur_down(1)


def test_pictures():
    delay = 0.5

    for i in range(12):
        display_hangman(i)
        time.sleep(delay)


def get_random_word():
    f = open('words.txt')
    # Read in the file once and build a list of line offsets
    line_offset = []
    offset = 0

    for line in f:
        line_offset.append(offset)
        offset += len(line)

    f.seek(0)
    # Skip to line n (with the first line being line 0)
    f.seek(line_offset[random.randint(1, sum(1 for line in f))])
    return f.readline()


def play():
    word = get_random_word().lower()
    # Remove the newline
    word = word[:-1]
    guesses = []
    fail_count = 0

    os.system('clear')
    dashes_letters, x = get_dashes_and_letters_str(word, guesses)
    display_hangman(0, dashes_letters, [''])

    while True:
        # Get the first letter the user inputs
        letter = input("Your guess: ")[0:1].lower()

        if letter[0:1] not in guesses and letter[0:1] != '' and letter[0:1].isalpha():
            guesses.append(letter[0:1])
            dashes_letters, incorrect = get_dashes_and_letters_str(
                word, guesses)

            if incorrect == True:
                fail_count += 1

            display_hangman(fail_count, dashes_letters, guesses)

            if dashes_letters == word:
                print("                    You win!")
                break
            if fail_count == MAX_GUESSES:
                print(f"Out of guesses :o(  The word was \'{word}\'\n")
                break
        else:
            move_cur_up(2)


def hangman():
    cur_ctrl = CursorCtrl()
    thr = cur_ctrl.start_cur_flashing()

    while True:
        play()
        play_again = input("Play again? [y/n]")
        if play_again != 'y':
            break

    cur_ctrl.stop_cur_flashing(thr)


if __name__ == '__main__':
    hangman()
