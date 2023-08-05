from tornado import web, ioloop, routing
from .router import router as mvc_router
from .config import configuration
import sys
from .logger import logger

class main(web.RequestHandler):
    def prepare(self):
        self.isExec = True
        for middlewareName in configuration.middleware_list:
            middleware = getattr(__import__(middlewareName), middlewareName)(self)
            if hasattr(middleware, "prepare"):
                self.isExec = getattr(middleware, "prepare")()
                if not self.isExec:
                    break

    def on_finish(self):
        if self.isExec:
            for middlewareName in configuration.middleware_list:
                middleware = getattr(__import__(middlewareName), middlewareName)(self)
                if hasattr(middleware, "finish"):
                    getattr(middleware, "finish")()

    def get(self):
        if self.isExec:
            self.router()

    def post(self):
        if self.isExec:
            self.router()

    def router(self):
        try:
            router = mvc_router(self.request.uri)
            controller = getattr(__import__(router.controller), router.controller)(self)
            getattr(controller, router.action)()
        except Exception as e:
            logger.error("An error has occurred in the main run {router.controller}/{router.action}, error:{e}".format(**locals()))
            self.set_status(500, e)

class application():
    def __init__(self, appPath, config, port=None):
        self.port = port
        configuration.init(config, appPath)
        self._init_router()
        self._init_path()
        self._run_plugins()

    def _init_router(self):
        self.router = [(r".*", main)]

    def _init_path(self):
        sys.path.insert(0, configuration.controller_path)
        sys.path.insert(0, configuration.middleware_path)
        sys.path.insert(0, configuration.plugin_path)
        sys.path.insert(0, configuration.filter_path)

    def _run_plugins(self):
        for plugin in configuration.plugin_list:
            plugin = getattr(__import__(plugin), plugin)
            self._run_plugin(plugin)

    def _run_plugin(self, plugin):
        plugin(self)

    def run(self):
        self.app = web.Application(self.router)
        self.app.listen(configuration.port if not self.port else self.port)
        ioloop.IOLoop.current().start()