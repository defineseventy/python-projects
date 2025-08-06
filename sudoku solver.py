#Sudoku Solver w a GUI using customtkinter

import customtkinter as ctk
from tkinter import messagebox

#set appearance
ctk.set_appearance_mode("System") #will make a toggle button later
ctk.set_default_color_theme("green")

class SudokuSolver(ctk.CTk):
    #initalize
    def __init__(self):
        super().__init__() #used for creating window in customtkinter (very important to include)
        self.title("Sudoku Solver")
        self.geometry("500x550")
        self.resizable(True, True) #want it to be resizable
        self.grid = [[0]*9 for _ in range(9)]

        self.create_widgets()
    
    def create_widgets(self):
        self.entries = [[None]*9 for _ in range(9)]

        #Sudoku grid
        for i in range(9):
            for j in range(9):
                entry = ctk.CTkEntry(self, width=40, height=40, font=('Arial', 20), justify='center')
                entry.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 1, 2 if j % 3 == 2 else 1),
                                         pady=(2 if i % 3 == 0 else 1, 2 if i % 3 == 2 else 1))
                self.entries[i][j] = entry

        
        #solve button
        solve_button = ctk.CTkButton(self, text="Solve", font=("Arial", 18), command=self.solve)
        solve_button.grid(row=10, column=0, columnspan=3, pady=15)

        #reset button
        reset_button = ctk.CTkButton(self, text="Reset", font=("Arial", 18), command=self.reset)
        reset_button.grid(row=10, column=3, columnspan=3, pady=15)

        #theme button
        self.theme_mode = "System"
        toggle_button = ctk.CTkButton(self, text="Toggle", font=("Arial", 18), command=self.toggle)
        toggle_button.grid(row=10, column=6, columnspan=3, pady=15)

    def solve(self):
        #load values
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit() and i <= int(val) <= 9:
                    self.grid[i][j] = int(val)
                else:
                    self.grid[i][j] = 0
        if self.backtrack_solve():
            self.update_grid()
            messagebox.showinfo("Success", "Sudoku Solved!")
        else:
            messagebox.showerror("Error", "No solution exists for the given puzzle.")
    
    def update_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, ctk.END)   
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
    
    def reset(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, ctk.END)
        self.grid = [[0]*9 for _ in range(9)]
    
    def toggle(self):
        if self.theme_mode == "Light":
            ctk.set_appearance_mode("Dark")
            self.theme_mode = "Dark"
        elif self.theme_mode == "Dark":
            ctk.set_appearance_mode("System")
            self.theme_mode = "System"
        else:
            ctk.set_appearance_mode("Light")
            self.theme_mode = "Light"
    #find empty
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None
    
    #check if valid
    def is_valid(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    #solving the sudoku
    def backtrack_solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.backtrack_solve():
                    return True
                self.grid[row][col] = 0
        return False
    
#Will be put onto Github too :))
if __name__ == "__main__":
    app = SudokuSolver()
    app.mainloop()