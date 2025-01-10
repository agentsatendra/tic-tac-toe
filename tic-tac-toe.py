import speech_recognition as sr
import tkinter as tk

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the Tic Tac Toe board
board = [' ' for _ in range(9)]

# Initialize a variable to keep track of the current player
current_player = 'X'

# Create a function to update the game board
def update_board():
    for i in range(9):
        buttons[i].config(text=board[i])

# Create a function to check for a win
def check_win(player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]

    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

# Create a function to handle player moves
def handle_move(position):
    global current_player
    if board[position] == ' ':
        board[position] = current_player
        update_board()
        if check_win(current_player):
            result_label.config(text=f"Player {current_player} wins!")
            disable_buttons()
        elif ' ' not in board:
            result_label.config(text="It's a tie!")
            disable_buttons()
        else:
            current_player = 'X' if current_player == 'O' else 'O'
            result_label.config(text=f"Player {current_player}'s turn")

# Create a function to disable all buttons after the game ends
def disable_buttons():
    for button in buttons:
        button.config(state=tk.DISABLED)

# Create the main game window
root = tk.Tk()
root.title("Voice-Activated Tic Tac Toe")

# Create buttons for the Tic Tac Toe board
buttons = [tk.Button(root, text=' ', width=30, height=8, command=lambda i=i: handle_move(i)) for i in range(9)]
for i, button in enumerate(buttons):
    row = i // 3
    col = i % 3
    button.grid(row=row, column=col)

# Create a label to display the game result
result_label = tk.Label(root, text=f"Player {current_player}'s turn", font=("Helvetica", 16))
result_label.grid(row=3, columnspan=3)

# Function to reset the game
def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    update_board()
    for button in buttons:
        button.config(state=tk.NORMAL)
    result_label.config(text=f"Player {current_player}'s turn")

# Create a reset button
reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.grid(row=4, columnspan=3)

# Function to recognize speech and make moves
def recognize_speech():
    with sr.Microphone() as source:
        print("Speak your move (e.g., 'top left', 'mid', 'bottom right'):")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        spoken_text = recognizer.recognize_google(audio)
        spoken_text = spoken_text.lower()
        for position, value in positions.items():
            if position in spoken_text:
                handle_move(value)
                return
        print("Invalid move. Try again.")
    except sr.UnknownValueError:
        print("Could not understand your move. Try again.")

# Create a start button for voice recognition
start_button = tk.Button(root, text="Start Voice Recognition", command=recognize_speech)
start_button.grid(row=5, columnspan=3)

# Mapping of spoken positions to board positions
positions = {'top left': 0, 'top mid': 1, 'top right': 2,
             'mid left': 3, 'mid': 4, 'mid right': 5,
             'bottom left': 6, 'bottom mid': 7, 'bottom right': 8}

# Initialize the game
update_board()

# Start the GUI main loop
root.mainloop()