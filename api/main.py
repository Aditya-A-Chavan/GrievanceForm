import re
from flask import Flask, request, session, render_template, send_file, redirect, url_for
import random
from functools import wraps

app = Flask(__name__)

app.secret_key = 'your_secret_key'

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_contact_number(contact):
    pattern = r'^\d{10}$'
    return re.match(pattern, contact)

def validating_Id_number(id_number):
    pattern = r'\d'
    return re.match(pattern, id_number)

def validating_roll_number(roll_number):
    pattern = r'\d'
    return re.match(pattern, roll_number)



@app.route('/', methods=['GET', 'POST'])
def form():
    error_message = None

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        id_number = request.form['id_number']
        class_div = request.form['class_div']
        roll_number = request.form['roll_number']
        grievance = request.form['grievance']

        if not validate_email(email):
            error_message = 'Please enter email in correct format'

        if not validate_contact_number(contact):
            error_message = 'Please enter Contact number in correct format'


        if not validating_Id_number(id_number):
            error_message = 'Please enter Id Number in correct format'

        if not validating_roll_number(roll_number):
            error_message = 'Please enter Roll number in correct format'
        
        if error_message:
            return render_template('error.html', Error=error_message)
        
        
        ticket_number = random.randint(1000, 9999)
       

       
        form_data = f"Name: {name}\nContact Number: {contact}\nEmail ID: {email}\nID Number: {id_number}\nRoll Number: {roll_number}\nClass & Division: {class_div}\nGrievance: {grievance}"

        
        with open("ticket_data.txt", "a") as file:
            file.write(f"{ticket_number}\n{form_data}\n\n")

        return render_template('ticket.html', ticket_number=ticket_number)

    return render_template('form.html', error_message=error_message)


#login Sequences below is "assssss" follows

admin_username = "admin"
admin_password = "admin"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin-login.html', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return render_template('download-ticket-data.html')
        
        #now this, this took me around 2 hrs to do. first html wouldnt echo the username and password back to python and when it started to 
#echo, pythons script for rendering download-ticket-data.html just wouldn't work ffs
#now finally all this is working and i am gonna work on putting login sessions in this
        
        else:
            error_message = "Wrond Credentials \n Invalid Username or Password"
            return render_template('error.html', Error = error_message)
        
        
    return render_template('admin-login.html', error = False)

@app.route ('/download-ticket-data', methods=['GET', 'POST'])
@login_required
def download_ticket_data():
    return send_file('\ticket_data.txt', as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

#reading login sesssions documentation and understanding them took me 2 hrs
#implementing it took me 30 sweet minutes <3 <3
#i hope i dont forget to remove these comments before showing it to sir
#just in case i forget: Sir sorry i was bored. please ignore these


if __name__ == '__main__':
    app.run(debug=False)