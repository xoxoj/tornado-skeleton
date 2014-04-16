#!/usr/bin/env python3

# Vendor
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.util
import time, os, os.path
import my.config

# App internal

# Command line option
tornado.options.define("env", default='local', help="Run environment", type=str)

class App(tornado.web.Application):

    def __init__(self):
        # Routes
        handlers = []
        loaded = {}
        for url, module, handler in my.config.routes:
            # Dynamic import handlers
            if not module in loaded:
                loaded[module] = tornado.util.import_object('handler.' + module)
            handlers.append((url, getattr(loaded[module], handler)))
        my.config['ui_modules'] = tornado.util.import_object('ui')
        handlers.append((r"/static/(.*)", tornado.web.StaticFileHandler, {"path": config.path + "/static"}))
        super().__init__(handlers, **my.config)
        self.config = my.config
        if self.conf.env_name != 'local':
            logging.basicConfig(filename=self.base_path + '/var/app.log', level=logging.WARNING)

class IOLoop(tornado.ioloop.IOLoop):
    pass
    
def main():
    tornado.options.parse_command_line()
    app = App()
    os.environ['TZ'] = app.conf.timezone
    time.tzset()
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