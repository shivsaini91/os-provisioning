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
        # token = request.args.get('token')

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

#api key decorator
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.cookies.get('token')
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         cursor = db_connection.cursor()
#         cursor.execute('SELECT api_key FROM login WHERE api_key = %s', (token,))
#         api_key_match = cursor.fetchone()

#         if not api_key_match:
#             return jsonify({'message': 'Invalid token!'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired!'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Invalid token!'}), 401

#         return f(*args, **kwargs)

#     return decorated



@app.route('/')
def home():
    return render_template('login.html')
    # return render_template('provision.html')



# Generate a 64-character hex token
def generate_api_key():
    return secrets.token_hex(32)  


#api key token
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     cursor = db_connection.cursor()
#     cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
#     user = cursor.fetchone()
#     # return jsonify(user)

#     if not user:
#         # User doesn't exist, insert new user logic
#         hashed_password = generate_password_hash(password)
#         api_key = generate_api_key()
#         cursor.execute('INSERT INTO login (username, password, api_key) VALUES (%s, %s, %s)', (username, hashed_password, api_key))
#         db_connection.commit()
#         # cursor.fetchall()  # Consume the unread result from the previous query
#         cursor.close()
        
#         token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
#         response = make_response(jsonify({'message': 'Login successful New................'}))
#         response.set_cookie('token', token, httponly=True)  # Store token in an HTTP-only cookie
        
#         return response
#     else:
#         # User exists, check password logic
#         if check_password_hash(user[2], password):
#             session['username'] = username            
#             if user[3] is None:
#                 # User has no API key, generate and update API key
#                 api_key = generate_api_key()
#                 app.logger.info("Generated API key: %s", api_key)
#                 cursor.execute('UPDATE login SET api_key = %s WHERE username = %s', (api_key, username))
#                 db_connection.commit()  
#                 cursor.close()            
#                 return jsonify({'message': 'Login successful ********************** exist', 'api_key': api_key})            
#             else:
#                 api_key = user[3]  # Use the existing API key     

#             cursor.close()            
#             return render_template('provision.html')

#         else:
#             cursor.close()            
#             error_message = 'Login failed Try Again'
#             return render_template('login.html', error_message=error_message)
        

    

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
        # session['username'] = token
#       return redirect(url_for('gen')) # or
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        # return jsonify({'token': token})
        response = make_response(jsonify({'message': 'Login successful'}))
        response.set_cookie('token', token, httponly=True)  # Store token in an HTTP-only cookie
        return render_template('provision.html')
    else:
        error_message = 'Login failed Try Again'
        return render_template('login.html', error_message=error_message)
    


    
# ansible data processing
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

    # Save the generated text to a file
    aifini=os.path.join(script_dir,'tt/aif.ini')
    with open(aifini, 'w') as f:
        f.write(generated_text)
    lyaml=os.path.join(script_dir,'lamp.yml')
    dyaml=os.path.join(script_dir,'devops.yml')
    cyaml=os.path.join(script_dir,'cyber.yml')
    byaml=os.path.join(script_dir,'basic.yml')
    # Execute Linux command based on selected service
    if service == 'LAMP':
        command = f'ansible-playbook -i  aifini "{lyaml}"'
        # command = 'ls'
    elif service == 'DevOps':
        command = f'ansible-playbook -i  aifini "{dyaml}"'
    elif service == 'Cyber':
        command = f'ansible-playbook -i  aifini "{cyaml}"'
    elif service == 'Basic':
        command = f'ansible-playbook -i  aifini "{byaml}"'
    else:
        return 'Invalid service selection'

    # Run the command using subprocess
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        command_output = result.stdout
        # result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        # # return f"<pre>{result.decode('utf-8')}</pre>"
        if result.returncode == 0:
            result_message = 'Success'
        else:
            result_message = 'Failed'
    except Exception as e:
        command_output = str(e)
        result_message = 'Failed'
    # return f"<pre>{result.decode('utf-8')}</pre>"
    return f'Command Output: {command_output}<br>Command Result: {result_message}'
  





@app.route('/users', methods=['GET'])
@token_required
# token = request.cookies.get('token')
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    # return jsonify(users)
    return users

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
    db_connection.commit()

    return jsonify({'message': 'User added successfully'})


@app.route('/cmd')
# @token_required
def index():
    return render_template('index.html')

@app.route('/scmd')
def index2():
    return render_template('sindex.html')




@app.route('/runcmd', methods=['POST'])
def run_command():
    try:
        command = request.form.get('command')
        if command:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return f"<pre>{result.decode('utf-8')}</pre>"
        else:
            return "No command provided."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/sudo', methods=['POST'])
def run_command2():
    try:
        command = request.form.get('command')
        password = request.form.get('password')

        if command and password:
            sudo_cmd = f"echo {password} | sudo -S {command}"
            result = subprocess.check_output(sudo_cmd, shell=True, stderr=subprocess.STDOUT)
            return f"<pre>{result.decode('utf-8')}</pre>"
        else:
            return "No command or password provided."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"An error occurred: {str(e)}"





@app.route('/generate', methods=['POST'])
def generate_text_file():
    name = request.form.get('name')
    age = request.form.get('age')

    with open('/home/shiv/api/i.j2', 'r') as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    generated_text = template.render(
        name=name,
        age=age
    )

    # Save the generated text to a file
    with open('/home/shiv/api/tt/generated_text.txt', 'w') as f:
        f.write(generated_text)

    return f'Text file generated: <a href="/download">Download</a>'

@app.route('/gen')
def gen():
    return render_template('j.html')






if __name__ == "__main__":
	app.run()
