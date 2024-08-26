import subprocess
import time

def run_bot(timestamp):
    while True:
        subprocess.run(['python', 'bot/run.py'])  # Replace 'run.py' with the actual filename if different
        time.sleep(timestamp)  # Delay for 5 minutes (300 seconds)

if __name__ == "__main__":
    timestamp = 1000  # Delay in seconds
    run_bot(timestamp)