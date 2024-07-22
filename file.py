import tkinter as tk
from tkinter import ttk, messagebox
import random

class WordSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Solver")

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme

        self.rows = 12
        self.cols = 12
        self.cell_size = 30  # Size of each cell in the grid
        self.board = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.words = []
        self.word_positions = {}

        # Load dictionary from file
        self.dictionary = self.load_dictionary("dictionary.txt")

        # Select random words from dictionary that are guaranteed to be in crossword
        self.select_words()

        # Menu Bar
        self.create_menu()

        # Frames
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.pack(padx=10, pady=10, side=tk.LEFT)

        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(padx=10, pady=10, side=tk.LEFT)

        self.board_frame = ttk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10, side=tk.LEFT)

        # Labels and Entry for "Words to Find"
        self.label_words_to_find = ttk.Label(self.left_frame, text="Words to Find", font=('Arial', 14, 'bold'))
        self.label_words_to_find.pack(pady=(10, 5))

        self.words_to_find_frame = ttk.Frame(self.left_frame)
        self.words_to_find_frame.pack(padx=10, pady=10)

        # Labels and Entry for "Found Words"
        self.label_found_words = ttk.Label(self.right_frame, text="Found Words", font=('Arial', 14, 'bold'))
        self.label_found_words.pack(pady=(10, 5))

        self.found_words_frame = ttk.Frame(self.right_frame)
        self.found_words_frame.pack(padx=10, pady=10)

        # Labels and Entry
        self.label_selected_word = ttk.Label(self.board_frame, text="Enter a word from the list:")
        self.label_selected_word.pack(pady=(10, 0))

        self.selected_word_var = tk.StringVar()
        self.selected_word_entry = ttk.Entry(self.board_frame, textvariable=self.selected_word_var)
        self.selected_word_entry.pack(pady=5)

        # Buttons
        self.check_button = ttk.Button(self.board_frame, text="Find Word", command=self.find_word)
        self.check_button.pack(pady=5)

        self.next_word_button = ttk.Button(self.board_frame, text="Find Next Word", command=self.find_next_word)
        self.next_word_button.pack(pady=5)

        # Canvas for Board
        self.canvas = tk.Canvas(self.board_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size, highlightthickness=0)
        self.canvas.pack()

        # Color mapping for words
        self.word_colors = {}  # Dictionary to store word colors
        self.highlight_colors = ['yellow', 'cyan', 'magenta', 'orange', 'green', 'purple']  # List of highlight colors

        # Binding events for drag to select
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Draw initial board
        self.fill_board_with_random_letters()
        self.draw_board()
        self.display_dictionary_words()

        # Initialize found words list
        self.found_words = []

        # Display words to find
        self.display_words_to_find()

        # Display found words
        self.display_found_words()

    def load_dictionary(self, filename):
        with open(filename, 'r') as f:
            return [line.strip().upper() for line in f.readlines()]

    def select_words(self):
        # Randomly select 10 words from the dictionary
        num_words = 10
        selected_words = random.sample(self.dictionary, num_words)

        # Place words in the crossword grid using backtracking
        self.place_words(selected_words)

        self.words = selected_words

    def place_words(self, words):
        for word in words:
            placed = False
            while not placed:
                direction = random.choice(['horizontal', 'vertical', 'diagonal'])
                if direction == 'horizontal':
                    col = random.randint(0, self.cols - len(word))
                    row = random.randint(0, self.rows - 1)
                    if self.check_horizontal_placement(row, col, word):
                        self.place_horizontal(row, col, word)
                        placed = True
                elif direction == 'vertical':
                    col = random.randint(0, self.cols - 1)
                    row = random.randint(0, self.rows - len(word))
                    if self.check_vertical_placement(row, col, word):
                        self.place_vertical(row, col, word)
                        placed = True
                elif direction == 'diagonal':
                    col = random.randint(0, self.cols - len(word))
                    row = random.randint(0, self.rows - len(word))
                    if self.check_diagonal_placement(row, col, word):
                        self.place_diagonal(row, col, word)
                        placed = True

    def check_horizontal_placement(self, row, col, word):
        if col + len(word) > self.cols:
            return False
        for i in range(len(word)):
            if self.board[row][col + i] != '' and self.board[row][col + i] != word[i]:
                return False
        return True

    def place_horizontal(self, row, col, word):
        for i in range(len(word)):
            self.board[row][col + i] = word[i]
            self.word_positions[(row, col + i)] = word

    def check_vertical_placement(self, row, col, word):
        if row + len(word) > self.rows:
            return False
        for i in range(len(word)):
            if self.board[row + i][col] != '' and self.board[row + i][col] != word[i]:
                return False
        return True

    def place_vertical(self, row, col, word):
        for i in range(len(word)):
            self.board[row + i][col] = word[i]
            self.word_positions[(row + i, col)] = word

    def check_diagonal_placement(self, row, col, word):
        if row + len(word) > self.rows or col + len(word) > self.cols:
            return False
        for i in range(len(word)):
            if self.board[row + i][col + i] != '' and self.board[row + i][col + i] != word[i]:
                return False
        return True

    def place_diagonal(self, row, col, word):
        for i in range(len(word)):
            self.board[row + i][col + i] = word[i]
            self.word_positions[(row + i, col + i)] = word

    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='gray', fill='white')
                self.canvas.create_text(x0 + self.cell_size // 2, y0 + self.cell_size // 2, text=self.board[i][j], font=('Arial', 12))

    def fill_board_with_random_letters(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == '':
                    self.board[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def display_dictionary_words(self):
        for idx, word in enumerate(self.words):
            label = ttk.Label(self.words_to_find_frame, text=f"{word}", font=('Arial', 12))
            label.pack(anchor=tk.W)

    def find_word(self):
        word_to_find = self.selected_word_var.get().strip().upper()

        if word_to_find in self.words:
            found = self.backtrack_find_word(word_to_find)
            if found:
                self.highlight_word(word_to_find)
                self.move_word_to_found(word_to_find)
                self.show_word_found_message(word_to_find)
            else:
                messagebox.showinfo("Word Search Solver", f"Word '{word_to_find}' is not in the grid.")
        else:
            self.highlight_extra_word(word_to_find)

    def find_next_word(self):
        found_next = False
        for word in self.words:
            if self.backtrack_find_word(word):
                self.highlight_word(word)
                self.move_word_to_found(word)
                self.show_word_found_message(word)
                found_next = True
                break
        
        if not found_next:
            messagebox.showinfo("Word Search Solver", "All words have been found!")

    def backtrack_find_word(self, word):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == word[0]:
                    if self.backtrack_find_word_from_position(i, j, word, 0):
                        return True
        return False

    def backtrack_find_word_from_position(self, i, j, word, k):
        if k == len(word):
            return True
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols or self.board[i][j] != word[k]:
            return False
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            if self.backtrack_find_word_from_position(i + di, j + dj, word, k + 1):
                return True
        return False

    def highlight_word(self, word):
        if word not in self.word_colors:
            # Assign a unique color to the word
            color_index = len(self.word_colors) % len(self.highlight_colors)
            self.word_colors[word] = self.highlight_colors[color_index]

        for (r, c), placed_word in list(self.word_positions.items()):
            if placed_word == word:
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                # Draw a colored background rectangle
                color = self.word_colors[word]
                rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill=color, tags="highlight")
                # Change text color to black for readability
                self.canvas.create_text(x0 + self.cell_size // 2, y0 + self.cell_size // 2, text=self.board[r][c], font=('Arial', 12), fill='black', tags="highlight_text")

    def move_word_to_found(self, word):
        self.words.remove(word)
        self.found_words.append(word)
        self.display_words_to_find()
        self.display_found_words()

    def display_words_to_find(self):
        # Clear existing words to find display
        for widget in self.words_to_find_frame.winfo_children():
            widget.destroy()

        # Display words to find
        for idx, word in enumerate(self.words):
            label = ttk.Label(self.words_to_find_frame, text=f"{word}", font=('Arial', 12))
            if word in self.word_colors:
                label.configure(background=self.word_colors[word])
            label.pack(anchor=tk.W)

    def display_found_words(self):
        # Clear existing found words display
        for widget in self.found_words_frame.winfo_children():
            widget.destroy()

        # Display found words
        for idx, word in enumerate(self.found_words):
            label = ttk.Label(self.found_words_frame, text=f"{word}", font=('Arial', 12))
            if word in self.word_colors:
                label.configure(background=self.word_colors[word])
            label.pack(anchor=tk.W)

    def highlight_extra_word(self, word):
        # Implement this method if needed to handle extra words not in the dictionary
        pass

    def show_word_found_message(self, word):
        messagebox.showinfo("Word Search Solver", f"Word '{word}' found in the grid!")

    def on_click(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        if self.start_x and self.start_y:
            self.end_x = self.canvas.canvasx(event.x)
            self.end_y = self.canvas.canvasy(event.y)
            self.canvas.delete("highlight_rect")
            self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='black', tags="highlight_rect")

    def on_release(self, event):
        if self.start_x and self.start_y and self.end_x and self.end_y:
            self.canvas.delete("highlight_rect")
            selected_words = self.get_words_in_selection(self.start_x, self.start_y, self.end_x, self.end_y)
            if selected_words:
                for word in selected_words:
                    self.selected_word_var.set(word)
                    self.find_word()
            self.start_x = None
            self.start_y = None
            self.end_x = None
            self.end_y = None

    def get_words_in_selection(self, x0, y0, x1, y1):
        selected_words = []
        for (r, c), placed_word in self.word_positions.items():
            x_center = c * self.cell_size + self.cell_size // 2
            y_center = r * self.cell_size + self.cell_size // 2
            if x0 <= x_center <= x1 and y0 <= y_center <= y1:
                selected_words.append(placed_word)
        return selected_words

    def create_menu(self):
        # Implement menu creation if needed
        pass

# Main function to start the application
def main():
    root = tk.Tk()
    app = WordSearchGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
