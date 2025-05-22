#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import cv2
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ArchivoMultimedia:
    def __init__(self, ruta_archivo):
        self.ruta = ruta_archivo
        self.nombre = os.path.basename(ruta_archivo)

    def analizar(self):
        raise NotImplementedError("Este método debe ser implementado por subclases.")

    def resumen(self):
        raise NotImplementedError("Este método debe ser implementado por subclases.")

class Imagen(ArchivoMultimedia):
    def analizar(self):
        self.imagen = cv2.imread(self.ruta)
        if self.imagen is None:
            raise ValueError(f"No se pudo cargar la imagen: {self.ruta}")

        self.altura, self.ancho = self.imagen.shape[:2]
        self.resolucion = f"{self.ancho}x{self.altura}"
        self.tamaño_kb = os.path.getsize(self.ruta) / 1024
        self.color_promedio = np.mean(self.imagen, axis=(0, 1)).astype(int)

    def resumen(self):
        return {
            "tipo": "imagen",
            "nombre": self.nombre,
            "resolucion": self.resolucion,
            "ancho": self.ancho,
            "alto": self.altura,
            "tamaño_kb": round(self.tamaño_kb, 2),
            "color_promedio": tuple(self.color_promedio)
        }

class Audio(ArchivoMultimedia):
    def analizar(self):
        self.audio, self.sr = librosa.load(self.ruta, sr=None)
        self.duracion = librosa.get_duration(y=self.audio, sr=self.sr)
        self.tamaño_kb = os.path.getsize(self.ruta) / 1024

    def resumen(self):
        return {
            "tipo": "audio",
            "nombre": self.nombre,
            "duracion_seg": round(self.duracion, 2),
            "frecuencia_muestreo": self.sr,
            "tamaño_kb": round(self.tamaño_kb, 2)
        }

def procesar_carpeta(ruta_carpeta):
    datos = []
    extensiones_imagen = ('.jpg', '.jpeg', '.png', '.bmp')
    extensiones_audio = ('.wav', '.mp3')

    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        if archivo.lower().endswith(extensiones_imagen):
            archivo_obj = Imagen(ruta_completa)
        elif archivo.lower().endswith(extensiones_audio):
            archivo_obj = Audio(ruta_completa)
        else:
            continue

        try:
            archivo_obj.analizar()
            datos.append(archivo_obj.resumen())
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    return pd.DataFrame(datos)

ruta = "./fotos_audios"

df_resultado = procesar_carpeta(ruta)

df_resultado.to_csv("reporte_multimedia.csv", index=False)
print("✅ Datos exportados a reporte_multimedia.csv")

def graficar_datos(df):
    plt.figure(figsize=(12, 5))

    if "duracion_seg" in df.columns:
        plt.subplot(1, 2, 1)
        df_audios = df[df["tipo"] == "audio"]
        plt.bar(df_audios["nombre"], df_audios["duracion_seg"], color='skyblue')
        plt.xticks(rotation=90)
        plt.title("Duración de Archivos de Audio")
        plt.ylabel("Segundos")

    if "resolucion" in df.columns:
        plt.subplot(1, 2, 2)
        df_imagenes = df[df["tipo"] == "imagen"]
        resoluciones = df_imagenes["resolucion"].value_counts()
        plt.bar(resoluciones.index, resoluciones.values, color='salmon')
        plt.title("Distribución de Resoluciones de Imagen")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

graficar_datos(df_resultado)

