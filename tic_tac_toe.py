
#TIC TAC TOE
import tkinter as tk
import random
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe: You vs AI")
        self.board = [[" "]*3 for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.human = "X"
        self.ai = "O"
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text=" ", font="Arial 20", width=5, height=2,
                                command=lambda r=i, c=j: self.human_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def human_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.human
            self.buttons[row][col].config(text=self.human, state="disabled")
            if self.check_winner(self.human):
                self.end_game("You win!")
                return
            elif not self.get_empty_cells():
                self.end_game("It's a draw!")
                return
            self.window.after(500, self.ai_move)

    def ai_move(self):
        move = self.best_move()
        if move:
            i, j = move
            self.board[i][j] = self.ai
            self.buttons[i][j].config(text=self.ai, state="disabled")
            if self.check_winner(self.ai):
                self.end_game("AI wins!")
            elif not self.get_empty_cells():
                self.end_game("It's a draw!")

    def best_move(self):
        # Win
        for i, j in self.get_empty_cells():
            self.board[i][j] = self.ai
            if self.check_winner(self.ai):
                return (i, j)
            self.board[i][j] = " "

       
        for i, j in self.get_empty_cells():
            self.board[i][j] = self.human
            if self.check_winner(self.human):
                self.board[i][j] = " "
                return (i, j)
            self.board[i][j] = " "

        if self.board[1][1] == " ":
            return (1, 1)

        
        for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if self.board[i][j] == " ":
                return (i, j)

       
        return random.choice(self.get_empty_cells())

    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.window.destroy()

if __name__ == "__main__":
    TicTacToe()
