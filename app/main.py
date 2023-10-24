import json
from datetime import datetime, timedelta
from io import BytesIO
from flask import request, session
import bcrypt
import cloudinary.api
from flask import (
    render_template, request, session, redirect,
    make_response, jsonify, flash, url_for, Flask
)
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, current_user
from flask_mail import Mail, Message
from flask_principal import Principal, Permission, RoleNeed
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import extract

from app import models
from app.models import db, Tour, HoaDon, User, DiaDiem, Feedback, UuDai

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:matkhauroot@localhost/doan?charset=utf8mb4"
app.config['SECRET_KEY'] = '123456'
db.init_app(app)
principal = Principal(app)

# Define permissions
admin_permission = Permission(RoleNeed(0))

# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# email
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your email server's SMTP address
app.config['MAIL_PORT'] = 465  # Your email server's SMTP port (e.g., 587 for TLS)
app.config['MAIL_USE_TLS'] = False  # Use TLS for secure connection
app.config['MAIL_USE_SSL'] = True  # Use SSL for secure connection (usually not both TLS and SSL)
app.config['MAIL_USERNAME'] = 'tql1305@gmail.com'  # Your email username
app.config['MAIL_PASSWORD'] = 'grhofctjnjssfern'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'tql1305@gmail.com'
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


cloudinary.config(
    cloud_name="drhgfqbzv",
    api_key="158819295119423",
    api_secret="***************************"
)

image_url = cloudinary.utils.cloudinary_url(
    "test",
    width=300,
    height=200,
    crop="fill"
)[0]


@app.route("/")
def index():
    feedback_data = Feedback.query.all()
    user_data = {user.ID: user.Ten for user in User.query.all()}
    return render_template("index.html", feedback_data=feedback_data, user_data=user_data)


@app.route('/setcookie', methods=['POST'])
def setcookie():
    if request.form['iput1']:
        data = {
            'input1': request.form['iput1'],
            'input2': request.form['iput2'],
            'input3': request.form['iput3'],
        }
    else:
        data = {
            'input1': request.form['input1'],
            'input2': request.form['input2'],
            'input3': request.form['input3'],
        }

    data_json = json.dumps(data)

    response = make_response(redirect('/tour'))
    response.set_cookie('input_cookie', data_json)
    return response


input_d = None


