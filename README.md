# Personal Todo List Application

A modern, user-friendly task management application built with Python and CustomTkinter.

## Features

- **User Management**
  - Personal user accounts
  - Persistent user data
  - Welcome screen with user authentication

- **Task Management**
  - Add new tasks with title, description, and due date
  - Mark tasks as complete/incomplete
  - Delete tasks
  - Filter tasks by completion status
  - Search tasks by title or description

- **User Interface**
  - Modern dark theme
  - Responsive layout
  - Intuitive navigation
  - Task cards with clear information display
  - Real-time task search

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-list.git
cd todo-list
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter your name on the welcome screen
3. Use the sidebar to:
   - View all tasks
   - View pending tasks
   - Add new tasks
   - Search tasks
   - Logout

## Project Structure

- `main.py`: Main application file with GUI implementation
- `todo.py`: Core task management classes
- `storage.py`: Data persistence implementation
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## Dependencies

- Python 3.13
- customtkinter==5.2.2
- pillow==10.2.0
- colorama==0.4.6
- tabulate==0.9.0

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 