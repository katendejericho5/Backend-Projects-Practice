import json
import sys
import os
from datetime import datetime

# File path for tasks.json
TASKS_FILE = 'task-tracker/tasks.json'

# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Generate a new task ID
def generate_id(tasks):
    if tasks:
        return tasks[-1]['id'] + 1
    return 1

# Add a new task
def add_task(description):
    tasks = load_tasks()
    new_task = {
        'id': generate_id(tasks),
        'description': description,
        'status': 'todo',
        'createdAt': str(datetime.now()),
        'updatedAt': str(datetime.now())
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

# Update an existing task
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

# Mark a task as in-progress or done
def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")

# List all tasks, or filter by status
def list_tasks(status=None):
    tasks = load_tasks()
    for task in tasks:
        if status and task['status'] != status:
            continue
        print(f"ID: {task['id']} | {task['description']} | Status: {task['status']} | Created: {task['createdAt']} | Updated: {task['updatedAt']}")

# Main function to handle CLI commands
def main():
    args = sys.argv[1:]
    if not args:
        print("Please provide a command.")
        return
    
    command = args[0]
    
    if command == 'add' and len(args) > 1:
        add_task(args[1])
    elif command == 'update' and len(args) > 2:
        update_task(int(args[1]), args[2])
    elif command == 'delete' and len(args) > 1:
        delete_task(int(args[1]))
    elif command == 'mark-in-progress' and len(args) > 1:
        mark_task(int(args[1]), 'in-progress')
    elif command == 'mark-done' and len(args) > 1:
        mark_task(int(args[1]), 'done')
    elif command == 'list':
        if len(args) > 1:
            list_tasks(args[1])
        else:
            list_tasks()
    else:
        print("Invalid command or missing arguments.")

# Entry point of the script
if __name__ == '__main__':
    main()
