import allure
from assertpy import assert_that, soft_assertions

@allure.suite("Тест на проверку активированного пользователя")
class TestLoginUser:


    @allure.title("Проверка входа активированного пользователя")
    def test_get_v1_account_auth1(self, account_helper, login='Siberaia1', password='123456789'):
        response = account_helper.user_login(
            login=login, password=password, validate_response=True
        )
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to("Siberaia1")
