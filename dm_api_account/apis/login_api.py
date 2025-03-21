import requests

from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, **kwargs):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(path=f"/v1/account/login", **kwargs)
        return response
