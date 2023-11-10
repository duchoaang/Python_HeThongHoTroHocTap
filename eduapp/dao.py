from eduapp.models import MonHoc, User, HocKy, MonHoc_HocKy, DiemMonHoc, BaiTap, DapAnBaiTap
from eduapp import app
from flask_login import current_user
import qrcode
from flask import Response, jsonify
from pyzbar.pyzbar import decode
import cv2
from flask_login import login_user
def get_info_user_by_id():
    get_u = User.query.get(1)
    return get_u

def check_login(username, password):
    if username and password:
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def encode_qr(user):
    username = user.username
    qr_content = "user"

    img = qrcode.make(qr_content)
    img.save("qr_user.png")

def get_user_by_username(username):
    return User.query.filter(User.username.__eq__(username.strip())).first()


def decode_qr():
    cap = cv2.VideoCapture(0)
    qr_decoded = False
    u_login = ''
    while not qr_decoded:
        ret, frame = cap.read()

        if not ret:
            return jsonify({'error': 'Không thể truy cập camera'})


        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f'Dữ liệu mã QR: {qr_data}')

            u_login = get_user_by_username(qr_data)
            if u_login:
                qr_decoded = True
                print(u_login)
                cap.release()
                cv2.destroyAllWindows()
                return u_login

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return u_login


def get_all_diem_by_user_id(user_id):
    all_diem = DiemMonHoc.query.filter_by(user_id=user_id).all()

    return all_diem
def get_diem_warning_by_user_id(user_id):
    diem_warning = DiemMonHoc.query.filter(DiemMonHoc.user_id.__eq__(user_id), DiemMonHoc.diem_so < 6).all()

    return diem_warning

def get_all_bai_tap_nhieu_dap_an():
    all_bai_tap = BaiTap.query.filter(BaiTap.dang_bai_tap.__eq__("NHIEU_DAP_AN")).all()
    return all_bai_tap

def get_bai_tap_by_id(baitap_id):
    bai_tap = BaiTap.query.filter(BaiTap.id.__eq__(baitap_id)).first()
    return bai_tap

def get_dap_an_bai_tap_by_id(baitap_id):
    dap_an = DapAnBaiTap.query.filter(DapAnBaiTap.bai_tap_id.__eq__(baitap_id)).all()
    return dap_an


def get_dap_an_dung_bai_tap_by_id(baitap_id):
    dap_an_dung = DapAnBaiTap.query.filter(DapAnBaiTap.bai_tap_id == baitap_id, DapAnBaiTap.is_correct==True).first()
    return dap_an_dung
