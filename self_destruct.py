import time
import os

def self_destruct(filename, ttl=60):
    time.sleep(ttl)  # Wait for TTL to expire
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} deleted after {ttl} seconds.")
    else:
        print(f"{filename} does not exist.")

# Example usage
self_destruct('voice_message.wav', ttl=30)
