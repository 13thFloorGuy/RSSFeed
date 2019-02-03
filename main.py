import sys
import time
import feedparser
from threading import Thread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *


feed_dict = dict()

class Window(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'RSSFeeder'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 120
        self.feed_container_list = list()
        self.feed_container_list.append(FeedContainer("YT", "Youtube"))
        self.feed_container_list.append(FeedContainer("IZ*ONE Reddit", "Reddit - IZ*ONE"))
        self.label_lastUpdate = QtWidgets.QLabel("------")
        self.initUI()
        self.get_thread = FeederThread(self)
        self.get_thread.start()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedWidth(self.width)
        self.initWidget()
        self.show()

    def initWidget(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        self.setLabel()

        for feed_container in self.feed_container_list:
            layout.addWidget(feed_container.label_name)
            layout.addWidget(feed_container.label_title)
            layout.addWidget(feed_container.label_link)

        layout.addWidget(self.label_lastUpdate)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setLabel(self):
        for feed_container in self.feed_container_list:
            feed_container.updateLabel()

        self.label_lastUpdate.setText("Last Update : " + str(feed_dict.get("TIME")))

    def link(self, linkStr):
        QDesktopServices.openUrl(QtCore.QUrl(linkStr))

class FeedContainer:
    
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.label_name = QtWidgets.QLabel("------")
        self.label_title = QtWidgets.QLabel("------")
        self.label_link = QtWidgets.QLabel("------")
        self.label_link.linkActivated.connect(self.link)

    def updateLabel(self):
        feed = feed_dict.get(self.key)
        if feed != None:
            self.label_name.setText("# " + self.name + " ( by " + feed.author + " )")
            self.label_title.setText("| Title : " + feed.title)
            self.label_link.setText("| Link : " + '<a href="' + str(feed.link) + '">' + str(feed.link) + '</a>')
        else:
            self.label_name.setText("# -")
            self.label_title.setText("| Title : -")
            self.label_link.setText("| Link : -")

    def link(self, linkStr):
        QDesktopServices.openUrl(QtCore.QUrl(linkStr))


class FeederThread(QtCore.QThread):
    
    trigger = QtCore.pyqtSignal()

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.trigger.connect(window.setLabel)

    def __del__(self):
        self.wait()

    def run(self):
        i = 0
        while True:

            # get Youtube's feed
            feed_dict["YT"] = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCvqRdlKsE5Q8mf8YXbdIJLw").entries[0]
            feed_dict["IZ*ONE Reddit"] = feedparser.parse("https://www.reddit.com/r/iZone/.rss").entries[0]

            feed_dict["TIME"] = time.ctime()
            i += 1

            # emit the signal
            self.trigger.emit()
            
            # delay loop
            self.sleep(60)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # app.setQuitOnLastWindowClosed(False)

    icon = QIcon("icon.png")

    tray = QtWidgets.QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QtWidgets.QMenu()
    action_open = QtWidgets.QAction("Open")
    menu.addAction(action_open)

    tray.setContextMenu(menu)

    window = Window()
    app.exec_()