@app.route("/tour")
def tour():
    global input_d
    if input_d is None:
        input_d = request.cookies.get('input_cookie')
    input_d = request.cookies.get('input_cookie')
    users = models.User.query.all()
    dia_diem_data = []  # Initialize an empty list to store data
    input_value = request.args.get('input_value', '')
    input_value2 = request.args.get('input_value2', '')
    input_value3 = request.args.get('input_value3', '')

    if input_d:
        data = json.loads(input_d)
        input1, input2, input3 = data['input1'], data['input2'], data['input3']
        dia_diems = models.DiaDiem.query.filter_by(Ten=input1).all()

        if dia_diems:
            for dia_diem in dia_diems:
                tours = models.Tour.query.filter_by(Dia_diem_ID=dia_diem.ID).all()

                for tour in tours:
                    dia_diem_data.append({
                        'Ten': dia_diem.Ten,
                        'Mota': dia_diem.Mo_ta,
                        'Gia': tour.Tong_tien,
                        'ID': tour.ID,
                        'SoLuong': tour.SoLuong,
                        'KhoiHanh': tour.Ngay_bat_dau_di,
                        'Anh': tour.Anh,
                        'Anh2': tour.Anh2,
                        'Anh3': tour.Anh3,
                        'KetThuc': tour.Ngay_ket_thuc,
                        'bg1': tour.Baogom1,
                        'bg2': tour.Baogom2,
                        'bg3': tour.Baogom3,
                        'bg4': tour.Baogom4
                    })

            if dia_diem_data:  # Check if there's any data
                session['dia_diem_data'] = dia_diem_data
                return render_template("tour.html", input_d1=input1, input_d2=input2, input_d3=input3, users=users)
    else:
        dia_diems = models.DiaDiem.query.filter_by(Ten=input_value).all()
        if dia_diems:
            for dia_diem in dia_diems:
                tours = models.Tour.query.filter_by(Dia_diem_ID=dia_diem.ID).all()

                for tour in tours:
                    dia_diem_data.append({
                        'Ten': dia_diem.Ten,
                        'Mota': dia_diem.Mo_ta,
                        'Gia': tour.Tong_tien,
                        'ID': tour.ID,
                        'SoLuong': tour.SoLuong,
                        'KhoiHanh': tour.Ngay_bat_dau_di,
                        'Anh': tour.Anh,
                        'Anh2': tour.Anh2,
                        'Anh3': tour.Anh3,
                        'KetThuc': tour.Ngay_ket_thuc,
                        'bg1': tour.Baogom1,
                        'bg2': tour.Baogom2,
                        'bg3': tour.Baogom3,
                        'bg4': tour.Baogom4
                    })

            if dia_diem_data:  # Check if there's any data
                session['dia_diem_data'] = dia_diem_data
                return render_template("tour.html", input_d1=input_value, input_d2=input_value2, input_d3=input_value3,
                                       users=users)

    return render_template("tour.html", input_d1=input1, input_d2=input2, input_d3=input3, users=users,
                           input_value=input_value)


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.ID)
    response = {'success': False, 'message': ''}
    if user:
        # Update user attributes based on the form input
        user.Ho = request.form.get('ho')
        user.Ten = request.form.get('ten')
        user.Email = request.form.get('email')
        user.Thanh_pho = request.form.get('thanh_pho')
        user.Sdt = request.form.get('sdt')

        # Commit the changes to the database
        db.session.commit()

        session['Ho'] = user.Ho
        session['Ten'] = user.Ten
        session['Email'] = user.Email
        session['Thanh_pho'] = user.Thanh_pho
        session['Sdt'] = user.Sdt
        response['success'] = True
        response['message'] = 'Đổi thông tin thành công'
        flash('Profile updated successfully!', 'success')
    else:
        response['message'] = 'Đổi thông tin không thành công'
        flash('User not found', 'error')

    return jsonify(response)


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    user = User.query.get(current_user.ID)
    response = {'success': False, 'message': ''}

    if user:
        # Verify the old password
        Check1 = bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8'))
        if Check1:
            if new_password == confirm_password:
                # Hash the new password
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                user.password = hashed_new_password
                db.session.commit()

                # Update the password in the session
                session['password'] = user.password

                flash('Password changed successfully!', 'success')
                response['success'] = True
                response['message'] = 'Đổi mật khẩu thành công, hãy tải lại trang'
            else:
                flash('New passwords do not match.', 'error')
                response['message'] = 'Xác nhận mật khẩu SAI'
        else:
            flash('Old password is incorrect.', 'error')
            response['message'] = 'SAI mật khẩu'
    else:
        flash('User not found', 'error')
        response['message'] = 'ERROR'

    return jsonify(response)


@app.route("/lichsu_dattour")
@login_required
def lichsu_datttour():
    # Get hoadon records for the current user
    hoadon_data = HoaDon.query.filter_by(khachhang_id=current_user.ID).all()
    tour_data = Tour.query.all()
    diadiem_data = DiaDiem.query.all()
    uudai_data = UuDai.query.all()
    return render_template("lichsu_dattour.html", hoadon_data=hoadon_data, tour_data=tour_data, diadiem_data=diadiem_data, uudai_data=uudai_data)


@app.route('/submit_feedback', methods=['POST'])
@login_required  # Ensure that the user is logged in to submit feedback
def submit_feedback():
    data = request.json
    feedback_text = data['Feedback']
    Tour_ID = data['Tour_ID']
    rating = data['Rating']
    if current_user.is_authenticated and current_user.ID:
        feedback = Feedback(
            Khach_ID=current_user.ID,
            Feedback=feedback_text,
            Dia_diem_ID=Tour_ID,
            Ngay_Danh_gia=datetime.now(),
            Danh_gia=rating
        )
        db.session.add(feedback)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False})


