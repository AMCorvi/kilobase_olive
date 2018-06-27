import os
from flask import render_template, Flask
from .utils.blog import Blog

MARKDOWN_EXTENSION = ".md"
POST_DIR = os.path.join("blog", "posts")

app = Flask(__name__)
blog = Blog(app, root_dir=os.path.relpath(POST_DIR))



@app.template_filter("date")
def format_date(value, format="%B %d, %Y"):
    return value.strftime(format)


@app.route("/")
def index():
    return render_template("index.html", posts=blog.posts)


@app.route("/blog/<path:path>")
def post(path):
    post = blog.get_post_or_404(path)
    return render_template('post.html', post=post)
