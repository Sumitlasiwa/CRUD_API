"""In-memory task repository and persistence helpers."""

tasks = [
    {"id": 1, "title": "read harry potter", "done": True },
    {"id": 2, "title": "learn api dev 1 hr", "done": False },
    {"id": 3, "title": "upper body workout", "done": False }
]

initial_tasks = tasks.copy()  # Store the initial tasks for reset

def search_task(id):
    """Find a task by ID and return its index and object."""
    for index, task in enumerate(tasks):
        if task['id'] == id:
            return index, task

def create_task(input):
    """Add a new task to the in-memory task list."""
    tasks.append(input)
    return {**input}

def get_tasks_by_done(done: bool):
    return [task for task in tasks if task["done"] == done]

def get_tasks_by_search(search: str):
    return [task for task in tasks if search.lower() in task["title"].lower()]

def get_tasks_by_done_and_search(done: bool, search: str):
    return [task for task in tasks if task["done"] == done and search.lower() in task["title"].lower()]

def get_tasks():
    return tasks

def get_total_tasks():
    return len(tasks)

def get_completed_tasks():
    return len([task for task in tasks if task["done"]])

def reset_tasks():
    global tasks
    tasks = initial_tasks.copy()  # Reset to the initial tasks
    return {"message": "All tasks have been reset!"}

def update_task(index, input):
    tasks[index] = input
    return {**input}

def delete_task(index):
    tasks.pop(index)