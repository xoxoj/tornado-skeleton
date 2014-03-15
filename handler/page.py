from . import base

class View(base.Handler):
    def get(self, slug):
        self.render('page/article.html', name=slug)