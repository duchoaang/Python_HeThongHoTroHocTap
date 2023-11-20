from eduapp import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from eduapp.models import GiangVien, User, DiemMonHoc, MonHoc


admin = Admin(app = app, name="Code Heroes Education", template_mode='bootstrap4')

class UserView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['mssv']

admin.add_view(ModelView(GiangVien, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(DiemMonHoc, db.session))
admin.add_view(ModelView(MonHoc, db.session))