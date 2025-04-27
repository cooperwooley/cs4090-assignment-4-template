import pytest
import os
from datetime import datetime, timedelta
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks

TEST_FILE = "test_tasks.json"

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "description": "Description 1", "priority": "High", "category": "Personal", "due_date": "2099-01-01", "completed": False},
        {"id": 2, "title": "Task 2", "description": "Description 2", "priority": "Medium", "category": "Work", "due_date": "2000-01-01", "completed": True},
        {"id": 3, "title": "Task 3", "description": "Description 3", "priority": "Low", "category": "School", "due_date": "2099-01-01", "completed": False}
    ]

def test_save_and_load_tasks(sample_tasks):
    save_tasks(sample_tasks, TEST_FILE)
    loaded_tasks = load_tasks(TEST_FILE)
    assert loaded_tasks == sample_tasks
    os.remove(TEST_FILE)

def test_generate_unique_id(sample_tasks):
    new_id = generate_unique_id(sample_tasks)
    assert new_id == 4

def test_filter_tasks_by_priority(sample_tasks):
    high_priority_tasks = filter_tasks_by_priority(sample_tasks, "High")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0]["title"] == "Task 1"

def test_filter_tasks_by_category(sample_tasks):
    personal_tasks = filter_tasks_by_category(sample_tasks, "Personal")
    assert len(personal_tasks) == 1
    assert personal_tasks[0]["category"] == "Personal"

def test_filter_tasks_by_completion(sample_tasks):
    completed_tasks = filter_tasks_by_completion(sample_tasks, completed=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["completed"] is True

    incomplete_tasks = filter_tasks_by_completion(sample_tasks, completed=False)
    assert len(incomplete_tasks) == 2
    assert all(not task["completed"] for task in incomplete_tasks)

def tests_get_overdue_tasks(sample_tasks):
    overdue_tasks = get_overdue_tasks(sample_tasks)
    assert len(overdue_tasks) == 0

    sample_tasks[0]["due_date"] = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    overdue_tasks = get_overdue_tasks(sample_tasks)
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0]["title"] == "Task 1"