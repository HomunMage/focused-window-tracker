from fastapi import FastAPI, Request, HTTPException
from prometheus_client import make_asgi_app, Counter, Gauge, Histogram, start_http_server, Info
import json

app = FastAPI()

# Prometheus metrics
window_updates_total = Counter("window_updates_total", "Total number of window updates received")
current_window_name = Info("current_window_name", "Currently active window name")
request_latency = Histogram("request_latency_seconds", "Latency of update requests")

# Start Prometheus HTTP server on port 17891 (within the container)
start_http_server(17891)

# Prometheus endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.post("/update")
async def update_window_name(request: Request):
    with request_latency.time():
        try:
            data = await request.json()
            window_name = data.get("window_name")
            if not window_name:
                raise HTTPException(status_code=400, detail="window_name is required")
            current_window_name.info({"window_name":window_name})
            window_updates_total.inc()
            return {"message": "Window name updated successfully", "window_name": window_name}

        except json.JSONDecodeError:
          raise HTTPException(status_code=400, detail="Invalid JSON")