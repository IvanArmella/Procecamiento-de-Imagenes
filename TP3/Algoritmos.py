# -⁻- coding: UTF-8 -*-
import numpy as np 
import matplotlib.pyplot as plot
import imageio.v2 as imageio

def toYIQ(im):
    fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
    y=im.copy()/255
    for i in range(y.shape[0]):
        y[i,:,:]=np.transpose(np.dot(fRGB,np.transpose(y[i,:,:])))
    return y

def toRGB(im):
    fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
    y=im.copy()
    for i in range(y.shape[0]):
        y[i,:,:]=np.transpose(np.dot(fYIQ,np.transpose(y[i,:,:])))
    y[:,:,:]=np.clip(y[:,:,:]*255,0,255)
    y=y.astype(np.uint8)
    return y

def lineal(x,xmin,xmax):
    m=1/(xmax-xmin)
    b=-m*xmin
    r=x.copy()
    r[:,:,0]=m*x[:,:,0]+b
    r[:,:,0][r[:,:,0]<0]=0
    r[:,:,0][r[:,:,0]>1]=1
    return r


x=toYIQ(imageio.imread("image2.png"))
x=toRGB(lineal(x,0.30,0.9))
plot.imshow(x)
plot.show()
datos=toYIQ(imageio.imread("image1.png"))[:,:,0]
datos=datos.reshape(datos.shape[0]*datos.shape[1],1)
bins=np.linspace(0,1,11).tolist()
n, bins, patches=plot.hist(x=datos, bins=11)
plot.title('Histograma')
plot.xlabel('Luminancia')
plot.ylabel('Frecuencia')
plot.xticks(bins)
plot.show()




