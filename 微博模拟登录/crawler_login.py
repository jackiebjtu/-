from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from wb_login import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

def login(base_url):
    driver = webdriver.Chrome()
    driver.get(base_url)
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, 200)')  # 遇见了反爬行为，通过滚动页面对抗

    time.sleep(5)

    ui.textBrowser.setText("正在进行微博登录网页打开")

    driver.find_element(By.CSS_SELECTOR, "a span.hidden.md\\:inline").click()


    phone = ui.lineEdit.text()
    # 定位手机号输入框
    phone_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='手机号']")
    verification_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='验证码']")
    get_code_link = driver.find_element(By.XPATH, "//a[text()='获取验证码']")

    ui.textBrowser.setText("请手动获取验证码")

    phone_input.send_keys(phone)
    time.sleep(3)
    # get_code_link.click()

    # get_code_link.click()

    verification, ok = QInputDialog.getText(MainWindow, "输入验证码", "请输入获取到的验证码", QLineEdit.Normal)


    verification_input.send_keys(verification)
    # driver.find_element_by_xpath("//input[@type='text']").send_keys(phone)
    time.sleep(1)
    # driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
    time.sleep(1)
    # 点击登录

    time.sleep(3)
    cookies = driver.get_cookies()  # 获取cookie,列表形./式
    f1 = open('cookies.txt', 'w')
    f1.write(json.dumps(cookies))
    f1.close()
    # driver.close()
    QMessageBox.question(MainWindow, '成功', '登录成功！',
                         QMessageBox.Ok)

if __name__ == '__main__':
    # 模拟登陆-给定登陆的网址
    base_url = "https://passport.weibo.cn/signin/login"
    # login(base_url)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.pushButton.clicked.connect(lambda: login(base_url))

    MainWindow.show()
    sys.exit(app.exec_())

    # print("新浪微博登陆成功！")
