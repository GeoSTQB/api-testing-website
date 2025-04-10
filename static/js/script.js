document.addEventListener('DOMContentLoaded', () => {
    const userList = document.getElementById('user-list');

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
            userList.appendChild(listItem);
        });
    }

    // Function to fetch users from the API
    function fetchUsers() {
        fetch('/api/users') // Fetch from the API endpoint
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
                displayUsers(null); // Display error message in the list
            });
    }

    // Initial fetch of users when the page loads
    fetchUsers();

    // Function to create a new user
    function createUser() {
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

    // Expose the createUser function globally so it can be called from the button
    window.createUser = createUser;
}); 