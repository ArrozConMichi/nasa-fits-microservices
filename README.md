# NASA FITS Microservices Dashboard

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3.12-blue.svg?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-4285F4?logo=grpc&logoColor=white)

Sistema de procesamiento y visualización de datos astronómicos (formato FITS) diseñado bajo arquitectura de microservicios utilizando gRPC, Django REST Framework, Docker y Astropy.

Este proyecto fue desarrollado como demostración técnica para experimentos y procesamiento distribuido de datos científicos.

## 📸 Captura

## 🏗️ Arquitectura
El sistema se divide en servicios desacoplados:

1. Fits-Metadata (gRPC): Servicio en Python/Astropy encargado de leer las cabeceras científicas de los archivos FITS.

2. Fits-Processor (gRPC): Servicio en Python/Matplotlib encargado del renderizado, normalización de histograma y conversión a formatos web.

3. API Gateway (Django): Fachada HTTP que traduce peticiones REST a gRPC para servir al frontend.

4. Frontend (Nginx): Interfaz web estática de alta velocidad.

## 🚀 Quick Start (Requisitos)
Necesitas tener instalado:
- Docker
- Docker Compose

## 💻 Instalación y Uso
1. Clonar el repositorio
2. git clone https://github.com/ArrozConMichi/nasa-fits-microservices.git
3. (Opcional) Generar datos de prueba:

* Este proyecto incluye un generador sintético para crear archivos FITS de carga, ejecutando el siguiente comando: `python generador.py`, esto creará archivos en la carpeta data/.
  
4. Levantar el sistema usando `docker compose up --build`
  
5. Para acceder, abre tu navegador en: http://localhost:8080

🛠️ Tech Stack
- Backend: Python 3.12, Django 5, gRPC, Astropy.
- Procesamiento: Matplotlib, NumPy.
- Orquestación: Docker, Docker Compose, Nginx.
- Protocol Buffers: Protobuf v3.
