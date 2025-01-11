FROM python:3.9-slim

WORKDIR /app

COPY grpc_server/server.py /app/server.py
COPY grpc_server/__init__.py /app/__init__.py

COPY vehicle_pb2.py /app/vehicle_pb2.py
COPY vehicle_pb2_grpc.py /app/vehicle_pb2_grpc.py

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
