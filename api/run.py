from flask.helpers import get_debug_flag
from gazo import api, settings

CONFIG = settings.DevConfig if get_debug_flag() else settings.ProdConfig
app = api.create_app(CONFIG)
app.config["JSON_SORT_KEYS"] = False
app.run(host=app.config['HOST_BASENAME'], port=app.config['HOST_PORT'])
