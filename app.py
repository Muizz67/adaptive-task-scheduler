from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Make sure run in '/adaptive-task-scheduler'
DB_PATH = 'db/TaskScheduleDB.json' # change accordingly

def load_tasks():
    with open(DB_PATH, 'r') as file:
        return json.load(file)

def save_task(task):
    tasks = load_tasks()
    tasks.append(task)
    with open(DB_PATH, 'w') as file:
        json.dump(tasks, file, indent=4)

 # Sort tasks by StartTime within each day
def groupTasks(tasks):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grouped_tasks = {day: [] for day in days}
    
    for task in tasks:
        task_date = datetime.strptime(task['Date'], '%Y-%m-%d')
        day_of_week = task_date.strftime('%A')  # Get the full name of the day

        if day_of_week in grouped_tasks:
            grouped_tasks[day_of_week].append(task)
    
    # Sort tasks by StartTime (from 00:00 to 23:59)
    for day in grouped_tasks:
        grouped_tasks[day] = sorted(grouped_tasks[day], key=lambda x: datetime.strptime(x['StartTime'], "%H:%M:%S"))
    
    return grouped_tasks

# Routing
@app.route('/')
def schedule():
    tasks = load_tasks()
    grouped_tasks = groupTasks(tasks)
    return render_template('schedule.html', tasks=grouped_tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    task_data = request.json
    if task_data:
        save_task(task_data)
        return jsonify({'message': 'Task added successfully'}), 200
    return jsonify({'message': 'Failed to add task'}), 400

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    grouped_tasks = groupTasks(tasks)
    return jsonify(grouped_tasks)

if __name__ == '__main__':
    app.run(debug=True)
