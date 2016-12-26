from tornado.web import RequestHandler

from web.handlers.handlers_module import HandlersModule


class View(HandlersModule):
    def module(self):
        return "view"

    def rendering_handler(self, view):
        class Handler(RequestHandler):
            def get(self, *args):
                self.render(view + ".html")
        return Handler

    def handlers_specs(self):
        return [
            ("visualisation3d", self.rendering_handler("visualization_3d")),
            ("visualisation2d", self.rendering_handler("visualization_2d")),
            ("fingerprint", self.rendering_handler("fingerprint")),
            ("path", self.rendering_handler("path")),
            ("report2d", self.rendering_handler("report_2d")),
            ("root", self.rendering_handler("index"))
        ]