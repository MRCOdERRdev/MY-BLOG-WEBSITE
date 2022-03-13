from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body=CKEditorField("Body Content",validators=[DataRequired()])

    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    blog=BlogPost.query.all()
    return render_template("index.html", all_posts=blog)

@app.route('/edit-post/<post_id>',methods=["GET","POST"])
def edit_post(post_id):
    blog_details=BlogPost.query.filter_by(id=post_id).first()
    title=blog_details.title
    author=blog_details.author
    subtitle=blog_details.subtitle
    img_url=blog_details.img_url
    date=blog_details.date
    form=CreatePostForm(title=title,author=author,subtitle=subtitle,img_url=img_url)
    if(request.method=="POST"):
            blog=BlogPost.query.filter_by(id=int(post_id)).first()
            blog.title=request.form.get('title')
            blog.subtitle=request.form.get('subtitle')
            blog.author=request.form.get('author')
            blog.img_url=request.form.get('img_url')
            blog.date=date
            blog.body=request.form.get('body')
            db.session.commit()
            return redirect('/')

    return render_template('make-post.html',form=form,prop="Edit")
    
@app.route('/delete/<int:index>')
def delete_post(index):
    blog=BlogPost.query.filter_by(id=index).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect('/')


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.filter_by(id=index).first()
   
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/new-post',methods=['GET','POST'])
def new_post():
    form=CreatePostForm()

    if(request.method=="POST"):
        title=request.form.get('title')
        subtitle=request.form.get('subtitle')
        author=request.form.get('author')
        img_url=request.form.get('img_url')
        today=datetime.now()
        date=today.strftime('%B')+today.strftime('%d')+','+today.strftime('%Y')
        date_today=date
        body=request.form.get('body')
        blog=BlogPost(title=title,subtitle=subtitle,author=author,img_url=img_url,date=date_today,body=body)
        db.session.add(blog)
        db.session.commit()
        return redirect('/')


    return render_template('make-post.html',form=form,prop="New")
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False,port=5000)
    # app.run(debug=True)