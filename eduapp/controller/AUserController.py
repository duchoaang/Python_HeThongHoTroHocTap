from flask import Blueprint, jsonify, request
from eduapp import dao, app
from eduapp.models import User

from flask import jsonify, request

def user_serializer(user):
    return {
        'mssv': user.mssv,
        'email': user.email,
        'gpa': user.gpa,
        'diemHeMuoi': user.diemHeMuoi,
        'avatar': user.avatar,
        'diachi': user.diachi,
        'username': user.username,
        'password': user.password,
        'name': user.name,
        'lop': user.lop,
        'nien_khoa': user.nien_khoa,
        'diem_ren_luyen': user.diem_ren_luyen,
        'nganh': user.nganh,
        'is_active': user.is_active,
        'joined_at': user.joined_at.strftime('%Y-%m-%d %H:%M:%S'),  # Chuyển đổi thành chuỗi ngày giờ
        'role': user.role.value  # Chuyển đổi thành giá trị enum
    }


@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        serialized_user = user_serializer(user)
        return jsonify(serialized_user)
    else:
        return jsonify({'error': 'User not found'})

