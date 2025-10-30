"""
State Broadcaster - Send robot state updates to WebSocket server
"""

import requests
from typing import Optional


class StateBroadcaster:
    """Send robot state updates to WebSocket server"""

    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        Initialize state broadcaster

        Args:
            server_url: URL of the WebSocket server
        """
        self.server_url = server_url
        self.enabled = True

    def send_state(self, state: str, text: str = ""):
        """
        Send state update to server

        Args:
            state: Robot state (idle, listening, thinking, speaking)
            text: Optional text to display
        """
        if not self.enabled:
            return

        try:
            response = requests.post(
                f"{self.server_url}/state",
                params={"state": state, "text": text},
                timeout=1
            )
            if response.status_code == 200:
                print(f"📡 State broadcasted: {state}")
            else:
                print(f"⚠️  Failed to broadcast state: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️  WebSocket server not running - UI won't update")
            self.enabled = False  # Disable further attempts
        except Exception as e:
            print(f"⚠️  Error broadcasting state: {e}")

    def idle(self, text: str = ""):
        """Set state to idle"""
        self.send_state("idle", text)

    def listening(self, text: str = "Listening..."):
        """Set state to listening"""
        self.send_state("listening", text)

    def thinking(self, text: str = "Processing..."):
        """Set state to thinking"""
        self.send_state("thinking", text)

    def speaking(self, text: str = ""):
        """Set state to speaking"""
        self.send_state("speaking", text)


# Example usage
if __name__ == "__main__":
    import time

    broadcaster = StateBroadcaster()

    print("Testing state broadcaster...")

    broadcaster.idle("Ready")
    time.sleep(2)

    broadcaster.listening("Recording audio...")
    time.sleep(3)

    broadcaster.thinking("Processing with LLM...")
    time.sleep(2)

    broadcaster.speaking("Hello! How can I help you?")
    time.sleep(3)

    broadcaster.idle("Ready for next student")
