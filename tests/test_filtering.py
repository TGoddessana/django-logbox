from unittest.mock import MagicMock, patch

from django.http import HttpRequest, HttpResponse

from django_logbox.app_settings import settings
from django_logbox.filtering import LogboxLogFilter


class TestLogboxLogFilter:
    def test_should_filter_log_with_already_logged_request(self):
        request = MagicMock(spec=HttpRequest)
        request.logbox_logged = True
        response = MagicMock(spec=HttpResponse)

        result = LogboxLogFilter.should_filter_log(request, response)

        assert result is True

    @patch.object(LogboxLogFilter, "should_log_request", return_value=False)
    def test_should_filter_log_with_request_to_filter(self, mock_should_log_request):
        request = MagicMock(spec=HttpRequest)
        response = MagicMock(spec=HttpResponse)

        result = LogboxLogFilter.should_filter_log(request, response)

        assert result is True
        mock_should_log_request.assert_called_once_with(request=request)

    @patch.object(LogboxLogFilter, "should_log_request", return_value=True)
    @patch.object(LogboxLogFilter, "should_log_response", return_value=False)
    def test_should_filter_log_with_response_to_filter(
        self, mock_should_log_response, mock_should_log_request
    ):
        request = MagicMock(spec=HttpRequest)
        response = MagicMock(spec=HttpResponse)

        result = LogboxLogFilter.should_filter_log(request, response)

        assert result is True
        mock_should_log_request.assert_called_once_with(request=request)
        mock_should_log_response.assert_called_once_with(response=response)

    @patch.object(LogboxLogFilter, "should_log_request", return_value=True)
    @patch.object(LogboxLogFilter, "should_log_response", return_value=True)
    def test_should_filter_log_with_request_and_response_to_log(
        self, mock_should_log_response, mock_should_log_request
    ):
        request = MagicMock(spec=HttpRequest)
        response = MagicMock(spec=HttpResponse)

        result = LogboxLogFilter.should_filter_log(request, response)

        assert result is False
        mock_should_log_request.assert_called_once_with(request=request)
        mock_should_log_response.assert_called_once_with(response=response)

    @patch("django_logbox.filtering.get_client_ip", return_value="127.0.0.1")
    @patch("django_logbox.filtering.get_server_ip", return_value="127.0.0.1")
    @patch.object(LogboxLogFilter, "is_client_ip_allowed", return_value=True)
    @patch.object(LogboxLogFilter, "is_server_ip_allowed", return_value=True)
    @patch.object(LogboxLogFilter, "is_path_allowed", return_value=True)
    def test_should_log_request_when_all_conditions_are_met(
        self,
        mock_is_path_allowed,
        mock_is_server_ip_allowed,
        mock_is_client_ip_allowed,
        mock_get_server_ip,
        mock_get_client_ip,
    ):
        request = MagicMock(spec=HttpRequest)
        request.path = "/api/test"

        result = LogboxLogFilter.should_log_request(request)

        assert result is True
        mock_get_client_ip.assert_called_once_with(request=request)
        mock_get_server_ip.assert_called_once_with(request=request)
        mock_is_client_ip_allowed.assert_called_once_with(client_ip="127.0.0.1")
        mock_is_server_ip_allowed.assert_called_once_with(server_ip="127.0.0.1")
        mock_is_path_allowed.assert_called_once_with(request_path="/api/test")

    @patch("django_logbox.filtering.get_client_ip", return_value="127.0.0.1")
    @patch("django_logbox.filtering.get_server_ip", return_value="127.0.0.1")
    @patch.object(LogboxLogFilter, "is_client_ip_allowed", return_value=False)
    def test_should_log_request_when_client_ip_not_allowed(
        self, mock_is_client_ip_allowed, mock_get_server_ip, mock_get_client_ip
    ):
        request = MagicMock(spec=HttpRequest)

        result = LogboxLogFilter.should_log_request(request)

        assert result is False
        mock_get_client_ip.assert_called_once_with(request=request)
        mock_is_client_ip_allowed.assert_called_once_with(client_ip="127.0.0.1")

    def test_is_method_allowed(self):
        with patch.object(
            settings, "LOGBOX_SETTINGS", {"LOGGING_HTTP_METHODS": ["GET", "POST"]}
        ):
            assert LogboxLogFilter.is_method_allowed("GET") is True
            assert LogboxLogFilter.is_method_allowed("POST") is True
            assert LogboxLogFilter.is_method_allowed("DELETE") is False

    def test_is_client_ip_allowed(self):
        with patch.object(
            settings,
            "LOGBOX_SETTINGS",
            {"LOGGING_CLIENT_IPS_TO_EXCLUDE": ["192.168.1.1"]},
        ):
            assert LogboxLogFilter.is_client_ip_allowed("127.0.0.1") is True
            assert LogboxLogFilter.is_client_ip_allowed("192.168.1.1") is False

    def test_is_server_ip_allowed(self):
        with patch.object(
            settings, "LOGBOX_SETTINGS", {"LOGGING_SERVER_IPS_TO_EXCLUDE": ["10.0.0.1"]}
        ):
            assert LogboxLogFilter.is_server_ip_allowed("127.0.0.1") is True
            assert LogboxLogFilter.is_server_ip_allowed("10.0.0.1") is False

    def test_is_path_allowed(self):
        with patch.object(
            settings,
            "LOGBOX_SETTINGS",
            {"LOGGING_PATHS_TO_EXCLUDE": [r"^/admin/", r"^/static/"]},
        ):
            assert LogboxLogFilter.is_path_allowed("/api/test") is True
            assert LogboxLogFilter.is_path_allowed("/admin/login") is False
            assert LogboxLogFilter.is_path_allowed("/static/css/main.css") is False

    def test_should_log_response(self):
        with patch.object(
            settings, "LOGBOX_SETTINGS", {"LOGGING_STATUS_CODES": [200, 404]}
        ):
            response_200 = MagicMock(spec=HttpResponse)
            response_200.status_code = 200
            response_404 = MagicMock(spec=HttpResponse)
            response_404.status_code = 404
            response_500 = MagicMock(spec=HttpResponse)
            response_500.status_code = 500

            assert LogboxLogFilter.should_log_response(response_200) is True
            assert LogboxLogFilter.should_log_response(response_404) is True
            assert LogboxLogFilter.should_log_response(response_500) is False
