# Task Tracker CLI

Task Tracker is a powerful yet simple command-line interface (CLI) application designed to help you efficiently manage your tasks and to-do list. With intuitive commands, you can easily add, update, delete, and track the status of your tasks. All your task data is conveniently stored in a JSON file for persistence and easy access.

## Features

- **Add new tasks**: Quickly add tasks to your list
- **Update existing tasks**: Modify task descriptions as needed
- **Delete tasks**: Remove completed or unnecessary tasks
- **Mark task progress**: Set tasks as "todo", "in-progress", or "done"
- **List all tasks**: Get an overview of all your tasks
- **Filter tasks by status**: View tasks based on their current status
- **Data persistence**: All tasks are saved in a JSON file for future sessions

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task-tracker-cli
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

## Usage

Run the CLI using Python. Here are the available commands:

### Add a Task

```bash
python task_tracker.py add "Your task description"
```

Example:
```bash
python task_tracker.py add "Buy groceries"
```

Output:
```
Task added successfully (ID: 1)
```

### Update a Task

```bash
python task_tracker.py update <task_id> "New task description"
```

Example:
```bash
python task_tracker.py update 1 "Buy groceries and cook dinner"
```

Output:
```
Task 1 updated successfully.
```

### Delete a Task

```bash
python task_tracker.py delete <task_id>
```

Example:
```bash
python task_tracker.py delete 1
```

Output:
```
Task 1 deleted successfully.
```

### Mark a Task as In-Progress

```bash
python task_tracker.py mark-in-progress <task_id>
```

Example:
```bash
python task_tracker.py mark-in-progress 1
```

Output:
```
Task 1 marked as in-progress.
```

### Mark a Task as Done

```bash
python task_tracker.py mark-done <task_id>
```

Example:
```bash
python task_tracker.py mark-done 1
```

Output:
```
Task 1 marked as done.
```

### List All Tasks

```bash
python task_tracker.py list
```

Output:
```
ID: 1 | Buy groceries | Status: todo | Created: 2024-08-28 12:34:56 | Updated: 2024-08-28 12:34:56
ID: 2 | Finish report | Status: in-progress | Created: 2024-08-28 13:00:00 | Updated: 2024-08-28 14:30:00
```

### List Tasks by Status

```bash
python task_tracker.py list <status>
```

Example:
```bash
python task_tracker.py list done
```

Output:
```
ID: 3 | Call mom | Status: done | Created: 2024-08-28 10:00:00 | Updated: 2024-08-28 11:00:00
```

## Task Properties

Each task has the following properties:

- `id`: A unique identifier for the task
- `description`: A short description of the task
- `status`: The current status of the task (todo, in-progress, done)
- `createdAt`: The date and time when the task was created
- `updatedAt`: The date and time when the task was last updated

## Data Storage

Tasks are stored in a JSON file named `tasks.json` in the current directory. The file is created automatically if it doesn't exist.

## Error Handling

The application includes robust error handling for:

- Invalid task IDs
- Missing arguments
- Invalid commands
- File I/O errors

If you encounter any issues, the application will provide clear error messages to help you resolve them.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all the contributors who have helped to improve this project.
- Inspired by various task management tools and productivity applications.

---

For more information or to report issues, please visit the [project repository](https://github.com/yourusername/task-tracker-cli).