# -⁻- coding: UTF-8 -*-
#Autor: Armella, Iván Javier
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from interfaz import Ui_TP4
import numpy as np 
import imageio.v2 as imageio

class Programa(QtWidgets.QMainWindow):
    def __init__(self):
        super(Programa, self).__init__()
        self.interfaz=Ui_TP4()
        self.interfaz.setupUi(self)
        self.interfaz.btnSeleccionar.clicked.connect(self.abrir)
        self.interfaz.btnFiltrar.clicked.connect(self.operar)
        self.interfaz.btnGuardar.clicked.connect(self.guardar)
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

    def guardar(self):
        if type(self.img2)!=type(""):
            ruta=QtWidgets.QFileDialog(self).getSaveFileName(caption="Seleccionar imagen",filter="Imagenes(*.png *.bmp)")
            if ruta[0]!="":
                imageio.imwrite(ruta[0],self.img2)
        else:
            QtWidgets.QMessageBox.information(self, "Mensaje", "Filtre una imagen primero",QtWidgets.QMessageBox.Ok)

    def operar(self):
        if type(self.img1)!=type(""):
            if len(self.img1.shape)==3:
                self.img2=self.getYIQ(self.img1)
                x=self.img2[:,:,0]
            else:
                x=self.img1.copy()
            if self.interfaz.cboxModo.currentText()=="Plano 3x3":
                x=self.convolucionar2(x,np.ones((3,3))/9)
            if self.interfaz.cboxModo.currentText()=="Plano 5x5":
                x=self.convolucionar2(x,np.ones((5,5))/25)
            if self.interfaz.cboxModo.currentText()=="Plano 7x7":
                x=self.convolucionar2(x,np.ones((7,7))/49)
            elif self.interfaz.cboxModo.currentText()=="Bartlett 3x3":
                x=self.convolucionar2(x,self.kernelBartlett(3))
            elif self.interfaz.cboxModo.currentText()=="Bartlett 5x5":
                x=self.convolucionar2(x,self.kernelBartlett(5))
            elif self.interfaz.cboxModo.currentText()=="Bartlett 7x7":
                x=self.convolucionar2(x,self.kernelBartlett(7))
            elif self.interfaz.cboxModo.currentText()=="Gaussiano 5x5":
                x=self.convolucionar2(x,self.kernelGaussiano(5))
            elif self.interfaz.cboxModo.currentText()=="Gaussiano 7x7":
                x=self.convolucionar2(x,self.kernelGaussiano(7))   
            elif self.interfaz.cboxModo.currentText()=="Laplaciano v4 3x3":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,1)
                else:
                    x=self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Laplaciano v8 3x3":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,1)
                else:
                    x=self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Sobel Norte":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("norte")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("norte")).clip(0,255)            
            elif self.interfaz.cboxModo.currentText()=="Sobel Noreste":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("noreste")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("noreste")).clip(0,255)      
            elif self.interfaz.cboxModo.currentText()=="Sobel Este":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("este")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("este")).clip(0,255)      
            elif self.interfaz.cboxModo.currentText()=="Sobel Sureste":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("sureste")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("sureste")).clip(0,255)   
            elif self.interfaz.cboxModo.currentText()=="Sobel Sur":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("sur")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("sur")).clip(0,255)              
            elif self.interfaz.cboxModo.currentText()=="Sobel Suroeste":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("suroeste")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("suroeste")).clip(0,255)     
            elif self.interfaz.cboxModo.currentText()=="Sobel Oeste":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("oeste")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("oeste")).clip(0,255)    
            elif self.interfaz.cboxModo.currentText()=="Sobel Noroeste":
                if len(self.img1.shape)==3:
                    x=self.convolucionar2(x,self.kernelSobel("noroeste")).clip(0,1)
                else:
                    x=self.convolucionar2(x,self.kernelSobel("noroeste")).clip(0,255)
            elif self.interfaz.cboxModo.currentText()=="Pasabanda":
                if len(self.img1.shape)==3:
                    x=(self.convolucionar2(x,self.kernelGaussiano(3)).clip(0,1)-self.convolucionar2(x,self.kernelGaussiano(5)).clip(0,1)).clip(0,1)
                else:
                    x=((self.convolucionar2(x,self.kernelGaussiano(3)).clip(0,255)-self.convolucionar2(x,self.kernelGaussiano(5)).clip(0,255)).clip(0,1)*255).astype(int)        
            elif self.interfaz.cboxModo.currentText()=="Pasaalto Laplaciano V4 0.2":
                if len(self.img1.shape)==3:
                    x=(x+self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,1)*0.2).clip(0,1) 
                else:
                    x=(x+self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,255)*0.2).clip(0,255).astype(int)
            elif self.interfaz.cboxModo.currentText()=="Pasaalto Laplaciano V4 0.4":
                if len(self.img1.shape)==3:
                    x=(x+self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,1)*0.4).clip(0,1) 
                else:
                    x=(x+self.convolucionar2(x,np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)).clip(0,255)*0.4).clip(0,255).astype(int)
            elif self.interfaz.cboxModo.currentText()=="Pasaalto Laplaciano V8 0.2":
                if len(self.img1.shape)==3:
                    x=(x+self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,1)*0.2).clip(0,1)
                else:
                    x=(x+self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,255)*0.2).clip(0,255).astype(int)
            elif self.interfaz.cboxModo.currentText()=="Pasaalto Laplaciano V8 0.4":
                if len(self.img1.shape)==3:
                    x=(x+self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,1)*0.4).clip(0,1)
                else:
                   x=(x+self.convolucionar2(x,np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)).clip(0,255)*0.4).clip(0,255).astype(int)
            if len(self.img1.shape)==3:
                self.img2[:,:,0]=x
                self.img2=self.getRGB(self.img2)
                im=QtGui.QImage(self.img2.astype(np.uint8),self.img2.shape[1],self.img2.shape[0],self.img2.shape[1]*3,QtGui.QImage.Format_RGB888)
                self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))
            else:
                self.img2=x
                im=QtGui.QImage(self.img2.astype(np.uint8),self.img2.shape[1],self.img2.shape[0],self.img2.shape[1],QtGui.QImage.Format_Grayscale8)
                self.interfaz.lblImagen2.setPixmap(QtGui.QPixmap(im).scaled(self.interfaz.lblImagen2.geometry().width(),self.interfaz.lblImagen2.geometry().height()))  
        else:
             QtWidgets.QMessageBox.information(self, "Mensaje", "Abra una imagen primero",QtWidgets.QMessageBox.Ok)
             
    def convolucionar(self,x,kernel):
        r=np.zeros(np.array(x.shape)-np.array(kernel.shape)+1)
        for i in range(r.shape[0]):
            for j in range(r.shape[1]):
                r[i,j]=(x[i:i+kernel.shape[0],j:j+kernel.shape[1]]*kernel).sum()
        return r

    def convolucionar2(self,x,kernel):
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
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                y[i,j]=(r[i:i+kernel.shape[0],j:j+kernel.shape[1]]*kernel).sum()
        return y

    def kernelGaussiano(self,n):
        r=list()
        j=0
        for i in range(n):
            r.append(np.math.factorial(n-1)/(np.math.factorial(n-1-j)*np.math.factorial(j)))
            j+=1
        r=np.array(r).astype(int).reshape(n,1)
        r=np.dot(r,r.transpose())
        return  r/np.sum(r)

    def kernelBartlett(self,dim=1):
        n=round(dim/2+0.5)
        r=np.concatenate((np.arange(1,n+1,1),np.arange(n-1,0,-1))).reshape(2*n-1,1)
        r=np.dot(r,r.transpose())
        return r/np.sum(r)

    def kernelSobel(self,d):
        if d=="norte":
            return np.array((-1,-2,-1,0,0,0,1,2,1)).reshape(3,3)
        elif d=="sur":
            return np.array((1,2,1,0,0,0,-1,-2,-1)).reshape(3,3)
        elif d=="oeste":
            return np.array((-1,0,1,-2,0,2,-1,0,1)).reshape(3,3)
        elif d=="este":
            return np.array((1,0,-1,2,0,-2,1,0,-1)).reshape(3,3)
        elif d=="noreste":
            return np.array((0,-1,-2,1,0,-1,2,1,0)).reshape(3,3)
        elif d=="suroeste":
            return np.array((0,1,2,-1,0,1,-2,-1,0)).reshape(3,3)
        elif d=="noroeste":
            return np.array((-2,-1,0,-1,0,1,0,1,2)).reshape(3,3)
        elif d=="sureste":
            return np.array((2,1,0,1,0,-1,0,-1,-2)).reshape(3,3)

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
