import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from dm_api_account.models.user_must_be_authenticated import UserMustBeAuthenticated
from restclient.client import RestClient


class LoginApi(RestClient):



    def post_v1_account_login(self, login_credentials: LoginCredentials, validate_response=True):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(path=f'/v1/account/login',
                             json=login_credentials.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def delete_v1_account_login(self, validate_response=True, **kwargs):
        """
        Logout as current user
        :return:
        """
        response = self.delete(path=f'/v1/account/login', **kwargs)
        if validate_response:
            return UserMustBeAuthenticated(**response.json())
        return response


    def delete_v1_account_login_all(self, validate_response=True, **kwargs):
        """
        Logout from every device
        :return:
        """
        response = self.delete(path=f'/v1/account/login/all', **kwargs, validate_response=True)
        if validate_response:
            return UserMustBeAuthenticated(**response.json())
        return response