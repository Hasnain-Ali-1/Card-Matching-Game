"""
File: py_match.py
Author: Hasnain Ali
Section: 23
Email: hali6@umbc.edu
Date: 4/22/22
Description: The code generates a random matrix that is a user specified size along with user specified symbols. The user selects an element of the matrix, which acts as a card, and tries to guess the other cards that have the same symbol. The user is told how many cards of the same symbol are left. If they guess wrong and they haven't found all of the cards with their current symbol, then all of their cards with the current symbol get flipped back over and the user has to re-guess them. Once all the cards are revelaed, the program stops.  
"""

import random

def get_file(file_name):

    """
    A function that gets the symbols for the game
    :param file_name: The file name the user wishes to access and use for their game
    :return: a list that contains the symbols that will be used
    """
    
    dataList = []

    try:
        infile = open(file_name, "r")
        line = infile.readline().strip("'")
        dataList.append(line)
        infile.close()
        dataList = line.split()
        flag = False
        dataList.append(flag)
        return dataList

    except FileNotFoundError:
        print("file was not found, try again")
        flag = True
        return flag 


def create_solution_board(user_row, user_col, symbols):

    """
    A function that creates the answer key to the randomly generated board
    :param user_row: The number of rows used to generate the board
    :param user_col: The number of columns used to generate the board
    :param symbols: The symbols that are going to be used in the board, taken from the file the user specified
    :return: A board that serves as an answer key
    """
    
    board = []
    for i in range(user_row):
        row = []
        board.append(row)
        for j in range(user_col):
            value = random.choice(symbols)
            row.append(value)

    return board


def create_game_board(user_row, user_col):

    """
    A function that creates the board the user will interact with throughout the game
    :param user_row: The number of rows used to generate the board
    :param user_col: The number of columns used to generate the board
    :return: A board that serves as the game board of the user
    """
    
    board = []
    for i in range(user_row):
        row = []
        board.append(row)
        for j in range(user_col):
            row.append(".")
    
    return board


def play_game(row, col, solution_board, game_board, previous_letter):
    
    """
    A function that is responsible for the actual playing of the game. It asks the user for the position they wish to choose and keeps on going until the game ends
    :param row: The number of rows in the board
    :param col: The number of columns in the board
    :param solution_board: The answer key to the randomly generated board
    :param game_board: The board that serves as the game board
    :param previous_letter: The previous letter the user guessed. Will be passed into another function to check if it matches with the current guess
    :return: A value for flag that either stops the while loop or continues it, or a list that contains the value for flag and the updated value for previous_letter
    """
    
    if game_board == solution_board:
        print("Congratulations, you win!")
        flag = False
        return flag
    else:
        if previous_letter == "placeholder":
            user_choice = input("Enter the position to guess (seperated by a space): ")
        else:
            remaining_letter = previous_letter[0]
            previous_letter = previous_letter[1]
            user_choice = input("Enter position to guess that matches "+str(previous_letter)+" (seperated by a space). There are "+str(remaining_letter)+" remaining: ")

        if len(user_choice) < 3:
            print("Remember to enter a space between the row and column of the position you are guessing")
            for i in range(row):
                for j in range(col):
                    print(game_board[i][j], end=" ")
                print("")
            flag = True
            return flag
        user_choice = user_choice.split()
        user_row, user_col = user_choice
        user_row = int(user_row)
        user_col = int(user_col)
        if user_row-1 >= row or user_col-1 >= col:
            print("The position you entered is out of bounds")
            for i in range(row):
                for j in range(col):
                    print(game_board[i][j], end=" ")
                print("")
            flag = True
            return flag
        
        elif game_board[user_row-1][user_col-1] == solution_board[user_row-1][user_col-1]:
            print("You have already guessed this position")
            for i in range(row):
                for j in range(col):
                    print(game_board[i][j], end=" ")
                print("")
            flag = True
            return flag

        else:
            result = check_letter(row, col, user_row-1, user_col-1, solution_board, game_board, previous_letter)
            previous_letter = result
            for i in range(row):
                for j in range(col):
                    print(game_board[i][j], end=" ")
                print("")
            flag = True
            flag_list = []
            flag_list.append(flag)
            flag_list.append(previous_letter)
            return flag_list

        
def check_letter(row, col, user_row, user_col, solution_board, game_board, prior_letter):
    
    """
    A function that checks if the letter the user picked matches the previous letter, if their is a previous letter they need to match
    :param row: The number of rows on the board
    :param col: The number of columns on the board
    :param user_row: The row the user selected in their guess
    :param user_col: The column the user selected in their guess
    :param solution_board: The answer key to the randomly generated board
    :param game_board: The board that serves as the game board
    :param prior_letter: The previous letter the user guessed
    :return: It returns an updated value for previous_letter, or a list containing the update values for previous_letter and remaining_letters
    """
    
    game_letter_count = 0
    solution_letter_count = 0

# If prior_letter is the defualt value or it equals the symbol at the current user pick, then it's a valid guess
    
    if prior_letter == "placeholder" or prior_letter == solution_board[user_row][user_col]:
        prior_letter = solution_board[user_row][user_col]
        game_board[user_row][user_col] = solution_board[user_row][user_col]
        for i in range(row):
            for j in range(col):
                if solution_board[i][j] == solution_board[user_row][user_col]:
                    solution_letter_count = solution_letter_count + 1
                if game_board[i][j] == solution_board[user_row][user_col]:
                    game_letter_count = game_letter_count + 1
        remaining_letters = solution_letter_count - game_letter_count
        if remaining_letters == 0:
            prior_letter = "placeholder"
            print("You have found all of the "+str(solution_board[user_row][user_col]))
            return prior_letter

# If all of the previous letters aren't found, then a list containing prior_letter and remaining_letter is returned

        else:            
            remaining_letter_list = []
            remaining_letter_list.append(remaining_letters)
            remaining_letter_list.append(prior_letter)
            return remaining_letter_list

# This part is responsible for guesses that don't match the previous letter
        
    else:
        game_board[user_row][user_col] = solution_board[user_row][user_col]
        print("No match rhis time:")
        for i in range(row):
            for j in range(col):
                print(game_board[i][j], end=" ")
            print("")
        print("Try again!")
        for i in range(row):
            for j in range(col):
                if game_board[i][j] == prior_letter or game_board[i][j] == game_board[user_row][user_col]:
                    game_board[i][j] = "."
        prior_letter = "placeholder"
        return prior_letter

if __name__ == "__main__":
    board_info = (input("Enter the row, col, and seed (seperated by a comma): "))
    board_info = board_info.split(",")
    board_row, board_col, seed = board_info
    random.seed(int(seed))
    flag = True
    while flag == True:
        userfile = input("What is the symbol file name: ")
        game_symbols = get_file(userfile)
        if game_symbols == True:
            flag = game_symbols
        else:
            flag = game_symbols[-1]
            game_symbols.remove(game_symbols[-1])
            
    solution_board = create_solution_board(int(board_row), int(board_col), game_symbols)
    game_board = create_game_board(int(board_row), int(board_col))
    previous_letter = "placeholder"

    for i in range(int(board_row)):
        for j in range(int(board_col)):
            print(game_board[i][j], end=" ")
        print("")

    flag_2 = True
    while flag_2 == True:
        result = play_game(int(board_row), int(board_col), solution_board, game_board, previous_letter)
        if result == True or result == False:
            flag_2 = result
        else:
            previous_letter = result[1]
            flag_2 = result[0]
