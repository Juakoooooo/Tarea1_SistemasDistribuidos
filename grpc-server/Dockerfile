FROM python:3.9-slim

WORKDIR /app

COPY . .

# Instala las dependencias del sistema necesarias para 'dig'
RUN apt-get update && apt-get install -y dnsutils

RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["python", "grpc_server.py"]
