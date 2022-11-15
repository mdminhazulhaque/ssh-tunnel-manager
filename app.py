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
import shutil
import time
import glob
import os
import requests

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
    ICON_WINDOW = "icons/settings.png"
    ICON_START = "icons/start.png"
    ICON_STOP = "icons/stop.png"
    ICON_SSH_KILL = "icons/kill.png"
    SSH = "ssh"
    HEADER_NAME = "Name"
    HEADER_LOCAL_ADDRESS = "Local Address"
    HEADER_REMOTE_ADDRESS = "Remote Address"
    HEADER_JUMP_HOST = "Proxy Host"
    HEADER_ACTION = "Action"
    SSH_KILL = "killall ssh"

class TunnelConfig(QDialog):
    def __init__(self, parent, data):
        super(TunnelConfig, self).__init__(parent)
        uic.loadUi("tunnelconfig.ui", self)
        
        self.remote_address.setText(data.get(LANG.REMOTE_ADDRESS))
        self.proxy_host.setText(data.get(LANG.PROXY_HOST))
        self.browser_open.setText(data.get(LANG.BROWSER_OPEN))
        self.local_port.setValue(data.get(LANG.LOCAL_PORT))
        
        self.remote_address.textChanged.connect(self.render_ssh_command)
        self.proxy_host.textChanged.connect(self.render_ssh_command)
        self.local_port.valueChanged.connect(self.render_ssh_command)
        self.copy.clicked.connect(self.do_copy_ssh_command)
        
        self.render_ssh_command()
    
    def render_ssh_command(self):
        ssh_command = F"ssh -L 127.0.0.1:{self.local_port.value()}:{self.remote_address.text()} {self.proxy_host.text()}"
        self.ssh_command.setText(ssh_command)
        
    def do_copy_ssh_command(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.ssh_command.text(), mode=cb.Clipboard)
        
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
        
        self.tunnelconfig.icon = F"./icons/{name}.png"
        
        if not os.path.exists(self.tunnelconfig.icon):
          self.tunnelconfig.icon = "./icons/robi.png"
        
        self.icon.setPixmap(QPixmap(self.tunnelconfig.icon))
        self.action_tunnel.clicked.connect(self.do_tunnel)
        self.action_settings.clicked.connect(self.tunnelconfig.show)
        self.action_open.clicked.connect(self.do_open_browser)
        
        self.process = None
        
    def do_open_browser(self):
        browser_open = self.tunnelconfig.browser_open.text()
        if browser_open:
            urlobj = urlparse(browser_open)
            local_port = self.tunnelconfig.local_port.value()
            new_url = urlobj._replace(netloc=F"{urlobj.hostname}:{local_port}").geturl()
            QDesktopServices.openUrl(QUrl(new_url))
        
    def do_tunnel(self):
        if self.process:
            self.stop_tunnel()
        else:
            self.start_tunnel()
    
    def start_tunnel(self):
        params = self.tunnelconfig.ssh_command.text().split(" ")
        
        self.process = QProcess()
        self.process.start(params[0], params[1:])
                    
        self.action_tunnel.setIcon(QIcon(LANG.ICON_STOP))
        
        self.do_open_browser()
    
    def stop_tunnel(self):
        try:
            self.process.kill()
            self.process = None
        except:
            pass
        
        self.action_tunnel.setIcon(QIcon(LANG.ICON_START))
        
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
        
        self.kill_button = QPushButton(LANG.SSH_KILL)
        self.kill_button.setIcon(QIcon(LANG.ICON_SSH_KILL))
        self.kill_button.setFocusPolicy(Qt.NoFocus)
        self.kill_button.clicked.connect(self.do_killall_ssh)
        
        self.grid.addWidget(self.kill_button, i+1, 0)
        
        self.setLayout(self.grid)
        self.resize(10, 10)
        self.setWindowTitle(LANG.TITLE)
        self.setWindowIcon(QIcon(LANG.ICON_WINDOW))
        self.show()
    
    def do_killall_ssh(self):
        for tunnel in self.tunnels:
            tunnel.stop_tunnel()
        os.system(LANG.SSH_KILL)
            
    def closeEvent(self, event):
        data = {}
        for tunnel in self.tunnels:
            name = tunnel.name.text()
            data[name] = tunnel.tunnelconfig.as_dict()
        timestamp = int(time.time())
        shutil.copy(CONF_FILE, F"{CONF_FILE}-{timestamp}")
        with open(CONF_FILE, "w") as fp:
            yaml.dump(data, fp)
        backup_configs = glob.glob(F"{CONF_FILE}-*")
        if len(backup_configs) > 10:
            for config in sorted(backup_configs, reverse=True)[10:]:
                os.remove(config)
        event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    sm = QSharedMemory("3866273d-f4d5-4bf3-b27b-772ca7915a61")
    
    if not sm.create(1):
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setText("SSH Tunnel Manager is already running")
        mb.setWindowTitle("Oops!")
        mb.setStandardButtons(QMessageBox.Close)
        mb.show()
    elif not os.path.isfile(CONF_FILE):
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setText(F"No {CONF_FILE} file found in application directory")
        mb.setWindowTitle("Oops!")
        mb.setStandardButtons(QMessageBox.Close)
        mb.show()
    else:        
        tm = TunnelManager()
            
    sys.exit(app.exec_())
