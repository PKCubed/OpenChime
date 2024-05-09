from flask import Flask
app = Flask(__name__)
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from werkzeug.security import generate_password_hash, check_password_hash

user = 'admin'
pw = 'test1234'
users = {
    user: generate_password_hash(pw)
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/hello')
@auth.login_required
def hello_world():
    return 'Hello, World!'
    
if __name__ == '__main__':
    print('Starting app')
    app.run(host='0.0.0.0', debug=True, port=8080)