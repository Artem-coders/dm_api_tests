import allure

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

@allure.suite("Тесты на проверку метода POST /v1/account")
class TestsPostV1Account:


    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(
            login=login, password=password, validate_response=True
        )

        PostV1Account.check_response_values(response)



    @allure.title("Проверка регистрации нового пользователя c некорректным логином")
    def test_post_v1_account_negative_check_login(self, account_helper):
        with check_status_code_http(400, "Validation failed"):
            login = 'B'
            password = '123456789'
            email = "Good@mail.ru"
            account_helper.register_new_user(login=login, password=password, email=email)

    @allure.title("Проверка регистрации нового пользователя c некорректным паролем")
    def test_post_v1_account_negative_check_password(self, account_helper):
        with check_status_code_http(400, "Validation failed"):
            login = 'Bad1234567810'
            password = '12345'
            email = "Bad1234567810@mail.ru"
            account_helper.register_new_user(login=login, password=password, email=email)

    @allure.title("Проверка регистрации нового пользователя c некорректным email")
    def test_post_v1_account_negative_check_email(self, account_helper):
        with check_status_code_http(400, "Validation failed"):
            login = 'Bad987654'
            password = '123456789'
            email = "Bad987654mail.ru"
            account_helper.register_new_user(login=login, password=password, email=email)

    @allure.title("Проверка регистрации нового пользователя c некорректными данными: логин, пароль, email")
    def test_post_v1_account_negative_check_login_password_email(self, account_helper):
        with check_status_code_http(400, "Validation failed"):
            login = 'B'
            password = '12345'
            email = "Bsdskmail.ru"
            account_helper.register_new_user(login=login, password=password, email=email)