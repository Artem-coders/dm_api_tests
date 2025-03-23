import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
    expected_status_code: requests.status_codes = requests.codes.OK,
    expected_message: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение '{expected_message}', но запрос пришёл успешно"
            )
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()["title"] == expected_message



@contextmanager
def check_negative_login_http(
        expected_status_code: requests.status_codes = requests.codes.OK,
        expected_message: str = "",
        expected_login_error: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение '{expected_message}', но запрос пришёл успешно"
            )
        if expected_login_error:
            raise AssertionError(
                f"Должно быть в errors: Login: '{expected_login_error}', но запрос пришёл успешно"
            )
    except HTTPError as e:
        response_json = e.response.json()
        assert e.response.status_code == expected_status_code
        assert response_json["title"] == expected_message
        if expected_login_error:
            assert "Login" in response_json["errors"], f"Отсутствует ошибка для поля 'Login'"
            assert expected_login_error in response_json["errors"]["Login"], f"Ожидаемая ошибка '{expected_login_error}' не найдена для поля 'Login'"


@contextmanager
def check_negative_password_http(
        expected_status_code: requests.status_codes = requests.codes.OK,
        expected_message: str = "",
        expected_password_error: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение '{expected_message}', но запрос пришёл успешно"
            )
        if expected_password_error:
            raise AssertionError(
                f"Должно быть в errors: Password: '{expected_password_error}', но запрос пришёл успешно"
            )
    except HTTPError as e:
        response_json = e.response.json()
        assert e.response.status_code == expected_status_code
        assert response_json["title"] == expected_message
        if expected_password_error:
            assert "Password" in response_json["errors"], f"Отсутствует ошибка для поля 'Password'"
            assert expected_password_error in response_json["errors"]["Password"], f"Ожидаемая ошибка '{expected_password_error}' не найдена для поля 'Password'"

@contextmanager
def check_negative_email_http(
        expected_status_code: requests.status_codes = requests.codes.OK,
        expected_message: str = "",
        expected_email_error: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение '{expected_message}', но запрос пришёл успешно"
            )
        if expected_email_error:
            raise AssertionError(
                f"Должно быть в errors: Email: '{expected_email_error}', но запрос пришёл успешно"
            )
    except HTTPError as e:
        response_json = e.response.json()
        assert e.response.status_code == expected_status_code
        assert response_json["title"] == expected_message
        if expected_email_error:
            assert "Email" in response_json["errors"], f"Отсутствует ошибка для поля 'Email'"
            assert expected_email_error in response_json["errors"]["Email"], f"Ожидаемая ошибка '{expected_email_error}' не найдена для поля 'Email'"

@contextmanager
def check_negative_login_password_email_http(
        expected_status_code: requests.status_codes = requests.codes.OK,
        expected_message: str = "",
        expected_login_error: str = "",
        expected_password_error: str = "",
        expected_email_error: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение '{expected_message}', но запрос пришёл успешно"
            )
        if expected_login_error:
            raise AssertionError(
                f"Должно быть в errors: Login: '{expected_login_error}', но запрос пришёл успешно"
            )
        if expected_password_error:
            raise AssertionError(
                f"Должно быть в errors: Password: '{expected_password_error}', но запрос пришёл успешно"
            )
        if expected_email_error:
            raise AssertionError(
                f"Должно быть в errors: Email: '{expected_email_error}', но запрос пришёл успешно"
            )

    except HTTPError as e:
        response_json = e.response.json()
        assert e.response.status_code == expected_status_code
        assert response_json["title"] == expected_message
        if expected_login_error:
            assert "Login" in response_json["errors"], f"Отсутствует ошибка для поля 'Login'"
            assert expected_login_error in response_json["errors"]["Login"], f"Ожидаемая ошибка '{expected_login_error}' не найдена для поля 'Login'"
        if expected_password_error:
            assert "Password" in response_json["errors"], f"Отсутствует ошибка для поля 'Password'"
            assert expected_password_error in response_json["errors"]["Password"], f"Ожидаемая ошибка '{expected_password_error}' не найдена для поля 'Password'"
        if expected_email_error:
            assert "Email" in response_json["errors"], f"Отсутствует ошибка для поля 'Email'"
            assert expected_email_error in response_json["errors"]["Email"], f"Ожидаемая ошибка '{expected_email_error}' не найдена для поля 'Email'"