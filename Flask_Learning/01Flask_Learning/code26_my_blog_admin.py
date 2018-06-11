# it needs a special model to process the modular(blueprint)
from flask import Blueprint
admin = Blueprint("admin",__name__,url_prefix="/admin")
@admin.route('/')
def admin_home():
    return 'admin_home'

@admin.route('/new')
def new():
    return 'new'

@admin.route('/edit')
def edit():
    return 'edit'

@admin.route('/publish')
def publish():
    return 'publish'