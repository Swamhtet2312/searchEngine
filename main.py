from flask import Flask, render_template, request, session, redirect, url_for
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "2312"

@app.route('/')
def home():
    return render_template(
        'index.html',
        userName=session.get('userName'),
        userEmail=session.get('userEmail'),
        account=session.get('userAccount', False)
    )

@app.route('/submit', methods=['GET', 'POST'])
def search():
    user_input = request.form.get('query') if request.method == 'POST' else request.args.get('query')

    from serpapi import GoogleSearch

    normalSearch = {
        "engine": "google",
        "q": user_input,
        "api_key": "e7fc3656a8e82b062a50c7e63f54c74531e9b7e3bb759d24bb28b04eddf1395a"
    }

    imageSearch = {
        "engine": "google_images",
        "q": user_input,
        "api_key": "e7fc3656a8e82b062a50c7e63f54c74531e9b7e3bb759d24bb28b04eddf1395a"
    }

    search = GoogleSearch(normalSearch)
    image_search = GoogleSearch(imageSearch)

    results = search.get_dict()
    image_results = image_search.get_dict()

    search_status = results.get("search_metadata", {}).get("status")
    image_status = image_results.get("search_metadata", {}).get("status")

    if search_status == "Success" and image_status == "Success":
        search_results = results.get("organic_results", [])
        image_data = image_results.get("images_results", [])
        return render_template(
            'search.html',
            results=search_results,
            imageResults=image_data,
            query=user_input,
            userName=session.get('userName'),
            userEmail=session.get('userEmail'),
            account=session.get('userAccount', False)
        )
    else:
        return render_template('error.html', results=results)



    # url = "https://real-time-web-search.p.rapidapi.com/search"
    # querystring = {"q": f"{user_input}", "limit": "16"}
    # headers = {
    #     "x-rapidapi-key": "9e2e2c8a80msh11dab44ed2e4748p1fd328jsnd2bb3c55a8a4",
    #     "x-rapidapi-host": "real-time-web-search.p.rapidapi.com"
    # }

    # response = requests.get(url, headers=headers, params=querystring)
    # response_data = response.json()

    # if response_data.get("status") == "OK":
    #     result = response_data.get('data', [])
    #     return render_template('search.html', 
    #                            results=result, 
    #                            query=user_input, 
    #                            userName=session.get('userName'),
    #                            userEmail=session.get('userEmail'),
    #                            account=session.get('userAccount', False))
    # else:
    #     result = response_data.get('data', [])
    #     return render_template('error.html', results=result)

# Database management
file = 'users.json'

def load_users():
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(file, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()

        # Check if user exists
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['userAccount'] = True
                session['userName'] = user['username']
                session['userEmail'] = user['email']
                return redirect(url_for('home'))

        return render_template('login.html', error="Invalid credentials, please try again.")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        email = request.form.get('email')

        if not email:
            return render_template('signup.html', error="Email is required.")

        # Check if email exists
        for user in users:
            if user['email'] == email:
                return render_template('signup.html', error="Email already exists.")

        username = request.form.get('username')
        password = request.form.get('password')

        users.append({
            'username': username,
            'email': email,
            'password': password
        })

        save_users(users)

        # Save user session data
        session['userAccount'] = True
        session['userName'] = username
        session['userEmail'] = email

        return render_template('signup.html', success="Account created successfully.")

    return render_template('signup.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        users = load_users()
        email = request.form.get('email')

        if not email:
            return render_template('account.html', error="Email is required.")

        # Check if email exists
        for user in users:
            if user['email'] == email:
                return render_template('account.html', error="Email already exists.")

        username = request.form.get('username')
        password = request.form.get('password')

        users.append({
            'username': username,
            'email': email,
            'password': password
        })

        save_users(users)

        # Save user session data
        session['userAccount'] = True
        session['userName'] = username
        session['userEmail'] = email

        return render_template('account.html', success="Account created successfully.")

    return render_template('account.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
