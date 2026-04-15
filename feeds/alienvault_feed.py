import os
import requests
from dotenv import load_dotenv

load_dotenv()
OTX_KEY = os.getenv("OTX_API_KEY")

def fetch_malicious_ips():
    url = "https://otx.alienvault.com/api/v1/indicators/export"
    headers = {"X-OTX-API-KEY": OTX_KEY}
    params = {"type": "IPv4"}
    
    print("Connecting to AlienVault OTX...")
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    
    if resp.status_code == 200:
        data = resp.json()   # ✅ FIX: use JSON
        indicators = data.get("results", [])
        
        ips = [item["indicator"] for item in indicators if item["type"] == "IPv4"]
        
        print(f"Got {len(ips)} malicious IPs from AlienVault")
        return ips
    else:
        print(f"Error: {resp.status_code}")
        return []

if __name__ == "__main__":
    ips = fetch_malicious_ips()
    for ip in ips[:5]:
        print(ip)