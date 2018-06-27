import os

from flask import abort, url_for
from werkzeug import cached_property
from .sorted_dict import SortedDict
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
import yaml

MARKDOWN_EXTENSION = ".md"


class Blog(object):
    def __init__(self, app, root_dir='', file_ext=MARKDOWN_EXTENSION):
        self.root_dir = root_dir
        self.file_ext = file_ext
        self._app = app
        self._cache = SortedDict(key=lambda post: post.date, reverse=True)
        self._initialize_cache()

    @property
    def posts(self):
        return self._cache.values()

    def get_post_or_404(self, path):
        try:
            return self._cache[path]
        except KeyError:
            abort(404)

    def _initialize_cache(self):
        for (root, dirs, files) in os.walk(self.root_dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == self.file_ext:
                    filepath = os.path.join(root, file).replace(
                        self.root_dir, "")
                    post = Post(filepath, root_dir=self.root_dir)
                    self._cache[post.urlpath] = post


class Post(object):
    def __init__(self, path, root_dir=""):
        self.urlpath = os.path.splitext(path.strip('/'))[0]
        self.filepath = os.path.join(root_dir, path.strip('/'))
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.filepath, "r") as fin:
            content = fin.read().split("\n\n", 1)[1].strip()
        return markdown.markdown(content, extensions=[FencedCodeExtension()])

    def _initialize_metadata(self):
        content = ""
        with open(self.filepath, "r") as fin:
            for line in fin:
                if not line.strip():
                    break
                content += line
        self.__dict__.update(yaml.load(content))

    def url(self, _external = False):
        return url_for("post", path=self.urlpath, _external=_external)
