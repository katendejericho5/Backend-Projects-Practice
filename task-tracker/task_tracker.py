import json
import sys
import os
from datetime import datetime

# File path for tasks.json
TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def generate_id(tasks):
    if tasks:
        return tasks[-1]['id'] + 1
    return 1

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


def main():
    args = sys.argv[1:]
    if not args:
        print("Please provide a command.")
        return
    if command == 'add' and len(args) > 1:
        add_task(args[1])
    if command == 'update' and len(args) > 2:
        update_task(int(args[1]), args[2])

    
    command = args[0]
    
    # Command handling will go here

if __name__ == '__main__':
    main()
