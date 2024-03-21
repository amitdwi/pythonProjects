from flask import Flask, request, jsonify, current_app

from db import db
from cache import redisClient
from bson.objectid import ObjectId

tasks = db['tasks']

taskSchema = {
    'assignee': str,
    'description': str,
    'status': str
}

class Tasks:

    # Create Task

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
    
    # Get All Tasks

    def get_tasks(self):
        query = {}
        # Filter by status
        if request.args.get('status'):
            query['status'] = request.args.get('status')
        # Filter by assignee
        if request.args.get('assignee'):
            query['assignee'] = request.args.get('assignee')
    
        Tasks = tasks.find(query)
        return [{**task, "_id": str(task["_id"])} for task in Tasks], 200
    
    # Get task by ID

    def get_task(self, task_id):
        task = redisClient.json().get(task_id)
        if not task or not task["_id"]:
            task = tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            return {**task, "_id": str(task["_id"])}, 200
        return jsonify({'message': 'Task not found'}), 404
    
    # Update task 

    def update_task(self, task_id):
        task_data = request.json
        if 'assignee' not in task_data:
            task_data['assignee'] = 'unassigned'
        updated_task = {}
        for key in taskSchema.keys():
            if key in task_data:
                updated_task[key] = task_data[key]
        result = tasks.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
        if result.modified_count > 0:
            updated_task = tasks.find_one({'_id': ObjectId(task_id)})
            updated_task['_id'] = str(updated_task['_id'])
            redisClient.json().set(task_id , '$', updated_task)
            return jsonify({'message': 'Task updated !!'}), 200
        return jsonify({'message': 'Task not found'}), 404
    
    # Delete task 

    def delete_task(self, task_id):
        result = tasks.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count > 0:
            redisClient.delete(task_id)
            return jsonify({'message': 'Task deleted successfully'}), 200
        return jsonify({'message': 'Task not found'}), 404