import allure


@allure.suite("Тест на проверку метода по смене пароля")
class TestsPutV1AccountPassword:

    @allure.title("Меняем пароль пользователя")
    def test_put_v1_account_password(self, account_helper, prepare_user, prepare_password):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        old_password = password
        new_password = prepare_password.password
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        x_dm_auth_token = response.headers.get("x-dm-auth-token")
        account_helper.change_password(
            login=login,
            old_password=old_password,
            new_password=new_password,
            email=email,
            x_dm_auth_token=x_dm_auth_token,
        )
        account_helper.user_login(login=login, password=new_password)
