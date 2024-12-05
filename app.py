# sudo apt-get install -y python3-flask-login

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets

app = Flask(__name__)

# 设置密码
password = "123456789"

# 定义路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buttons', methods=['POST'])
def buttons():
    # 获取输入的密码
    entered_password = request.form['password']

    # 验证密码
    if entered_password == password:
        user = User()
        user.id = 1  # 假設只有一個用戶
        login_user(user)
        return render_template('buttons.html')
    else:
        return redirect(url_for('index'))


#######################################
######### 導入 登入模組 START #########
#######################################
class User(UserMixin):
    pass

app.config['SECRET_KEY'] = secrets.token_hex(48)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user
#######################################
######### 導入 登入模組 END #########
#######################################

#######################################
######### 導入嵌入式模組 START #########
#######################################
import RPi.GPIO as GPIO
import time
# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
# 定义使用的GPIO引脚
pin_number_17 = 17   
pin_number_18 = 18  
pin_number_27 = 27  
pin_number_22 = 22 
# 设置引脚为输出模式
GPIO.setup(pin_number_17, GPIO.OUT)
GPIO.setup(pin_number_18, GPIO.OUT)
GPIO.setup(pin_number_27, GPIO.OUT)
GPIO.setup(pin_number_22, GPIO.OUT)

# 设置初始状态为高电位，代表断路
GPIO.output(pin_number_17, GPIO.HIGH)
GPIO.output(pin_number_18, GPIO.HIGH)
GPIO.output(pin_number_27, GPIO.HIGH)
GPIO.output(pin_number_22, GPIO.HIGH)
# 定义GPIO控制函数
def open():
    GPIO.output(pin_number_18, GPIO.LOW)
    print("open - running...")
    time.sleep(1)
    GPIO.output(pin_number_18, GPIO.HIGH)
    time.sleep(1)
def lock():
    GPIO.output(pin_number_22, GPIO.LOW)
    print("lock - running...")
    time.sleep(1)
    GPIO.output(pin_number_22, GPIO.HIGH)
    time.sleep(1)
def up():
    GPIO.output(pin_number_17, GPIO.LOW)
    print("up - running...")
    time.sleep(1)
    GPIO.output(pin_number_17, GPIO.HIGH)
    time.sleep(1)
def down():
    GPIO.output(pin_number_27, GPIO.LOW)
    print("down - running...")
    time.sleep(1)
    GPIO.output(pin_number_27, GPIO.HIGH)
    time.sleep(1)


@app.route('/button_open')
@login_required
def button_open():
    print("open - running... (web) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    open()
    return render_template('buttons.html')

@app.route('/button_lock')
@login_required
def button_lock():
    print("lock - running... (web) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    lock()
    return render_template('buttons.html')

@app.route('/button_up')
@login_required
def button_up():
    print("up - running... (up) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    up()
    return render_template('buttons.html')

@app.route('/button_down')
@login_required
def button_down():
    print("down - running... (down) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    down()
    return render_template('buttons.html')

#######################################
######### 導入嵌入式模組  END ##########
#######################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
