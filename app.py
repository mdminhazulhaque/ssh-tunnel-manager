#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout
from PyQt5.QtCore import QProcess, Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5 import uic
import sys
import json

class LANG:
    TITLE = "SSH Tunnel Manager"
    START = "Start"
    STOP = "Stop"
    ADD = "Add"
    CLOSE = "Close"
    QSS_START = "QPushButton { background-color: #5cb85c; }"
    QSS_STOP = "QPushButton { background-color: #d43f3a; }"
    REMOTE_ADDRESS = "remote_address"
    LOCAL_PORT = "local_port"
    PROXY_HOST = "proxy_host"
    BROWSER_OPEN = "browser_open"
    ICON = "icon"
    ICON_WINDOW = "network-vpn"
    ICON_START = "kt-start"
    ICON_STOP = "kt-stop"
    SSH = "ssh"
    HEADER_NAME = "Name"
    HEADER_LOCAL_ADDRESS = "Local Address"
    HEADER_REMOTE_ADDRESS = "Remote Address"
    HEADER_JUMP_HOST = "Proxy Host"
    HEADER_ACTION = "Action"
    
class Tunnel(QWidget):
    def __init__(self, name, data):
        super(Tunnel, self).__init__()
        uic.loadUi("tunnel.ui", self)
        
        self.name.setText(name)
        self.icon.setPixmap(QPixmap("./icons/"+name))
        self.remote_address.setText(data[LANG.REMOTE_ADDRESS])
        self.proxy_host.setText(data[LANG.PROXY_HOST])
        self.browser_open.setText(data[LANG.BROWSER_OPEN])
        self.local_port.setValue(data[LANG.LOCAL_PORT])
        
        self.action.clicked.connect(self.do_tunnel)
        self.action.setStyleSheet(LANG.QSS_START)
        self.proxy_host.setHidden(True)
        
    def do_tunnel(self):
        local_port = self.local_port.value()
        remote_address = self.remote_address.text()
        proxy_host = self.proxy_host.text()
        
        if self.action.text() == LANG.START:
            param = ["-L", F"127.0.0.1:{local_port}:{remote_address}", proxy_host]            
            
            self.process = QProcess()
            self.process.start(LANG.SSH, param)
            
            self.action.setText(LANG.STOP)
            self.action.setStyleSheet(LANG.QSS_STOP)
            
            if self.browser_open.text().startswith("http"):
                QDesktopServices.openUrl(QUrl(self.browser_open.text()))
        else:
            self.process.kill()
            self.process.close()
            
            self.action.setText(LANG.START)
            self.action.setStyleSheet(LANG.QSS_START)

class TunnelManager(QWidget):
    def __init__(self):
        super().__init__()
        
        with open("config.json", "r") as fp:
            data = json.load(fp)
            
        self.grid = QGridLayout(self)
        self.tunnels = []
        
        for i, name in enumerate(data):
            tunnel = Tunnel(name, data[name])
            self.tunnels.append(tunnel)
            self.grid.addWidget(tunnel, i, 0)
        
        self.setLayout(self.grid)
        self.resize(700, 100)
        self.setWindowTitle(LANG.TITLE)
        self.setWindowIcon(QIcon.fromTheme(LANG.ICON_WINDOW))
        self.show()
        
    #def closeEvent(self, event):
        #data = {}
        #for tunnel in self.tunnels:
            #name = tunnel.name.text()
            #data[name] = {
                #LANG.REMOTE_ADDRESS: tunnel.remote_address.text(),
                #LANG.PROXY_HOST: tunnel.proxy_host.text(),
                #LANG.LOCAL_PORT: tunnel.local_port.value(),
                #LANG.BROWSER_OPEN: tunnel.browser_open.text()
            #}
        #print(json.dumps(data, indent=2))
        #with open("config.json", "w") as fp:
            #json.dumps(data, fp)
        #event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TunnelManager()
    sys.exit(app.exec_())
