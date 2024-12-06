from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from demo import Ui_MainWindow
import requests
import sys

class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化播放器
        #self.player = QMediaPlayer(self)
        # 设置播放器的视频输出widget
        #self.player.setVideoOutput(self.wgt_video)
        # 播放器
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.wgt_video)
        # 连接按钮
        self.btn_open.clicked.connect(self.openVideo)  # 打开视频按钮
        self.btn_close.clicked.connect(self.closeVideo)  # 关闭视频流按钮
        self.btn_play.clicked.connect(self.playVideo)  # 播放
        self.btn_stop.clicked.connect(self.pauseVideo)  # 暂停
        self.btn_up.clicked.connect(self.moveUp)  # 上移云台
        self.btn_down.clicked.connect(self.moveDown)  # 下移云台
        self.btn_left.clicked.connect(self.moveLeft)  # 左移云台
        self.btn_right.clicked.connect(self.moveRight)  # 右移云台
        self.btn_zoomin.clicked.connect(self.zoomIn)  # 放大画面
        self.btn_zoomout.clicked.connect(self.zoomOut)  # 缩小画面
        # 摄像头控制参数（可根据实际设备调整）
        self.access_token = ""#输入你的萤石云token
        self.device_serial = ""#输入你的萤石云device
        self.access_url = "ezopen://open.ys7.com/your_device_serial/1.live"#更改为你的萤石云device
        # 创建一个 QGraphicsScene 和 QGraphicsView 用来管理和缩放视频
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setScene(self.scene)
        self.view.setGeometry(100, 30, 611, 411)  # 设置位置和大小
        self.scene.addWidget(self.wgt_video)  # 将 video widget 添加到场景中
        # 设置缩放的初始比例
        self.zoom_factor = 1.0
        self.min_zoom_factor = 0.3  # 最小缩放限制
        self.max_zoom_factor = 1.0  # 最大缩放限制
        # 保存原始视频显示矩形区域
        self.original_rect = self.wgt_video.geometry()

    def openVideo(self):
        """ 打开视频流文件 """
        if self.player is None:
            self.closeVideo()
        # 固定的 RTSP 地址
        rtsp_url = "RTSP://admin:your_verifycode@192.168.your_ip:your_rtsp/live.sdp"
        # 使用固定的 RTSP 流 URL 设置视频源
        media = QMediaContent(QUrl(rtsp_url))
        self.player.setMedia(media)  # 使用 QUrl 对象加载 RTSP 流
        self.player.play()  # 播放视频流

    def closeVideo(self):
        """关闭视频流"""
        self.player.stop()  # 停止播放
        self.player.setMedia(None)  # 清空媒体内容
        self.player.deleteLater()  # 释放播放器资源
        # 设置黑屏背景
        self.wgt_video.setStyleSheet("background-color: black;")

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()

    # 云台控制方法
    def moveUp(self):
        self.controlPTZ(0)  # 上移
        self.stopPTZ()
    def moveDown(self):
        self.controlPTZ(1)  # 下移
        self.stopPTZ()
    def moveLeft(self):
        self.controlPTZ(2)  # 左移
        self.stopPTZ()
    def moveRight(self):
        self.controlPTZ(3)  # 右移
        self.stopPTZ()

    def controlPTZ(self, direction):
        """ 控制云台移动的函数 """
        url = "https://open.ys7.com/api/lapp/device/ptz/start"
        params = {
            'accessToken': self.access_token,
            'speed': 2,  # 旋转速度
            'direction': direction,  # 云台方向（0: 上, 1: 下, 2: 左, 3: 右）
            'channelNo': 1,
            'deviceSerial': self.device_serial
        }

        try:
            response = requests.post(url, params=params, timeout=2)
            response_data = response.json()
            if response_data.get('code') == '60000':
                print(f"INFO: {response_data.get('msg')}")
            else:
                print(f"INFO: {response_data.get('msg')}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


    def stopPTZ(self):
        url = "https://open.ys7.com/api/lapp/device/ptz/stop"
        params = {
            'accessToken': self.access_token,
            'channelNo': 1,
            'deviceSerial': self.device_serial
        }

        try:
            response = requests.post(url, params=params, timeout=2)
            response_data = response.json()
            if response_data.get('code') == '200':
                print(f"INFO: {response_data.get('msg')}")
            else:
                print(f"INFO: {response_data.get('msg')}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # 电子缩放功能
    def zoomIn(self):
        """ 放大画面 """
        self.zoom_factor /= 1.2  # 每次放大 20%
        if self.zoom_factor < self.min_zoom_factor:
            self.zoom_factor = self.min_zoom_factor
        self.applyZoom()

    def zoomOut(self):
        """ 缩小画面 """
        self.zoom_factor *= 1.2  # 每次缩小 20%
        if self.zoom_factor > self.max_zoom_factor:
            self.zoom_factor = self.max_zoom_factor
        self.applyZoom()

    def applyZoom(self):
        """ 实现局部放大的逻辑 """
        # 获取当前视频显示的几何区域
        rect = self.original_rect

        # 计算新的缩放矩形区域
        center_x = rect.center().x()
        center_y = rect.center().y()
        new_width = int(rect.width() / self.zoom_factor)
        new_height = int(rect.height() / self.zoom_factor)

        # 创建新的几何区域
        new_rect = QRect(center_x - new_width // 2, center_y - new_height // 2, new_width, new_height)

        # 直接更新视频控件的几何位置，而不是更新场景
        self.wgt_video.setGeometry(new_rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_gui = myMainWindow()
    video_gui.show()
    sys.exit(app.exec_())