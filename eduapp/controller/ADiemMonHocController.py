from flask import Blueprint, jsonify, request
from eduapp import dao, app
from eduapp.models import DiemMonHoc

from flask import jsonify, request

def diem_serializer(diem):
    return {
        'user': diem.user.name,
        'mon_hoc': diem.mon_hoc.ten_mon_hoc,
        'hoc_ki': diem.hoc_ky.ten_hoc_ky,
        'thoi_gian': diem.thoi_gian.strftime('%Y-%m-%d'),
        'diem': diem.diem_so
    }


@app.route('/api/diem/<user_id>')
def get_diem(user_id):
    list_diem= dao.get_all_diem_by_user_id(user_id)
    # print(diem)
    if list_diem is not None:
        serialized_diem_list = [diem_serializer(diem) for diem in list_diem]
        return jsonify(serialized_diem_list)
    else:
        return jsonify({'error': 'Diem not found'})

# @app.route('api/check-dap-an')
# def check_da_an():
#
# dap_an = request.