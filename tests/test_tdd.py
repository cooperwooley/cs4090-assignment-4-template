import pytest
from tasks import mark_all_tasks_completed, search_tasks, get_overdue_tasks
from datetime import datetime, timedelta

def test_mark_all_tasks_completed():
    tasks = [
        {"id": 1, "title": "Task 1", "completed": False},
        {"id": 2, "title": "Task 2", "completed": False}
    ]
    updated_tasks = mark_all_tasks_completed(tasks)
    assert all(task["completed"] for task in updated_tasks)

def test_search_tasks():
    tasks = [
        {"id": 1, "title": "Buy eggs", "description": "Get 2 dozen", "completed": False},
        {"id": 2, "title": "Homework", "description": "Math assignment", "completed": False}
    ]
    result = search_tasks(tasks, "eggs")
    assert len(result) == 1
    assert result[0]["title"] == "Buy eggs"

def test_get_overdue_tasks():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [
        {"id": 1, "title": "Old Task", "due_date": yesterday, "completed": False},
        {"id": 2, "title": "Future Task", "due_date": tomorrow, "completed": False}
    ]
    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1
    assert overdue[0]["title"] == "Old Task"