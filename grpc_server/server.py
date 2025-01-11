import grpc
from concurrent import futures
import time
from google.protobuf.json_format import MessageToDict
from prometheus_client import start_http_server as start_http_prometheus_server, Counter, Gauge
from vehicle_pb2_grpc import VehicleServiceServicer, add_VehicleServiceServicer_to_server
from vehicle_pb2 import Response

# Prometheus metrics
VEHICLE_DATA_COUNT = Counter('vehicle_data_count', 'Number of vehicle data messages received')
VEHICLE_SPEED = Gauge('vehicle_speed', 'Vehicle speed in km/h')
VEHICLE_RPM = Gauge('vehicle_rpm', 'Vehicle engine RPM')
VEHICLE_LONGITUDE = Gauge('vehicle_longitude', 'Vehicle longitude')
VEHICLE_LATITUDE = Gauge('vehicle_latitude', 'Vehicle latitude')
VEHICLE_SOC = Gauge('vehicle_state_of_charge', 'Vehicle battery state of charge in percentage')

class VehicleService(VehicleServiceServicer):
    def SendVehicleData(self, request_iterator, context):
        for vehicle_data in request_iterator:
            data_dict = MessageToDict(vehicle_data)
            print(f"Received: {data_dict}")

            # Update Prometheus metrics
            VEHICLE_DATA_COUNT.inc()
            VEHICLE_SPEED.set(vehicle_data.speed)
            VEHICLE_RPM.set(vehicle_data.rpm)
            VEHICLE_LONGITUDE.set(vehicle_data.longitude)
            VEHICLE_LATITUDE.set(vehicle_data.latitude)
            VEHICLE_SOC.set(vehicle_data.state_of_charge)

        return Response(message="Data received successfully")

def serve():
    # Start Prometheus metrics HTTP server
    start_http_prometheus_server(8000)  # Prometheus will scrape metrics from this port
    print("Prometheus metrics available on port 8000")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_VehicleServiceServicer_to_server(VehicleService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
