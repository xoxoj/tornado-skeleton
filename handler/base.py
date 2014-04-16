import tornado.web

class Handler(tornado.web.RequestHandler):

    def initialize(self):
        # Instance database
        
    def set_default_headers(self):
        # For security
        self.clear_header('Server')
    
    def get_current_user(self):
        # Overide parent class' method
        pass
        
    def write_error(self, status_code, **kwargs):
        import traceback
        if self.settings['debug']:
            super().write_error(status_code, **kwargs)
        else:
            self.render('error', code=status_code)
    def bulk_arguments(self, fields):
        return { field: self.get_body_argument(field, '') for field in fields }
        
    def get_template_namespace(self):
        namespace = super().get_template_namespace()
        namespace.update({
            'helper': import_object('tmpl.helper')
        })
        return namespace