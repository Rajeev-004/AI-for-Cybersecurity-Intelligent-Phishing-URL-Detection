import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'unmyeong'

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            input_url TEXT NOT NULL,
            label TEXT NOT NULL,
            probability REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

import torch
import torch.nn as nn
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "model/cnn_rcnn_phishing.pt"
VOCAB_PATH = "model/char_vocab.pkl"
MAX_LEN = 200
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading model and vocabulary...")

char2idx = joblib.load(VOCAB_PATH)
PAD_IDX = 0
vocab_size = len(char2idx) + 1

class CNN_RCNN(nn.Module):
    def __init__(self, vocab_size, emb_dim=64, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=PAD_IDX)
        self.conv = nn.Conv1d(in_channels=emb_dim, out_channels=128, kernel_size=5, padding=2)
        self.relu = nn.ReLU()
        self.lstm = nn.LSTM(input_size=128, hidden_size=hidden_dim,
                            batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(hidden_dim * 2, 64)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.embedding(x)
        x = x.permute(0, 2, 1)
        x = self.relu(self.conv(x))
        x = x.permute(0, 2, 1)
        out, _ = self.lstm(x)
        out = torch.mean(out, dim=1)
        out = self.dropout(self.relu(self.fc1(out)))
        out = torch.sigmoid(self.fc2(out))
        return out.squeeze()

def preprocess_url(url, char2idx, max_len=MAX_LEN):
    seq = [char2idx.get(c, 0) for c in url[:max_len]]
    if len(seq) < max_len:
        seq += [0] * (max_len - len(seq))
    return np.array(seq, dtype=np.int64)

def predict_url(url, model):
    seq = preprocess_url(url, char2idx)
    X = torch.tensor(seq, dtype=torch.long).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        prob = model(X).item()
    label = "bad" if prob > 0.5 else "good"
    return label, prob

# Load model once
model = CNN_RCNN(vocab_size).to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()
print("Model loaded successfully!")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        conn = get_db_connection()
        user_check = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()

        if user_check:
            flash('Username or email already exists. Please choose a different one.', 'error')
            conn.close()
            return render_template('register.html')
        hashed_password = generate_password_hash(password)

        try:
            conn.execute(
                'INSERT INTO users (username, email, phone_number, password) VALUES (?, ?, ?, ?)',
                (username, email, phone_number, hashed_password)
            )
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('An error occurred during registration. Please try again.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'username' not in session:
        flash('Please log in to access the home page.', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute(
        'SELECT username, email, phone_number FROM users WHERE username = ?',
        (session['username'],)
    ).fetchone()
    conn.close()

    return render_template('home.html', user=user)

from flask import request, session, render_template, flash, redirect, url_for
from datetime import datetime

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        flash('You must be logged in to make predictions.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        input_url = request.form.get('url', '').strip()
        if not input_url:
            flash('Please enter a URL.', 'error')
            return render_template('predict.html')

        # Run model prediction
        label, prob = predict_url(input_url, model)

        # Retrieve current user
        conn = get_db_connection()
        user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()
        if not user:
            flash('User session invalid.', 'error')
            return redirect(url_for('login'))

        # Save to database
        conn.execute('INSERT INTO predictions (user_id, input_url, label, probability) VALUES (?, ?, ?, ?)',
                     (user['id'], input_url, label, prob))
        conn.commit()
        conn.close()

        flash(f'Prediction complete: {label.upper()} site (Confidence: {prob:.4f})', 'success')
        return render_template('predict.html', result={'url': input_url, 'label': label, 'prob': prob})

    return render_template('predict.html')


@app.route('/history')
def history():
    if 'username' not in session:
        flash('You must log in to view history.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()
    rows = conn.execute('SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC', (user['id'],)).fetchall()
    conn.close()
    return render_template('history.html', rows=rows)


@app.route('/analytics')
def analytics():
    if 'username' not in session:
        flash('You must log in to view analytics.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()

    # Count predictions grouped by label for this user
    rows = conn.execute('''
        SELECT label, COUNT(*) as count
        FROM predictions
        WHERE user_id = ?
        GROUP BY label
    ''', (user['id'],)).fetchall()
    conn.close()

    # Convert query results to a dict for easy access in template
    counts = {'good': 0, 'bad': 0}
    for row in rows:
        counts[row['label']] = row['count']

    return render_template('analytics.html', counts=counts)

@app.route('/datascience')
def datascience():
    return render_template('datascience.html')

@app.route('/exsisting')
def exsisting():
    return render_template('exsisting.html')

@app.route('/proposed')
def proposed():
    return render_template('proposed.html')

if __name__ == '__main__':
    app.run(debug=True)
