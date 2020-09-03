# tkinter help and guidance from http://newcoder.io/gui/part-3/
import generate_sudoku_board
import tkinter
import copy
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

margin = 20
side = 50
width = margin * 2 + side * 9
height = margin * 2 + side * 9

#draws the board is the user interface for the game
class sudokuGUI(Frame):

    def __init__(self, parent, completeboard, board):
        self.endboard = completeboard
        self.board = board
        self.parent = parent
        Frame.__init__(self, parent)
        self.row = 0
        self.col = 0
        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.difficulty = "easy"
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self, width = width, height = height)
        self.canvas.pack(fill = BOTH, side = TOP)

        newGameButton = Button(self, text = "New Game", width = 10, height = 1, command = self.new_game)
        newGameButton.place (x = 20, y = 500 )
        easyButton = Button(self, text = "Easy", width = 10, height = 1, command = self.easy_game)
        easyButton.place (x = 120, y = 500 )
        mediumButton = Button(self, text = "Medium", width = 10, height = 1, command = self.medium_game)
        mediumButton.place (x = 220, y = 500 )
        hardButton = Button(self, text = "Hard", width = 10, height = 1, command = self.hard_game)
        hardButton.place (x = 320, y = 500 )

        self.draw_grid()
        self.draw_numbers()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    def draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = margin + i * side
            y0 = margin
            x1 = margin + i * side
            y1 = height - margin
            self.canvas.create_line(x0, y0, x1, y1, fill = color)

            x0 = margin
            y0 = margin + i * side
            x1 = width - margin
            y1 = margin + i * side
            self.canvas.create_line(x0, y0, x1, y1, fill = color)

    def draw_numbers(self):
        self.canvas.delete("numbers")
        for row in range(9):
            for col in range(9):
                numberentered = self.board[row][col]
                if numberentered != 0:
                    x = margin + col * side + side / 2
                    y = margin + row * side + side / 2
                    answer = self.endboard[row][col]
                    color = "black" if answer == numberentered else "firebrick"
                    self.canvas.create_text( x, y, text = numberentered, tags = "numbers", fill = color )

    def new_game(self):
        self.endboard = generate_sudoku_board.completedSudokuBoard()
        self.board = generate_sudoku_board.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("victory")
        self.draw_numbers()

    def easy_game(self):
        self.endboard = generate_sudoku_board.completedSudokuBoard()
        self.difficulty = "easy"
        self.board = generate_sudoku_board.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("victory")
        self.draw_numbers()
    
    def medium_game(self):
        self.endboard = generate_sudoku_board.completedSudokuBoard()
        self.difficulty = "medium"
        self.board = generate_sudoku_board.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("victory")
        self.draw_numbers()

    def hard_game(self):
        self.endboard = generate_sudoku_board.completedSudokuBoard()
        self.difficulty = "hard"
        self.board = generate_sudoku_board.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("victory")
        self.draw_numbers()

    def cell_clicked(self, event):
        if self.endboard == self.board:
            self.victory_text()
            return
        x = event.x
        y = event.y
        if (margin < x < width - margin and margin < y < height - margin):
            self.canvas.focus_set()

            # get row and col from x,y coordinates
            row = int((y - margin) / side)
            col = int((x - margin) / side)
 
            # deselects a cell
            if (row, col) == (self.row, self.col):
                self.row = -1
                self.col = -1
            else:
                self.row = row
                self.col = col

        self.draw_highlight()

    def draw_highlight(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = margin + self.col * side + 1
            y0 = margin + self.row * side + 1
            x1 = margin + (self.col + 1) * side - 1
            y1 = margin + (self.row + 1) * side - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def key_pressed(self, event):
        if event.keysym == "Left":
            self.col -= 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Right":
            self.col += 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Up":
            self.row -= 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Down":
            self.row += 1
            self.draw_numbers()
            self.draw_highlight()

        elif self.endboard == self.board:
            self.victory_text()
            return
        elif self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.board[self.row][self.col] = int(event.char)
            self.draw_numbers()
            self.draw_highlight()
            if self.endboard == self.board:
                self.victory_text()

#says that the player won
    def victory_text(self):
        x = y = margin + 4 * side + side / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="coral", font=("Arial", 64)
        )


answerboard = generate_sudoku_board.completedSudokuBoard()
puzzleboard = generate_sudoku_board.puzzleSudokuBoard(answerboard, "easy")

root = Tk()
root.geometry("%dx%d" % (width, height + 40))

sudokuGUI(root, answerboard, puzzleboard)
root.mainloop()