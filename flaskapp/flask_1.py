from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from forms import MusicSearchForm

app = Flask(__name__)

#Config Mysql
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 's16012000'
app.config['MYSQL_DB']= 'flaskapp'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'
#INitialize Mysql

mysql= MySQL(app)

Articles= Articles()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/articles')
def articles():
    return render_template("articles.html",articles=Articles)


@app.route('/article/<string:id>')
def article(id):
    return render_template("article.html",id=id)

class RegisterForm(Form):
	name = StringField('Name',[validators.Length(min=1, max=50)])
	username = StringField('Username',[validators.Length(min=4, max=25)])
	email = StringField('Email',[validators.Length(min=6, max=50)])
	password=PasswordField('Password',[
			validators.DataRequired()
			])

#search function begins

#search function ends



@app.route('/register',methods=['GET','POST'])
def register():
	form =RegisterForm(request.form)
	if request.method=='POST' and form.validate():
		name= form.name.data
		username= form.username.data
		email=form.email.data
		password=sha256_crypt.encrypt(str(form.password.data))

		#Create Cursor
		cur= mysql.connection.cursor()

		#Execution
		cur.execute("INSERT INTO users(name,username,email,password) VALUES(%s,%s,%s,%s)", (name,username,email,password))

		#Commit to DB

		mysql.connection.commit()

		#close connection

		cur.close()

		flash('Registered Successfully', 'success')
		redirect(url_for('index'))

		return render_template("register.html",form= form)

	return render_template("register.html",form=form)

if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)