from datetime import datetime, timedelta, timezone

import pytest

from apps.services.integration_api.api_content import ApiRequestDetails
from apps.services.integration_soap.soap_content import IntegrationApiClient


@pytest.fixture()
def api_request_detail_obj(page):
    yield ApiRequestDetails(page)


# fixture definitions
@pytest.fixture(scope="session")
def api_client():
    return IntegrationApiClient()


@pytest.fixture
def batch_data(request):
    return request.param


@pytest.fixture(scope="session")
def formatted_datetime() -> str:
    nzst = timezone(timedelta(hours=12))
    return datetime.now(nzst).isoformat(timespec="seconds")
