import os
import json
from datetime import datetime

TASK_FILE = "tasks.json"

# Load tasks
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)

# Save tasks
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task cannot be empty.")
        return

    priority = input("Priority (High/Medium/Low): ").capitalize()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"

    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    try:
        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")
    except:
        print("Invalid date format. Setting due date as None.")
        due_date = ""

    task = {
        "title": title,
        "status": "Pending",
        "priority": priority,
        "due_date": due_date
    }

    tasks.append(task)
    print("Task added successfully!")

# Display tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- YOUR TASKS ---")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']}  |  {task['status']}  |  Priority: {task['priority']}  |  Due: {task['due_date'] or 'None'}")
    print("-------------------\n")

# Select index helper
def choose_index(tasks, prompt):
    view_tasks(tasks)
    if not tasks:
        return None
    try:
        num = int(input(prompt))
        if 1 <= num <= len(tasks):
            return num - 1
    except:
        pass
    print("Invalid task number.")
    return None

# Mark complete
def complete_task(tasks):
    idx = choose_index(tasks, "Enter task number to mark complete: ")
    if idx is not None:
        tasks[idx]["status"] = "Completed"
        print("Task marked as completed!")

# Delete task
def delete_task(tasks):
    idx = choose_index(tasks, "Enter task number to delete: ")
    if idx is not None:
        tasks.pop(idx)
        print("Task deleted successfully!")

# Edit task
def edit_task(tasks):
    idx = choose_index(tasks, "Enter task number to edit: ")
    if idx is None:
        return

    new_title = input("New title (leave blank to keep current): ").strip()
    if new_title:
        tasks[idx]["title"] = new_title

    new_priority = input("New priority (High/Medium/Low, leave blank to keep): ").capitalize()
    if new_priority in ["High", "Medium", "Low"]:
        tasks[idx]["priority"] = new_priority

    new_due = input("New due date (YYYY-MM-DD, blank to keep): ").strip()
    if new_due:
        try:
            datetime.strptime(new_due, "%Y-%m-%d")
            tasks[idx]["due_date"] = new_due
        except:
            print("Invalid format. Keeping old date.")

    print("Task updated!")

# Search tasks
def search_tasks(tasks):
    keyword = input("Enter keyword to search: ").lower()
    results = [t for t in tasks if keyword in t["title"].lower()]

    if not results:
        print("No matching tasks found.")
        return

    print("\n--- SEARCH RESULTS ---")
    for task in results:
        print(f"- {task['title']} | {task['status']} | {task['priority']} | {task['due_date'] or 'None'}")
    print("-----------------------\n")

# Sort tasks
def sort_tasks(tasks):
    print("1. Sort by priority")
    print("2. Sort by due date")
    choice = input("Choose sorting method: ")

    if choice == "1":
        order = {"High": 1, "Medium": 2, "Low": 3}
        tasks.sort(key=lambda x: order[x["priority"]])
        print("Sorted by priority.")
    elif choice == "2":
        tasks.sort(key=lambda x: x["due_date"] or "9999-12-31")
        print("Sorted by due date.")
    else:
        print("Invalid choice.")

# Clear all tasks
def clear_all(tasks):
    confirm = input("Are you sure you want to delete ALL tasks? (yes/no): ")
    if confirm.lower() == "yes":
        tasks.clear()
        print("All tasks cleared!")
    else:
        print("Cancelled.")

# Main program
def main():
    tasks = load_tasks()

    while True:
        print("\n==== TO-DO LIST MENU ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Search Task")
        print("7. Sort Tasks")
        print("8. Clear All Tasks")
        print("9. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            search_tasks(tasks)
        elif choice == "7":
            sort_tasks(tasks)
        elif choice == "8":
            clear_all(tasks)
        elif choice == "9":
            save_tasks(tasks)
            print("All tasks saved. Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
