import os
from flask import render_template, Flask, request
from werkzeug.contrib.atom import AtomFeed
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


@app.route("/blog/<path:path>/")
def post(path):
    post = blog.get_post_or_404(path)
    return render_template('post.html', post=post)


@app.route('/feed.atom/')
def feed():
    feed = AtomFeed(
        'Recent Articles', feed_url=request.url, url=request.url_root)
    posts = blog.posts
    title = lambda p: "{}: {}".format(p.title, p.subtitle) if hasattr(p, 'subtitle') else p.title
    for post in posts:
        feed.add(
            title(post),
            bytes(post.html, "utf-8"),
            content_type='html',
            author='AMCorvi',
            url=post.url(_external=True),
            updated=post.date,
            published=post.date)
    return feed.get_response()
