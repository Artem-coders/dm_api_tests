from json import loads
import pytest
from api_class_client.class_client import ApiClient
from conftest import *
from api_mailhog.apis.mailhog_api import MailhogApi


def test_create_user(login_data):
    """Создание пользователя с логином, передаваемым через фикстуру."""
    api_client = ApiClient(host='http://5.63.153.31:5051')

    response = api_client.post_v1_account(json_data={
        'login': login_data['login'],
        'email': login_data['email'],
        'password': login_data['password'],
    })

    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, 'Пользователь не был создан'


def test_activate_user(login_data):
    """Активация пользователя с логином из фикстуры."""
    api_client = ApiClient(host='http://5.63.153.31:5025')
    api_client_login = ApiClient(host='http://5.63.153.31:5051')

    # Получить письма из почтового сервера
    response = api_client.get_api_v2_messages()
    print(f"Status Code для получения писем: {response.status_code}")
    print(f"Ответ на запрос: {response.text}")
    assert response.status_code == 200, 'Письма не были получены'

    # Получить активационный токен
    token = get_activation_token_by_login(login_data['login'], response)
    print(f"Получен токен: {token}")
    assert token is not None, f"Токен для пользователя {login_data['login']} не был получен"

    # Активация пользователя
    response = api_client_login.put_v1_account_token(token=token)
    print(f"Status Code для активации: {response.status_code}")
    print(f"Ответ на запрос активации: {response.text}")

    assert response.status_code == 200, f"Пользователь не был активирован. Статус: {response.status_code}"



def test_user_login(login_data):
    """Авторизация пользователя с логином из фикстуры."""
    api_client = ApiClient(host='http://5.63.153.31:5051')

    response = api_client.post_v1_account_login(json_data={
        'login': login_data['login'],
        'password': login_data['password'],
        'rememberMe': True,
    })

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не смог авторизоваться'


def get_activation_token_by_login(login, response):
    token = None
    if 'items' not in response.json():
        raise ValueError(f'❌ Не найдено ни одного письма для пользователя {login}')

    for item in response.json()['items']:
        body = item['Content']['Body']
        print(f"Тело письма: {body}")

        # Пытаемся распарсить тело как JSON, но если не получится — ищем вручную
        try:
            user_data = loads(body)
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        except ValueError:
            # Письмо не в формате JSON — ищем ссылку вручную
            for line in body.splitlines():
                if 'ConfirmationLinkUrl' in line:
                    token = line.split('/')[-1].strip()
                    break

    if not token:
        raise ValueError(f'❌ Не удалось найти токен активации для пользователя {login}')

    return token



