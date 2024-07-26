from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, abort, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import os
import json
import re
from flask_cors import CORS
from filelock import FileLock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
NUM_PAGES = 3  # Configurable number of pages

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app)

# Load user data from CSV
def load_user_data(csv_file):
    try:
        df = pd.read_csv(csv_file)
        users = {}
        for index, row in df.iterrows():
            user_id = str(row['username']).strip()
            password = str(row['password']).strip()
            users[user_id] = password
        return users
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

users = load_user_data('user_credentials.csv')

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Attempting login with username: {username} and password: {password}")
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('protected'))
        else:
            flash('Login failed. Please check your username and password and try again.', 'danger')
    return render_template('login.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

@app.route('/midterm')
@login_required
def midterm():
    user_id = current_user.id
    user_folder = os.path.join(os.getcwd(), 'answer_sheet_scans', user_id)
    if not os.path.exists(user_folder):
        flash(f"No folder found for user {user_id}.", 'danger')
        return redirect(url_for('protected'))

    grades_file = os.path.join(os.getcwd(), 'grades.json')
    if os.path.exists(grades_file):
        with open(grades_file, 'r') as f:
            grades = json.load(f)
    else:
        grades = {}

    images = []
    total_score = 0
    for filename in sorted(os.listdir(user_folder), key=lambda x: int(x.split('.')[0])):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            page_number = filename.split('.')[0]
            score = grades.get(user_id, {}).get(page_number, 'N/A')
            images.append((filename, score))
            if score != 'N/A':
                total_score += int(score)

    return render_template('midterm.html', user_id=user_id, images=images, total_score=total_score)

@app.route('/uploads/<user_id>/<filename>')
@login_required
def uploaded_file(user_id, filename):
    if user_id != current_user.id and current_user.id != 'TA_CS230':
        abort(403)  # Forbidden access

    return send_from_directory(os.path.join(os.getcwd(), 'answer_sheet_scans', user_id), filename)

@app.route('/final')
@login_required
def final():
    return "This is the Final page."

@app.route('/grading')
@login_required
def grading():
    if current_user.id != 'TA_CS230':
        abort(403)
    return render_template('grading.html', num_pages=NUM_PAGES)

@app.route('/grading/page/<int:page_number>')
@login_required
def grading_page(page_number):
    if current_user.id != 'TA_CS230':
        abort(403)

    grades_file = os.path.join(os.getcwd(), 'grades.json')
    if os.path.exists(grades_file):
        with open(grades_file, 'r') as f:
            grades = json.load(f)
    else:
        grades = {}

    scans_dir = os.path.join(os.getcwd(), 'answer_sheet_scans')
    students = [d for d in os.listdir(scans_dir) if os.path.isdir(os.path.join(scans_dir, d)) and re.fullmatch(r'\d+', d)]
    student_images = [(student, os.path.join(scans_dir, student, f'{page_number}.png'), grades.get(student, {}).get(str(page_number), '')) for student in students]
    
    return render_template('grading_page.html', page_number=page_number, student_images=student_images)

@app.route('/save_grade', methods=['POST'])
@login_required
def save_grade():
    if current_user.id != 'TA_CS230':
        abort(403)

    student_id = request.form['student_id']
    page_number = request.form['page_number']
    grade = request.form['grade']

    grades_file = os.path.join(os.getcwd(), 'grades.json')
    lock_file = grades_file + '.lock'

    # Lock the file to prevent concurrent writes
    with FileLock(lock_file):
        if os.path.exists(grades_file):
            with open(grades_file, 'r') as f:
                grades = json.load(f)
        else:
            grades = {}

        if student_id not in grades:
            grades[student_id] = {}
        grades[student_id][page_number] = grade

        with open(grades_file, 'w') as f:
            json.dump(grades, f, indent=4)

    return jsonify({'message': f'Grade saved for student {student_id}, page {page_number}.'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

