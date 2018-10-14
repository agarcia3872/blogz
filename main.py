from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:stg!@#$%@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(360))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        # new_title = Blog(blog_title)
        body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        # db.session.add(blog_body)
        db.session.commit()
        
    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()

    return render_template('newpost.html', title='Build a Blog', blogs=blogs, completed_blogs=completed_blogs)

@app.route('/blog', methods=['POST', 'GET'])
def blog_listings():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newblog = Blog(title, body)
        db.session.add(newblog)
        db.session.commit()
    
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newblog = Blog(title, body)
        db.session.add(newblog)
        db.session.commit()

        blogs = Blog.query.all()
        blogs.append(newblog)
        

    return render_template('newpost.html')

    
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/blog/<int:id>')
def single_post(id=None):
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single-entry.html', blog=blog)



if __name__ == '__main__':
    app.run()