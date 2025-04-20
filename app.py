from flask import Flask, render_template, request, redirect
import random
import string
import json
import os

app = Flask(__name__, template_folder='templates')
PASSWORD_FILE = "./file/passwords.json"

# Load saved passwords
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        try:
            with open(PASSWORD_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

# Save passwords to file
def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_password = ""
    saved_passwords = {}
    show_passwords = False

    if request.method == 'POST':
        action = request.form.get('action')
        app_name = request.form.get('app_name', '').strip()

        if action == 'Generate Password':
            length = 12
            characters = string.ascii_letters + string.digits + string.punctuation
            generated_password = ''.join(random.choice(characters) for _ in range(length))

            if app_name:
                passwords = load_passwords()
                passwords[app_name] = generated_password
                save_passwords(passwords)
        elif action == 'Show Passwords':
            saved_passwords = load_passwords()
            show_passwords = True

    return render_template("index.html", generated_password=generated_password,
                           show_passwords=show_passwords, saved_passwords=saved_passwords)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
