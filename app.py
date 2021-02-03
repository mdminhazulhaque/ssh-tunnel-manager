#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout
from PyQt5.QtCore import QProcess, Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
import sys
import json

try:
    with open("config.json") as fp:
        HOSTS = json.load(fp)
except:
    sys.stderr.write("Error loading config.json\n")
    exit(1)

class STRINGS:
    TITLE = "SSH Tunnel Manager"
    START = "Start"
    STOP = "Stop"
    
    QSS_START = "QPushButton { background-color: #5cb85c; }"
    QSS_STOP = "QPushButton { background-color: #d43f3a; }"
    
    LOCAL_ADDRESS = "local_address"
    REMOTE_ADDRESS = "remote_address"
    PROXY_HOST = "proxy_host"
    BROWSER_OPEN = "browser_open"
    
    ICON_WINDOW = "network-vpn"
    ICON_START = "kt-start"
    ICON_STOP = "kt-stop"
    
    SSH_PATH = "/usr/bin/ssh"
    
    HEADER_NAME = "Name"
    HEADER_LOCAL_ADDRESS = "Local Address"
    HEADER_REMOTE_ADDRESS = "Remote Address"
    HEADER_JUMP_HOST = "Proxy Host"
    HEADER_ACTION = "Action"
    
class TunnelManager(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
                
    def initUI(self):
        self.grid = QGridLayout(self)
        
        self.grid.addWidget(QLabel(STRINGS.HEADER_NAME), 0, 0)
        self.grid.addWidget(QLabel(STRINGS.HEADER_LOCAL_ADDRESS), 0, 1)
        self.grid.addWidget(QLabel(STRINGS.HEADER_REMOTE_ADDRESS), 0, 2)
        self.grid.addWidget(QLabel(STRINGS.HEADER_JUMP_HOST), 0, 3)
        self.grid.addWidget(QLabel(STRINGS.HEADER_ACTION), 0, 4)
        
        for i, host in enumerate(HOSTS):
            tunnel_info = HOSTS[host]
            name = QLabel(host)
            
            proxy_host = QLineEdit(tunnel_info[STRINGS.PROXY_HOST])
            proxy_host.setDisabled(True)
            
            remote_address = QLineEdit(tunnel_info[STRINGS.REMOTE_ADDRESS])
            remote_address.setDisabled(True)
            
            local_address = QLineEdit(tunnel_info[STRINGS.LOCAL_ADDRESS])
            local_address.setDisabled(True)
            
            action = QPushButton(STRINGS.START)
            action.setStyleSheet(STRINGS.QSS_START)
            action.setIcon(QIcon.fromTheme(STRINGS.ICON_START))
            action.clicked.connect(self.do_tunnel)
            
            self.grid.addWidget(name, i+1, 0)
            self.grid.addWidget(local_address, i+1, 1)
            self.grid.addWidget(remote_address, i+1, 2)
            self.grid.addWidget(proxy_host, i+1, 3)
            self.grid.addWidget(action, i+1, 4)
        
        self.setLayout(self.grid)
        self.resize(650, 100)
        self.setWindowTitle(STRINGS.TITLE)
        self.setWindowIcon(QIcon.fromTheme(STRINGS.ICON_WINDOW))
        self.show()
        
        self.tunnels = {}
        
    def do_tunnel(self):
        button = self.sender()
        idx = self.grid.indexOf(button)
        row, _, _, _ = self.grid.getItemPosition(idx)
        
        name = self.grid.itemAtPosition(row, 0).widget().text()
        tunnel_info = HOSTS[name]
        
        local_address = tunnel_info[STRINGS.LOCAL_ADDRESS]
        remote_address = tunnel_info[STRINGS.REMOTE_ADDRESS]
        proxy_host = tunnel_info[STRINGS.PROXY_HOST]
        
        action = button.text()
        
        if action == STRINGS.START:
            process = QProcess()
            process.start(
                STRINGS.SSH_PATH,
                ["-L", F"{local_address}:{remote_address}", proxy_host]
            )
            self.tunnels[name] = process
            
            button.setText(STRINGS.STOP)
            button.setStyleSheet(STRINGS.QSS_STOP)
            button.setIcon(QIcon.fromTheme(STRINGS.ICON_STOP))
            
            url = tunnel_info.get(STRINGS.BROWSER_OPEN)
            if url:
                QDesktopServices.openUrl(QUrl(url))
        elif action == STRINGS.STOP:
            process = self.tunnels[name]
            process.kill()
            process.close()
            del self.tunnels[name]
            
            button.setText(STRINGS.START)
            button.setStyleSheet(STRINGS.QSS_START)
            button.setIcon(QIcon.fromTheme(STRINGS.ICON_START))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TunnelManager()
    sys.exit(app.exec_())
