# -*- coding: utf-8 -*-
"""
Created on Wed May 21 18:28:35 2025

@author: co232
"""
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Clase padre
class Multimedia:
    def __init__(self, ruta):
        self.ruta = ruta #ruta del archivo
        self.nombre = ruta.split("/")[-1] #separa solo el nombre

    def features(self): #metodo que se implementara en la subclase extraer caracteristicas
        pass

    def info(self): #método que se implementara en la subclase resumen de datos
        pass

# Clase imagen (hija)
class Imagen(Multimedia):
    def features(self): # Extrae características de la imagen como tamaño, dimensiones y color promedio
        imagen = cv2.imread(self.ruta) #lee la imagen
        
        self.alto, self.ancho, self.canales = imagen.shape #alto, ancho, canales
        self.tamano_bytes = len(imagen.tobytes()) #tamaño del archivo en bytes
        self.color_promedio = imagen.mean(axis=0).mean(axis=0) #BGR promedio

        with open(self.ruta, "rb") as f:
            f.seek(0, 2)
            self.tamano = f.tell()

    def info(self): #retorna un diccionario con info resumida de la imagen
        return {
            "archivo": self.nombre,
            "ancho": self.ancho,
            "alto": self.alto,
            "tamano_kb": round(self.tamano / 1024, 2),
            "color_r": round(self.color_promedio[2], 1),
            "color_g": round(self.color_promedio[1], 1),
            "color_b": round(self.color_promedio[0], 1),
        }

# Analizar carpeta de imágenes
def analizar_imagenes(carpeta="imagenes"): #se utiliza libreria glob para leer el contenido de la carpeta
    rutas = glob.glob(f"{carpeta}/*.[jp][pn]g") + glob.glob(f"{carpeta}/*.jpeg")  
    datos = []

    for ruta in rutas:
        imagen = Imagen(ruta)
        try:
            imagen.features()
            datos.append(imagen.info())
        except Exception as e:
            print(f"Error en {ruta}: {e}")
    
    return pd.DataFrame(datos)

# Visualización
def visualizar(df):
    # Gráfico 1: ancho vs alto
    plt.figure(figsize=(10, 5))
    plt.scatter(df["ancho"], df["alto"], color='darkorange')
    plt.xlabel("Ancho (px)")
    plt.ylabel("Alto (px)")
    plt.title("Relación entre ancho y alto de las imágenes")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("relacion_ancho_alto.png")
    plt.show()

    # Gráfico 2: tamaño en KB por archivo
    plt.figure(figsize=(10, 5))
    plt.bar(df["archivo"], df["tamano_kb"], color='mediumseagreen')
    plt.xlabel("Archivo de imagen")
    plt.ylabel("Tamaño (KB)")
    plt.title("Tamaño de las imágenes en kilobytes")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("tamano_imagenes.png")
    plt.show()

# ---- EJECUCIÓN ----
df = analizar_imagenes("imagenes")
df.to_csv("resumen_imagenes.csv", index=False)
print("Resumen guardado en 'resumen_imagenes.csv'")
visualizar(df)
