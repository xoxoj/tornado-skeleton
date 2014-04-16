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
        for url, assignee in my.config.routes:
            # Dynamic import handlers
            (module, handler) = assignee.split('@')
            if not module in loaded:
                loaded[module] = tornado.util.import_object('handler.' + module)
            handlers.append((url, getattr(loaded[module], handler)))
        handlers.append((r"/static/(.*)",  tornado.web.StaticFileHandler, {"path": my.config.path + "/static"}))
        my.config.setting.update(dict(
            ui_modules = tornado.util.import_object('ui')
        ))
        super().__init__(handlers, **my.config.setting)
        self.config = my.config
        if not my.config.setting['debug']:
            logging.basicConfig(filename=self.base_path + '/var/app.log', level=logging.WARNING)

class IOLoop(tornado.ioloop.IOLoop):
    pass
    
def main():
    tornado.options.parse_command_line()
    app = App()
    os.environ['TZ'] = my.config.timezone
    time.tzset()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(my.config.port, my.config.host)
    ioloop = IOLoop.instance()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        # Gracefully shutdown, add cleanup here if necessary
        print('Server got the signal. Bye!')

if __name__ == "__main__":
    main()