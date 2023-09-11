from flask import *
import pymysql
# CRUD operation in flask
# C -> Inserting records to a database
# R -> Retrieve 

# start
app = Flask(__name__)

# home(/)
@app.route('/')
def home():
    return render_template('index.html')

# signup
@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        #step1: Get data from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']
        image = request.files['image']
        

        image.save('static/images/'+ image.filename)

        if password != confirm:
            return render_template('signup.html', error = 'Password Dont Match')
        else:
            connection = pymysql.connect(host='localhost',user='root',password='',database='MpesaTestDB')
            cursor = connection.cursor()

            sql = 'insert into registration (username,email,password,image) values(%s,%s,%s,%s)'
            data = (username,email,password,image.filename)
            cursor.execute(sql,data)
            connection.commit()
            return render_template('signup.html',success = 'Saved Successfully')
    else:
        return render_template('signup.html')


#Read data from the database: Login, display info......
@app.route('/display')
def display():
    connection = pymysql.connect(host='localhost',user='root',password='',database='MpesaTestDB')
    cursor = connection.cursor()
    sql = 'select * from registration '
    cursor.execute(sql)

    count = cursor.rowcount
    if count ==0:
        return render_template('display.html', message = 'No data available')
    else:
        data = cursor.fetchall()
        return render_template('display.html', records = data)

app.run(debug=True)
# end