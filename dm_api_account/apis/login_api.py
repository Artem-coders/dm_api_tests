import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):


    @allure.step("Авторизуем пользователя")
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

    @allure.step("Разлогин пользователя")
    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :return:
        """
        response = self.delete(path=f'/v1/account/login', **kwargs)
        return response

    @allure.step("Разлогин пользователя на всех устройствах")
    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :return:
        """
        response = self.delete(path=f'/v1/account/login/all', **kwargs, validate_response=True)
        return response