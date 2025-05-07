import threading
import time
import serial
import serial.tools.list_ports
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Estado inicial
espacios = {
    "A1": "verde",
    "A2": "verde",
    "A3": "verde",
    "A4": "verde"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estado")
def estado():
    return jsonify(espacios)

# ---------------- SERIAL ----------------

arduino = None

def detectar_puerto():
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        if "USB Serial Device" in puerto.description:
            return puerto.device
    return None

def leer_arduino():
    global arduino
    puerto = detectar_puerto()
    if puerto is None:
        print("❌ Arduino no detectado.")
        return
    try:
        arduino = serial.Serial(puerto, 9600, timeout=1)
        print(f"✅ Conectado a {puerto}")
        time.sleep(2)
        while True:
            if arduino.in_waiting > 0:
                mensaje = arduino.readline().decode().strip()
                print(f"📩 Recibido: {mensaje}")
                actualizar_espacios_desde_serial(mensaje)
    except Exception as e:
        print(f"⚠️ Error al leer Arduino: {e}")

def actualizar_espacios_desde_serial(mensaje):
    ocupados = mensaje.split(",") if mensaje != "ninguno" else []
    for slot in espacios.keys():
        espacios[slot] = "rojo" if slot in ocupados else "verde"

# ---------------- MAIN ----------------

if __name__ == "__main__":
    hilo_serial = threading.Thread(target=leer_arduino)
    hilo_serial.daemon = True
    hilo_serial.start()

    app.run(debug=False)