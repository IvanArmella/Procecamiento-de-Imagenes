# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TP1(object):
    def setupUi(self, TP1):
        TP1.setObjectName("TP1")
        TP1.resize(733, 642)
        TP1.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(TP1)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblImagen = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblImagen.sizePolicy().hasHeightForWidth())
        self.lblImagen.setSizePolicy(sizePolicy)
        self.lblImagen.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.lblImagen.setText("")
        self.lblImagen.setObjectName("lblImagen")
        self.verticalLayout.addWidget(self.lblImagen)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblLuminancia = QtWidgets.QLabel(self.centralwidget)
        self.lblLuminancia.setObjectName("lblLuminancia")
        self.horizontalLayout_4.addWidget(self.lblLuminancia)
        self.edtLuminancia = QtWidgets.QLineEdit(self.centralwidget)
        self.edtLuminancia.setObjectName("edtLuminancia")
        self.horizontalLayout_4.addWidget(self.edtLuminancia)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.lblSaturacion = QtWidgets.QLabel(self.centralwidget)
        self.lblSaturacion.setObjectName("lblSaturacion")
        self.horizontalLayout_4.addWidget(self.lblSaturacion)
        self.edtSaturacion = QtWidgets.QLineEdit(self.centralwidget)
        self.edtSaturacion.setObjectName("edtSaturacion")
        self.horizontalLayout_4.addWidget(self.edtSaturacion)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnSeleccionar = QtWidgets.QPushButton(self.centralwidget)
        self.btnSeleccionar.setObjectName("btnSeleccionar")
        self.horizontalLayout.addWidget(self.btnSeleccionar)
        self.btnActualizar = QtWidgets.QPushButton(self.centralwidget)
        self.btnActualizar.setObjectName("btnActualizar")
        self.horizontalLayout.addWidget(self.btnActualizar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        TP1.setCentralWidget(self.centralwidget)

        self.retranslateUi(TP1)
        QtCore.QMetaObject.connectSlotsByName(TP1)

    def retranslateUi(self, TP1):
        _translate = QtCore.QCoreApplication.translate
        TP1.setWindowTitle(_translate("TP1", "TP1"))
        self.lblLuminancia.setText(_translate("TP1", "Luminancia"))
        self.edtLuminancia.setText(_translate("TP1", "1"))
        self.lblSaturacion.setText(_translate("TP1", "Saturación"))
        self.edtSaturacion.setText(_translate("TP1", "1"))
        self.btnSeleccionar.setText(_translate("TP1", "Seleccionar"))
        self.btnActualizar.setText(_translate("TP1", "Actualizar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TP1 = QtWidgets.QMainWindow()
    ui = Ui_TP1()
    ui.setupUi(TP1)
    TP1.show()
    sys.exit(app.exec_())