import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from assertpy import assert_that, soft_assertions
from dm_api_account.models.user_envelope import UserRole

@allure.suite("Тесты на проверку метода get_v1_account")
class TestGetV1Account:

    @allure.title("Проверка активированного пользователя")
    def test_get_v1_account_auth(self, auth_account_helper):
            response = auth_account_helper.dm_account_api.account_api.get_v1_account(
                validate_response=True
            )
            GetV1Account.check_response_value_get_v1_account(response, expected_login="Good")
            with soft_assertions():
                assert_that(response.resource.login).is_equal_to("Good_15_03_2025_22_21%S")
                assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)


    @allure.title("Проверка не активированного пользователя")
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, "User must be authenticated"):
            account_helper.dm_account_api.account_api.get_v1_account(
                validate_response=False
            )
