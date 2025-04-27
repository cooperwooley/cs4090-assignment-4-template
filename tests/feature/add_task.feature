Feature: Adding and Managing Tasks
    As a user
    I want to add, view, and manage my tasks
    So that I can stay organized

    Scenario: Add a new tasks successfully
        Given there are no tasks
        When I add a new task with title "Buy Groceries"
        Then there should be 1 task
        And the task title should be "Buy Groceries"

    Scenario: Filter tasks by priority
        Given a task with priority "High" exists
        When I filter tasks by priority "High"
        Then I should find 1 task

    Scenario: Filter tasks by category
        Given a task with category "Work" exists
        When I filter tasks by category "Work"
        Then I should find 1 task

    Scenario: Mark task as completed
        Given a task titled "Finish Homework" exists
        When I mark the task "Finish Homework" as completed
        Then the task "Finish Homework" should be marked as completed

    Scenario: Find overdue tasks
        Given a task with due date in the past exists
        When I get overdue tasks
        Then I should find 1 overdue task

