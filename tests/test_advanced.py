import pytest
import os
from unittest import mock
from tasks import load_tasks, filter_tasks_by_priority, save_tasks

TEST_FILE = "test_tasks.json"

@pytest.mark.parametrize(
    "tasks, priority, expected",
    [
        ([{"priority": "High"}, {"priority": "Low"}], "High", [{"priority": "High"}]),
        ([{"priority": "Medium"}, {"priority": "Low"}], "Low", [{"priority": "Low"}]),
        ([], "High", [])
    ]
)
def test_filter_tasks_by_priority_param(tasks, priority, expected):
    assert filter_tasks_by_priority(tasks, priority) == expected

def test_load_tasks_mocked():
    with mock.patch("test_advanced.load_tasks", return_value=[{"id": 1, "title": "Mocked Task"}]):
        tasks = load_tasks()
        assert tasks == [{"id": 1, "title": "Mocked Task"}]

def test_save_tasks():
    tasks = [{"id": 1, "title": "Test Task"}]
    save_tasks(tasks, file_path=TEST_FILE)

    with open(TEST_FILE, "r") as f:
        content = f.read()
        assert '"title": "Test Task"' in content
    
    os.remove(TEST_FILE)