from flask import Flask, jsonify, render_template
import serial
import serial.tools.list_ports
import threading
import time

app = Flask(__name__)
estados = {"A1": "rojo", "A2": "rojo", "A3": "rojo", "A4": "rojo"}
arduino = None

def detectar_puerto():
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        if "Arduino" in puerto.description or "CH340" in puerto.description or "USB-SERIAL" in puerto.description:
            return puerto.device
    return None

def iniciar_arduino():
    global arduino
    puerto_detectado = detectar_puerto()
    if puerto_detectado:
        try:
            arduino = serial.Serial(puerto_detectado, 9600, timeout=1)
            print(f"Arduino conectado en {puerto_detectado}")
        except serial.SerialException as e:
            print(f"No se pudo abrir el puerto {puerto_detectado}: {e}")
    else:
        print("No se detectó ningún Arduino conectado.")

def leer_datos():
    global estados
    while True:
        try:
            if arduino and arduino.in_waiting:
                linea = arduino.readline().decode('utf-8').strip()
                print(f"Datos recibidos: {linea}")  # Log para depurar
                if linea:
                    disponibles = linea.split(",")
                    for slot in estados:
                        estados[slot] = "verde" if slot in disponibles else "rojo"
        except Exception as e:
            print("Error leyendo desde el Arduino:", e)
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estado')
def estado():
    return jsonify(estados)

if __name__ == '__main__':
    iniciar_arduino()
    hilo = threading.Thread(target=leer_datos, daemon=True)
    hilo.start()
    app.run(debug=True)
