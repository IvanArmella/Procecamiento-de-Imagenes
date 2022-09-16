import numpy as np 
import matplotlib.pyplot as plt
import imageio.v2 as imageio


def CSC(x,y,espacio="RGB"):
    if espacio=="RGB":
        return np.minimum(x+y,255)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=np.minimum((a[:,:,0]+b[:,:,0]),1)
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)    

def CSP(x,y,espacio="RGB"):
    if espacio=="RGB":
        return ((x+y)/2+0.5).astype(int)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=(a[:,:,0]+b[:,:,0])/510
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)

def CRC(x,y,espacio="RGB"):
    if espacio=="RGB":
        return np.maximum(x-y,0)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=np.maximum((a[:,:,0]-b[:,:,0]),0)
        c[:,:,1]=(a[:,:,0]*a[:,:,1]-b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]-b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)
    
def CRP(x,y,espacio="RGB"):
    if espacio=="RGB":
        return (0.5*(x-y)+128).astype(int)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=(a[:,:,0]-b[:,:,0])/510+0.5
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)

def CRA(x,y,espacio="RGB"):
    if espacio=="RGB":
        return abs(x-y)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=abs(a[:,:,0]-b[:,:,0])
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)

def MUL(x,y,espacio="RGB"):
    if espacio=="RGB":
        return np.around(x*y/255,0).astype(int)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        c=a.copy()
        c[:,:,0]=(a[:,:,0]*b[:,:,0])/65025
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)

def DIV(x,y,espacio="RGB"):
    if espacio=="RGB":
        return np.around(x/np.maximum(y,1)).astype(int)
    else:
        a=toYIQ(x)
        b=toYIQ(y)
        b[b==0]=1
        c=a.copy()
        c[:,:,0]=(a[:,:,0]/b[:,:,0])
        c[:,:,1]=(a[:,:,0]*a[:,:,1]+b[:,:,0]*b[:,:,1])/(a[:,:,0]+b[:,:,0])
        c[:,:,2]=(a[:,:,0]*a[:,:,2]+b[:,:,0]*b[:,:,2])/(a[:,:,0]+b[:,:,0])
        return toRGB(c)
    
def IL(x,y):
    a=toYIQ(x)
    b=toYIQ(y)
    c=a.copy();  
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i,j,0]>b[i,j,0]:
                c[i,j,:]=a[i,j,:]
            else:
                c[i,j,:]=b[i,j,:]
    return toRGB(c)

def ID(x,y):
    a=toYIQ(x)
    b=toYIQ(y)
    c=a.copy(); 
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i,j,0]<b[i,j,0]:
                c[i,j,:]=a[i,j,:]
            else:
                c[i,j,:]=b[i,j,:]
    return toRGB(c)               

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


a=imageio.imread("image1.png").astype(int)
b=imageio.imread("image2.png").astype(int)
c=CRA(a,b)
plt.subplot(211)
plt.imshow(c)
a=imageio.imread("image1.png").astype(int)
b=imageio.imread("image2.png").astype(int)
c=CRA(a,b,"YIQ")
plt.subplot(212)
plt.imshow(c)
plt.show()
