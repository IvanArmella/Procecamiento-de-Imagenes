# -⁻- coding: UTF-8 -*-
import numpy as np 
import matplotlib.pyplot as plot
import imageio.v2 as imageio

def getYIQ(im):
    fRGB=np.array([0.299,0.587,0.114,0.595716,-0.274453,-0.321263,0.211456,-0.522591,0.311135]).reshape(3,3)
    y=im.copy()/255
    for i in range(y.shape[0]):
        y[i,:,:]=np.transpose(np.dot(fRGB,np.transpose(y[i,:,:])))
    return y

def getRGB(im):
    fYIQ=np.array([1,0.9663,0.6210,1,-0.2721,-0.6474,1,-1.1070,1.7046]).reshape(3,3)
    y=im.copy()
    for i in range(y.shape[0]):
        y[i,:,:]=np.transpose(np.dot(fYIQ,np.transpose(y[i,:,:])))
    y[:,:,:]=np.clip(y[:,:,:]*255,0,255)
    y=y.astype(np.uint8)
    return y

def convolucionar(x,kernel):
    r=np.zeros(np.array(x.shape)-np.array(kernel.shape)+1)
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            r[i,j]=(x[i:i+kernel.shape[0],j:j+kernel.shape[1]]*kernel).sum()
    return r

def kernelGaussiano(n):
    r=list()
    j=0
    for i in range(n):
        r.append(np.math.factorial(n-1)/(np.math.factorial(n-1-j)*np.math.factorial(j)))
        j+=1
    r=np.array(r).astype(int).reshape(n,1)
    r=np.dot(r,r.transpose())
    return  r/np.sum(r)

def kernelBartlett(dim=1):
    n=round(dim/2+0.5)
    r=np.concatenate((np.arange(1,n+1,1),np.arange(n-1,0,-1))).reshape(2*n-1,1)
    r=np.dot(r,r.transpose())
    return r/np.sum(r)
def kernelIdentidad(n):
    r=np.zeros((n,n))

def kernelSobel(d):
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

def convolucionar2(x,kernel):
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
        
## Para laplacianos clipear el resultado con 0 y 1 o 0 y 255
l4=np.array((0,-1,0,-1,4,-1,0,-1,0)).reshape(3,3)
l8=np.array((-1,-1,-1,-1,8,-1,-1,-1,-1)).reshape(3,3)
## Pasa altos cortes clipear el resultado con 0 y 1 o 0 y 255
p402=np.identity(3)+l4*0.2
p404=np.identity(3)+l4*0.4
p802=np.identity(3)+l8*0.2
p804=np.identity(3)+l8*0.4
##Pasa Banda (convolucionar2(x,kernelGaussiano(3)).clip(0,255)-convolucionar2(x,kernelGaussiano(5)).clip(0,255)).clip(0,1)*255
#(x+convolucionar2(x,l8).clip(0,255)*0.2).clip(0,255)
x=imageio.imread("figura19.bmp")
r=convolucionar2(x,np.ones((3,3))/5).clip(0,255)
#((convolucionar2(x,np.ones((1,3))/3).clip(0,255)-convolucionar2(x,kernelGaussiano(5)).clip(0,255)).clip(0,1)*255).astype(int)
plot.subplot(121)
plot.imshow(x,"gray")
plot.subplot(122)
plot.imshow(r,"gray")
plot.show()





