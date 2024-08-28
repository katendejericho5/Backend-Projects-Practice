import sys
import json
from datetime import datetime

# File to store expenses
EXPENSE_FILE = 'expense-tracker/expenses.json'

def load_expenses():
    try:
        with open(EXPENSE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def add_expense(description, amount):
    expenses = load_expenses()
    expense_id = len(expenses) + 1
    expense = {
        'id': expense_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense_id})")

def list_expenses():
    expenses = load_expenses()
    if expenses:
        print(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount':<10}")
        for exp in expenses:
            print(f"{exp['id']:<5} {exp['date']:<12} {exp['description']:<20} ${exp['amount']:<10}")
    else:
        print("No expenses found.")

def delete_expense(expense_id):
    expenses = load_expenses()
    filtered_expenses = [exp for exp in expenses if exp['id'] != expense_id]
    if len(filtered_expenses) < len(expenses):
        save_expenses(filtered_expenses)
        print(f"Expense {expense_id} deleted successfully")
    else:
        print(f"Expense ID {expense_id} not found")

def update_expense(expense_id, description, amount):
    expenses = load_expenses()
    for exp in expenses:
        if exp['id'] == expense_id:
            exp['description'] = description
            exp['amount'] = amount
            save_expenses(expenses)
            print(f"Expense {expense_id} updated successfully")
            return
    print(f"Expense ID {expense_id} not found")

def show_summary(month=None):
    expenses = load_expenses()
    total = 0
    for exp in expenses:
        if month:
            if datetime.strptime(exp['date'], '%Y-%m-%d').month == month:
                total += exp['amount']
        else:
            total += exp['amount']
    
    if month:
        print(f"Total expenses for month {month}: ${total}")
    else:
        print(f"Total expenses: ${total}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python expense_tracker.py <command> [options]")
        return
    
    command = sys.argv[1]
    
    if command == 'add':
        description = sys.argv[3]
        amount = float(sys.argv[5])
        add_expense(description, amount)
    elif command == 'list':
        list_expenses()
    elif command == 'delete':
        expense_id = int(sys.argv[3])
        delete_expense(expense_id)
    elif command == 'update':
        expense_id = int(sys.argv[3])
        description = sys.argv[5]
        amount = float(sys.argv[7])
        update_expense(expense_id, description, amount)
    elif command == 'summary':
        if len(sys.argv) > 3 and sys.argv[2] == '--month':
            month = int(sys.argv[3])
            show_summary(month)
        else:
            show_summary()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
