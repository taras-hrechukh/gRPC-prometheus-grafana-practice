# Vehicle metrics tracking and visualizing system 

**Description:** Simple client-server metrics system.
Client generates random vehicle metrics and sends them through gRPC to the server.
Server includes prometheus client to collect and points and then show on Grafana dashboard.


## How to run locally

### Step 1: Install dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
  pip install -r requirements.txt
```

### Step 2: Run the gRPC server:
```bash
  python grpc_server/server.py
```
You should see the message about server start

### Step 3: Run the gRPC client:
```bash
  python grpc_client/client.py
```
You should see the message about client start, and generated data sent

You can check that server receiving sent data

### Step 4: Run Prometheus and Grafana locally:
You can run Prometheus and Grafana locally using Docker so you can use one from `docker-compose.yml`


## How to run complete system using docker-compose
To run all services by one command you can use `docker-compose`

```bash
  docker-compose up --build
```
Grafana UI will be available at http://localhost:3000

User and password are `admin` by default

When logged in you need to add Prometheus as data source:
1) search for "Add data source"
2) select "Prometheus" as data source
3) set Prometheus host to http://localhost:9090

When done you can add panel to your dashboard:
1) search for "Add panel"
2) select "Prometheus" data source if not set by default
3) select metric or multiple metrics

After that you should be able to see metrics flow in your Grafana dashboard