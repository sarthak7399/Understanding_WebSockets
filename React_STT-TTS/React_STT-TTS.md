# React_STT-TTS #

## Description ##

This is a full-stack project built with React for the frontend and Python for the backend. The frontend is developed using React.js while the backend is implemented with Python using the FastAPI framework.

## Installation ##

### Frontend (React) ###

1. Make sure you have Node.js and npm installed on your system. If not, download and install them from Node.js website.
2. Clone the repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Run `npm install` to install all the required dependencies.


### Backend (Python) ###

1. Ensure you have Python installed on your system. If not, download and install it from Python's official website.
2. Clone the repository to your local machine.
3. Navigate to the backend directory within the project in your terminal.
4. Create a virtual environment by running `python -m venv env`. Activate the virtual environment using `source env/bin/activate` (for Linux/macOS) or `.\env\Scripts\activate` (for Windows).
5. Run `pip install -r requirements.txt` to install all the necessary Python packages specified in the requirements.txt file.

### Environment Configuration ###

To add a .env file with the specified variables, follow these steps:

1. In the backend directory of your project, create a new file named .env.
2. Open the .env file using a text editor.
3. Add the following lines to the .env file, replacing the placeholders with your actual API keys and access credentials:
`OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
`
4. Save the .env file.

Make sure not to share your .env file or expose your API keys and access credentials publicly. It's best to add .env to your .gitignore file to prevent it from being committed to version control systems like Git.

## Running the Application ##

### Frontend (React) ###

1. Navigate to the project directory in your terminal.
2. Run `npm start` to start the development server for the React frontend.
3. Access the frontend application at 'http://localhost:3000' in your web browser.

### Backend (Python) ###

1. Navigate to the backend directory within the project in your terminal.
2. Run `uvicorn server:app --reload` to start the backend server using Uvicorn with automatic reloading enabled.
3. The backend server will be running at `http://localhost:8000`.

## Additional Information ##

** Make sure both the frontend and backend servers are running simultaneously for the full functionality of the application.
** Feel free to explore and modify the codebase as per your requirements.

