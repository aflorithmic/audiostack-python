from unittest.mock import Mock, patch

import pytest

import audiostack
from audiostack.helpers.request_interface import RequestInterface


@patch("audiostack.helpers.request_interface.open")
@patch("audiostack.helpers.request_interface.shutil")
@patch("audiostack.helpers.request_interface.requests")
def test_RequestInterface_download_url(
    mock_requests: Mock, mock_shutil: Mock, mock_open: Mock, tmp_path: str
) -> None:
    mock_requests.get.return_value.status_code = 200

    RequestInterface.download_url(url="foo", name="bar", destination=tmp_path)
    mock_requests.get.assert_called_once_with(
        url="foo",
        stream=True,
        headers={
            "x-api-key": audiostack.api_key,
            "x-python-sdk-version": audiostack.sdk_version,
        },
    )
    mock_open.assert_called_once_with(f"{tmp_path}/bar", "wb")
    mock_shutil.copyfileobj.assert_called_once()


@patch("audiostack.helpers.request_interface.open")
@patch("audiostack.helpers.request_interface.shutil")
@patch("audiostack.helpers.request_interface.requests")
def test_RequestInterface_download_url_assume_org(
    mock_requests: Mock, mock_shutil: Mock, mock_open: Mock, tmp_path: str
) -> None:
    mock_requests.get.return_value.status_code = 200
    audiostack.assume_org_id = "child_org_id"  # type: ignore
    RequestInterface.download_url(url="foo", name="bar", destination=tmp_path)
    mock_requests.get.assert_called_once_with(
        url="foo",
        stream=True,
        headers={
            "x-api-key": audiostack.api_key,
            "x-python-sdk-version": audiostack.sdk_version,
            "x-assume-org": "child_org_id",
        },
    )
    mock_open.assert_called_once_with(f"{tmp_path}/bar", "wb")
    mock_shutil.copyfileobj.assert_called_once()

    # Resetting value after test
    audiostack.assume_org_id = None  # type: ignore


@patch("audiostack.helpers.request_interface.requests")
def test_RequestInterface_download_url_4XX(
    mock_requests: Mock,
) -> None:
    mock_requests.get.return_value.status_code = 400
    with pytest.raises(Exception):
        RequestInterface.download_url(url="foo", name="bar", destination="baz")
