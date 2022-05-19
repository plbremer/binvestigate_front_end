from flask import Flask
from config import Config

# extensions
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    # configuration
    app.config.from_object(config_class)

    # register extensions
    bootstrap.init_app(app)

    with app.app_context():

        # register blueprints
        from app.main import bp as bp_main
        app.register_blueprint(bp_main)
        from app.dashapps import bp as bp_dashapps
        app.register_blueprint(bp_dashapps)

        # process dash apps
        # dash app 1
        # from app.dashapps.dash_app_1 import add_dash as ad1
        # app = ad1(app)
        # # # dash app 2
        # from app.dashapps.dash_app_2 import add_dash as ad2
        # app = ad2(app)
        # #leaf frontend

        from app.dashapps.sunburst_frontend import add_dash as ad1
        #this is the third "add dash" function, independent of the dash apps name
        app = ad1(app)

        from app.dashapps.venn_frontend import add_dash as ad2
        #this is the third "add dash" function, independent of the dash apps name
        app = ad2(app)

        from app.dashapps.leaf_frontend import add_dash as ad3
        #this is the third "add dash" function, independent of the dash apps name
        app = ad3(app)

        from app.dashapps.group_or_parent_frontend import add_dash as ad4
        #this is the third "add dash" function, independent of the dash apps name
        app = ad4(app)

        from app.dashapps.compound_frontend import add_dash as ad5
        #this is the third "add dash" function, independent of the dash apps name
        app = ad5(app)

        from app.dashapps.rootdistance_frontend import add_dash as ad6
        #this is the third "add dash" function, independent of the dash apps name
        app = ad6(app)

        return app




