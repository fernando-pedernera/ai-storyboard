import cv2
import os
import glob
import numpy as np

def create_animatic(image_folder: str, output_video: str = "animatic.mp4", fps: int = 1):
    """
    Toma todas las imágenes (escenas) generadas por ComfyUI en la carpeta especificada
    y las une en un archivo de video (animática) con una duración por frame.
    """
    print(f"[*] Buscando imágenes generadas en: {image_folder}")
    
    # Buscar imágenes que empiecen con scene_ o storyboard_
    image_files = glob.glob(os.path.join(image_folder, "scene_*.png"))
    image_files.sort() # Asegurar orden secuencial
    
    if not image_files:
        print(f"Error: No se encontraron imágenes en {image_folder} para crear el video.")
        print("Asegúrate de ejecutar primero main_pipeline.py y tener las imágenes listas.")
        return

    # Leer la primera imagen para obtener el tamaño base
    first_frame = cv2.imread(image_files[0])
    height, width, layers = first_frame.shape
    size = (width, height)
    
    print(f"[*] Creando video {output_video} a {fps} FPS con resolución {width}x{height}")
    
    # Inicializar VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Formato MP4
    out = cv2.VideoWriter(output_video, fourcc, fps, size)
    
    # Escribir cada imagen en el video
    # Si queremos que cada imagen dure más (ej. 3 segundos), escribimos el frame varias veces
    seconds_per_image = 3
    
    for filename in image_files:
        print(f"  -> Añadiendo {filename}...")
        img = cv2.imread(filename)
        
        # Redimensionar por si alguna imagen tiene un tamaño diferente
        if (img.shape[1], img.shape[0]) != size:
            img = cv2.resize(img, size)
            
        for _ in range(fps * seconds_per_image):
            out.write(img)
            
    out.release()
    print(f" Video animática guardado con éxito como: {output_video}")

if __name__ == "__main__":
    print("=" * 60)
    print(" CREADOR DE ANIMÁTICAS - INICIANDO ")
    print("=" * 60)
    
    # En nuestro ejemplo, las imágenes se guardan en la raíz o en una carpeta /output
    current_dir = os.path.dirname(os.path.abspath(__file__))
    create_animatic(image_folder=current_dir, output_video="storyboard_pitch.mp4", fps=24)
