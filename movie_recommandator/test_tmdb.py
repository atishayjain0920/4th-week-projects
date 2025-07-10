import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv
import logging
import socket

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    print("❌ TMDB_API_KEY not found.")
    exit()

query = "Inception"

# TMDB API endpoint
url = "https://api.themoviedb.org/3/search/movie"
params = {
    "api_key": api_key,
    "query": query,
    "language": "en-US",
    "page": 1,
    "include_adult": "false"
}
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Setup retry strategy
retry_strategy = Retry(
    total=3,  # Max retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
    allowed_methods=["GET"],  # Retry only on GET
    backoff_factor=1  # Wait 1s, 2s, 4s between retries
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

# Make request with retry and enhanced error handling
try:
    response = http.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("✅ API call successful. Number of results:", len(data.get("results", [])))
except requests.exceptions.Timeout as e:
    print("❌ API call timed out:", e)
except requests.exceptions.ConnectionError as e:
    # Check for ConnectionResetError inside ConnectionError
    if isinstance(e.args[0], socket.error):
        print("❌ Connection reset by peer or network error:", e)
    else:
        print("❌ Connection error:", e)
except requests.exceptions.HTTPError as e:
    status_code = e.response.status_code if e.response else "Unknown"
    print(f"❌ HTTP error {status_code}:", e)
except requests.exceptions.RequestException as e:
    print("❌ API call failed:", e)

# Suggestions for network/proxy/certificate issues:
print("\nSuggestions if you face connection reset or SSL errors:")
print("- Check your internet connection and firewall settings.")
print("- Try using a different network or VPN.")
print("- If behind a proxy, configure requests to use the proxy.")
print("- For SSL issues, consider verifying certificates or disabling SSL verification (not recommended for production).")
