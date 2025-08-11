#!/usr/bin/env python3
"""
Keep-alive service to prevent Render free tier from sleeping.
Pings the API every 5 minutes to maintain activity.
"""

import time
import requests
import threading
import logging
import os
from datetime import datetime

class KeepAliveService:
    def __init__(self, ping_interval=300):  # 5 minutes in seconds
        self.ping_interval = ping_interval
        self.is_running = False
        self.thread = None
        
        # Get the base URL - try environment variable first, fallback to localhost
        self.base_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:5000')
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        """Start the keep-alive service"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
            self.thread.start()
            self.logger.info(f"Keep-alive service started - pinging {self.base_url} every {self.ping_interval} seconds")
    
    def stop(self):
        """Stop the keep-alive service"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        self.logger.info("Keep-alive service stopped")
    
    def _keep_alive_loop(self):
        """Main keep-alive loop"""
        # Wait 2 minutes before starting pings to let the app fully start
        time.sleep(120)
        
        while self.is_running:
            try:
                self._ping_server()
                time.sleep(self.ping_interval)
            except Exception as e:
                self.logger.error(f"Keep-alive error: {str(e)}")
                # Continue running even if ping fails
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _ping_server(self):
        """Send a ping request to keep the server active"""
        try:
            # Use the health endpoint for keep-alive pings
            response = requests.get(
                f"{self.base_url}/health",
                timeout=30,
                headers={'User-Agent': 'KeepAlive/1.0'}
            )
            
            if response.status_code == 200:
                self.logger.info(f"Keep-alive ping successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                self.logger.warning(f"Keep-alive ping returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Keep-alive ping failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error in keep-alive ping: {str(e)}")

# Global instance
keep_alive_service = KeepAliveService()

def start_keep_alive():
    """Start the keep-alive service"""
    keep_alive_service.start()

def stop_keep_alive():
    """Stop the keep-alive service"""
    keep_alive_service.stop()