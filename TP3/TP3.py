# -⁻- coding: UTF-8 -*-
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from interfaz import Ui_TP3
import numpy as np 
import matplotlib.pyplot as plt
import imageio.v2 as imageio

class Programa(QtWidgets.QMainWindow):
    def __init__(self):
        super(Programa, self).__init__()
        self.interfaz=Ui_TP3()
        self.interfaz.setupUi(self)
        self.validadorFloat(self.interfaz.edtMax)
        self.validadorFloat(self.interfaz.edtMin)
        self.interfaz.edtMin.textChanged.connect(lambda: self.reemplazar(self.interfaz.edtMin))
        self.interfaz.edtMax.textChanged.connect(lambda: self.reemplazar(self.interfaz.edtMax))
        self.interfaz.btnSeleccionar.clicked.connect(self.abrir)
        self.interfaz.btnProcesar.clicked.connect(self.operar)
        self.interfaz.btnGuardar.clicked.connect(self.guardar)
        self.interfaz.btnHistogramas.clicked.connect(self.getHistograma)
        self.img1="";self.img2="";
        self.show()

    def getHistograma(self):
        if type(self.img1)!=type(""):   
            datos=self.img1[:,:,0]
            datos=datos.reshape(datos.shape[0]*datos.shape[1],1)
            bins=np.linspace(0,1,11).tolist()
            if type(self.img2)!=type(""):  
                plt.subplot(121)
                plt.hist(x=datos, bins=bins,edgecolor = "black")
                plt.title('Imagen Original')
                plt.xlabel('Luminancia')
                plt.ylabel('Frecuencia')
                plt.xticks(bins)
                datos=self.getYIQ(self.img2)[:,:,0]
                datos=datos.reshape(datos.shape[0]*datos.shape[1],1)
                plt.subplot(122)
                plt.hist(x=datos, bins=bins,edgecolor = "black")
                plt.title('Imagen Filtrada')
                plt.xlabel('Luminancia')
                plt.ylabel('Frecuencia')
                plt.xticks(bins)
            else:
                plt.hist(x=datos, bins=bins,edgecolor = "black")
                plt.title('Imagen Original')
                plt.xlabel('Luminancia')
                plt.ylabel('Frecuencia')
                plt.xticks(bins)
            plt.show()
        else:
            QtWidgets.QMessageBox.information(self, "Mensaje", "Abra una imagen primero",QtWidgets.QMessageBox.Ok)
        
    def abrir(self):
        ruta=QtWidgets.QFileDialog(self).getOpenFileName(caption="Seleccionar imagen",filter="Imagenes(*.png *.bmp)")
        if ruta[0][-4:]==".png" or ruta[0][-4:]==".bmp":
            img=imageio.imread(ruta[0]).astype(int)
            self.interfaz.lblImagen.setPixmap(QtGui.QPixmap(ruta[0]).scaled(self.interfaz.lblImagen.geometry().width(),self.interfaz.lblImagen.geometry().height()))
            self.img1=self.getYIQ(img)

    def operar(self):
        if type(self.img1)!=type(""):   
            if self.interfaz.cboxModo.currentText()=="Cuadrado":
                self.img2=self.img1.copy()
                self.img2[:,:,0]=self.img1[:,:,0]**2
                self.img2=self.getRGB(self.img2)
            elif self.interfaz.cboxModo.currentText()=="Raiz Cuadrada":
                self.img2=self.img1.copy()
                self.img2[:,:,0]=self.img1[:,:,0]**0.5
                self.img2=self.getRGB(self.img2)
            else:
                a=float(self.interfaz.edtMin.text())
                b=float(self.interfaz.edtMax.text())
                if a<b:
                    self.img2=self.getRGB(self.lineal(self.img1,a,b))
                else:
                    QtWidgets.QMessageBox.information(self, "Mensaje", "La luminancia mínima debe ser mayor a la máxima",QtWidgets.QMessageBox.Ok)
            im=QtGui.QImage(self.img2.astype(np.uint8),self.img2.shape[1],self.img2.shape[0],self.img2.shape[1]*3,QtGui.QImage.Format_RGB888)
            self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))
        else:
             QtWidgets.QMessageBox.information(self, "Mensaje", "Abra una imagen primero",QtWidgets.QMessageBox.Ok)
             
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

    def guardar(self):
        if type(self.img2)!=type(""):
            ruta=QtWidgets.QFileDialog(self).getSaveFileName(caption="Seleccionar imagen",filter="Imagenes(*.png *.bmp)")
            if ruta[0]!="":
                imageio.imwrite(ruta[0],self.img2)

    def lineal(self,x,xmin,xmax):
        m=1/(xmax-xmin)
        b=-m*xmin
        r=x.copy()
        r[:,:,0]=m*x[:,:,0]+b
        r[:,:,0][r[:,:,0]<0]=0
        r[:,:,0][r[:,:,0]>1]=1
        return r

    def reemplazar(self,obj):
        if ',' in obj.text():
            obj.setText(obj.text().replace(",","."))

    def validadorFloat(self,obj):
        exp  = QtCore.QRegExp("[0-9]+((\.|\,)[0-9]+)?")
        obj.setValidator(QtGui.QRegExpValidator(exp));
        obj.textChanged.connect(lambda: self.reemplazar(obj))

if __name__ == "__main__": 
    app=QtWidgets.QApplication(sys.argv)
    programa=Programa()
    sys.exit(app.exec())
