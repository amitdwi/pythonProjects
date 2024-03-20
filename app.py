from flask import Flask
from routes.tasks import Tasks

app = Flask(__name__)

@app.route('/tasks', methods=['POST'])
def create_tasks():
    return Tasks().create_task()

@app.route('/')
def home():
    return 'Welcome to Home page'

if __name__ == "__main__":
    app.run(debug=True)
    