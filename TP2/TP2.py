# -⁻- coding: UTF-8 -*-
import sys
from turtle import xcor
from PyQt5 import QtWidgets,QtGui,QtCore
from interfaz import Ui_TP2
import numpy as np 
import matplotlib.pyplot as plt
import imageio.v2 as imageio

class Programa(QtWidgets.QMainWindow):
    def __init__(self):
        super(Programa, self).__init__()
        self.interfaz=Ui_TP2()
        self.interfaz.setupUi(self)
        self.interfaz.btnSeleccionar1.clicked.connect(lambda: self.abrir(True))
        self.interfaz.btnSeleccionar2.clicked.connect(lambda: self.abrir(False))
        self.interfaz.lblImagen.setScaledContents(True)
        self.interfaz.lblImagen2.setScaledContents(True)
        self.interfaz.lblImagen3.setScaledContents(True)
        self.interfaz.rbtnSumaC.clicked.connect(self.control)
        self.interfaz.rbtnSumaP.clicked.connect(self.control)
        self.interfaz.rbtnRestaC.clicked.connect(self.control)
        self.interfaz.rbtnRestaP.clicked.connect(self.control)
        self.interfaz.rbtnProducto.clicked.connect(self.control)
        self.interfaz.rbtnCociente.clicked.connect(self.control)
        self.interfaz.rbtnIL.clicked.connect(self.control)
        self.interfaz.rbtnID.clicked.connect(self.control)
        self.interfaz.rbtnRestaAbs.clicked.connect(self.control)
        self.interfaz.rbtnRGB.clicked.connect(self.control)
        self.interfaz.rbtnYIQ.clicked.connect(self.control)
        self.interfaz.btnProcesar.clicked.connect(self.operar)
        self.interfaz.btnGuardar.clicked.connect(self.guardar)
        self.img1="";self.img2="";self.img3=""
        
        self.show()
        
    def abrir(self,modo):
        ruta=QtWidgets.QFileDialog(self).getOpenFileName(caption="Seleccionar imagen",filter="PNG(*.png)")
        if ruta[0][-4:]==".png":
            img=imageio.imread(ruta[0]).astype(int)
            if modo:
                if type(self.img2)==type("") or img.shape==self.img2.shape:
                    self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(ruta[0]).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
                    self.img1=img
                elif img.shape!=self.img2.shape:
                    QtWidgets.QMessageBox.information(self, "Mensaje", "Las imagenes deben tener la misma dimensión",QtWidgets.QMessageBox.Ok)
            else:
                if type(self.img1)== type("") or img.shape==self.img1.shape:
                    self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(ruta[0]).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))
                    self.img2=imageio.imread(ruta[0]).astype(int)
                elif img.shape!=self.img2.shape:
                    QtWidgets.QMessageBox.information(self, "Mensaje", "Las imagenes deben tener la misma dimensión",QtWidgets.QMessageBox.Ok)

    def control(self):
        if self.interfaz.rbtnIL.isChecked() or self.interfaz.rbtnID.isChecked():
            self.interfaz.rbtnRGB.setChecked(False)
            self.interfaz.rbtnYIQ.setChecked(True)
            self.interfaz.rbtnRGB.setCheckable(False)
        else:
            self.interfaz.rbtnRGB.setCheckable(True)

    def operar(self):
        if type(self.img1)!= type("") and type(self.img2)!= type(""):
            if self.interfaz.rbtnRGB.isChecked():
                formato="RGB"
            else:
                formato="YIQ"
            if self.interfaz.rbtnSumaC.isChecked():
                self.img3=self.CSC(self.img1,self.img2,formato)
            elif self.interfaz.rbtnSumaP.isChecked():
                self.img3=self.CSP(self.img1,self.img2,formato)
            elif self.interfaz.rbtnRestaC.isChecked():
                self.img3=self.CRC(self.img1,self.img2,formato)
            elif self.interfaz.rbtnRestaP.isChecked():
                self.img3=self.CRP(self.img1,self.img2,formato)
            elif self.interfaz.rbtnProducto.isChecked():
                self.img3=self.MUL(self.img1,self.img2,formato)      
            elif self.interfaz.rbtnCociente.isChecked():
                self.img3=self.DIV(self.img1,self.img2,formato)      
            elif self.interfaz.rbtnIL.isChecked():
                self.img3=self.IL(self.img1,self.img2)    
            elif self.interfaz.rbtnID.isChecked():
                self.img3=self.ID(self.img1,self.img2)    
            elif self.interfaz.rbtnRestaAbs.isChecked():
                self.img3=self.CRA(self.img1,self.img2,formato) 
            imageio.imwrite('a.png',self.img3)
            self.interfaz.lblImagen3.setPixmap(QtGui.QPixmap("a.png").scaled(self.interfaz.lblImagen3.geometry().width(),self.interfaz.lblImagen3.geometry().height()))
        else:
             QtWidgets.QMessageBox.information(self, "Mensaje", "Abra 2 imagenes primero",QtWidgets.QMessageBox.Ok)



    def CSC(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return np.minimum(x+y,255).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=np.minimum((a[:,:,0]+b[:,:,0]),1)
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)    

    def CSP(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return ((x+y)/2+0.5).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=(a[:,:,0]+b[:,:,0])/2
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)

    def CRC(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return np.maximum(x-y,0).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=np.maximum((a[:,:,0]-b[:,:,0]),0)
            c[:,:,1]=(a[:,:,0]*a[:,:,1]-b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]-b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)
    
    def CRP(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return (0.5*(x-y)+128).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=(a[:,:,0]-b[:,:,0])/2+0.5
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)

    def CRA(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return abs(x-y).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=abs(a[:,:,0]-b[:,:,0])
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)

    def MUL(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return np.around(x*y/255,0).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=a.copy()
            c[:,:,0]=(a[:,:,0]*b[:,:,0])
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)

    def DIV(self,x,y,espacio="RGB"):
        if espacio=="RGB":
            return np.around(x/np.maximum(y,1)).astype(np.uint8)
        else:
            a=self.toYIQ(x)
            b=self.toYIQ(y)
            c=b[:,:,0]
            c[c==0]=1
            b[:,:,0]=c
            c=a.copy()
            c[:,:,0]=np.minimum(a[:,:,0]/b[:,:,0],1)
            c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
            c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
            return self.toRGB(c)
    
    def IL(self,x,y):
        a=self.toYIQ(x)
        b=self.toYIQ(y)
        c=a.copy();  
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if a[i,j,0]>b[i,j,0]:
                    c[i,j,:]=a[i,j,:]
                else:
                    c[i,j,:]=b[i,j,:]
        return self.toRGB(c)

    def ID(self,x,y):
        a=self.toYIQ(x)
        b=self.toYIQ(y)
        c=a.copy(); 
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if a[i,j,0]<b[i,j,0]:
                    c[i,j,:]=a[i,j,:]
                else:
                    c[i,j,:]=b[i,j,:]
        return self.toRGB(c)               

    def toYIQ(self,im):
        fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
        y=im.copy()/255
        for i in range(y.shape[0]):
            y[i,:,:]=np.transpose(np.dot(fRGB,np.transpose(y[i,:,:])))
        return y

    def toRGB(self,im):
        fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
        y=im.copy()
        for i in range(y.shape[0]):
            y[i,:,:]=np.transpose(np.dot(fYIQ,np.transpose(y[i,:,:])))
        y[:,:,:]=np.clip(y[:,:,:]*255,0,255)
        y=y.astype(np.uint8)
        return y

    def guardar(self):
        if self.img3!="":
            ruta=QtWidgets.QFileDialog(self).getSaveFileName(caption="Seleccionar imagen",filter="PNG(*.png)")
            imageio.imwrite(ruta[0],self.img3)

if __name__ == "__main__": 
    app=QtWidgets.QApplication(sys.argv)
    programa=Programa()
    sys.exit(app.exec())