@app.route('/login', methods=['POST'])
def login():
    username, password = request.form['login'], request.form['password']
    user = models.User.query.filter_by(username=username).first()
    response = {'success': False, 'message': ''}

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        flash('Incorrect username or password. Please try again.', 'error')
        response['message'] = 'Sai tài khoản hoặc mật khẩu'
    elif user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        login_user(user)
        session['user_id'], session['username'], session['password'], session['Ho'], session['Ten'], session['Email'], \
        session['Thanh_pho'], session['Sdt'], session['user_role'] = (
            user.ID,
            user.username,
            user.password,
            user.Ho,
            user.Ten,
            user.Email,
            user.Thanh_pho,
            user.Sdt,
            user.user_role
        )
        flash('Login successful! Please reload the page.', 'success')
        response['success'] = True
        response['message'] = 'Đăng nhập thành công, hãy tải lại trang'

    return jsonify(response)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    # feedback_data = Feedback.query.all()
    # user_data = {user.ID: user.Ten for user in User.query.all()}
    # return render_template("index.html", feedback_data=feedback_data, user_data=user_data)


@app.route('/register', methods=['POST'])
def register():
    response = {'success': False, 'message': ''}
    if request.method == 'POST':
        username = request.form['login']
        raw_password = request.form['password']  # Get the raw password from the form
        email = request.form['email']
        user = models.User.query.filter_by(username=username).first()
        existing_email = models.User.query.filter_by(Email=email).first()

        if user is None and existing_email is None:
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(raw_password.encode('utf8'), bcrypt.gensalt())

            new_user = models.User(username=username, password=hashed_password, Email=email, Ho=username, Ten=username)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            response['success'] = True
            response['message'] = 'Đăng ký thành công. Bạn có thể đăng nhập'
        elif user:
            flash('Username already exists.', 'danger')
            response['message'] = 'Tên tài khoản đã tồn tại'
        elif existing_email:
            flash('Email already exists.', 'danger')
            response['message'] = 'Email đã tồn tại'
    return jsonify(response)


@app.route('/protected_route')
@login_required
def protected_route():
    # This route is only accessible to authenticated users
    return 'This is a protected route for logged-in users.'


# phần thanh toán
@app.route('/payment', methods=['POST'])
def payment():
    # Extract form data
    tour_id = request.form.get("updatedSoLuong2")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    people = request.form.get("people")
    note = request.form.get("note")
    updater = Tour.query.get(tour_id)
    total_price = updater.Tong_tien
    diadiem = DiaDiem.query.get(updater.Dia_diem_ID)
    departure = updater.Ngay_bat_dau_di
    comeback = updater.Ngay_ket_thuc

    return render_template("confirm.html", tour_id=tour_id, customer_name=name, customer_email=email,
                           customer_phone=phone, num_people=people, customer_note=note,
                           tour_name=diadiem.Ten, departure=departure, comeback=comeback,
                           total_price=total_price)


@app.route('/check_promo_code', methods=['POST'])
def check_promo_code():
    promo_code = request.get_json().get("promo_code")
    uu_dai = UuDai.query.filter_by(ma_giam_gia=promo_code).first()

    if uu_dai:
        return jsonify({"valid": True, "promo_value": uu_dai.gia_tri})
    else:
        return jsonify({"valid": False})


@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    try:
        tour_id = request.form.get("tour_id")
        num_people = request.form.get("num_people")
        total_price = request.form.get("total_price")
        customer_note = request.form.get("customer_note")
        promo_code = request.form.get("promo_code")
        recipient = request.form.get('recipient')
        message_body = request.form.get('message_body')

        total_price = float(total_price) * float(num_people)

        uu_dai = UuDai.query.filter_by(ma_giam_gia=promo_code).first()
        if uu_dai:
            promo = uu_dai.gia_tri
            total_price = float(total_price) * (1 - promo)

        if tour_id and num_people:
            tour = Tour.query.filter_by(ID=tour_id).first()
            Hoadon1 = models.HoaDon(
                Tour_ID=tour_id,
                So_tien_thanh_toan=total_price,
                UuDai_ID=uu_dai.id,
                So_luong_nguoi_di=num_people,
                khachhang_id=current_user.ID,
                Note=customer_note
            )
            tour.SoLuong -= int(num_people)
            db.session.add(Hoadon1)
            db.session.commit()

            msg = Message('Thông tin xác nhận', recipients=[recipient])
            msg.body = message_body
            mail.send(msg)

            success_message = f"Tổng tiền bạn đã thanh toán là: {total_price}."
            return jsonify({"success": True, "message": success_message})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({"success": False, "message": error_message})


