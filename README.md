# Student Management System

A full-featured web-based Student Management System built with Python (Flask), MySQL, and modern HTML/CSS.

## Features
- Add, update, search, and delete students
- Modern, responsive web interface
- Secure database credentials via `.env`
- MySQL backend with full schema
- Inline editing and validation
- Easy deployment instructions
## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Student-Management-System.git
   cd Student-Management-System
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with MySQL credentials and Flask secret key:
   ```
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=student_db
   FLASK_SECRET_KEY=your_secret_key
   ```
4. Create the database using `student_db.sql`.
5. Run the app:
   ```
   python app.py
   ```
6. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Security
- Do NOT upload your `.env` file to GitHub. Add `.env` to your `.gitignore`.

## License
MIT

