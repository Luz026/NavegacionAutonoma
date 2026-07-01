import sys
sys.path.append('/Applications/Webots.app/Contents/lib/controller/python')

from controller import Keyboard, Camera
from vehicle import Driver
import numpy as np
import cv2
import csv
import os

def main():
    driver = Driver()
    timestep = int(driver.getBasicTimeStep())
    
    # Dispositivos
    camera = driver.getDevice("camera")
    camera.enable(timestep)
    keyboard = Keyboard()
    keyboard.enable(timestep)

    # Configuración de archivos
    if not os.path.exists('dataset'): os.makedirs('dataset')
    csv_file = open('dataset/data.csv', 'a', newline='') # 'a' para añadir datos si paras y sigues
    writer = csv.writer(csv_file)
    
    # Variables de control
    speed = 20.0
    nav_command = 2 # 1:Izq, 2:Recto, 3:Der
    angle = 0.0
    counter = 0

    print("--- CONTROLADOR Y RECOLECTOR LISTO ---")
    print("Flechas: Volante | 1,2,3: Comando | Esc: Salir")

    while driver.step() != -1:
        driver.setCruisingSpeed(speed)
        
        # Lectura de teclado
        key = keyboard.getKey()
        
        # Lógica de dirección (Suave)
        if key == Keyboard.LEFT: angle = max(angle - 0.05, -0.5)
        elif key == Keyboard.RIGHT: angle = min(angle + 0.05, 0.5)
        elif key == Keyboard.UP: angle = 0.0
            
        # Lógica de comandos de navegación
        if key == ord('1'): nav_command = 1
        elif key == ord('2'): nav_command = 2
        elif key == ord('3'): nav_command = 3
        
        driver.setSteeringAngle(angle)
        
        # Captura cada 5 pasos para tener un dataset más denso
        if counter % 5 == 0:
            img_name = f"dataset/img_{counter:05d}.png"
            raw_img = camera.getImage()
            img = np.frombuffer(raw_img, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
            cv2.imwrite(img_name, img[:, :, :3])
            writer.writerow([img_name, angle, nav_command])
            print(f"Grabando: Ángulo={angle:.2f} | Cmd={nav_command}")
        
        counter += 1

    csv_file.close()

if __name__ == "__main__":
    main()