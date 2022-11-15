#!/usr/bin/python3

# -*- coding: utf-8 -*-

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QGridLayout, QDialog, QMessageBox
from PyQt5.QtCore import QProcess, Qt, QUrl, QSharedMemory
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap

from urllib.parse import urlparse

import sys
import yaml
import shutil
import time
import glob
import os
import requests

from tunnel import Ui_Tunnel
from tunnelconfig import Ui_TunnelConfig
from vars import CONF_FILE, LANG, KEYS, ICONS, CMDS
import icons

class TunnelConfig(QDialog):
    def __init__(self, parent, data):
        super(TunnelConfig, self).__init__(parent)
        
        self.ui = Ui_TunnelConfig()
        self.ui.setupUi(self)
        
        self.ui.remote_address.setText(data.get(KEYS.REMOTE_ADDRESS))
        self.ui.proxy_host.setText(data.get(KEYS.PROXY_HOST))
        self.ui.browser_open.setText(data.get(KEYS.BROWSER_OPEN))
        self.ui.local_port.setValue(data.get(KEYS.LOCAL_PORT))
        
        self.ui.remote_address.textChanged.connect(self.render_ssh_command)
        self.ui.proxy_host.textChanged.connect(self.render_ssh_command)
        self.ui.local_port.valueChanged.connect(self.render_ssh_command)
        self.ui.copy.clicked.connect(self.do_copy_ssh_command)
        
        self.render_ssh_command()
    
    def render_ssh_command(self):
        ssh_command = F"ssh -L 127.0.0.1:{self.ui.local_port.value()}:{self.ui.remote_address.text()} {self.ui.proxy_host.text()}"
        self.ui.ssh_command.setText(ssh_command)
        
    def do_copy_ssh_command(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.ui.ssh_command.text(), mode=cb.Clipboard)
        
    def as_dict(self):
        return {
            KEYS.REMOTE_ADDRESS: self.ui.remote_address.text(),
            KEYS.PROXY_HOST: self.ui.proxy_host.text(),
            KEYS.BROWSER_OPEN: self.ui.browser_open.text(),
            KEYS.LOCAL_PORT: self.ui.local_port.value(),
        }

class Tunnel(QWidget):
    def __init__(self, name, data):
        super(Tunnel, self).__init__()
        
        self.ui = Ui_Tunnel()
        self.ui.setupUi(self)
        
        self.tunnelconfig = TunnelConfig(self, data)
        self.tunnelconfig.setWindowTitle(name)
        self.tunnelconfig.setModal(True)
        self.ui.name.setText(name)
        
        self.tunnelconfig.icon = F"./icons/{name}.png"
        
        if not os.path.exists(self.tunnelconfig.icon):
          self.tunnelconfig.icon = ICONS.TUNNEL
        
        self.ui.icon.setPixmap(QPixmap(self.tunnelconfig.icon))
        self.ui.action_tunnel.clicked.connect(self.do_tunnel)
        self.ui.action_settings.clicked.connect(self.tunnelconfig.show)
        self.ui.action_open.clicked.connect(self.do_open_browser)
        
        self.process = None
        
    def do_open_browser(self):
        browser_open = self.tunnelconfig.ui.browser_open.text()
        if browser_open:
            urlobj = urlparse(browser_open)
            local_port = self.tunnelconfig.ui.local_port.value()
            new_url = urlobj._replace(netloc=F"{urlobj.hostname}:{local_port}").geturl()
            QDesktopServices.openUrl(QUrl(new_url))
        
    def do_tunnel(self):
        if self.process:
            self.stop_tunnel()
        else:
            self.start_tunnel()
    
    def start_tunnel(self):
        params = self.tunnelconfig.ui.ssh_command.text().split(" ")
        
        self.process = QProcess()
        self.process.start(params[0], params[1:])
                    
        self.ui.action_tunnel.setIcon(QIcon(ICONS.STOP))
        
        self.do_open_browser()
    
    def stop_tunnel(self):
        try:
            self.process.kill()
            self.process = None
        except:
            pass
        
        self.ui.action_tunnel.setIcon(QIcon(ICONS.START))
        
class TunnelManager(QWidget):
    def __init__(self):
        super().__init__()
        
        with open(CONF_FILE, "r") as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)

        self.grid = QGridLayout(self)
        self.tunnels = []
        
        for i, name in enumerate(sorted(data.keys())):
            tunnel = Tunnel(name, data[name])
            self.tunnels.append(tunnel)
            self.grid.addWidget(tunnel, i, 0)
        
        self.kill_button = QPushButton(LANG.KILL_SSH)
        self.kill_button.setIcon(QIcon(ICONS.KILL_SSH))
        self.kill_button.setFocusPolicy(Qt.NoFocus)
        self.kill_button.clicked.connect(self.do_killall_ssh)
        
        self.grid.addWidget(self.kill_button, i+1, 0)
        
        self.setLayout(self.grid)
        self.resize(10, 10)
        self.setWindowTitle(LANG.TITLE)
        self.setWindowIcon(QIcon(ICONS.TUNNEL))
        self.show()
    
    def do_killall_ssh(self):
        for tunnel in self.tunnels:
            tunnel.stop_tunnel()
        if os.name == 'nt':
            os.system(CMDS.SSH_KILL_WIN)
        else:
            os.system(CMDS.SSH_KILL_NIX)
            
    def closeEvent(self, event):
        data = {}
        for tunnel in self.tunnels:
            name = tunnel.ui.name.text()
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
        mb.setText(LANG.ALREADY_RUNNING)
        mb.setWindowTitle(LANG.OOPS)
        mb.setStandardButtons(QMessageBox.Close)
        mb.show()
    elif not os.path.exists(CONF_FILE):
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setText(LANG.CONF_NOT_FOUND)
        mb.setWindowTitle(LANG.OOPS)
        mb.setStandardButtons(QMessageBox.Close)
        mb.show()
    else:        
        tm = TunnelManager()
            
    sys.exit(app.exec_())
