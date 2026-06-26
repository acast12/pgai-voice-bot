import requests
import time
from scenarios import SCENARIOS

if __name__ == "__main__":
    for scenario in SCENARIOS[9:10]:
        print(f"Launching: {scenario['name']}")
        requests.post("http://localhost:5000/launch", json={"scenario_id": scenario["id"]})
        time.sleep(180)
        

