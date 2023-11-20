from flask import render_template, request, redirect, session, jsonify, url_for
from eduapp import app, login
import dao
from eduapp.routes.api import api
from flask_login import login_user, current_user, logout_user
from openai import OpenAI

client = OpenAI(
    api_key="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",
)


@app.route("/")
def index():
    if current_user.is_authenticated:
        pass
    else:
        return redirect(url_for('user_login'))

    user = dao.get_user_by_id(current_user.id)
    diem_user = dao.get_all_diem_by_user_id(current_user.id)
    diem_user_warning = dao.get_diem_warning_by_user_id(current_user.id)
    for d in diem_user_warning:
        print(d.user.name)
    return render_template("index.html", user=user, diem_user=diem_user, diem_user_warning=diem_user_warning)


@app.route("/course")
def course():
    return "course"


@app.route("/profile")
def profile():
    user = dao.get_info_user_by_id()

    return render_template("profile.html")


@app.route("/user_login", methods=['get', 'post'])
def user_login():
    err_msg = ''

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.check_login(username, password)

        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = 'Username hoac password k chinh xac'
    return render_template('login.html', err_msg=err_msg)


@app.route("/user_logout")
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route("/encode_qr")
def encode_qr():
    img = dao.encode_qr(current_user)
    return img


@app.route("/decode_qr")
def decode_qr():
    user = dao.decode_qr()
    if user:
        login_user(user)
        return redirect(url_for('index'))
    else:
        return "Không tìm thấy người dùng hoặc có lỗi xảy ra"


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route("/baitap_nhieudapan")
def baitap_nhieudapan():
    all_bai_tap = dao.get_all_bai_tap_nhieu_dap_an()
    print(all_bai_tap)
    return render_template("baitap_nhieudapan.html", all_bai_tap=all_bai_tap)


@app.route("/baitap_chitiet/<int:id>")
def baitap_chitiet(id):
    print(id)
    bai_tap = dao.get_bai_tap_by_id(id)
    dap_an = dao.get_dap_an_bai_tap_by_id(id)
    dap_an_dung = dao.get_dap_an_dung_bai_tap_by_id(id)
    # print(dap_an[0])
    print(dap_an_dung)
    # print(dap_an)
    # for da in dap_an:

    # print(bai_tap)
    return render_template("baitap_chitiet.html", baitapchitiet=bai_tap, dap_an=dap_an, dap_an_dung=dap_an_dung)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    # user_input = "Say hi"
    chat_response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="gpt-3.5-turbo",
    )
    
    reply = chat_response.choices[0].message.content
    print(reply)
    return jsonify({'reply': reply})

@app.route('/thongke_user')
def thongke_user():
    diem_user = dao.get_all_diem_by_user_id(current_user.id)
    diem_user_warning = dao.get_diem_warning_by_user_id(current_user.id)
    return render_template('thongke_user.html', diem_user = diem_user, diem_user_warning = diem_user_warning)


@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    from eduapp.admin import *
    app.run(debug=True, port=5050)
