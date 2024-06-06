import json
import webbrowser
import sinaweibopy3
import urlmid
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from wb_api import *  # 导入添加的资源（根据实际情况填写文件名）


APP_KEY = '3824822653' #微博开放平台获取
APP_SECRET = '5b73ec3fb9b61a736512e7284a39dff7'
REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)


def get_data(url):  # 'Od2l4BjmM'

    mid = urlmid.url_to_mid(url)
    result = client.comments_show(mid)


    model = QStandardItemModel(60, 5)
    model.setHorizontalHeaderLabels(['id', '昵称', '评论',  '时间',  '地域'])

    # number=result["total_number"]
    disdata = {}
    index = 0

    # 定义csv文件
    f = open('评论_api.csv', mode='w', encoding='utf-8-sig', newline='')
    csv_write = csv.writer((f))
    csv_write.writerow(['id', 'screen_name', 'text_raw', 'created_at', 'source'])

    if result["comments"]:  # 确保statuses列表不为空
        user_text = result["comments"][0]["status"]["text"]
        ui.textBrowser.setText(user_text)
        print(user_text)
        print("\n")
        num = len(result["comments"])

        model = QStandardItemModel(num, 5)
        model.setHorizontalHeaderLabels(['id', '昵称', '评论', '时间', '地域'])
        print("ok")
        for i in range(num):
            comments = result["comments"][i]  # 获取第一个微博
            user= comments["user"]  # 获取微博的用户信息

            disdata[0] = uid = user["id"] #用户id
            disdata[1] = screen_name = user["screen_name"] #用户昵称
            disdata[2] = text_raw = comments["text"] #评论信息
            disdata[3] = created_at = comments["created_at"] #发表时间
            disdata[4] = source = user["location"]  # 发表地域

            for column in range(5):
                item = QStandardItem(str(disdata[column]))
                # 设置每个位置的文本值
                model.setItem(index, column, item)

            index += 1
            print(uid, screen_name, text_raw, created_at, source)
            csv_write.writerow([uid, screen_name, text_raw, created_at, source])



        ui.tableView.setEditTriggers(QTableView.NoEditTriggers)

        ui.tableView.resize(1170, 550)
        ui.tableView.setModel(model)
        ui.tableView.setColumnWidth(0, 190)
        ui.tableView.setColumnWidth(2, 500)
        ui.tableView.setColumnWidth(3, 200)
        ui.tableView.setColumnWidth(4, 100)



def html_clicked():
    url_text = ui.lineEdit.text()[-9:]  # 获取url
    print(url_text)  # 打印

    get_data(url_text)




def Api_clicked():
    # print("test")

    url = client.get_authorize_url()
    webbrowser.open_new(url)
    #result = client.request_access_token(input("please input code: "))

    # 第三个参数表示显示类型，可选，有正常（QLineEdit.Normal）、密碼（ QLineEdit. Password）、不显示（ QLineEdit. NoEcho）三种情况
    value, ok = QInputDialog.getText(MainWindow, "输入code", "请输入code", QLineEdit.Normal)

    if ok and len(value) == 32:
        result = client.request_access_token(value)
        client.set_access_token(result.access_token, result.expires_in)
        ui.push_html.setEnabled(True)
        ui.push_Api.setEnabled(False)
        QMessageBox.question(MainWindow, '成功', '输入成功！',
                             QMessageBox.Yes)
    elif ok and len(value) != 32:
        QMessageBox.question(MainWindow, '失败', '输入错误，请重新输入！',
                             QMessageBox.Yes)

    #client.set_access_token(result.access_token, result.expires_in)





app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.push_html.setEnabled(False)


ui.push_Api.clicked.connect(Api_clicked)
ui.push_html.clicked.connect(html_clicked)
# url = 'Od2l4BjmM'


MainWindow.show()
sys.exit(app.exec_())