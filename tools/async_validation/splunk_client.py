from utils.clients.base import LoggedResponse, ResponseNotFound  # noqa: F401


class SplunkClient:
    """Fetches the IIB response for a transaction id from Splunk via Playwright."""

    def __init__(self, playwright):
        self._playwright = playwright
        self._browser = None  # launched and logged in lazily on first get_response()

    def get_response(self, transaction_id: str) -> LoggedResponse:
        # TODO: launch browser + log in once, run the search for transaction_id,
        # extract the response body (and status code if logged).
        # Raise ResponseNotFound if there are no results.
        raise NotImplementedError("SplunkClient.get_response is not implemented yet")

    def close(self):
        if self._browser:
            self._browser.close()
