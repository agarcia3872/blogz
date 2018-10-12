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
    completed = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.completed = completed


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['newpost']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    posts = Blog.query.filter_by(completed=False).all()
    completed_blog = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs, completed_blogs=completed_blogs)


# @app.route('/new-post', methods=['POST'])
# def new_post():

#     blog_id = int(request.form['blog-id'])
#     blog = Blog.query.get(blog_id)
#     blog.completed = True
#     db.session.add(post)
#     db.session.commit()

#     return redirect('/')

# @app.route('/blog', methods=['POST'])
# def blog_listings():
    

#     if __name__ == "__main__":
#         app.run()