import requests

from dm_api_account.models.get_user import GetUser
from dm_api_account.models.login_credentials import LoginCredentials
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


    def get_v1_account(self, validate_response=True, **kwargs):
        """
        Get current user
        :return:
        """
        response = self.get(path=f'/v1/account', **kwargs)
        if validate_response:
            return GetUser(**response.json())
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


    def put_v1_account_password(self, json_data, validate_response=True):
        """
        Change registered user password
        :return:
        """
        response = self.put(path=f'/v1/account/password', json=json_data)
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def post_v1_account_password(self, json_data, validate_response=True):
        """
        Reset registered user password
        :return:
        """
        response = self.post(path=f'/v1/account/password', json=json_data)
        if validate_response:
            response_data = response.json()
            # Eсли metadata — это словарь, извлекаем нужное поле
            if isinstance(response_data.get('metadata'), dict):
                response_data['metadata'] = response_data['metadata'].get('email', '')
            return UserEnvelope(**response_data)
        return response
