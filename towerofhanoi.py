#Making a tower of Hanoi puzzle using customtkinter

import customtkinter as ctk
from tkinter import messagebox
import json
import time
import threading
import os

#Let's do this together
#First, I'll make the game window

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

#oops, supposed to be class
class TowerOfHanoi(ctk.CTk):
    #initialize
    def __init__(self):
        super().__init__()
        self.title("Tower of Hanoi")
        self.geometry("780x620")
        self.resizable(True, True)

        self.num_disks = 4
        self.towers = [[], [], []]
        self.disk_widgets = {}
        self.selected_disk = None
        self.moves = 0
        self.move_history = []

        self.setup_ui()

    #make the ui
    def setup_ui(self):
        self.disk_selector = ctk.CTkComboBox(self, values=[str(i) for i in range(3, 9)], command=self.set_disk_count)
        self.disk_selector.set(str(self.num_disks))
        self.disk_selector.pack(pady=10)

        self.canvas = ctk.CTkCanvas(self, width=700, height=400, bg="#F5F5F5", highlightthickness=0)
        self.canvas.pack(pady=10)

        rod_x_positions = [150, 350, 550]
        self.rods = [self.canvas.create_rectangle(x-5, 150, x+5, 350, fill="#333") for x in rod_x_positions]
        self.rod_x_positions = rod_x_positions

        self.move_label = ctk.CTkLabel(self, text="Moves: 0", font=("Arial", 16))
        self.move_label.pack()

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Reset", command=self.reset).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="Undo", command=self.undo_move).grid(row=0, column=1, padx=6)
        ctk.CTkButton(btn_frame, text="Solve", command=self.solve).grid(row=0, column=2, padx=6)
        ctk.CTkButton(btn_frame, text="Save", command=self.save_game).grid(row=0, column=3, padx=6)
        ctk.CTkButton(btn_frame, text="Load", command=self.load_game).grid(row=0, column=4, padx=6)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.reset()
    
    #use a dropdown here
    def set_disk_count(self, choice):
        self.num_disks = int(choice)
        self.reset()
    
    #reset to the start
    def reset(self):
        self.canvas.delete("disk")
        self.towers = [[i for i in range(self.num_disks, 0, -1)], [], []]
        self.disk_widgets = {}
        self.selected_disk = None
        self.moves = 0
        self.move_history = []
        self.move_label.configure(text="Moves: 0")
        self.draw_disks()
    
    #draw disks
    def draw_disks(self):
        self.canvas.delete("disk")
        colors = ["#FF9999", "#FFCC66", "#99CCFF", "#66FF99", "#CC99FF", "#FF6666", "#66CCCC", "#CCCC66"]
        for rod in range(3):
            for height, disk in enumerate(self.towers[rod]):
                width = disk * 20 + 20
                x = self.rod_x_positions[rod]
                y = 340 - height * 20
                disk_id = self.canvas.create_rectangle(
                    x - width // 2, y, x + width // 2, y + 20,
                    fill=colors[disk % len(colors)], tags="disk"
                )
                self.canvas.tag_bind(disk_id, "<Button-1>", lambda e, ro=rod: self.select_disk(ro))
                self.disk_widgets[disk] = disk_id

    def select_disk(self, rod):
        if not self.towers[rod]:
            return
        top_disk = self.towers[rod][-1]
        self.selected_disk = (rod, top_disk)

    def on_canvas_click(self, event):
        x = event.x
        rod_index = 0 if x < 250 else 1 if x < 450 else 2

        if self.selected_disk:
            from_rod, disk = self.selected_disk
            if from_rod == rod_index:
                self.selected_disk = None
                return
            if not self.towers[rod_index] or self.towers[rod_index][-1] > disk:
                self.make_move(from_rod, rod_index)
            else:
                messagebox.showwarning("Invalid Move", "Cannot place larger disk on top of smaller one.")
                self.selected_disk = None

    def make_move(self, from_rod, to_rod):
        disk = self.towers[from_rod].pop()
        self.towers[to_rod].append(disk)
        self.moves += 1
        self.move_history.append((from_rod, to_rod))
        self.move_label.configure(text=f"Moves: {self.moves}")
        self.selected_disk = None
        self.draw_disks()
        if self.check_win():
            messagebox.showinfo("Congratulations!", f"You solved it in {self.moves} moves!")

    def undo_move(self):
        if not self.move_history:
            return
        to_peg, from_peg = self.move_history.pop()
        disk = self.towers[from_peg].pop()
        self.towers[to_peg].append(disk)
        self.moves -= 1
        self.move_label.configure(text=f"Moves: {self.moves}")
        self.draw_disks()
    
    #check if win
    def check_win(self):
        return len(self.towers[2]) == self.num_disks

    def solve(self):
        if self.moves > 0:
            confirm = messagebox.askyesno("Warning", "Auto-solve will reset the game. Continue?")
            if not confirm:
                return
        self.reset()
        threading.Thread(target=self.solve_hanoi, args=(self.num_disks, 0, 2, 1)).start()
    
    #Perform recursive function
    def solve_hanoi(self, n, src, tgt, aux):
        if n == 0:
            return
        self.solve_hanoi(n-1, src, aux, tgt)
        time.sleep(0.3)
        self.make_move(src, tgt)  # This line performs the move
        self.solve_hanoi(n-1, aux, tgt, src)
    
    #save game
    def save_game(self):
        data = {
            "towers": self.towers,
            "moves": self.moves,
            "history": self.move_history,
            "num_disks": self.num_disks
        }
        with open("hanoi_save.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Game state saved successfully.")
    
    #Load game
    def load_game(self):
        if not os.path.exists("hanoi_save.json"):
            messagebox.showwarning("Not Found", "No saved game found.")
            return
        with open("hanoi_save.json", "r") as f:
            data = json.load(f)
        self.num_disks = data["num_disks"]
        self.disk_selector.set(str(self.num_disks))
        self.towers = data["towers"]
        self.moves = data["moves"]
        self.move_history = data["history"]
        self.selected_disk = None
        self.move_label.configure(text=f"Moves: {self.moves}")
        self.draw_disks()

#Let's test it out, I'll upload this to Github
if __name__ == "__main__":
    app = TowerOfHanoi()
    app.mainloop()
