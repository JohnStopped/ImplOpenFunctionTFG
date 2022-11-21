from flask import Flask, request, redirect
import numpy as np
import cv2
import os

def quitaFondo(img_src):
    # Convertir la imagen a escala de grises
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

    # Creamos una imagen con histiéresis para eliminar ciertos valores de grises que será el canal alfa
    img_whiteless = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)[1]
    img_whiteless = 255 - img_whiteless
    
    # Para perfeccionar los bordes de esta imagen aplicamos un filtro de blur (hace partes borrosas)
    img_whiteless = cv2.GaussianBlur(img_whiteless, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)
    
    # Estiramiento lineal, los valores a 127 se convierten en 0 (255 se mantiene en 255)
    img_whiteless = (2*(img_whiteless.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # Montamos la imagen resultado
    result = img_src.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = img_whiteless
    
    return result

def main(request):
    if len(request.files.to_dict(flat=True))==0:
            return make_response({"msg": "No has enviado fichero con la imagen"})

    else:        
        # Recoger imagen de la petición
        files = request.files.to_dict(flat=True)
        img_file = files['image']
        img_file.save(os.environ['HOME'] + "/" + img_file.filename)
        img = cv2.imread(os.environ['HOME'] + "/" + img_file.filename)
        
        # Procesar la imagen
        res_img = quitaFondo(img)

        # Codificamos la imagen en png
        res_array_img = cv2.imencode('.png',res_img)[1] # [0] es un bool que indica el resultado de la operación

