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

    def __repr__(self):

        return '<Blog {0}>'.format(self.title)




@app.route('/')
def home_page():

    return redirect('/blog')




@app.route('/newpost', methods=['POST', 'GET'])
def index():
    
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



#@app.route('/posted', methods=['POST', 'GET'])
#def posted():
#    blog_title = request.args.get('title')
#    blog_body = request.args.get('body')#

#    return render_template('posted.html', title='BLOGADOCIOUS', blogbody = blog_body, blogtitle = blog_title)

@app.route('/blog', methods=['POST', 'GET'])
def mainblog():
    blog_id = request.args.get('id')
    if blog_id == None:
        entries = Blog.query.all()
        return render_template('blog.html', title='BLOGADOCIOUS!',entries=entries)
    else:
        entries = Blog.query.get(blog_id)
        return render_template('blog.html', title='BLOGADOCIOUS!', entries=entries)

    

    


if __name__ == '__main__':
    app.run()
