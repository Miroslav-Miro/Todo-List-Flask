from flask import Flask, request, jsonify , send_from_directory
import db
import os


app = Flask(__name__, static_folder=os.path.join(os.getcwd(), '..', 'frontend'))

@app.route('/')
def index():
    index_path = os.path.join(os.getcwd(), '..', 'frontend', 'index.html')  
    print(f"Resolved index.html path: {index_path}")
    return send_from_directory(os.path.join(os.getcwd(), '..', 'frontend'), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    file_path = os.path.join(os.getcwd(), '..', 'frontend', filename)  
    print(f"Resolved file path: {file_path}")
    return send_from_directory(os.path.join(os.getcwd(), '..', 'frontend'), filename)


@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get('task_name')
    
    if task_name:
        db.add_task(task_name)
        return jsonify({'message': 'Task added!'}), 201
    else:
        return jsonify({'message': 'Task name is required!'}), 400
    
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    db.delete_task(id)
    
    task = db.get_task_by_id(id)
    if task == None:
        return jsonify({'message': 'Task not found!'}), 404
    
    
@app.route('/update/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.get_task_by_id(id)
    if task == None:
        return jsonify({'message': 'Task not found!'}), 404

    db.complete_task(id)
    return jsonify({'message': f'Task {id} marked as completed!'}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_tasks()
    return jsonify(tasks), 200

if __name__ == '__main__':
    app.run(debug=True)
    print('ALEYUYA its running')
