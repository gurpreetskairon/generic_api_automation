from utils.clients.base import LoggedResponse, ResponseNotFound  # noqa: F401


class AppInsightsClient:
    """Fetches the APIM response for a transaction id from Azure Application Insights."""

    def get_response(self, transaction_id: str) -> LoggedResponse:
        # TODO: authenticate, query Application Insights for transaction_id,
        # return the response body (and status code if logged).
        # Raise ResponseNotFound if there are no results.
        raise NotImplementedError("AppInsightsClient.get_response is not implemented yet")

    def close(self):
        pass
