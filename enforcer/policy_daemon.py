import subprocess
import time
import logging
from db.mongo_handler import indicators

logging.basicConfig(
    filename="enforcer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

blocked_ips = set()

def block_ip(ip):
    if ip in blocked_ips:
        return
    result = subprocess.run(
        ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        blocked_ips.add(ip)
        logging.info(f"BLOCKED: {ip}")
        print(f"Blocked: {ip}")

def unblock_ip(ip):
    subprocess.run(
        ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
        capture_output=True, text=True
    )
    blocked_ips.discard(ip)
    print(f"Unblocked: {ip}")

print("Policy Enforcer started. Checking every 60 seconds...")
while True:
    all_ips = indicators.find({"type": "ip"})
    for doc in all_ips:
        block_ip(doc["value"])
    time.sleep(60)
