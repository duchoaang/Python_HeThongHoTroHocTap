from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum, Date
from sqlalchemy.orm import relationship,backref
from eduapp import db, app
from enum import Enum as UserEnum
from datetime import datetime
from flask_login import UserMixin
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    SINHVIEN = 1
    GIANGVIEN = 2
    ADMIN = 3

class DangBaiTap(UserEnum):
    TRUE_FALSE = 1
    NHIEU_DAP_AN = 2
    MOT_DAP_AN = 3
    DIEN_KHUYET = 4



class GiangVien(BaseModel):
    __tablename__ = 'giang_vien'
    ma_giang_vien = Column(String(10), nullable=False, unique=True)
    ten_giang_vien = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.GIANGVIEN)

class MonHoc(BaseModel):
    __tablename__ = 'mon_hoc'
    ma_mon_hoc = Column(String(10), nullable=False)
    ten_mon_hoc = Column(String(50), nullable=False)
    image = Column(String(255), default="https://cuongquach.com/wp-content/uploads/2019/03/code-dao-ki-su-pdf.jpg")
    is_active = Column(Boolean, default=True)
    so_tin_chi = Column(String(50))

class GiangVienMonHoc(BaseModel):
    __tablename__ = 'giangvien_monhoc'

    idGiangVien = Column(Integer, ForeignKey(GiangVien.id), nullable=False, primary_key=True)
    idMonHoc = Column(Integer, ForeignKey(MonHoc.id), nullable=False, primary_key=True)


class HocKy(BaseModel):
    __tablename__ = 'hoc_ky'
    ma_hoc_ky = Column(String(10), nullable=False, unique=True)
    ten_hoc_ky = Column(String(50), nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)


class MonHoc_HocKy(BaseModel):
    __tablename__ = 'mon_hoc_hoc_ky'
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.id'), nullable=False)
    hoc_ky_id = Column(Integer, ForeignKey('hoc_ky.id'), nullable=False)
    mon_hoc = relationship('MonHoc', backref='hoc_ky')
    hoc_ky = relationship('HocKy', backref='mon_hoc')

class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    mssv = Column(String(10), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gpa = Column(Float, default=4)
    diemHeMuoi = Column(Float, default=10)
    avatar = Column(Text, default='https://antimatter.vn/wp-content/uploads/2022/11/anh-avatar-trang-fb-mac-dinh.jpg')
    diachi = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    lop = Column(String(50), nullable=False)
    nien_khoa = Column(String(20), nullable=False)
    diem_ren_luyen = Column(Integer, default=80)
    nganh = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime, nullable=False, default=datetime.now())
    role = Column(Enum(UserRole), default=UserRole.SINHVIEN)

class DiemMonHoc(BaseModel):
    __tablename__ = 'diem_mon_hoc'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    mon_hoc_id = Column(Integer, ForeignKey(MonHoc.id), nullable=False)
    hoc_ky_id = Column(Integer, ForeignKey(HocKy.id), nullable=False)
    diem_so = Column(Float, nullable=False)
    thoi_gian = Column(DateTime, default=datetime.now())
    user = relationship('User', backref='diem_mon_hoc')
    mon_hoc = relationship('MonHoc', backref='diem_mon_hoc')
    hoc_ky = relationship('HocKy', backref='diem_mon_hoc')


class BaiTap(BaseModel):
    __tablename__ = 'bai_tap'

    ten_bai_tap = Column(String(100), nullable=False)
    de_bai = Column(String(255))
    cau_hoi = Column(String(255), nullable=False)
    dang_bai_tap = Column(Enum(DangBaiTap), nullable= False)
    image = Column(String(255), default="https://s3.vio.edu.vn/media-thumbnail/g1_200819_1.1.%20Cac%20so%201%202%203.PNG")
    mon_hoc_id = Column(Integer,ForeignKey(MonHoc.id), nullable= False)
    mon_hoc = relationship('MonHoc', backref='bai_tap')


