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

# Helper function to find a task by ID
def find_task_by_id(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# Route: Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tasks=tasks)

# Route: Add Task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["task_name"]
        due_time_str = request.form["due_time"]
        priority = int(request.form["priority"])

        try:
            due_time = datetime.strptime(due_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD HH:MM."

        suggestions = analyze_task_description(task_name)
        tasks.append({
            "id": len(tasks) + 1,
            "task": task_name,
            "due_time": due_time,
            "priority": priority,
            "status": "Not Started",
            "suggestions": suggestions
        })
        return redirect(url_for("index"))
    
    # Form for adding a task
    return render_template("add_task.html")

# Route: Show Tasks
@app.route("/show_tasks", methods=["GET", "POST"])
def show_tasks():
    mood = request.form.get("mood", "neutral")  # Default mood if not provided
    sorted_tasks = prioritize_tasks(mood)
    return render_template("show_tasks.html", tasks=sorted_tasks)

# Route: Update Task Status
@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    task = find_task_by_id(task_id)
    if not task:
        return "Task not found.", 404

    if request.method == "POST":
        new_status = request.form["new_status"]
        task["status"] = new_status
        return redirect(url_for("index"))
    
    # Form for updating task status
    return render_template("update_task.html", task=task)

# Helper Functions
def prioritize_tasks(mood):
    if mood.lower() in ["stressed", "busy", "overwhelmed"]:
        return sorted(tasks, key=lambda x: x['priority'], reverse=True)
    return sorted(tasks, key=lambda x: x['priority'])

# Run the App
if __name__ == "__main__":
    app.run(debug=True)