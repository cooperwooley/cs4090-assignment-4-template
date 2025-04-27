import streamlit as st
import pytest
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

def run_test_basic():
    exit_code = pytest.main(["tests/test_basic.py", "-q"])
    if exit_code == 0:
        return "All tests passed!"
    return f"Tests failed with code {exit_code}."

def run_test_coverage():
    exit_code = pytest.main(["--cov=tasks", "tests/", "-q", "--cov-report", "term-missing"])
    if exit_code == 0:
        return "Coverage test passed!"
    return f"Coverage test failed with code {exit_code}."

def run_test_parametrization():
    exit_code = pytest.main(["tests/test_advanced.py::test_filter_tasks_by_priority_param", "-q"])
    if exit_code == 0:
        return "Parametrization tests passed!"
    return f"Parametrization tests failed with code {exit_code}"

def run_test_mocking():
    exit_code = pytest.main(["tests/test_advanced.py::test_load_tasks_mocked", "-q"])
    if exit_code == 0:
        return "Mocking test passed!"
    return f"Mocking test failed with code {exit_code}."

def run_html_report():
    pytest.main(["tests/", "--html=report.html", "--self-contained-html"])
    return "HTML report generated successfully! Check 'report.html' file."

def run_tdd_tests():
    exit_code = pytest.main(["tests/test_tdd.py", "-q"])
    if exit_code == 0:
        return "TDD tests passed!"
    return f"TDD tests failed with code {exit_code}."

def run_bdd_tests():
    exit_code = pytest.main(["tests/feature/steps/test_add_steps.py", "-q"])
    if exit_code == 0:
        return "BDD tests passed!"
    return f"BDD tests failed with code {exit_code}."

if __name__ == "__main__":
    main()

    st.sidebar.header("Testing")

    if st.sidebar.button("Run Tests Basic"):
        st.sidebar.text_area("Test Basic Output", run_test_basic(), height=300)

    if st.sidebar.button("Run Coverage Tests"):
        st.sidebar.text_area("Coverage Test Output", run_test_coverage(), height=300)

    if st.sidebar.button("Run Parametrization Tests"):
        st.sidebar.text_area("Parametrization Test Output", run_test_parametrization(), height=300)

    if st.sidebar.button("Run Mocking Tests"):
        st.sidebar.text_area("Mocking Test Output", run_test_mocking(), height=300)

    if st.sidebar.button("Generate HTML Report"):
        st.sidebar.success(run_html_report())

    if st.sidebar.button("Run TDD Tests"):
        st.sidebar.text_area("TDD Tests Output", run_tdd_tests(), height=300)

    if st.sidebar.button("Run BDD Tests"):
        st.sidebar.text_area("BDD Test Output", run_bdd_tests(), height=300)