import tornado.web

class Handler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # For security
        self.clear_header('Server')
    
    def get_current_user(self):
        # Overide parent class' method
        pass
        
    def write_error(self, status_code, **kwargs):
        import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k] ) for k in self.request.__dict__.keys()])
            error = exc_info[1]
            self.set_header('Content-Type', 'text/html')
            # No template, in case of failed
            self.finish(
                """<html><title>%s</title><body>
                <h2>Error</h2><p>%s</p>
                <h2>Traceback</h2><p>%s</p>
                <h2>Request Info</h2><p>%s</p>
                </body></html>""" % \
                (error, error, trace_info, request_info))
        else:
            super(Handler, self).write_error(status_code, **kwargs)
