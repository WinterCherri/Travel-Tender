from flask import Flask, render_template, request, redirect, make_response
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(host="sql9.freesqldatabase.com",user="sql9595338",password="xJMeStuNuM",database="sql9595338")

cursor = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/planatrip')
def plan_a_trip():
    return render_template("planatrip.html")

@app.route("/logged_in_success")
def logged_in_success():
    return render_template("logged_in_success.html")

@app.route("/collections")
def collections():
    return render_template("collections.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")



@app.route('/login_validation', methods = ['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users=cursor.fetchall()
    print(users[0][0])
    
    if len(users)>0:
        return redirect('/logged_in_success')
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    return "User registered successfully {} {} {}".format(name,email,password)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        email = request.form['email']
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('email', email)
    return resp 

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('email')
    return '<h1>welcome ' + str(name) + '</h1>'

'''@app.route("/delete_cookie")
def delete_cookie():
    if request.method == 'POST':
        email = request.form['email']
        resp = make_response("Cookie deleted")
        resp.delete_cookie("email", email)
        return resp'''


#------------adding tags-------------
@app.route('/add_tags', methods=['POST'])
def add_tags():
    
    country=request.form.get('country')
    month=request.form.get('month')
    year=request.form.get('year')
    first_choice=request.form.get('first_choice')
    second_choice=request.form.get('second_choice')
    third_choice=request.form.get('third_choice')
    email = request.cookies.get('email')

    cursor.execute("UPDATE `users` SET `country`='{}',`month`='{}', `year`='{}', `first_choice`='{}', `second_choice`='{}', `third_choice`='{}'  WHERE `email`='{}'".format(country,month,year,first_choice,second_choice,third_choice,email))
    conn.commit()
    return "User registered successfully {} {} {} {} {} {} {}".format(country,month,year,first_choice,second_choice,third_choice,email)


if __name__=="__main__":
    app.run(debug=True)