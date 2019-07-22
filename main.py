from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = '?/>qb7T;Fe:RYMae'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body ):
        self.title = title
        self.completed = False
        self.body = body
        self.owner = owner


    def __repr__(self):

        return '<Blog {0}>'.format(self.title)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

        if blog_title == '':
            flash('Oops! Your entry needs a title.', 'error')
            return render_template('newpost.html', title='BLOGADOCIOUS!')
        elif blog_body == '':
            flash('Hold on a sec! Please enter some text into your blog.', 'error')
            return render_template('newpost.html', title='BLOGADOCIOUS!')
        
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('/posted.html', title='BLOGADOCIOUS', blog_title=blog_title, blog_body=blog_body)
    else:
        return render_template('newpost.html', title="BLOGADOCIOUS!") 


@app.route('/blog', methods=['POST', 'GET'])
def mainblog():
    

    blog_id = request.args.get('id')
    if blog_id == None:
        entries = Blog.query.all()
        return render_template('blog.html', title='BLOGADOCIOUS!',entries=entries)
    else:
        single = Blog.query.get(blog_id)
        blog_title = single.title
        blog_body = single.body

        return render_template('posted.html', title='BLOGADOCIOUS!',blog_title=blog_title, blog_body=blog_body)
        
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
       
        #TODO - validate user data
        if username == '':
            flash('Whoa there! An username is required to enter Blogz.', 'error')
            return render_template('signup.html', title='BLOGADOCIOUS!')
        elif password == '':
            flash('Uh oh! There needs to be a password.', 'error')
            return render_template('signup.html', title='BLOGADOCIOUS!')
        elif password != verify:
            flash('Password and verification must match.', 'error')
            return render_template('signup.html', title='BLOGADOCIOUS!')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Sorry! That username already exists.')
        
    return render_template('signup.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/newpost')
        else:
            flash("User password incorrect, or user does not exist", 'error')

    return render_template('login.html')


@app.route('/index')



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


    

    


if __name__ == '__main__':
    app.run()
