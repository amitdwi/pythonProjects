from flask import Flask, request, jsonify

from db import db
from cache import redisClient

tasks = db['tasks']

taskSchema = {
    'email': str,
    'assignee': str,
    'description': str,
    'status': str
}

class Tasks:

    def create_task(self):
        task_data = request.json
        if 'assignee' not in task_data:
            task_data['assignee'] = 'unassigned'
        new_task = {}
        for key in taskSchema.keys():
            if key in task_data:
                new_task[key] = task_data[key]
        result = tasks.insert_one(new_task)
        inserted_task = tasks.find_one({'_id': result.inserted_id})
        inserted_task['_id'] = str(inserted_task['_id'])
        redisClient.json().set(inserted_task['_id'], '$', inserted_task)
        return jsonify({'msg': "Task created successfully"}), 201