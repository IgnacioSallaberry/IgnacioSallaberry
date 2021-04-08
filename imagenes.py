# -*- coding: utf-8 -*-
"""
Created on Fri May 22 19:21:02 2020

@author: Ignacio Sallaberry
"""
from PIL import Image
import numpy as np
from skimage import io
from tifffile import imsave


def Imagenes_2(name, numero_de_imagenes, DIVIDER=2):
####  ------------------------    armo los nombres de las imágenes      -------------------
    indice = np.asarray(['%03d' % x for x in range(2,numero_de_imagenes+1)])
####  ------------------------    PARA UNA IMAGEN    -------------------
    im = Image.open(name)   #importa la imagen .tif
    im = np.array(im) #crea una matriz de valores de la imagen importada
    im = (np.array(im)/DIVIDER).astype(int) ## los valores de cada pixel de la imagen están divididos por 2 en el simFCS, además tomo la parte entera para que no quede 2.5 por ejemplo
    # im = []
    #creo que ese dividido 2 es el "DIVIDER" del simFCS
    imarray = [im.tolist()]
    
####  ------------------------    armo array con las matrices de las 100 imágenes  -------------------
    i=0
    while i<len(indice):
        im = Image.open(name[:len(name)-7]+indice[i]+'.tif')
        im = (np.array(im)/DIVIDER).astype(int) ## los valores de cada pixel de la imagen están divididos por 2 en el simFCS, además tomo la parte entera para que no quede 2.5 por ejemplo
        imarray.append(im.tolist())
        print(indice[i])    
        i+=1
    imarray = np.array(imarray)  ##esto convierte los datos en matrices
    
    return imarray



def Imagenes(name,DIVIDER=2):
    #    
####  ------------------------    PARA UNA IMAGEN    -------------------
    im = Image.open(name)   #importa la imagen .tif
#    im = np.array(im) #crea una matriz de valores de la imagen importada
    im = (np.array(im)/DIVIDER).astype(int) ## los valores de cada pixel de la imagen están divididos por 2 en el simFCS, además tomo la parte entera para que no quede 2.5 por ejemplo
    #creo que ese dividido 2 es el "DIVIDER" del simFCS
    imarray = [im.tolist()]
    print ('001.tif')
####  ------------------------    armo los nombres de los archivos    -------------------
    i=2
    indice=[]
    while i<101:
        if i<10:
            indice.append(f'00{i}.tif')
        elif 9<i<100:
            indice.append(f'0{i}.tif')
        else:
            indice.append(f'{i}.tif')
        i+=1
####  ------------------------    armo array con las matrices de las 100 imágenes  -------------------
    i=0
    while i<len(indice):
        im = Image.open(name[:len(name)-7]+indice[i])
        im = (np.array(im)/DIVIDER).astype(int) ## los valores de cada pixel de la imagen están divididos por 2 en el simFCS, además tomo la parte entera para que no quede 2.5 por ejemplo
        imarray.append(im.tolist())
        print(indice[i])    
        i+=1
    imarray = np.array(imarray)  ##esto convierte los datos en matrices
    
    return imarray



def chromaslide(path,nombres, DIVIDER=2):
    # #==============================================================================
    # #     Permite: abrir varias mediciones de chromaslide solamente pasando el path, una lista con los nombres de las carpetas y el divider deseado
    # #    Devuelve: Matriz donde cada slice es UNA imagen.
    # #============================================================================== 
        
    imagenes=[]
    for i in nombres:
        k=Imagenes(path+i, DIVIDER=DIVIDER)
        for k in k:
            imagenes.append(k)
    
    return np.array(imagenes)


def stack_de_imagenes(name, DIVIDER=2, bits=np.uint16):
##==============================================================================
##                                Toma un stack de imagenes y devuelve un array donde cada slide es una imagen
##============================================================================== 
    im = (((io.imread(name)).astype(bits))/DIVIDER).astype(int)

    imagenes = [(im[0]).tolist()]
    i=1
    while i<len(im):
        imagenes.append((im[i]).tolist())
        i+=1
            
    imagenes = np.array(imagenes) 
    
    return np.array(imagenes)



def selector_de_imagenes(stack, primera_imagen=0, cantidad_de_imagenes=1, intervalo=1):
    imagenes = [(stack[primera_imagen]).tolist()]
    print(f'imagen{primera_imagen}')
    i=0
    j=intervalo
    while i<cantidad_de_imagenes-1:
        imagenes.append((stack[j]).tolist())
        print(f'imagen{j}')
        j+=intervalo
        i+=1
    imagenes = np.array(imagenes) 
    
    return imagenes



def guardar_imagen_por_imagen(array,ubicacion,nombre,bits=np.uint16):
    i=0
    while i<len(array):
        imagen = Image.fromarray(array[i].astype(bits)) # float32
        imagen.save(ubicacion+r'\{}{}.tif'.format(nombre,i), "TIFF")
        i+=1

def guardar_stack_de_imagenes(imagenes,ubicacion,nombre,bits=np.uint16):
    imsave(ubicacion+r'\{}.tif'.format(nombre), imagenes.astype(bits))

    