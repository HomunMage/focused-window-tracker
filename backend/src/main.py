from fastapi import FastAPI, Request, HTTPException
from prometheus_client import make_asgi_app, Counter, Gauge, Histogram, start_http_server, Info
import json
import time

app = FastAPI()

# Prometheus metrics
window_updates_total = Counter("window_updates_total", "Total number of window updates received")
current_window_name = Gauge("current_window_name", "Current active window name", ["window_name"])
request_latency = Histogram("request_latency_seconds", "Latency of update requests")

# Start Prometheus HTTP server on port 17891 (within the container)
start_http_server(17891)

# Prometheus endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

last_window_name = None


@app.post("/update")
async def update_window_name(request: Request):
    global last_window_name
    with request_latency.time():
        try:
            data = await request.json()
            window_name = data.get("window_name")
            if not window_name:
                raise HTTPException(status_code=400, detail="window_name is required")

            window_updates_total.inc()
            
            if window_name != last_window_name:
                 if last_window_name is not None:
                     current_window_name.labels(last_window_name).set(0) #Set old name to 0
                 current_window_name.labels(window_name).set(1) #Set current name to 1
                 last_window_name = window_name


            return {"message": "Window name updated successfully", "window_name": window_name}

        except json.JSONDecodeError:
          raise HTTPException(status_code=400, detail="Invalid JSON")