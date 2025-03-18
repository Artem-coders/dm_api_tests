# Авторизованный клиент
def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    print(response)

# Не авторизованный клиент
def test_get_v1_account_no_auth(account_helper):
    response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    print(response)


def test_get_v1_account_with_token(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    # Получение информации о пользователе
    account_helper.client_token(login=login, password=password)
