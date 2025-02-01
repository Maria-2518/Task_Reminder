from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Global variables
tasks = []

# Function to analyze task description
def analyze_task_description(task_name):
    suggestions = []
    if "report" in task_name.lower():
        suggestions.append("Prepare data for the report")
        suggestions.append("Review previous reports for insights")
    elif "meeting" in task_name.lower():
        suggestions.append("Prepare agenda for the meeting")
        suggestions.append("Review meeting notes from last meeting")
    if "urgent" in task_name.lower() or "asap" in task_name.lower():
        suggestions.append("Prioritize this task as it is urgent")
    return suggestions

# Route: Home Page
@app.route("/", methods=["GET"])
def index():
    # Generate HTML dynamically
    task_list = "<ul>"
    for task in tasks:
        task_list += f"<li>{task['task']} - Due: {task['due_time'].strftime('%Y-%m-%d %H:%M')} <a href='{url_for('update_task', task_name=task['task'])}'>Update Status</a></li>"
    task_list += "</ul>"

    return f"""
    <h2>Home</h2>
    <a href="{url_for('add_task')}">Add Task</a>
    <a href="{url_for('show_tasks')}">Show Tasks</a>
    {task_list}
    """

# Route: Add Task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["task_name"]
        due_time_str = request.form["due_time"]
        priority = int(request.form["priority"])
        due_time = datetime.strptime(due_time_str, "%Y-%m-%d %H:%M")
        suggestions = analyze_task_description(task_name)
        tasks.append({
            "task": task_name,
            "due_time": due_time,
            "reminded": False,
            "priority": priority,
            "status": "Not Started",
            "suggestions": suggestions
        })
        return redirect(url_for("index"))
    
    # Form for adding a task
    return """
    <h2>Add Task</h2>
    <form method="POST">
        <label for="task_name">Task Name:</label>
        <input type="text" id="task_name" name="task_name" required><br>
        <label for="due_time">Due Time (YYYY-MM-DD HH:MM):</label>
        <input type="text" id="due_time" name="due_time" placeholder="YYYY-MM-DD HH:MM" required><br>
        <label for="priority">Priority (1-5):</label>
        <input type="number" id="priority" name="priority" min="1" max="5" required><br>
        <button type="submit">Add Task</button>
    </form>
    <a href="/">Back to Home</a>
    """

# Route: Show Tasks
@app.route("/show_tasks", methods=["GET", "POST"])
def show_tasks():
    mood = request.form.get("mood", "neutral")  # Default mood if not provided
    sorted_tasks = prioritize_tasks(mood)

    # Generate HTML dynamically
    task_list = "<ul>"
    for task in sorted_tasks:
        task_list += f"<li>{task['task']} - Priority: {task['priority']}, Status: {task['status']}</li>"
    task_list += "</ul>"

    return f"""
    <h2>Your Tasks</h2>
    <form method="POST">
        <label for="mood">How are you feeling today?</label>
        <input type="text" id="mood" name="mood" placeholder="happy, stressed, relaxed, etc." required>
        <button type="submit">Sort Tasks</button>
    </form>
    {task_list}
    <a href="/">Back to Home</a>
    """

# Route: Update Task Status
@app.route("/update_task/<task_name>", methods=["GET", "POST"])
def update_task(task_name):
    if request.method == "POST":
        new_status = request.form["new_status"]
        update_task_status(task_name, new_status)
        return redirect(url_for("index"))
    
    # Form for updating task status
    return f"""
    <h2>Update Task Status</h2>
    <form method="POST">
        <label for="new_status">New Status:</label>
        <select id="new_status" name="new_status">
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
        </select><br>
        <button type="submit">Update</button>
    </form>
    <a href="/">Back to Home</a>
    """

# Helper Functions
def update_task_status(task_name, new_status):
    for task in tasks:
        if task["task"] == task_name:
            task["status"] = new_status
            break

def prioritize_tasks(mood):
    if mood.lower() in ["stressed", "busy", "overwhelmed"]:
        return sorted(tasks, key=lambda x: x['priority'], reverse=True)
    return sorted(tasks, key=lambda x: x['priority'])

# Run the App
if __name__ == "__main__":
    app.run(debug=True)