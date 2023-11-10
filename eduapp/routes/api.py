from flask import Blueprint
from eduapp.controller.AUserController import *
from eduapp.controller.ADiemMonHocController import *

api = Blueprint('api', __name__)

api.route('/user/<id>', methods=['GET'])(get_user)
api.route('/diem/<id>', methods=['GET'])(get_diem)
