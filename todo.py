from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init()

@dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    title: str
    description: str
    due_date: Optional[datetime]
    completed: bool = False
    created_at: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convert task to dictionary for storage."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            due_date=datetime.fromisoformat(data['due_date']) if data['due_date'] else None,
            completed=data['completed'],
            created_at=datetime.fromisoformat(data['created_at'])
        )

class TodoList:
    """Manages a collection of tasks."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str, due_date: Optional[datetime] = None) -> Task:
        """Add a new task to the list."""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            due_date=due_date
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def remove_task(self, task_id: int) -> bool:
        """Remove a task by its ID."""
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        return len(self.tasks) < initial_length

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self, show_completed: bool = True) -> List[Task]:
        """Get all tasks, optionally filtered by completion status."""
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]

    def filter_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by completion status."""
        if completed is None:
            return self.tasks
        return [task for task in self.tasks if task.completed == completed]

    def to_dict(self) -> dict:
        """Convert todo list to dictionary for storage."""
        return {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TodoList':
        """Create a TodoList instance from a dictionary."""
        todo_list = cls()
        todo_list.tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
        todo_list.next_id = data['next_id']
        return todo_list

    def list_tasks(self, show_completed: bool = True) -> None:
        """Display all tasks in a formatted table."""
        filtered_tasks = self.tasks if show_completed else [t for t in self.tasks if not t.completed]
        
        if not filtered_tasks:
            print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
            return

        headers = ["ID", "Title", "Description", "Due Date", "Status"]
        table_data = []
        
        for task in filtered_tasks:
            status = f"{Fore.GREEN}Completed{Style.RESET_ALL}" if task.completed else f"{Fore.RED}Pending{Style.RESET_ALL}"
            due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
            table_data.append([
                task.id,
                task.title,
                task.description,
                due_date,
                status
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid")) 