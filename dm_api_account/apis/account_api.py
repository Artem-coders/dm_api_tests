import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, **kwargs):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(path=f'/v1/account', **kwargs)
        return response


    def put_v1_account_token(self, token, **kwargs):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(path=f'/v1/account/{token}', **kwargs)
        return response
