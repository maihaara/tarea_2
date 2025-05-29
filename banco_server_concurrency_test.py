from fastapi import FastAPI
from banco.main import app as banco_app
import argparse
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecutar API del Banco con configuración de concurrencia personalizada.")
    
    parser.add_argument(
        "--host", type=str, default="0.0.0.0",
        help="Dirección del host. Por defecto: 0.0.0.0"
    )
    
    parser.add_argument(
        "--port", type=int, default=8001,
        help="Puerto de ejecución. Por defecto: 8001"
    )
    
    parser.add_argument(
        "--limit-concurrency", type=int, default=20,
        help="Número máximo de conexiones concurrentes. Por defecto: 20"
    )

    parser.add_argument(
        "--backlog", type=int, default=1000,
        help="Tamaño del backlog para conexiones pendientes. Por defecto: 1000"
    )
    
    args = parser.parse_args()

    print(f"\nIniciando API Banco con limit_concurrency={args.limit_concurrency} en el puerto {args.port}...\n")

    uvicorn.run(
        banco_app,
        host=args.host,
        port=args.port,
        backlog=args.backlog,
        limit_concurrency=args.limit_concurrency
    )
