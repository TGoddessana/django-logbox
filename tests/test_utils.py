from datetime import datetime
from http import HTTPStatus
from unittest.mock import Mock

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from ua_parser import parse

from django_logbox.utils import browser_str, device_str, get_log_data, os_str


@pytest.fixture
def mock_get_request():
    request_factory = RequestFactory()
    request = request_factory.get(
        path="/api/v1/test/",
        data={"param1": "value1", "param2": "value2"},
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/132.0.0.0 Whale/4.30.291.11 Safari/537.36",
        },
    )
    return request


@pytest.fixture
def mock_get_request_without_user_agent():
    request_factory = RequestFactory()
    request = request_factory.get(
        path="/api/v1/test/",
        data={"param1": "value1", "param2": "value2"},
    )
    return request


@pytest.fixture
def mock_ok_response():
    response = Mock(spec=HttpResponse)
    response.status_code = HTTPStatus.OK
    return response


####################
# utils.device_str #
####################


def test_device_str():
    parsed_user_agents = [
        parse(user_agent)
        for user_agent in [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
        ]
    ]
    assert device_str(parsed_user_agents[0]) is None
    assert device_str(parsed_user_agents[1]) == "Mac(Apple, Mac)"
    assert device_str(parsed_user_agents[2]) == "Samsung SM-G973F(Samsung, SM-G973F)"
    assert device_str(parsed_user_agents[3]) == "iPhone(Apple, iPhone)"
    assert device_str(parsed_user_agents[4]) == "HTC Sensation(HTC, Sensation)"
    assert device_str(parsed_user_agents[5]) == "PlayStation 4(Sony, PlayStation 4)"


def test_os_str():
    parsed_user_agents = [
        parse(user_agent)
        for user_agent in [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
        ]
    ]
    assert os_str(parsed_user_agents[0]) == "Windows(10)"
    assert os_str(parsed_user_agents[1]) == "Mac OS X(10.15.7)"
    assert os_str(parsed_user_agents[2]) == "Android(10)"
    assert os_str(parsed_user_agents[3]) == "iOS(14.0)"
    assert os_str(parsed_user_agents[4]) == "Android(4.0.3)"
    assert os_str(parsed_user_agents[5]) is None


def test_browser_str():
    parsed_user_agents = [
        parse(user_agent)
        for user_agent in [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
        ]
    ]
    assert browser_str(parsed_user_agents[0]) == "Chrome(86.0.4240.75)"
    assert browser_str(parsed_user_agents[1]) == "Safari(14.0)"
    assert browser_str(parsed_user_agents[2]) == "Chrome Mobile(86.0.4240.75)"
    assert browser_str(parsed_user_agents[3]) == "Mobile Safari(14.0)"
    assert browser_str(parsed_user_agents[4]) is None


######################
# utils.get_log_data #
######################


def test_normal_case(mock_get_request, mock_ok_response):
    data = get_log_data(
        1742645740.731122,
        mock_get_request,
        mock_ok_response,
    )

    assert data["method"] == "GET"
    assert data["path"] == "/api/v1/test/"
    assert (
        data["user_agent"] == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/132.0.0.0 Whale/4.30.291.11 Safari/537.36"
    )
    assert data["querystring"] == "param1=value1&param2=value2"
    assert data["timestamp"] == datetime.fromtimestamp(1742645740.731122)
    assert data["server_ip"] == "testserver"
    assert data["client_ip"] == "127.0.0.1"
    assert data["status_code"] == HTTPStatus.OK


def test_empty_user_agent(mock_get_request_without_user_agent, mock_ok_response):
    data = get_log_data(
        1742645740.731122,
        mock_get_request_without_user_agent,
        mock_ok_response,
    )
    assert data["user_agent"] is None
    assert data["device"] is None
    assert data["os"] is None
    assert data["browser"] is None
