from flask import Flask, jsonify, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = load_tasks()

    
    if request.method == 'POST':
        description = request.form.get("description")
        category = request.form.get("category")

        
        if description and category:
            new_task = {
                "id": max(task["id"] for task in tasks) + 1 if tasks else 1,
                "description": description,
                "category": category,
                "status": "pending"
            }
            tasks.append(new_task)
            save_tasks(tasks)

    return render_template('index.html', tasks=tasks)


@app.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    password = request.form.get('password')

    
    if password == '123':
        tasks = [task for task in tasks if task["id"] != task_id]
        save_tasks(tasks)
        return redirect(url_for('index'))
    else:
        
        error_message = "Fel lösenord, uppgiften kunde inte tas bort!"
        return render_template('index.html', tasks=tasks, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
