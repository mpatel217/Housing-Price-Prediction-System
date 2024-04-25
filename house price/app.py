from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
model = pickle.load(open('model.pkl', 'rb'))

historical_searches = []

@app.route('/')
def index():
    if 'username' in session and session['username'] == 'admin':
        return render_template('price.html', data=None, historical_searches=historical_searches, logged_in=True)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '12345678':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password. Please try again."
    return render_template('login.html', error=error)

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' in session and session['username'] == 'admin':
        val1 = request.form['bedrooms']
        val2 = request.form['bathrooms']
        val3 = request.form['floors']
        val4 = request.form['yr_built']
        arr = np.array([val1, val2, val3, val4])
        arr = arr.astype(np.float64)
        pred = model.predict([arr])

        historical_searches.append({
            'bedrooms': val1,
            'bathrooms': val2,
            'floors': val3,
            'yr_built': val4,
            'predicted_price': int(pred),
        })

        return render_template('price.html', data=int(pred), historical_searches=historical_searches, logged_in=True)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)