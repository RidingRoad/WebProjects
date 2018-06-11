from flask import Blueprint
user_blue = Blueprint("user",__name__,url_prefix="/ridingroad")
from  user import views

#
# @user_blue.route('/user')
# def user():
#     return "user"