class DapAnBaiTap(BaseModel):
    __tablename__ = 'dap_an_bai_tap'

    noi_dung_dap_an = Column(String(100), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    bai_tap_id = Column(Integer, ForeignKey(BaiTap.id), nullable=False)
    bai_tap = relationship('BaiTap', backref='dap_an_bai_tap')



if __name__ == '__main__':
    with app.app_context():
        # step 0
        # db.drop_all()
        # db.create_all()
        # giangvien1 = GiangVien(ma_giang_vien="GV001", ten_giang_vien="Hồ Hướng Thiên", email="gv1@example.com",
        #                        role=UserRole.GIANGVIEN)
        # giangvien2 = GiangVien(ma_giang_vien="GV002", ten_giang_vien="Nguyễn Hữu A", email="gv2@example.com",
        #                        role=UserRole.GIANGVIEN)
        # db.session.add(giangvien1)
        # db.session.add(giangvien2)
        #
        # # Tạo dữ liệu cho bảng MonHoc
        # monhoc1 = MonHoc(ma_mon_hoc="MH001", ten_mon_hoc="Lập trình hướng đối tượng", is_active=True, so_tin_chi="3")
        # monhoc2 = MonHoc(ma_mon_hoc="MH002", ten_mon_hoc="Toán cao cấp", is_active=True, so_tin_chi="4")
        # monhoc3 = MonHoc(ma_mon_hoc="MH003", ten_mon_hoc="Lịch sử đảng", is_active=True, so_tin_chi="4")
        # monhoc4 = MonHoc(ma_mon_hoc="MH004", ten_mon_hoc="Mạng máy tính", is_active=True, so_tin_chi="4")
        # db.session.add(monhoc1)
        # db.session.add(monhoc2)
        # db.session.add(monhoc3)
        # db.session.add(monhoc4)
        #
        # # Tạo dữ liệu cho bảng HocKy
        # hocky1_22 = HocKy(ma_hoc_ky="HK001_22", ten_hoc_ky="Học kỳ 1", ngay_bat_dau=datetime(2022, 1, 1),
        #                ngay_ket_thuc=datetime(2022, 3, 31))
        # hocky1_23 = HocKy(ma_hoc_ky="HK001_23", ten_hoc_ky="Học kỳ 1", ngay_bat_dau=datetime(2023, 1, 1),
        #                ngay_ket_thuc=datetime(2023, 3, 31))
        # hocky2_23 = HocKy(ma_hoc_ky="HK002_23", ten_hoc_ky="Học kỳ 2", ngay_bat_dau=datetime(2024, 3, 1),
        #                ngay_ket_thuc=datetime(2023, 6, 24))
        # hocky3_23 = HocKy(ma_hoc_ky="HK003_23", ten_hoc_ky="Học kỳ 3", ngay_bat_dau=datetime(2024, 6, 23),
        #                ngay_ket_thuc=datetime(2023, 9, 23))
        # db.session.add(hocky1_22)
        # db.session.add(hocky1_23)
        # db.session.add(hocky2_23)
        # db.session.add(hocky3_23)
        #
        #
        # # Tạo dữ liệu cho bảng User
        # user1 = User(
        #     mssv="SV001",
        #     email="sv1@example.com",
        #     gpa=3.5,
        #     diemHeMuoi=8,
        #     avatar="https://antimatter.vn/wp-content/uploads/2022/11/anh-avatar-trang-fb-mac-dinh.jpg",
        #     diachi="Dia chi 1",
        #     username="user",
        #     password="123",
        #     name="Nguyễn Đức Hoàng A",
        #     lop="DH20IT01",
        #     nien_khoa="2023-2024",
        #     diem_ren_luyen=85,
        #     nganh="Công Nghệ Thông Tin",
        #     role=UserRole.SINHVIEN,
        # )
        #
        # user2 = User(
        #     mssv="SV002",
        #     email="sv2@example.com",
        #     gpa=3.8,
        #     diemHeMuoi=9,
        #     avatar="https://antimatter.vn/wp-content/uploads/2022/11/anh-avatar-trang-fb-mac-dinh.jpg",
        #     diachi="Đắk lăk",
        #     username="user1",
        #     password="123",
        #     name="Nguyễn Đức Hoàng",
        #     lop="DH20IT01",
        #     nien_khoa="2023-2024",
        #     diem_ren_luyen=90,
        #     nganh="Công nghệ sinh học",
        #     role=UserRole.SINHVIEN,
        # )
        # db.session.add(user1)
        # db.session.add(user2)

        # step 1

        diem1 = DiemMonHoc(user_id=1, mon_hoc_id=1, hoc_ky_id=1, diem_so=8.5)
        diem2 = DiemMonHoc(user_id=1, mon_hoc_id=2, hoc_ky_id=2, diem_so=9.0)
        diem3 = DiemMonHoc(user_id=1, mon_hoc_id=3, hoc_ky_id=3, diem_so=7.5)
        diem4 = DiemMonHoc(user_id=1, mon_hoc_id=4, hoc_ky_id=4, diem_so=5.5)
        db.session.add(diem1)
        db.session.add(diem2)
        db.session.add(diem3)
        db.session.add(diem4)
        monhoc_hocky1 = MonHoc_HocKy(mon_hoc_id=1, hoc_ky_id=1)
        monhoc_hocky2 = MonHoc_HocKy(mon_hoc_id=2, hoc_ky_id=2)
        monhoc_hocky3 = MonHoc_HocKy(mon_hoc_id=3, hoc_ky_id=3)
        monhoc_hocky4 = MonHoc_HocKy(mon_hoc_id=4, hoc_ky_id=4)
        db.session.add(monhoc_hocky1)
        db.session.add(monhoc_hocky2)
        db.session.add(monhoc_hocky3)
        db.session.add(monhoc_hocky4)




        bai_tap_1 = BaiTap(
            ten_bai_tap = 'Bài tập củng cố',
            de_bai = 'Việt nam có nhiều thành phố lớn',
            cau_hoi = 'Đâu là thành phố của Việt Nam',
            dang_bai_tap = DangBaiTap.NHIEU_DAP_AN,
            mon_hoc_id = '1',
        )
        db.session.add(bai_tap_1)
        bai_tap_2 = BaiTap(
            ten_bai_tap='Bài tập củng cố',
            de_bai='Mỹ có nhiều thành phố lớn',
            cau_hoi='Đâu là thành phố của Mỹ',
            dang_bai_tap=DangBaiTap.NHIEU_DAP_AN,
            mon_hoc_id='1',
        )
        db.session.add(bai_tap_2)




        dap_an = DapAnBaiTap(
            noi_dung_dap_an = 'Paries',
            is_correct = False,
            bai_tap_id = 1,
        )
        dap_an_2 = DapAnBaiTap(
            noi_dung_dap_an = 'TPHCM',
            is_correct = True,
            bai_tap_id = 1
        )
        dap_an_3 = DapAnBaiTap(noi_dung_dap_an = 'America', is_correct = False, bai_tap_id = 1)
        db.session.add(dap_an)
        db.session.add(dap_an_2)
        db.session.add(dap_an_3)


        db.session.commit()