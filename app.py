from flask import Flask
from routes.tasks import Tasks

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Home page'

@app.route('/tasks', methods=['POST'])
def create_tasks():
    return Tasks().create_task()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return Tasks().get_tasks()

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    return Tasks().get_task(task_id)


if __name__ == "__main__":
    app.run(debug=True)
    