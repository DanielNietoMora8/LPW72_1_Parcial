Este proyecto en Python permite analizar archivos multimedia (imágenes y audios) ubicados en una carpeta. 
El programa genera un reporte en formato CSV y muestra visualizaciones gráficas del contenido procesado.

Antes de ejecutar este proyecto, asegúrate de lo siguiente:

1.Tener Python 3.10 o superior instalado en tu sistema.
 
2. Tener `pip` actualizado:
   bash (cmd)
   * python -m pip install --upgrade pip

3. Instalar las bibliotecas necesarias:
(cmd)
	* pip install numpy pandas matplotlib opencv-python librosa
	* pip install ffmpeg-python

espera a que se instale o se actualicen los programas

4. Clona el repositorio desde GitHub:
	* git clone https://github.com/tu_usuario/tu_repositorio.git
	* cd tu_repositorio

5. Agrega tus imágenes y audios en la carpeta fotos_audios.

6. Ejecuta el programa desde la terminal o CMD:
	* python multimedia.py

7. Se generará un archivo reporte_multimedia.csv con el análisis.
   También se abrirá una ventana con gráficas sobre:

	La duración de los audios.
	La distribución de resoluciones de imagen.

8. Si ves un mensaje como No se pudo cargar la imagen, asegúrate de que el archivo no esté dañado.
   Si te falta alguna librería, instálala con pip install nombre_libreria.

Desarrollado como parte del curso de Lenguaje de Programación I — 2025-1
Autor: Juan Marín