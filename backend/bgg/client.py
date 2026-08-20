import time

import httpx


class BGGClient:
    BASE_URL = "https://boardgamegeek.com/xmlapi2"

    def __init__(
        self,
        timeout: float = 30.0,
        retry_delay: float = 5.0,
        max_retries: int = 5,
    ):
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.max_retries = max_retries

    def get_collection(self, username: str) -> str:
        url = f"{self.BASE_URL}/collection"

        params = {
            "username": username,
            "own": 1,
        }

        for attempt in range(self.max_retries):
            response = httpx.get(
                url,
                params=params,
                timeout=self.timeout,
            )

            if response.status_code == 202:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        "BGG collection request remained queued "
                        "after maximum retries"
                    )

                time.sleep(self.retry_delay)
                continue

            response.raise_for_status()

            return response.text

        raise RuntimeError("Unable to retrieve BGG collection")

    def get_game(self, bgg_id: int) -> str:
        url = f"{self.BASE_URL}/thing"

        params = {
            "id": bgg_id,
            "stats": 1,
        }

        for attempt in range(self.max_retries):
            response = httpx.get(
                url,
                params=params,
                timeout=self.timeout,
            )

            if response.status_code == 202:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        "BGG game request remained queued "
                        "after maximum retries"
                    )

                time.sleep(self.retry_delay)
                continue

            response.raise_for_status()

            return response.text

        raise RuntimeError("Unable to retrieve BGG game")