from flask import Flask, session, request, jsonify, request, render_template, redirect, url_for, Response, make_response
from jinja2 import Template
import subprocess
import jwt
import datetime
import mysql.connector
from functools import wraps
import secrets
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os

os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'  # Adjust the PATH as needed





app = Flask(__name__)
app.config['SECRET_KEY'] = 'shiv'

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ztech@44',
    database='db'
)
cursor = db_connection.cursor()


#token check function
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated




@app.route('/')
def home():
    return render_template('login.html')
    # return render_template('provision.html')



# Generate a 64-character hex token
def generate_api_key():
    return secrets.token_hex(32)  

    

#login token
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
    user = cursor.fetchall()
    if user and user[0][2] == password:
        session['username'] = username

        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')

        response = make_response(render_template('provision.html'))
        response.set_cookie('token', token, httponly=True, path='/')  
        return response
    else:
        error_message = 'Login failed Try Again'
        return render_template('login.html', error_message=error_message)
    


    
@app.route('/adp', methods=['POST'])
def adp():
    service = request.form['service']
    ip = request.form['ip'].split(',') 
    password = request.form['password']
    user = request.form['user']
    script_dir = os.path.dirname(__file__)
    aitj2=os.path.join(script_dir,'ait.j2')
    with open(aitj2, 'r') as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    generated_text = template.render(
        ip=ip,
        user=user,
        password=password
    ).strip()

    aifini=os.path.join(script_dir,'tt/aif.ini')
    with open(aifini, 'w') as f:
        f.write(generated_text)
    lyaml=os.path.join(script_dir,'lamp.yml')
    dyaml=os.path.join(script_dir,'devops.yml')
    cyaml=os.path.join(script_dir,'cyber.yml')
    byaml=os.path.join(script_dir,'basic.yml')
    if service == 'LAMP':
        command = f'ansible-playbook -i  "{aifini}" "{byaml}"'
    elif service == 'DevOps':
        command = f'ansible-playbook -i  "{aifini}" "{byaml}"'
    elif service == 'Cyber':
        command = f'ansible-playbook -i  "{aifini}" "{byaml}"'
    elif service == 'Basic':
        command = f'ansible-playbook -i  "{aifini}" "{byaml}"'
    else:
        return 'Invalid service selection'


    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        command_output = result.stdout

        if result.returncode == 0:
            result_message = 'Success'
        else:
            result_message = 'Failed'
    except Exception as e:
        command_output = str(e)
        result_message = 'Failed'

    return f'Command Output: {command_output}<br>Command Result: {result_message}'
  














if __name__ == "__main__":
	app.run()
