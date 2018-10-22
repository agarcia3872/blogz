from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:stg!@#$%@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "agg!@#Rivera@usa)(*)"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(360))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.blogs = blogs
        # self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    encoded_username = request.args.get("username")
    encoded_password = request.args.get("password")
    encoded_error1 = request.args.get("error1")
    encoded_error2 = request.args.get("error2")
        
    users = User.query.all()
    return render_template('index.html', users=users, username=encoded_username, 
    password=encoded_password, error1=encoded_error1, error2=encoded_error2)

    # if request.method == 'POST':
    #     title = request.form['title']
    #     body = request.form['body']
    #     owner = User.query.filter_by(username=session['username']).first()
    #     new_blog = Blog(blog_title, blog_body, owner)
    #     db.session.add(new_blog)
    #     db.session.commit()

    

    # blogs = Blog.query.filter_by(completed=False).all()
    # completed_blogs = Blog.query.filter_by(completed=True,).all()

    # return render_template('newpost.html', username=encoded_username, 
    # password=encoded_password, error1=encoded_error1, error2=encoded_error2, 
    # title='Blogz', blogs=blogs, completed_blogs=completed_blogs,)


##############################################################

@app.route('/blog', methods=['POST', 'GET'])
def blog_listings():
    
    # if request.method == 'POST':
    #     title = request.form['title']
    #     body = request.form['body']
    #     newblog = Blog(title, body, owner)
    #     db.session.add(newblog)
    #     db.session.commit()

    # blogs = Blog.query.all()
    # return render_template('blog.html', blogs=blogs)
    

    if "user" in request.args:
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        user_blogs = Blog.query.filter_by(owner=user).all()
        return render_template("single-user.html", title = user.username + "'s Posts!", user_blogs=user_blogs)
    
    single_post = request.args.get("id")

    if single_post:
        blog = Blog.query.get(single_post)
        return render_template("single-entry.html", blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title ="All Blog Posts!", blogs=blogs)

    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    title_error = "Please fill in the title"
    body_error = "Please fill in the body"
        
    if request.method == 'POST':
        newBlog_title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        newblog = Blog(newBlog_title, body, owner)
        db.session.add(newblog)
        db.session.commit()

        # Stores the id of the post
        new_postId = str(newblog.id)
        
        blogs = Blog.query.all()
        blogs.append(newblog)

        if newBlog_title == "" or body == "":

             return render_template('newpost.html', newBlog_title=newBlog_title, body=body, title_error=title_error,
             body_error=body_error)

        #return redirect('/blog')

        #redirects to single-entry.html to show the post
        return redirect('/single_post/' + new_postId)

    return render_template('newpost.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if not user:
            username_error = "Username does not exist"
            return render_template('login.html', username_error=username_error)
        if user.password != password:
            password_error = "Wrong Password"
            return render_template('login.html', password_error=password_error)
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error1 = ""
    error2 = ""
    error3 = ""
    error4 = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_passwd = request.form['verify-passwd']

        if not username:
            error1 = "That's not a valid username"
            
        if not password or len(password) < 3 or len(password) > 20 or " " in password:
            error2 = "That's not a valid password"
            
        if not verify_passwd or verify_passwd == " " or password != verify_passwd:
            error3 = "Passwords do not match"
        
        if username == "" or password == "" or verify_passwd == "":
            return render_template('signup.html', username=username, error1=error1, error2=error2, error3=error3)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            error4 = "That username already exists"
            return render_template('signup.html', error4=error4)

        if not existing_user:
            new_user = User(username, password, verify_passwd)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        

    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
    
@app.route('/single_post/<int:id>', methods=['POST', 'GET'])
def single_post(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single-entry.html', blog=blog)



if __name__ == '__main__':
    app.run()
