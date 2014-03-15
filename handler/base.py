import tornado.web

class Handler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # For security
        self.clear_header('Server')
