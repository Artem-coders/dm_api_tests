import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тест на проверку попытки авторизации нового пользователя без активации email")
class TestsPutV1AccountEmail:


    @allure.title("Попытка авторизации нового пользователя без активации email")
    def test_change_email1(self, prepare_user, account_helper):
        with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
            login = prepare_user.login
            password = prepare_user.password
            email = prepare_user.email
            account_helper.register_new_user_without_token_activation(login=login, password=password, email=email)
            account_helper.user_login(
                login=login, password=password, validate_response=True
            )
