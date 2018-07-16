import sys

from flask_frozen import Freezer
from blog.generator import app, blog

freezer = Freezer(app)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        post_files = [post.filepath for post in blog.posts]
        app.run(port=8000, debug=True, extra_files=post_files)
