from tkinter import *
from tkinter import filedialog
import numpy as np 
import matplotlib.pyplot as plt
import imageio.v2 as imageio

class Interfaz:
    def __init__(self,ventana):
        self.ventana=ventana
        self.ventana.title("Procesamiento de Imagenes")
        self.ruta="image2.png"
        self.imagen=PhotoImage(file=self.ruta)
        self.lblImagen=Label(ventana,image=self.imagen,padx=5,pady=5)
        self.btnSeleccionar=Button(ventana,text="Selecconar",command=self.seleccionar,padx=5,pady=5)
        self.btnActualizar=Button(ventana,text="Actualizar",command=self.actualizar,padx=5,pady=5)
        self.lblSaturacion=Label(ventana,text="Saturación",padx=5,pady=5)
        self.lblLuminancia=Label(ventana,text="Luminancia",padx=5,pady=5)
        self.edtSaturacion=Entry(ventana)
        self.edtLuminancia=Entry(ventana)
        self.edtSaturacion.insert(0,"1")
        self.edtLuminancia.insert(0,"1")
        self.lblImagen.grid(row=1,columnspan=4)
        self.lblLuminancia.grid(row=2,column=0)
        self.edtLuminancia.grid(row=2,column=1)
        self.lblSaturacion.grid(row=2,column=2)
        self.edtSaturacion.grid(row=2,column=3)
        self.btnSeleccionar.grid(row=3,column=2)
        self.btnActualizar.grid(row=3,column=3)

    def seleccionar(self):
        ruta=filedialog.askopenfilename(title="Seleccionar Imagen",filetypes=[("Imagenes", ".png")])
        if ruta[-4:]==".png":
            self.imagen=PhotoImage(file=ruta)
            self.lblImagen=Label(ventana,image=self.imagen,padx=5,pady=5)
            self.lblImagen.grid(row=1,columnspan=4)
            self.edtSaturacion.delete(0, END)
            self.edtLuminancia.delete(0, END)
            self.edtSaturacion.insert(0,"1")
            self.edtLuminancia.insert(0,"1")
        
    def actualizar(self):
        fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
        fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
        im=imageio.imread(self.ruta)/255
        a=float(self.edtLuminancia.get())
        b=float(self.edtSaturacion.get())
        f=im.shape[0]
        c=im.shape[1]
        for i in range(f):
            for j in range(c):
                im[i,j,:]=np.matmul(fRGB,im[i,j,:])
        im[:,:,0]=np.minimum(im[:,:,0]*a,1)
        im[:,:,1:]=np.clip(im[:,:,1:]*b,-0.5957,0.5957)
        for i in range(f):
            for j in range(c):
                im[i,j,:]=np.matmul(fYIQ,im[i,j,:])
        im[:,:,:]=np.clip(im[:,:,:]*255,0,255)
        im=im.astype(np.uint8)
        imageio.imwrite('a.png',im)
        self.imagen=PhotoImage(file="a.png")
        self.lblImagen=Label(ventana,image=self.imagen,padx=5,pady=5)
        self.lblImagen.grid(row=1,columnspan=4)


ventana=Tk()
programa=Interfaz(ventana)
ventana.mainloop()
