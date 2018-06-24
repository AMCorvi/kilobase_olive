from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/blog/post")
def post():
    return render_template('post.html', post_content="Hola Mundo! (de templato)" )


if __name__ == "__main__":
    app.run(port=8000)
