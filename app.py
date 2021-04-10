#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout, QDialog, QMessageBox
from PyQt5.QtCore import QProcess, Qt, QUrl, QSharedMemory
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5 import uic
import sys
import yaml
from urllib.parse import urlparse

CONF_FILE = "config.yml"

class LANG:
    TITLE = "SSH Tunnel Manager"
    START = "Start"
    STOP = "Stop"
    ADD = "Add"
    CLOSE = "Close"
    QSS_START = "QPushButton { background-color: #34A853; }"
    QSS_STOP = "QPushButton { background-color: #EA4335; }"
    QSS_OPEN = "QPushButton { background-color: #4285F4; }"
    REMOTE_ADDRESS = "remote_address"
    LOCAL_PORT = "local_port"
    PROXY_HOST = "proxy_host"
    BROWSER_OPEN = "browser_open"
    ICON = "icon"
    ICON_WINDOW = "network-vpn"
    ICON_START = "kt-start"
    ICON_STOP = "kt-stop"
    ICON_HIDE = "gnumeric-column-hide"
    ICON_UNHIDE = "gnumeric-column-unhide"
    SSH = "ssh"
    HEADER_NAME = "Name"
    HEADER_LOCAL_ADDRESS = "Local Address"
    HEADER_REMOTE_ADDRESS = "Remote Address"
    HEADER_JUMP_HOST = "Proxy Host"
    HEADER_ACTION = "Action"
    
class TunnelConfig(QDialog):
    def __init__(self, parent, data):
        super(TunnelConfig, self).__init__(parent)
        uic.loadUi("tunnelconfig.ui", self)
        
        self.remote_address.setText(data.get(LANG.REMOTE_ADDRESS))
        self.proxy_host.setText(data.get(LANG.PROXY_HOST))
        self.browser_open.setText(data.get(LANG.BROWSER_OPEN))
        self.local_port.setValue(data.get(LANG.LOCAL_PORT))
        
    def as_dict(self):
        return {
            LANG.REMOTE_ADDRESS: self.remote_address.text(),
            LANG.PROXY_HOST: self.proxy_host.text(),
            LANG.BROWSER_OPEN: self.browser_open.text(),
            LANG.LOCAL_PORT: self.local_port.value(),
        }
        
class Tunnel(QWidget):
    def __init__(self, name, data):
        super(Tunnel, self).__init__()
        uic.loadUi("tunnel.ui", self)
        
        self.tunnelconfig = TunnelConfig(self, data)
        self.tunnelconfig.setWindowTitle(name)
        self.tunnelconfig.setModal(True)
        self.name.setText(name)
        self.icon.setPixmap(QPixmap("./icons/"+name))
        
        self.action_tunnel.clicked.connect(self.do_tunnel)
        self.action_settings.clicked.connect(self.tunnelconfig.show)
        self.action_open.clicked.connect(self.do_open_browser)
        self.action_tunnel.setStyleSheet(LANG.QSS_START)
        
        self.process = None
        
    def do_open_browser(self):
        browser_open = self.tunnelconfig.browser_open.text()
        if browser_open:
            urlobj = urlparse(browser_open)
            local_port = self.tunnelconfig.local_port.value()
            new_url = urlobj._replace(netloc=F"{urlobj.hostname}:{local_port}").geturl()
            QDesktopServices.openUrl(QUrl(new_url))
        
    def do_tunnel(self):
        local_port = self.tunnelconfig.local_port.value()
        remote_address = self.tunnelconfig.remote_address.text()
        proxy_host = self.tunnelconfig.proxy_host.text()
        browser_open = self.tunnelconfig.browser_open.text()
        
        if self.process == None:
            param = ["-L", F"127.0.0.1:{local_port}:{remote_address}", proxy_host]
            
            self.process = QProcess()
            self.process.start(LANG.SSH, param)
            
            self.action_tunnel.setStyleSheet(LANG.QSS_STOP)
            self.action_tunnel.setIcon(QIcon.fromTheme(LANG.ICON_STOP))
            
            self.do_open_browser()
        else:
            self.process.kill()
            self.process.close()
            self.process = None
            
            self.action_tunnel.setIcon(QIcon.fromTheme(LANG.ICON_START))
            self.action_tunnel.setStyleSheet(LANG.QSS_START)

class TunnelManager(QWidget):
    def __init__(self):
        super().__init__()
        
        with open(CONF_FILE, "r") as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)
            
        self.grid = QGridLayout(self)
        self.tunnels = []
        
        for i, name in enumerate(data):
            tunnel = Tunnel(name, data[name])
            self.tunnels.append(tunnel)
            self.grid.addWidget(tunnel, i, 0)
        
        self.setLayout(self.grid)
        self.resize(300, 100)
        self.setWindowTitle(LANG.TITLE)
        self.setWindowIcon(QIcon.fromTheme(LANG.ICON_WINDOW))
        self.show()
    
    def closeEvent(self, event):
        data = {}
        for tunnel in self.tunnels:
            name = tunnel.name.text()
            data[name] = tunnel.tunnelconfig.as_dict()
        with open(CONF_FILE, "w") as fp:
            yaml.dump(data, fp)
        event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    sm = QSharedMemory("3866273d-f4d5-4bf3-b27b-772ca7915a61")
    
    if not sm.create(1):
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setText("SSH Tunnel Manager is already running")
        mb.setWindowTitle("Oops!")
        mb.setStandardButtons(QMessageBox.Ok)
        mb.show()
    else:
        tm = TunnelManager()
    
    sys.exit(app.exec_())
