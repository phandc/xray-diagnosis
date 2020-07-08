
from flask import Flask,send_from_directory,render_template, redirect, request,url_for, session
from package.model import conn
from admin import admin1
from doctor import doctor1
# import json
#
#
# with open('config.json') as data_file:
#     config = json.load(data_file)






app = Flask(__name__)
app.secret_key = "duyennguyen"

app.register_blueprint(admin1, url_prefix="/admin")

app.register_blueprint(doctor1, url_prefix="/doctor")






# Routes
@app.route('/login', methods=["GET", "POST"])
def login():
   if request.method == "POST":
       username = request.form['username']
       password = request.form['password']

       #user = conn.execute("SELECT * FROM user WHERE username=?", (username,)).fetchall()

       user = conn.execute("SELECT u.*,r.* from user u LEFT JOIN role r ON u.user_id = r.role_id WHERE u.username=?", (username, )).fetchall()
       print(user[0]['username'] + " " + username)
       print(password + user[0]['password'])
       print(user)
       if username == user[0]['username'] and password == user[0]['password']:
           if user[0]['role'] == 'admin':
              session['user'] = username
              return  redirect(url_for("admin.admin"))
           else:
               session['user'] = username
               return redirect(url_for("doctor.doctor"))
       else:
           return redirect(url_for("login"))

   return  render_template("login.html")



@app.route('/')
def index():
    return render_template('admin/index.html')

@app.route('/index')
def index1():
    return render_template('admin/index_test.html')


# @app.route('/doctorpage')
# def doctor_page():
#     return app.send_static_file('doctor/doctor.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)