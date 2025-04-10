from flask import Flask, jsonify, request, render_template
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# In-memory storage for users (replace with database later)
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'}
]
next_user_id = 4

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
        description: Missing 'name' in request body
    """
    global next_user_id
    if not request.json or not 'name' in request.json:
        return jsonify({'error': 'Missing name in request body'}), 400

    new_user = {
        'id': next_user_id,
        'name': request.json['name']
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

if __name__ == '__main__':
    app.run(debug=True) 