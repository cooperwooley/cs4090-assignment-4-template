import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks
from datetime import datetime, timedelta

TEST_FILE = "test_tasks.json"

scenarios('../add_task.feature')

@pytest.fixture
def empty_tasks(monkeypatch):
    monkeypatch.setattr("tasks.DEFAULT_TASKS_FILE", TEST_FILE)
    save_tasks([])
    return []

# --- Given ---

@given("there are no tasks")
def no_tasks(empty_tasks):
    pass

@given(parsers.parse('a task with priority "{priority}" exists'))
def task_with_priority_exists(empty_tasks, priority):
    task = {
        "id": 1,
        "title": f"Task with {priority} priority",
        "description": "",
        "priority": priority,
        "category": "General",
        "due_date": datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_tasks([task])

@given(parsers.parse('a task with category "{category}" exists'))
def task_with_category_exists(empty_tasks, category):
    task = {
        "id": 1,
        "title": f"Task in {category}",
        "description": "",
        "priority": "Medium",
        "category": category,
        "due_date": datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_tasks([task])

@given(parsers.parse('a task titled "{title}" exists'))
def task_with_title_exists(empty_tasks, title):
    task = {
        "id": 1,
        "title": title,
        "description": "",
        "priority": "Medium",
        "category": "School",
        "due_date": datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_tasks([task])

@given("a task with due date in the past exists")
def task_with_past_due_date(empty_tasks):
    task = {
        "id": 1,
        "title": "Past Due Task",
        "description": "",
        "priority": "High",
        "category": "Work",
        "due_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_tasks([task])

# --- When ---

@when(parsers.parse('I add a new task with title "{title}"'))
def add_new_task(title):
    tasks = load_tasks()
    new_task = {
        "id": generate_unique_id(tasks),
        "title": title,
        "description": "",
        "priority": "Medium",
        "category": "Personal",
        "due_date": datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)

@when(parsers.parse('I filter tasks by priority "{priority}"'))
def filter_by_priority(priority):
    tasks = load_tasks()
    filtered = filter_tasks_by_priority(tasks, priority)
    save_tasks(filtered)

@when(parsers.parse('I filter tasks by category "{category}"'))
def filter_by_category(category):
    tasks = load_tasks()
    filtered = filter_tasks_by_category(tasks, category)
    save_tasks(filtered)

@when(parsers.parse('I mark the task "{title}" as completed'))
def mark_task_completed(title):
    tasks = load_tasks()
    for task in tasks:
        if task["title"] == title:
            task["completed"] = True
    save_tasks(tasks)

@when("I get overdue tasks")
def get_overdue():
    overdue = get_overdue_tasks(load_tasks())
    save_tasks(overdue)

# --- Then ---

@then("there should be 1 task")
def there_should_be_one_task():
    tasks = load_tasks()
    assert len(tasks) == 1

@then(parsers.parse('the task title should be "{title}"'))
def task_title_should_be(title):
    tasks = load_tasks()
    assert tasks[0]["title"] == title

@then("I should find 1 task")
def should_find_one_task():
    tasks = load_tasks()
    assert len(tasks) == 1

@then(parsers.parse('the task "{title}" should be marked as completed'))
def task_should_be_completed(title):
    tasks = load_tasks()
    for task in tasks:
        if task["title"] == title:
            assert task["completed"] is True

@then("I should find 1 overdue task")
def should_find_one_overdue_task():
    tasks = load_tasks()
    assert len(tasks) == 1