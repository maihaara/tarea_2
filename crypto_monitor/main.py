import asyncio
import json
import random
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar carpeta static para servir crypto_monitor.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# Lista de criptomonedas disponibles (simuladas)
CRYPTOCURRENCIES = ["BTC", "ETH", "XRP", "LTC", "DOGE"]

# Manager para conexiones y preferencias
class ConnectionManager:
    def __init__(self):
        # Diccionario: WebSocket -> lista de criptos preferidas
        self.active_connections: Dict[WebSocket, List[str]] = {}

    async def connect(self, websocket: WebSocket, preferences: List[str]):
        await websocket.accept()
        self.active_connections[websocket] = preferences

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

manager = ConnectionManager()

# Endpoint para servir el archivo HTML
@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/crypto_monitor.html", "r", encoding="utf-8") as f:
        return f.read()

# Endpoint WebSocket corregido: aceptar antes de recibir datos
@app.websocket("/ws/crypto_prices")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Aceptar conexión primero
    try:
        # Recibir preferencias iniciales desde el cliente
        data = await websocket.receive_text()
        data_json = json.loads(data)
        preferences = data_json.get("preferences", CRYPTOCURRENCIES)

        # Guardar conexión con preferencias
        manager.active_connections[websocket] = preferences

        # Mantener conexión abierta
        while True:
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# Tarea de fondo para enviar precios simulados cada 3 segundos
@app.on_event("startup")
async def start_sending_crypto_prices():
    asyncio.create_task(send_crypto_prices_periodically())

async def send_crypto_prices_periodically():
    while True:
        await asyncio.sleep(3)
        # Simular precios aleatorios para todas las criptos
        prices = {crypto: round(random.uniform(10, 1000), 2) for crypto in CRYPTOCURRENCIES}

        to_remove = []
        for websocket, prefs in manager.active_connections.items():
            # Filtrar solo las criptos que el cliente quiere recibir
            filtered_prices = {c: prices[c] for c in prefs if c in prices}
            if not filtered_prices:
                continue
            try:
                # Enviar datos JSON al cliente
                await websocket.send_text(json.dumps(filtered_prices))
            except Exception:
                # Si error, desconectar para evitar problemas
                to_remove.append(websocket)

        for ws in to_remove:
            manager.disconnect(ws)

