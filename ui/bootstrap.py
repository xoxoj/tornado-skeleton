import tornado.web
 
class BootstrapBase(tornado.web.UIModule):

    def javascript_files():
        return [
            "/static/js/jquery-2.1.0.min.js",
            "/static/js/bootstrap.min.js",
            "/static/js/underscore-min.js",
        ]
        
    def css_files():
        return [
            "/static/css/bootstrap.min.css"
        ]
        
    def render(self):
        return ''