from flask_sqlalchemy import SQLAlchemy

from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, create_engine, Date
from sqlalchemy.orm import relationship, Session, sessionmaker
from datetime import datetime
#



class User(db.Model, UserMixin):
    __tablename__ = 'User'

    ID = db.Column(db.Integer, primary_key=True)
    Ho = Column(String(length=255))
    Ten = Column(String(length=255))
    Email = Column(String(length=255))
    Thanh_pho = Column(String(length=255))
    Sdt = Column(String(length=255))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_role = db.Column(db.Integer, nullable=False, default=1)
    feedbacks = relationship('Feedback', backref='khachhang')
    hoa_dons = relationship('HoaDon', backref='khachhang')

    def get_id(self):
        return str(self.ID)




class DiaDiem(db.Model):
    __tablename__ = 'diaDiem'

    ID = Column(Integer, primary_key=True)
    Ten = Column(String(length=255))
    Mo_ta = Column(String(length=1000))
    Gia = Column(Float)
    feedbacks = relationship('Feedback', backref='diadiem')
    tours = relationship('Tour', backref='diadiem')


class Feedback(db.Model):
    __tablename__ = 'feedBack'

    ID = Column(Integer, primary_key=True)
    Khach_ID = Column(Integer, ForeignKey('User.ID'))
    Feedback = Column(String(length=255))
    Dia_diem_ID = Column(Integer, ForeignKey('diaDiem.ID'))
    Danh_gia = Column(Integer)
    Ngay_Danh_gia = Column(DateTime, default=datetime.now())


class Tour(db.Model):
    __tablename__ = 'tour'

    ID = Column(Integer, primary_key=True)
    Dia_diem_ID = Column(Integer, ForeignKey('diaDiem.ID'))
    Ngay_bat_dau_di = Column(DateTime)
    Ngay_ket_thuc = Column(DateTime)
    Anh = Column(String(length=255))
    Anh2 = Column(String(length=255))
    Anh3 = Column(String(length=255))
    Tong_tien = Column(Float)
    SoLuong = Column(Integer)
    Baogom1 = Column(String(length=255))
    Baogom2 = Column(String(length=255))
    Baogom3 = Column(String(length=255))
    Baogom4 = Column(String(length=255))
    hoadons = relationship('HoaDon', backref='tour')




class HoaDon(db.Model):
    __tablename__ = 'hoaDon'

    ID = Column(Integer, primary_key=True)
    Tour_ID = Column(Integer, ForeignKey('tour.ID'))
    UuDai_ID = Column(Integer, ForeignKey('uudai.id'))
    Ngay_thanh_toan = Column(DateTime, default=datetime.now())
    So_tien_thanh_toan = Column(Float)
    So_luong_nguoi_di = Column(Integer)
    khachhang_id = Column(Integer, ForeignKey('User.ID'))
    Note = Column(String(length=1000))

class UuDai(db.Model):
    __tablename__ = 'uudai'

    id = db.Column(db.Integer, primary_key=True)
    ma_giam_gia = db.Column(db.String(20), unique=True, nullable=False)
    gia_tri = db.Column(db.Float, nullable=False)
    hoadon_uudai = relationship('HoaDon', backref='uudai')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
