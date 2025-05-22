import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
from PIL import Image, ImageTk
import json
import os
from todo import TodoList
from storage import Storage
from tkinter import ttk

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.on_login = on_login
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Welcome Label
        self.welcome_label = ctk.CTkLabel(
            self,
            text="Welcome to Your Personal Todo List",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, pady=20)
        
        # Name Entry
        self.name_label = ctk.CTkLabel(
            self,
            text="Please enter your name:",
            font=ctk.CTkFont(size=16)
        )
        self.name_label.grid(row=1, column=0, pady=(0, 10))
        
        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Your Name",
            width=300,
            height=40
        )
        self.name_entry.grid(row=2, column=0, pady=(0, 20))
        
        # Start Button
        self.start_button = ctk.CTkButton(
            self,
            text="Start",
            command=self.start_app,
            width=200,
            height=40
        )
        self.start_button.grid(row=3, column=0, pady=20)

    def start_app(self):
        name = self.name_entry.get().strip()
        if name:
            self.on_login(name)
        else:
            messagebox.showwarning("Warning", "Please enter your name!")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Personal Todo List")
        self.geometry("1000x600")
        
        # Initialize storage and todo list
        self.storage = Storage()
        self.todo_list = self.storage.load() or TodoList()
        
        # User data
        self.user_name = ""
        self.user_data_file = "user_data.json"
        
        # Show welcome screen
        self.show_welcome_screen()
        
    def show_welcome_screen(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create and show welcome screen
        self.welcome_screen = WelcomeScreen(self, self.on_login)
        self.welcome_screen.pack(fill="both", expand=True)
        
    def on_login(self, name):
        self.user_name = name
        self.load_user_data()
        self.show_main_screen()
        
    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    data = json.load(f)
                    if self.user_name in data:
                        self.todo_list = TodoList.from_dict(data[self.user_name])
            except:
                pass
                
    def save_user_data(self):
        data = {}
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
                
        data[self.user_name] = self.todo_list.to_dict()
        
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def show_main_screen(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_container, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # User info
        user_frame = ctk.CTkFrame(sidebar)
        user_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            user_frame,
            text=f"Welcome,\n{self.user_name}!",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(sidebar)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search tasks...",
            width=180
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        
        self.search_entry.bind('<Return>', lambda e: self.search_tasks())
        
        ctk.CTkButton(
            search_frame,
            text="🔍",
            width=30,
            command=self.search_tasks
        ).pack(side="right")
        
        # Navigation buttons
        ctk.CTkButton(
            sidebar,
            text="All Tasks",
            command=lambda: self.show_tasks(show_completed=True)
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            sidebar,
            text="Pending Tasks",
            command=lambda: self.show_tasks(show_completed=False)
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            sidebar,
            text="Add New Task",
            command=self.show_add_task_dialog
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            sidebar,
            text="Logout",
            command=self.show_welcome_screen,
            fg_color="red",
            hover_color="darkred"
        ).pack(fill="x", padx=10, pady=5)
        
    def create_main_content(self):
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="Your Tasks",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Task list
        self.task_list = ctk.CTkScrollableFrame(self.content_frame)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show all tasks initially
        self.show_tasks(show_completed=True)
        
    def show_tasks(self, show_completed=True):
        # Clear existing tasks
        for widget in self.task_list.winfo_children():
            widget.destroy()
            
        # Update title
        self.title_label.configure(
            text="All Tasks" if show_completed else "Pending Tasks"
        )
        
        # Show tasks
        tasks = self.todo_list.get_all_tasks(show_completed)
        if not tasks:
            ctk.CTkLabel(
                self.task_list,
                text="No tasks found!",
                font=ctk.CTkFont(size=16)
            ).pack(pady=20)
            return
            
        for task in tasks:
            self.create_task_widget(task)
            
    def create_task_widget(self, task):
        task_frame = ctk.CTkFrame(self.task_list)
        task_frame.pack(fill="x", padx=5, pady=5)
        
        # Task info
        info_frame = ctk.CTkFrame(task_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=task.title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=task.description,
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
        ctk.CTkLabel(
            info_frame,
            text=f"Due: {due_date}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")
        
        # Action buttons
        button_frame = ctk.CTkFrame(task_frame)
        button_frame.pack(side="right", padx=5, pady=5)
        
        if not task.completed:
            ctk.CTkButton(
                button_frame,
                text="Complete",
                command=lambda t=task: self.complete_task(t),
                width=100
            ).pack(pady=2)
            
        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=lambda t=task: self.delete_task(t),
            fg_color="red",
            hover_color="darkred",
            width=100
        ).pack(pady=2)
        
    def show_add_task_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Task")
        dialog.geometry("500x500")
        
        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()
        
        # Task input fields
        ctk.CTkLabel(
            dialog,
            text="Title:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(20, 5))
        
        title_entry = ctk.CTkEntry(dialog, width=300)
        title_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(
            dialog,
            text="Description:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))
        
        description_entry = ctk.CTkEntry(dialog, width=300)
        description_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(
            dialog,
            text="Due Date (YYYY-MM-DD):",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))
        
        due_date_entry = ctk.CTkEntry(dialog, width=300)
        due_date_entry.pack(pady=(0, 20))
        
        def add_task():
            title = title_entry.get().strip()
            description = description_entry.get().strip()
            due_date_str = due_date_entry.get().strip()
            
            if not title:
                messagebox.showwarning("Warning", "Title cannot be empty!")
                return
                
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
                    
            self.todo_list.add_task(title, description, due_date)
            self.save_user_data()
            self.show_tasks(show_completed=True)
            dialog.destroy()
            
        ctk.CTkButton(
            dialog,
            text="Add Task",
            command=add_task,
            width=200
        ).pack(pady=20)
        
    def complete_task(self, task):
        if self.todo_list.complete_task(task.id):
            self.save_user_data()
            self.show_tasks(show_completed=True)
            
    def delete_task(self, task):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            if self.todo_list.remove_task(task.id):
                self.save_user_data()
                self.show_tasks(show_completed=True)

    def search_tasks(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            self.show_tasks(show_completed=True)
            return
            
        # Clear existing tasks
        for widget in self.task_list.winfo_children():
            widget.destroy()
            
        # Update title
        self.title_label.configure(text=f"Search Results: {search_term}")
        
        # Search tasks
        tasks = self.todo_list.get_all_tasks(show_completed=True)
        matching_tasks = [
            task for task in tasks
            if search_term in task.title.lower() or 
               search_term in task.description.lower()
        ]
        
        if not matching_tasks:
            ctk.CTkLabel(
                self.task_list,
                text="No matching tasks found!",
                font=ctk.CTkFont(size=16)
            ).pack(pady=20)
            return
            
        for task in matching_tasks:
            self.create_task_widget(task)

def main():
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = TodoApp()
    app.mainloop()

if __name__ == "__main__":
    main() 