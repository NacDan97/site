from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin 
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/daniel/Documents/pypro/daniel_site/blog.db'
app.config['SECRET_KEY'] = 'Notecard97!'
# login_manager = LoginManager()
# login_manager.init_app(app)

db = SQLAlchemy(app)

class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(20), default = "title")
	subtitle = db.Column(db.String(50))
	body = db.Column(db.Text)
	date_posted = db.Column(db.DateTime)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog/')
def blog():
	posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
	return render_template('blog.html', posts = posts)

@app.route('/manage/')
def manage():
	return render_template('manage.html')

@app.route('/addpost/', methods=['POST'])
def add_post():
	title = request.form['title']
	subtitle = request.form['subtitle']
	body = request.form['body']

	return '<h1>Title: {} Subtitle: {} Body: {}</h1>'.format(title, subtitle, body)
	# title = request.form['title']
	# subtitle = request.form['subtitle']
	# body = request.form['body']

	# post = BlogPost(title = title, subtitle = subtitle, body = body)

	# db.session.add(post)
	# db.session.commit()

	# return redirect(url_for('blog'))

	# try:
	# 	title = request.form['title']
	# 	subtitle = request.form['subtitle']
	# 	body = request.form['body']
	# 	post = BlogPost(title = title, subtitle = subtitle, body = body, date_posted = datetime.now())
	# 	db.session.add(post)
	# 	db.session.commit()

	# 	return(redirect(url_for('blog')))

	# except Exception as e:
	# 	flash(e)
	# 	return redirect(url_for('manage'))

@app.route('/post/<int:post_id>')
def post(post_id):
	post = BlogPost.query.filter_by(id = post_id).one()
	return render_template('post.html', post = post)

@app.route('/login/', methods=["GET", "POST"])
def login():
	# user = 'Daniel'
	error = ''
	try:
		if request.method == "POST":
			attempted_password = request.form['password']

			flash(attempted_password)

			if attempted_password == app.config['SECRET_KEY']:
				# login_user(user)
				return redirect(url_for('manage'))
			else:
				flash("Password incorrect")

		return render_template('login.html', error = error)

	except Exception as e:
		flash(e)
		return render_template('login.html', error = error)


