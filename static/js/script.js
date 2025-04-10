document.addEventListener('DOMContentLoaded', () => {
    const userList = document.getElementById('user-list');
    const selectedUserInfo = document.getElementById('selected-user-info');
    const editButton = document.getElementById('edit-user-button');
    const deleteButton = document.getElementById('delete-user-button');
    const editForm = document.getElementById('edit-form');
    const editUserNameInput = document.getElementById('edit-user-name');
    
    let selectedUser = null;

    // Function to display users in the list
    function displayUsers(users) {
        userList.innerHTML = ''; // Clear existing list
        if (!users || users.length === 0) {
            userList.innerHTML = '<li>No users found or error loading users.</li>';
            return;
        }
        users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = `ID: ${user.id}, Name: ${user.name}`;
            listItem.dataset.userId = user.id;
            listItem.dataset.userName = user.name;
            
            // Add click handler for selection
            listItem.addEventListener('click', () => selectUser(user, listItem));
            
            userList.appendChild(listItem);
        });
    }

    // Function to select a user
    function selectUser(user, listItem) {
        // Remove selection from previously selected user
        const previouslySelected = userList.querySelector('.selected');
        if (previouslySelected) {
            previouslySelected.classList.remove('selected');
        }

        // Add selection to clicked user
        listItem.classList.add('selected');
        selectedUser = user;

        // Update sidebar info
        selectedUserInfo.innerHTML = `
            <p><strong>Selected User:</strong></p>
            <p>ID: ${user.id}</p>
            <p>Name: ${user.name}</p>
        `;

        // Enable action buttons
        editButton.disabled = false;
        deleteButton.disabled = false;

        // Hide edit form if it's open
        editForm.classList.add('hidden');
    }

    // Function to edit selected user
    window.editSelectedUser = function() {
        if (!selectedUser) return;

        editUserNameInput.value = selectedUser.name;
        editForm.classList.remove('hidden');
    }

    // Function to save user edit
    window.saveUserEdit = function() {
        const newName = editUserNameInput.value.trim();
        if (!newName || !selectedUser) return;

        fetch(`/api/users/${selectedUser.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newName })
        })
        .then(response => response.json())
        .then(updatedUser => {
            console.log('User updated:', updatedUser);
            editForm.classList.add('hidden');
            fetchUsers(); // Refresh the list
        })
        .catch(error => console.error('Error updating user:', error));
    }

    // Function to cancel edit
    window.cancelEdit = function() {
        editForm.classList.add('hidden');
    }

    // Function to delete selected user
    window.deleteSelectedUser = function() {
        if (!selectedUser) return;

        if (confirm(`Are you sure you want to delete user "${selectedUser.name}"?`)) {
            fetch(`/api/users/${selectedUser.id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(result => {
                console.log('User deleted:', result);
                selectedUser = null;
                selectedUserInfo.innerHTML = '<p>Select a user to perform actions</p>';
                editButton.disabled = true;
                deleteButton.disabled = true;
                fetchUsers(); // Refresh the list
            })
            .catch(error => console.error('Error deleting user:', error));
        }
    }

    // Function to fetch users from the API
    function fetchUsers() {
        fetch('/api/users')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(users => {
                displayUsers(users);
            })
            .catch(error => {
                console.error('Error fetching users:', error);
                displayUsers(null);
            });
    }

    // Function to create a new user
    window.createUser = function() {
        const userNameInput = document.getElementById('new-user-name');
        const userName = userNameInput.value.trim();

        if (!userName) {
            alert('Please enter a user name');
            return;
        }

        fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: userName })
        })
        .then(response => response.json())
        .then(newUser => {
            console.log('User created:', newUser);
            userNameInput.value = ''; // Clear the input
            fetchUsers(); // Refresh the list
        })
        .catch(error => console.error('Error creating user:', error));
    }

    // Initial fetch of users when the page loads
    fetchUsers();
}); 