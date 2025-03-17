import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry
from functools import wraps


def time_it(func):
    """
    Декоратор для измерения времени выполнения
    Пример использования: @time_it
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} выполнилась за {end - start:.2f} секунд")
        return result
    return wrapper


# С использованием библиотеки
def retry_if_exception(exception):
    """
    Повторяем попытку, если произошла ошибка активации
    Пример использования: @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_exception=retry_if_exception)
    """

    return isinstance(exception, AssertionError)

# Самописный, такой же как retry_if_exception
def retry_on_exception(max_attempts=5, delay=1):
    """
    Декоратор для повторных попыток выполнения функции при исключениях
    Пример использования: @retry_on_exception(max_attempts=5, delay=1)

    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Попытка {attempt} из {max_attempts}")
                    return function(*args, **kwargs)
                except AssertionError as e:
                    print(f"Ошибка: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator





def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(function):
    def wraper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток активационного токена!")
            if token:
                return token
            time.sleep(1)


    return wraper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog


    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(json_data={'login': login, 'password': password})
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)


    def client_token(self, login: str, password: str):
        # Авторизация пользователя и получение токена
        response = self.user_login(login=login, password=password)
        assert response.status_code == 200, f"Не удалось сбросить пароль. Ответ: {response.text}"
        # Получение токена из ответа
        token = response.headers.get("x-dm-auth-token")
        assert token, "Токен авторизации не был получен после входа в систему"
        # Устанавливаем токен в заголовки
        response = self.dm_account_api.account_api.get_v1_account(headers={"X-Dm-Auth-Token": token})
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        # Получаем данные аккаунта
        response = self.dm_account_api.account_api.get_v1_account()
        assert response.status_code == 200
        json_data = response.json()
        assert "login" in json_data["resource"]
        assert json_data["resource"]["login"] == login


    def post_password(self, login: str, email: str, password: str):
        # Авторизация пользователя и получение токена
        response = self.user_login(login=login, password=password)
        assert response.status_code == 200, f"Не удалось сбросить пароль. Ответ: {response.text}"
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.login_api.set_headers(token)

        # Сбрасываем пароль
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f"Не удалось поменять пароль. Ответ: {response.text}"
        return response

    def change_password(self, login: str, old_password: str, new_password: str, token: str = None):
        if not token:
            token = self.get_token_by_password(login=login)
            assert token is not None, f"Токен для пользователя {login} не был получен"
        json_data = {
            'login': login,
            'token': token,
            'oldPassword': old_password,
            'newPassword': new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        assert response.status_code == 200, 'Пароль не поменялся'
        return response

    def delete_user(self, login: str, password: str):
        # Авторизация пользователя и получение токена
        response = self.user_login(login=login, password=password)
        assert response.status_code == 200, f"'Пользователь не смог авторизоваться'. Ответ: {response.text}"
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.login_api.set_headers(token)
        # Разлогин пользователя
        response = self.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, f"Не удалось разлогиниться. Ответ: {response.text}"
        # Разлогин пользователя
        return response

    def delete_all_user(self, login: str, password: str):
        # Авторизация пользователя и получение токена
        response = self.user_login(login=login, password=password)
        assert response.status_code == 200, f"'Пользователь не смог авторизоваться'. Ответ: {response.text}"
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.login_api.set_headers(token)
        # Разлогин пользователя
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, f"Не удалось разлогиниться. Ответ: {response.text}"
        # Разлогин пользователя
        return response


    def register_new_user(self, login: str, password: str, email: str):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь не был активирован'
        return response


    def user_login(self, login: str, password: str, rememder_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': rememder_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)

        assert response.status_code == 200, 'Пользователь не смог авторизоваться'
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_by_password(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            print(item)
            user_data = loads(item['Content']['Body'])
            print(f"Письмо: {user_data}")
            user_login = user_data['Login']
            if user_login == login:
                token = user_data.get('ConfirmationLinkUri')
                if token:
                    token = token.split('/')[-1]
                    break
                else:
                    print(f"ConfirmationLinkUri не найден в письме для пользователя {login}")
        if token is None:
            print(f"Токен не найден для пользователя {login}")

        return token
