import requests
import os
import time
import logging
from dotenv import load_dotenv
import os

load_dotenv()  
VT_API_KEY = os.getenv("VT_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3"

HEADERS = {
    "x-apikey": VT_API_KEY
}


def _safe_request(method, url, **kwargs):
    """
    Wrapper for safe API requests with error handling
    """
    try:
        response = requests.request(method, url, headers=HEADERS, timeout=15, **kwargs)

        if response.status_code == 429:
            return {"error": "Rate limit exceeded"}

        if response.status_code >= 400:
            return {
                "error": f"HTTP {response.status_code}",
                "details": response.text
            }

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# 🔍 URL ANALYSIS
def check_url(url):
    if not VT_API_KEY:
        return {"error": "API key missing"}

    try:
        # Step 1: Submit URL
        submit_resp = _safe_request(
            "POST",
            f"{BASE_URL}/urls",
            data={"url": url}
        )

        if "error" in submit_resp:
            return submit_resp

        analysis_id = submit_resp.get("data", {}).get("id")

        if not analysis_id:
            return {"error": "Failed to get analysis ID"}

        # Step 2: Poll for results (retry loop)
        for _ in range(3):
            time.sleep(2)

            report_resp = _safe_request(
                "GET",
                f"{BASE_URL}/analyses/{analysis_id}"
            )

            if "error" in report_resp:
                continue

            attributes = report_resp.get("data", {}).get("attributes", {})
            stats = attributes.get("stats", {})

            # If stats exist, return
            if stats:
                return {
                    "type": "url",
                    "target": url,
                    "stats": stats
                }

        return {
            "type": "url",
            "target": url,
            "error": "Analysis not ready"
        }

    except Exception as e:
        return {"error": str(e)}


# 🌐 IP ANALYSIS
def check_ip(ip):
    if not VT_API_KEY:
        return {"error": "API key missing"}

    try:
        resp = _safe_request(
            "GET",
            f"{BASE_URL}/ip_addresses/{ip}"
        )

        if "error" in resp:
            return resp

        attributes = resp.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})

        return {
            "type": "ip",
            "target": ip,
            "stats": stats
        }

    except Exception as e:
        return {"error": str(e)}