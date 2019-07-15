from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = '?/>qb7T;Fe:RYMae'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body ):
        self.title = title
        self.completed = False
        self.body = body









@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']

        if blog_name == '':
            flash('Oops! Your entry needs a title.', 'error')
            return render_template('newpost.html', title='BLOGADOCIOUS!', blogbody=blog_body)
        elif blog_body == '':
            flash('This field cannot be empty. Please enter some text into your blog.', 'error')
            return render_template('newpost.html', title='BLOGADOCIOUS!', blogname=blog_name)

        new_blog = Blog(blog_name, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('newpost.html', title="BLOGADOCIOUS!") 

    entries = Blog.query.all()

@app.route('/blog', methods=['POST', 'GET'])
def posted():
    entries = Blog.query.all()

    return render_template('blog.html', title='BLOGADOCIOUS!',entries=entries)

    


if __name__ == '__main__':
    app.run()
