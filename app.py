#!/usr/bin/env python3

# Vendor
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.util
import os.path

# App internal

# Command line option
tornado.options.define("env", default='local', help="Run environment", type=str)

class App(tornado.web.Application):

    def __init__(self):
        import conf
        conf.envName = tornado.options.options['env']
        settings = conf.env['common']
        settings.update(conf.env[conf.envName])
        
        # Routes
        handlers = []
        loaded_modules = {}
        importer = tornado.util.import_object
        for url, module, handler in conf.routes:
            # Dynamic import handlers
            if not module in loaded_modules:
                loaded_modules[module] = importer(conf.handler_path + module)
            handlers.append((url, getattr(loaded_modules[module], handler)))
        settings['ui_modules'] = importer('ui')
        super(App, self).__init__(handlers, **settings)
        self.conf = conf
        self.base_path = os.path.realpath(__file__) + '/' # App base path

class IOLoop(tornado.ioloop.IOLoop):
    pass
    
def main():
    tornado.options.parse_command_line()
    app = App()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(app.conf.port, app.conf.host)
    ioloop = IOLoop.instance()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        # Gracefully shutdown, add cleanup here if necessary
        print('Server got the signal. Bye!')

if __name__ == "__main__":
    main()