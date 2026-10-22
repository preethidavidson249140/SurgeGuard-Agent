

import os
import requests
import json

API_KEY = os.getenv("DIFY_API_KEY")
API_URL = "https://api.dify.ai/v1"


def run_surgeguard(inputs):
    if not API_KEY:
        raise ValueError(
            "DIFY_API_KEY is missing. Set it in the terminal first."
        )

    response = requests.post(
        f"{API_URL}/workflows/run",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "inputs": inputs,
            "response_mode": "blocking",
            "user": "surgeguard-demo-user",
        },
        timeout=60,
    )

    if not response.ok:
        print("Dify status code:", response.status_code)
        print("Dify error details:", response.text)
        return None

    return response.json()


if __name__ == "__main__":
    test_inputs = {
        "movement_mm": 6,
        "sensor_status": "NORMAL",
        "arg1": "gloves",
        "arg2": 5,
    }

    try:
        result = run_surgeguard(test_inputs)

        if result is not None:
            print("\nDify response:")
            print(json.dumps(result, indent=2))

    except Exception as error:
        print("Connection failed:", error)
