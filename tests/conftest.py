import pytest
import subprocess
import time
import requests
import os
import json
from helpers.rest_api import RestApi

WIREMOCK_URL = "http://localhost:8080"


@pytest.fixture(scope="session", autouse=True)
def wiremock():
    import subprocess, requests, time, os, json

    print("\nStarting WireMock...")
    subprocess.run(["docker-compose", "up", "-d", "wiremock"], check=True)

    # Wait until WireMock admin endpoint is ready
    for _ in range(40):
        try:
            resp = requests.get(f"{WIREMOCK_URL}/__admin/mappings")
            if resp.status_code == 200:
                print("WireMock is ready.")
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("WireMock did not become ready in time.")

    # Load mappings
    mapping_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wiremock", "mappings")

    if os.path.exists(mapping_dir):
        print("Loading WireMock mappings...")
        for file_name in os.listdir(mapping_dir):
            if not file_name.endswith(".json"):
                continue
            path = os.path.join(mapping_dir, file_name)
            with open(path, "r") as f:
                mapping = json.load(f)
            requests.post(f"{WIREMOCK_URL}/__admin/mappings", json=mapping)
        print("All mappings loaded.")
    else:
        print("No mappings folder found, skipping load.")

    yield  # Run tests

    print("\nStopping WireMock...")
    subprocess.run(["docker-compose", "down"], check=True)
    print("WireMock stopped.")



@pytest.fixture(scope="session")
def base_url():
    """
    Base URL for the API under test.
    """
    return WIREMOCK_URL


@pytest.fixture(scope="session")
def token():
    """
    Mock token used for API calls.
    Replace with real token fetch if required.
    """
    return "mock-token"


@pytest.fixture
def api(base_url, token):
    """
    Creates a RestApi instance for each test dynamically.
    Tests can override the URL per call, so this provides a base RestApi helpers.
    """
    return lambda endpoint: RestApi(f"{base_url}{endpoint}", token)
