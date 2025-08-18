#make a to do list with customtkinter
import customtkinter as ctk
from tkinter import messagebox

# Setup appearance
ctk.set_appearance_mode("System")  # Light/Dark/System
ctk.set_default_color_theme("green")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("400x500")

        # Task list
        self.tasks = []

        # Title
        self.title_label = ctk.CTkLabel(self, text="✅ To-Do List", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Entry + Add button
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(pady=5)

        self.task_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter a task")
        self.task_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.add_button = ctk.CTkButton(self.entry_frame, text="Add", command=self.add_task)
        self.add_button.pack(side="right", padx=5)

        # Task listbox
        self.task_listbox = ctk.CTkTextbox(self, width=350, height=300)
        self.task_listbox.pack(pady=10)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.remove_button = ctk.CTkButton(self.button_frame, text="Remove Selected", command=self.remove_task)
        self.remove_button.grid(row=0, column=0, padx=5)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear All", fg_color="red", command=self.clear_tasks)
        self.clear_button.grid(row=0, column=1, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, "end")
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def remove_task(self):
        try:
            index = int(self.task_listbox.index("insert").split(".")[0]) - 1
            if 0 <= index < len(self.tasks):
                self.tasks.pop(index)
                self.update_task_list()
        except Exception:
            messagebox.showwarning("Warning", "Please click inside a task to remove it.")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks.clear()
            self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete("1.0", "end")
        for i, task in enumerate(self.tasks, start=1):
            self.task_listbox.insert("end", f"{i}. {task}\n")

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()