@app.route("/admin")
@login_required
def admin():
    if current_user.user_role == 0:
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('index'))


# Create the database tables
with app.app_context():
    db.create_all()

# Create the admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')


# Create a ModelView for your models
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 0




@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    labels = session.get('labels', [])
    values = session.get('values', [])

    # Create a PDF
    pdf_data = generate_pdf(labels, values)

    # Send the PDF as a response
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=thongke.pdf'
    return response


def generate_pdf(labels, values):
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Set the title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Thong ke tien trong nam ")

    # Set the font for labels and values
    p.setFont("Helvetica", 12)

    # Add labels and values to the PDF
    y_position = 700  # Starting vertical position for text
    for label, value in zip(labels, values):
        # Write label and value to the PDF
        p.drawString(100, y_position, f"{label}: {value}" + " $")
        y_position -= 20  # Move down for the next line

    # Save the PDF to the buffer
    p.showPage()
    p.save()

    # Rewind the buffer for reading its content
    buffer.seek(0)

    return buffer.read()


class ThongKe(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        hoa_dons = HoaDon.query.all()
        if request.method == 'POST':
            Year = request.form.get('Year')
            records_for_desired_year = HoaDon.query.filter(extract('year', HoaDon.Ngay_thanh_toan) == Year).all()
            if records_for_desired_year:
                monthly_incomes = []

                # Calculate total income for each month
                for month in range(1, 13):
                    hoa_dons_month = [hoa_don for hoa_don in hoa_dons if hoa_don.Ngay_thanh_toan.month == month]
                    total_income_month = sum(hoa_don.So_tien_thanh_toan for hoa_don in hoa_dons_month)
                    monthly_incomes.append(total_income_month)

                data = {
                    "tháng 1": monthly_incomes[0],
                    "tháng 2": monthly_incomes[1],
                    "tháng 3": monthly_incomes[2],
                    "tháng 4": monthly_incomes[3],
                    "tháng 5": monthly_incomes[4],
                    "tháng 6": monthly_incomes[5],
                    "tháng 7": monthly_incomes[6],
                    "tháng 8": monthly_incomes[7],
                    "tháng 9": monthly_incomes[8],
                    "tháng 10": monthly_incomes[9],
                    "tháng 11": monthly_incomes[10],
                    "tháng 12": monthly_incomes[11],
                }
                labels = list(data.keys())
                values = list(data.values())
                session['labels'] = labels
                session['values'] = values
            else:
                data = {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0,
                    "11": 0,
                    "12": 0,
                }
                labels = list(data.keys())
                values = list(data.values())

        else:
            total_tour = 0
            total_income_month = 0
            labels = ["tháng", "tiền"]
            values = [total_income_month, total_tour]

        return render_template('admin/thong_ke.html', labels=json.dumps(labels), values=json.dumps(values))


class EmailView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def send_email(self):
        if request.method == 'POST':
            recipient = request.form.get('recipient')
            subject = request.form.get('subject')
            message_body = request.form.get('message_body')

            # Create an email message
            message = Message(subject=subject, recipients=[recipient])
            message.body = message_body

            try:
                mail.send(message)
                flash('Email sent successfully', 'success')
            except Exception as e:
                flash(f'Email could not be sent: {str(e)}', 'error')

        return self.render('admin/gui_mail.html')


admin.add_view(MyModelView(User, db.session, name='Users', endpoint='user', url='users'))
admin.add_view(MyModelView(DiaDiem, db.session, name='DiaDiem', endpoint='diadiem', url='diadiem'))
admin.add_view(MyModelView(Feedback, db.session, name='Feedback', endpoint='feedback', url='feedback'))
admin.add_view(MyModelView(Tour, db.session, name='Tour', endpoint='tour', url='tour'))
admin.add_view(MyModelView(HoaDon, db.session, name='HoaDon', endpoint='hoadon', url='hoadon'))
admin.add_view(MyModelView(UuDai, db.session, name='UuDai', endpoint='uudai', url='uudai'))
admin.add_view(EmailView(name='Send Email', endpoint='send_email'))
admin.add_view(ThongKe(name='Chart', endpoint='chart'))

if __name__ == "__main__":
    app.run(debug=True)
