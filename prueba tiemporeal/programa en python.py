from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Estado inicial del estacionamiento
parking_state = {
    'A1': 'ocupado',
    'A2': 'libre',
    'A3': 'ocupado',
    'A4': 'libre'
}

@app.route('/')
def index():
    return render_template('index.html')

# Manejo de eventos WebSocket: cuando un cliente se conecta
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    # Enviar el estado inicial del estacionamiento al cliente
    emit('estado_estacionamiento', parking_state)

# Manejo de eventos WebSocket: cuando se recibe un cambio de estado
@socketio.on('cambiar_estado')
def handle_estado(data):
    global parking_state
    parking_state = data
    print('Estado actualizado:', parking_state)
    # Enviar el nuevo estado a todos los clientes
    emit('estado_estacionamiento', parking_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
