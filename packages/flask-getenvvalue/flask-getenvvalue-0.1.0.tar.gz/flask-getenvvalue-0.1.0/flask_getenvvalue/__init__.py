__version__ = '0.1.0'

import os


class GetEnvValue:
    def __init__(self,
                 app=None,
                 envnames=None,
                 *,
                 ignore_undefined=True,
                 protect_exists=False):
        self.envnames = envnames if envnames else []
        self.ignore_undefined = ignore_undefined
        self.protect_exists = protect_exists
        if app:
            self.init_app(app)

    def init_app(self, app):
        for envname in self.envnames:
            value = os.environ.get(envname)
            if self.ignore_undefined and value is None:
                continue
            if self.protect_exists and envname in app.config:
                continue
            app.config[envname] = value
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        pass
