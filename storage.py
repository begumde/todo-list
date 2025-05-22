import json
from pathlib import Path
from typing import Optional
from todo import TodoList

class Storage:    
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)

    def save(self, todo_list: TodoList) -> bool:
        try:
            data = todo_list.to_dict()
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False

    def load(self) -> Optional[TodoList]:
        try:
            if not self.file_path.exists():
                return TodoList()

            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TodoList.from_dict(data)
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return None 