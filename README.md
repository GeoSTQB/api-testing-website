<img align=right style="width: 5em;" src="static/icons/GeoSQTB%20vector%20logo.png">

# 🚀 API Testing Website

A simple Flask-based web application for testing API endpoints with a user-friendly interface. This project demonstrates basic CRUD operations (Create, Read, Update, Delete) for user management.

## ✨ Features

- User-friendly web interface
- RESTful API endpoints for user management
- Interactive Swagger documentation
- Modern UI with responsive design

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/GeoSTQB/api-testing-website.git
cd api-testing-website
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
api-testing-website/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── css/
│   │   └── style.css  # Stylesheet
│   ├── js/
│   │   └── script.js  # JavaScript code
│   └── icons/         # Image assets
└── templates/
    └── index.html     # Main HTML template
```

## 🚀 Running the Application

1. Make sure you're in the project directory and your virtual environment is activated.

2. Start the Flask development server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 📚 API Documentation

The application includes Swagger documentation. To access it, visit:
```
http://127.0.0.1:5000/apidocs
```

## 🔌 Available API Endpoints

- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
- `GET /api/users/<id>` - Get a specific user
- `PUT /api/users/<id>` - Update a user
- `PATCH /api/users/<id>` - Partially update a user
- `DELETE /api/users/<id>` - Delete a user

## 💻 Using the Web Interface

1. **View Users**
   - The main page displays a list of all registered users
   - Each user is shown with their ID and name

2. **Create a User**
   - Enter the user's name in the input field
   - Click the "Create New User" button
   - The new user will appear in the list

## ⚠️ Troubleshooting

If you encounter any issues:

1. **Port already in use**
   - Make sure no other application is using port 5000
   - You can change the port in `app.py` by modifying the `app.run()` line

2. **Module not found errors**
   - Ensure all dependencies are installed correctly
   - Try running `pip install -r requirements.txt` again

3. **Static files not loading**
   - Make sure you're running the application through Flask
   - Don't open the HTML file directly in the browser

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 
