import win32gui
import time
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_active_window_title():
    """Gets the title of the currently active window."""
    try:
        window_handle = win32gui.GetForegroundWindow()
        if window_handle:
            title = win32gui.GetWindowText(window_handle)
            return title
        else:
            return ""
    except Exception as e:
        logging.error(f"Error getting window title: {e}")
        return ""

def send_window_update(window_title):
    """Sends the window title to the backend API."""
    url = "http://localhost:17892/update"
    headers = {'Content-Type': 'application/json'}
    data = {'window_name': window_title}
    try:
      response = requests.post(url, headers=headers, data=json.dumps(data))
      response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
      if response.status_code == 200:
         logging.info(f"Window name updated: {window_title}")
      else:
         logging.warning(f"Request successful but return code: {response.status_code}, response body: {response.text}")
    except requests.exceptions.RequestException as e:
      logging.error(f"Failed to update window name: {e}")

if __name__ == "__main__":
    logging.info("Starting window monitor script...")
    last_title = None
    while True:
       title = get_active_window_title()
       if title and title != last_title:
           send_window_update(title)
           last_title = title
       time.sleep(1)