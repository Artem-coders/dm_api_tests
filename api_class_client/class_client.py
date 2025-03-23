from json import loads

import requests


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        body = item['Content']['Body']

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

class ApiClient:
    """Клиент для работы с API сервера."""

    def __init__(self, host, headers=None):
        self.host = host
        self.email = headers

    def post_v1_account(self, json_data):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(url=f'{self.host}/v1/account', json=json_data)
        return response

    def put_v1_account_token(self, token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = requests.put(url=f'{self.host}/v1/account/{token}', headers=headers)
        return response

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(url=f'{self.host}/v1/account/login', json=json_data)
        return response


    def get_api_v2_messages(self, limit=50):
        """
        Get Users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = requests.get(url=f'{self.host}/api/v2/messages', params=params, verify=False)
        return response