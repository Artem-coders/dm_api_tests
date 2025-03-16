# Авторизованный клиент
def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()

# Не авторизованный клиент
def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()


# Задание 2.1 в файле get_v1_account.py
# - Получить информацию о пользователе (используя авторизованный клиент)
def test_get_v1_account_with_token(account_helper_get_token):
    token = "IQJh+zgzF5CpXuV4YvhMOINFI9f/7tw9zC5gv171Ib/0sf4Pd6CNH1fcw6SjiuvEqSQLO+au44Xm3IUIdrkZ6Cf9jxi7N7BLdUt4a43X8eiQCxjLwXUniEA7RU5aARIkHWIKwObFd7c="

    account_helper_get_token.client_token(token)
    response = account_helper_get_token.dm_account_api.account_api.get_v1_account()

    assert response.status_code == 200
    json_data = response.json()
    assert "login" in json_data["resource"]
    assert json_data["resource"]["login"] == "Good_15_03_2025_22_21%S"