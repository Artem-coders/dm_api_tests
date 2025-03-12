import requests

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