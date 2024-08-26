import subprocess
from config import POOL_URL, WALLET_ADDRESS, WORKER_NAME, WORKER_PASSWORD

def start_cpu_mining():
    """
    Starts CPU mining using cpuminer on the VPS.
    """
    command = f"minerd -a scrypt -o {POOL_URL} -O {WORKER_NAME}:{WORKER_PASSWORD} --coinbase-addr={WALLET_ADDRESS} -t 1"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_mining(process):
    """
    Stops the mining process.
    """
    process.terminate()
