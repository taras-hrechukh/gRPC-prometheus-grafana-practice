import grpc
import time
import random
from google.protobuf.json_format import MessageToDict
from vehicle_pb2_grpc import VehicleServiceStub
from vehicle_pb2 import VehicleData


def generate_random_vehicle_data():
    """Generate random vehicle data."""
    return VehicleData(
        speed=random.uniform(0, 120),  # Speed in km/h
        rpm=random.uniform(500, 7000),  # Engine RPM
        longitude=random.uniform(-180, 180),  # Longitude
        latitude=random.uniform(-90, 90),  # Latitude
        state_of_charge=random.uniform(0, 100),  # Battery SOC in percentage
    )


def run():
    """Send vehicle data to the server every second."""
    with grpc.insecure_channel('grpc_server:50051') as channel:
        stub = VehicleServiceStub(channel)
        print("Sending vehicle data to the server...")

        def vehicle_data_stream():
            while True:
                data = generate_random_vehicle_data()
                data_dict = MessageToDict(data)  # Convert VehicleData to a dictionary
                print(f"Sending: {data_dict}")
                yield data
                time.sleep(5)

        response = stub.SendVehicleData(vehicle_data_stream())
        print(f"Server response: {response.message}")


if __name__ == "__main__":
    run()
