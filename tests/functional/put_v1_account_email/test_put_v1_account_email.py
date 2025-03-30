import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тест на проверку авторизации нового пользователя с новым email")
class TestsPutV1AccountEmail:

    @allure.title("Меняем email пользователя и выполняем авторизацию")
    def test_put_v1_account_email(self, account_helper, prepare_user, prepare_email):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = prepare_email.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        x_dm_auth_token = response.headers.get("x-dm-auth-token")
        account_helper.change_email(
            login=login,
            password=password,
            new_email=new_email,
            x_dm_auth_token=x_dm_auth_token,
        )
        with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
            account_helper.user_login(login=login, password=password)

        token = account_helper.get_activation_token_by_login(login=login)
        account_helper.dm_account_api.account_api.put_v1_account_token(
            token=token, validate_response=True
        )
        account_helper.user_login(login=login, password=password)
