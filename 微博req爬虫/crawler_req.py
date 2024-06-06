import requests
import csv
import my_sqlite
from wb_req import *
import sys
import urlmid
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 定义请求头
headers = {
    # 用户身份信息，替换成自己的cookie
    'cookie': 'SINAGLOBAL=7410687713922.781.1715180541191; ULV=1715180541193:1:1:1:7410687713922.781.1715180541191:; SCF=Ag7TT-7tbojNUPXpeqnt8IPzcA4D8dKOj7K7TaKsrUVpNHiyiurgw0rCRIK_c1J9orvWH5QfYFwUsmzI7xGMBtk.; SUB=_2A25LOkJiDeRhGeNM6lMQ8yzJyDiIHXVoNtuqrDV8PUNbmtANLRbmkW9NTlVTnmvNdGCp-tNlIL9FB80W_s5O58Yq; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5g9ADDq1g8W-4JG.I_-l4G5JpX5KMhUgL.Fo-EeK2pe0zfe0B2dJLoI7LCqgL09-vV9KMt; ALF=1717944114; PC_TOKEN=8333a9048f; XSRF-TOKEN=Tm5_FFiowM3DbT-7AXLNlHAH; WBPSESS=Fxl-soFz_YTW2JsuQ04-SXfw4KfeHWHXRqUzHnRfmZ2OoWJXIa9pJG1kviOais-RhjBEljS3VZPsdv1gmhc1Gy4hjOfAUa-5P4X7TirIkwRNxTGYEmzYcgLIQN9PUOfhcH_N2mUUz4DW77VEvtfcRw==',
    # 防盗链
    'referer': 'https://weibo.com/u/5211132534/home?wvr=5',
    # 浏览器基本信息
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}


def req_html():

    ui.findButton.setEnabled(True)
    ui.deleteButton.setEnabled(True)

    html = ui.lineEdit.text()
    url = html[-9:]
    mid = urlmid.url_to_mid(url)
    print(mid)

    model = QStandardItemModel(60, 7)
    model.setHorizontalHeaderLabels(['id', '昵称', '评论', '地域', '时间', '跟评', '点赞'])

    next = 'count=10'
    disdata = {}
    index = 0

    # 定义csv文件
    f = open('评论_req.csv', mode='w', encoding='utf-8-sig', newline='')
    csv_write = csv.writer((f))
    csv_write.writerow(['id', 'screen_name', 'text_raw', 'like_counts', 'total_number', 'created_at', 'source'])

    for i in range(2):
        url = (
            f'https://www.weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={str(mid)}&is_show_bulletin=2&is_mix=0&{next}&uid=2803301701&fetch_level=0&locale=zh-CN'
        )
        response = requests.get(url=url, headers=headers)

        json_data = response.json()

        data_list = json_data['data']
        max_id = json_data['max_id']  # 这里是单独获取这个分页的max_id

        for data in data_list:
            disdata[0] = uid = data['id']  # 发表评论人的id
            disdata[1] = screen_name = data['user']['screen_name']  # 评论人的昵称
            disdata[2] = text_raw = data['text_raw']  # 评论文字
            disdata[3] = source = data['source']  # 发表地域
            disdata[4] = created_at = data['created_at']  # 发表时间
            disdata[5] = total_number = data['total_number']  # 跟评数量
            disdata[6] = like_counts = data['like_counts']  # 该评论的点赞数量

            for column in range(7):
                item = QStandardItem(str(disdata[column]))
                # 设置每个位置的文本值
                model.setItem(index, column, item)

            index += 1
            print(uid, screen_name, text_raw, like_counts, total_number, created_at, source)
            csv_write.writerow([uid, screen_name, text_raw, like_counts, total_number, created_at, source])
            my_sqlite.insertdata(data,'wb_req.db')

        ui.tableView.setEditTriggers(QTableView.NoEditTriggers)

        ui.tableView.resize(1170, 621)
        ui.tableView.setModel(model)
        ui.tableView.setColumnWidth(0, 200)
        ui.tableView.setColumnWidth(2, 400)
        ui.tableView.setColumnWidth(3, 80)
        ui.tableView.setColumnWidth(4, 200)
        ui.tableView.setColumnWidth(5, 50)
        ui.tableView.setColumnWidth(6, 50)

        next = 'max_id=' + str(max_id)

    f.close()


def find_data():

    uid, ok = QInputDialog.getText(MainWindow, "输入uid", "请输入要查找的uid", QLineEdit.Normal)

    ok, result = my_sqlite.finddata(uid,'wb_req.db')

    model = QStandardItemModel()  # 重新实例化一个空模型
    ui.FindtableView.setModel(model)  # 将新模型设置到视图上

    if ok and result != 0 :
        result = list(result[0])
        print(result)
        temp1, temp2 = result[3], result[4]
        result[3], result[4] = result[6], result[5]
        result[6], result[5] = temp1, temp2

        QMessageBox.question(MainWindow, '成功',
                             '查找成功！',
                             QMessageBox.Yes)

        model = QStandardItemModel(1, 7)
        model.setHorizontalHeaderLabels(['id', '昵称', '评论', '地域', '时间', '跟评', '点赞'])

        for column in range(7):
            item = QStandardItem(str(result[column]))
            # 设置每个位置的文本值
            model.setItem(0, column, item)

        ui.FindtableView.setEditTriggers(QTableView.NoEditTriggers)
        ui.FindtableView.setModel(model)
        ui.FindtableView.setColumnWidth(0, 200)
        ui.FindtableView.setColumnWidth(2, 400)
        ui.FindtableView.setColumnWidth(3, 80)
        ui.FindtableView.setColumnWidth(4, 200)
        ui.FindtableView.setColumnWidth(5, 50)
        ui.FindtableView.setColumnWidth(6, 50)

    else:
        QMessageBox.question(MainWindow, '失败', '查找失败，未找到对应数据！',
                             QMessageBox.No)


def delete_data():
    #my_sqlite.showdata('wb_req.db')
    #value, ok = QInputDialog.getText(MainWindow, "输入code", "请输入code", QLineEdit.Normal)
    uid, ok = QInputDialog.getText(MainWindow, "输入uid", "请输入要删除的uid", QLineEdit.Normal)

    ok = my_sqlite.deletedata(uid,'wb_req.db')

    if ok:
        QMessageBox.question(MainWindow, '成功', '删除成功！',
                             QMessageBox.No)
    else:
        QMessageBox.question(MainWindow, '失败', '删除失败，未找到对应数据！',
                             QMessageBox.No)




app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

my_sqlite.createdatabase('wb_req.db')
my_sqlite.erasealldata('wb_req.db')

ui.findButton.setEnabled(False)
ui.deleteButton.setEnabled(False)

ui.pushButton.clicked.connect(req_html)
ui.findButton.clicked.connect(find_data)
ui.deleteButton.clicked.connect(delete_data)

MainWindow.show()
sys.exit(app.exec_())






