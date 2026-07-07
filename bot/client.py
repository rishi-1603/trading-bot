import time
import hmac
import hashlib
from urllib.parse import urlencode
import requests


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com", logger=None):
        self.api_key = api_key.strip()
        self.api_secret = api_secret.strip()
        self.base_url = base_url.rstrip("/")
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.time_offset_ms = 0
        self.sync_time()

    def sync_time(self):
        url = f"{self.base_url}/fapi/v1/time"
        try:
            r = self.session.get(url, timeout=10)
            data = r.json()
            server_time = int(data["serverTime"])
            local_time = int(time.time() * 1000)
            self.time_offset_ms = server_time - local_time
            if self.logger:
                self.logger.info(f"SERVER TIME SYNC | server={server_time} local={local_time} offset_ms={self.time_offset_ms}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"TIME SYNC ERROR: {e}")
            self.time_offset_ms = 0

    def _sign_params(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000) + self.time_offset_ms
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def place_order(self, payload: dict) -> dict:
        url = f"{self.base_url}/fapi/v1/order"
        signed_payload = self._sign_params(payload.copy())

        if self.logger:
            self.logger.info(f"REQUEST POST {url} | payload={signed_payload}")

        response = self.session.post(url, params=signed_payload, timeout=15)
        data = response.json()

        if self.logger:
            self.logger.info(f"RESPONSE status={response.status_code} body={data}")

        if response.status_code == 400 and data.get("code") == -1021:
            self.sync_time()
            signed_payload = self._sign_params(payload.copy())
            if self.logger:
                self.logger.info(f"RETRY REQUEST POST {url} | payload={signed_payload}")
            response = self.session.post(url, params=signed_payload, timeout=15)
            data = response.json()
            if self.logger:
                self.logger.info(f"RETRY RESPONSE status={response.status_code} body={data}")

        response.raise_for_status()
        return data