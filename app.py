from flask import Flask, jsonify, request, render_template
from flasgger import Swagger
from datetime import datetime
import uuid

app = Flask(__name__)
swagger = Swagger(app)

# In-memory storage for users (replace with database later)
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'}
]
next_user_id = 4

# In-memory storage for async tasks
async_tasks = {}

def generate_unique_id():
    return str(uuid.uuid4())

# --- API Endpoints ---

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Returns the list of all users.
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The user ID
              name:
                type: string
                description: The user name
    """
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Creates a new user.
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: Name for the new user
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      400:
        description: Missing 'name' in request body or name is empty/contains only spaces
    """
    global next_user_id
    if not request.json or not 'name' in request.json:
        return jsonify({'error': 'Missing name in request body'}), 400

    name = request.json['name'].strip()
    if not name:
        return jsonify({'error': 'Name cannot be empty or contain only spaces'}), 400

    new_user = {
        'id': next_user_id,
        'name': name
    }
    users.append(new_user)
    next_user_id += 1
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Returns a specific user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to retrieve
    responses:
      200:
        description: User details
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates an existing user (replaces the entire user).
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: New name for the user
    responses:
      200:
        description: User updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      400:
        description: Missing 'name' in request body
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'Missing name in request body'}), 400

    # In a real app, you might validate the input further
    user['name'] = request.json['name']
    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    """
    Partially updates an existing user.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to partially update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: New name for the user (optional)
    responses:
      200:
        description: User updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
      400:
        description: Missing request body
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if not request.json:
        return jsonify({'error': 'Missing request body'}), 400

    # Update fields present in the request
    if 'name' in request.json:
        user['name'] = request.json['name']
        # Add other fields here if needed

    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: User not found
    """
    global users
    initial_length = len(users)
    users = [u for u in users if u['id'] != user_id]
    if len(users) == initial_length:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/')
def index():
    # Serve the main HTML page using render_template
    return render_template('index.html')

@app.route('/api-testing')
def api_testing():
    # Serve the API testing page
    return render_template('api_testing.html')

@app.route('/api/silent-error', methods=['POST'])
def silent_error():
    """
    Demonstrates a problematic API pattern where 200 OK is returned with an error in the body.
    ---
    tags:
      - Testing
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
          properties:
            username:
              type: string
              description: Username to validate
    responses:
      200:
        description: Always returns 200 OK, even with errors
        schema:
          type: object
          properties:
            success:
              type: boolean
            error:
              type: string
    """
    if not request.json or 'username' not in request.json:
        return jsonify({
            'success': False,
            'error': 'Username is required'
        })
    
    username = request.json['username']
    if len(username) < 3:
        return jsonify({
            'success': False,
            'error': 'Username must be at least 3 characters long'
        })
    
    return jsonify({
        'success': True,
        'message': 'User created successfully'
    })

@app.route('/api/async-tasks', methods=['POST'])
def create_async_task():
    """
    Creates a new async task.
    ---
    tags:
      - Async Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - description
          properties:
            description:
              type: string
              description: Description of the task
    responses:
      200:
        description: Task created successfully
        schema:
          type: object
          properties:
            task_id:
              type: string
              description: ID of the created task
    """
    if not request.json or 'description' not in request.json:
        return jsonify({'error': 'Missing description in request body'}), 400

    task_id = generate_unique_id()
    task = {
        'id': task_id,
        'description': request.json['description'],
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'error': None
    }
    async_tasks[task_id] = task

    # Simulate async task completion after 5 seconds
    def complete_task():
        import time
        time.sleep(5)
        async_tasks[task_id]['status'] = 'completed'

    import threading
    threading.Thread(target=complete_task).start()

    return jsonify({'task_id': task_id}), 200

@app.route('/api/async-tasks/<task_id>', methods=['GET'])
def get_async_task(task_id):
    """
    Gets the status of an async task.
    ---
    tags:
      - Async Tasks
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
        description: ID of the task to retrieve
    responses:
      200:
        description: Task status
        schema:
          type: object
          properties:
            id:
              type: string
            status:
              type: string
            created_at:
              type: string
            error:
              type: string
      404:
        description: Task not found
    """
    if task_id not in async_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(async_tasks[task_id])

@app.route('/api/incomplete-data', methods=['GET'])
def get_incomplete_data():
    """
    Demonstrates an API that returns 200 OK but with missing or incomplete data.
    ---
    tags:
      - Testing
    responses:
      200:
        description: Always returns 200 OK, but data may be missing or incomplete
        schema:
          type: object
          properties:
            status:
              type: string
            data:
              type: object
              properties:
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    email:
                      type: string
                    profile:
                      type: object
                      properties:
                        bio:
                          type: string
                        avatar:
                          type: string
    """
    # Simulate different scenarios of incomplete data
    import random
    scenario = random.randint(1, 4)
    
    if scenario == 1:
        # Empty data object
        return jsonify({
            'status': 'success',
            'data': {}
        })
    elif scenario == 2:
        # Partial user data
        return jsonify({
            'status': 'success',
            'data': {
                'user': {
                    'id': 1,
                    'name': 'John Doe'
                    # Missing email and profile
                }
            }
        })
    elif scenario == 3:
        # Nested missing data
        return jsonify({
            'status': 'success',
            'data': {
                'user': {
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'profile': {}  # Empty profile object
                }
            }
        })
    else:
        # Complete data (rare case)
        return jsonify({
            'status': 'success',
            'data': {
                'user': {
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'profile': {
                        'bio': 'Software Developer',
                        'avatar': 'https://example.com/avatar.jpg'
                    }
                }
            }
        })

if __name__ == '__main__':
    app.run(debug=True) 