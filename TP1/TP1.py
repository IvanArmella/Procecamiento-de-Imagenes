# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 02:13:24 2022

@author: Ivan
"""
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from interfaz import Ui_TP1
import numpy as np 
import matplotlib.pyplot as plt
import imageio.v2 as imageio

class Programa(QtWidgets.QMainWindow):
    def __init__(self):
        super(Programa, self).__init__()
        self.interfaz=Ui_TP1()
        self.interfaz.setupUi(self)
        self.validadorFloat(self.interfaz.edtLuminancia)
        self.validadorFloat(self.interfaz.edtSaturacion)
        self.interfaz.lblImagen.setPixmap(QtGui.QPixmap("image2.png").scaled(715,529))
        self.interfaz.btnSeleccionar.clicked.connect(self.seleccionar)
        self.interfaz.btnActualizar.clicked.connect(self.actualizar)
        self.ruta="image2.png"
        self.show()
        
    def seleccionar(self):
        ruta=QtWidgets.QFileDialog(self).getOpenFileName(caption="Seleccionar imagen",filter="PNG(*.png)")
        if ruta[0][-4:]==".png":
            self.ruta=ruta[0]
            self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(ruta[0]).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
            self.interfaz.edtLuminancia.setText("1")
            self.interfaz.edtSaturacion.setText("1")
        
    def reemplazar(self,obj):
        if ',' in obj.text():
            obj.setText(obj.text().replace(",","."))

    def validadorFloat(self,obj):
        exp  = QtCore.QRegExp("[0-9]+((\.|\,)[0-9]+)?")
        obj.setValidator(QtGui.QRegExpValidator(exp));
        obj.textChanged.connect(lambda: self.reemplazar(obj))
        
    def actualizar(self):
        fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
        fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
        im=imageio.imread(self.ruta)/255
        a=float(self.interfaz.edtLuminancia.text())
        b=float(self.interfaz.edtSaturacion.text())
        f=im.shape[0]
        c=im.shape[1]
        for i in range(f):      
                im[i,:,:]=np.transpose(np.dot(fRGB,np.transpose(im[i,:,:])))
        im[:,:,0]=np.minimum(im[:,:,0]*a,1)
        im[:,:,1:]=np.clip(im[:,:,1:]*b,-0.5957,0.5957)
        for i in range(f):
                im[i,:,:]=np.transpose(np.dot(fYIQ,np.transpose(im[i,:,:])))
        im[:,:,:]=np.clip(im[:,:,:]*255,0,255)
        im=im.astype(np.uint8)
        imageio.imwrite('a.png',im)
        self.interfaz.lblImagen.setPixmap(QtGui.QPixmap("a.png").scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
        print(self.interfaz.lblImagen.geometry().height())
        

    
    
if __name__ == "__main__": 
    app=QtWidgets.QApplication(sys.argv)
    programa=Programa()
    sys.exit(app.exec())
