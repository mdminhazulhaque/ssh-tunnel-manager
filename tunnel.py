# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tunnel.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tunnel(object):
    def setupUi(self, Tunnel):
        Tunnel.setObjectName("Tunnel")
        Tunnel.resize(360, 36)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Tunnel)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtWidgets.QLabel(Tunnel)
        self.icon.setMinimumSize(QtCore.QSize(24, 24))
        self.icon.setMaximumSize(QtCore.QSize(24, 24))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.name = QtWidgets.QLabel(Tunnel)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.name.setFont(font)
        self.name.setIndent(5)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        self.action_tunnel = QtWidgets.QPushButton(Tunnel)
        self.action_tunnel.setMaximumSize(QtCore.QSize(32, 16777215))
        self.action_tunnel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.action_tunnel.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":icons/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_tunnel.setIcon(icon)
        self.action_tunnel.setIconSize(QtCore.QSize(20, 20))
        self.action_tunnel.setFlat(True)
        self.action_tunnel.setObjectName("action_tunnel")
        self.horizontalLayout.addWidget(self.action_tunnel)
        self.action_open = QtWidgets.QPushButton(Tunnel)
        self.action_open.setMaximumSize(QtCore.QSize(32, 16777215))
        self.action_open.setFocusPolicy(QtCore.Qt.NoFocus)
        self.action_open.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":icons/browser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_open.setIconSize(QtCore.QSize(20, 20))
        self.action_open.setFlat(True)
        self.action_open.setObjectName("action_open")
        self.horizontalLayout.addWidget(self.action_open)
        self.action_settings = QtWidgets.QPushButton(Tunnel)
        self.action_settings.setMaximumSize(QtCore.QSize(32, 32))
        self.action_settings.setFocusPolicy(QtCore.Qt.NoFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_settings.setIcon(icon2)
        self.action_settings.setIconSize(QtCore.QSize(20, 20))
        self.action_settings.setFlat(True)
        self.action_settings.setObjectName("action_settings")
        self.horizontalLayout.addWidget(self.action_settings)

        self.retranslateUi(Tunnel)
        QtCore.QMetaObject.connectSlotsByName(Tunnel)

    def retranslateUi(self, Tunnel):
        _translate = QtCore.QCoreApplication.translate
        Tunnel.setWindowTitle(_translate("Tunnel", "Form"))
        self.icon.setText(_translate("Tunnel", "icon"))
        self.name.setText(_translate("Tunnel", "TextLabel"))
