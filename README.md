# focused-window-tracker
This project monitors active window names and visualizes them using Prometheus and Grafana. It's just like ActivityWatch.

## Overview

This project consists of three main components:

1.  **`backend`**: A Python FastAPI application that receives window name updates and exposes Prometheus metrics.
2.  **`prometheus`**: A Prometheus server that scrapes metrics from the `backend` application.
3.  **`grafana`**: A Grafana instance that visualizes the metrics stored in Prometheus as a timeline showing which window was active and how long.
4. **`Scripts/monitor.sh`**: A script that sends active window name to backend.


## Setup Instructions
1.  **Build the Docker Images**

    ```bash
    docker compose build
    ```

2.  **Start the Docker Containers**

    ```bash
    docker compose up -d
    ```

    This will start all services (`backend`, `prometheus`, and `grafana`) in detached mode.

3.  **Start the window monitor script**
    * Linux: 
    ```bash
      bash ./Scripts/monitor.sh
    ```
    
    * Windows:
    ```
    python ./Scripts/monitor.py
    ```

    This script will start sending requests to the backend.

4.  **Access Grafana**

    *   Open your web browser and go to `http://127.0.0.1:3000`.
    *   Log in with the default credentials:
        *   Username: `usr`
        *   Password: `pwd`

5.  **Configure Prometheus Data Source**

    *   In the Grafana sidebar, navigate to "Connections" (the plug icon).
    *   Click "Data sources."
    *   Click "Add data source."
    *   Search and select "Prometheus."
    *   Enter the Prometheus URL: `http://prometheus:9090`.
    *   Click "Save & test." You should see a "Successfully queried the Prometheus API" message.

6.  **Create the Visualization**

   * Create a new dashboard by navigating to "Dashboards" and click "New Dashboard"
   * Add a new panel of type "Time series".
   * In the "Query" section, enter the following Prometheus query: `current_window_name`
   * In the "Transform" tab, add the following transforms:
      *   Select 'Reduce' in dropdown, and 'Last (Not NaN)' in function dropdown, then 'Group By' and 'window_name' in the Group By dropdown
      *  Click 'Add Transform' and select 'Prepare Time Series'
      *   Click 'Add Transform' and select 'Organize fields' and Rename 'Value' to 'is_active'. Uncheck Timestamp, Select is_active and set Display style to 'Hidden'. Select window_name and select 'Type' as 'String'
      *   Click 'Add Transform' and select 'Filter by value'. Set the Filter to 'is_active' and select condition 'is equal to' and set value '1'
   * Go to display, and in the section 'Band' Select 'Gradient Mode' to 'Scheme' and set Scheme to 'Cool to Warm'.
    * In the Legend set mode to 'Table'
   * Save the dashboard.
