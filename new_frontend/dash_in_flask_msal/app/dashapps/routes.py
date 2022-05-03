from flask import render_template

from app.dashapps import bp
# from app.dashapps import dash_app_1 as dash_app_1_obj
# from app.dashapps import dash_app_2 as dash_app_2_obj
from app.dashapps import leaf_frontend as leaf_frontend_obj
from app.dashapps import group_or_parent_frontend as group_or_parent_frontend_obj
from app.dashapps import compound_frontend as compound_frontend_obj
from app.dashapps import rootdistance_frontend as rootdistance_frontend_obj
# @bp.route("/dash_app_1")
# def dash_app_1():
#     return render_template('dashapps/dash_app.html', dash_url=dash_app_1_obj.URL_BASE, min_height=dash_app_1_obj.MIN_HEIGHT)

# @bp.route("/dash_app_2")
# def dash_app_2():
#     return render_template('dashapps/dash_app.html', dash_url=dash_app_2_obj.URL_BASE, min_height=dash_app_2_obj.MIN_HEIGHT)

@bp.route("/leaf_frontend")
def leaf_frontend():
    return render_template('dashapps/dash_app.html', dash_url=leaf_frontend_obj.URL_BASE, min_height=leaf_frontend_obj.MIN_HEIGHT)
@bp.route("/group_or_parent_frontend")
def group_or_parent_frontend():
    return render_template('dashapps/dash_app.html', dash_url=group_or_parent_frontend_obj.URL_BASE, min_height=group_or_parent_frontend_obj.MIN_HEIGHT)
@bp.route("/compound_frontend")
def compound_frontend():
    return render_template('dashapps/dash_app.html', dash_url=compound_frontend_obj.URL_BASE, min_height=compound_frontend_obj.MIN_HEIGHT)
@bp.route("/rootdistance_frontend")
def rootdistance_frontend():
    return render_template('dashapps/dash_app.html', dash_url=rootdistance_frontend_obj.URL_BASE, min_height=rootdistance_frontend_obj.MIN_HEIGHT)
