# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyMusicknbBcg.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
package = "com.pts.music"
import os

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
import sys
from pygame import mixer
from tinytag import TinyTag
mixer.init()
playList = []

nowMusic = 0

class Ui_MainWindow(object):
    playing = False
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(371, 410)
        MainWindow.setWindowFlags(Qt.WindowMinimizeButtonHint)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 20, 371, 41))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 60, 31, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(170, 60, 211, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(140, 80, 31, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(170, 80, 211, 16))
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 220, 351, 181))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(150, 140, 75, 24))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(60, 140, 75, 24))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(230, 140, 75, 24))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(60, 170, 31, 16))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(100, 170, 160, 18))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setValue(10)
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(80, 190, 75, 24))
        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(160, 190, 75, 24))
        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(290, 0, 75, 24))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 194, 55, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_7.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_7.clicked.connect(MainWindow.close)
        self.pushButton_5.clicked.connect(self.playList)
        self.listWidget.itemClicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.pause)
        self.pushButton_4.clicked.connect(self.nextMusic)
        self.pushButton_3.clicked.connect(self.previous)
        self.horizontalSlider.valueChanged.connect(self.changeVolume)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def playList(self):
        self.listWidget.clear()
        global playList, reply
        import easygui as g
        reply = g.diropenbox()
        fileList = os.listdir(reply)
        for i in fileList:
            if ".mp3" in i :
                music = i
                playList.append(music)
        self.listWidget.addItems(playList)


    def play(self, item):
        global nowMusic, playing
        item2 = item.text()
        mixer.music.load(reply + "\\" +item2)
        mixer.music.play(1, 0)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"| |", None))
        nowMusic = int(playList.index(item2))
        playing = True
        tag = TinyTag.get(reply + "\\" + item2)
        self.label.setText(QCoreApplication.translate("MainWindow", tag.title, None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", tag.album, None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", tag.artist, None))

    def pause(self):
        global playing
        if playing:
            mixer.music.pause()
            playing = False
            self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"▶", None))
        elif not playing:
            mixer.music.unpause()
            playing = True
            self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"| |", None))

    def nextMusic(self):
        global nowMusic
        try:
            nextMusic = playList[nowMusic + 1]
            mixer.music.stop()
            mixer.music.load(reply + "\\" + nextMusic)
            mixer.music.play(1, 0)
            tag = TinyTag.get(reply + "\\" + nextMusic)
            self.label.setText(QCoreApplication.translate("MainWindow", tag.title, None))
            self.label_3.setText(QCoreApplication.translate("MainWindow", tag.album, None))
            self.label_5.setText(QCoreApplication.translate("MainWindow", tag.artist, None))
            indexMu = playList.index(nextMusic)
            nowMusic += 1
        except:
            os.system("python.exe ../Application/" + package + "/tip.py")

    def previous(self):
        global nowMusic
        previous = playList[nowMusic - 1]
        mixer.music.stop()
        mixer.music.load(reply + "\\" + previous)
        mixer.music.play(1, 0)
        tag = TinyTag.get(reply + "\\" + previous)
        self.label.setText(QCoreApplication.translate("MainWindow", tag.title, None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", tag.album, None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", tag.artist, None))
        indexMu = playList.index(previous)
        nowMusic -= 1

    def changeVolume(self):
        Volume = self.horizontalSlider.value()
        volume = float(Volume)
        vol = volume / 10
        mixer.music.set_volume(vol)



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyMusic Player", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u672a\u64ad\u653e\u97f3\u4e50", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4e13\u8f91\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u672a\u64ad\u653e\u97f3\u4e50", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6b4c\u624b\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u672a\u64ad\u653e\u97f3\u4e50", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"▶", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u91cf\uff1a", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u97f3\u4e50", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"X  \u9000\u51fa", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u64ad\u653e\u5217\u8868", None))
    # retranslateUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