#         # Commit the changes to the database

        session = Session()

        User = User(ID=1, Ho='John1', Ten='Doe1', Email='1john@example.com', Thanh_pho='City', Sdt='1234567891',
                    username='admin', password='$2a$12$0cn6DBynD.10/vQEza1svekS.C8U40mSUmLIQttfcZgl9sJuMSEJK',user_role=0)
        db.session.add(User)

        # Example data for DiaDiem table
        diadiem = DiaDiem(ID=1, Ten='Đà Lạt',
                          Mo_ta='Đà Lạt là thành phố tỉnh lỵ trực thuộc tỉnh Lâm Đồng, nằm trên cao nguyên Lâm Viên, thuộc vùng Tây Nguyên, Việt Nam. Từ xa xưa, vùng đất này vốn là địa bàn cư trú của những cư dân người Lạch, người Chil và người Srê thuộc dân tộc Cơ Ho. Cuối thế kỷ 19, khi tìm kiếm một địa điểm để xây dựng trạm nghỉ dưỡng dành cho người Pháp ở Đông Dương, Toàn quyền Paul Doumer đã quyết định chọn cao nguyên Lâm Viên theo đề nghị của bác sĩ Alexandre Yersin, người từng thám hiểm tới nơi đây vào năm 1893. Trong nửa đầu thế kỷ 20, từ một địa điểm hoang vu, người Pháp đã quy hoạch và xây dựng lên một thành phố xinh đẹp với những biệt thự',
                          Gia=200.0)
        diadiem2 = DiaDiem(ID=2, Ten='Vũng Tàu',
                           Mo_ta='Đây là trung tâm kinh tế, tài chính, văn hóa, du lịch, giao thông - vận tải và giáo dục và là một trong những trung tâm kinh tế của vùng Đông Nam Bộ.',
                           Gia=200.0)
        diadiem3 = DiaDiem(ID=3, Ten='Hội An',
                           Mo_ta='Phố cổ Hội An từng là một thương cảng quốc tế sầm uất, gồm những di sản kiến trúc đã có từ hàng trăm năm trước.',
                           Gia=200.0)
        diadiem4 = DiaDiem(ID=4, Ten='Đồng Bằng Sông Cửu Long',
                           Mo_ta='Vùng đồng bằng sông Cửu Long là vùng cực nam của Việt Nam, một trong hai phần của Nam Bộ',
                           Gia=300.0)
        diadiem5 = DiaDiem(ID=5, Ten='Sài Gòn',
                           Mo_ta='Thành phố Hồ Chí Minh (thường được gọi là Sài Gòn) là một thành phố ở miền nam Việt Nam nổi tiếng với vai trò nòng cốt trong chiến tranh Việt Nam.',
                           Gia=400.0)
        diadiem6 = DiaDiem(ID=6, Ten='Hà Nội',
                           Mo_ta='Hà Nội, thủ đô của Việt Nam, nổi tiếng với kiến trúc trăm tuổi và nền văn hóa phong phú',
                           Gia=200.0)
        diadiem7 = DiaDiem(ID=7, Ten='Nha Trang',
                           Mo_ta='Nha Trang là một thành phố ven biển và là trung tâm chính trị, kinh tế, văn hóa, khoa học kỹ thuật và du lịch của tỉnh Khánh Hòa, Việt Nam',
                           Gia=100.0)
        diadiem8 = DiaDiem(ID=8, Ten='Đà Nẵng',
                           Mo_ta='Đà Nẵng là một trong năm thành phố trực thuộc trung ương của Việt Nam',
                           Gia=200.0)
        diadiem9 = DiaDiem(ID=9, Ten='Sapa',
                           Mo_ta='Sapa - một vùng đất khiêm nhường, lặng lẽ nhưng ẩn chứa bao điều kỳ diệu của cảnh sắc thiên nhiên. Phong cảnh thiên nhiên của Sa Pa được kết hợp với sức sáng tạo của con người cùng với địa hình của núi đồi, màu xanh của rừng, như bức tranh có sự sắp xếp theo một bố cục hài hoà tạo nên một vùng có nhiều cảnh sắc thơ mộng hấp dẫn. Chìm trong làn mây bồng bềnh thị trấn Sa Pa như một thành phố trong sương huyền ảo, làm cho du khách cữ ngỡ như mình đang lạc trong chốn thần tiên. Nơi đây, có thứ tài nguyên vô giá đó là khí hậu trong lành mát mẻ, mang nhiều sắc thái đa dạng.',
                           Gia=300.0)

        db.session.add(diadiem)
        db.session.add(diadiem2)
        db.session.add(diadiem3)
        db.session.add(diadiem4)
        db.session.add(diadiem5)
        db.session.add(diadiem6)
        db.session.add(diadiem7)
        db.session.add(diadiem8)
        db.session.add(diadiem9)

        # Example data for Tour table
        tour = Tour(ID=1, Dia_diem_ID=1, Ngay_bat_dau_di='2023-09-15',
                    Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng', Baogom4='Mát xa',
                    Ngay_ket_thuc='2023-09-20',
                    Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-1-400h_otzoep.webp',
                    Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-31-1500w_dojbcv.webp',
                    Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-51-1500w_u4wnbl.webp',
                    Tong_tien=180.0, SoLuong=2)
        tours = Tour(ID=2, Dia_diem_ID=1, Ngay_bat_dau_di='2023-09-15',
                    Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng', Baogom4='Mát xa',
                    Ngay_ket_thuc='2023-09-20',
                    Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-1-400h_otzoep.webp',
                    Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-2-400h_oyn2dl.webp',
                    Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-51-1500w_u4wnbl.webp',
                    Tong_tien=180.0, SoLuong=2)
        tour1 = Tour(ID=3, Dia_diem_ID=2, Ngay_bat_dau_di='2023-09-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Tối', Baogom4='Gym',
                     Ngay_ket_thuc='2023-09-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-1-400h_otzoep.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-51-1500w_u4wnbl.webp',
                     Tong_tien=180.0, SoLuong=1)
        tour2 = Tour(ID=4, Dia_diem_ID=3, Ngay_bat_dau_di='2023-10-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng', Baogom4='Mát xa',
                     Ngay_ket_thuc='2023-10-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-2-400h_oyn2dl.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-31-1500w_dojbcv.webp',
                     Tong_tien=180.0, SoLuong=3)
        tour3 = Tour(ID=5, Dia_diem_ID=4, Ngay_bat_dau_di='2023-09-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Tối', Baogom4='Gym',
                     Ngay_ket_thuc='2023-09-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-2-400h_oyn2dl.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-2-400h_oyn2dl.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-61-1500w_kno8vi.webp',
                     Tong_tien=180.0, SoLuong=3)
        tour4 = Tour(ID=6, Dia_diem_ID=5, Ngay_bat_dau_di='2023-09-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng', Baogom4='Mát xa',
                     Ngay_ket_thuc='2023-09-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-3-400h_zhpzph.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-1-400h_otzoep.webp',
                     Tong_tien=180.0, SoLuong=3)
        tour5 = Tour(ID=7, Dia_diem_ID=6, Ngay_bat_dau_di='2023-11-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Tối', Baogom4='Gym',
                     Ngay_ket_thuc='2023-11-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-31-1500w_dojbcv.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-31-1500w_dojbcv.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-2-400h_oyn2dl.webp',
                     Tong_tien=180.0, SoLuong=1)
        tour6 = Tour(ID=8, Dia_diem_ID=7, Ngay_bat_dau_di='2023-12-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng', Baogom4='Mát xa',
                     Ngay_ket_thuc='2023-12-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-41-1500w_augj8j.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712354/offers-31-1500w_dojbcv.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Tong_tien=180.0, SoLuong=3)
        tour7 = Tour(ID=9, Dia_diem_ID=8, Ngay_bat_dau_di='2023-09-15',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng - Tối', Baogom4='Gym',
                     Ngay_ket_thuc='2023-09-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-81-1500w_al9jqj.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-61-1500w_kno8vi.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Tong_tien=180.0, SoLuong=3)
        tour8 = Tour(ID=10, Dia_diem_ID=9, Ngay_bat_dau_di='2023-09-10',
                     Baogom1='Khách sạn 5 sao', Baogom2='Hồ Bơi', Baogom3='Bữa Sáng - Tối', Baogom4='Gym',
                     Ngay_ket_thuc='2023-09-20',
                     Anh='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-61-1500w_kno8vi.webp',
                     Anh3='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712404/destination-4-400h_kkfvbr.webp',
                     Anh2='https://res.cloudinary.com/drhgfqbzv/image/upload//c_thumb,w_160,h_140,g_auto/v1695712353/offers-81-1500w_al9jqj.webp',
                     Tong_tien=180.0, SoLuong=3)
        db.session.add(tour)
        db.session.add(tours)
        db.session.add(tour1)
        db.session.add(tour2)
        db.session.add(tour3)
        db.session.add(tour4)
        db.session.add(tour5)
        db.session.add(tour6)
        db.session.add(tour7)
        db.session.add(tour8)

        # Example data for Feedback table
        feedback = Feedback(Khach_ID=1, Dia_diem_ID=1, Feedback='Great experience!', Danh_gia=5,
                            Ngay_Danh_gia='2023-07-21'
                           )
        feedback1 = Feedback(Khach_ID=1, Dia_diem_ID=1, Feedback='Great great experience!', Danh_gia=5,
                            Ngay_Danh_gia='2023-07-21'
                            )
        db.session.add(feedback)
        db.session.add(feedback1)

        # Example data for UuDai table
        uudai = UuDai(id=1, gia_tri=0.3, ma_giam_gia='SUMMER10')
        uudai1 = UuDai(id=2, gia_tri=0.2, ma_giam_gia='SUMMER20')
        db.session.add(uudai)
        db.session.add(uudai1)

        # Example data for HoaDon table
        hoadon = HoaDon(Tour_ID=1, UuDai_ID=1, Ngay_thanh_toan='2023-01-22', So_tien_thanh_toan=150.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon0 = HoaDon(Tour_ID=1, UuDai_ID=1, Ngay_thanh_toan='2023-02-22', So_tien_thanh_toan=180.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon1 = HoaDon(Tour_ID=2, UuDai_ID=1, Ngay_thanh_toan='2023-03-22', So_tien_thanh_toan=150.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon2 = HoaDon(Tour_ID=3, UuDai_ID=1, Ngay_thanh_toan='2023-04-22', So_tien_thanh_toan=180.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon3 = HoaDon(Tour_ID=4, UuDai_ID=1, Ngay_thanh_toan='2023-05-22', So_tien_thanh_toan=200.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon4 = HoaDon(Tour_ID=5, UuDai_ID=1, Ngay_thanh_toan='2023-06-22', So_tien_thanh_toan=150.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon5 = HoaDon(Tour_ID=6, UuDai_ID=1, Ngay_thanh_toan='2023-07-22', So_tien_thanh_toan=200.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon6 = HoaDon(Tour_ID=7, UuDai_ID=1, Ngay_thanh_toan='2023-08-22', So_tien_thanh_toan=200.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon7 = HoaDon(Tour_ID=8, UuDai_ID=1, Ngay_thanh_toan='2023-09-22', So_tien_thanh_toan=150.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon8 = HoaDon(Tour_ID=9, UuDai_ID=1, Ngay_thanh_toan='2023-10-22', So_tien_thanh_toan=300.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        hoadon9 = HoaDon(Tour_ID=10, UuDai_ID=1, Ngay_thanh_toan='2023-11-22', So_tien_thanh_toan=150.0,
                        So_luong_nguoi_di=2, khachhang_id=1)
        db.session.add(hoadon)
        db.session.add(hoadon0)
        db.session.add(hoadon1)
        db.session.add(hoadon2)
        db.session.add(hoadon3)
        db.session.add(hoadon4)
        db.session.add(hoadon5)
        db.session.add(hoadon6)
        db.session.add(hoadon7)
        db.session.add(hoadon8)
        db.session.add(hoadon9)

#
        db.session.commit()
