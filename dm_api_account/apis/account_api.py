import requests

from dm_api_account.models.registration import Registration
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        Register new user
        :return:
        exlude_none: если поле необязательно, то не будем передавать
        """
        response = self.post(path=f'/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        return response


    def get_v1_account(self, **kwargs):
        """
        Get current user
        :return:
        """
        response = self.get(path=f'/v1/account', **kwargs)
        return response


    def put_v1_account_token(self, token, validate_response=True):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(path=f'/v1/account/{token}', headers=headers)
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def put_v1_account_password(self, json_data):
        """
        Change registered user password
        :return:
        """
        response = self.put(path=f'/v1/account/password', json=json_data)
        return response


    def post_v1_account_password(self, json_data):
        """
        Reset registered user password
        :return:
        """
        response = self.post(path=f'/v1/account/password', json=json_data)
        return response