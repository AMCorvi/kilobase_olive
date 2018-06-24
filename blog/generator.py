from flask import Flask, render_template
from werkzeug import cached_property
import os
import markdown

MARKDOWN_EXTENSION = ".md"
app = Flask(__name__)


class Post(object):
    def __init__(self, path):
        self.path = path

    @cached_property
    def html(self):
        with open(self.path, "r") as fin:
            content = fin.read().strip()
        return markdown.markdown(content)


@app.route("/")
def index():
    return "Hello World"


@app.route("/blog/<path:path>")
def post(path):
    path = os.path.join("posts", path + MARKDOWN_EXTENSION)
    post_content = Post(path)
    return render_template('post.html', post=post_content)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
