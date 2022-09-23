# -⁻- coding: UTF-8 -*-
#Autor: Armella, Iván Javier
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from interfaz import Ui_TP5
import numpy as np 
import imageio.v2 as imageio

class Programa(QtWidgets.QMainWindow):
    def __init__(self):
        super(Programa, self).__init__()
        self.interfaz=Ui_TP5()
        self.interfaz.setupUi(self)
        self.interfaz.btnSeleccionar.clicked.connect(self.abrir)
        self.interfaz.btnGuardar.clicked.connect(self.guardar)
        self.interfaz.cboxModo.currentIndexChanged.connect(self.operar)
        self.interfaz.btnUtilizar.clicked.connect(self.utilizar)
        self.img1="";self.img2="";
        self.show()

    def abrir(self):
        ruta=QtWidgets.QFileDialog(self).getOpenFileName(caption="Seleccionar imagen",filter="Imagenes(*.png *.bmp)")
        if ruta[0][-4:]==".png" or ruta[0][-4:]==".bmp":
            img=imageio.imread(ruta[0]).astype(int)
            self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(ruta[0]).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
            self.img1=img
            self.interfaz.lblImagen2.clear()
            self.img2=""
            self.operar()

    def guardar(self):
        if type(self.img2)!=type(""):
            ruta=QtWidgets.QFileDialog(self).getSaveFileName(caption="Seleccionar imagen",filter="Imagenes(*.png *.bmp)")
            if ruta[0]!="":
                imageio.imwrite(ruta[0],self.img2)
        else:
            QtWidgets.QMessageBox.information(self, "Mensaje", "Filtre una imagen primero",QtWidgets.QMessageBox.Ok)

    def operar(self):
        if type(self.img1)!=type(""):
            if self.interfaz.cboxModo.currentText()=="Erosión 3x3":
                self.img2=self.convolucionar(self.img1,np.ones((3,3)),1)
            elif self.interfaz.cboxModo.currentText()=="Erosión 5x5":
                self.img2=self.convolucionar(self.img1,np.ones((5,5)),1)
            elif self.interfaz.cboxModo.currentText()=="Dilatación 3x3":
                self.img2=self.convolucionar(self.img1,np.ones((3,3)),2)
            elif self.interfaz.cboxModo.currentText()=="Dilatación 5x5":
                self.img2=self.convolucionar(self.img1,np.ones((5,5)),2)
            elif self.interfaz.cboxModo.currentText()=="Apertura 3x3":
                self.img2=self.convolucionar(self.convolucionar(self.img1,np.ones((3,3)),1),np.ones((3,3)),2)
            elif self.interfaz.cboxModo.currentText()=="Apertura 5x5":
                self.img2=self.convolucionar(self.convolucionar(self.img1,np.ones((5,5)),1),np.ones((5,5)),2)               
            elif self.interfaz.cboxModo.currentText()=="Cierre 3x3":
                self.img2=self.convolucionar(self.convolucionar(self.img1,np.ones((3,3)),2),np.ones((3,3)),1)
            elif self.interfaz.cboxModo.currentText()=="Cierre 5x5":
                self.img2=self.convolucionar(self.convolucionar(self.img1,np.ones((5,5)),2),np.ones((5,5)),1)    
            elif self.interfaz.cboxModo.currentText()=="Borde Exterior 3x3":
                if self.img1.ndim==3: self.img2=(self.convolucionar(self.img1,np.ones((3,3)),2)-self.img1[:,:,0:3]).clip(0,255)
                else: self.img2=(self.convolucionar(self.img1,np.ones((3,3)),2)-self.img1).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Borde Exterior 5x5":
                if self.img1.ndim==3: self.img2=self.convolucionar(self.img1,np.ones((5,5)),2)-self.img1[:,:,0:3]
                else: self.img2=(self.convolucionar(self.img1,np.ones((5,5)),2)-self.img1).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Borde Interior 3x3":
                if self.img1.ndim==3: self.img2=(self.img1[:,:,0:3]-self.convolucionar(self.img1,np.ones((3,3)),1)).clip(0,255)
                else: self.img2=(self.img1-self.convolucionar(self.img1,np.ones((3,3)),1)).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Borde Interior 5x5":
                if self.img1.ndim==3: self.img2=(self.img1[:,:,0:3]-self.convolucionar(self.img1,np.ones((5,5)),1)).clip(0,255)
                else: self.img2=self.img1-self.convolucionar(self.img1,np.ones((5,5)),1)
            elif self.interfaz.cboxModo.currentText()=="Mediana 3x3":
                self.img2=self.convolucionar(self.img1,np.ones((3,3)),3)
            elif self.interfaz.cboxModo.currentText()=="Mediana 5x5":
                self.img2=self.convolucionar(self.img1,np.ones((5,5)),3)
            elif self.interfaz.cboxModo.currentText()=="Gradiente 3x3":
                self.img2=(self.convolucionar(self.img1,np.ones((3,3)),2)-self.convolucionar(self.img1,np.ones((3,3)),1)).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Gradiente 5x5":
                self.img2=(self.convolucionar(self.img1,np.ones((5,5)),2)-self.convolucionar(self.img1,np.ones((5,5)),1)).clip(0,255)
            if  self.img2.ndim==3:
                im=QtGui.QImage(self.img2.astype(np.uint8),self.img2.shape[1],self.img2.shape[0],self.img2.shape[1]*3,QtGui.QImage.Format_RGB888)
                self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))
            else:
                im=QtGui.QImage(self.img2.astype(np.uint8),self.img2.shape[1],self.img2.shape[0],self.img2.shape[1],QtGui.QImage.Format_Grayscale8)
                self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))  
        else:
             QtWidgets.QMessageBox.information(self, "Mensaje", "Abra una imagen primero",QtWidgets.QMessageBox.Ok)


    def utilizar(self):
        if type(self.img2)!=type(""):
            self.img1=self.img2.copy()
            if  self.img1.ndim==3:
                im=QtGui.QImage(self.img1.astype(np.uint8),self.img1.shape[1],self.img1.shape[0],self.img1.shape[1]*3,QtGui.QImage.Format_RGB888)
                self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
            else:
                im=QtGui.QImage(self.img1.astype(np.uint8),self.img1.shape[1],self.img1.shape[0],self.img1.shape[1],QtGui.QImage.Format_Grayscale8)
                self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
            self.operar()
        else:
            QtWidgets.QMessageBox.information(self, "Mensaje", "Filtre una imagen primero",QtWidgets.QMessageBox.Ok)


             
    def convolucionar(self,im,kernel,modo=0):
        if im.ndim!=2:
            yiq=self.getYIQ(im[:,:,0:3])
            x=yiq[:,:,0]
        else: x=im
        r=np.zeros(np.array(x.shape)+np.array(kernel.shape)-1)
        lim=((np.array(r.shape)-np.array(x.shape))/2).astype(int)
        r[lim[0]:lim[0]+x.shape[0],lim[1]:lim[1]+x.shape[1]]=x
        aux=x[0,:]
        aux2=x[x.shape[0]-1,:]
        aux=np.append(np.repeat(aux[0],lim[1]),aux)
        aux=np.append(aux,np.repeat(aux[aux.shape[0]-1],lim[1]))
        aux2=np.append(np.repeat(aux2[0],lim[1]),aux2)
        aux2=np.append(aux2,np.repeat(aux2[aux2.shape[0]-1],lim[1]))
        r[0:lim[0],:]=np.tile(aux,(lim[0],1))
        r[r.shape[0]-lim[0]:r.shape[0],:]=np.tile(aux2,(lim[0],1))
        r[lim[0]:r.shape[0]-lim[0],0:lim[1]]=np.tile(x[:,0],(lim[1],1)).transpose()
        r[lim[0]:r.shape[0]-lim[0],r.shape[1]-lim[1]:r.shape[1]]=np.tile(x[:,x.shape[0]-1],(lim[1],1)).transpose()
        y=np.zeros(x.shape)
        if modo==0:
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    y[i,j]=(r[i:i+kernel.shape[0],j:j+kernel.shape[1]]*kernel).sum()
        elif modo==1:
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    y[i,j]=r[i:i+kernel.shape[0],j:j+kernel.shape[1]].min()
        elif modo==2:
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    y[i,j]=r[i:i+kernel.shape[0],j:j+kernel.shape[1]].max()
        else:
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    y[i,j]=np.sort(r[i:i+kernel.shape[0],j:j+kernel.shape[1]])[(kernel.shape[0]-1)//2,(kernel.shape[1]-1)//2]
        if im.ndim!=2:
            yiq[:,:,0]=y
            y=self.getRGB(yiq)
        return y

    def getYIQ(self,im):
        fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
        y=im.copy()/255
        for i in range(y.shape[0]):
            y[i,:,:]=np.transpose(np.dot(fRGB,np.transpose(y[i,:,:])))
        return y

    def getRGB(self,im):
        fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
        y=im.copy()
        for i in range(y.shape[0]):
            y[i,:,:]=np.transpose(np.dot(fYIQ,np.transpose(y[i,:,:])))
        y[:,:,:]=np.clip(y[:,:,:]*255,0,255)
        y=y.astype(np.uint8)
        return y          

if __name__ == "__main__": 
    app=QtWidgets.QApplication(sys.argv)
    programa=Programa()
    sys.exit(app.exec())
